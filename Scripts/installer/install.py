#!/usr/bin/env python3
"""
OpenCode Ultimate — Instalador
Instala el entorno completo desde cero.
"""
import os
import sys
import subprocess
import json
from pathlib import Path

REPO_URL = "https://github.com/Fipo08/playingwithIA.git"
REQUIRED_DIRS = [
    "AI/Memory", "AI/Personas", "AI/Prompts", "AI/Rules",
    "AI/Templates", "AI/Workflows", "AI/KnowledgeBase", "AI/Config",
    "Documentation", "Projects", "Scripts", "web",
]

OLLAMA_MODELS = ["qwen3:8b", "deepseek-r1:8b", "llama3.1:8b"]


def step(label, status, icon):
    print(f"{icon} [{status}] {label}")


def check_git():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10)
        step(f"Git: {result.stdout.strip()}", "OK", "✅")
        return True
    except Exception:
        step("Git no encontrado. Instálalo desde https://git-scm.com", "FAIL", "❌")
        return False


def check_python():
    try:
        result = subprocess.run(
            [sys.executable, "--version"], capture_output=True, text=True, timeout=10
        )
        step(f"Python: {result.stdout.strip()}", "OK", "✅")
        return True
    except Exception:
        step("Python no encontrado", "FAIL", "❌")
        return False


def check_ollama():
    try:
        result = subprocess.run(
            ["ollama", "--version"], capture_output=True, text=True, timeout=10
        )
        step(f"Ollama: {result.stdout.strip()}", "OK", "✅")
        return True
    except Exception:
        step("Ollama no encontrado. Descárgalo desde https://ollama.com", "FAIL", "❌")
        return False


def pull_ollama_models():
    for model in OLLAMA_MODELS:
        print(f"  Descargando {model}...")
        subprocess.run(["ollama", "pull", model], capture_output=True, timeout=600)
        step(f"Modelo {model} listo", "OK", "  ✅")


def clone_repo(target_dir):
    if Path(target_dir).exists():
        step(f"La carpeta {target_dir} ya existe", "WARN", "⚠️")
        return True

    result = subprocess.run(
        ["git", "clone", REPO_URL, target_dir],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode == 0:
        step(f"Repositorio clonado en {target_dir}", "OK", "✅")
        return True
    else:
        step(f"Error al clonar: {result.stderr.strip()}", "FAIL", "❌")
        return False


def create_user(target_dir, username):
    users_dir = Path(target_dir) / "AI" / "Memory" / "users"
    users_json = users_dir / "users.json"
    user_dir = users_dir / username

    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / "sessions").mkdir(exist_ok=True)

    for f in ["perfil.md", "preferencias.md", "proyectos.md"]:
        path = user_dir / f
        if not path.exists():
            path.write_text(f"# {f.replace('.md', '').capitalize()}\n", encoding="utf-8")

    if users_json.exists():
        data = json.loads(users_json.read_text(encoding="utf-8"))
        if username not in data["users"]:
            data["users"].append(username)
        data["active"] = username
    else:
        data = {"users": [username], "active": username, "created": "2026"}

    users_json.write_text(json.dumps(data, indent=2), encoding="utf-8")
    step(f"Usuario '{username}' creado", "OK", "✅")


def install_python_deps(target_dir):
    req_file = Path(target_dir) / "web" / "requirements.txt"
    if req_file.exists():
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
            capture_output=True, timeout=120,
        )
        step("Dependencias Python instaladas", "OK", "✅")


def init_git(target_dir):
    os.chdir(target_dir)
    if not Path(".git").exists():
        subprocess.run(["git", "init"], capture_output=True, timeout=10)
        subprocess.run(["git", "add", "."], capture_output=True, timeout=10)
        subprocess.run(
            ["git", "commit", "-m", "OpenCode Ultimate v2.0"],
            capture_output=True, timeout=10,
        )
        step("Git inicializado con commit inicial", "OK", "✅")
    else:
        step("Git ya inicializado", "OK", "✅")


def main():
    print("=" * 50)
    print("  OpenCode Ultimate — Instalador")
    print("=" * 50)
    print()

    target = input("Directorio de instalación (Enter para actual): ").strip()
    if not target:
        target = os.getcwd()

    username = input("Nombre de usuario (Enter para 'default'): ").strip() or "default"

    print()

    # Checks
    all_ok = all([check_git(), check_python(), check_ollama()])
    if not all_ok:
        print("\nCorrige los errores y vuelve a ejecutar el instalador.")
        sys.exit(1)

    # Pull models
    pull = input("\n¿Descargar modelos Ollama? (s/N): ").strip().lower() == "s"
    if pull:
        pull_ollama_models()

    # Clone or setup
    if not clone_repo(target):
        sys.exit(1)

    # Create user
    create_user(target, username)

    # Install deps
    install_python_deps(target)

    # Init git
    init_git(target)

    print()
    print("=" * 50)
    print("  Instalación completada.")
    print(f"  Tus datos están en: {Path(target) / 'AI' / 'Memory' / 'users' / username}")
    print(f"  Panel web: cd {target}/web && python main.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
