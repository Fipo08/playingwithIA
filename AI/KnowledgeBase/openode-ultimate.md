# OpenCode Ultimate — Referencia Rápida

## Estructura
```
AI/
├── Config/         → agents.json, modelos, providers
├── KnowledgeBase/  → snippets y referencias técnicas
├── Memory/         → sesiones, perfiles de usuario
├── Personas/       → perfiles de agente (Developer, Architect, etc.)
├── Prompts/        → prompts reutilizables
├── Rules/          → reglas de codificación
├── Templates/      → plantillas (commits, proyectos, PRs)
└── Workflows/      → workflows operativos
Scripts/            → automatización principal
```

## Scripts clave
| Comando | Función |
|---------|---------|
| `Scripts\status.ps1` | Estado del proyecto |
| `Scripts\orchestrate.py --always --task "..."` | Delegar a agente cloud |
| `Scripts\update-memory.ps1` | Actualizar memoria |
| `Scripts\backup.ps1` | Backup del proyecto |
| `Scripts\auto-memory.ps1` | Gestión automática de memoria |

## AGENTS.md
Archivo de instrucciones principal. Incluye:
- Reglas de orquestación (`--always`, `--detect`)
- Personas disponibles y cuándo usarlas
- Flujo de recuperación de sesión
- Workflows predefinidos

## Memoria de sesiones
`AI/Memory/users/<user>/sessions/` — registro de cada sesión.
Formato: `YYYYMMDD-descripcion.md` con objetivo, tareas, decisiones, pendientes.
