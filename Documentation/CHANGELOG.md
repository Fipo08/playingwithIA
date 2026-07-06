# Changelog

## v2.1 — Knowledge Base (2026-07-06)
- AI/KnowledgeBase/ con 6 archivos de snippets y referencias técnicas
- Python Snippets: pathlib, async, argparse, logging, subprocess
- PowerShell Snippets: helpers, IO, errores, convenience
- Git Workflows: conventional commits, merge/rebase, undo, worktrees
- OpenAI API Reference: endpoints, providers, rate limits, streaming
- OpenCode Ultimate Reference: estructura del proyecto, scripts clave
- HTML/CSS/JS Snippets: fetch, promises, grid, flexbox, forms
- status.ps1 ahora detecta automáticamente los archivos

## v3.0 — Orquestador Multi-Agente (2026-07)
- `Scripts/orchestrate.py` — orquestador desde terminal con detección automática
- Auto-fallback entre agentes cuando un proveedor falla o se queda sin saldo
- `--detect` selecciona el mejor agente según keywords de la tarea
- `--always` modo delegación forzosa (solo cloud, sin Ollama)
- `--task-id` tracking de resultados con checkpoint y recuperación
- `--cleanup-pending` y `--status-pending` para gestión de pendientes
- Sistema de token budget por proveedor con límites configurables

### Proveedores cloud integrados
- **Groq** — Llama 3.3 70B, Mixtral 8x7B (gratis)
- **DeepSeek** — DeepSeek-V2, DeepSeek-Coder (gratis con registro)
- **Gemini** — Gemini 2.0 Flash, 1.5 Pro (capa gratuita generosa)
- **OpenRouter** — Qwen, Claude, Gemini, DeepSeek y cientos más
- **Kimi (Moonshot AI)** — contexto 32k y 128k
- **Qwen (Alibaba Cloud)** — Qwen Max, Qwen Plus

### Perfiles de persona ampliados
- **Qwen Programador** — código, code review, scripts
- **Kimi Context** — análisis de documentos largos, contexto extenso
- Chat como fallback general para conversación

## v2.0 — Memoria inteligente, Configuración, Integraciones (2026-07-01)
- Sistema de sesiones en AI/Memory/sessions/
- archivos de configuración: env, models, integrations
- GitHub Actions workflow para verificar estructura
- Script avanzado auto-memory.ps1 (sesiones + sincronización git)
- AI/Config/ poblado con referencias completas
- Estructura multi-usuario con memoria por usuario

## v1.3 — Automatización con Scripts (2026-07-01)
- setup.ps1 — Verificación del entorno (Git, Ollama, estructura)
- new-project.ps1 — Scaffolding de nuevos proyectos
- backup.ps1 — Backup comprimido del proyecto
- status.ps1 — Panel de estado del proyecto
- update-memory.ps1 — Actualización rápida de memoria

## v1.2 — Documentación y Workflows avanzados (2026-07-01)
- Documentación de arquitectura y uso
- Workflows: Code Review, Git Flow, Deploy
- Templates mejorados con ejemplos concretos

## v1.1 — Personas, Rules, Prompts, Templates, Workflows (2026-07-01)
- AGENTS.md + CLAUDE.md para instrucciones a la IA
- Memoria persistente poblada con perfil del desarrollador
- Personas: Software Architect y Developer
- Prompts funcionales: planner y debugger
- Reglas de codificación, git y seguridad
- Templates: proyecto, commit, PR
- Workflows: Crear Proyecto, Solución de Bugs

## v1.0 — Estructura base
- Estructura de carpetas inicial
- Proyecto creado
