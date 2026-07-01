param(
    [switch]$Session,
    [switch]$FromGit
)

function Write-Memory {
    param([string]$File, [string]$Content)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    Add-Content -Path $File -Value "`n## [$timestamp]"
    Add-Content -Path $File -Value $Content
    Write-Host "  Memoria actualizada: $File" -ForegroundColor Gray
}

if ($Session) {
    # Iniciar sesión
    $sessionFile = "AI/Memory/sessions/session-$(Get-Date -Format 'yyyyMMdd-HHmmss').md"
    $obj = Read-Host "Objetivo de la sesion"
    $persona = Read-Host "Persona a usar (Architect/Developer)"
@"
# Sesion: $(Get-Date -Format "yyyy-MM-dd HH:mm")

## Objetivo
$obj

## Persona
$persona

## Tareas

## Decisiones

## Archivos modificados

## Pendiente

## Notas
"@ | Out-File -FilePath $sessionFile -Encoding utf8
    Write-Host "Sesion iniciada: $sessionFile" -ForegroundColor Green
}

if ($FromGit) {
    # Analizar git log para actualizar memoria automáticamente
    Write-Host "Analizando actividad Git..." -ForegroundColor Cyan

    $log = git log --oneline -5 --format="%h %s"
    if ($log) {
        $content = "Commits recientes:"
        $content += "`n$log"
        Write-Memory -File "AI/Memory/proyectos.md" -Content $content
    }

    $changedFiles = git diff --name-only HEAD~1..HEAD 2>$null
    if ($changedFiles) {
        $files = ($changedFiles | ForEach-Object { "- $_" }) -join "`n"
        Write-Memory -File "AI/Memory/proyectos.md" -Content "Archivos modificados:`n$files"
    }

    Write-Host "Memoria sincronizada con Git." -ForegroundColor Green
}

if (-not $Session -and -not $FromGit) {
    Write-Host "Uso: .\Scripts\auto-memory.ps1 -Session  (iniciar sesion)"
    Write-Host "     .\Scripts\auto-memory.ps1 -FromGit (sincronizar con git)"
}
