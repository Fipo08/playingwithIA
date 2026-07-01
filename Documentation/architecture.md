# Arquitectura de OpenCode Ultimate

## Propósito
Proveer un entorno de desarrollo con IA que mantenga memoria persistente, roles especializados y procesos repetibles.

## Capas

### 1. Memoria (AI/Memory/)
Persistencia del contexto del desarrollador y sus proyectos.
- `perfil.md` — Quién es el desarrollador
- `preferencias.md` — Stack, herramientas, estilo
- `proyectos.md` — Proyectos activos y archivados

### 2. Personas (AI/Personas/)
Roles que la IA adopta según la tarea.
- Cada persona tiene: Rol, Responsabilidades, Output esperado, Activación
- Se elige según el tipo de tarea (arquitectura → Architect, código → Developer)

### 3. Procesos (AI/Workflows/)
Secuencias de pasos para tareas recurrentes.
- Workflow define QUÉ hacer
- Persona define QUIÉN lo hace
- Prompts definen CÓMO hacerlo

### 4. Reglas (AI/Rules/)
Restricciones y buenas prácticas que la IA debe seguir siempre.

### 5. Prompts (AI/Prompts/)
Instrucciones especializadas para tareas concretas (planificar, debuggear).

### 6. Templates (AI/Templates/)
Plantillas reutilizables para commits, proyectos, PRs.

### 7. Conocimiento (AI/KnowledgeBase/)
Referencias técnicas, snippets, guías rápidas.

### 8. Configuración (AI/Config/)
Ajustes del entorno (modelos de IA, paths, preferencias globales).

## Flujo de trabajo típico
```
Usuario pide tarea
  → IA lee AGENTS.md, Memory/, Rules/
  → IA selecciona Persona según tarea
  → IA sigue Workflow correspondiente
  → IA usa Prompt si aplica
  → IA ejecuta y reporta
  → IA pregunta si actualizar Memory/
```
