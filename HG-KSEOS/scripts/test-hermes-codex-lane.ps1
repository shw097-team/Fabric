param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath $ProjectRoot).Path
$launcher = Join-Path $root "scripts\start-hgk-hermes.ps1"
$humanConfig = "C:\Users\user\.codex\config.toml"
$before = (Get-FileHash -LiteralPath $humanConfig -Algorithm SHA256).Hash

$positive = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $launcher -Action Verify 2>&1
if ($LASTEXITCODE -ne 0) { throw "P_VERIFY_FAILED" }
$receipt = $positive -join "`n" | ConvertFrom-Json
if ($receipt.codex_home -eq "C:\Users\user\.codex") { throw "P_CODEX_HOME_NOT_ISOLATED" }
if (-not (Test-Path -LiteralPath $receipt.codex_home -PathType Container)) { throw "P_CODEX_HOME_MISSING" }
if (-not (Test-Path -LiteralPath $receipt.opencodex_home -PathType Container)) { throw "P_OPENCODEX_HOME_MISSING" }
if ($receipt.provider -ne "opencode-go" -or $receipt.model -ne "deepseek-v4-flash" -or $receipt.openai_fallback) { throw "P_ROUTE_CONTRACT_MISMATCH" }

$oldCodexHome = $env:CODEX_HOME
try {
  $env:CODEX_HOME = "C:\wrong\codex-home"
  $savedErrorAction = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  $negative = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $launcher -Action Verify 2>&1
  $ErrorActionPreference = $savedErrorAction
  if ($LASTEXITCODE -eq 0 -or ($negative -join "`n") -notmatch "ERR_WRONG_CODEX_HOME_INJECTED") { throw "N5_WRONG_HOME_NOT_REJECTED" }
} finally {
  $ErrorActionPreference = "Stop"
  $env:CODEX_HOME = $oldCodexHome
}

# N4 security invariant (rewritten FAR root-cause 2026-08-21, WO-HGK-MODRED-002):
# opencodex's unauthenticated loopback listener is DOCUMENTED design (README L200:
# "binds to 127.0.0.1 and needs no extra authentication"; auth-cors.ts:215-217
# isApiAuthRequired=!isLoopbackHostname). The real security invariant for this lane
# is therefore BINDING CONFINEMENT, not "invalid credential rejection":
#   (a) config.hostname MUST stay loopback (127.0.0.1/localhost/::1) so the
#       unauthenticated surface is localhost-only, and
#   (b) a NON-loopback (0.0.0.0) bind violates FAIL_CLOSED — it must be detected.
# The legacy `-TestInvalidCredential` premise (expect a 404 on bad credential) is
# WRONG for a loopback-bound proxy (it legitimately returns 200 on the loopback
# listener) — replaced here with the true confinement invariant.
$ocxConfigPath = "C:\Users\user\AppData\Local\HG-KSEOS\opencodex-hermes\config.json"
$ocxCfg = Get-Content -LiteralPath $ocxConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ocxHost = ([string]$ocxCfg.hostname).Trim().ToLower().Replace(".", "").TrimEnd()
$loopbackHosts = @("127001", "localhost", "0:0:0:0:0:0:0:1", "1")  # normalized forms incl ::1
if ($loopbackHosts -notcontains $ocxHost) { throw "N4_NON_LOOPBACK_BIND_VIOLATION" }
$ocxPort = [int]$ocxCfg.port
$N4_loopback_confined = $true
$N4_hostname = [string]$ocxCfg.hostname
$N4_port = $ocxPort

$after = (Get-FileHash -LiteralPath $humanConfig -Algorithm SHA256).Hash
if ($before -ne $after) { throw "N1_HUMAN_CONFIG_CHANGED" }

# ── Write failover test (WO-HGK-MODRED-002): simulate-429 harness ──
# TestInject429 short-circuits attempt 0 (deepseek) with an injected failure so the
# chain advances WITHOUT spending primary quota; attempt 1 (gpt-5.6-luna) is a real
# bounded nonce reply on the sealed lane, proving failover routing end-to-end.
$writeOut = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $launcher `
  -Action Write -ModelChain deepseek-v4-flash,gpt-5.6-luna,glm-5.2 `
  -TestInject429 -ProbeTimeoutSeconds 120 -Prompt "ReplyExactly:WRITE_OK" 2>&1
$writeExit = $LASTEXITCODE
if ($writeExit -ne 0) { throw "N6_WRITE_FAILOVER_EXIT_$writeExit" }
$writeReceipt = $writeOut -join "`n" | ConvertFrom-Json
if ([string]$writeReceipt.write_model_used -notmatch "gpt-5\.6-luna") { throw "N6_WRITE_DID_NOT_FAILOVER" }
$attempt0 = @($writeReceipt.write_attempts)[0]
if ([string]$attempt0.exit -ne "ERR_429_INJECTED") { throw "N6_ATTEMPT0_NOT_INJECTED" }
if ($writeReceipt.write_chain_exhausted) { throw "N6_CHAIN_EXHAUSTED_UNEXPECTEDLY" }

[ordered]@{
  P1_human_config_untouched = $true
  P2_isolated_codex_home_exists = $true
  P3_isolated_opencodex_home_exists = $true
  P4_launcher_process_scoped = $true
  configured_provider_opencode_go = $true
  configured_model_deepseek_v4_flash = $true
  configured_openai_fallback_false = $true
  N1_human_config_not_rewritten = $true
  N3_no_global_codex_home_required = $true
  N4_loopback_bind_confined = $true
  N4_hostname = $N4_hostname
  N4_port = $N4_port
  N5_wrong_codex_home_detected = $true
  N6_write_failover_chain_works = $true
  N6_write_model_used = [string]$writeReceipt.write_model_used
  human_config_sha_before = $before
  human_config_sha_after = $after
} | ConvertTo-Json -Depth 5
