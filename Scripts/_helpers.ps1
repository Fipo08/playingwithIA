function Get-ActiveUser {
    $jsonPath = "AI/Memory/users/users.json"
    if (Test-Path $jsonPath) {
        $config = Get-Content $jsonPath -Raw | ConvertFrom-Json
        return $config.active
    }
    return $null
}

function Get-UserPath {
    $user = Get-ActiveUser
    if ($user) {
        return "AI/Memory/users/$user"
    }
    return "AI/Memory/users/_template"
}

function Get-UserFile {
    param([string]$Name)
    $userPath = Get-UserPath
    return "$userPath/$Name"
}
