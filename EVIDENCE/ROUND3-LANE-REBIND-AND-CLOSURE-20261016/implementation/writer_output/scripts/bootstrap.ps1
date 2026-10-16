param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$BootstrapPython = ""
)

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$venv = Join-Path $resolvedRoot ".venv"
if (Test-Path -LiteralPath $venv) {
    throw "ERR_VENV_EXISTS: $venv"
}
if (-not $BootstrapPython) {
    $candidate = Get-Command python -ErrorAction SilentlyContinue
    if ($candidate) {
        $BootstrapPython = $candidate.Source
    } else {
        $bundled = "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
        if (Test-Path -LiteralPath $bundled) {
            $BootstrapPython = $bundled
        } else {
            throw "ERR_BOOTSTRAP_PYTHON_NOT_FOUND"
        }
    }
}

& $BootstrapPython -m venv $venv
if ($LASTEXITCODE -ne 0) { throw "ERR_VENV_CREATE:$LASTEXITCODE" }
$python = Join-Path $venv "Scripts\python.exe"
$env:PYTHONPATH = Join-Path $resolvedRoot "src"
& $python -m hg_kseos --root $resolvedRoot bootstrap
if ($LASTEXITCODE -ne 0) { throw "ERR_HGK_BOOTSTRAP:$LASTEXITCODE" }
& $python -m hg_kseos --root $resolvedRoot doctor
if ($LASTEXITCODE -ne 0) { throw "ERR_HGK_DOCTOR:$LASTEXITCODE" }

