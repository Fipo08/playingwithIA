# Template: Mensaje de Commit

## Formato
```
[tipo]([contexto]): [descripción corta en presente]
```

## Tipos
| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `chore` | Mantenimiento, config, dependencias |
| `docs` | Documentación |
| `refactor` | Refactorización sin cambio funcional |
| `style` | Formato, estilos (no funcional) |
| `test` | Añadir o corregir tests |
| `perf` | Mejora de rendimiento |

## Ejemplos
```
feat: implementar autenticación con JWT
fix: corregir error 500 al crear usuario sin email
docs(api): documentar endpoint de login
refactor: extraer validación a middleware
chore: actualizar dependencias
test: añadir tests para el controlador de usuarios
perf: cachear consultas de usuarios frecuentes
```

## Reglas
- Máximo 72 caracteres en la primera línea
- Usar imperativo ("añadir", no "añadido")
- No terminar con punto
- Incluir contexto entre paréntesis si aplica
