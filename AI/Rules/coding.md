# Coding Rules

## Generales
- Código limpio y legible
- Funciones pequeñas (máximo 30 líneas)
- Nombres descriptivos en inglés para código
- Comentarios solo cuando el código no se explica solo
- Sin código muerto o comentado

## Git
- Commits atómicos (un cambio por commit)
- Mensajes descriptivos en español o inglés
- No commitees archivos generados, .env, node_modules

## Seguridad
- No hardcodees contraseñas, tokens o API keys
- Usa variables de entorno para secretos
- No expongas información interna en mensajes de error

## Estructura
- Cada archivo con una responsabilidad clara
- Separación entre lógica y configuración
- Preferir archivos planos (md, json, yaml) para configuración
