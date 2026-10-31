| Recorded metric (primary sample) | SBL + HG-KSEOS: FAR 023 / 025 / 026 | HG-KSEOS-only: remediation / MiniMax / fallback reorder |
|---|---:|---:|
| Rounds examined | 3 | 3 |
| Round-level recorded WorkOrder outcomes | 3 FAILED; R7 also preserves a ROLLED_BACK chain | 1 VERIFIED; 1 CREATED workorder family; 1 NA (state absent from reviewed receipts) |
| Recorded acceptance outcomes | 3 FAIL | 1 NOT_RUN; 2 NA (no acceptance-row verdict in reviewed receipts); neither claims acceptance |
| Finding rows | 44 = 19 + 14 + 11; not 44 unique defects | NA comparable inventory; MiniMax self-review has 4 defects and AO transcription 2 open items |
| Retained spawned lane attempts, all roles | 39 | 15 |
| Retained EXECUTE-role attempts (includes probes) | 8 | 5 |
| Timed-out spawned attempts | 0 | 4 |
| Sum of retained attempt seconds, all roles | 2,611.06 s | 2,983.27 s |
| Full-round wall-clock duration measurable | 0/3 | 0/3 |
| Round-attributed relay usage / token / monetary cost | NOT_MEASURABLE | NOT_MEASURABLE |

# W4 — recorded performance delta and residual adjudication

## Ruling and scope

**Measured: the sampled SBL rounds repeatedly did not obtain acceptance. Not measured: that SBL makes HG-KSEOS materially slower or more expensive.** The controls also exhibit missing acceptance, sandbox-related timeout losses, nonce errors and cross-surface drift. The partial lane sample contains *more* SBL attempts but *fewer* seconds and timeouts; none is a normalized end-to-end cost comparison. Do not interpret FAILED as proof that the delivered product failed its tests: R7 maps INCONCLUSIVE to FAIL, R9 had no independent acceptance, and R10 requires a different session to validate its handover.

This is an artifact-only, read-only audit. No tests, dispatches, builds, admission APIs, database mutation, git mutation or network calls were run. Only this output file is written. Existing evidence is historical, not independently re-executed now. Cohorts were selected for contemporaneous lane binding/remediation, candidate-only effects and checker use, not randomly or as matched workloads. The three HGK controls have no SBL in their directory names; their product scope is HGK/runtime routing. MiniMax's explicit `SBL-EXCLUSION-NOTE.md` also distinguishes its work from concurrent SBL work. The same shared lane machinery and concurrent orders confound causal attribution.

Primary sources use these absolute prefixes:

- **FAR** = `C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/`.
- **SBL** = `C:/Projects/Agent_Workspace/SBL/`.
- **HGK** = `C:/Projects/Agent_Workspace/HG-KSEOS/`.

Required FAR source sets were read: `VERDICT.json`, `FINDINGS.tsv`, `ResearchRunReceipt.json`, `LEARNING.md` in `FAR-20261021-023-sbl-r7-residual-closure/`, `FAR-20261021-025-sbl-r9-ctrlpkg/`, `FAR-20261021-026-sbl-r10-handover/`. Findings were parsed as TSV rows, not counted by prose mentions. R7's F10/F17, F13/F16 and other overlaps make the finding-row total unsuitable as a unique-defect total.

## Per-round measurements

A number is a retained-evidence count, never an assertion of exhaustive historical coverage. EXECUTE is the receipt's role/lane, not a claim that product implementation ran. In R9/R10 the retained EXECUTE calls are availability probes, not substantive writer work. Full-round duration is NA throughout: there is no complete start/end pair covering admission, execution, interruptions and acceptance. Timestamped verdicts and seal receipts are not starts.

| Round / source | Full-round wall span | EXECUTE attempts | All-role attempts / seconds | Timeouts | WorkOrder state | Acceptance | Findings / defects | Independent verify lane actually ran? |
|---|---|---:|---:|---:|---|---|---|---|
| SBL R7 / FAR 023 | NA: no full start/end pair | 5 | 30 / 2,577.09 s | 0 | FAILED; earlier chain ROLLED_BACK | FAIL (checker INCONCLUSIVE, not accepted) | 19 TSV rows | Yes: rounds 1, 2, 4 served; final round 4 INCONCLUSIVE |
| SBL R9 / FAR 025 | NA: no full start/end pair | 1 | 3 / 12.06 s | 0 | FAILED | FAIL (no independent acceptance) | 14 TSV rows | No substantive checker receipt found; VERIFY gate probe only; 4 research workers are not acceptance |
| SBL R10 / FAR 026 | NA: no full start/end pair | 2 | 6 / 21.91 s | 0 | FAILED | FAIL (fresh-session criterion unmet) | 11 TSV rows | No substantive checker receipt found; 2 VERIFY probes only; workers=0 |
| HGK FAR-REMEDIATION-20261021 | NA: no full start/end pair | 2 | 3 / 244.49 s | 0 | CREATED for recorded P0..P4/AO family | NA: verdict row not supplied; receipt explicitly says no independent acceptance | NA: no exhaustive finding ledger in reviewed round receipts | Attempted; AO process returned error, no substantive verdict |
| HGK FAR-MINIMAX-MANDATE-20261021 | NA: no full start/end pair | 3 | 8 / 2,065.86 s | 3 | NA: not in reviewed receipts | NA: no acceptance-row verdict; signed AO verdict missing | 4 self-review defects; 2 AO open items, not additive unique defects | Yes: substantive AO checks; no persisted signed verdict; 3 timeouts |
| HGK FAR-FBKREORDER-20261021 | NA: no full start/end pair | 0 retained; total implementation attempts NA | 4 / 672.92 s | 1 | VERIFIED | NOT_RUN | NA exhaustive defect count; 3 semantic checker verdicts FAIL/PASS/FAIL on differing criteria | Yes: latest semantic verdict FAIL; middle PASS checked wrong retention criterion |

Sources: R7 `SBL/_governance/round-20261021-r7/90_EVIDENCE/SBL_R7_EXECUTION_STATUS.json` (use `hgk_admission.second_attempt`, not its stale original CREATED field), `40_VERIFY/CHECKER_STATUS.json`, and `HGK/var/R7-LANES/`. R9/R10 FAR verdicts supply lifecycle state. HGK-only state/ceilings come from `var/FAR-REMEDIATION-20261021/RECEIPT.md`, `var/FAR-MINIMAX-MANDATE-20261021/{CHECKPOINT.md,SELF-REVIEW.json,AO2_findings_transcribed.json}`, and `var/FAR-FBKREORDER-20261021/EVIDENCE.md` §11. The fallback WorkOrder VERIFIED / acceptance NOT_RUN / checker FAIL disagreement is explicitly retained, not converted to an accepted control.

### R8 / R11 coverage (not silently missing and not pooled into the primary FAR comparison)

| Additional slot | EXECUTE / all attempts / seconds | Timeouts | State, verdict, findings, independent verify |
|---|---|---:|---|
| SBL R8, `SBL/_governance/round-20261021-r8/LANE_MANDATE_R8.json`; `HGK/var/R8-GATE/` | 3 / 9 / 31.17 s | 0 | Own WorkOrder/acceptance NA (not supplied); carries R7 non-acceptance, 3 named R8 defects D1–D3; VERIFY availability probes, not substantive independent acceptance. Full duration NA. |
| R11 nearby lane mandate, `HGK/var/R11-LANE-MANDATE-20261021/` | 1 / 3 / 17.10 s | 0 | All three probes served; SBL round attribution not proven by these receipts. WorkOrder, acceptance, findings and substantive independent verification NA. Full duration NA. |

`SBL/_governance/round-20261021-r11/` is absent; no r11-named file was found in the three requested SBL evidence roots. No `SBL/_governance/lifecycle*.json` exists. Therefore do not infer a completed SBL R11 from three HGK lane probes. Full-round measurable durations: **0/6 primary rounds; 0/8 inspected round/slot rows including R8 and the unassigned R11 probes**.

## Error and retry accounting

| Round | Codes retained in resolution receipts (receipt count, not unique incidents) | Additional recorded limitations |
|---|---|---|
| SBL R7 | ERR_NO_ARM_EMITTED_NONCE ×5; ERR_REQUIRED_ARM_NOT_SERVED ×1; ERR_LANE_PIN_IDENTITY_INVALID ×3; ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED ×1 | ERR_LANE_TOOLCHAIN_BINARY_MISSING in causal detail; provider usage-limit exhaustion; one owner shutdown interruption. Quota failure is not a timeout. |
| SBL R9 | None in 3 retained gate receipts | No independent acceptance; absence of an error in probes does not mean zero implementation errors. |
| SBL R10 | None in 6 retained gate receipts | DRIFT_VALUE in historical rebind findings; no fresh-session handover check. |
| HGK remediation | ERR_LANE_ALL_ROUTES_EXHAUSTED ×1 | RECEIPT.md also records ERR_LANE_REQUIRED_ARM_ABSENT on stale rank and HTTP 400 “Model is unavailable”; no signed AO verdict. Its provider-transient attribution is the receipt's diagnosis, not re-proven here. |
| HGK MiniMax | ERR_LANE_ALL_ROUTES_EXHAUSTED ×3; ERR_LANE_REQUIRED_ARM_ABSENT ×2; ERR_NO_ARM_EMITTED_NONCE ×1 | Three timeouts: 600.03, 540.06, 900.02 s; AO write denial and concurrent pool movement. Early top-level admission summary says REFUSED; later `admission/admission_summary.json` records ADMITTED. Preserve chronology, not an apparent contradiction. |
| HGK fallback | ERR_NO_ARM_EMITTED_NONCE ×1 in retained final resolution JSONs | Append-only history preserves a 300.02 s timeout overwritten in dispatch3.json; EVIDENCE.md also records guard-required, arm-absent and 2 worker HTTP-429 failures; these prose events are not added to spawned-attempt counters. |

Method: read only immediate JSON / `*.attempts.ndjson` in each named evidence directory. Parse attempt arrays and append-only histories; deduplicate by recorded `stdout_path`, so the same attempt in JSON and NDJSON is counted once. The latter is essential: fallback `verify-lane/dispatch3.json.attempts.ndjson` has both the lost timeout and the later 275.78 s attempt, while `dispatch3.json` holds only the latter. No deep temporary-tree census was used. Interrupted dispatches without completed attempt receipts are not invented or counted as timeouts.

### Timing and accounting ceilings

All-role seconds sum each retained attempt's `seconds`; concurrent calls may overlap. These totals exclude orchestration, human pauses, builds/tests outside these calls, unretained attempts and research workers. They are neither wall-clock time nor billable usage. Report the full-round duration as NA, not the difference between FAR 025 and 026 seal times.

The following are **receipt timestamp coverage**, not round duration (earliest/latest `generated_utc` among the retained resolution JSONs):

- SBL-R7: `2026-10-21T05:23:17.031616+00:00` → `2026-10-21T10:50:39.037906+00:00`; 19642.006 s of timestamp coverage.
- SBL-R9: `2026-10-21T13:28:19.299436+00:00` → `2026-10-21T13:28:31.094815+00:00`; 11.795 s of timestamp coverage.
- SBL-R10: `2026-10-21T14:29:55.583797+00:00` → `2026-10-21T14:34:06.273969+00:00`; 250.690 s of timestamp coverage.
- HGK-remediation: `2026-10-21T04:10:26.930583+00:00` → `2026-10-21T04:32:03.299931+00:00`; 1296.369 s of timestamp coverage.
- HGK-minimax: `2026-10-21T05:43:58.523877+00:00` → `2026-10-21T07:42:08.673022+00:00`; 7090.149 s of timestamp coverage.
- HGK-fallback: `2026-10-21T05:55:17.811691+00:00` → `2026-10-21T06:24:34.456259+00:00`; 1756.645 s of timestamp coverage.
- SBL-R8: `2026-10-21T12:55:15.016923+00:00` → `2026-10-21T13:11:09.805209+00:00`; 954.788 s of timestamp coverage.
- SBL-R11: `2026-10-21T15:11:29.655028+00:00` → `2026-10-21T15:11:51.380313+00:00`; 21.725 s of timestamp coverage.

Relay accounting was located via `HGK/scripts/hgk-lane-dispatch.py:81`: `%LOCALAPPDATA%/HG-KSEOS/opencodex-hermes/usage.jsonl`, resolving here to `C:/Users/user/AppData/Local/HG-KSEOS/opencodex-hermes/usage.jsonl`. The one read parsed **21,008 rows, 0 malformed**. Top-level fields include requestId, timestamp, provider, model, conversationId, status, durationMs and usage; **no round field** was found. Per the requested rule, round-attributed relay-row counts are **NOT_MEASURABLE**. Global rows are not a round denominator. `usage_rows_after_offset` in receipts is not summed: concurrent traffic can contaminate that interval. No dollar-rate table or complete round-token join was available; no money estimate is made.

## Measured / inferred / unsupported

**MEASURED**

- Primary SBL rounds: 3/3 recorded FAILED and acceptance FAIL; no independent acceptance PASS. R7 preserves a rollback of a premature PASS. This is an acceptance-throughput deficit within that programme, not a matched comparative product failure rate.
- Controls: one recorded VERIFIED WorkOrder still leaves acceptance NOT_RUN; remediation remains CREATED; MiniMax lacks a recorded lifecycle verdict in reviewed receipts and a signed AO verdict. Hence the controls are not a clean “successful HGK-only” baseline. Failure-rate ratios are not computable with a missing state and different acceptance criteria.
- Primary retained attempts: SBL 39 versus controls 15; EXECUTE-role calls 8 versus 5. SBL has 0 timed-out attempts versus controls' 4. Partial all-role seconds are 2,611.06 versus 2,983.27. Unequal capture, many probes and unmatched work prevent using these as comparative cost ratios.
- Repeated D1-class cross-surface gaps exist on both sides: MiniMax `SELF-REVIEW.json` D1/D2; SBL R8 D1; FAR 025 F2/F3/F4/F5; FAR 026 F1/F2. FAR 026 explicitly calls its D1 the third reproduction. This is a recorded recurrence statement, not three fresh defects counted from repeated prose. R7 checker D1 (blanket build skip) is a different identifier/class and is not merged with routing D1.
- Product progress is also recorded: R9 fixes 4→0 acceptance-pointer mismatches without changing 34 edges, pins 14 control-document digests, and reports 218 passed / 2 skipped on its candidate. R8's historical same-environment conformance improves 575 passed / 21 failed to 580 / 16, with 0 new failures; three untracked test files prevent clean-checkout reproduction. No R10 conformance re-measurement is recorded after b22706e.
- R10 handover backlog: 7 open entries, independently recounted from `HANDOVER_STATE_R10.json.open`. These are distinct from frozen R6 scope ledgers: 149/149 children OPEN; 50 parents (37 OPEN, 13 PARTIAL_EVIDENCE_ONLY); 38 surfaces (21 OPEN, 12 PARTIAL_LOCAL_SCOPED, 5 NOT_ADMITTED_NO_DISPATCH). They are not current-round closures or an additive common denominator. The child ledger's open=186 counts 37 wholly-OPEN parents +149 children; 13 partial parents are also not fully closed.

**INFERRED**

Repeated incomplete acceptance, poorly scoped gate assertions, writable-scratch mismatches and duplicated routing declarations plausibly consume rework. Shared HGK mechanisms can propagate delays into SBL; additional contract/host/SP obligations plausibly enlarge the work. These are supported mechanisms and scope differences, not measured incremental SBL cost or regression-introducing changes.

**NOT_SUPPORTED_BY_ARTEFACTS**

“SBL+HGK is materially slower/more expensive than HGK-only,” any percentage cost premium, a causal claim that SBL introduced the shared failures, an apples-to-apples round failure-rate ratio, a completed SBL R11, current conformance after the R10 rebind, or full-contract completion percentage. No full-round timing series, round-tagged relay usage, normalized work units or semantic contract denominator exists in the reviewed evidence. Treating additional recorded findings as worse quality also ignores audit coverage and duplicate findings.

## Newest SBL FAR residual worklist: what this read-only round can close

Newest *required SBL-programme FAR round* is 026 (R10). Its exact `next_best_action` is: **“R10-01 (re-measure conformance) as the first action because it gates every other claim, then R10-02 for the first independent verdict.”** The machine handover calls these CONFORM and R9-02 respectively. Reconcile those labels; do not create additional work items from the aliases.

| Residual / source | Recorded fact and close condition | Adjudication in this audit |
|---|---|---|
| R10-01 / CONFORM | Conformance not re-measured after b22706e. Needs absolute + same-baseline measurement. | OPEN. Historical 580/16 is not the requested post-rebind result; executing pytest would violate the read-only / one-file scope and can append evidence. |
| R10-02 / R9-02 independent acceptance | Needs authorized writable isolated checker scratch and one independent verdict bound to frozen subject, persisted readably. | OPEN. R7 has a genuine INCONCLUSIVE verdict, not no checker; R9/R10 probes do not supply acceptance. This audit cannot self-accept. |
| R9-04 Runtime/Orchestration permit | Needs scoped permit from HGK binding/permit authority, read back. | OPEN. An availability probe or local binding is not issuer authority. |
| R9-05 clean-checkout reproducibility | Three test files untracked; owner disposition and reproducible clean-checkout counts required. R10 F7 also records ignored var/ instruments. | OPEN. Historical defect and exact missing-test count are established; no files staged or policy changed here. |
| R9-06 lifecycle _repo_head CWD/swallowed invariant | Needs clean-baseline regression test with project repo different from caller CWD and no swallowed InvariantViolation. | OPEN. R7 workaround + FAR 025 F10 establish the defect; no repair demonstrated by reviewed successor evidence. |
| SP-INT / FAR 026 F11 | Dispatcher binds models, not SPs; no inspected path invokes commander_sp/external_challenge_sp/sign_verdict. Needs admitted thin adapters at PLAN handoff / VERIFY pre-spawn with real invocation receipts. | OPEN implementation. Evidence closes the diagnostic ambiguity: model servability is not SP integration. No current source-wide absence claim beyond recorded inspections. |
| DOC-00..13 semantic denominator | Package declares UNKNOWN / UNRESOLVED / NOT_ESTABLISHED. Needs semantic denominator before phased full-contract execution; recorded 10 engineer-day stop-loss is a plan, not measured effort. | OPEN engineering scope. CLOSED research question: inventory counts cannot justify a completion percentage. |
| FAR 026 F8 installation | Package + standalone bootstrap + adapter files hold (3/5); effective host installation and native integration do not. ABI says native_effect/permit_signing/workorder_admission not_provided. | OPEN host/native requirements. CLOSED classification question: 3/5 is an installation-achievement taxonomy, not full capability completion; 9/9 selftest and ROOT_READY 6/6 cannot close it. |
| FAR 026 F9 FABRIC target | FABRIC has no SBL installation target; none manufactured. | CLOSED as a recorded scope/target question (NO_TARGET / not attempted); not a successful FABRIC install and not authority to invent a target. |

Thus **no engineering/acceptance residual is newly closed**. This audit closes evidence/classification questions only: cost premise unproven, historical acceptance and retries quantified, FABRIC target non-applicability established, and host/SP ceilings disambiguated. Seven machine-listed open items remain open; F8/F9/F11 clarify related boundaries rather than adding a fabricated closure count.

## Claim ceilings (exact source wording)

- `FAR-20261021-023-sbl-r7-residual-closure/VERDICT.json.claim_ceiling`: `SCOPED_R7_CLOSURE_ONLY__EXACT_RECEIPTS__THREE_MERGES_AND_A_PRERELEASE_EXECUTED__INDEPENDENT_VERDICT_IS_INCONCLUSIVE_NOT_ACCEPTED__HGK_ACCEPTANCE_RECORDED_AS_FAIL__NOT_FULL_CONTRACT_PASS__RELEASE_IS_A_PRERELEASE_NOT_LATEST__NO_NATIVE_ISSUER_NO_HOST_GRANT__FOUR_CONTRACT_CAPABILITY_BINDINGS_OPEN__CANONICAL_HERMES_BINDING_RECEIPT_MISSING__LINUX_NATIVE_REPRODUCTION_NOT_RUN`
- `FAR-20261021-025-sbl-r9-ctrlpkg/VERDICT.json.claim_ceiling`: `CANDIDATE_ONLY. Two verified corrections. No acceptance, no native integration, no host installation, no full-contract closure, no completion percentage.`
- `FAR-20261021-026-sbl-r10-handover/VERDICT.json.claim_ceiling`: `CANDIDATE_ONLY. Candidate pool and candidate declarations re-ordered under owner authority. Not an acceptance, not native integration, not host installation, not a full-contract closure, no completion percentage.`
- SBL R8 `LANE_MANDATE_R8.json.claim_ceiling`: `CANDIDATE_ONLY lane re-order under owner authority. Not a native issuer signature, not an acceptance of any subject, not a promotion of the pool to ACTIVE. The lane arm is measured available and serving; that is availability, not acceptance.`
- R11 lane probe receipt ceiling (availability only): `a pass here proves the Codex-CLI lane served this turn through the relay with a matching usage receipt; it is not an acceptance of any subject`.
- HGK remediation `RECEIPT.md`: “locally verified”; “No independent acceptance, no external acceptance, no release.”
- HGK MiniMax `AO2_findings_transcribed.json.claim_ceiling`: `transcribed findings from a run whose own verdict file was never written. The transcription is faithful to the run's command outputs, but it is NOT the AO's own signed verdict. A re-run is required for a signed verdict.`
- HGK fallback `EVIDENCE.md`: `APPLIED_AND_LOCALLY_VERIFIED (live config bytes) + independent readback. Not a release, not a promotion.` Acceptance remains NOT_RUN despite the WorkOrder's recorded VERIFIED state.

## Extraction manifest (source locators; no extra files emitted)

Receipt inventories below define the exact count boundaries. Counts include only deduplicated spawned attempts in these immediate directories; refusal-code counts use the retained resolution snapshots and are explicitly not exhaustive historical error counts.

### SBL-R7
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/R7-LANES`

Resolution JSONs read: `probe2_EXECUTE.json`, `probe2_PLAN.json`, `probe2_VERIFY_SECURITY.json`, `probe_canonical_PLAN_minimax.json`, `probe_canonical_VERIFY_minimax.json`, `probe_canonical_VERIFY_minimax2.json`, `probe_EXECUTE.json`, `probe_final_EXECUTE_deepseek.json`, `probe_final_PLAN_gpt.json`, `probe_final_VERIFY_gpt.json`, `probe_gpt_61sol_VERIFY.json`, `probe_gpt_61sol_VERIFY2.json`, `probe_gpt_61sol_VERIFY3.json`, `probe_minimax_VERIFY.json`, `probe_PLAN.json`, `probe_VERIFY_SECURITY.json`, `resume2_probe_EXECUTE.json`, `resume2_probe_PLAN.json`, `resume2_probe_VERIFY_SECURITY.json`, `resume_probe_EXECUTE.json`, `resume_probe_PLAN.json`, `resume_probe_VERIFY_SECURITY.json`, `verify_chk_r7_a1.json`, `verify_chk_r7_a2.json`, `verify_chk_r7_a3.json`, `verify_chk_r7_a4.json`.

Deduplicated attempts: 30; EXECUTE: 5; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### SBL-R9
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/R9-GATE`

Resolution JSONs read: `gate_EXECUTE.json`, `gate_PLAN.json`, `gate_VERIFY_SECURITY.json`.

Deduplicated attempts: 3; EXECUTE: 1; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### SBL-R10
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/R10-GATE`

Resolution JSONs read: `final_EXECUTE.json`, `final_PLAN.json`, `final_VERIFY_SECURITY.json`, `gate_EXECUTE.json`, `gate_PLAN.json`, `gate_VERIFY_SECURITY.json`.

Deduplicated attempts: 6; EXECUTE: 2; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### HGK-remediation
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-REMEDIATION-20261021/probes`

Resolution JSONs read: `AO_verdict.json`, `EXECUTE_apply.json`, `probe_MINIMAX_EXECUTE.json`.

Deduplicated attempts: 3; EXECUTE: 2; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### HGK-minimax
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-MINIMAX-MANDATE-20261021/probes`

Resolution JSONs read: `AO_FINAL2_receipt.json`, `AO_FINAL3_receipt.json`, `AO_FINAL_receipt.json`, `AO_minimax_binding.json`, `EXECUTE_admit.json`, `EXECUTE_minimax.json`, `EXECUTE_minimax2.json`, `PLAN_admit.json`, `VERIFY_admit.json`, `VERIFY_minimax.json`.

Deduplicated attempts: 8; EXECUTE: 3; timeouts: 3. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### HGK-fallback
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-FBKREORDER-20261021/verify-lane`

Resolution JSONs read: `dispatch.json`, `dispatch2.json`, `dispatch3.json`.

Deduplicated attempts: 4; EXECUTE: 0; timeouts: 1. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### SBL-R8
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/R8-GATE`

Resolution JSONs read: `final_probe_EXECUTE.json`, `final_probe_PLAN.json`, `final_probe_VERIFY_SECURITY.json`, `mandate_probe_EXECUTE.json`, `mandate_probe_PLAN.json`, `mandate_probe_VERIFY_SECURITY.json`, `probe_execute_minimax.json`, `probe_PLAN.json`, `probe_VERIFY_SECURITY.json`.

Deduplicated attempts: 9; EXECUTE: 3; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

### SBL-R11
Directory: `C:/Projects/Agent_Workspace/HG-KSEOS/var/R11-LANE-MANDATE-20261021`

Resolution JSONs read: `EXECUTE_deepseek.json`, `PLAN_gpt61.json`, `VERIFY_gpt61.json`.

Deduplicated attempts: 3; EXECUTE: 1; timeouts: 0. Paired `*.attempts.ndjson` files, where present, were read and joined by stdout path.

Raw final assistant messages were also parsed from the source stdout paths in R7 checker receipts and the three HGK control checker receipts. This confirmed R7 round 4 INCONCLUSIVE / NOT ACCEPTED, fallback FAIL/PASS/FAIL, and missing signed MiniMax verdicts; a dispatcher ok=true was never treated as semantic PASS. R7 round 2 is 1,395.41 s and round 1 includes a 464.74 s fallback in addition to the 392.58 s quota-ended primary: reporting only the widely quoted 392 s and 237.3 s would undercount the preserved work.

No complete round duration, token bill, unique programme-defect total, or new engineering closure is claimed. No independent acceptance of this audit was performed in this worker.
