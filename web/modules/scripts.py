import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = BASE_DIR / "Scripts"


def list_scripts():
    scripts = []
    for f in sorted(SCRIPTS_DIR.glob("*.ps1")):
        if f.name.startswith("_"):
            continue
        scripts.append({
            "name": f.stem,
            "path": str(f.relative_to(BASE_DIR)),
        })
    return scripts


def run_script(script_name):
    script_path = SCRIPTS_DIR / f"{script_name}.ps1"
    if not script_path.exists():
        raise FileNotFoundError(f"Script no encontrado: {script_name}.ps1")

    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
        timeout=120,
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }
