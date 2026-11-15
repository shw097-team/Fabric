# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: CNV-FAR018-FAR019-ARCHIVE-20261016
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Under the Fabric governance contract with HG-KSEOS as the sole control plane and canonical Hermes as its governed Runtime/Orchestration Plane, archive the three EXISTING candidate evidence pull requests #12 (R7R11 archive), #13 (FAR-018) and #14 (FAR-019) into shw097-team/Fabric as candidate evidence, under one bounded maintainer authorisation: freeze each PR's live HEAD, prove each diff stays inside its single EVIDENCE prefix, run a trusted scoped secrets scan with positive and clean controls, take a single bounded owner-approved merge batch, merge each PR normally at its approved exact SHA, read the merged prefix and blobs back from main, and publish a machine-readable evidence return pack. No product, runtime or world effect: this round changes only archived candidate evidence.
Expected outcome: Three per-PR outcomes, each with URL, frozen HEAD before and after, allowed prefix, trusted scan summary, maintainer approval reference, real merge commit SHA, main readback, rollback pointer, terminal verdict and first-fail; plus a 12/12 disposition of the acceptance report's findings, the compiler receipt, and the return pack handed to an external independent acceptance officer.
ChangeSet: EVIDENCE_ONLY
Affected domains: evidence, verification, local_asset_repair, handover

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R1 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric × Hermes × HG-KSEOS｜FAR-018／FAR-019 歸檔指揮薄 PROMPT.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric × Hermes × HG-KSEOS｜FAR-018／FAR-019 歸檔指揮薄 PROMPT.md role=NORMATIVE
- R2 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md role=NORMATIVE
- R3 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\驗收報告\Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\驗收報告\Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md role=NORMATIVE
- R4 C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md role=NORMATIVE
- R5 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\00_KNOW_INDEX.md C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\00_KNOW_INDEX.md role=NORMATIVE
- R6 C:\Projects\Agent_Workspace\_handover\CNV-FAR018-FAR019-ARCHIVE-20261016\A03_GITHUB_FREEZE.json C:\Projects\Agent_Workspace\_handover\CNV-FAR018-FAR019-ARCHIVE-20261016\A03_GITHUB_FREEZE.json role=NORMATIVE
- R7 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\驗收報告\Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\Fabric_HG-KSEOS_Convergence\驗收報告\Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md role=NORMATIVE
- R8 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills\software-development\hgk-governed-execution\SKILL.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\skills\software-development\hgk-governed-execution\SKILL.md role=NORMATIVE
- R9 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler\scripts\prompt_contract_compiler.py C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler\scripts\prompt_contract_compiler.py role=NORMATIVE
- R10 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler\references\prompt-contract.schema.json C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler\references\prompt-contract.schema.json role=NORMATIVE
- R11 C:\Projects\Agent_Workspace\HG-KSEOS\config\hermes.json C:\Projects\Agent_Workspace\HG-KSEOS\config\hermes.json role=NORMATIVE
- R12 C:\Projects\Agent_Workspace\Fabric\FABRIC\control\SOD_POLICY.yaml C:\Projects\Agent_Workspace\Fabric\FABRIC\control\SOD_POLICY.yaml role=NORMATIVE
- R13 C:\Projects\Agent_Workspace\Fabric\FABRIC\control\RELEASE_POLICY.yaml C:\Projects\Agent_Workspace\Fabric\FABRIC\control\RELEASE_POLICY.yaml role=NORMATIVE
- R14 C:\Projects\Agent_Workspace\Fabric\AGENTS.md C:\Projects\Agent_Workspace\Fabric\AGENTS.md role=NORMATIVE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: The user hands over the goal, the three PRs and the credential path once; the runtime recognises the exact subject and its claim ceiling, keeps every failure and non-verdict visible, asks for nothing it can determine itself, and reports a partial result as partial rather than rounding it up.
Constraints:
- change_class is EVIDENCE_ONLY; only the three existing evidence prefixes are written.
- Read the canonical control plane and the three PRs read-only; never rewrite frozen R6..R11 or any already-merged evidence.
- The credential file is read only by the isolated publisher process; its value never appears in stdout, a log, a commit or the publication package.
- A real secret or a path outside the single allowed prefix HOLDS that one PR only; the other two keep their independent gating.
- An unknown remote effect is resolved by reading the remote state back first; a blind retry is forbidden.
- No force-push and no rewrite of main, ever.
- Scripts stored inside the archive are evidence and are never executed.
- The claim ceiling of this round is CANDIDATE_EVIDENCE_ARCHIVED_ONLY.
Non-goals:
- No PIPD validator code promotion, no checker-isolation repair, no Fresh G1, no API/DB/desktop effect.
- No production release, no canonical AO acceptance, no DOC-05 effect admission, no full convergence.
- No re-opening of the already-merged #3..#11 and no signing of all 60 owner items.
- No second control plane, reducer, manifest architecture or workflow engine.
Authorized mutations:
- GitHub: turn PR #12 out of draft, merge #12, #13, #14 normally at their approved exact HEADs, and commit this round's archival evidence to its own new EVIDENCE prefix on a dedicated branch.
- Local: write this round's own receipts, registers and publication inputs under its round directory.
Forbidden mutations:
- Canonical product code, control-plane config, hooks, workflows, .env, credential stores, runtime DB.
- Any file outside the three allowed EVIDENCE prefixes and this round's own new prefix.
- Any force-push, rebase or history rewrite of main or of a frozen evidence branch.
Claim ceiling: LOCAL

## 4. Active / Deferred / Forbidden scope
Active:
- ARCHIVE_PREFIX_AND_CHANGE_CLASS_PREFLIGHT: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- TRUSTED_SECRETS_AND_MANIFEST_PREFLIGHT: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- PER_PR_FREEZE_AND_ROLLBACK_POINTER: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- MAINTAINER_APPROVAL_GATE: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- REMOTE_MERGE_AND_READBACK: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- K_LEDGER_METADATA_ERRATA: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- EIA_FINDING_DISPOSITION_MATRIX: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- EVIDENCE_RETURN_PACK_PUBLICATION: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
Non-active:
- none
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- #3..#11 (merged)
- R6..R11 frozen evidence
- 221 live tests
- the eight runtime gates
- the 60 owner items
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- ARCHIVE_PREFIX_AND_CHANGE_CLASS_PREFLIGHT: verdict=NOT_READY; work=Re-derive each PR's live HEAD, exact changed-file set and single evidence prefix, and re-derive change_class so any escape invalidates the evidence-only exception.
- TRUSTED_SECRETS_AND_MANIFEST_PREFLIGHT: verdict=NOT_READY; work=Trusted secrets/privacy scan over every changed blob plus deterministic manifest-vs-tracked-set checks performed OUTSIDE the PR, without executing archived helpers.
- PER_PR_FREEZE_AND_ROLLBACK_POINTER: verdict=NOT_READY; work=Freeze each PR separately on repo/base/head/prefix/diff with its own rollback pointer and approval record; never one atomic transaction.
- MAINTAINER_APPROVAL_GATE: verdict=NOT_READY; work=A real repository maintainer grants one prefix + actual HEAD + candidate-only/no-auto-execute + rollback approval per PR; never self-signed by maker or reviewer.
- REMOTE_MERGE_AND_READBACK: verdict=NOT_READY; work=Ordered merge by the authorised maintainer followed by main/merge-SHA/tree-prefix readback and a recomputed preflight.
- K_LEDGER_METADATA_ERRATA: verdict=NOT_READY; work=Add new-version crosswalk metadata separating source_linked 20/20 from same_run_retested 0/20 without rewriting the historical snapshot.
- EIA_FINDING_DISPOSITION_MATRIX: verdict=NOT_READY; work=Carry all ten EIA-20261016 findings with class, earliest legal owner, blocking point and minimum re-test.
- EVIDENCE_RETURN_PACK_PUBLICATION: verdict=NOT_READY; work=Publish the machine-readable return pack plus the single evidence MD through the credential broker and mirror it byte-identically.
Required user journeys:
- JNY-ARCHIVE-THREE-PRS: Hand the goal, the three candidate evidence pull requests and the credential path to a governed runtime and receive per-PR archival verdicts for exactly those three PRs. → Three rows, each with URL, frozen HEAD before and after, changed set, trusted scan summary, maintainer approval reference, real merge commit SHA, main readback, nonclaims, blocked first-fail and rollback pointer.
Acceptance predicates:
- ACC-ARCHIVE_PREFIX_AND_CHANGE_CLASS_PREFLIGHT subject=ARCHIVE_PREFIX_AND_CHANGE_CLASS_PREFLIGHT depth=L3_INTEGRATION_RUNTIME
- ACC-TRUSTED_SECRETS_AND_MANIFEST_PREFLIGHT subject=TRUSTED_SECRETS_AND_MANIFEST_PREFLIGHT depth=L3_INTEGRATION_RUNTIME
- ACC-PER_PR_FREEZE_AND_ROLLBACK_POINTER subject=PER_PR_FREEZE_AND_ROLLBACK_POINTER depth=L3_INTEGRATION_RUNTIME
- ACC-MAINTAINER_APPROVAL_GATE subject=MAINTAINER_APPROVAL_GATE depth=L3_INTEGRATION_RUNTIME
- ACC-REMOTE_MERGE_AND_READBACK subject=REMOTE_MERGE_AND_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-K_LEDGER_METADATA_ERRATA subject=K_LEDGER_METADATA_ERRATA depth=L3_INTEGRATION_RUNTIME
- ACC-EIA_FINDING_DISPOSITION_MATRIX subject=EIA_FINDING_DISPOSITION_MATRIX depth=L3_INTEGRATION_RUNTIME
- ACC-EVIDENCE_RETURN_PACK_PUBLICATION subject=EVIDENCE_RETURN_PACK_PUBLICATION depth=L3_INTEGRATION_RUNTIME
- ACC-JNY-ARCHIVE-THREE-PRS subject=JNY-ARCHIVE-THREE-PRS depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-001 subject=REQ-CNV-EA-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-002 subject=REQ-CNV-EA-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-003 subject=REQ-CNV-EA-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-004 subject=REQ-CNV-EA-004 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-005 subject=REQ-CNV-EA-005 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-CNV-EA-006 subject=REQ-CNV-EA-006 depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-PER-PR-PREFLIGHT-VERDICT subject=DEL-PER-PR-PREFLIGHT-VERDICT depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-CONVERGENCE-EVIDENCE-RETURN-PACK subject=DEL-CONVERGENCE-EVIDENCE-RETURN-PACK depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-SINGLE-EVIDENCE-MD subject=DEL-SINGLE-EVIDENCE-MD depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-EIA-FINDING-DISPOSITION-MATRIX subject=DEL-EIA-FINDING-DISPOSITION-MATRIX depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-FAR-RULING subject=DEL-FAR-RULING depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-RESIDUAL-UNIVERSE subject=DEL-RESIDUAL-UNIVERSE depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-DEFECT-DOSSIER subject=DEL-DEFECT-DOSSIER depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-HANDOVER-CHECKPOINT subject=DEL-HANDOVER-CHECKPOINT depth=L3_INTEGRATION_RUNTIME
- ACC-DEL-SINGLE-EVIDENCE-MD subject=DEL-SINGLE-EVIDENCE-MD depth=L3_INTEGRATION_RUNTIME
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: bounded maintainer merge approval (carried by this order), a real secret exposure, a scope escape.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: ARCHIVE_MERGED_READBACK_PASS, ARCHIVE_READY_HOLD, PARTIAL, TEMP_CLOSED, FAIL.
Nonterminal pauses: BLOCKED_HITL, PARTIAL_RESUMABLE, FAILED_STOP_ESCALATE.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above LOCAL.
