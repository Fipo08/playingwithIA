# Configuración de Modelos

## Modelos disponibles (Ollama local)

| Modelo | Tamaño | Uso recomendado | Temperatura |
|--------|--------|-----------------|-------------|
| qwen3:8b | 5.2 GB | Trabajo diario, código, análisis | 0.3 - 0.5 |
| deepseek-r1:8b | 5.2 GB | Razonamiento complejo, debugging | 0.5 - 0.7 |
| llama3.1:8b | 4.9 GB | Documentación, revisión, formato | 0.2 - 0.4 |

## Configuración por persona

| Persona | Modelo | Temp | Contexto |
|---------|--------|------|----------|
| Software Architect | deepseek-r1:8b | 0.5 | Alto |
| Developer | qwen3:8b | 0.3 | Medio |

## API Reference
```powershell
# Chat
$body = @{
    model = "qwen3:8b"
    messages = @(@{role="user"; content="Hola"})
    stream = $false
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:11434/api/chat" -Method Post -Body $body -ContentType "application/json"

# Generate
$body = @{
    model = "qwen3:8b"
    prompt = "Hola"
    stream = $false
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $body -ContentType "application/json"
```
