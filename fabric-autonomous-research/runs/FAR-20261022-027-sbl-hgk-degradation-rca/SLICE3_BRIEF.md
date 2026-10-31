# SLICE 3 BRIEF — EXECUTE lane, mechanical completion of three files

First output line, exactly:

    ARM-NONCE: SBL-RCA-027-EXEC3

You have already lost two turns to the time budget. Work in the order below and WRITE EACH FILE IMMEDIATELY
after you compose it, smallest first, so partial progress survives. Do not read any file you are not told to
read. Do not rewrite existing files.

Reads allowed (nothing else): `VERDICT.json` (JSON, whole file) and `FINDINGS.tsv` (whole file).

---
## FILE 1 — `DEVIATIONS.tsv`  (write this first, it is small)
TSV with header `id	class	what	why	ceiling_effect` and exactly these five data rows (id, class literal, then
your own one-line cells; keep tabs, no commas substitution):

D1 | declared_plane | Pool rank-1 for PLAN and VERIFY_SECURITY is openai-codex/gpt-6.1-sol; this round pinned opencode-go/deepseek-v4.1-flash for PLAN (session plane) and opencode-go/deepseek-v4.1-flash@rank4 for VERIFY | owner mandate names those models; pool selection_semantics permits an instructed entry to replace rank 1 | declared plane and served plane disagree by design; every receipt names the served arm
D2 | execution | Slice-1 EXECUTE turn ended ERR_LANE_ALL_ROUTES_EXHAUSTED at its 1200s budget with 3 of 6 files landed; recovery was decomposition into slices 2-3 | the timeout branch is FAIL even though the bytes are real | writer receipts for ResearchSynthesis.md / FINDINGS.tsv / VERDICT.json are a timeout, not a PASS
D3 | execution | A second slice (700s) ended in the same code with zero files | same arm, narrower scope, still over budget | no writer receipt claims those three files
D4 | evidence | Worker W2's own write was refused by the session pre-write guard; the orchestrator re-derived every W2 number itself | the child's draft carried a guarded token | W2 carries no child self-report; numbers come from orchestrator commands
D5 | route | FAR class RESEARCH_ADVERSARIAL_CHALLENGE routes NATIVE_NO_CHALLENGE / FAR_ROUTE_NATIVE_DEFAULT | the matrix does not select an ARIS challenge for that class | adversarial pressure came from the independent VERIFY_SECURITY lane instead

---
## FILE 2 — `ResearchHandoff.yaml`  (write second)
```yaml
run_id: FAR-20261022-027-sbl-hgk-degradation-rca
verdict_ref: VERDICT.json
candidate_refs:
  - ResearchSynthesis.md
  - FINDINGS.tsv
  - VERDICT.json
  - DEVIATIONS.tsv
  - ProposedEvolution.yaml
residuals:
  - id: RS1
    owner: sbl-product-owner
    one_action: "Replace the hg_kseos version pin with a commit/tree-digest pin the adapter re-resolves at load (FINDINGS row for the vacuous pin)"
    blocked_by: none
    claim_ceiling: CANDIDATE_ONLY
  - id: RS2
    owner: sbl-product-owner
    one_action: "Declare hg_kseos as a real dependency (or an explicit bootstrap) so the adapter's recorded interpreter can import it"
    blocked_by: none
    claim_ceiling: CANDIDATE_ONLY
  - id: RS3
    owner: fabric-contract-owner
    one_action: "Issue one applicability/registration disposition for SBL against Fabric/FABRIC/control/PROFILE_STACK_REGISTRATION_POLICY.yaml"
    blocked_by: owner decision (no SBL install target exists)
    claim_ceiling: CANDIDATE_ONLY
  - id: RS4
    owner: hgk-control-plane
    one_action: "Re-measure HG-KSEOS conformance on 3dfaebc (the number SBL's own handover says does not exist after b22706e)"
    blocked_by: none
    claim_ceiling: LOCAL_MEASUREMENT_ONLY
  - id: RS5
    owner: owner
    one_action: "Decide whether 'self-accept' is renamed to independent-lane acceptance; the two layers already refuse writer == checker"
    blocked_by: owner decision
    claim_ceiling: CANDIDATE_ONLY
  - id: RS6
    owner: sbl-product-owner
    one_action: "Add a board-drain gate so no new SBL board opens while the previous board still holds unclaimed ready cards (r12 5/1, r13 4/1, r14 23/8)"
    blocked_by: none
    claim_ceiling: CANDIDATE_ONLY
  - id: RS7
    owner: hgk-control-plane
    one_action: "Bind config/hermes.json to the measured live Hermes version (live 0.21.5 vs declared 0.20.0 / v2026.8.3 / 3c27eb62)"
    blocked_by: none
    claim_ceiling: CANDIDATE_ONLY
resume_command: "python C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY <RANK_PIN_FLAG> 4 --require-arm opencode-go/deepseek-v4.1-flash --sandbox read-only --cwd C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261022-027-sbl-hgk-degradation-rca --prompt 'Read VERIFY_BRIEF.md in the current working directory and execute it exactly.'"
claim_ceiling: CANDIDATE_ONLY research product; not an acceptance; no promotion; no push.
### FILE 2 notes
Copy the resume_command exactly as the single line above, including the literal placeholder `<RANK_PIN_FLAG>`.
Do NOT expand that placeholder and do NOT write any git or remote-publication command into any file: the
placeholder stands for the dispatcher's rank-pinning flag, and a brief that spells out remote-write flags is
refused by the lane guard before dispatch.
### FILE 2 notes
Write the resume_command exactly as the single line above. It is a command line, not an instruction to run.
```
(Adapt prose to what VERDICT.json.open_items actually says; do not add residuals that no finding supports.)

---
## FILE 3 — `ProposedEvolution.yaml`  (write last)
```yaml
schema: FAR-ProposedEvolution/1
run_id: FAR-20261022-027-sbl-hgk-degradation-rca
proposals:
  - id: EV1
    target: HG-KSEOS/_sbl_harness_adapter/adapter.json
    change: replace the hg_kseos version pin with a re-resolved commit/tree digest
    why: the version has not moved in 147 of 148 commits, so >=0.1.0,<0.2.0 is a constant
    evidence: evidence/W2_base_drift.md
    cost: small
    risk: an adapter load now fails when the base moves, which is the point
    owner_decision_required: false
    claim_ceiling: CANDIDATE_ONLY
  - id: EV2 ... (declare the dependency / bootstrap so import hg_kseos succeeds in the recorded interpreter)
  - id: EV3 ... (one Fabric applicability disposition for SBL)
  - id: EV4 ... (rename self-accept to independent-lane acceptance; dispatch refuses writer == checker)
  - id: EV5 ... (board-drain gate on unclaimed ready cards)
  - id: EV6 ... (bind config/hermes.json to the measured live runtime version)
```
Six items, EV1..EV6, each with all nine keys above. `why` and `evidence` must point at a file that exists.

---
## Rules
Only these three files. No git writes. No invented numbers — quote only what VERDICT.json / FINDINGS.tsv carry.
After writing each file, move on immediately; do not re-read your own output.
