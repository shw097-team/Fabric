# Sealed Codex lane invocation + PowerShell capture pitfalls

Verified 2026-08-12 on the HGK stack. The Codex CLI is NOT on PATH; it lives at the
pinned lane path. Drive it through the same pattern the HGK launcher
(`scripts/start-hgk-hermes.ps1`) uses, but with a real bounded diagnostic prompt.

> **Related (2026-08-15, WO-HGK-GPTWORK-CODEX-RESTORE-001):** the HUMAN Codex home
> (`C:\Users\user\.codex` — backs the OpenAI ChatGPT desktop app's Work/Codex modes) is a
> SEPARATE lane from this sealed lane and can be hijacked by `opencodex (ocx)`. Restore
> recipe, HGK-lane zero-touch rule, CRLF `\r\r\n` trap, and daemon on-demand governance:
> `references/gptwork-codex-desktop-restore.md`. **Also:** `start-hgk-hermes.ps1 -Action
> Probe` throwing `ERR_CODEX_ROUTE_EXIT_` is the Start-Process ExitCode-null trap (pitfall 1
> below), NOT a route failure — verify via codex-probe-*.log nonce + usage.jsonl receipt
> before declaring failure; re-run the canary with the `& $codexExe @args` splatting form.

## Lane identity (from config/hermes-codex-lane.json)

```text
codex_exe        %LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe
codex_version    codex-cli 0.147.0-alpha.6.5
codex_home       %LOCALAPPDATA%\HG-KSEOS\codex-hermes        (isolated CODEX_HOME)
opencodex_home   %LOCALAPPDATA%\HG-KSEOS\opencodex-hermes    (isolated OPENCODEX_HOME)
opencodex_root   %LOCALAPPDATA%\HG-KSEOS\runtime\opencodex-2.11.0
opencodex_port   10101
provider         opencode-go / model deepseek-v4-flash / openai_fallback false
credential_env   OPENCODE_GO_API_KEY  (source: %LOCALAPPDATA%\hermes\.env)
```

OpenCodex proxy entry: `node_modules\bun\bin\bun.exe run src\cli\index.ts start --port 10101`
(then `sync` once; health = GET http://127.0.0.1:10101/healthz → 200).

## PowerShell 5.1 capture pitfalls (all hit live; each cost a failed run)

1. **`Start-Process -PassThru -RedirectStandardOutput/-RedirectStandardError` loses
   `.ExitCode`** (returns null even after `WaitForExit()` + `Refresh()`). Do NOT read the
   exit code from that object. Fix: invoke synchronously —
   `& $codexExe @codexArgs *> $logFile; $exitCode = $LASTEXITCODE` (array splatting quotes
   each arg correctly, including the multi-word prompt).
2. **PowerShell 5.1 `*>` redirect writes UTF-16LE** — reading it back with
   `Get-Content -Encoding UTF8` yields interleaved NULs (`\u0000` between every char) and
   JSON parsing fails. Read with `[System.IO.File]::ReadAllText($path, [System.Text.Encoding]::Unicode)`.
3. **`$ErrorActionPreference="Stop"` + native command stderr = terminating
   `NativeCommandError`**. Codex prints "Reading additional input from stdin..." to stderr,
   which kills the script mid-run. Wrap the invocation: save EAP, set `"Continue"`, run,
   restore.
4. **`Start-Process -ArgumentList` splits a multi-word prompt into separate args**
   (`error: unexpected argument 'are' found`). If you must use Start-Process, pre-quote:
   `('"{0}"' -f $prompt.Replace('"', '\"'))` — but the `&` splatting form (pitfall 1)
   avoids this entirely.

## Canonical invocation (works)

```powershell
$env:CODEX_HOME = $codexHome; $env:OPENCODEX_HOME = $openCodexHome   # process-scoped
$codexArgs = @(
  "--model", $model, "--sandbox", "read-only", "--ask-for-approval", "never",
  "--cd", $root, "exec", "--skip-git-repo-check", "--ephemeral", "--json", $prompt
)
Push-Location $root
try {
  $eap = $ErrorActionPreference; $ErrorActionPreference = "Continue"
  try { & $codexExe @codexArgs *> $codexOut; $exitCode = $LASTEXITCODE }
  finally { $ErrorActionPreference = $eap }
} finally { Pop-Location }
$codexJson = [System.IO.File]::ReadAllText($codexOut, [System.Text.Encoding]::Unicode)
```

Credential: read ONLY the exact named line `OPENCODE_GO_API_KEY=` from
`%LOCALAPPDATA%\hermes\.env` and set it in the process env; never print or persist it.

## Parsing the NDJSON output

`codex exec --json` emits an NDJSON **event stream** (`item.started`, `item.completed`,
`turn.completed`). The answer is the `text` of the LAST `item.completed` event whose
`item.type == "agent_message"` — it contains the model's JSON (sometimes fenced in
```json ... ```). Parse per line:

```powershell
foreach ($line in ($codexJson -split "`r?`n")) {
  $evt = $line | ConvertFrom-Json
  if ($evt.type -eq "item.completed" -and $evt.item.type -eq "agent_message") {
    $lastAgentText = [string]$evt.item.text
  }
}
# strip ```json fences, then ConvertFrom-Json
```

## Inspection target: REAL repo, not a detached worktree

A `git worktree add --detach <dir> HEAD` only contains TRACKED content at HEAD —
untracked files (`config/hermes-codex-lane.json`) are missing and modified files show
stale committed content (e.g. the old retired-runtime binding). The sealed lane Probe uses
`--cd $root` on the real repo with `--sandbox read-only`; do the same. Prove no tracked
mutation: `git status --porcelain` count + `git rev-parse HEAD` before and after must be
identical.

## Evidence of the route

- Codex process actually spawned: capture PID + exit code (0).
- Provider receipt: tail of `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` →
  `provider=opencode-go`, `model=deepseek-v4-flash`, `status=200`; record `requestId` and
  the usage.jsonl SHA-256.
- `fallback_used = false`; `HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0`.
- WorkOrder id + Kanban task id bound to the canary run.
