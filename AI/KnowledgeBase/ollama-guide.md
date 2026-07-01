# Ollama — Referencia rápida

## Comandos
```
ollama list                       # Modelos descargados
ollama pull [modelo]              # Descargar modelo
ollama run [modelo]               # Ejecutar modelo interactivo
ollama rm [modelo]                # Eliminar modelo
ollama ps                         # Modelos en ejecución
ollama stop [modelo]              # Detener modelo
```

## Modelos recomendados
| Modelo | Uso |
|--------|-----|
| qwen3:8b | Trabajo diario, código, chat |
| deepseek-r1:8b | Problemas complejos, razonamiento |
| llama3.1:8b | Documentación, análisis |

## API
```
POST http://localhost:11434/api/generate
{"model": "qwen3:8b", "prompt": "Hola", "stream": false}

POST http://localhost:11434/api/chat
{"model": "qwen3:8b", "messages": [{"role": "user", "content": "Hola"}]}
```
