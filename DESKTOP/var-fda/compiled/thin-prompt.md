# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: FDA-IMPLEMENTATION-2026-08-13-001
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Implement fabric-desktop-automation blueprint v2026.08.13-r2: materialize the FDA shared-infrastructure team artifact, capability matrix, fabric-desktop-cua and fabric-desktop-ufo2 profiles, deterministic router + one-writer lease + idempotency, XQ PAPER fixture qualification, security/SoD negative suite, interop dispositions, and freeze one evidence MD for external acceptance.
Expected outcome: One evidence MD the external verifier can audit; every hard claim carries SHA-256 + raw receipts; FDA_PROFILE_TEAM_ACTIVE declared only if all runtime predicates pass, otherwise FAIL_CLOSED with exact blockers.
ChangeSet: NEW_IMPLEMENTATION
Affected domains: FABRIC_GOVERNANCE, WINDOWS_DESKTOP_AUTOMATION, XQ_PAPER_CONSUMER

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R1 C:\Users\user\AppData\Local\hermes\attachments\fabric-desktop-automation_藍圖_v2026.08.13-r2.md C:\Users\user\AppData\Local\hermes\attachments\fabric-desktop-automation_藍圖_v2026.08.13-r2.md role=NORMATIVE
- R1 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\fabric-desktop-automation\fabric-desktop-automation_藍圖_v2026.08.13-r2.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\fabric-desktop-automation\fabric-desktop-automation_藍圖_v2026.08.13-r2.md role=NORMATIVE
- R2 C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md role=NORMATIVE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: User supplies only the blueprint + design intent; HGK governs admission; Hermes orchestrates; Codex is tracked writer; external verifier receives the evidence MD.
Constraints:
- no third heavy stack; heavy stacks stay HGK+SQS
- no second scheduler/task DB/reducer/knowledge platform
- no schema fork; parent-compatible extension only
- one active desktop writer per session; unknown-state failover forbidden
- SQS live trading NOT_AUTHORIZED; FDA v1 = LOCAL/PAPER/NO-LIVE-WRITE
- no credential/MFA automation; HumanGate only
- no self-accept / self-promote; independent Acceptance Officer
- parent tool matrix rows preserved additively; missing row = FAIL
Non-goals:
- NOT installing OpenAdapt / AgentS3 / Appium / third GUI framework
- NOT creating a desktop scheduler/task DB
- NOT authorizing live trading or semi-auto entry
- NOT reopening RP-002 Stage-1/2/3
- NOT creating remote CI/SLSA platform
- NOT replacing SQS Financial Truth owner
Authorized mutations:
- Fabric/rp002 profile team manifest additive extension
- Fabric/rp002 tool matrix additive extension
- Fabric/fabric-desktop-automation/* new artifacts
- Fabric/profiles/fabric-desktop-cua + fabric-desktop-ufo2
- Fabric/control MIN_PATCH only where policy gap proven
Forbidden mutations:
- HGK/SQS/FABRIC_ASSURANCE profile rows removal
- RP002 gate catalog new gates
- child schema fork
- live trading / broker write authorization
Claim ceiling: LOCAL

## 4. Active / Deferred / Forbidden scope
Active:
- FDA-C0_AUTHORITY_READBACK: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FDA-C1_TEAM_PROFILE_MATERIALIZATION: ACTIVE_REQUIRED; action=INSTALL; runtime_required=true
- FDA-CAPABILITY_MATRIX: ACTIVE_REQUIRED; action=INSTALL; runtime_required=true
- FDA-C2_CUA_QUALIFICATION: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FDA-C3_UFO2_QUALIFICATION: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FDA-C4_XQ_PAPER_FIXTURES: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FDA-C5_ROUTER_LEASE_IDEMPOTENCY: ACTIVE_REQUIRED; action=INSTALL; runtime_required=true
- FDA-C6_KNOWLEDGE_SECURITY_SOD: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FDA-C7_INDEPENDENT_ACCEPTANCE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
Non-active:
- none
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- RP-002 Stage-1/2/3 seals
- RP002_GATE_CATALOG.yaml
- SQS live trading authority
- existing profile distributions
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- FDA-C0_AUTHORITY_READBACK: verdict=RUNTIME_READY; work=fresh readback bound
- FDA-C1_TEAM_PROFILE_MATERIALIZATION: verdict=RUNTIME_READY; work=team artifact + 2 profiles + matrix materialized
- FDA-CAPABILITY_MATRIX: verdict=RUNTIME_READY; work=canonical matrix owner/schema/version/rollback
- FDA-C2_CUA_QUALIFICATION: verdict=NOT_READY; work=hermes computer-use status/install; exact pin; fixtures
- FDA-C3_UFO2_QUALIFICATION: verdict=NOT_READY; work=exact pin; security disposition; fixtures
- FDA-C4_XQ_PAPER_FIXTURES: verdict=NOT_READY; work=XQ version readback; 12-fixture matrix
- FDA-C5_ROUTER_LEASE_IDEMPOTENCY: verdict=RUNTIME_READY; work=router impl + lease + idempotency unit tests
- FDA-C6_KNOWLEDGE_SECURITY_SOD: verdict=RUNTIME_READY; work=ACL + negative suites
- FDA-C7_INDEPENDENT_ACCEPTANCE: verdict=RUNTIME_READY; work=swarm lanes + AO verify
Required user journeys:
- UJ-FDA-IMPLEMENTATION: Implement fabric-desktop-automation blueprint r2 end-to-end under HGK governance with Kanban/Swarm/gstack/OpenSpec/Codex surfaces and freeze one evidence MD for external acceptance → FDA team artifact + capability matrix + 2 provider profiles + router/lease/idempotency + XQ PAPER fixture qualification + single evidence MD with SHA-256
Acceptance predicates:
- ACC-FDA-C0 subject=FDA-C0_AUTHORITY_READBACK depth=L2_UNIT_BEHAVIOR
- ACC-FDA-C1 subject=FDA-C1_TEAM_PROFILE_MATERIALIZATION depth=L2_UNIT_BEHAVIOR
- ACC-FDA-MATRIX subject=FDA-CAPABILITY_MATRIX depth=L2_UNIT_BEHAVIOR
- ACC-FDA-C2 subject=FDA-C2_CUA_QUALIFICATION depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-C3 subject=FDA-C3_UFO2_QUALIFICATION depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-C4 subject=FDA-C4_XQ_PAPER_FIXTURES depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-C5 subject=FDA-C5_ROUTER_LEASE_IDEMPOTENCY depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-C6 subject=FDA-C6_KNOWLEDGE_SECURITY_SOD depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-C7 subject=FDA-C7_INDEPENDENT_ACCEPTANCE depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-UJ subject=UJ-FDA-IMPLEMENTATION depth=L3_INTEGRATION_RUNTIME
- ACC-FDA-REQ subject=REQ-FDA-001 depth=L2_UNIT_BEHAVIOR
- ACC-FDA-DELIV subject=FDA-EVIDENCE-MD depth=L2_UNIT_BEHAVIOR
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: XQ login/MFA, provider install authorization, ambiguous desktop state, human gate for future semi-auto.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: PASS.
Nonterminal pauses: PARTIAL_RESUMABLE, BLOCKED_HITL, BLOCKED_EXTERNAL, TEMP_CLOSED, FAIL, FAILED_STOP_ESCALATE.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above LOCAL.
