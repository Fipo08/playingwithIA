Write-Host "=== OpenCode Ultimate — Status ===" -ForegroundColor Cyan
Write-Host ""

# Versión
$version = "2.0"
Write-Host "Version: v$version" -ForegroundColor Yellow

# Git
if (Test-Path ".git") {
    $branch = git branch --show-current
    $log = git log --oneline -3 2>$null
    $changes = git status --porcelain | Measure-Object | Select-Object -ExpandProperty Count
    Write-Host "Branch: $branch"
    Write-Host "Cambios: $changes sin commit"
    Write-Host "Ultimos commits:"
    $log | ForEach-Object { Write-Host "  $_" }
}

# Estructura
Write-Host "`n--- Recursos ---" -ForegroundColor Cyan
$resources = @(
    @("Personas", (Get-ChildItem "AI/Personas/*.md" -Exclude "README.md" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Workflows", (Get-ChildItem "AI/Workflows/*.md" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Prompts", (Get-ChildItem "AI/Prompts/*.md" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Templates", (Get-ChildItem "AI/Templates/*.md" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Knowledge Base", (Get-ChildItem "AI/KnowledgeBase/*.md" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Scripts", (Get-ChildItem "Scripts/*.ps1" | Measure-Object | Select-Object -ExpandProperty Count)),
    @("Proyectos", ((Get-ChildItem "Projects" -Directory | Measure-Object | Select-Object -ExpandProperty Count) - 0))
)
foreach ($r in $resources) {
    Write-Host "  $($r[0]): $($r[1])"
}

# Proyectos activos
if (Test-Path "AI/Memory/proyectos.md") {
    $proyectos = Get-Content "AI/Memory/proyectos.md" | Select-String "^-\s+\*\*"
    if ($proyectos) {
        Write-Host "`n--- Proyectos activos ---" -ForegroundColor Cyan
        $proyectos | ForEach-Object { Write-Host "  $_" }
    }
}

Write-Host ""
Write-Host "=== Fin ===" -ForegroundColor Green
