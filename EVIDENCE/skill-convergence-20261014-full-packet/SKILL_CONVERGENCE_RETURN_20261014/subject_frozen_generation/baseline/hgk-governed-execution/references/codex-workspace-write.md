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
