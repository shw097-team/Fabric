# R9-0 self-research / self-learning / self-iteration / self-evolution

Governed by HG-KSEOS AGENTS.md and the PKG v2.0.0 anchor. Claim ceiling **LOCAL / candidate-only**: this is not an acceptance, a Gate PASS or a release.

## Research (measured this round)
- **RS-01** The R8-0 hardening failed on main for a caller-shape reason, not a contract contradiction: validate_bundle() fails closed when the caller supplies no frozen context although the bundle carries the atoms, and derive_frozen_context() assumed a mapping where the newer fixture supplies a string.
  - evidence: 2 passed / 629 deselected after the 2-hunk adaptation (orchestrator re-run, 20.26s; lane run 18.49s) against 2 failed pre-edit; M04/M06/M16 all observed=REJECT
  - ceiling: local
- **RS-02** The R8 VERIFY/SECURITY verdict was served by that lane's rank-2 fallback (opencode-go/glm-5.3-flash); the mandated rank-1 arm was absent from the lane's live identity gate, not merely unpinned.
  - evidence: dispatch receipt attempts[0] rank=2 provider=opencode-go model=glm-5.3-flash + identity_gate.arms[] listing only rank 2
  - ceiling: receipt-bound
- **RS-03** A drift-clean registry is not a mandate-conformant one: check_drift compares routes against their own projections, so both can agree on a value the owner's pool and mandate disagree with.
  - evidence: check_drift(registry=load_registry()) -> [] while routes[].PLAN=opencode-go/glm-5.3-flash and the pool rank 1 = openai-codex/gpt-6.1-sol
  - ceiling: local
- **RS-04** The stack had already registered the PLAN row conflict as F1-PLAN-ROUTE-ROW-OUTLIER and left it unrepaired for lack of authorisation; and the same rebind is already proposed in openspec change hgk-far-remediation-20261016 (R1).
  - evidence: quoted registry finding text + the proposal's ChangeSet R1 wording
  - ceiling: local
- **RS-05** No governing document states a skill main-file size cap; the real limit is the platform constant MAX_SKILL_CONTENT_CHARS (100000) enforced on the LF-normalized len(), and the byte and raw-CRLF measures both misjudge it.
  - evidence: 0 PKG occurrences of 100000; tools/skill_manager_tool.py:111/:192/:488; the stack's SKILLCAP-20261007 research naming 996, 105116 and 101219 as the three confusable figures
  - ceiling: local
- **RS-06** The PKG's 10/6 partition is by piece/marker, not by slice count: ACC-RQ06 names AVR/10-piece and HGK/6-piece reconstruction; the HGK entry map carries exactly 6 slices whose 6 dest ranges verify, and the AVR candidate carries 10 SKCV-SLICE markers.
  - evidence: ACC-RQ06.child_obligations verbatim + measured slice/marker counts
  - ceiling: local
- **RS-07** The blocked slim candidate was blocked by exactly two lost live reference texts; restoring them makes all six harness checks pass with 112 references accounted and none lost.
  - evidence: C6 FAIL->PASS; 89 byte-identical + 23 fully embedded; main file 21026 bytes
  - ceiling: scratch experiment

## Learning (rules to carry forward)
- **LN-01** Arm attribution survives a nonce failure: read attempts[] (rank/provider/model/exit/seconds/nonce_present) before writing any 'the served arm is unprovable' finding — the nonce gates completion attestation, not attribution.
  - applies to: hgk-kanban-and-lane-routing / lane-model-attribution
- **LN-02** A verification turn must have its ARM RANK BOUND at dispatch (--force-rank with --max-candidates 1), then assert required_arm == served_arm in the receipt; otherwise a declared fallback can serve the check silently while every label still names the mandated model.
  - applies to: hgk-kanban-and-lane-routing / lane dispatch surfaces
- **LN-03** check_drift == [] proves projection agreement only; conformance also requires reading the file's own declared_conflicts/notes and the owner's pool. Quote which of the three surfaces disagrees rather than reporting 'drift'.
  - applies to: hgk-kanban-and-lane-routing / registry editing
- **LN-04** Search the openspec changes directory before preparing an owner action: the identical rebind was already proposed, so the deliverable was a citation plus a new measurement, not a second proposal.
  - applies to: openspec-explore / governance rounds
- **LN-05** A round that withdraws or recalibrates its own earlier claims must carry those corrections in the same change, or its ledger only ever grows.
  - applies to: adversarial-verification-rounds / round records
- **LN-06** Measure a skill's size with the GOVERNED measure (LF-normalized len) and report bytes alongside it; a byte threshold is not the platform's threshold.
  - applies to: hermes-agent-skill-authoring / skill pipelines

## Iteration (what this round would do differently)
- **IT-01** Bind the checker lane's rank explicitly and assert required==served on both WRITER and CHECKER turns (this round's WRITER receipt satisfied rank 1; the R8 CHECKER did not and was not caught).  _(trigger: RS-02)_
- **IT-02** Run the 2x2 baseline matrix (clean base vs changed tree on the SAME two named tests) before attributing any failure to a change; re-validated this round.  _(trigger: RS-01)_
- **IT-03** Serialize long lanes: one sealed lane at a time, because the second dispatch shares the relay and the budget; queue the next brief instead of fanning two writers out.  _(trigger: observed contention risk)_
- **IT-04** Reuse the proven guarded-apply mechanism (pre-image + receipt + rollback drill + post-apply re-measure) for every canonical apply instead of authoring a new one.  _(trigger: RS-07)_
- **IT-05** For a claimed defect, name the exact fix surface (file + anchor) and the negative control that must still fail-closed; a repair without a negative control cannot be distinguished from a relaxation.  _(trigger: RS-01)_

## Evolution proposals (each with an owner, a gate and a falsification condition)
- **EV-01** Populate used_rank / served_arm in a dispatch receipt even when the nonce gate fails, or document attempts[] as the attribution contract.
  - owner: control-plane owner (dispatcher)
  - gate: a receipt from a nonce-absent turn still names the served arm
  - falsification: a post-change receipt with a nonce failure and a null served arm
- **EV-02** Rebind routes[].PLAN to openai-codex/gpt-6.1-sol to match today's mandate (already proposed as hgk-far-remediation-20261016 R1).
  - owner: HGK Lifecycle Owner + DOC05 admission
  - gate: check_drift [] + the repo conformance test green + every affected projection moved
  - falsification: any PLAN projection still expecting glm-5.3-flash
- **EV-03** Make the lifecycle plan() spec-id derivation collision-proof so two projects sharing a final dash segment can both admit.
  - owner: HGK Lifecycle Owner
  - gate: both projects admit; the second no longer strands in PLAN_READY
  - falsification: an IntegrityError on the second admission (spine.py:277)
- **EV-04** Adopt restore-before-slim plus C6 reference-coverage as the standing shape for a slim candidate, so a lost reference text is a blocking check rather than a post-hoc discovery.
  - owner: Skill Owner
  - gate: C1–C6 PASS with 0 references lost
  - falsification: a shipped candidate whose reference bytes are absent
- **EV-05** Give checker lanes a governed write root outside every guarded subject, with a typed refusal when an out-dir resolves inside one.
  - owner: owner (identity/write-root decision)
  - gate: the refusal fires on an in-subject out-dir
  - falsification: a checker artifact landing inside a guarded subject
- **EV-06** Make a claim-correction ledger a first-class round artifact alongside the findings ledger.
  - owner: round owner
  - gate: every withdrawn claim has a replacement evidence row in the same change
  - falsification: a published claim withdrawn with no replacement
- **EV-07** Report skill file sizes with the governed LF-normalized character count first and bytes second in every receipt.
  - owner: Skill Owner
  - gate: both figures present in the receipt
  - falsification: a receipt reporting bytes only

## Not claimed
- no acceptance, no Gate PASS, no AO verdict, no release
- no independence established between PLAN and VERIFY while both may run on the same model family
- no claim that the two repaired artifacts are canonical
- no claim that the owner gates listed above are satisfied
