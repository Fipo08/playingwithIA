import os
import httpx
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://api.openai.com/v1")
        key_env = config.get("key_env", "OPENAI_API_KEY")
        self.api_key = os.getenv(key_env, "")

    async def chat(self, messages: list, temperature: float = 0.3) -> str:
        if not self.api_key:
            return "❌ API key no configurada. Revisa tu archivo .env"

        model = self.config.get("model", "gpt-4o-mini")
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"Error OpenAI ({r.status_code}): {r.text}"

    async def is_available(self) -> bool:
        return bool(self.api_key)
