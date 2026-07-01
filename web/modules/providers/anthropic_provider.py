import os
import httpx
from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://api.anthropic.com/v1")
        key_env = config.get("key_env", "ANTHROPIC_API_KEY")
        self.api_key = os.getenv(key_env, "")

    async def chat(self, messages: list, temperature: float = 0.3) -> str:
        if not self.api_key:
            return "❌ API key no configurada. Revisa tu archivo .env"

        model = self.config.get("model", "claude-sonnet-4-20250514")

        system_msg = ""
        cleaned = []
        for m in messages:
            if m["role"] == "system":
                system_msg += m["content"] + "\n"
            else:
                cleaned.append(m)

        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": cleaned,
            "temperature": temperature,
        }
        if system_msg:
            payload["system"] = system_msg.strip()

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f"{self.api_url}/messages",
                json=payload,
                headers=headers,
            )
            if r.status_code == 200:
                return r.json()["content"][0]["text"]
            return f"Error Anthropic ({r.status_code}): {r.text}"

    async def is_available(self) -> bool:
        return bool(self.api_key)
