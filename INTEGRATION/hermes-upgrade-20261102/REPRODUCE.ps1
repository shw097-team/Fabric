param([Parameter(Mandatory=$true)][string]$IsolatedRoot)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath($IsolatedRoot)
if($root.Length -gt 64){throw 'Choose a shorter new root: PM generation paths plus SDK module names can exceed Windows path limits.'}
if(Test-Path -LiteralPath $root){throw 'Use a NEW directory; never reuse a live Hermes home.'}
New-Item -ItemType Directory -Path $root | Out-Null
$code=Join-Path $root 'hermes-agent'
git clone --depth 1 --single-branch --branch v0.22.5 https://github.com/NousResearch/hermes-agent.git $code
if($LASTEXITCODE -ne 0){throw 'Official clone failed'}
$expected='bf0203a794a07aac3ff764972ab9087baa4e4f4e'
if((git -C $code rev-parse HEAD) -ne $expected){throw 'Stable source identity mismatch'}
$env:HERMES_HOME=Join-Path $root 'state'
$env:HERMES_RUNTIME_DIR=Join-Path $root 'tools'
$env:UV_CACHE_DIR=Join-Path $root 'uv-cache'
$env:UV_PYTHON_INSTALL_DIR=Join-Path $root 'uv-python'
Remove-Item Env:HERMES_PROFILE -ErrorAction SilentlyContinue
Remove-Item Env:HERMES_INSTALL_ROOT -ErrorAction SilentlyContinue
Set-Location -LiteralPath $code
. .\activate.ps1
hermes --version
hermes profile create fhs --no-alias --no-skills --description 'Isolated FHS read/draft verification'
if($LASTEXITCODE -ne 0){throw 'Native profile creation failed'}
hermes profile list
Write-Output 'Source/Profile prepared; provider, Desktop, Native E2E and cutover are NOT verified.'
Write-Output 'For headless verification, use this isolated shell: hermes -p fhs serve --isolated --port 0 --host 127.0.0.1'
Write-Output 'Use the official authenticated JSON-RPC client for session.create; retry the same idempotency_key and compare session_id.'
Write-Output 'After stopping only the process you started, resume with stored_session_id, not the transient session_id.'
Write-Output 'Negative: a missing stored Session must be refused; an openai-codex provider paired with opencode-go/deepseek-v4.1-flash must be refused.'
Write-Output 'Do not provision live OAuth refresh tokens or messaging channels in this scratch home.'
