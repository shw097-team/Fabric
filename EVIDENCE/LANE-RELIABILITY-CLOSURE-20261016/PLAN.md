# PLAN — round `LANE-RELIABILITY-CLOSURE-20261016`

Owner order (this session): under the current Fabric governance contract, HG-KSEOS is the sole
control plane, canonical Hermes is its governed Runtime / Orchestration plane, and the THREE lanes
must be **usable and reliable** with the owner-named model per lane:

| role | lane token | model | provider | auth | surface |
|---|---|---|---|---|---|
| PLAN & Orchestrator | `PLAN` | `gpt-6.1-sol` (medium) | `openai-codex` | OpenAI OAuth | in-Hermes (governed profile) |
| Codex bounded writer | `EXECUTE` | `deepseek-v4.1-flash` | `opencode-go` | env key | CODEX CLI sealed lane |
| Independent Acceptance Officer | `VERIFY_SECURITY` | `gpt-6.1-sol` (medium) | `openai-codex` | OpenAI OAuth | CODEX CLI sealed lane |

Successor round to `LANE-ENFORCEMENT-APPLY-20261015` (handover:
`_handover/CHECKPOINT_HGK-LANE-ENFORCEMENT-APPLY-20261015.md`). This round EXISTS to close the four
items that round named and deliberately did not finish.

## 0. CORE BIG GOAL (核心大目標)

Make the three lanes' **model selection** demonstrably usable and reliable — i.e. for each lane:
(a) the serving surface is MEASURED live (not read from a config file), (b) the declared model/effort
is ENFORCED (a drift is refused by a typed gate, not by nothing), (c) the control cannot fail closed
into an outage, and (d) the evidence is frozen and published for an external acceptance officer.

Priority 1 — explicitly ordered by the owner this session — is the **PLAN & Orchestrator lane**
(`gpt-6.1-sol` medium, OpenAI OAuth, inside Hermes): its availability must be re-measured end-to-end
and its declaration surfaces must stop contradicting each other.

## 1. WHAT THE PREVIOUS ROUND ALREADY BUILT (reuse, do not rebuild)

Read first, from the working session itself, not from memory:

1. `<HERMES_HOME>/profiles/hgk-governed/config.yaml` — the governed PLAN plane binding:
   `model.default: gpt-6.1-sol`, `model.provider: openai-codex`, `reasoning_effort: medium`, plus the
   `governed_runtime` guard binding (protected roots HG-KSEOS + Fabric, controller command, timeout 10).
2. `config/hermes.json::governed_hermes_home` — ADDITIVE key (R3 activation) pointing at that profile;
   `canonical_hermes_home` deliberately UNCHANGED so un-governed consumers keep their binding.
3. `scripts/hermes-core.ps1` lines 11-14 + 21 — the 4-line override that prefers
   `governed_hermes_home` when declared. Absent key => byte-identical previous behaviour.
4. `scripts/hgk-governed-runtime-controller.py` (the guard's controller) and
   `<HERMES_HOME>/hermes-agent/agent/mandatory_tool_guard.py` (the pre-tool guard).
5. `var/LANE-ENFORCEMENT-APPLY-20261015/` — `APPLY_P6/APPLY_RECEIPT.json`, `R3_ACTIVATION/
   R3_ACTIVATION_RECEIPT.json`, `FAR-GAP-RULING-20261015/FAR_PLAN_ORCHESTRATOR_MODEL_RULING.md`,
   `FAR_R3_AND_REMAINING_OPTIONS_RULING.md`, `role_mandate.json`, `ACCEPTANCE_MATRIX.json`.
6. Skill `hgk-kanban-and-lane-routing` references: `lane-chain-rebind.md`,
   `gstack-named-method-readback.md`, `codex-lane-transport-and-identity.md`.

Plane separation the whole round rests on (`effective_wiring.main_agent`):
PLAN & Orchestrator = `config.yaml model.default` + `model.provider` of the profile the process runs
under; the interactive session model is a DIFFERENT surface (`state.db::sessions.model`); EXECUTE is
the CODEX CLI sealed lane. KANBAN / SWARM / GSTACK / OPENSPEC are **orchestration surfaces, not model
routers** — enabling them routes nothing, and GSTACK has no separate implementation in this repo.

## 2. TASK EXECUTION SPEC

Authority chain: owner order -> this PLAN -> HGK typed admission (Requirement FROZEN / TaskSpec
ADMITTED / WorkOrder CREATED) -> bounded writer -> independent checker -> orchestrator re-derivation.

Invariants in force:
- Candidate-only. No agent self-acceptance and no self-promotion; the checker's verdict is ADVISORY.
- Every canonical mutation is WorkOrder-gated, backed up as `.bak-<change>-<UTC>`, with before/after
  sha256 recorded, and disclosed as a side effect of the round.
- No agent may resolve acceptance. `hgk_canonical_acceptance: NOT_PERFORMED`.
- Claim ceilings are printed on every artifact, and unverifiable items stay explicitly unverifiable.
- SoD residual must be stated, never smoothed: PLAN and VERIFY/SECURITY are the SAME model
  (`openai-codex/gpt-6.1-sol`), so plan-vs-checker MODEL independence is ABSENT; only process / lane /
  evidence-path independence remains. Maker (`deepseek-v4.1-flash`) != checker still HOLDS.

The exact candidate change sets this round authorises (nothing else):

**ChangeSet A — PLAN-lane declaration coherence (config; authored by the orchestrator under a
WorkOrder, since config data is not product code and must not be smuggled through a maker round)**
- A1 `config/model-lane-assignment.json`: additive, explicit declaration of the in-Hermes
  PLAN & Orchestrator PLANE binding (its serving surface, the R3 activation key, the MEASURED
  availability with date + raw evidence ref, the claim ceiling, and the explicit statement that the
  `PLAN` lane_group row is the LANE-DISPATCH declaration which the in-Hermes PLAN plane does not
  consume). Bump `revision` 19 -> 20 and `registry_epoch` 19 -> 20 with a dated reason.
- A2 `config/lane-routing-registry.yaml`: publication counter `epoch` 19 -> 20; the two bindings that
  pin `/revision` and `/registry_epoch` follow; and the pre-existing `DRIFT_VALUE` on
  `/codex_sha256` (registry expected the PRE-repair, wrong digest `D13914CE...DAEC` while the live
  config carries the measured-true `e98c516f...b99e`) is corrected to the MEASURED live sha256.
- A3 acceptance: `lane_policy.check_drift(registry=reg)` returns ZERO findings (today: 1 fatal
  DRIFT_VALUE), and `check_sod(PLAN, VERIFY_SECURITY)` outcome is recorded verbatim (it stays
  `SOD_OK` because the lane-dispatch PLAN route remains unchanged; the PLANE collision is declared,
  not hidden).

**ChangeSet B — M03 effort-axis enforcement (product code; to the EXECUTE lane)**
- B1 `scripts/runtime_role_binding_assert.py` gains the effort axis: mandate `reasoning_effort` is
  compared against the declared arm's pool entry, plus an optional `--served-effort`.
  Typed refusals: `ERR_MANDATE_EFFORT_MISMATCH`, `ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL`,
  `ERR_SERVED_EFFORT_MISMATCH`, `ERR_SERVED_EFFORT_UNVERIFIABLE`. Exit code 7.
- B2 NEW `tests/test_lane_effort_enforcement.py`: 6 subprocess cases (1 POSITIVE control on the same
  fixture + 4 typed negatives + 1 pass-through positive). RED first, on the real behaviour.
- Basis: measured — `grep -c effort scripts/runtime_role_binding_assert.py` == 0, i.e. the mandate's
  `gpt-6.1-sol` **MEDIUM** is enforced by nothing.

**ChangeSet C — controller absent-session-id outage (product code; to the EXECUTE lane)**
- C1 `scripts/hgk-governed-runtime-controller.py`: a blank/absent `session_id` is ANSWERED
  (`{"action":"allow","reason":"no-session-id-unattributable"}`, exit 0) instead of being mapped to
  exit 3. Rationale recorded in-code: a governed binding REQUIRES a non-empty session, so a blank id
  cannot be a governed round; exit 3 makes the guard refuse EVERY mutating call for any agent without
  a session id — an outage, and an inconsistency with the already-allowed unknown-id case.
- C2 `tests/test_governed_runtime_controller.py`: 3 new subprocess cases (blank, null, and the
  free-text class), each asserting its OWN reason string. POSITIVE CONTROL on the same fixture:
  `test_neg_maker_write_inside_protected_denied` must still deny when the session id IS present.
- Residual disclosed: a governed agent whose session id is missing would be treated as un-governed;
  the lane-level frozen-subject digest guard still catches a write into the audited subject.

**Not authorised this round** (named so nobody drifts into them): no registry `routes[]` re-route, no
relay/transport change, no new control plane, no secrets, no service restart, no `RP002 Stage3`,
no acceptance resolution, no E11 sandbox redesign.

## 3. TASK EXECUTION LIST (ordered, with the surface that executes each)

| # | task | executing surface |
|---|---|---|
| T1 | Re-measure the PLAN plane live: reply probe + tool-executing probe + effective-HERMES-HOME resolution + profile serving rows | Hermes one-shot under the governed profile |
| T2 | HGJK typed admission: Requirement FROZEN / TaskSpec ADMITTED / WorkOrder CREATED for EXECUTE and VERIFY | `hg_kseos.spine` typed API |
| T3 | Freeze the candidate + subject digests | orchestrator |
| T4 | KANBAN board + real SWARM DAG (root/worker/verifier/synthesizer), ids written to disk | `hermes kanban` |
| T5 | OPENSPEC change record for this round | repo `openspec` CLI + OPENSPEC/changes |
| T6 | GSTACK named-method / lane-routing readback | `hg_kseos.named_methods` + `lane_policy` |
| T7 | EXECUTE lane: apply ChangeSet B+C as exact hunks, RED -> GREEN, emit receipt before long runs | CODEX CLI `opencode-go/deepseek-v4.1-flash` |
| T8 | Orchestrator re-derives the lane's named acceptance command (207 expected) — the lane's receipt is a claim | orchestrator |
| T9 | VERIFY/SECURITY lane: independent re-derivation over the FROZEN candidate, `--guard-subject` | CODEX CLI `openai-codex/gpt-6.1-sol` medium |
| T10 | ChangeSet A under WorkOrder: backups + before/after sha256 + drift sweep to zero | orchestrator (disclosed authoring surface) |
| T11 | Self-check harness: armed must-refuse probes, re-derived invariants, printed claim ceiling | orchestrator |
| T12 | Canonical apply of the verified candidate + full suite at the canonical root | orchestrator, WorkOrder-gated |
| T13 | Publish implementation + evidence to `shw097-team/Fabric` for the external acceptance officer | git write to the remote, owner-supplied credential |
| T14 | Self-research / self-learn / self-iterate: skill + memory updates, FAR-style learnings note | orchestrator |

## 4. DETECTION LIST (檢測清單) — each item is re-derived from live evidence, never from the round's own summary

| id | check | expected | how it is re-derived |
|---|---|---|---|
| D01 | PLAN plane serves gpt-6.1-sol at medium through the profile binding | PASS | profile `state.db::sessions` row `model`/`billing_provider` + probe stdout, both quoted |
| D02 | PLAN plane can ACT, not only reply | PASS | tool-executing probe must print the command's exact stdout |
| D03 | formal adapter resolves HERMES_HOME to the governed profile | PASS | `r3_resolution_probe.ps1` output |
| D04 | `grep -c effort scripts/runtime_role_binding_assert.py` after B | > 0 | direct grep |
| D05 | M03 negatives refuse with their OWN typed code | PASS | the 4 throwaway-fixture runs, exit 7, code quoted |
| D06 | M03 positive control on the same fixture | PASS | exit 0 + `effort_verified: true` |
| D07 | controller answers a blank session id | PASS | exit 0 + `reason=no-session-id-unattributable` |
| D08 | controller still denies a real governed maker write | PASS | `test_neg_maker_write_inside_protected_denied` green |
| D09 | suite at the candidate root | `207 tests OK` | the named command re-run by the orchestrator |
| D10 | suite at the CANONICAL root after apply | `207 OK` | same command, canonical cwd |
| D11 | `check_drift(registry=reg)` | `[]` | live run, before and after ChangeSet A |
| D12 | `check_sod(PLAN, VERIFY_SECURITY)` outcome recorded verbatim | recorded | live run |
| D13 | lane receipts: `required_arm == served_arm`, `usage_receipt_ok` | PASS | `dispatch_receipt*.json`, never the verdict's own model line |
| D14 | checker's window over the frozen subject | CLEAN, `accepted:false` advisory | `subject_mutation` verdict |
| D15 | KANBAN/SWARM ids exist on disk AND in the board DB | PASS | board DB readback + artifact |
| D16 | OPENSPEC change validates with the project's own CLI | PASS / recorded | `npx openspec validate --strict` |
| D17 | Fabric remote carries the implementation + evidence | PASS | remote readback of the pushed blobs, not the local commit |
| D18 | every artifact prints a claim ceiling and no artifact says PASS for acceptance | PASS | grep the round's artifacts |
| D19 | no lane/agent resolved acceptance | NOT_PERFORMED | grep for acceptance-resolution calls |
| D20 | rollback path for every canonical mutation | present | backup files + sha256 before/after |

## 5. CLAIM CEILINGS THAT BIND THIS ROUND

- PLAN == VERIFY == `gpt-6.1-sol`: plan-vs-checker model independence is ABSENT (owner-accepted).
- This session's interactive turn is served by a different model than the PLAN plane; the PLAN-plane
  claim is made on the profile's own measured rows, and the two are reported separately.
- The checker's verdict is advisory. It is not an OracleReceipt and not a canonical acceptance.
- `hgk_canonical_acceptance: NOT_PERFORMED`.
- E11 (five AO-guard cases) stays a NAMED OPEN RESIDUAL: host 136/136 vs checker sandbox
  131 passed / 4 failed / 1 error on relay-metadata access. Unchanged by this round.
