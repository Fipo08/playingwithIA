param(
    [string]$Category = "",
    [string]$Content = ""
)

if (-not $Category -or -not $Content) {
    Write-Host "Uso: .\Scripts\update-memory.ps1 -Category [perfil|preferencias|proyectos] -Content 'texto'" -ForegroundColor Yellow
    exit 1
}

$validCategories = @("perfil", "preferencias", "proyectos")
if ($Category -notin $validCategories) {
    Write-Host "Categoria invalida. Usa: $($validCategories -join ', ')" -ForegroundColor Red
    exit 1
}

$filePath = "AI/Memory/$Category.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

Add-Content -Path $filePath -Value "`n## [$timestamp]"
Add-Content -Path $filePath -Value $Content

Write-Host "Memoria actualizada: $filePath" -ForegroundColor Green
