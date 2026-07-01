# Memoria

## Estructura multi-usuario

```
users/
├── [nombre]/
│   ├── perfil.md          — Datos personales
│   ├── preferencias.md    — Stack, herramientas, estilo
│   ├── proyectos.md       — Proyectos activos/archivados
│   └── sessions/          — Historial de sesiones
├── _template/             — Plantilla para nuevos usuarios
└── users.json             — Lista de usuarios registrados
```

## ¿Cómo se usa?
1. La IA pregunta "¿quién eres?" al iniciar
2. Carga los archivos de `users/[tu_nombre]/`
3. Al finalizar, actualiza la memoria y commit + push
