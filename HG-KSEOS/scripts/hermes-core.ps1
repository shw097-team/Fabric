param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$configPath = Join-Path $resolvedRoot "config\hermes.json"
if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) { throw "ERR_HERMES_CONFIG_MISSING" }
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
$hermes = [string]$config.executable
$hermesPython = [string]$config.python_executable
$hermesHome = [string]$config.canonical_hermes_home
$installRoot = [string]$config.install_root
if (-not (Test-Path -LiteralPath $hermes -PathType Leaf)) { throw "ERR_HERMES_EXECUTABLE_MISSING" }
if (-not (Test-Path -LiteralPath $hermesPython -PathType Leaf)) { throw "ERR_HERMES_PYTHON_MISSING" }
if (-not (Test-Path -LiteralPath $hermesHome -PathType Container)) { throw "ERR_HERMES_HOME_MISSING" }
if (-not (Test-Path -LiteralPath $installRoot -PathType Container)) { throw "ERR_HERMES_INSTALL_ROOT_MISSING" }

$env:HERMES_HOME = $hermesHome
$output = & $hermes --version 2>&1
if ($LASTEXITCODE -ne 0) { throw "ERR_HERMES_VERSION_COMMAND" }
$expected = "Hermes Agent v$($config.release.version) ($($config.release.tag.Substring(1)))"
if (($output -join "`n") -notmatch [regex]::Escape($expected)) { throw "ERR_HERMES_VERSION_MISMATCH" }
$output
exit 0
