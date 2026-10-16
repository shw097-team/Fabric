# Change: hgk-lane-reliability-closure-20261016

## Why
The owner order for session `20261016_104922_d455e7` requires the three HG-KSEOS lanes to be **usable and
reliable** with the named model per lane, with the **PLAN & Orchestrator lane inside Hermes bound to
GPT 6.1 SOL-MEDIUM (OpenAI OAuth)** and its model selection demonstrably usable. The predecessor round
`LANE-ENFORCEMENT-APPLY-20261015` applied the control to canonical and left four named items open
(its own checkpoint, §4): the M03 effort axis, `CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED`, the matrix
slice, and an independent check of the applied state.

This change records the closure round for those items and the reliability findings measured while
re-measuring the PLAN lane.

## What changes
- **ChangeSet A (config, orchestrator-authored under the round's WorkOrder)** — `config/model-lane-assignment.json`
  gains an ADDITIVE, explicit `in_hermes_plan_orchestrator_plane` declaration (binding surface, R3
  activation key, MEASURED availability with its raw evidence reference, claim ceiling, and the statement
  that the `PLAN` lane_group row is the LANE-DISPATCH declaration which the in-Hermes PLAN plane does not
  consume). `revision` 19 -> 20 and `registry_epoch` 19 -> 20 with a dated reason. `config/lane-routing-registry.yaml`
  follows: `epoch` 19 -> 20, the two bindings pinning `/revision` and `/registry_epoch` move with it, and the
  pre-existing fatal `DRIFT_VALUE` on `/codex_sha256` (the registry still expected the PRE-repair, wrong
  digest while the live config carries the measured-true one) is corrected to the MEASURED live sha256.
- **ChangeSet B (product code, bounded writer via the CODEX CLI EXECUTE lane)** — `scripts/runtime_role_binding_assert.py`
  enforces the **effort axis**: the mandate's `reasoning_effort` is compared against the declared arm's pool
  entry, plus an optional `--served-effort`. Typed refusals `ERR_MANDATE_EFFORT_MISMATCH`,
  `ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL`, `ERR_SERVED_EFFORT_MISMATCH`, `ERR_SERVED_EFFORT_UNVERIFIABLE`;
  exit code 7. New `tests/test_lane_effort_enforcement.py`.
- **ChangeSet C (product code, same writer turn)** — `scripts/hgk-governed-runtime-controller.py` answers a
  blank/absent `session_id` with `{"action":"allow","reason":"no-session-id-unattributable"}` (exit 0) instead
  of mapping the typed `ERR_ROLE_BINDING_SESSION_REQUIRED` refusal to exit 3, which made the guard refuse EVERY
  mutating call of any agent without a session id. Three new cases in `tests/test_governed_runtime_controller.py`.
- **No route, registry-route, relay or transport re-route.** PLAN is not dispatched through
  `scripts/hgk-lane-dispatch.py`, so its registry route is not the serving surface of the in-Hermes plane;
  re-pointing it would also collapse the `PLAN != VERIFY_SECURITY` SoD pair the conformance suite asserts.

## Not claimed
- PLAN == VERIFY == `openai-codex/gpt-6.1-sol`, so **plan-vs-checker MODEL independence is ABSENT**; only
  process / lane / evidence-path independence remains (owner-authorised deviation).
- The writer's green run and the checker's verdict are both CLAIMS. Neither is verification and neither is
  acceptance. `hgk_canonical_acceptance: NOT_PERFORMED`.
- KANBAN / SWARM / GSTACK / OPENSPEC are orchestration surfaces, NOT model routers. GSTACK has no separate
  implementation in this repository and is reported as a named-method / role-map readback.
- E11 (five AO-guard cases) remains a named open residual, unchanged by this round.
