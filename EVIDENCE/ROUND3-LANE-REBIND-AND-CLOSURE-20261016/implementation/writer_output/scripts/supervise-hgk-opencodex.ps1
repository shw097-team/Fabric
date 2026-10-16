#Requires -Version 7.0
<#
supervise-hgk-opencodex.ps1 — relay supervisor for the sealed EXECUTE lane (CANDIDATE).

Health-checks the isolated opencodex relay at http://127.0.0.1:<port>/healthz and /v1/models,
restarts it at most MaxRestarts times within WindowSeconds, and emits a JSON receipt. It fails
closed: if the relay cannot be made healthy within budget it stays DEGRADED/BLOCKED rather than
looping forever, and it will NEVER start a process other than the HG-KSEOS launcher script
(scripts/start-hgk-hermes.ps1 -Action StartOpenCodex).

Written for PowerShell 7 (pwsh). Everything is CANDIDATE; no live install is modified.
#>
[CmdletBinding()]
param(
  [ValidateSet("Verify", "Run", "Stop")]
  [string]$Action = "Verify",
  [string]$BindingPath = "",
  [int]$HealthIntervalSeconds = 5,
  [int]$StartupTimeoutSeconds = 30,
  [int]$MaxRestarts = 3,
  [int]$WindowSeconds = 300
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
if ([string]::IsNullOrWhiteSpace($BindingPath)) {
  $BindingPath = Join-Path $root "config\hermes-codex-lane.json"
}
$launcher = Join-Path $root "scripts\start-hgk-hermes.ps1"
$receiptPath = Join-Path $root "var\far-lane-sod-003\evidence\relay-supervisor.receipt.json"


# BEGIN FAR-SOD-010 additive persistence. Existing receipt schema is untouched.
$historyPath = Join-Path (Split-Path -Parent $receiptPath) 'relay-supervisor.receipts.jsonl'
$statePath = Join-Path (Split-Path -Parent $receiptPath) 'relay-supervisor.cooldown.json'
$runLock = $null
$runState = $null
$historyWritten = $false
$cooldownEpoch = $null
function Save-RunState {
  # The exclusive lock serialises manual invocations as well as Scheduler Run.
  $tmp = "$statePath.tmp"
  $runState | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $tmp -Encoding utf8
  [System.IO.File]::Move($tmp, $statePath, $true)
}
function Add-RunHistory($RunReceipt) {
  if ($Action -ne 'Run' -or $null -eq $runState -or $historyWritten) { return }
  $line = [ordered]@{
    run_seq = [long]$runState.run_seq; epoch = $cooldownEpoch
    status = $RunReceipt.status; restart_count = $RunReceipt.restart_count
    healthy = [bool]$RunReceipt.healthy
    receipt_epoch = $RunReceipt.epoch
    checked_utc = (Get-Date).ToUniversalTime().ToString('o')
  } | ConvertTo-Json -Compress -Depth 6
  [System.IO.File]::AppendAllText($historyPath, $line + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
  $script:historyWritten = $true
}
if ($Action -eq 'Run') {
  if ($WindowSeconds -le 0) { throw 'ERR_COOLDOWN_WINDOW_INVALID' }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $receiptPath) | Out-Null
  $runLock = [System.IO.File]::Open("$statePath.lock", 'OpenOrCreate', 'ReadWrite', 'None')
}
try {
  if ($Action -eq 'Run') {
    if (Test-Path -LiteralPath $statePath) {
      $runState = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
      if ($runState.schema -ne 'HGK-RELAY-COOLDOWN/1' -or $null -eq $runState.run_seq -or [long]$runState.run_seq -lt 0) { throw 'ERR_COOLDOWN_STATE_INVALID' }
    } else {
      # Explicit first-install bootstrap only. Missing state with existing history
      # is NOT a fresh install: refuse rather than silently reset the counter.
      if ((Test-Path -LiteralPath $historyPath) -and (Get-Item -LiteralPath $historyPath).Length -gt 0) { throw 'ERR_COOLDOWN_STATE_MISSING_WITH_HISTORY' }
      $runState = [pscustomobject]@{ schema = 'HGK-RELAY-COOLDOWN/1'; run_seq = 0; last_restart_unix = $null; last_restart_epoch = $null; bootstrap_utc = (Get-Date).ToUniversalTime().ToString('o') }
    }
    $runState.run_seq = [long]$runState.run_seq + 1
    $cooldownEpoch = [long][math]::Floor([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / [double]$WindowSeconds)
    Save-RunState
  }
# END FAR-SOD-010 persistence bootstrap; remainder stays inside try/finally.

function Fail-Closed([string]$Code, [string]$Detail) {
  $receipt = [ordered]@{
    schema       = "HGK-RELAY-LEASE/1"
    claim_ceiling = "CANDIDATE_ONLY"
    action       = $Action
    status       = "BLOCKED"
    failure_code = $Code
    detail       = $Detail
    binding_path = $BindingPath
    launcher     = $launcher
    port         = $null
    healthy      = $false
    restart_count = 0
    epoch        = [guid]::NewGuid().ToString()
    checked_utc  = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  }
  Add-RunHistory $receipt
  Write-Output ($receipt | ConvertTo-Json -Depth 6)
  exit 2
}

if (-not (Test-Path -LiteralPath $BindingPath -PathType Leaf)) { Fail-Closed "ERR_RELAY_BINDING_MISSING" $BindingPath }
if (-not (Test-Path -LiteralPath $launcher -PathType Leaf)) { Fail-Closed "ERR_RELAY_LAUNCHER_MISSING" $launcher }

$binding = Get-Content -LiteralPath $BindingPath -Raw -Encoding UTF8 | ConvertFrom-Json
$port = [int]$binding.opencodex_port
if ($port -le 0 -or $port -gt 65535) { Fail-Closed "ERR_RELAY_PORT_INVALID" "$port" }

$healthz = "http://127.0.0.1:$port/healthz"
$models  = "http://127.0.0.1:$port/v1/models"

function Test-RelayHealth {
  param([int]$Port)
  $result = [ordered]@{ healthy = $false; healthz_status = $null; models_ok = $false; detail = "" }
  try {
    $h = Invoke-WebRequest -UseBasicParsing -Uri $healthz -TimeoutSec 3
    $result.healthz_status = [int]$h.StatusCode
    if ([int]$h.StatusCode -ne 200) { $result.detail = "ERR_RELAY_HEALTHZ_$($h.StatusCode)"; return $result }
  } catch {
    $result.detail = "ERR_RELAY_HEALTHZ_UNREACHABLE"
    return $result
  }
  try {
    $m = Invoke-WebRequest -UseBasicParsing -Uri $models -TimeoutSec 3
    if ([int]$m.StatusCode -eq 200) { $result.models_ok = $true }
    else { $result.detail = "ERR_RELAY_MODELS_$($m.StatusCode)"; return $result }
  } catch {
    $result.detail = "ERR_RELAY_MODELS_UNREACHABLE"
    return $result
  }
  $result.healthy = $true
  return $result
}

function Wait-RelayHealthy {
  param([int]$Port, [int]$TimeoutSeconds)
  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  $last = $null
  while ((Get-Date) -lt $deadline) {
    $last = Test-RelayHealth -Port $Port
    if ($last.healthy) { return $last }
    Start-Sleep -Milliseconds 500
  }
  return $last
}

$started = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$restartCount = 0
$restartAttempts = @()

switch ($Action) {
  "Verify" {
    $health = Test-RelayHealth -Port $port
    $receipt = [ordered]@{
      schema = "HGK-RELAY-LEASE/1"; claim_ceiling = "CANDIDATE_ONLY"
      action = "Verify"; status = if ($health.healthy) { "HEALTHY" } else { "DEGRADED" }
      port = $port; healthy = $health.healthy; healthz_status = $health.healthz_status
      models_ok = $health.models_ok; detail = $health.detail
      binding_path = $BindingPath; launcher = $launcher
      restart_count = 0; epoch = [guid]::NewGuid().ToString()
      started_utc = $started; checked_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    Write-Output ($receipt | ConvertTo-Json -Depth 6)
    if ($health.healthy) { exit 0 } else { exit 2 }
  }

  "Stop" {
    # Fail closed: the supervisor only stops a relay it can identify as the launcher's child.
    # Without a verified lease it does not kill anything.
    $receipt = [ordered]@{
      schema = "HGK-RELAY-LEASE/1"; claim_ceiling = "CANDIDATE_ONLY"
      action = "Stop"; status = "NOOP_NO_VERIFIED_LEASE"
      port = $port; healthy = (Test-RelayHealth -Port $port).healthy
      binding_path = $BindingPath; launcher = $launcher
      restart_count = 0; epoch = [guid]::NewGuid().ToString()
      detail = "stop requires a verified owned lease; refusing to kill an unidentified process"
      checked_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    Write-Output ($receipt | ConvertTo-Json -Depth 6)
    exit 0
  }

  "Run" {
    $health = Test-RelayHealth -Port $port
    $windowStart = Get-Date
    while (-not $health.healthy -and $restartCount -lt $MaxRestarts) {
      if (((Get-Date) - $windowStart).TotalSeconds -gt $WindowSeconds) { break }
      # At most ONE reserved attempt in this epoch, AND a full WindowSeconds
      # since the previous attempt (prevents adjacent-bucket boundary bursts).
      $nowUnix = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
      $attemptEpoch = [long][math]::Floor($nowUnix / [double]$WindowSeconds)
      if (($null -ne $runState.last_restart_epoch -and [long]$runState.last_restart_epoch -eq $attemptEpoch) -or
          ($null -ne $runState.last_restart_unix -and ($nowUnix - [long]$runState.last_restart_unix) -lt $WindowSeconds)) { break }
      # Reserve durably BEFORE calling the only sanctioned launcher; failed starts
      # consume the cooldown too. No new launcher, process kill, or model routing.
      $runState.last_restart_unix = $nowUnix
      $runState.last_restart_epoch = $attemptEpoch
      Save-RunState
      $restartCount++
      $attempt = [ordered]@{ index = $restartCount; at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ") }
      try {
        # ONLY the HG-KSEOS launcher script may be started here.
        & $launcher -Action StartOpenCodex
        $attempt.launcher_exit = $LASTEXITCODE
      } catch {
        $attempt.launcher_error = $_.Exception.Message
      }
      $health = Wait-RelayHealthy -Port $port -TimeoutSeconds $StartupTimeoutSeconds
      $attempt.healthy = $health.healthy
      $restartAttempts += $attempt
    }

    $status = if ($health.healthy) { "HEALTHY" } else { "BLOCKED" }
    $receipt = [ordered]@{
      schema = "HGK-RELAY-LEASE/1"; claim_ceiling = "CANDIDATE_ONLY"
      action = "Run"; status = $status
      port = $port; healthy = $health.healthy; healthz_status = $health.healthz_status
      models_ok = $health.models_ok; detail = $health.detail
      binding_path = $BindingPath; launcher = $launcher
      restart_count = $restartCount; max_restarts = $MaxRestarts; window_seconds = $WindowSeconds
      restart_attempts = $restartAttempts
      epoch = [guid]::NewGuid().ToString()
      started_utc = $started; checked_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $receiptPath) | Out-Null
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
    Add-RunHistory $receipt
    Write-Output ($receipt | ConvertTo-Json -Depth 8)
    if ($health.healthy) { exit 0 } else { exit 2 }
  }
}

} catch {
  # Preserve fail-closed exit behaviour; exceptions still leave a Run audit line
  # once a run_seq has been allocated. Corrupt/unreadable state fails before it.
  if ($Action -eq 'Run' -and $null -ne $runState -and -not $historyWritten) {
    Add-RunHistory ([ordered]@{ status = 'BLOCKED'; restart_count = $restartCount; healthy = $false; epoch = $null })
  }
  throw
} finally {
  if ($null -ne $runLock) { $runLock.Dispose() }
}
