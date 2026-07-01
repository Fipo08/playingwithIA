import json
import os
from pathlib import Path

from dotenv import load_dotenv

from .providers.ollama_provider import OllamaProvider
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider

BASE_DIR = Path(__file__).resolve().parent.parent.parent
AGENTS_FILE = BASE_DIR / "AI" / "Config" / "agents.json"
PROVIDERS_FILE = BASE_DIR / "AI" / "Config" / "providers.json"
ENV_FILE = BASE_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

_PROVIDER_CLASSES = {
    "ollama": OllamaProvider,
    "openai": OpenAIProvider,
    "groq": OpenAIProvider,
    "deepseek": OpenAIProvider,
    "openrouter": OpenAIProvider,
    "kimi": OpenAIProvider,
    "qwen": OpenAIProvider,
    "gemini": GeminiProvider,
}

_cache = {"agents": None, "providers": None, "instances": {}}


def _load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def get_all_agents():
    if _cache["agents"] is None:
        data = _load_json(AGENTS_FILE)
        _cache["agents"] = data.get("agents", [])
    return _cache["agents"]


def get_agent(agent_id: str) -> dict | None:
    for a in get_all_agents():
        if a["id"] == agent_id:
            return a
    return None


def get_providers_config():
    if _cache["providers"] is None:
        _cache["providers"] = _load_json(PROVIDERS_FILE)
    return _cache["providers"]


def get_provider_instance(agent_id: str):
    if agent_id in _cache["instances"]:
        return _cache["instances"][agent_id]

    agent = get_agent(agent_id)
    if not agent:
        return None

    provider_name = agent["provider"]
    providers_config = get_providers_config()
    provider_config = providers_config.get(provider_name, {})
    provider_config["model"] = agent["model"]

    # Permitir override de API URL desde variable de entorno
    url_env = f"{provider_name.upper()}_API_URL"
    env_url = os.getenv(url_env)
    if env_url:
        provider_config["api_url"] = env_url

    cls = _PROVIDER_CLASSES.get(provider_name)
    if not cls:
        return None

    instance = cls(provider_config)
    _cache["instances"][agent_id] = instance
    return instance
