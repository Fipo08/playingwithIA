import httpx
from pathlib import Path

REPO = "Fipo08/playingwithIA"
GITHUB_API = f"https://api.github.com/repos/{REPO}/releases/latest"

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_current_version():
    changelog = BASE_DIR / "Documentation" / "CHANGELOG.md"
    if changelog.exists():
        for line in changelog.read_text(encoding="utf-8").split("\n"):
            if line.startswith("## v"):
                return line.strip().split(" ")[1]
    return "0.0.0"


async def check_update():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(GITHUB_API)
            if r.status_code == 200:
                data = r.json()
                latest = data.get("tag_name", "").lstrip("v")
                current = get_current_version()
                return {
                    "has_update": latest != current,
                    "current": current,
                    "latest": latest,
                    "url": data.get("html_url", ""),
                    "body": data.get("body", ""),
                }
    except Exception:
        pass
    return {"has_update": False, "current": get_current_version(), "latest": "", "url": "", "body": ""}
