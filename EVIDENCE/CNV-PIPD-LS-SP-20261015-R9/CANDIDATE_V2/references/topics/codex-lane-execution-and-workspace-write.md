<!-- SKCV-TOPIC-ENTRY path=skill/references/codex-canary-powershell.md offset=170 length=5511 sha256=4be423b5e1137632a54c92f4be82ab6a32419bcf07cafcdab4ce5ce02c84b774 -->
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
<!-- SKCV-TOPIC-ENTRY path=skill/references/codex-lane-log-liveness-markers.md offset=5860 length=2029 sha256=9a2a56a7f19e6db8fb048a84d37fb91c0378632716778fa468f474a131f1e850 -->
# Judging a CODEX CLI lane's liveness from its log

## Why
A sealed CODEX lane writes to a plain redirect file that grows continuously, so unlike a Hermes
one-shot it is *not* empty while running. That invites a different wrong heuristic: gating on the
launcher's terminal marker.

A lane log DOES contain `^EXIT=` lines that are **not** the terminal marker: the launcher appends
`EXIT=$RC` as the last line at exit, but the lane's own body also prints `EXIT=...` while discussing
or running things. Measured: the marker appeared at line 1216 of 1936 and at line 6146 of a longer
log, in both cases mid-run with the lane still working.

## Rules

1. **`grep -c '^EXIT='` on a lane log is unreliable in BOTH directions.** Non-zero does not mean the
   lane closed; a single marker does not mean only one exit happened.
2. **Liveness needs at least two of these, all positive:**
   - the marker is the **last non-empty line** (not merely present), AND
   - the log **size/mtime still advances** across two samples >=15 s apart, AND
   - the lane's declared **target files are still not written/unchanged** (a lane writes bodies before
     it edits its main target), AND
   - the child process is still present.
3. **Never conclude "no artifacts" from a listing whose stderr was swallowed.** `ls ... 2>/dev/null`
   prints the same empty-looking result for "the lane has not written it yet" and "the path is wrong".
   Probe each path explicitly (`stat`) and report ABSENT separately from unchanged.
4. **Check the target file, not the log, for progress on the real deliverable.** A lane can be deep in
   context for a long time before it touches `its main target`; the log growing proves work, not closure.
5. **Repair-dispatch discipline:** never dispatch a repair/retry lane until rule 2 is satisfied. The
   cost of waiting is minutes; the cost of a premature repair dispatch is a duplicated side effect that
   can exceed a one-use authorization (recorded defect, round HGK-GCM-APPLY-20261013).
<!-- SKCV-TOPIC-ENTRY path=skill/references/codex-sealed-lane-windows.md offset=8063 length=11271 sha256=3d1d8a2ca61c0c0fdf5bbfc875a9459d3863f17a7a537cee3420be8ad94aa0ab -->
# Sealed Codex EXECUTE lane on Windows — operating rules

Purpose: make EXECUTE-lane volume work genuinely run through the Codex CLI (not the
main loop), and prove it did. Every rule below was learned by measurement on this
Windows host; each states the failure it prevents.

## 1. Starting the lane (relay)
- Start: `pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/start-hgk-hermes.ps1 -Action StartOpenCodex`
  (run from the HG-KSEOS repo root, as a background process).
- `pwsh` is already on PATH; do NOT forge the path via `ls .../pwsh | head -1` — a glob
  artifact there yields `/.../pwsh*` and the launcher never starts.
- Readiness (never assume): `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:10101/healthz`
  → 200, and `/v1/models` → 200. Before start, both return `000` (relay down).
- The relay serves a fixed slug list; confirm the model you intend is in `/v1/models`.

## 2. Lane config (CODEX_HOME)
- Lane home: `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` (`config.toml`, `opencodex-catalog.json`).
  Isolate with `export CODEX_HOME=...`; never touch `%USERPROFILE%\.codex` (first-party lane).
- `config.toml` `model` MUST equal a catalog `slug` exactly
  (e.g. `opencode-go/deepseek-v4.1-flash`). A bare name (`deepseek-v4.1-flash`) is accepted
  by the relay but logs `Model metadata ... not found. Defaulting to fallback metadata`.
- `openai_base_url` must point at the relay (`http://127.0.0.1:10101/v1`).

## 3. Sandbox: `workspace-write` is a trap on this host
- With `-s workspace-write` + `approval=never`, EVERY model shell command comes back
  `rejected: blocked by policy` (read-only behaviour). The process still exits 0 and writes
  a confident "I attempted every write/execute path… all were rejected… this is BLOCKED" message.
  Same for `-s read-only` — and the real variable is the lane home's Windows sandbox PROVISIONING,
  not the flag or the endpoint: see `references/codex-workspace-write.md` §CORRECTION (measured
  2026-10-14: same binary/model/flags on the human home runs tools, on an unprovisioned lane home
  every command is denied).
- **A lane run that exits 0 is not a lane run that did work.** Always count
  `"type":"command_execution"` in `codex_events.jsonl` and `grep -c "blocked by policy" <stderr>`.
  Healthy = hundreds of command_execution, 0 blocked, plus `file_change` events.
- To let the lane actually execute use `-s danger-full-access`. Trade-off: the lane then has
  full filesystem access and is NOT covered by Hermes's FDA pre-call gate (separate process),
  so the boundary must be enforced by construction (staging clone + env pin) and verified
  after the fact — see §6.
- Spawn form (prompt on stdin, JSONL events, final message to a file):
  `cat CODEX_TASK.md | "$CODEX" exec --cd <staging-root> --skip-git-repo-check -s danger-full-access --json -o codex_last_message.txt - > codex_events.jsonl 2> codex_stderr.txt`
  where `CODEX=<%LOCALAPPDATA%>\HG-KSEOS\runtime\codex-<ver>\codex.exe`. Run it as a
  background process with notify on exit.

## 4. Proving which model ran
- `state_5.sqlite` (in the lane home) `threads` table: newest row's `model` is the model the
  thread actually used (`opencode-go/deepseek-v4.1-flash`). Cross-check `model/`opencode-go`
  hits in `codex_events.jsonl`. Config alone is not evidence.

## 5. MSYS path pitfalls (this shell is git-bash; path translation is DISABLED)
- Pass `C:/...` native paths to native programs (git, python, codex). An MSYS `/c/...`
  argument is taken literally: `git clone <src> /c/projects/x` silently creates `C:\c\projects\x`,
  and `PYTHONPATH=/c/...` makes native python import from `C:\c\...`. The clone then looks
  non-existent (".git not found") while the import check still prints a plausible path.
- Bash builtins (`cd`, `cp`, redirects) handle `/c/...` fine — only native-tool argv is at risk.
- `git -C <dir>` needs a native path; `rm -rf` of a staging clone may report
  `Device or resource busy` if the session cwd is inside it (`cd` out first).

## 6. Boundary verification for a lane run (do all four)
1. `git -C <canonical> status --porcelain | md5sum` before/after — must be identical.
2. `select count(*) from canonical_events` on the canonical spine before/after — must be equal.
3. `git -C <canonical> rev-parse HEAD` unchanged.
4. Staging clone only: confirm no `var/shared-spine/` materialises in the clone.
Git-tree equality alone is insufficient: tests can append to the canonical spine DB without
changing the worktree, so check the DB count too.

## 7. Hermeticity leak pattern (why suite runs mutated a canonical spine)
- Symptom: `canonical_events` grows ~1 per full-suite run (e.g. `HGK-PRJ-CLI2 → PROJECT_CREATED`).
- Cause: a test spawned the CLI with `env = dict(PYTHONPATH=...)`, which REPLACES the child
  environment and drops the spine override, so the child resolved the canonical root's DB.
- Fix shape: one resolver (`spine_database(root)`) that all entry points (`cli`, `bootstrap`,
  `doctor`, `providers`) route through; `HGK_SPINE_DB` env override installed per run by the
  test package; child processes must **inherit** `os.environ` (then set PYTHONPATH); the guard
  refuses a canonical override outright. Verify by running the suite twice and showing the
  canonical count unchanged.
- Production default must stay untouched: with `HGK_SPINE_DB` unset the resolver returns
  `<root>/config[canonical_database]` exactly as before — never silently redirect production.

## 8. Fixing red suite items honestly
- A red item is either an artifact defect or a STALE TEST EXPECTATION. Never delete, skip,
  `xfail`, or loosen an assertion to reach green; no swallowing `try/except`.
- Rebinding is legitimate when it is subject-correct and equal-or-stronger, with the
  authoritative source cited (path + section/sha). Examples that passed review:
  whole-worktree `git status` → the ChangeSet's admitted target set + its materialization
  commit; `recorded_head == rev-parse HEAD` → `recorded_head == acceptance-candidate head`
  plus `--is-ancestor` against live HEAD; guide "current claim = Task-015" → bind the
  acceptance receipt that actually establishes the current claim, and assert the stale claim
  is absent.
- Require the executor to hand back a `no_weakening` section quoting every changed assertion
  before/after, then re-run the suite yourself and re-check the boundary (§6).

## 9. Keep orchestration admission separate from arm qualification
- Pass a real, current lane-shaped arm probe receipt to `hgk-lane-guard.py`; a typed Shared Spine Requirement/TaskSpec/WorkOrder readback is a different schema and cannot prove the arm completed model/tool round-trips. Attribute a wrong-receipt refusal to the caller, not provider availability. Never replace it with a fabricated `ADMITTED` string.
- Read the installed probe's live implementation before treating a binding as sufficient. A live branch explicitly marked unimplemented cannot mint genuine arm admission; keep UNPROVEN and require a separately governed qualification implementation.
- Reconcile counter semantics before any freshness repair: registry publication/route-shape epoch and source policy revision may be independently defined counters. Matching source revision and SHA256 does not make a guard's cross-counter equality valid. Preserve the refusal, request a bounded independently checked comparator repair, and never force a matching epoch, substitute a local registry, restore foreign SSOT pins, or modify routing outside scope.
- Check whether the correct anchor already exists before proposing a schema or config change. On this stack the admission receipt already carries `policy_epoch` (set to the registry epoch by the probe) while the guard reads a *different* document's `revision` and never reads the receipt field at all — so the repair is 'read the anchor you were already given', not 'add a field'. Prefer the option that stays inside the frozen-file prohibition (guard-script-only) and note that a receipt-anchored freshness check is not an integrity anchor.
- Treat clarification-form authorization as unrecognized when the guard still refuses the exact call. Pause without rewriting the payload; request a formal user chat authorization for the same limited scope, then test the unchanged call once. A successful read proves only that call was admitted, not credential access, reseal, global routing changes, or future/child authorization.

## 10. Respect child command-policy refusals even without an OS sandbox
- Treat `danger-full-access` as absence of an OS sandbox, not absence of Codex command-policy restrictions. An in-scope destructive operation can still return command `exit_code=-1` with an explicit policy rejection. Stop the owned invocation and request a human decision; do not retry quoting variants, replace deletion with another utility, relax policy, or treat typed path admission as overriding that refusal.
- Attribute watcher termination precisely: preserve the exact refused event IDs, operation class, class-specific count, owned PIDs stopped, exit code, incomplete candidate manifest and missing maker receipt. Distinguish immediate security-refusal intervention from the ten-minute/repeated-over-four rule. Never describe a killed invocation as a provider failure or successful maker result.
- Confirm a rejection from structured event status/exit code and explicit result content, not a phrase appearing in successfully read source, tests or documentation. Preserve the original automated intervention receipt and append a causal audit; do not rewrite history if the classifier was wrong.

## 11. Destructive verbs are Forbidden under approval_policy=never (measured)
- A lane run with `-s danger-full-access -c approval_policy=never` still cannot delete: `Remove-Item` (and other "dangerous PowerShell words") returns command `exit_code = -1`, output `` `...` rejected: blocked by policy ``, wall time 0.0s — refused before process creation. Root cause is Codex's own `core/src/exec_policy.rs`: dangerous-command detection maps `AskForApproval::Never` to `Decision::Forbidden` unless the sandbox is explicitly disabled as a permission profile (`danger-full-access` alone does not qualify). Upstream reports the same class (openai/codex issues #34331, #49248).
- Therefore write candidate task prompts so cleanup never needs a destructive verb: create a fresh directory/file instead of deleting, or ask the operator to delete out-of-band. Never retry with alternate deletion utilities, quoting variants, or a relaxed approval policy — that is bypassing a real safety boundary, and the refusal carries no rule ID to appeal.
- Verify attribution before blaming the relay: the string is absent from the opencodex bundle and present in `codex.exe` (`codex-0.147.0-alpha.6.5`); scanning the ~293 MB binary for `blocked by policy` / `exec_policy.rs` is the cheap confirmation.

- Keep an unfinished VERIFY card waiting on its maker dependency. A Kanban block command can return failure while still appending a comment; read back exact status, comments and parent edges before asserting a transition succeeded.


<!-- SKCV-TOPIC-ENTRY path=skill/references/codex-workspace-write.md offset=19505 length=17006 sha256=fd9dfe87142d314acc880960cec0b68544c4a025496bbf82d1c7c55d7092eab5 -->
# Codex sealed-lane writes: `workspace-write` is forced read-only; the working pattern is `danger-full-access` + process-boundary safety

Verified 2026-08-12 on the HGK stack (A-3 implementation runs). The sealed lane
(`%LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe` → opencodex 2.11.0
proxy at 127.0.0.1:10101, isolated CODEX_HOME/OPENCODEX_HOME, credential
`OPENCODE_GO_API_KEY` from `%LOCALAPPDATA%\hermes\.env`) CANNOT write files with any
`workspace-write`-flavored invocation.

## Symptom

Model reports "the sandbox is read-only (permission profile grants read access only)",
shell writes (`Set-Content`, `New-Item`, `cmd /c echo >`) are rejected with
`codex_core::tools::router: ... rejected: blocked by policy`, and the tool catalog has
NO `apply_patch` (only shell_command, update_plan, request_user_input, view_image,
multi-agent tools).

## What was tried and failed (10+ probes in a throwaway dir)

| attempt | result |
|---|---|
| `--sandbox workspace-write --ask-for-approval never` | all writes blocked by policy |
| `--approve-for-me` (implies workspace-write; mutually exclusive with `--sandbox`) | write escalation rejected via "provider/infrastructure error" |
| `-c sandbox_permissions=["disk-full-read-access","disk-write-access",...]` | ignored |
| `--ask-for-approval untrusted` | ignored (still reports approval policy `never`) |
| `--model opencode-go/deepseek-v4-flash` (full catalog slug) | fixes the "Model metadata not found → fallback metadata" warning but does NOT unlock writes; apply_patch still absent |
| `config.toml` `sandbox_mode = "workspace-write"` + `approval_policy = "untrusted"` | ignored |
| `config.toml` `model = "opencode-go/deepseek-v4-flash"` | same as the flag; no writes |

Root cause: codex CLI 0.147.0-alpha.6.5 client-forces a read-only sandbox profile when
talking to the custom (non-OpenAI) opencodex endpoint; the proxy's tool catalog does not
advertise `apply_patch`. Do not burn time re-probing this — the flags are structurally
ignored for this endpoint.

## CORRECTION — measured 2026-10-14: the discriminating variable is the CODEX_HOME, not the endpoint

The endpoint reading above is REFUTED by a same-machine A/B (same binary, same model, same
`--sandbox read-only`, same relay):

| CODEX_HOME | `--sandbox` | served via | command_execution items | `blocked by policy` | real output |
|---|---|---|---|---|---|
| lane home `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` | read-only | relay 10101 | 0 | yes | none |
| lane home | workspace-write | relay 10101 | 0 | yes | none |
| lane home | danger-full-access | relay 10101 | 2 | no | real |
| lane home | read-only | relay 10101 (OAuth arm `gpt-6.1-sol`) | 0 | yes | none |
| **human home `%USERPROFILE%\.codex`** | read-only | relay 10101 | 2 | no | real |
| **human home** | read-only | native OpenAI | 2 | no | real |

Same refusal on codex builds 0.162.0-alpha.17.2 / 0.154.0-alpha.6.2 / 0.147.0-alpha.6.5 (the build
only changes the refusal's SHAPE: 0.147 emits one `command_execution` item carrying the refusal text
with `exit_code:-1`; 0.162/0.154 emit none). The serving model/arm and the endpoint are NOT the
variable; the CODEX_HOME is.

Mechanism: the Windows sandbox is provisioned PER HOME by `codex-windows-sandbox-setup.exe` —
`\.sandbox\setup_marker.json`, `\.sandbox-secrets\sandbox_users.json`, `\.sandbox-bin\codex-command-runner-<ver>.exe`.
The human home has all three (and its `\.sandbox\sandbox.<date>.log` shows the setup binary spawning and
applying read ACLs before each command); the lane home has none (its `.sandbox` log stops at helper
START lines), so under read-only/workspace-write the sandbox cannot be established and every command is
denied; only `danger-full-access` (no sandbox needed) executes.

## ROOT CAUSE (measured 2026-10-14, second pass): a missing `[windows] sandbox` key, not an unprovisioned home

The switch is one config key in the lane's OWN home:

| home | `[windows] sandbox` | read-only command execution |
|---|---|---|
| human `%USERPROFILE%\.codex` | `"elevated"` (present in every backup back to 2026-08-12) | runs, `exit_code 0` |
| lane `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` | **absent** in all three of its historical versions (current, 2026-10-10 bak, 2026-10-02 bak) | `blocked by policy`, 0 command_execution |

With the key present codex provisions that home ON DEMAND (`\.sandbox\setup_marker.json`,
`\.sandbox-secrets\sandbox_users.json`, `\.sandbox-bin\codex-command-runner-<ver>.exe`, read ACLs) and
sandboxed commands execute; with it absent it never sets the home up and denies. **The key must be present
on every run** — after a home HAS been provisioned, a run without the key still refuses (measured). Both
`"elevated"` and `"unelevated"` were observed to work; the machine-wide sandbox accounts
(`CodexSandboxOffline` / `CodexSandboxOnline`, see `net user`) and `codex-windows-sandbox-service.exe`
already exist, so no one-time elevation step is needed.

Read-only semantics survive the fix: with the key + `--sandbox read-only`, a write attempt is still denied
(the lane's patch tool reports `writing is blocked by read-only sandbox`; on the human home `Set-Content`
returns `Access to the path … is denied`) and no file lands. So a read-only CHECKER lane can regain tool use
without gaining write capability.

Repair (owner-authorised, either form):
- no config mutation (matches the dispatcher's design): add `-c windows.sandbox="elevated"` to the lane argv;
- durable: append `[windows]` + `sandbox = "elevated"` to the lane home's `config.toml` (back it up first).
Acceptance triple, all measured: positive = key + read-only + read command runs and returns real output;
negative = no key + read-only + same prompt refuses; boundary = key + read-only + write attempt is denied.

Rules this earns:
- Before blaming the relay, the provider, the arm or the build for `blocked by policy`, compare the two homes'
  `config.toml` for `[windows] sandbox` and list the home's sandbox artifacts. A lane run that exits 0 with a
  nonce and a usage receipt is NOT a lane run that executed anything — count `"type":"command_execution"` first.
- Do NOT diagnose "nothing was changed" from the flag defaults alone: the same dispatcher table and the same
  binary were in place for weeks; the load-bearing difference was a key the lane home never carried.
- NEVER transplant `setup_marker.json`, `.sandbox-secrets/` or `cap_sid` between homes: two such attempts hung
  with no artifact and needed `taskkill /F /T` (the sandbox helper inherits the stdout pipe). Let codex
  provision the home itself after the key is present.
- A `read-only` lane in an unprovisioned home can audit a bundle it was handed and can never re-derive
  the tree. Do not put `git`/`python`/file reads in such a prompt; escalate the sandbox for that round
  instead (`--sandbox danger-full-access --allow-sandbox-escalation` + the dispatcher's `--guard-subject`
  non-mutation guard), which is the only measured path that runs tools.
- NEVER transplant `setup_marker.json`, `.sandbox-secrets/` or `cap_sid` from one home into another: two
  such attempts produced no artifact and no `.sandbox` log, hung past the caller bound, and needed
  `taskkill /F /T` (the sandbox helper inherits the stdout pipe, so a naive timeout does not return).
  Provision the home with the CLI's own setup inside an operator window if that is what is wanted.

## The WORKING write pattern (validated: 2 implementation runs, exit 0)

```powershell
$codexArgs = @(
  "--model", "deepseek-v4-flash",
  "--sandbox", "danger-full-access",      # Hermes codex skill: gateway-context fallback
  "--ask-for-approval", "never",
  "--cd", $Root,
  "exec", "--skip-git-repo-check", "--ephemeral", "--json", $prompt
)
& $codexExe @codexArgs *> $OutLog   # then read UTF-16, parse NDJSON, extract final agent_message
```

Compensating controls that make this governance-acceptable (all applied on A-3):
- WorkOrder-scoped NARROW prompt enumerating the exact files to create/modify and
  forbidding everything else (no `git commit`, no network, no files outside the list).
- Explicit writable roots = the admitted repos only; pre/post `git status --porcelain`
  + full `git diff` review after.
- Targeted tests rerun independently after the run (compiler 22/22, suites).
- Independent checker (checker ≠ maker) re-reads every fact fresh.
- Evidence of the sandbox decision goes into the evidence payload §D ("fallback state").

`--dangerously-bypass-approvals-and-sandbox` was NOT used (no sandbox AND no approvals =
unsafe; `danger-full-access` keeps the approval system and is the documented Hermes
pattern for service contexts).

## PowerShell 5.1 prompt-quoting trap (cost one failed run)

`& $codexExe @codexArgs` with a prompt string containing embedded `"` (e.g. quoted
Windows paths) splits the prompt into multiple CLI arguments:
`error: unexpected argument '31c.' found`. Fix: sanitize the prompt FILE before passing
(`prompt.replace('"', "'")`) — the A-3 prompts were rewritten quote-free. This is
distinct from the documented `Start-Process -ArgumentList` splitting bug.

## CODEX_HOME env trap: defaulting to the human `~/.codex` (spurious ChatGPT-auth error)

Verified 2026-08-20 (方案 D method-finalization round). Calling `codex.exe` directly
from a shell (git-bash or PowerShell) **without exporting the lane env has a silent
footgun**: codex resolves its home to the HUMAN `~/.codex` (whose `auth.json` is a
native ChatGPT login), so even when the HGK opencodex daemon (127.0.0.1:10101) is
healthy you get:

```
The 'deepseek-v4-flash' model is not supported when using Codex with a ChatGPT account.
  (status 400, turn.failed)
```

Healthz 200 + `usage.jsonl` showing `provider=opencode-go/status 200` does NOT protect
you — those are daemon-side; the CLI-side home resolution is what bites. **Fix: export
the lane env in the SAME invocation** (bash env doesn't persist across tool calls):

```bash
export CODEX_HOME="$LOCALAPPDATA/HG-KSEOS/codex-hermes"
export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"
"$LOCALAPPDATA/HG-KSEOS/runtime/codex-0.147.0-alpha.6.5/codex.exe" \
  --model deepseek-v4.1-flash --sandbox read-only -c approval_policy=never \
  --cd <Root> exec --skip-git-repo-check --ephemeral --json "<prompt>"
```

Verify with `CODEX_HOME` grep: the lane `config.toml` must show
`openai_base_url = http://127.0.0.1:10101/v1` + `model = "deepseek-v4.1-flash"`.

## session-header-and-relay: `400 MissingSessionID` is a protocol defect, not a model defect

Verified 2026-10 (SWOF evidence-repair round). **opencode-go requires an
`x-opencode-session` header on EVERY request.** Without it the provider boundary returns
`HTTP 400 MissingSessionID`. The trap: the error surfaces at the model layer, so it reads
as "that model slug does not exist / is not supported" and you burn runs swapping models
(`deepseek-v4-flash` → `deepseek-v4.1-flash` → fallbacks) with zero change.

**Diagnose before switching anything.** Two one-line probes settle it:

```bash
# no session header  -> expect HTTP 400 MissingSessionID
# with x-opencode-session -> expect HTTP 200 + a real completion
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:10101/v1/chat/completions \
  -H 'content-type: application/json' -H "x-opencode-session: $SID" \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"ping"}]}'
```

**Fix — inject the header at the relay's provider definition, once:**
`ocx provider edit opencode-go --headers` with a stable session id (+ user-agent). The
relay (opencodex, adapter `openai-chat`) forwards provider headers but does not originate
this one itself.

**Relay must be up or the lane fail-closes.** If `127.0.0.1:10101` is not listening the
symptom is `CODEX_LANE_BLOCKED_PROVIDER_ROUTE`. Start it in the ISOLATED home — never let
it touch the human `~/.codex`:

```bash
export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"
node bin/ocx.mjs start --port 10101
```

**A route change must land on ALL THREE surfaces, or you get a partial, self-contradicting
lane** (back each up first — `config.toml.bak-<tag>` / equivalent):

| surface | role | field |
|---|---|---|
| `HG-KSEOS/config/hermes-codex-lane.json` | HGK lane authority | lane model + a permanent `model_routing_change` record |
| `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\config.json` | relay config | `defaultModel` / `selectedModels` / `models` / `subagentModels` |
| `%LOCALAPPDATA%\HG-KSEOS\codex-hermes\config.toml` | Codex client | `model = "..."` |

**`ocx provider selected --set <id>` silently drops the new id from the static
`models`/`subagentModels` arrays** even when it sets `defaultModel` — the model then does
not appear selectable. Stop the relay, hand-patch those JSON arrays, restart, re-verify all
three surfaces.

## A Codex refusal to verdict without file access is CORRECT — grant the narrow read

When Codex is asked to verify artifacts and cannot read them, it may return an explicit
refusal rather than invent a verdict. **That is the fail-closed behavior you want; it is
not a lane defect and not something to press past.** Give it the narrowest read-only
permission that lets it inspect the subject (bounded, no-shell prompt), then take its
grounded verdict. Also record the Codex SUCCESS attempt row in the lane outcome artifact —
a failure-only `attempts[]` next to a resolution note reads as "never worked" and an
independent lane WILL flag it.

## Static-review compensates for the read-only sandbox (triple-verification pattern)

With `--sandbox read-only` (or danger-full-access on the custom endpoint), codex cannot
execute `python -m unittest` — every interpreter invocation is "blocked by policy". This
is expected, NOT a failure. The proven pattern for product-code verification without a
write-capable test run:
- Codex performs a **static read-only review** of every invariant (state enums, gate
  lists, cost-model constants, schema `required`/`additionalProperties`) and returns a
  JSON verdict `{"writer":"codex","verdict":...}` — still a real provider-receipt-backed
  engagement.
- The test suite is run separately by Hermes/Swarm (`PYTHONPATH=src python -m unittest`)
  and cross-checked against the receipt's engine_identity / result hash.
- Record Codex verdict + provider receipt (usage.jsonl status 200) as co-evidence so the
  round still proves a genuine Codex tracked-writer participation even when sandbox
  blocks execution.

## Lane config hygiene

Never leave the codex-hermes `config.toml` modified after experiments: back it up first
(`cp config.toml config.toml.bak-<tag>`), restore afterwards, verify byte-identical,
then remove the backup. The sealed lane is `ACTIVE_FAIL_CLOSED`; a drifted config is an
integrity violation even if CLI flags masked it.

## Maker-run hygiene in a git worktree (post-run, before you freeze anything)

The maker runs in an isolated `git worktree`; do NOT trust its self-report. Two traps bit
this lane:

1. **Re-verify the commit actually exists on the branch.** After the maker reports
   "3 files changed, worktree dirty, no commit", commit them yourself, then IMMEDIATELY
   `git rev-parse HEAD` and `git rev-parse <branch>` to confirm the branch tip holds the new
   SHA. A worktree branch can silently sit at the baseline (detached / re-pointed), so the
   commit becomes a dangling object while `git status` still shows your edits as uncommitted —
   every later raw log would then name the wrong `git HEAD`.
2. **Sweep the maker's untracked scratch before committing.** The run leaves `dbg.py`,
   `rights1.txt`, `*_SPEC.md`, and ad-hoc `acceptance/` dirs. `git status --porcelain | grep '^??'`,
   delete the scratch, and `git add` ONLY the intended source files — never `git add -A` on a
   shared worktree.

Also: a `--sandbox workspace-write` maker run fails at *exploration* (it cannot even read the
spec — `CreateProcess ... blocked by policy`, no `Read`/`apply_patch` in the catalog), so it
returns a blocker and writes zero files rather than doing partial work. Go straight to
`--sandbox danger-full-access` for the maker lane; a workspace-write attempt is a wasted round.
Verify lane liveness first (`curl -s 127.0.0.1:10101/healthz`) — a dead relay yields the same
"cannot work" symptom for a different reason.

## Evidence of the route

- codex process actually spawned: capture PID/exit (0) + started/finished UTC from the
  wrapper report.
- Provider receipt: tail of `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` →
  `provider=opencode-go`, `model=deepseek-v4-flash`, `status=200`.
- `CODEX_FALLBACK_USED = NO`, `HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0`.
