$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$scriptPath = Join-Path $repoRoot "scripts\check_windows_bootstrap.ps1"

if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Missing bootstrap script: $scriptPath"
}

$output = & $scriptPath
$exitCode = $LASTEXITCODE

if ($exitCode -notin @(0, 1)) {
    throw "Unexpected exit code from bootstrap script: $exitCode"
}

$requiredSections = @(
    "Robot Sorting RL Windows Bootstrap Check",
    "Python",
    "WSL",
    "Project virtual environment",
    ".venv-win python",
    "Next action"
)

foreach ($section in $requiredSections) {
    if (($output -join "`n") -notmatch [regex]::Escape($section)) {
        throw "Missing expected output section: $section"
    }
}
