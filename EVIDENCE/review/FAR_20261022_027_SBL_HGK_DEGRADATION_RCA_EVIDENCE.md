# EVIDENCE — ROUND-SBL-HGK-RCA-20261022 / FAR-20261022-027-sbl-hgk-degradation-rca

Single evidence MD for a governed FAR round executed under HG-KSEOS admission, with the current canonical
Hermes bound as its Runtime/Orchestration Plane.

| Field | Value |
|---|---|
| Round | `ROUND-SBL-HGK-RCA-20261022` |
| FAR run | `FAR-20261022-027-sbl-hgk-degradation-rca` (Fabric repo) |
| Requirement | `REQ-HGK-PRJ-SBL-HGK-RCA-20261022` — **FROZEN** (event `EVT-c090a87eaa0c007a`, v1) |
| TaskSpec | `TS-req-hgk-prj-sbl-hgk-rca-20261022` — **ADMITTED**, writable root = the FAR run directory |
| WorkOrder | `WO-TS-REQ-HGK-PRJ-SBL-HGK-RCA-20261022-EXEC` — writer `codex-lane:opencode-go/minimax-m3.1-flash-free@EXECUTE-rank1`, base_head `d62635626d5d2e54fe5bba22a500a17423c85719` |
| Acceptance | `ACC-REQ-HGK-PRJ-SBL-HGK-RCA-20261022` — **NOT_RUN** (by design: nothing applied, owner-only act) |
| Project | `HGK-P0` (lineage-continuous with the SBL R10 round) |
| Kanban | board `round-sbl-hgk-rca-20261022`, cards K1..K8 |
| Claim ceiling | **CANDIDATE_ONLY** research product: not an acceptance, not native integration, not an installation, not a promotion, not a release, no completion percentage, no cost figure. |

## 1. Model plan (owner stop-clause) — MANDATE vs OBSERVED

| Role | Owner mandate | Observed | Evidence |
|---|---|---|---|
| SBL-Commander & PLAN | DEEPSEEK V4.1 FLASH (opencode-go) | Hermes session plane `opencode-go/deepseek-v4.1-flash` | session runtime; `ResearchPlan.yaml.execution_lanes.PLAN` |
| SBL-EXECUTE & Codex bounded writer | MiniMax M3.1 Flash (opencode-go) via CODEX CLI | `opencode-go/minimax-m3.1-flash-free@EXECUTE-rank1`, `ok=true`, 3.78 s, usage ok | `var/ROUND-SBL-HGK-RCA-20261022/probe/exec_receipt.json` |
| Acceptance Challenge / AO / VERIFY / SECURITY | DEEPSEEK V4.1 FLASH via CODEX CLI | `opencode-go/deepseek-v4.1-flash@VERIFY_SECURITY-rank4`, `ok=true`, 2.50 s, usage ok | `.../probe/verify_receipt.json` |

**Plan AVAILABLE → the stop clause did not fire.** Disclosed deviation: the pool's DECLARED rank-1 for PLAN
and VERIFY_SECURITY is `openai-codex/gpt-6.1-sol`; this round pinned the owner's arms under the pool's own
`selection_semantics` ("the instructed entry replaces rank 1"). Declared plane ≠ served plane, by design, and
every receipt names the served arm. Recorded as `DEVIATIONS.tsv` D1.

## 2. What the round produced

| Artifact | Bytes | What it is |
|---|---|---|
| `OWNER_MANDATE.txt` | frozen owner text | the bind |
| `ResearchRequest.yaml` / `ResearchPlan.yaml` | admitted request + plan | R0/R1 |
| `ROUTE_DECISION.json` / `GSTACK_ROUTE_DECISION.json` | real route receipts | `RESEARCH_LITERATURE_REPO → NATIVE_WITH_SELECTED_ARIS / FAR_ROUTE_NATIVE_ARIS`; `brownfield → OPENSPEC / CERTIFIED_ACTIVE_BROWNFIELD`; `qa-review → gstack.review`; `ship → NATIVE (provider null while gstack.ship IS in ACTIVE_SELECTED)` |
| `evidence/W1_fabric_integration.md` | 34,637 | SBL × Fabric integration audit (ABSENT / ABSENT / ABSENT / CITED_ONLY) |
| `evidence/W2_base_drift.md` | 4,872 | base drift, orchestrator-re-derived |
| `evidence/W3_capability_probe.md` | 61,182 | seven surfaces + self-* measured |
| `evidence/W4_performance_delta.md` | 25,396 | artifact-only performance comparison |
| `ResearchSynthesis.md` | 37,235 | the report (zh-TW, §0–§9) |
| `FINDINGS.tsv` | 12,542 | F1..F34, classes structural/process/declarative/defect/method/claim |
| `VERDICT.json` | 29,474 | FAR-VERDICT/1: answers Q1–Q4, 10 capability states, mandate, open_items |
| `DEVIATIONS.tsv` | 1,406 | D1–D5 |
| `ProposedEvolution.yaml` | 3,381 | EV1–EV6, candidate-only |
| `ResearchHandoff.yaml` | 2,402 | RS1–RS7, owner-ready |
| `LEARNING.md` | 6,272 | the round's governed self-learning/iteration/evolution record |
| `VERIFY_REPORT.md` | 4,236 | verbatim transcription of the checker's verdict |
| `ORCHESTRATOR_ADDENDUM.md` | 3,786 | D6–D9 concurrency + stall census |

## 3. Lanes actually run (this round, not inherited)

| Gate | Lane / principal | Identity | Result |
|---|---|---|---|
| K1 admission | Shared Spine typed API | orchestrator | REQ FROZEN, TS ADMITTED, WO CREATED; readback printed |
| K2 SWARM | 4 parallel `delegate_task` workers | gpt-6.1-sol | W1/W3/W4 persisted; W2 refused by the session pre-write guard → orchestrator re-derived all its numbers |
| K3 GSTACK/OPENSPEC+FAR route | `hg_kseos.named_methods.route` + `far_router.route` + `openspec` CLI | orchestrator | measured, receipts on disk |
| K4 EXECUTE | CODEX CLI, `opencode-go/minimax-m3.1-flash-free@rank1` | writer | 6 deliverables; 2 timeouts + 1 pre-dispatch refusal + 1 success (282.67 s) |
| K5 VERIFY/SECURITY | CODEX CLI, `opencode-go/deepseek-v4.1-flash@rank4`, read-only, own process | checker | `VERDICT: PASS`, `UNVERIFIED: NONE`, A1–A9 |
| K6 AO | fresh-context subagent, no access to the writer transcript | officer | see §5 |
| K7 freeze/mirror | `freeze.py` | orchestrator | index + three-root byte-identical mirror |
| K8 evolution | `LEARNING.md` + `ProposedEvolution.yaml` + `ResearchHandoff.yaml` | orchestrator (governed record) | candidate-only, nothing promoted |

Separation of duties: writer ≠ checker ≠ officer, at lane, entry-point and process level. **Same-model
residual:** the mandated checker (deepseek-v4.1-flash) is the same model as the mandated PLAN/Commander
(session plane); independence survives at lane/entry-point/evidence-path level only, not at model level. Stated,
not glossed.

## 4. The six answers (short form; the report carries the locators)

- **Q1 — is SBL integrated into the Fabric governance contract?** No. Fabric schemas, install/registration
  target and evidence/packet contract are **ABSENT**; HGK WorkOrder/Permit issuance is **CITED_ONLY**. Fabric
  appears in SBL only as a hashed non-governing `AGENTS` support source (`governs: false`). SBL's own record
  says `NO_SBL_INSTALL_TARGET`, ceiling `STANDALONE_ONLY`, `native_effect: NOT_GRANTED`.
- **Q2 — is SBL on the current HG-KSEOS base?** No. It is **18 commits / 278 changed paths** (260 A / 18 M / 0 D)
  behind `3dfaebc`, its own handover pins `b22706e` and states no conformance measurement exists after it, its
  compatibility gate is a **version pin that cannot fail** (`>=0.1.0,<0.2.0` on a package whose version has not
  moved in 147 of 148 commits), and the interpreter its adapter records cannot `import hg_kseos`
  (`ModuleNotFoundError`; `dependencies = []`). Not a stale root, not a source fork.
- **Q3 — why does "SBL & HG-KSEOS" perform worse than HG-KSEOS alone?** The measurable degradation is
  **acceptance throughput** and **declared-vs-implemented consistency**, not time or money: 3/3 sampled SBL
  rounds end `FAILED` / acceptance `FAIL`; 32 unclaimed ready cards across three SBL boards; recurring
  cross-surface disagreement that the drift gate structurally cannot see (it compares each pin to its file, never
  two surfaces to each other). A cost premium is **NOT_SUPPORTED_BY_ARTEFACTS** (relay ledger: 21,008 rows, no
  round field → `NOT_MEASURABLE`; full-round wall-clock 0/8 measurable).
- **Q4 — can it really enable all seven surfaces + self-*?** **No, not as specified.** Measured:
  KANBAN PARTIAL, SWARM PASS (graph only), GSTACK PARTIAL, OPENSPEC **FAIL** (`openspec validate --all` = 37
  passed / 2 failed, exit 1), CODEX_CLI PASS (receipt scope), SUB_AGENTS PARTIAL, self-detect PASS (detection
  exists, no mandatory caller), self-repair PARTIAL (planner, no executor), self-accept **FAIL**, self-evolve
  **FAIL** (ledger, no apply/validate/rollback consumer).

**The load-bearing conflict:** "self-accept" and separation of duties are structurally incompatible. SBL raises
`SBL_E_SELF_CHECK_FORBIDDEN` for maker == checker; HG-KSEOS raises `ERR_WORKORDER_SELF_REVIEW` before opening a
transaction (`src/hg_kseos/spine.py:345-346`, re-opened by the checker). The defensible vocabulary is
**self-detect + self-repair + acceptance by an independent lane** — which is exactly how this round was run.

## 5. Independent verdicts

- **VERIFY_SECURITY (checker):** `VERDICT: PASS`, `UNVERIFIED: NONE` — verbatim in `VERIFY_REPORT.md`, with the
  honest note that the lane receipt code was `ERR_NO_ARM_EMITTED_NONCE` while `usage_receipt_ok=true`
  (2,238,514 in / 57,737 out tokens) and the verdict rests on 293,518 B of persisted stdout.
- **Acceptance Officer (fresh context, gpt-6.1-sol, no writer transcript):**
  `ACCEPTANCE_OFFICER_VERDICT: FAIL` — `CONFIDENCE: high`; two overclaims found, both in this round's own files:
  (AO-1) `ResearchSynthesis.md:143` attributed the three sampled rounds' missing acceptance to the
  self-accept/SoD collision without a mechanism, and (AO-2) `ORCHESTRATOR_ADDENDUM.md:12` understated the
  mid-round control-plane advance as 3 commits where `git rev-list --count` returns 9. It recorded **no missing
  or out-of-bounds finding locators**. Full text: `ACCEPTANCE_OFFICER_VERDICT.md`.
- **Disposition of the round: `AO_FAIL_THEN_CORRECTED`.** Both defects were corrected in place and disclosed with
  before/after in `POST_FREEZE_CORRECTIONS.md`; no second officer was dispatched, so this is **not** a PASS and
  the HGK acceptance stays `NOT_RUN`. The gap that let AO-1 through is recorded as learning `L9`: an A-list that
  tests ceilings, states and figures can still miss a causal sentence — the criterion the maker writes for the
  checker is itself a defect until it is checked against the admitted contract.
- **The officer also downgraded the checker's PASS:** "A4 and the admitted root-cause criterion require more than
  an explicit answer: the checker missed the unsupported causal attribution, so its unconditional PASS is not
  fully earned." The PASS in `VERIFY_REPORT.md` is transcribed verbatim and stands as what the lane returned; this
  round does **not** claim it was a complete verification of the root-cause answer. Two other officer notes were
  acted on at seal 2: `ResearchHandoff.yaml`'s `resume_command` carried a `<RANK_PIN_FLAG>` placeholder (not
  copy-ready → now the literal flag plus a guard note) and RS4 targeted the superseded `3dfaebc` (now the live
  head).

## 6. Deviations and non-claims (all disclosed, none repaired by loosening a gate)

D1 pinned vs declared arms · D2 slice-1 timeout with 3/6 files landed · D3 slice-2 timeout, 0 files · D4 blocked
child write re-derived by the orchestrator · D5 adversarial-challenge FAR class routes `NATIVE_NO_CHALLENGE` ·
D6 HG-KSEOS advanced `3dfaebc → 5ae4190` mid-round (3 commits by another session, 11:32) · D7 the audited SBL
board drained 3 of 23 cards mid-round · D8 stall census · D9 the grouped-vs-split SELF_* row discrepancy · D10 the acceptance officer returned FAIL on
two overclaims in this round's own artefacts, both corrected in place after the officer's read (`POST_FREEZE_CORRECTIONS.md`).

Not claimed: acceptance, promotion, push, release, native integration, installation, conformance on the current
head (`5ae4190`), per-round cost, and any completion percentage.

## 7. Integrity

`EVIDENCE_INDEX.json` lists every file in this directory with bytes and sha256, each recomputed from disk at
seal time with the count asserted; the index's own digest is reported separately in
`EVIDENCE_MIRROR_RECEIPT.json`, which also records the byte-identical mirror into
`HG-KSEOS|Fabric|SQS-THC evidence/review/`. An integrity readback is not an acceptance.
