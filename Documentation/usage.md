# Guía de uso de OpenCode Ultimate

## Primer uso
1. La IA lee automáticamente `AGENTS.md` al iniciar
2. La IA carga tu perfil desde `AI/Memory/`
3. Puedes empezar a pedir tareas directamente

## Pedir una tarea
Solo describe lo que necesitas. La IA:
- Elegirá la persona adecuada
- Seguirá el workflow correspondiente
- Aplicará las reglas de codificación
- Consultará los prompts si es necesario
- Usará la Knowledge Base para referencias rápidas

## Modo orquestador (multi-agente)
Para delegar tareas a agentes cloud especializados:
```powershell
python Scripts\orchestrate.py --always --task "<descripción>"
```
Más detalles en `Documentation/agent-system.md`.

## Knowledge Base
Referencias técnicas y snippets disponibles en `AI/KnowledgeBase/`:
- `python-snippets.md` — Pathlib, async, argparse, logging
- `powershell-snippets.md` — Helpers, IO, errores
- `git-workflows.md` — Conventional commits, merge/rebase
- `openai-api.md` — Endpoints, providers, rate limits
- `openode-ultimate.md` — Estructura y scripts del proyecto
- `html-css-js-snippets.md` — Fetch, promises, grid, flexbox

## Actualizar memoria
Después de completar una tarea importante, pide:
"Actualiza mi memoria con lo que hicimos"

## Cambiar de persona
Si quieres un enfoque específico, di:
"Actúa como [nombre de persona]"

## Personas disponibles
| Persona | Cuándo usarla |
|---------|---------------|
| Software Architect | Diseño, planificación, revisión de estructura |
| Developer | Implementación, bugs, refactor, tests |
| Qwen Programador | Programación, revisión de código, scripts |
| Kimi Context | Análisis de documentos largos, contexto extenso |

## Workflows disponibles
- `Crear Proyecto` — Nuevos proyectos desde cero
- `Solución de Bugs` — Debuggear y corregir errores
- `Code Review` — Revisar código
- `Git Flow` — Gestión de ramas y commits
- `Deploy` — Despliegue de proyectos
