import os
import httpx
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://api.openai.com/v1")
        key_env = config.get("key_env", "OPENAI_API_KEY")
        self.api_key = os.getenv(key_env, "")

    def _model_param(self) -> str:
        return self.config.get("model", "gpt-4o-mini")

    async def chat(self, messages: list, temperature: float = 0.3) -> str:
        model = self._model_param()
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                headers=headers,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            body = r.text[:500]
            return f"Error ({r.status_code}): {body}"

    async def is_available(self) -> bool:
        return True
