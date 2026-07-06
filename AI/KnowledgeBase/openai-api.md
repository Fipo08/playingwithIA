# OpenAI / LLM API Reference

## Chat Completions
```bash
POST https://api.openai.com/v1/chat/completions
Authorization: Bearer $KEY
Content-Type: application/json
```

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "Eres un asistente útil."},
    {"role": "user", "content": "Hola"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

## Providers alternativos
| Provider | Endpoint | Modelo recomendado |
|----------|----------|-------------------|
| OpenAI | `https://api.openai.com/v1` | gpt-4o, gpt-4o-mini |
| Groq | `https://api.groq.com/openai/v1` | llama-3.3-70b, deepseek-r1 |
| DeepSeek | `https://api.deepseek.com/v1` | deepseek-chat |
| Google (Gemini) | `https://generativelanguage.googleapis.com/v1beta` | gemini-2.0-flash |
| Ollama (local) | `http://localhost:11434/v1` | qwen3, deepseek-r1, llama3.1 |

## Rate Limits
- OpenAI: 500-10000 RPM según tier
- Groq: 30 req/min (gratis), 6000 (pago)
- DeepSeek: 500 RPM
- Gemini: 1500 RPM (gratis)

## Streaming
```json
{"stream": true}
```
Eventos SSE: `data: {"choices":[{"delta":{"content":"texto"}}]}`

## Formatos mensaje
```json
{"role": "user", "content": "texto"}
{"role": "assistant", "content": "respuesta"}
{"role": "system", "content": "instrucción"}
{"role": "user", "content": [{"type": "text", "text": "..."}]}
```
