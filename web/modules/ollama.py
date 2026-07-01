import httpx
import subprocess

OLLAMA_API = "http://localhost:11434"


async def is_ollama_running():
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            r = await client.get(f"{OLLAMA_API}/api/tags")
            return r.status_code == 200
    except Exception:
        return False


async def list_models():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{OLLAMA_API}/api/tags")
            if r.status_code == 200:
                data = r.json()
                return [m["name"] for m in data.get("models", [])]
    except Exception:
        pass
    return []


def list_models_sync():
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")[1:]
        models = []
        for line in lines:
            parts = line.split()
            if parts:
                models.append(parts[0].replace(":latest", ""))
        return models
    except Exception:
        return []
