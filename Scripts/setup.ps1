param([switch]$Quiet)

. "$PSScriptRoot\_helpers.ps1"

function Write-Step {
    param([string]$Label, [string]$Status, [string]$Icon)
    if (-not $Quiet) { Write-Host "$Icon [$Status] $Label" }
}

Write-Host "=== OpenCode Ultimate — Setup Check ===" -ForegroundColor Cyan
Write-Host ""

# 1. Git
try { $gitVer = git --version; Write-Step "Git: $gitVer" "OK" "✅" }
catch { Write-Step "Git no encontrado" "FAIL" "❌" }

# 2. Ollama
try {
    $ollamaModels = ollama list 2>$null
    $modelCount = ($ollamaModels | Select-String "G ").Count
    Write-Step "Ollama ($modelCount modelos)" "OK" "✅"
} catch { Write-Step "Ollama no disponible" "FAIL" "❌" }

# 3. Git repo
if (Test-Path ".git") {
    $branch = git branch --show-current
    $status = git status --porcelain | Measure-Object | Select-Object -ExpandProperty Count
    Write-Step "Git repo ($branch, $status cambios sin commit)" "OK" "✅"
} else { Write-Step "Git repo no inicializado" "WARN" "⚠️" }

# 4. Estructura del proyecto
$dirs = @("AI/Memory","AI/Personas","AI/Prompts","AI/Rules","AI/Templates","AI/Workflows","Documentation","Scripts","Projects")
$ok = 0; $fail = 0
foreach ($d in $dirs) { if (Test-Path $d) { $ok++ } else { $fail++ } }
Write-Step "Directorios base ($ok/$($dirs.Count) presentes)" $(if ($fail -eq 0) {"OK"} else {"WARN"}) $(if ($fail -eq 0) {"✅"} else {"⚠️"})

# 5. Usuarios
$userDir = "AI/Memory/users"
if (Test-Path $userDir) {
    $userCount = (Get-ChildItem "$userDir/*" -Directory | Where-Object { $_ -notlike "*_template*" }).Count
    Write-Step "Usuarios registrados: $userCount" "OK" "✅"
} else { Write-Step "Directorios de usuario no encontrados" "WARN" "⚠️" }

Write-Host ""
Write-Host "=== Setup completo ===" -ForegroundColor Green
