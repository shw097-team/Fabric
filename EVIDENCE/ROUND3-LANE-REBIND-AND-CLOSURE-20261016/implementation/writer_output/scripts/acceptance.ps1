param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$python = Join-Path $resolvedRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw "ERR_PROJECT_PYTHON_MISSING" }
$env:PYTHONPATH = Join-Path $resolvedRoot "src"
& $python (Join-Path $resolvedRoot "tools\run_acceptance.py") --root $resolvedRoot
exit $LASTEXITCODE
