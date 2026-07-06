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

## Inicio de sesión
Al comenzar, ejecutar:
```powershell
python Scripts\orchestrate.py --status-pending
```
Si hay checkpoint → recuperar sesión anterior.
Si no → continuar normalmente.

## Flujo orquestador (modo siempre-delegar)

### 1. Recibir tarea del usuario
Escuchar la solicitud.

### 2. Delegar siempre al orquestador con --always
Ejecutar:
```powershell
python Scripts\orchestrate.py --always --task "<tarea>"
```

`--always` implica:
- `--no-local`: solo agentes cloud (Ollama excluido por velocidad limitada)
- `--detect`: detección automática del mejor agente según keywords
- Auto-genera `--task-id` para tracking en `pending/results/`
- Si ningún agente especializado coincide → cae en `chat` (Gemini Flash)
- Si todos los cloud están sin saldo → avisa al usuario

O si ya sé qué agente usar:
```powershell
python Scripts\orchestrate.py --always --agent <id> --task "<tarea>"
```

### 3. Evaluar el resultado
- Presentar al usuario
- Si el resultado es error o fallback, sugerir alternativa

### 4. Actualizar memoria
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
- Usar siempre `--always` (modo siempre-delegar) para enrutar toda interacción al orquestador
- Solo agentes cloud (`--no-local` implícito con `--always`)
- Si un agente falla o no tiene saldo, rotar automáticamente al siguiente mejor del mismo perfil
- Si todos los cloud están sin saldo, avisar al usuario (no caer a Ollama)
- Toda interacción queda trackeada en `pending/results/` con su `--task-id`

## Workflows disponibles
- `Crear Proyecto` — Nuevos proyectos (Scripts/new-project.ps1)
- `Solución de Bugs` — Debugging (delegar a agente adecuado)
- `Code Review` — Revisión de código (delegar a Qwen Programador)
- `Git Flow` — Gestión de ramas
- `Deploy` — Despliegue

## Recuperación ante pérdida de sesión

### ¿Qué es?
Si la sesión actual se pierde por saturación de tokens antes de recibir
resultados de un subagente, el sistema de persistencia permite retomar
el trabajo sin pérdida de datos.

### Flujo de recuperación (ejecutar al inicio de cada sesión)

1. **Revisar** si existe `AI/Memory/pending/checkpoint.json`
   - Si NO existe: continuar normalmente
   - Si SÍ existe: hay tareas pendientes

2. **Recuperar resultados**: Leer archivos en `AI/Memory/pending/results/`
   - Cada archivo `task_<id>_<agent>.json` contiene el resultado completo

3. **Presentar al usuario**:
   - Indicar que se recuperó una sesión anterior
   - Mostrar un resumen de lo que se encontró
   - Preguntar si desea continuar, revisar los resultados, o descartarlos

4. **Limpiar**: Una vez recuperado, ejecutar:
   ```powershell
   python Scripts\orchestrate.py --cleanup-pending
   ```
   Esto elimina checkpoint.json y los archivos de results/ procesados.

### Cómo funciona

- Al delegar un subagente con `--task-id`, se guarda un checkpoint en
  `pending/checkpoint.json` antes de la ejecución
- El subagente escribe su resultado en `pending/results/<id>_<agent>.json`
- Al completarse, el checkpoint se elimina automáticamente
- Si la sesión muere antes de recibir el resultado, el checkpoint persiste

### Uso desde el orquestador

```powershell
# Delegar con tracking
python Scripts\orchestrate.py --detect --task "<tarea>" --task-id "misión1"

# Limpiar resultados pendientes
python Scripts\orchestrate.py --cleanup-pending

# Ver estado de pendientes
python Scripts\orchestrate.py --status-pending
```

## Scripts disponibles
- `Scripts/setup.ps1` — Verificar entorno
- `Scripts/status.ps1` — Estado del proyecto
- `Scripts/backup.ps1` — Backup
- `Scripts/update-memory.ps1` — Actualizar memoria
- `Scripts/orchestrate.py` — Orquestador de agentes (--always, --detect, --agent, --task, --task-id, --no-local, --cleanup-pending, --status-pending)
- `Scripts/cleanup-pending.ps1` — Limpiar/verificar resultados pendientes
- `Scripts/auto-memory.ps1` — Gestión de memoria (+ -Pending para recuperación)

## Comportamiento general
- Usa español para comunicarte con el usuario
- Explica qué agente usaste y por qué
- Si delegaste a un agente, muestra su respuesta textual
- Siempre da opción de refinar la respuesta o cambiar de agente
- Al final de cada tarea importante, pregunta si actualizar la memoria
