import httpx
from .base import BaseProvider


class OllamaProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "http://localhost:11434")

    async def chat(self, messages: list, temperature: float = 0.3) -> str:
        model = self.config.get("model", "qwen3:8b")
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.api_url}/api/chat", json=payload)
            if r.status_code == 200:
                return r.json()["message"]["content"]
            return f"Error Ollama ({r.status_code}): {r.text}"

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f"{self.api_url}/api/tags")
                return r.status_code == 200
        except Exception:
            return False
