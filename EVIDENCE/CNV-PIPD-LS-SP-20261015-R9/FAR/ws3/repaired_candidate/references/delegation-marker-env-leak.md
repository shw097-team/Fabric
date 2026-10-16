# HERMES_DELEGATED_CHILD_CONTEXT env leak — root-cause (verified 2026-08-20, primary source)

When the Hermes orchestrator's terminal/kanban surface dies with "delegate_task child contexts
cannot mutate Kanban tasks or boards" (or "...via the CLI") right after a `delegate_task` batch,
the cause is a **session-snapshot env leak**, not broken delegation or a bad Kanban DB.

## Root cause in one paragraph
Hermes terminals are "spawn-per-call + persistent session snapshot". To carry a delegated
child's lineage across a process fork, `scrub_kanban_env()` stamps
`HERMES_DELEGATED_CHILD_CONTEXT=1` into the **child's** subprocess env. But the top-level agent and
every delegate_task child share ONE cached environment (`_active_environments["default"]`), and
each command's wrapper re-dumps the whole shell env back into the shared snapshot file — including
that marker. The next orchestrator command `source`s the snapshot, so the marker leaks into the
MAIN session env; spawns that run `hermes kanban ...` inherit it and misread the main session as a
delegated child, so the kanban mutation guards fire.

## Verified source map (C:\Users\user\AppData\Local\hermes\hermes-agent\)
- **Write (the ONLY truthy write in the codebase):** `agent/delegation_context.py:138`
  `scrub_kanban_env()` → `cleaned[DELEGATED_CHILD_ENV_MARKER] = "1"` — writes into a NEW dict,
  NOT `os.environ`. Reached only when `is_delegated_child_process_context()` is True, via:
  - `tools/environments/local.py:516/524` `_scrub_delegated_child_kanban_env` (called at `:511`,
    `:654`, `:1326` inside `_make_run_env`)
  - `tools/code_execution_tool.py:296-297`
  - `agent/delegation_context.py:154` `delegated_child_subprocess_env`
- **Read/decision:** `is_delegated_child_process_context()` (`delegation_context.py:124-130`) reads
  `os.environ.get(marker)`; the ContextVar path is authoritative only in-process. Consumers:
  - `hermes_cli/kanban.py:1215-1220` `_is_delegated_child_cli_mutation`
  - `hermes_cli/kanban_db.py:176-185` `_assert_not_delegated_child_mutation` (fired inside
    `write_txn` at `:2823`, and board metadata mutators at `:518/:530/:743/:863`)
- **Leak channel:** `tools/terminal_tool.py:1089` `_active_environments` keyed by `effective_task_id`;
  `:2583-2587` all subagent task_ids collapse to "default" → main + children share ONE env;
  `:2678-2691` reuse across calls. `tools/environments/base.py:934-940` re-dumps shell env to the
  snapshot after EVERY command; `:884-887` re-sources it before every command. Exclusion regex
  `base.py:524-526` does NOT exclude `HERMES_DELEGATED_CHILD_CONTEXT`.

## Two message variants (same root cause — do not treat as different bugs)
- "…cannot mutate Kanban tasks **via the CLI**" → `kanban.py:1026-1031` CLI fast-fail (denied
  mutation actions: create/complete/claim/assign/…).
- "**could not initialize database**: …cannot mutate Kanban tasks or boards" →
  `kanban.py:1083-1086` wraps a `PermissionError` from `kanban_db.py:184` raised during
  `init_db`→connect→migration `write_txn`. Most visible on a fresh/uninitialized board or `init`.

## Recovery
`unset HERMES_DELEGATED_CHILD_CONTEXT` in the orchestrator terminal after a delegate_task batch
(also clears it from the snapshot on the next command re-dump).

## Root fix — APPLIED 2026-08-21 (user-approved NARROW_REPAIR, WO-HGK-ROOTCAUSE-IMPL-001)
> This supersedes the previously-recorded "Root fix direction (not yet in source)" line.

Root cause patch landed in `tools/environments/base.py` (the shared snapshot's single dump helper
`_export_dump_excluding_session_vars`, called by both bootstrap `:745` and per-command `:937`, across
all backends). Two additive changes:
- **Regex contract** `_SNAPSHOT_EXCLUDED_ENV_REGEX` (`:524-526`) — added `HERMES_DELEGATED_CHILD_CONTEXT`
  and `HERMES_KANBAN_`.
- **unset block** (`:569-570`) — added `"${!HERMES_KANBAN_*} HERMES_DELEGATED_CHILD_CONTEXT "` while
  PRESERVING the original `"unset ${!HERMES_SESSION_*} ${!HERMES_CRON_AUTO_DELIVER_*} "` line verbatim
  (the `*` on `HERMES_CRON_AUTO_DELIVER_*` must never be dropped — that would re-allow CRON auto-deliver env
  leak and break `test_snapshot_session_id_leak.py:51`).

Child isolation is intentionally preserved: the marker is still re-injected per-process by
`_make_run_env`/`_sanitize_subprocess_env` (`local.py:511,1326`) and `code_execution_tool.py` when
`is_delegated_child_process_context()` is True — the fix only prevents it from PERSISTING into the shared
snapshot, so the main orchestrator is no longer misread as a child.
- Regression: `test_snapshot_session_id_leak.py + test_snapshot_multiline_session_env_injection.py +
  test_delegate_kanban_isolation.py` → **8 passed, 3 skipped** (Codex static `PATCH_CORRECT` 5/5 + AO
  `ACCEPTANCE_OFFICER_VERDICT=PASS`). Full `tests/tools` suite: 5813 passed / 316 failed (all pre-existing
  environmental failures: WinError-2 bash path, absent Docker/vision/voice infra in a dev tree) — none touch
  the changed code.
- **Effect after restart**: the patch edits the canonical Hermes install (`C:\Users\user\AppData\Local\hermes\
  hermes-agent`); the running process already imported the module so takes effect on NEXT Hermes restart.
  Until then the `unset` recovery above still applies. Backup: `var/a2/base.py.backup-e867010e`.
- Evidence: `HGK/evidence/review/ROOTCAUSE_IMPL_EVIDENCE_20260821.md` (3 mirror roots byte-identical,
  spine `EV-ROOTCAUSE-IMPL-20260821` hash == on-disk).
