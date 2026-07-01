# Workflow: Code Review

## Pasos

### 1. Preparación
- Obtener el diff o los archivos a revisar
- Identificar el propósito del cambio

### 2. Revisión
- Leer el código línea por línea
- Verificar contra AI/Rules/coding.md:
  - Funciones pequeñas (< 30 líneas)
  - Nombres descriptivos
  - Sin código muerto
  - Sin secretos hardcodeados
- Buscar bugs potenciales
- Evaluar cobertura de casos edge

### 3. Feedback
- Clasificar hallazgos:
  - 🔴 Bloqueante: debe corregirse antes de merge
  - 🟡 Sugerencia: mejora opcional
  - 🔵 Pregunta: necesita aclaración
- Ser específico: dar ejemplo de código

### 4. Resumen
- ¿El cambio cumple su propósito?
- Veredicto: Approve / Changes Requested / Comment
