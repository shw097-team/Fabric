# RP-002 Design Contract (ADR/SDD) — Fabric-Governed Profile-Distributed Kanban-Coordinated Upgrade

artifact_id: RP002_D1_DESIGN_CONTRACT
generated_at_utc: 2026-08-11T16:07:14.706117+00:00
supersedes: r2 design lineage (r3 is current substantive blueprint; r2 discussions are design lineage only)
oracle: EXTERNAL_FROZEN_BOOTSTRAP_ORACLE
base_head: 22e21f0340501caf4ff0dbd67663faf49f521b03

## ADR-001 — Architecture decision: only HGK + SQS are heavy stacks
Decision: keep HG-KSEOS and SQS-THC as the only durable engineering/financial stacks.
Hermes runtime = execution plane (Profiles/Distribution/Kanban/A2A); Fabric = governance
contracts + bindings, never an actor/daemon. Second orchestrator/reducer/task-DB/
knowledge-platform is prohibited (r3 §1.2, §6.1; N-RP2-05/06).

## ADR-002 — Bootstrap inversion
G0~C1 execute with CURRENT_CERTIFIED_HGK_RUNTIME + EXTERNAL_FROZEN_BOOTSTRAP_ORACLE.
New Profile Team is not assumed before H1; internal Oracle candidate is null until O1
(r3 §15.1; FROZEN_ACCEPTANCE_ORACLE.yaml). G0 freeze binds prompt r1 + blueprint r3 +
current controls digests (RP002_G0_FREEZE.json).

## ADR-003 — WorkOrder is the executor contract
HGK WorkOrder remains normative; Kanban is runtime pointer/status only. ExecutionBinding
ABI (RP002_EXECUTION_BINDING.schema.json) binds workorder->kanban task->profile without
creating a second task truth (r3 §6.8, §14.2).

## SDD-001 — Factory second-acceptance contract chain
For each canonical gate requirement REQ-RP2-{GATE}:
  Requirement (FROZEN in Shared Spine) -> ADR/SDD (this doc) -> TaskSpec (TS-RP2-*)
  -> WorkOrder (WO-RP2-*) -> Acceptance (RP2-T0xx suite) -> Evidence (EVD1-*)
  -> Rollback (RB-* pointer). required_requirement_orphan = 0.

## SDD-002 — Profile Team runtime materialization
8 profile instances per RP002-PROFILE-TEAM-MANIFEST.yaml; each instance = distribution.yaml
+ SOUL.md + config.yaml + skills/ + toolset/model/provider/MCP readback; Profile != sandbox
(r3 §10.2-10.3). HGK/TEAM.md, SQS/TEAM.md, RP002/TEAM.md materialize the team graphs.

## SDD-003 — Inherited capability preservation
Codex/OpenCodex/OpenCode provider route, OpenSpec brownfield, gstack selected advisory
slices, Spec Kit XOR, GE, independent checker/reducers: preserve-or-requalify; silent
fallback/fake invocation prohibited (RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml).

## SDD-004 — Oracle internalization
construction-acceptance-oracle Profile: Oracle Core + KP00~19 + prompt compiler + validators
+ Acceptance Packs + OracleReceipt schema; CHECKER = fresh read-only context, no candidate
write tools (r3 §9). Meta-Oracle stays external for O1 qualification and E3.

## SDD-005 — SQS selective profileization + real canary
SQS Stack Manifest keeps Financial Truth owner in SQS controls; 3 profiles (orchestrator,
data-analysis, risk); S1 runs a real LOCAL/PAPER/NO-LIVE-WRITE task; live_trading
NOT_AUTHORIZED (r3 §10.5, §SQP1/S1).

## SDD-006 — Cross-stack + behavioral evolution
E1: real/fault-labeled SQS defect -> reproduce -> classify -> smallest HGK repair -> old+new
regression -> independent/domain check -> atomic promotion -> same task replay.
E2: SOUL/Skill/Profile/Pipeline durable behavior defect -> versioned patch -> fresh session
effective-load -> positive+negative+regression -> promotion -> replay -> rollback drill.

## SDD-007 — Evidence truth
Single canonical Evidence Manifest; MD is renderer, not truth owner. SubjectAttestation
binds repo heads + distribution commits + stack manifests + oracle digest + manifest digest
(r3 §6.6, §7.3).
