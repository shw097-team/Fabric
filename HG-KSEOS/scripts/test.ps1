param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$python = Join-Path $resolvedRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) { throw "ERR_PROJECT_PYTHON_MISSING" }
$env:PYTHONPATH = (Join-Path $resolvedRoot "src")
& $python -m unittest discover -s (Join-Path $resolvedRoot "tests") -t $resolvedRoot -v
exit $LASTEXITCODE

