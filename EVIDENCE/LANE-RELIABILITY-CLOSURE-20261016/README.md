# LANE-RELIABILITY-CLOSURE-20261016 — HG-KSEOS three-lane usability and reliability

Round of **2026-10-16**, session `20261016_104922_d455e7`. Owner order: under the current Fabric
governance contract, HG-KSEOS is the sole control plane, canonical Hermes is its governed
Runtime / Orchestration plane, and the three lanes must be **usable and reliable** with the
owner-named model per lane. This packet is the implementation and the evidence, published for an
external acceptance officer.

**Claim ceiling: CANDIDATE_ONLY.** Nothing here is accepted, promoted or merged.
`hgk_canonical_acceptance: NOT_PERFORMED`. The checker verdict below is advisory.

## The lanes and how each model selection was PROVEN

| lane | model | provider | surface | how it was proven (not read from config) |
|---|---|---|---|---|
| PLAN & Orchestrator | `gpt-6.1-sol` medium | `openai-codex` (OAuth) | inside Hermes, governed profile | reply probe (`PLAN_LANE_PROBE_OK`) **and** a tool-executing probe (`PLAN_TOOL_PROBE_OK`), plus the profile's own `state.db::sessions` rows: `model=gpt-6.1-sol, billing_provider=openai-codex, billing_base_url=https://chatgpt.com/backend-api/codex` |
| Codex bounded writer / EXECUTE | `deepseek-v4.1-flash` | `opencode-go` | CODEX CLI sealed lane | `dispatch.json`: `required_arm == served_arm == opencode-go/deepseek-v4.1-flash`, `usage_receipt_ok: true`, `used_rank: 1`, `nonce_present: true` |
| Independent Acceptance Officer / VERIFY / SECURITY | `gpt-6.1-sol` medium | `openai-codex` (OAuth) | CODEX CLI sealed lane | receipt + its own re-derivation (see `lanes/VERIFY_SECURITY/`) |

## What was changed

**ChangeSet B — the M03 effort axis** (`scripts/runtime_role_binding_assert.py`). Measured basis:
`grep -c effort` was **0**, so a lane served at a different reasoning effort than the mandate
declares was refused by NOTHING. The gate now compares the mandate effort against the declared
arm's pool entry and accepts an explicit `--served-effort`, refusing with this axis's own exit
code 7 and four typed codes.

**ChangeSet C — the absent-session-id outage** (`scripts/hgk-governed-runtime-controller.py`).
The guard allows only on exit 0 and sends `session_id = getattr(agent,"session_id","") or ""`; the
controller mapped a blank id to exit 3, so any agent without a session id had EVERY mutating call
refused. It now answers `{"action":"allow","reason":"no-session-id-unattributable"}`.

**ChangeSet A — PLAN declaration coherence + drift repair** (`config/…`, the only canonical
mutation; WorkOrder `WO-LANE-RELIABILITY-20261016-CHANGESET-A`). Additive PLAN-plane declaration with
this round's measured availability; registry `epoch` 19 -> 20; the stale `/codex_sha256` projection expectation corrected from the PRE-repair digest to the
measured live value; `source_of_routes` re-pinned. Backups and before/after sha256 are in
`CHANGESET_A_APPLY_RECEIPT.json`; canonical drift is now **[]**.

## Lane receipts (verbatim, from each `dispatch.json`)

| attempt | lane verdict (agg) | required arm (agg) | served arm (agg) | usage receipt (agg) | rank (agg) | attempt exit | attempt usage attribution | attempt usage receipt |
|---|---|---|---|---|---|---|---|---|
| EXECUTE/BC1 | FAIL ERR_LANE_ALL_ROUTES_EXHAUSTED | — | **null** | False | None | TIMEOUT | opencode-go/deepseek-v4.1-flash | True |
| EXECUTE/BC2 | TERMINATED | — | **null** | None | None | TERMINATED_BY_ORCHESTRATOR_AFTER_MEASURED_WEDGE | — | None |
| EXECUTE/BC3 | ok | opencode-go/deepseek-v4.1-flash | opencode-go/deepseek-v4.1-flash | True | 1 | None | opencode-go/deepseek-v4.1-flash | True |
| VERIFY_SECURITY/V1 | ok | openai-codex/gpt-6.1-sol | openai-codex/gpt-6.1-sol | True | 1 | None | openai-p6a1fe3/gpt-6.1-sol | True |
| VERIFY_SECURITY/V2 | ok | openai-codex/gpt-6.1-sol | openai-codex/gpt-6.1-sol | True | 1 | None | openai-p6a1fe3/gpt-6.1-sol | True |

Two notes so the table above is not misread:

1. **`served arm (agg)` is the identity gate; `attempt usage attribution` is not.** They can disagree, and on
   BC1 they do: the attempt names the mandated arm while the aggregate verdict is a failure with
   `served_arm` `null`. Read the gate from the aggregate columns. The `agg_*` / `attempt_*` split is deliberate.
2. **`openai-p6a1fe3` is not a different arm from `openai-codex`.** For OpenAI-OAuth turns the usage ledger
   records the pool-node id while the identity gate records the canonical provider, so the two columns show
   the same arm at two layers. Same class of two-level naming as note 1, opposite direction: here they agree.

## Detection list — every item re-derived, none taken from a lane's own prose

| item | status | observed |
|---|---|---|
| D01 | PASS | {"probe_exit": 0, "stdout_tail": "PLAN_LANE_PROBE_OK", "serving_rows": [["gpt-6.1-sol", "openai-codex", "https://chatgpt |
| D02 | PASS | {"exit": 0, "stdout_tail": "PLAN_TOOL_PROBE_OK", "stderr_tail": ""} |
| D03 | PASS | {"resolution_probe_tail": "EFFECTIVE_HERMES_HOME=C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\ |
| D04 candidate | PASS | {"grep_c_effort": "36"} |
| D04 canonical | BEFORE_STATE_ON_CANONICAL | {"grep_c_effort": "0"} |
| D05 candidate | PASS | {"pos_matching_effort": {"exit": 0, "code": null, "ok": true, "effort_verified": true, "declared_effort": "medium"}, "ne |
| D05 canonical | BEFORE_STATE_ON_CANONICAL | {"pos_matching_effort": {"exit": 0, "code": null, "ok": true, "effort_verified": null, "declared_effort": null}, "neg_ma |
| D06 candidate | PASS | {"pos_matching_effort": {"exit": 0, "code": null, "ok": true, "effort_verified": true, "declared_effort": "medium"}, "po |
| D06 canonical | PASS | {"pos_matching_effort": {"exit": 0, "code": null, "ok": true, "effort_verified": null, "declared_effort": null}, "pos_pa |
| D07 candidate | PASS | {"blank": {"exit": 0, "action": "allow", "reason": "no-session-id-unattributable"}, "null": {"exit": 0, "action": "allow |
| D07 canonical | BEFORE_STATE_ON_CANONICAL | {"blank": {"exit": 3, "action": null, "reason": null}, "null": {"exit": 3, "action": null, "reason": null}, "free_text": |
| D08 candidate | PASS | {"maker_write": {"exit": 0, "action": "deny", "reason": "maker-write-in-governed-round:WO-SC-1"}, "ordinary_read": {"exi |
| D08 canonical | PASS | {"maker_write": {"exit": 0, "action": "deny", "reason": "maker-write-in-governed-round:WO-SC-1"}, "ordinary_read": {"exi |
| D09 candidate | EXPECTED_ROOT_DIFFERENCE | {"exit": 1, "ran": ["Ran 82 tests in 22.101s"], "failures": ["FAIL: test_drift_injection_subcases (tests.test_lane_polic |
| D10 canonical | EXPECTED_ROOT_DIFFERENCE | {"exit": 1, "ran": ["Ran 74 tests in 23.596s"], "failures": ["ERROR: test_lane_effort_enforcement (unittest.loader._Fail |
| D11 | PASS | [] |
| D12 | RECORDED | {"ok": true, "reason": "SOD_OK glm-5.3-flash != gpt-6.1-sol", "plan": {"provider": "opencode-go", "model": "glm-5.3-flas |
| D13 | RECORDED | {"lanes\\EXECUTE\\BC1": {"ok": false, "code": "ERR_LANE_ALL_ROUTES_EXHAUSTED", "required_arm": "opencode-go/deepseek-v4. |
| D14 | PASS | {"attempts": {"V1": {"attempt": "V1", "ok": true, "exit": 0, "seconds": 122.08, "required_arm": "openai-codex/gpt-6.1-so |
| D15 | PASS | {"artifact": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\LANE-RELIABILITY-CLOSURE-20261016\\KANBAN_SWARM_GRAPH.json", |
| D16 | PASS | {"exit": 0, "tail": "Change 'hgk-lane-reliability-closure-20261016' is valid"} |
| D18 | PASS | {"artifacts_scanned": 159, "json_without_claim_ceiling": ["candidate\\config\\hermes-codex-lane.json", "candidate\\confi |
| D19 | PASS | {"matches": []} |
| D20 | PASS | {"config/model-lane-assignment.json": {"backup_exists": true, "backup_sha256": "6af264c9ffdb", "current_sha256": "d41f8f |

## Honest residuals (not smoothed)

- F1-PLAN-ROUTE-ROW-OUTLIER: registry routes[].PLAN (opencode-go/glm-5.3-flash) disagrees with the pool, the registry SoD block, the conformance test and the owner mandate. Out of scope this round; remediation priced in FINDINGS_F1_PLAN_ROUTE_OUTLIER.md.
- tests/test_lane_policy.py::test_registry_and_projection_shape is therefore RED on the canonical tree, and it is RED solely on F1 (the PLAN route row): both the test's other cases and everything else in the 7-module suite are green.
- PLAN and VERIFY/SECURITY are the SAME model (openai-codex/gpt-6.1-sol): plan-vs-checker MODEL independence is ABSENT and is declared as SOD006-C2 OPEN_OWNER_ORDERED. Only process / lane / evidence-path independence remains.
- EXECUTE lane-turn reliability: attempts BC1 and BC2 wedged (first file written, then no progress) and BC2 was terminated by the orchestrator on measurement. On the arm: the identity gate passed ONLY on BC3 (`required_arm == served_arm == opencode-go/deepseek-v4.1-flash`, `usage_receipt_ok: true`, rank 1). BC1's ATTEMPT-level attribution names the mandated arm (opencode-go/deepseek-v4.1-flash) but BC1's own aggregate verdict is `ok:false / ERR_LANE_ALL_ROUTES_EXHAUSTED / usage_receipt_ok:false / served_arm:null`, so BC1 does NOT establish arm identity; BC2 has no receipt at all and establishes nothing about the arm, although it DID produce the effort test module before wedging (tests/test_lane_effort_enforcement.py, mtime 11:30:24, 26 s into its own window and inside no other attempt's), which BC3 reused unchanged and which is therefore credited to BC2. Both fields are printed side by side in README's lane table for exactly this reason. The remedy applied in-round was an EDIT-ONLY turn (BC3), which completed in 74 s. A lane that wedges twice on the same brief shape is a standing reliability caveat for future rounds.
- The claim that the lanes are reliable rests on ONE successful EXECUTE turn and the PLAN plane probes; the first two EXECUTE turns did not complete. That is stated as a count, not smoothed.
- E11 (five AO-guard cases) remains a NAMED OPEN RESIDUAL from the previous round and is unchanged here.
- SELF-CORRECTION published with this packet: the first commit described BC1's ATTEMPT-level fields as the lane's served arm and receipt verdict, which overstated it. See the corrections block above and FINDINGS_SELF_CORRECTION_BC1_ARM_CLAIM.md. A round that only ever corrects other people's work has not looked at its own.
- The V1 checker brief was self-contradictory: it forbade every file write while requiring the checker to build mandate/pool fixtures. The checker refused to fabricate and returned UNCERTAIN with named_suite NOT_RUN; that refusal is why its other findings can be believed. The brief was repaired in-round to scope writes to the checker's own work directory, and V2 then seeded its own Shared Spine through the typed API with its own WorkOrder and CONFIRMED claim_B and claim_C. V1 is retained in the packet unedited: an acceptor is entitled to see that the first attempt did not agree and why.
- The checker's V2 caveat is adopted verbatim: the effort-axis checks are DECLARATION checks. They prove the mandate, the declared pool arm and the declared served effort agree; they are NOT proof of the backend's actual reasoning effort.
- Both checkers flagged registry integrity on the CANDIDATE copy (fatal /codex_sha256 drift, epoch 19). That is correct and expected: the candidate config/ is a pre-ChangeSet-A snapshot. ChangeSet A was applied to the CANONICAL config only, where canonical drift measures empty. The two facts are consistent, not contradictory, and both are published.
- Verification is only as independent as the sandbox: both checkers ran through the same CODEX CLI lane mechanism as the writer, and the V2 suite re-run was the 5-module named suite (71 tests, OK) rather than the 7-module run my harness performs. The failure counts in the two runs are therefore not comparable, and neither run is an acceptance.

## Independent verification (advisory, and it did not rubber-stamp)

The VERIFY/SECURITY lane ran twice over the frozen subject `c2527970…` (200 files, digest recomputed by the
checker itself and matched). V1 returned **`claim_B` UNCERTAIN, `claim_C` UNCERTAIN, suite NOT_RUN** because the
brief it was given forbade the file writes it also required — it refused to substitute static reading for observed
exit codes. That contradiction was a defect of my brief, is published unedited in this packet, and was repaired;
V2 then built its own fixtures, seeded its own Shared Spine and WorkOrder, and returned **`claim_B` AGREE,
`claim_C` AGREE**, with the named 5-module suite at exit 0 (`Ran 71 tests … OK`).

Adopted verbatim from the checker: *"These are declaration checks, not proof of actual backend effort."*
Neither verdict is an acceptance, and neither authorises a promotion or a merge.

## What an external acceptor should do

1. Recompute every file's sha256 against `PACKET_MANIFEST.json`. The packet is committed with
   `.gitattributes: * -text` so the delivered bytes are the produced bytes.
2. Re-run the named suite from the frozen candidate: 
   `python -B -m unittest tests.test_lane_effort_enforcement tests.test_governed_runtime_controller tests.test_role_binding_enforcement tests.test_mandatory_tool_guard tests.test_matrix_d_full`
3. Re-derive the six effort-axis cases and the five controller cases from your own fixtures (the
   `CHECKER_BRIEF.md` in this packet lists them).
4. Judge `F1` yourself: `tests/test_lane_policy.py::test_registry_and_projection_shape` fails on the
   canonical tree, and `FINDINGS_F1_PLAN_ROUTE_OUTLIER.md` prices the repair.

Correspondence with the local round directory: `HG-KSEOS/var/LANE-RELIABILITY-CLOSURE-20261016/`.
