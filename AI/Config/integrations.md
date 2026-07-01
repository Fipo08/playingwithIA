# Integraciones

## GitHub (CLI — gh)
```powershell
gh auth status                    # Verificar autenticación
gh repo list                      # Listar repos
gh repo create [name] --private   # Crear repo privado
gh repo edit [repo] --visibility  # Cambiar visibilidad
```

## GitHub Actions
Los workflows están en `.github/workflows/`.
- `check.yml` — Verifica estructura del proyecto en cada push

## Ollama API
```powershell
# Health check
Invoke-RestMethod http://localhost:11434/api/tags

# Listar modelos en ejecución
ollama ps
```

## Git Hooks (futuro)
Para automatizar:
- Pre-commit: verificar reglas de coding
- Post-commit: actualizar memoria
- Pre-push: ejecutar tests
