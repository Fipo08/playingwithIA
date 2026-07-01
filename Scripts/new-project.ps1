param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    [string]$Description = "",
    [string]$Stack = "",
    [switch]$Register
)

$projectPath = "Projects/$Name"

if (Test-Path $projectPath) {
    Write-Host "El proyecto '$Name' ya existe en $projectPath" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Path "$projectPath/src" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectPath/tests" -Force | Out-Null
New-Item -ItemType Directory -Path "$projectPath/docs" -Force | Out-Null

"# $Name`n`n$Description" | Out-File -FilePath "$projectPath/README.md" -Encoding utf8
"# node_modules`n.env`n" | Out-File -FilePath "$projectPath/.gitignore" -Encoding utf8
"# Configura variables aqui`nAPI_KEY=" | Out-File -FilePath "$projectPath/.env.example" -Encoding utf8

Write-Host "Proyecto creado: $projectPath" -ForegroundColor Green

if ($Register) {
    $entry = "`n- **$Name** — $Description`n  - Estado: En desarrollo`n  - Stack: $Stack"
    Add-Content -Path "AI/Memory/proyectos.md" -Value $entry -Encoding utf8
    Write-Host "Registrado en AI/Memory/proyectos.md" -ForegroundColor Yellow
}

Write-Host "`nSiguiente paso: cd $projectPath y empieza a codificar" -ForegroundColor Cyan
