#!/usr/bin/env python3
"""
OpenCode Ultimate — Orquestador de agentes.
Uso: python orchestrate.py --agent <id> --task "<tarea>"
      python orchestrate.py --detect "<tarea>"  (auto-detecta el mejor agente)
"""
import json
import os
import sys
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "Scripts"))

from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

from providers.ollama_provider import OllamaProvider
from providers.openai_provider import OpenAIProvider
from providers.gemini_provider import GeminiProvider

PROVIDER_CLASSES = {
    "ollama": OllamaProvider,
    "groq": OpenAIProvider,
    "deepseek": OpenAIProvider,
    "openrouter": OpenAIProvider,
    "kimi": OpenAIProvider,
    "qwen": OpenAIProvider,
    "gemini": GeminiProvider,
}

AGENTS_FILE = BASE_DIR / "AI" / "Config" / "agents.json"
PROVIDERS_FILE = BASE_DIR / "AI" / "Config" / "providers.json"
BUDGET_FILE = BASE_DIR / "AI" / "Memory" / "token_budget.json"
PENDING_DIR = BASE_DIR / "AI" / "Memory" / "pending"
PENDING_RESULTS_DIR = PENDING_DIR / "results"
PENDING_CHECKPOINT = PENDING_DIR / "checkpoint.json"


def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_agents():
    data = load_json(AGENTS_FILE)
    return data.get("agents", [])


def get_agent(agent_id):
    for a in get_agents():
        if a["id"] == agent_id:
            return a
    return None


def get_providers():
    return load_json(PROVIDERS_FILE)


def get_budget():
    default = {
        "groq": {"budget": 1000000, "used": 0, "unit": "tokens/dia"},
        "deepseek": {"budget": 500000, "used": 0, "unit": "tokens"},
        "gemini": {"budget": 1500, "used": 0, "unit": "requests/dia"},
        "ollama": {"budget": -1, "used": 0, "unit": "ilimitado"},
        "kimi": {"budget": 500000, "used": 0, "unit": "tokens"},
        "openrouter": {"budget": 100000, "used": 0, "unit": "tokens"},
        "qwen": {"budget": 500000, "used": 0, "unit": "tokens"},
    }
    if BUDGET_FILE.exists():
        data = json.loads(BUDGET_FILE.read_text(encoding="utf-8"))
        for k, v in default.items():
            if k not in data:
                data[k] = v
        return data
    return default


def save_budget(budget):
    BUDGET_FILE.write_text(json.dumps(budget, indent=2), encoding="utf-8")


def has_budget(provider_name):
    budget = get_budget()
    p = budget.get(provider_name, {})
    if p.get("budget", -1) == -1:
        return True
    return p.get("used", 0) < p.get("budget", 0)


def mark_used(provider_name, tokens=1):
    budget = get_budget()
    if provider_name in budget:
        budget[provider_name]["used"] = budget[provider_name].get("used", 0) + tokens
        save_budget(budget)


def detect_agent(task, no_local=False):
    task_lower = task.lower()
    agents = get_agents()
    scores = []

    keywords_map = {
        "arquitecto": ["arquitectur", "base de datos", "diseñar", "planificar", "estructura", "schema", "tabla", "api rest", "microservicio"],
        "desarrollador": ["bug", "error", "debug", "implementar", "codigo", "funcion", "clase", "test", "refactor"],
        "documentador": ["documentar", "readme", "changelog", "manual", "guia", "explicar", "resumir"],
        "groq-mixtral": ["razonar", "analizar", "comparar", "evaluar", "complejo", "decision"],
        "deepseek-coder": ["script", "algoritmo", "optimizar", "rendimiento", "complejidad", "codigo avanzado"],
        "kimi-128k": ["documento largo", "archivo grande", "analiza este archivo", "contexto largo", "procesar"],
        "gemini-flash": ["rapido", "simple", "cotidiano", "general", "traducir"],
        "qwen-coder": ["programar", "codigo", "desarrollar", "implementar", "funcion", "clase"],
        "chat": ["hola", "buenos dias", "buenas tardes", "como estas", "que tal", "charla", "conversacion", "pregunta", "quien", "cuando", "donde", "por que", "cual", "dimelo", "cuentame", "opinion"],
    }

    for agent in agents:
        if no_local and agent["provider"] == "ollama":
            continue
        score = 0
        keywords = keywords_map.get(agent["id"], [])
        for kw in keywords:
            if kw in task_lower:
                score += 2
        if has_budget(agent["provider"]):
            score += 1
        else:
            score -= 3
        scores.append((score, agent))

    scores.sort(key=lambda x: x[0], reverse=True)
    if scores and scores[0][0] > 0:
        return scores[0][1]
    # fallback default: agente chat si existe
    chat_agent = get_agent("chat")
    if chat_agent and (not no_local or chat_agent["provider"] != "ollama"):
        return chat_agent
    return None


def run_agent(agent, task, system_prompt=""):
    provider_name = agent["provider"]
    provider_config = get_providers().get(provider_name, {})

    url_env = f"{provider_name.upper()}_API_URL"
    env_url = os.getenv(url_env)
    if env_url:
        provider_config["api_url"] = env_url

    provider_config["model"] = agent["model"]

    cls = PROVIDER_CLASSES.get(provider_name)
    if not cls:
        return f"Error: No provider class for: {provider_name}"

    provider = cls(provider_config)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": task})

    try:
        result = provider.chat(messages, agent.get("temperature", 0.3))
        mark_used(provider_name, tokens=len(task) // 4 + 100)
        return result
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


def try_with_fallback(agent, task, system_prompt, max_attempts=5, no_local=False):
    seen = set()
    queue = [agent]
    while queue and len(seen) < max_attempts:
        current = queue.pop(0)
        if current["id"] in seen:
            continue
        seen.add(current["id"])

        if not has_budget(current["provider"]):
            print(f"[{current['provider']} sin saldo, buscando alternativa...]")
            alt = find_alternative(current, no_local)
            if alt:
                queue.append(alt)
            continue

        result = run_agent(current, task, system_prompt)
        if not result.startswith("Error"):
            return result, current

        print(f"[{current['name']} fallo: {result[:80]}...]")
        alt = find_alternative(current, no_local)
        if alt:
            queue.append(alt)

    if no_local:
        return "Todos los cloud sin saldo o fallaron. Configura más API keys o reduce consumo.", agent
    return "No se pudo completar la tarea con los agentes disponibles.", agent


def save_checkpoint(task_id, agent_id, task):
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "task": task,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }
    PENDING_CHECKPOINT.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_result(task_id, agent_id, task, result, status="completed"):
    PENDING_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": status,
        "task": task,
        "result": result,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }
    path = PENDING_RESULTS_DIR / f"{task_id}_{agent_id}.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    if PENDING_CHECKPOINT.exists():
        PENDING_CHECKPOINT.unlink()


def main():
    import argparse, uuid
    parser = argparse.ArgumentParser(description="OpenCode Ultimate - Orquestador")
    parser.add_argument("--agent", help="ID del agente a usar")
    parser.add_argument("--task", default="", help="Tarea a ejecutar")
    parser.add_argument("--system", default="", help="System prompt opcional")
    parser.add_argument("--detect", action="store_true", help="Auto-detectar el mejor agente")
    parser.add_argument("--task-id", default="", help="ID único para tracking de resultados")
    parser.add_argument("--cleanup-pending", action="store_true", help="Limpiar resultados pendientes")
    parser.add_argument("--status-pending", action="store_true", help="Ver estado de pendientes")
    parser.add_argument("--always", action="store_true", help="Enrutar toda interacción al orquestador (modo siempre-delegar)")
    parser.add_argument("--no-local", action="store_true", help="Excluir Ollama de la selección y fallback")
    args = parser.parse_args()

    if args.always:
        if not args.task:
            print("Usa --task <mensaje> con --always")
            sys.exit(1)
        if not args.task_id:
            ts = __import__("datetime").datetime.now().strftime("%y%m%d-%H%M%S")
            uid = uuid.uuid4().hex[:6]
            args.task_id = f"{ts}-{uid}"
        if not args.agent:
            args.detect = True
        args.no_local = True

    if args.cleanup_pending:
        import shutil
        if PENDING_RESULTS_DIR.exists():
            shutil.rmtree(PENDING_RESULTS_DIR)
            PENDING_RESULTS_DIR.mkdir(parents=True)
        if PENDING_CHECKPOINT.exists():
            PENDING_CHECKPOINT.unlink()
        print("Pendientes limpiados.")
        return

    if args.status_pending:
        pendientes = list(PENDING_RESULTS_DIR.glob("*.json")) if PENDING_RESULTS_DIR.exists() else []
        if pendientes:
            print(f"Resultados pendientes: {len(pendientes)}")
            for p in pendientes:
                data = json.loads(p.read_text(encoding="utf-8"))
                print(f"  - {data['task_id']} ({data['agent_id']}): {data['status']}")
        else:
            print("No hay resultados pendientes.")
        if PENDING_CHECKPOINT.exists():
            cp = json.loads(PENDING_CHECKPOINT.read_text(encoding="utf-8"))
            print(f"Checkpoint activo: {cp['task_id']} -> {cp['agent_id']}")
        return

    if not args.task and not args.cleanup_pending and not args.status_pending:
        print("Usa --task <tarea> o --status-pending o --cleanup-pending")
        sys.exit(1)

    if args.detect:
        agent = detect_agent(args.task, no_local=args.no_local)
        if not agent:
            print("No se detecto un agente adecuado. Usa --agent para elegir manualmente.")
            sys.exit(1)
    elif args.agent:
        agent = get_agent(args.agent)
        if not agent:
            print(f"Error: agente '{args.agent}' no encontrado")
            sys.exit(1)
    else:
        print("Usa --agent <id> o --detect")
        sys.exit(1)

    if args.always:
        print(f"[orquestador: {agent['name']}] ({agent['provider']}/{agent['model']})")
    else:
        print(f"[{agent['name']}] ({agent['provider']}/{agent['model']})")
    print("-" * 50)

    if args.task_id:
        save_checkpoint(args.task_id, agent["id"], args.task)

    try:
        result, used_agent = try_with_fallback(agent, args.task, args.system, no_local=args.no_local)
        if used_agent["id"] != agent["id"]:
            print(f"[Uso {used_agent['name']} como alternativa]")

        if args.task_id:
            is_error = result.startswith("Error") or result.startswith("No se pudo")
            save_result(args.task_id, used_agent["id"], args.task, result, "error" if is_error else "completed")

        safe = result.encode('ascii', errors='replace').decode('ascii')
        print(safe)
    except Exception as e:
        if args.task_id:
            save_result(args.task_id, agent["id"], args.task, f"Excepción: {e}", "error")
        print(f"Error crítico: {e}")


def find_alternative(agent, no_local=False):
    agents = get_agents()
    same_persona = [a for a in agents if a["persona"] == agent["persona"] and a["id"] != agent["id"]]
    for a in same_persona:
        if has_budget(a["provider"]) and (not no_local or a["provider"] != "ollama"):
            return a
    for a in agents:
        if has_budget(a["provider"]) and a["id"] != agent["id"] and (not no_local or a["provider"] != "ollama"):
            return a
    return None


if __name__ == "__main__":
    main()
