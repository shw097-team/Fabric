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


