import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
USERS_DIR = BASE_DIR / "AI" / "Memory" / "users"
USERS_JSON = USERS_DIR / "users.json"


def get_users():
    if USERS_JSON.exists():
        data = json.loads(USERS_JSON.read_text(encoding="utf-8"))
        return data.get("users", [])
    return []


def get_active_user():
    if USERS_JSON.exists():
        data = json.loads(USERS_JSON.read_text(encoding="utf-8"))
        return data.get("active", "feli")
    return "feli"


def set_active_user(username):
    if USERS_JSON.exists():
        data = json.loads(USERS_JSON.read_text(encoding="utf-8"))
        data["active"] = username
        USERS_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_user_files(username):
    user_dir = USERS_DIR / username
    if not user_dir.exists():
        return {}
    files = {}
    for f in ["perfil.md", "preferencias.md", "proyectos.md"]:
        path = user_dir / f
        if path.exists():
            files[f] = path.read_text(encoding="utf-8")
        else:
            files[f] = ""
    return files


def save_user_file(username, filename, content):
    user_dir = USERS_DIR / username
    path = user_dir / filename
    path.write_text(content, encoding="utf-8")


def get_sessions(username):
    sessions_dir = USERS_DIR / username / "sessions"
    if not sessions_dir.exists():
        return []
    sessions = []
    for f in sorted(sessions_dir.glob("*.md"), reverse=True):
        sessions.append({
            "name": f.name,
            "path": str(f.relative_to(BASE_DIR)),
            "content": f.read_text(encoding="utf-8"),
        })
    return sessions
