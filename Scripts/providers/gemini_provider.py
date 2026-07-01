import os
import json
import httpx
from .base import BaseProvider


class GeminiProvider(BaseProvider):
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_url = config.get("api_url", "https://generativelanguage.googleapis.com/v1beta")
        key_env = config.get("key_env", "GEMINI_API_KEY")
        self.api_key = os.getenv(key_env, "")

    def chat(self, messages: list, temperature: float = 0.3) -> str:
        if not self.api_key:
            return "Error: GEMINI_API_KEY no configurada"

        model = self.config.get("model", "gemini-2.0-flash")

        system_instruction = ""
        contents = []
        for m in messages:
            if m["role"] == "system":
                system_instruction = m["content"]
            elif m["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": m["content"]}]})
            elif m["role"] == "assistant":
                contents.append({"role": "model", "parts": [{"text": m["content"]}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": 8192},
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        url = f"{self.api_url}/models/{model}:generateContent?key={self.api_key}"
        r = httpx.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=180)
        if r.status_code == 200:
            try:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return f"Respuesta inesperada: {json.dumps(r.json(), indent=2)[:500]}"
        return f"Error Gemini ({r.status_code}): {r.text[:300]}"
