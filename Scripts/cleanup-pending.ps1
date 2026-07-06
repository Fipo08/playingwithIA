param(
    [switch]$Status
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pendingDir = Join-Path $scriptDir "..\AI\Memory\pending"
$pendingDir = Resolve-Path $pendingDir
$resultsDir = Join-Path $pendingDir "results"
$checkpoint = Join-Path $pendingDir "checkpoint.json"

if ($Status) {
    $pendientes = @()
    if (Test-Path -LiteralPath $resultsDir) {
        $pendientes = Get-ChildItem -LiteralPath $resultsDir -Filter "*.json"
    }
    if ($pendientes.Count -gt 0) {
        Write-Host "Resultados pendientes: $($pendientes.Count)" -ForegroundColor Yellow
        foreach ($p in $pendientes) {
            $data = Get-Content -LiteralPath $p.FullName -Encoding utf8 | ConvertFrom-Json
            Write-Host "  - $($data.task_id) ($($data.agent_id)): $($data.status)" -ForegroundColor Gray
        }
    } else {
        Write-Host "No hay resultados pendientes." -ForegroundColor Green
    }
    if (Test-Path -LiteralPath $checkpoint) {
        $cp = Get-Content -LiteralPath $checkpoint -Encoding utf8 | ConvertFrom-Json
        Write-Host "Checkpoint activo: $($cp.task_id) -> $($cp.agent_id)" -ForegroundColor Cyan
    }
    return
}

if (Test-Path -LiteralPath $resultsDir) {
    Remove-Item -LiteralPath "$resultsDir\*" -Force -ErrorAction SilentlyContinue
    Write-Host "Resultados eliminados." -ForegroundColor Gray
}
if (Test-Path -LiteralPath $checkpoint) {
    Remove-Item -LiteralPath $checkpoint -Force
    Write-Host "Checkpoint eliminado." -ForegroundColor Gray
}

Write-Host "Pendientes limpiados." -ForegroundColor Green
