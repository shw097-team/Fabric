# Tasks

## 1. PLAN & Orchestrator lane (priority 1 — owner ordered this session)
- [x] Re-measure the governed PLAN plane end-to-end: reply probe, **tool-executing** probe, effective-HERMES-HOME
      resolution probe, and the profile's OWN `state.db::sessions` serving rows.
- [x] Record the measured rows (`model=gpt-6.1-sol`, `billing_provider=openai-codex`,
      `billing_base_url=https://chatgpt.com/backend-api/codex`, `billing_mode=subscription_included`).
- [x] Record the declaration-surface divergence (`model-lane-assignment.json` revision 19 vs the round mandate,
      the pool rank 1 and the governed profile) and its measured counter-evidence.
- [ ] ChangeSet A: additive PLAN-plane declaration + stale `usable_now` correction + registry drift fix (WorkOrder-gated).

## 2. M03 effort axis (product code)
- [ ] RED: `tests/test_lane_effort_enforcement.py` fails against the current assert script.
- [ ] Implement the effort comparison + `--served-effort` in `scripts/runtime_role_binding_assert.py`.
- [ ] GREEN + the round's named acceptance command.

## 3. `CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED` (product code)
- [ ] RED: three new cases in `tests/test_governed_runtime_controller.py` (blank, null, free-text class).
- [ ] Answer the blank-session case instead of exiting 3; POSITIVE CONTROL on the same fixture stays denying.
- [ ] GREEN + the round's named acceptance command.

## 4. Independent verification, self-check, publication
- [ ] EXECUTE lane receipt: `required_arm == served_arm`, `usage_receipt_ok`.
- [ ] Orchestrator re-derives the writer's named acceptance command (the receipt is a claim).
- [ ] VERIFY/SECURITY lane (CODEX CLI, `openai-codex/gpt-6.1-sol`, `--guard-subject` = frozen candidate).
- [ ] Self-check harness with armed must-refuse probes and a machine-gate verdict (never PASS for acceptance).
- [ ] Canonical apply of the verified candidate + the full suite AT the canonical root.
- [ ] Publish implementation + evidence to `shw097-team/Fabric` for the external acceptance officer.

## 5. Orchestration surfaces (enabled, and positioned honestly)
- [x] KANBAN board `lane-reliability-closure-20261016` created; SWARM DAG root `t_d73fd9d5`, workers
      `t_c81ed79f` / `t_86dd7812` / `t_a64fc611`, verifier `t_92f55a9e`, synthesizer `t_dbdc8541`; ids written to
      `var/LANE-RELIABILITY-CLOSURE-20261016/KANBAN_SWARM_GRAPH.json`.
- [x] GSTACK named-method / role-map readback written to `GSTACK_READBACK.json` (7 ACTIVE_SELECTED methods,
      every activation invariant zero, `SELECTED_NOT_IN_MAP` reported as the explicit empty set).
- [ ] Drive the board cards to a real outcome (a card id is not a run).

## 6. Residual (unchanged by this change)
- [ ] E11: five AO-guard cases (host 136/136 vs checker sandbox 131 passed / 4 failed / 1 error on relay-metadata access).
- [ ] Matrix rows still NOT_RUN after this round's slice (each listed in the round's re-derived matrix readback).
