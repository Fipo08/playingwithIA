# Sistema de Agentes — OpenCode Ultimate

## Arquitectura

```
Usuario
  │
  ▼
orchestrate.py  ←  agents.json (config)
  │
  ├── Auto-detect (keywords → mejor agente)
  ├── Selección manual (--agent <id>)
  └── Fallback automático si falla o sin saldo
        │
        ▼
  providers/
  ├── OllamaProvider (local)
  ├── OpenAIProvider (Groq, DeepSeek, OpenRouter, Kimi, Qwen)
  └── GeminiProvider (Gemini Flash / Pro)
```

## Orquestador (`Scripts/orchestrate.py`)

### Flags principales

| Flag | Descripción |
|------|-------------|
| `--task "<texto>"` | Tarea a ejecutar |
| `--agent <id>` | Seleccionar agente específico |
| `--detect` | Auto-detectar el mejor agente por keywords |
| `--always` | Modo siempre-delegar (solo cloud, sin Ollama, genera task-id) |
| `--no-local` | Excluir Ollama de la selección |
| `--task-id <id>` | Trackear resultado con checkpoint |
| `--system "<prompt>"` | System prompt opcional |
| `--status-pending` | Ver tareas pendientes |
| `--cleanup-pending` | Limpiar pendientes |

### Ejemplos de uso

```powershell
# Auto-detectar agente
python Scripts\orchestrate.py --detect --task "implementa una funcion de ordenamiento"

# Modo siempre-delegar (a la nube)
python Scripts\orchestrate.py --always --task "revisa el codigo en src/"

# Agente específico
python Scripts\orchestrate.py --agent gemini-flash --task "traduce esto al ingles"

# Con tracking de resultado
python Scripts\orchestrate.py --detect --task "analiza este error" --task-id "bug001"
```

## Agentes Disponibles

### Cloud (requieren API key en .env)

| ID | Nombre | Proveedor | Modelo | Perfil | Ideal para |
|----|--------|-----------|--------|--------|------------|
| `groq-llama` | Groq Llama 3 | Groq | llama-3.3-70b | Developer | Tareas rápidas y gratis |
| `groq-mixtral` | Groq Mixtral | Groq | mixtral-8x7b | Architect | Razonamiento, análisis |
| `deepseek-coder` | DeepSeek Coder | DeepSeek | deepseek-coder | Developer | Código, optimización |
| `deepseek-chat` | DeepSeek Chat | DeepSeek | deepseek-chat | Architect | Chat general |
| `gemini-flash` | Gemini Flash | Gemini | gemini-2.0-flash | Developer | Rápido, multimodal |
| `gemini-pro` | Gemini Pro | Gemini | gemini-1.5-pro | Architect | Contexto largo |
| `qwen-turbo` | Qwen Turbo | OpenRouter | qwen/qwen-turbo | Qwen | Programación |
| `qwen-coder` | Qwen Coder | OpenRouter | qwen-2.5-coder | Qwen | Código avanzado |
| `claude-haiku` | Claude Haiku | OpenRouter | claude-3-haiku | Developer | Rápido y barato |
| `kimi-32k` | Kimi 32k | Kimi | moonshot-v1-32k | Kimi | Contexto medio |
| `kimi-128k` | Kimi 128k | Kimi | moonshot-v1-128k | Kimi | Documentos largos |
| `qwen-max` | Qwen Max | Qwen | qwen-max | Qwen | Tareas complejas |
| `qwen-plus` | Qwen Plus | Qwen | qwen-plus | Qwen | Uso general |
| `chat` | Chat | Gemini | gemini-2.0-flash | Chat | Conversación general |

### Local (Ollama, sin API key)

| ID | Nombre | Modelo | Perfil |
|----|--------|--------|--------|
| `arquitecto` | Arquitecto | deepseek-r1:8b | Architect |
| `desarrollador` | Desarrollador | qwen3:8b | Developer |
| `documentador` | Documentador | llama3.1:8b | Architect |

## Auto-detección por Keywords

El `--detect` puntúa agentes según palabras clave en la tarea:

| Agente | Keywords |
|--------|----------|
| arquitecto | arquitectura, base de datos, diseñar, planificar, estructura |
| desarrollador | bug, error, debug, implementar, código, función, test |
| groq-mixtral | razonar, analizar, comparar, evaluar, complejo |
| deepseek-coder | script, algoritmo, optimizar, rendimiento |
| kimi-128k | documento largo, archivo grande, contexto largo |
| gemini-flash | rápido, simple, cotidiano, traducir |
| qwen-coder | programar, código, desarrollar, implementar |
| chat | hola, preguntas, quién, qué, cuándo, charla |

Si ningún agente supera el umbral, cae en `chat` (Gemini Flash).

## Fallback Automático

Si un agente falla o el proveedor no tiene saldo:

1. Busca otro agente del **mismo perfil** (persona)
2. Si no hay, busca **cualquier agente disponible**
3. En modo `--no-local`, excluye Ollama
4. Si todos los cloud fallan, muestra mensaje de error

## Token Budget

`AI/Memory/token_budget.json` controla el consumo por proveedor:

| Proveedor | Límite | Unidad |
|-----------|--------|--------|
| Groq | 1,000,000 | tokens/día |
| DeepSeek | 500,000 | tokens |
| Gemini | 1,500 | requests/día |
| OpenRouter | 100,000 | tokens |
| Kimi | 500,000 | tokens |
| Qwen | 500,000 | tokens |
| Ollama | Ilimitado | — |

## Providers

Configuración en `AI/Config/providers.json`. API keys en `.env`.

| Proveedor | API Key Env | URL Base |
|-----------|-------------|----------|
| Groq | `GROQ_API_KEY` | https://api.groq.com/openai/v1 |
| DeepSeek | `DEEPSEEK_API_KEY` | https://api.deepseek.com |
| Gemini | `GEMINI_API_KEY` | https://generativelanguage.googleapis.com |
| OpenRouter | `OPENROUTER_API_KEY` | https://openrouter.ai/api/v1 |
| Kimi | `KIMI_API_KEY` | https://api.moonshot.cn/v1 |
| Qwen | `QWEN_API_KEY` | https://api.qwen.aliyuncs.com |
| Ollama | — | http://localhost:11434 |
