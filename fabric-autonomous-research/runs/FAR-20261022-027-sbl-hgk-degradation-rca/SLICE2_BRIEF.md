# SLICE 2 BRIEF — EXECUTE lane, decomposed continuation

First line of your output, exactly:

    ARM-NONCE: SBL-RCA-027-EXEC2

Slice 1 of this WorkOrder wrote `ResearchSynthesis.md`, `FINDINGS.tsv` and `VERDICT.json` and then hit the
lane's time budget. Do NOT rewrite or re-read those three in full. Your whole job is the three files slice 1
never reached. Bounded reads only:
- `VERDICT.json` — read it as JSON and use `claim_ceiling`, `answers`, `capability_states`,
  `mandate.declared_vs_pinned_deviation`, `open_items`.
- `FINDINGS.tsv` — read the id/class columns only (all 34 rows).
- `evidence/W2_base_drift.md` — the first 40 lines only (the numbers you may quote).

Do not read `evidence/W1`, `W3` or `W4`. Do not modify anything that already exists. Write exactly three
files, nothing else, no temp files:

### 1. `DEVIATIONS.tsv`
Header exactly: `id\tclass\twhat\twhy\tceiling_effect`
Rows (ids D1..Dn) — at minimum these five, each with a real locator:
- **D1** the pool's DECLARED rank-1 arms for PLAN and VERIFY_SECURITY are `openai-codex/gpt-6.1-sol`, while
  this round pinned the owner's arms (`PLAN` = Hermes session `opencode-go/deepseek-v4.1-flash`, `VERIFY` =
  `opencode-go/deepseek-v4.1-flash@rank4`) under the pool's own `selection_semantics`
  (`HG-KSEOS/config/lane-route-slots.candidate.json`). Why: owner mandate names those models. Effect: the
  declared plane and the served plane disagree by design; no receipt claims otherwise.
- **D2** slice-1 EXECUTE turn ended `ERR_LANE_ALL_ROUTES_EXHAUSTED` after its 1200 s budget with 3 of 6 files
  landed; recovery was DECOMPOSITION (this slice), not a loosened oracle. Effect: the lane receipt is a
  timeout, the bytes are real, and this round states both.
- **D3** worker W2's own write was refused by this session's pre-write guard (guarded token in its draft); the
  orchestrator re-derived every W2 number itself, so W2 carries no child self-report
  (`evidence/W2_base_drift.md`, header).
- **D4** the FAR adversarial-challenge class routes to `NATIVE_NO_CHALLENGE` / `FAR_ROUTE_NATIVE_DEFAULT`
  (`ROUTE_DECISION.json`), so no ARIS challenge method was selected; the adversarial half was carried by the
  independent VERIFY_SECURITY lane instead.
- **D5** SWARM was executed as four `delegate_task` workers in this harness, not through `kanban swarm`
  creation (creation mutates board state); graph capability itself was measured, not exercised.

### 2. `ProposedEvolution.yaml`
Schema-less candidate evolution list. Top-level key `proposals:` — each item:
`id, target, change, why, evidence, cost, risk, owner_decision_required, claim_ceiling: CANDIDATE_ONLY`.
Exactly six proposals, one per named defect:
- EV1 the vacuous version pin (`hg_kseos >=0.1.0,<0.2.0` while the version has not moved in 147 of 148
  commits) → replace with a commit/`tree`-digest pin the adapter re-resolves at load;
- EV2 the adapter's recorded `host.executable` cannot `import hg_kseos` and SBL declares `dependencies = []`
  → declare a real install-time dependency or an explicit `PYTHONPATH` bootstrap the adapter verifies;
- EV3 no Fabric registration/applicability seam for SBL (`NO_SBL_INSTALL_TARGET`) → one applicability
  disposition record against `Fabric/FABRIC/control/PROFILE_STACK_REGISTRATION_POLICY.yaml` fields;
- EV4 self-ACCEPT vs `ERR_WORKORDER_SELF_REVIEW` / `SBL_E_SELF_CHECK_FORBIDDEN` → rename the capability to
  self-detect + self-repair + INDEPENDENT-verify and make the acceptance lane structurally separate;
- EV5 SBL board backlog never drains (sbl-r12 5 ready/1 done, sbl-r13 4 ready/1 done, sbl-r14 23 ready/8 done)
  → a drain gate: a round may not open a new board while the previous board holds unclaimed ready cards;
- EV6 the control plane's own runtime binding is stale (`config/hermes.json` declares Hermes 0.20.0 /
  `v2026.8.3` / `3c27eb62`, live install is 0.21.5) → bind the live runtime by measured version, not a
  recorded string, and make a consumer refuse on mismatch.
Each `why` must cite a locator; no new measurement is required beyond what those files already carry.

### 3. `ResearchHandoff.yaml`
Keys: `run_id, verdict_ref, candidate_refs[], residuals[], resume_command, claim_ceiling`.
`residuals[]` items: `id, owner, one_action, blocked_by, claim_ceiling`. Take them from
`VERDICT.json.open_items` and make each OWNER-READY: one concrete action, no open question. `owner` is one of
`owner`, `hgk-control-plane`, `fabric-contract-owner`, `sbl-product-owner`. `blocked_by` names a real gate
(owner decision, a missing measurement, or nothing).

## Rules
No git writes. No files outside the three. No invented numbers: if you need a figure, it must already exist in
`VERDICT.json` or `FINDINGS.tsv`. Candidate-only, not an acceptance — say so inside each file where a ceiling
field exists.
