param(
    [string]$Comment = "backup"
)

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupName = "OpenCodeUltimate-$timestamp-$Comment"
$backupPath = "Backups/$backupName"
$zipPath = "Backups/$backupName.zip"

Write-Host "Creando backup..." -ForegroundColor Cyan

# Crear directorio
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

# Excluir Backups/ y .git
$exclude = @("Backups", ".git", "node_modules", ".venv")
Get-ChildItem -Path "." -Exclude $exclude | Copy-Item -Destination $backupPath -Recurse -Force

# Comprimir
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($backupPath, $zipPath)

# Eliminar carpeta sin comprimir
Remove-Item -Path $backupPath -Recurse -Force

$size = (Get-Item $zipPath).Length / 1MB
Write-Host "Backup creado: $zipPath ({0:N2} MB)" -f $size -ForegroundColor Green
