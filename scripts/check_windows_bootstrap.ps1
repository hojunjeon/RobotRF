$ErrorActionPreference = "Stop"

function Write-Section {
    param([string] $Name)
    Write-Output ""
    Write-Output "## $Name"
}

function Test-CommandExists {
    param([string] $Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvConfig = Join-Path $repoRoot ".venv\pyvenv.cfg"
$hasProblem = $false

Write-Output "Robot Sorting RL Windows Bootstrap Check"
Write-Output "Repository: $repoRoot"

Write-Section "Python"
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
$pyCommand = Get-Command py -ErrorAction SilentlyContinue

if ($pythonCommand) {
    Write-Output "python: FOUND ($($pythonCommand.Source))"
} else {
    Write-Output "python: MISSING"
    $hasProblem = $true
}

if ($pyCommand) {
    Write-Output "py launcher: FOUND ($($pyCommand.Source))"
} else {
    Write-Output "py launcher: MISSING"
}

Write-Section "WSL"
if (Test-CommandExists "wsl") {
    Write-Output "wsl.exe: FOUND"
    $wslListOutput = & wsl --list --all --verbose 2>&1
    $wslExitCode = $LASTEXITCODE
    if ($wslExitCode -eq 0) {
        Write-Output "wsl distributions:"
        $wslListOutput | ForEach-Object { Write-Output "  $_" }
    } else {
        Write-Output "wsl distributions: unavailable"
        $wslListOutput | ForEach-Object { Write-Output "  $_" }
        $hasProblem = $true
    }
} else {
    Write-Output "wsl.exe: MISSING"
    Write-Output "wsl status: optional for Windows smoke tests"
}

Write-Section "Project virtual environment"
if (Test-Path -LiteralPath $venvConfig) {
    Write-Output ".venv: FOUND"
    $homeLine = Select-String -LiteralPath $venvConfig -Pattern "^home = " -ErrorAction SilentlyContinue
    if ($homeLine) {
        $homePath = $homeLine.Line -replace "^home = ", ""
        Write-Output ".venv home: $homePath"
        if (-not (Test-Path -LiteralPath $homePath)) {
            Write-Output ".venv home status: MISSING"
            $hasProblem = $true
        } else {
            Write-Output ".venv home status: FOUND"
        }
    }
} else {
    Write-Output ".venv: MISSING"
    $hasProblem = $true
}

Write-Section ".venv python"
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    Write-Output ".venv python path: $venvPython"
    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $venvPythonVersion = & $venvPython --version 2>&1
    $venvPythonExitCode = $LASTEXITCODE
    $ErrorActionPreference = $previousErrorActionPreference
    if ($venvPythonExitCode -eq 0) {
        Write-Output ".venv python status: RUNNABLE"
        $venvPythonVersion | ForEach-Object { Write-Output ".venv python version: $_" }
    } else {
        Write-Output ".venv python status: BROKEN"
        $venvPythonVersion | ForEach-Object { Write-Output "  $_" }
        $hasProblem = $true
    }
} else {
    Write-Output ".venv python path: MISSING"
    $hasProblem = $true
}

Write-Section "Next action"
if ($hasProblem) {
    Write-Output "Repair the Windows .venv first, then rerun this script."
    Write-Output "Expected command after repair: .\.venv\Scripts\python.exe -m pytest"
    exit 1
}

Write-Output "Environment bootstrap looks ready."
Write-Output "Run: .\.venv\Scripts\python.exe -m pytest"
Write-Output "Run: .\.venv\Scripts\python.exe scripts\check_runtime.py"
exit 0
