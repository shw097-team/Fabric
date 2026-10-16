# Verify lane must be a pinned one-shot, not a delegate child

## Why (observed root cause, 2026-10)
`delegate_task` children all use the **delegation** model/provider (config `delegation.provider/model`);
they do NOT read Kanban card pins and cannot carry a per-lane model. So a "VERIFY" card pinned to a
checker model does nothing for a delegate child — it silently runs the delegation model instead, and
model-SoD is violated while looking like it was respected.

Second trap: on this stack nothing *forces* an EXECUTE->VERIFY handoff.
- sealed `start-hgk-hermes.ps1 -Action Write` prints a receipt then `exit 0`; it never spawns an AO.
- `lifecycle.py` FORWARD allows `EXECUTING -> (VERIFYING, EVOLUTION_REVIEW)`; VERIFYING is skippable.
- `kanban_db.complete_task` only recomputes readiness of **already-existing** children; it never
  spawns a missing VERIFY card.
- the "every round closes with independent acceptance" rule lives in the skill, i.e. depends on the
  orchestrator actually issuing the dispatch.

Guard facts (do not overclaim "no enforcement"): `spine.record_workorder_result` refuses
`writer == checker`; `ReleaseReducer` raises `INDEPENDENT_ACCEPTANCE_MISSING`; `scripts/hgk-lane-guard.py`
is a runnable pre-dispatch guard (REFUSE, rc=2). They exist but are **result gates at call time**, not a
scheduler that starts VERIFY.

## Rule
Route the independent VERIFY/AO through a **explicitly pinned one-shot**, never a delegate child:

```bash
cd <hermes-agent>
venv/Scripts/python.exe -B hermes_cli/main.py \
  -z '<VERIFY contract: read subject, verify against cited locators, write ONLY the verdict file>' \
  -m glm-5.3-flash --provider opencode-go --reasoning medium > <verify.log> 2>&1
```

`-z/--oneshot`, `-m/--model`, `--provider`, `--reasoning` are per-invocation overrides (no config change).
Checker model must be the pinned one, and the verdict must record `officer_identity.observed`.

## Pitfalls
- The `-z` one-shot **buffers stdout**; the log stays 0 B until it exits. A 0-B log is NOT a stall —
  check CPU + TCP connections + spawned `execute_code` kernel child instead of the log.
- Hermes logs the delegate lanes but a one-shot's turn may not appear in `logs/agent.log`; do not
  conclude "no session" from a missing log line.
- Freeze subject sha256 **before** verifying and bind the digests into the verdict; any later byte
  change SUPERSEDES the verdict. Officer nits get recorded in the verdict, NOT patched into the frozen
  subject (editing it would invalidate the verdict).
- Fail closed: absence of evidence is never PASS; require `exists(completed_VERIFY_after_candidate_freeze)`
  BEFORE any `all(...)` over the maker set, else an empty set passes vacuously.
- Keep PLAN/RESEARCH on the delegation model (gpt-6.1-sol via openai-codex) and EXECUTE on the sealed
  Codex lane (`deepseek-v4.1-flash`). Verify the lane's real model via its `codex.exe --model` argv or
  the `state_*.sqlite` `threads` row, not from a label.
