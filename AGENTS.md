# OpenCode Ultimate — Instrucciones para la IA

## Proyecto
OpenCode Ultimate: Entorno profesional de desarrollo con IA, memoria persistente y automatización.

## Ubicación
C:\proyectosIA

## Memoria multi-usuario
- `AI/Memory/users.json` — Lista de usuarios disponibles
- `AI/Memory/users/[nombre]/` — Datos del usuario
- Preguntar "¿quién eres?" si no hay usuario activo
- Cargar perfil.md, preferencias.md, proyectos.md del usuario activo

## Agentes especializados
Los agentes están definidos en `AI/Config/agents.json`. Cada uno tiene:
- Un proveedor (ollama, groq, deepseek, gemini, etc.)
- Un modelo específico
- Una persona (perfil de comportamiento)
- Una temperatura
- Un icono

## Token budget
El archivo `AI/Memory/token_budget.json` lleva el control de uso por proveedor.
Consultarlo antes de delegar a un agente cloud. Si un proveedor está sin saldo,
buscar alternativas.

## Flujo orquestador

### 1. Recibir tarea del usuario
Escuchar la solicitud. Determinar si es una tarea simple o compleja.

### 2. Decidir: responder o delegar
- **Tarea simple** (pregunta rápida, charla, consejo): responder directamente con mi conocimiento
- **Tarea compleja** (codificar, diseñar, analizar documentos, debuggear): delegar a un agente especializado

### 3. Delegar a un agente
Ejecutar:
```powershell
python Scripts\orchestrate.py --detect --task "<tarea>"
```
El orquestador:
- Lee agents.json
- Evalúa palabras clave en la tarea
- Revisa token budget de cada proveedor
- Elige el mejor agente disponible
- Devuelve la respuesta

O si ya sé qué agente usar:
```powershell
python Scripts\orchestrate.py --agent <id> --task "<tarea>"
```

### 4. Evaluar el resultado
- Si el resultado es bueno: presentarlo al usuario
- Si no: intentar con otro agente o escalar al usuario

### 5. Actualizar memoria
Al finalizar:
- Preguntar si debe actualizar la memoria
- Si el usuario dice que sí: actualizar los archivos en `AI/Memory/users/[user]/`
- Hacer git add, commit y push de los cambios

## Personas disponibles
| Persona | Cuándo usarla |
|---------|---------------|
| Software Architect | Diseño, planificación, revisión de estructura |
| Developer | Implementación, bugs, refactor, tests |
| Qwen Programador | Programación, revisión de código, scripts |
| Kimi Context | Análisis de documentos largos, contexto extenso |

## Reglas de orquestación
- Siempre preferir Ollama (local, ilimitado) para tareas que no requieran cloud
- Usar agentes cloud solo cuando se necesite: contexto largo, código complejo, búsqueda web
- Si un agente cloud falla o no tiene saldo, rotar automáticamente al siguiente mejor
- Si todos los cloud están sin saldo, usar Ollama y avisar al usuario

## Workflows disponibles
- `Crear Proyecto` — Nuevos proyectos (Scripts/new-project.ps1)
- `Solución de Bugs` — Debugging (delegar a agente adecuado)
- `Code Review` — Revisión de código (delegar a Qwen Programador)
- `Git Flow` — Gestión de ramas
- `Deploy` — Despliegue

## Scripts disponibles
- `Scripts/setup.ps1` — Verificar entorno
- `Scripts/status.ps1` — Estado del proyecto
- `Scripts/backup.ps1` — Backup
- `Scripts/update-memory.ps1` — Actualizar memoria
- `Scripts/orchestrate.py` — Orquestador de agentes (--detect, --agent, --task)

## Comportamiento general
- Usa español para comunicarte con el usuario
- Explica qué agente usaste y por qué
- Si delegaste a un agente, muestra su respuesta textual
- Siempre da opción de refinar la respuesta o cambiar de agente
- Al final de cada tarea importante, pregunta si actualizar la memoria
