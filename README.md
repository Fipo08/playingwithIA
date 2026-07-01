# OpenCode Ultimate

Entorno profesional de desarrollo con IA, memoria persistente y automatización.

## Versión actual
v3.0 — Multi-agente con orquestador desde terminal

## Estructura
```
├── AI/
│   ├── Config/          # Configuración (env, models, agents, providers)
│   ├── Memory/          # Memoria persistente + sesiones + token budget
│   ├── Personas/        # Roles de IA (Architect, Developer, Qwen, Kimi)
│   ├── Prompts/         # Prompts reutilizables (Planner, Debugger)
│   ├── Rules/           # Reglas de codificación y buenas prácticas
│   └── Workflows/       # Workflows ejecutables
├── Documentation/       # Documentación del proyecto
├── Projects/            # Proyectos activos
├── Scripts/             # Scripts de automatización + proveedores + orquestador
├── Backups/             # Backups del proyecto
├── AGENTS.md            # Instrucciones para la IA (orquestador)
└── CLAUDE.md            # Compatibilidad con Claude Code
```

## Cómo usar
Solo háblame desde la terminal. Yo:
1. Analizo tu tarea
2. Decido si responder yo o delegar a un agente especializado
3. Elijo el mejor proveedor según token budget
4. Ejecuto el agente y te traigo la respuesta
5. Actualizo la memoria si es necesario
