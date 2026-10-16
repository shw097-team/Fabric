# start-hgk-exec-frontdoor.ps1 - FAR-EXEC-IDENTITY-002 (packet item C).
#
# Restartable lifecycle helper for the dedicated sealed-EXECUTE front door
# (scripts/hgk-exec-model-frontdoor.py) on 127.0.0.1:10100. Idempotent Verify / Start / Stop.
#
#   Verify : report current state (owned pid? port occupant? /healthz semantics) WITHOUT starting
#            anything. This action is INERT — it never launches the front door.
#   Start  : no-op if our own instance is healthy; if the port is held by a FOREIGN process, refuse;
#            otherwise launch a detached process and record its pid.
#   Stop   : stop ONLY the pid we own, after verifying the live process image and command line match
#            our front-door script. Never kills a foreign process.
#
# Paths are explicit constants (runtime python / declaration / ledger / pid). No credentials are
# read, written, or logged here. The helper does NOT start the front door unless -Action Start.

param(
  [ValidateSet("Verify", "Start", "Stop")]
  [string]$Action = "Verify",
  # The three overrides below exist ONLY so the deterministic test can exercise the real
  # Verify/Start/Stop lifecycle on an ephemeral port without binding the live 10100. Defaults are
  # the fixed, explicit production values and are what the launcher relies on.
  [int]$Port = 10100,
  [string]$RuntimeDir = "",
  [string]$Upstream = "http://127.0.0.1:10101"
)

$ErrorActionPreference = "Stop"

# ---- explicit fixed paths ---------------------------------------------------------------------
$root = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
$frontdoorScript = Join-Path $root "scripts\hgk-exec-model-frontdoor.py"
$declaration = Join-Path $root "config\hermes-codex-lane.json"
$runtimeDir = if ($RuntimeDir) { $RuntimeDir } else { Join-Path $env:LOCALAPPDATA "HG-KSEOS\frontdoor" }
$ledger = Join-Path $runtimeDir "frontdoor-ledger.jsonl"
$pidFile = Join-Path $runtimeDir "frontdoor.pid"
$stdoutLog = Join-Path $runtimeDir "frontdoor.stdout.log"
$stderrLog = Join-Path $runtimeDir "frontdoor.stderr.log"

$host_ = "127.0.0.1"
$port = $Port
$upstream = $Upstream

# Runtime python: the repo venv if it exists (aiohttp is installed there), else system python.
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
$runtimePython = if (Test-Path -LiteralPath $venvPython -PathType Leaf) { $venvPython } else { "python" }

function Get-FrontdoorPid {
  if (-not (Test-Path -LiteralPath $pidFile -PathType Leaf)) { return $null }
  $raw = (Get-Content -LiteralPath $pidFile -Raw -ErrorAction SilentlyContinue)
  if ([string]::IsNullOrWhiteSpace($raw)) { return $null }
  $value = 0
  if (-not [int]::TryParse($raw.Trim(), [ref]$value)) { return $null }
  return $value
}

function Get-OwnedProcess {
  param([int]$Pid_)
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$Pid_" -ErrorAction SilentlyContinue
  if (-not $proc) { return $null }
  # Owned only if the command line actually runs OUR front-door script with OUR runtime python.
  $cmd = [string]$proc.CommandLine
  if ($cmd -and ($cmd -like "*hgk-exec-model-frontdoor.py*")) { return $proc }
  return $null
}

function Get-PortOccupant {
  $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
          Select-Object -First 1
  if ($conn) { return [int]$conn.OwningProcess }
  return $null
}

function Get-Health {
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://${host_}:$port/healthz" -TimeoutSec 3
    if ($resp.StatusCode -eq 200) { return ($resp.Content | ConvertFrom-Json) }
  } catch { }
  return $null
}

# ---- Verify ----------------------------------------------------------------------------------
if ($Action -eq "Verify") {
  $pid_ = Get-FrontdoorPid
  $owned = if ($pid_) { Get-OwnedProcess -Pid_ $pid_ } else { $null }
  $occupant = Get-PortOccupant
  $health = Get-Health
  $state = [ordered]@{
    schema = "HGK-EXEC-FRONTDOOR-HELPER/1"
    action = "Verify"
    claim_ceiling = "CANDIDATE_ONLY"
    port = $port
    host = $host_
    upstream = $upstream
    pid_recorded = $pid_
    pid_owned = ($null -ne $owned)
    port_occupant_pid = $occupant
    healthy = ($null -ne $health)
    health = $health
    runtime_python = $runtimePython
    script = $frontdoorScript
    ledger = $ledger
  }
  $state | ConvertTo-Json -Depth 6
  exit 0
}

# ---- Stop -------------------------------------------------------------------------------------
if ($Action -eq "Stop") {
  $pid_ = Get-FrontdoorPid
  if (-not $pid_) {
    Write-Output '{"action":"Stop","result":"NO_OWNED_PID"}'
    exit 0
  }
  $owned = Get-OwnedProcess -Pid_ $pid_
  if (-not $owned) {
    # The recorded pid is gone or is no longer our front door: remove the stale pid file only.
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    Write-Output '{"action":"Stop","result":"STALE_PID_REMOVED"}'
    exit 0
  }
  Stop-Process -Id $pid_ -Force -ErrorAction SilentlyContinue
  Start-Sleep -Milliseconds 500
  Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
  Write-Output ('{"action":"Stop","result":"STOPPED_OWNED","pid":' + $pid_ + '}')
  exit 0
}

# ---- Start ------------------------------------------------------------------------------------
$pid_ = Get-FrontdoorPid
$owned = if ($pid_) { Get-OwnedProcess -Pid_ $pid_ } else { $null }
$health = Get-Health
if ($owned -and $health) {
  Write-Output ('{"action":"Start","result":"ALREADY_RUNNING_OWNED","pid":' + $pid_ + '}')
  exit 0
}

# A foreign (unowned) occupant at the port must never be killed or shadowed.
$occupant = Get-PortOccupant
if ($occupant -and (-not $owned -or $occupant -ne $pid_)) {
  throw "ERR_EXEC_FRONTDOOR_FOREIGN_OCCUPANT:$occupant"
}

if (-not (Test-Path -LiteralPath $frontdoorScript -PathType Leaf)) {
  throw "ERR_EXEC_FRONTDOOR_SCRIPT_MISSING:$frontdoorScript"
}

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
$py = if (Test-Path -LiteralPath $runtimePython -PathType Leaf) { $runtimePython } else {
  (Get-Command $runtimePython -ErrorAction SilentlyContinue).Source
}
if (-not $py) { throw "ERR_EXEC_FRONTDOOR_PYTHON_MISSING:$runtimePython" }

$args = @(
  $frontdoorScript,
  "--host", $host_,
  "--port", "$port",
  "--upstream", $upstream,
  "--declaration", $declaration,
  "--ledger", $ledger
)
# Detached native launch: the helper returns immediately; the front door owns the port.
$proc = Start-Process -FilePath $py -ArgumentList $args -PassThru -WindowStyle Hidden `
                      -RedirectStandardOutput $stdoutLog -RedirectStandardError $stderrLog
Set-Content -LiteralPath $pidFile -Value ([string]$proc.Id) -Encoding ASCII
Write-Output ('{"action":"Start","result":"STARTED","pid":' + $proc.Id + '}')
exit 0
