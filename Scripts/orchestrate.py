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


def detect_agent(task):
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
    }

    for agent in agents:
        score = 0
        keywords = keywords_map.get(agent["id"], [])
        for kw in keywords:
            if kw in task_lower:
                score += 2
        if agent["provider"] == "ollama":
            score += 0.5
        if has_budget(agent["provider"]):
            score += 1
        else:
            score -= 3
        scores.append((score, agent))

    scores.sort(key=lambda x: x[0], reverse=True)
    if scores and scores[0][0] > 0:
        return scores[0][1]
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
        return f"No provider class for: {provider_name}"

    provider = cls(provider_config)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": task})

    result = provider.chat(messages, agent.get("temperature", 0.3))
    mark_used(provider_name, tokens=len(task) // 4 + 100)
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="OpenCode Ultimate - Orquestador")
    parser.add_argument("--agent", help="ID del agente a usar")
    parser.add_argument("--task", required=True, help="Tarea a ejecutar")
    parser.add_argument("--system", default="", help="System prompt opcional")
    parser.add_argument("--detect", action="store_true", help="Auto-detectar el mejor agente")
    args = parser.parse_args()

    if args.detect:
        agent = detect_agent(args.task)
        if not agent:
            print("No se detecto un agente adecuado. Usa --agent para elegir manualmente.")
            sys.exit(1)
        print(f"🤖 Agente seleccionado: {agent.get('icon','')} {agent['name']} ({agent['provider']}/{agent['model']})")
        print("-" * 50)
    elif args.agent:
        agent = get_agent(args.agent)
        if not agent:
            print(f"Error: agente '{args.agent}' no encontrado")
            sys.exit(1)
    else:
        print("Usa --agent <id> o --detect")
        sys.exit(1)

    if not has_budget(agent["provider"]):
        print(f"⚠️  {agent['provider']} sin saldo disponible. Buscando alternativas...")
        alt = find_alternative(agent)
        if alt:
            print(f"➡️  Usando {alt['name']} como alternativa")
            agent = alt
        else:
            print("No hay alternativas disponibles.")
            sys.exit(1)

    result = run_agent(agent, args.task, args.system)
    print(result)


def find_alternative(agent):
    agents = get_agents()
    same_persona = [a for a in agents if a["persona"] == agent["persona"] and a["id"] != agent["id"]]
    for a in same_persona:
        if has_budget(a["provider"]):
            return a
    for a in agents:
        if has_budget(a["provider"]) and a["id"] != agent["id"]:
            return a
    return None


if __name__ == "__main__":
    main()
