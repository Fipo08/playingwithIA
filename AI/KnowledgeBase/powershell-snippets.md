# PowerShell Snippets

## Helpers de proyecto
```powershell
function Get-ActiveUser {
    $cfg = Get-Content "AI/Memory/users/users.json" | ConvertFrom-Json
    return $cfg.active
}

function Get-UserFile($name) {
    $user = Get-ActiveUser
    return "AI/Memory/users/$user/$name"
}
```

## IO y archivos
```powershell
# Leer JSON
$data = Get-Content "file.json" | ConvertFrom-Json

# Escribir JSON
$obj | ConvertTo-Json -Depth 10 | Set-Content "file.json"

# Verificar existencia
if (Test-Path "ruta") { ... }

# Recursivo
Get-ChildItem -Path "src" -Recurse -Filter "*.py"
```

## Manejo de errores
```powershell
$ErrorActionPreference = "Stop"
trap {
    Write-Error $_.Exception.Message
    exit 1
}

try {
    # código que puede fallar
} catch {
    Write-Error $_.Exception.Message
    exit 1
}
```

## Convenience
```powershell
# Timestamp
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Prompt de confirmación
$resp = Read-Host "¿Continuar? (s/n)"
if ($resp -ne "s") { exit }

# Colores
Write-Host "Mensaje" -ForegroundColor Green
```

## Ejecutar comandos
```powershell
$result = & "comando" "arg1" "arg2" 2>&1
if ($LASTEXITCODE -ne 0) { throw $result }
```
