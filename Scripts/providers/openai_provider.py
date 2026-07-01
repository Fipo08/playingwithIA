import os
import httpx
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://api.openai.com/v1")
        key_env = config.get("key_env", "OPENAI_API_KEY")
        self.api_key = os.getenv(key_env, "")

    def chat(self, messages: list, temperature: float = 0.3) -> str:
        model = self.config.get("model", "gpt-4o-mini")
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        r = httpx.post(
            f"{self.api_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=180,
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"Error ({r.status_code}): {r.text[:300]}"
