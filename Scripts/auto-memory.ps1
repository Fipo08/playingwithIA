param(
    [switch]$Session,
    [switch]$FromGit,
    [switch]$Pending
)

. "$PSScriptRoot\_helpers.ps1"

function Write-Memory {
    param([string]$File, [string]$Content)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    Add-Content -Path $File -Value "`n## [$timestamp]"
    Add-Content -Path $File -Value $Content
    Write-Host "  Memoria actualizada: $File" -ForegroundColor Gray
}

if ($Session) {
    $userPath = Get-UserPath
    $sessionFile = "$userPath/sessions/session-$(Get-Date -Format 'yyyyMMdd-HHmmss').md"
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
    $proyectosFile = Get-UserFile "proyectos.md"
    Write-Host "Analizando actividad Git..." -ForegroundColor Cyan

    $log = git log --oneline -5 --format="%h %s"
    if ($log) {
        $content = "Commits recientes:"
        $content += "`n$log"
        Write-Memory -File $proyectosFile -Content $content
    }

    $changedFiles = git diff --name-only HEAD~1..HEAD 2>$null
    if ($changedFiles) {
        $files = ($changedFiles | ForEach-Object { "- $_" }) -join "`n"
        Write-Memory -File $proyectosFile -Content "Archivos modificados:`n$files"
    }

    Write-Host "Memoria sincronizada con Git." -ForegroundColor Green
}

if ($Pending) {
    $pendingDir = Join-Path (Resolve-Path "$PSScriptRoot/..") "AI\Memory\pending"
    $resultsDir = Join-Path $pendingDir "results"
    $checkpoint = Join-Path $pendingDir "checkpoint.json"

    if (Test-Path -LiteralPath $checkpoint) {
        Write-Host "`n=== SESION RECUPERADA ===" -ForegroundColor Cyan
        $cp = Get-Content -LiteralPath $checkpoint -Encoding utf8 | ConvertFrom-Json
        Write-Host "Tarea pendiente: $($cp.task_id)" -ForegroundColor Yellow
        Write-Host "Agente: $($cp.agent_id)" -ForegroundColor Yellow
        Write-Host "Tarea: $($cp.task)" -ForegroundColor Gray
        Write-Host "`nBuscando resultados..." -ForegroundColor Cyan

        $resultados = @()
        if (Test-Path -LiteralPath $resultsDir) {
            $resultados = Get-ChildItem -LiteralPath $resultsDir -Filter "*.json"
        }
        if ($resultados.Count -gt 0) {
            Write-Host "Resultados encontrados: $($resultados.Count)" -ForegroundColor Green
            foreach ($r in $resultados) {
                $data = Get-Content -LiteralPath $r.FullName -Encoding utf8 | ConvertFrom-Json
                Write-Host "  [$($data.status)] $($data.task_id) - $($data.agent_id)" -ForegroundColor Gray
            }
        } else {
            Write-Host "Aun sin resultados. El subagente sigue trabajando." -ForegroundColor Yellow
        }
    } else {
        Write-Host "No hay sesiones pendientes de recuperar." -ForegroundColor Green
    }
    return
}

if (-not $Session -and -not $FromGit -and -not $Pending) {
    Write-Host "Uso: .\Scripts\auto-memory.ps1 -Session   (iniciar sesion)"
    Write-Host "     .\Scripts\auto-memory.ps1 -FromGit  (sincronizar con git)"
    Write-Host "     .\Scripts\auto-memory.ps1 -Pending  (revisar pendientes)"
}
