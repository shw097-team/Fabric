param(
  [ValidateSet("Verify", "StartOpenCodex", "Probe", "Hermes", "Write")]
  [string]$Action = "Verify",
  [string[]]$HermesArgs = @(),
  [string[]]$ModelChain = @(),
  [string]$Prompt = "",
  [string]$Nonce = "HGK_CODEX_PROVIDER_LANE_NONCE_OK",
  [ValidateRange(30, 600)]
  [int]$ProbeTimeoutSeconds = 180,
  [switch]$TestInvalidCredential,
  [switch]$TestInject429
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
$bindingPath = Join-Path $root "config\hermes-codex-lane.json"
$binding = Get-Content -LiteralPath $bindingPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Expand-LanePath([string]$Value) {
  return [Environment]::ExpandEnvironmentVariables($Value)
}

function Import-ProcessCredentialFromEnvFile([string]$Name, [string]$Path) {
  $existing = [Environment]::GetEnvironmentVariable($Name, "Process")
  if (-not [string]::IsNullOrWhiteSpace($existing)) { return "existing-process-env" }
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "ERR_CREDENTIAL_SOURCE_MISSING" }
  foreach ($line in [IO.File]::ReadAllLines($Path)) {
    if ($line -notmatch '^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$') { continue }
    if ($Matches[1] -ne $Name) { continue }
    $value = $Matches[2].Trim()
    if (($value.StartsWith('"') -and $value.EndsWith('"')) -or
        ($value.StartsWith("'") -and $value.EndsWith("'"))) {
      $value = $value.Substring(1, $value.Length - 2)
    }
    if ([string]::IsNullOrWhiteSpace($value)) { throw "ERR_CREDENTIAL_SOURCE_EMPTY" }
    [Environment]::SetEnvironmentVariable($Name, $value, "Process")
    return "canonical-hermes-profile-env"
  }
  throw "ERR_CREDENTIAL_REFERENCE_NOT_FOUND"
}

$humanConfig = Expand-LanePath $binding.human_codex_config
$codexHome = Expand-LanePath $binding.hermes_codex_home
$openCodexHome = Expand-LanePath $binding.hermes_opencodex_home
$codexExe = Expand-LanePath $binding.codex_executable
$openCodexRoot = Expand-LanePath $binding.opencodex_root
$bunExe = Join-Path $openCodexRoot "node_modules\bun\bin\bun.exe"
$openCodexEntry = Join-Path $openCodexRoot "src\cli\index.ts"
$hermesExe = [string]$binding.hermes_executable
$hermesPython = [string]$binding.hermes_python
$hermesSource = [string]$binding.hermes_source
$hermesHome = [string]$binding.hermes_home
$credentialSourceFile = Expand-LanePath ([string]$binding.credential_source_file)
$port = [int]$binding.opencodex_port

foreach ($name in @("CODEX_HOME", "OPENCODEX_HOME")) {
  $permanentUser = [Environment]::GetEnvironmentVariable($name, "User")
  $permanentMachine = [Environment]::GetEnvironmentVariable($name, "Machine")
  if ($permanentUser -or $permanentMachine) { throw "ERR_GLOBAL_${name}_FORBIDDEN" }
}
if ($env:CODEX_HOME -and ([IO.Path]::GetFullPath($env:CODEX_HOME) -ne [IO.Path]::GetFullPath($codexHome))) {
  throw "ERR_WRONG_CODEX_HOME_INJECTED"
}
if ($env:OPENCODEX_HOME -and ([IO.Path]::GetFullPath($env:OPENCODEX_HOME) -ne [IO.Path]::GetFullPath($openCodexHome))) {
  throw "ERR_WRONG_OPENCODEX_HOME_INJECTED"
}

foreach ($directory in @($codexHome, $openCodexHome, $hermesSource, $hermesHome)) {
  if (-not (Test-Path -LiteralPath $directory -PathType Container)) { throw "ERR_ISOLATED_HOME_MISSING:$directory" }
}
foreach ($file in @($humanConfig, $codexExe, $bunExe, $openCodexEntry, $hermesExe, $hermesPython)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "ERR_RUNTIME_FILE_MISSING:$file" }
}

$humanText = Get-Content -LiteralPath $humanConfig -Raw -Encoding UTF8
if ($humanText -match '(?m)^\s*openai_base_url\s*=\s*"http://127\.0\.0\.1:1010[01]/v1"' -or
    $humanText -match '(?m)^\s*model_catalog_json\s*=.*opencodex') {
  throw "ERR_SHARED_MUTABLE_CODEX_CONFIG_STILL_ACTIVE"
}
$actualCodexHash = (Get-FileHash -LiteralPath $codexExe -Algorithm SHA256).Hash
if ($actualCodexHash -ne [string]$binding.codex_sha256) { throw "ERR_CODEX_HASH_MISMATCH" }

# These assignments affect this launcher and its children only. No setx or registry write is used.
$env:CODEX_HOME = $codexHome
$env:OPENCODEX_HOME = $openCodexHome
$env:HERMES_CODEX_HOME = $codexHome
$env:HERMES_OPENCODEX_HOME = $openCodexHome
$env:HERMES_HOME = $hermesHome
$env:Path = "$(Split-Path -Parent $codexExe);$env:Path"

$codexVersionReadback = (& $codexExe --version 2>&1) -join "`n"
Push-Location $openCodexRoot
try { $openCodexVersionReadback = (& $bunExe run $openCodexEntry --version 2>&1) -join "`n" }
finally { Pop-Location }

$receipt = [ordered]@{
  task_id = [string]$binding.task_id
  action = $Action
  human_config = $humanConfig
  human_config_sha256 = (Get-FileHash -LiteralPath $humanConfig -Algorithm SHA256).Hash
  codex_home = $env:CODEX_HOME
  opencodex_home = $env:OPENCODEX_HOME
  codex_executable = $codexExe
  codex_version_readback = $codexVersionReadback
  codex_sha256 = $actualCodexHash
  opencodex_root = $openCodexRoot
  opencodex_version_readback = $openCodexVersionReadback
  opencodex_port = $port
  hermes_executable = $hermesExe
  hermes_python = $hermesPython
  hermes_source = $hermesSource
  hermes_home = $env:HERMES_HOME
  provider = [string]$binding.provider
  model = [string]$binding.model
  openai_fallback = [bool]$binding.openai_fallback
  process_scoped = $true
}

if ($Action -eq "Verify") {
  $receipt | ConvertTo-Json -Depth 6
  exit 0
}

$credentialName = [string]$binding.credential_env
$credentialSource = Import-ProcessCredentialFromEnvFile -Name $credentialName -Path $credentialSourceFile
$receipt.credential_source = $credentialSource
if ($TestInvalidCredential) {
  if ($Action -ne "Probe") { throw "ERR_TEST_INVALID_CREDENTIAL_REQUIRES_PROBE" }
  [Environment]::SetEnvironmentVariable($credentialName, "HGK_INTENTIONALLY_INVALID_TEST_CREDENTIAL", "Process")
  $receipt.credential_source = "intentional-invalid-test-fixture"
}

if ($Action -eq "StartOpenCodex") {
  Push-Location $openCodexRoot
  try { & $bunExe run $openCodexEntry start --port $port; exit $LASTEXITCODE }
  finally { Pop-Location }
}

if ($Action -eq "Hermes") {
  try { $health = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$port/healthz" -TimeoutSec 3 }
  catch { throw "ERR_ISOLATED_OPENCODEX_NOT_HEALTHY" }
  if ($health.StatusCode -ne 200) { throw "ERR_ISOLATED_OPENCODEX_NOT_HEALTHY" }
  & $hermesExe @HermesArgs
  exit $LASTEXITCODE
}

# -- Write action: model-failover chain on the sealed lane (WO-HGK-MODRED-002) --
# Runs codex.exe --model <m> over the chain; on 429/non-zero, re-invokes with next
# model. Probe/Verify FAIL_CLOSED single-model gate stays intact (this branch only).
if ($Action -eq "Write") {
  if ([string]::IsNullOrWhiteSpace($Prompt)) { throw "ERR_CODEX_WRITE_REQUIRES_PROMPT" }
  $chain = @()
  if ($ModelChain.Count -gt 0) {
    # -File spawn style passes -ModelChain a,b,c as a single element; normalize by
    # splitting each element on commas so both real arrays and joined strings work.
    foreach ($mc in $ModelChain) {
      foreach ($part in ([string]$mc).Split(',')) {
        $p = $part.Trim()
        if ($p) { $chain += $p }
      }
    }
  }
  else {
    $chain = @([string]$binding.model)
    foreach ($fm in @($binding.model_fallbacks)) { $chain += [string]$fm }
    $chain = @($chain | Where-Object { $_ -and -not [string]::IsNullOrWhiteSpace($_)})
  }
  # Qualify bare model ids with the lane provider so opencodex routes them through
  # the opencode-go provider. opencodex reserves the bare gpt-* namespace for the
  # canonical OpenAI provider, so gpt-5.6-luna MUST be passed as <provider>/<model>.
  $prefixed = @()
  foreach ($m in $chain) {
    $s = [string]$m
    if ($s.Contains('/')) { $prefixed += $s }
    else { $prefixed += "$([string]$binding.provider)/$s" }
  }
  $chain = @($prefixed | Select-Object -Unique)
  try { $health = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$port/healthz" -TimeoutSec 3 }
  catch { throw "ERR_ISOLATED_OPENCODEX_NOT_HEALTHY" }
  if ($health.StatusCode -ne 200) { throw "ERR_ISOLATED_OPENCODEX_NOT_HEALTHY" }

  $logRoot = Join-Path (Split-Path -Parent $codexHome) "logs"
  New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
  $attempts = @()
  $usedModel = ""
  $chainExhausted = $true
  for ($i = 0; $i -lt $chain.Count; $i++) {
    $m = [string]$chain[$i]
    $attempt = [ordered]@{ index = $i; model = $m }
    # TestInject429: short-circuit the FIRST attempt as an injected failure to force
    # the chain forward WITHOUT spending real quota on the primary model.
    if ($TestInject429 -and $i -eq 0) {
      $attempt.exit = "ERR_429_INJECTED"
      $attempt.injected = $true
      $attempts += $attempt
      continue
    }
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssfffZ")
    $wLog = Join-Path $logRoot "codex-write-$stamp-m$i.log"
    $wErr = Join-Path $logRoot "codex-write-$stamp-m$i.stderr.log"
    $codexArgs = @(
      "--model", $m,
      "--sandbox", "danger-full-access",
      "-c", "approval_policy=never",
      "--cd", $root,
      "exec", "--skip-git-repo-check", "--ephemeral", "--json", $Prompt
    )
    $savedEAP = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { & $codexExe @codexArgs *> $wLog; $exit = $LASTEXITCODE } finally { $ErrorActionPreference = $savedEAP }
    $attempt.exit = $exit
    $attempt.log = $wLog
    $attempt.stderr_log = $wErr
    $attempts += $attempt
    if ($exit -eq 0) { $usedModel = $m; $chainExhausted = $false; break }
    # 429/quota exhaustion on deepseek -> try next model. Non-zero (but non-quota)
    # also advances so a stuck model does not dead-end the chain.
    Start-Sleep -Milliseconds 1500
  }
  $receipt.write_action = "Write"
  $receipt.write_prompt = if ($Prompt.Length -gt 80) { $Prompt.Substring(0,80) + "..." } else { $Prompt }
  $receipt.write_chain = $chain
  $receipt.write_attempts = $attempts
  $receipt.write_model_used = $usedModel
  $receipt.write_chain_exhausted = $chainExhausted
  if ($chainExhausted) { $receipt | ConvertTo-Json -Depth 8; throw "ERR_CODEX_WRITE_CHAIN_EXHAUSTED" }
  if ($TestInject429) { $receipt.test_inject_429 = $true }
  $receipt | ConvertTo-Json -Depth 8
  exit 0
}

$logRoot = Join-Path (Split-Path -Parent $codexHome) "logs"
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssfffZ")
$stdoutLog = Join-Path $logRoot "opencodex-probe-$stamp.stdout.log"
$stderrLog = Join-Path $logRoot "opencodex-probe-$stamp.stderr.log"
$syncLog = Join-Path $logRoot "opencodex-sync-$stamp.log"
$codexLog = Join-Path $logRoot "codex-probe-$stamp.log"
$codexErrorLog = Join-Path $logRoot "codex-probe-$stamp.stderr.log"
$proxy = $null
Push-Location $openCodexRoot
try {
  $proxy = Start-Process -FilePath $bunExe -ArgumentList @("run", $openCodexEntry, "start", "--port", "$port") -PassThru -WindowStyle Hidden -RedirectStandardOutput $stdoutLog -RedirectStandardError $stderrLog
  $healthy = $false
  for ($i = 0; $i -lt 30; $i++) {
    try {
      $health = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:$port/healthz" -TimeoutSec 2
      if ($health.StatusCode -eq 200) { $healthy = $true; break }
    } catch {}
    Start-Sleep -Milliseconds 500
  }
  if (-not $healthy) { throw "ERR_ISOLATED_OPENCODEX_START_FAILED" }
  $savedErrorAction = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  $syncOutput = & $bunExe run $openCodexEntry sync 2>&1
  $syncExit = $LASTEXITCODE
  $ErrorActionPreference = $savedErrorAction
  $syncOutput | Set-Content -LiteralPath $syncLog -Encoding UTF8
  if ($syncExit -ne 0) { throw "ERR_OPENCODEX_SYNC_EXIT_$syncExit" }
  $catalogPath = Join-Path $codexHome "opencodex-catalog.json"
  if (-not (Test-Path -LiteralPath $catalogPath -PathType Leaf)) { throw "ERR_ISOLATED_CATALOG_MISSING" }
  $codexArgs = @(
    "--model", ([string]$binding.model),
    "--sandbox", "read-only",
    "--ask-for-approval", "never",
    "--cd", $root,
    "exec", "--skip-git-repo-check", "--ephemeral", "--json",
    "ReplyExactly:$Nonce"
  )
  $codexProcess = Start-Process -FilePath $codexExe -ArgumentList $codexArgs -PassThru -WindowStyle Hidden -RedirectStandardOutput $codexLog -RedirectStandardError $codexErrorLog
  if (-not $codexProcess.WaitForExit($ProbeTimeoutSeconds * 1000)) {
    Stop-Process -Id $codexProcess.Id -Force -ErrorAction SilentlyContinue
    throw "ERR_CODEX_ROUTE_TIMEOUT"
  }
  $codexProcess.Refresh()
  $codexExit = $codexProcess.ExitCode
  $codexOutput = @()
  if (Test-Path -LiteralPath $codexLog -PathType Leaf) { $codexOutput += Get-Content -LiteralPath $codexLog -Encoding UTF8 }
  if (Test-Path -LiteralPath $codexErrorLog -PathType Leaf) { $codexOutput += Get-Content -LiteralPath $codexErrorLog -Encoding UTF8 }
  if ($codexExit -ne 0) { throw "ERR_CODEX_ROUTE_EXIT_$codexExit" }
  if (($codexOutput -join "`n") -notmatch [regex]::Escape($Nonce)) { throw "ERR_CODEX_ROUTE_NONCE_MISSING" }
  $usagePath = Join-Path $openCodexHome "usage.jsonl"
  if (-not (Test-Path -LiteralPath $usagePath -PathType Leaf)) { throw "ERR_OPENCODEX_USAGE_RECEIPT_MISSING" }
  $usageReceipt = (Get-Content -LiteralPath $usagePath -Encoding UTF8 | Select-Object -Last 1) | ConvertFrom-Json
  if ([string]$usageReceipt.provider -ne [string]$binding.provider -or
      [string]$usageReceipt.model -ne [string]$binding.model -or
      [int]$usageReceipt.status -ne 200) {
    throw "ERR_OPENCODEX_PROVIDER_RECEIPT_MISMATCH"
  }
  $receipt.route_nonce = $Nonce
  $receipt.route_exit_code = $codexExit
  $receipt.provider_route_confirmed = $true
  $receipt.provider_request_id = [string]$usageReceipt.requestId
  $receipt.provider_status = [int]$usageReceipt.status
  $receipt.usage_receipt_sha256 = (Get-FileHash -LiteralPath $usagePath -Algorithm SHA256).Hash
  $receipt.proxy_stdout = $stdoutLog
  $receipt.proxy_stderr = $stderrLog
  $receipt.sync_log = $syncLog
  $receipt.codex_log = $codexLog
  $receipt.codex_stderr_log = $codexErrorLog
  $receipt | ConvertTo-Json -Depth 6
} finally {
  Pop-Location
  if ($proxy -and -not $proxy.HasExited) { Stop-Process -Id $proxy.Id -Force -ErrorAction SilentlyContinue }
}
