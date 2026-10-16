$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'ERR_PROJECT_PYTHON_MISSING' }
$env:PYTHONPATH = Join-Path $ProjectRoot 'src'
& $Python -m hg_kseos --root $ProjectRoot reconcile-tt
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
