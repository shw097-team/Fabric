# HGK TEAM — RP-002 Profile Team Topology

stack_id: HGK_ENGINEERING
stack_manifest: HGK_STACK_MANIFEST.yaml
oracle_profile: construction-acceptance-oracle (internalized at O1; external frozen oracle before)
coordination: Hermes Kanban (board RP002-FABRIC-BOOTSTRAP, project-scoped)

## Roles
| Profile | Primary role | Handoff out | Handoff in |
|---|---|---|---|
| hgk-orchestrator | lifecycle/orchestration; WorkOrder admission; policy consumption | bounded order -> factories | gate evidence, policy events |
| hgk-knowledge-factory | source-bound distillation | K1-sealed current contract -> document factory | admitted corpora + source inventory |
| hgk-document-factory | ADR/SDD/TaskSpec/WO/acceptance chain | sealed engineering contract -> coding factory | K1-sealed contract |
| hgk-coding-factory | bounded implementation (Codex writer) | code + tests + maker evidence -> oracle checker | admitted TaskSpec |

## Handoff rules
1. WorkOrder is the executor contract; Kanban keeps runtime pointer/status only.
2. A downstream factory consumes only the SEALED output of the upstream factory.
3. Maker != checker: coding factory output is verified by the oracle CHECKER in a fresh read-only context.
4. Any divergence between WorkOrder and Kanban state -> BLOCK + reconcile from WorkOrder.

## Boundaries
- HGK/TEAM.md is not an Authority Matrix; powers come from Fabric/HGK/SQS controls.
- Profile != security sandbox (least privilege + separate credentials where required).
- No live broker write; production autonomy NOT_CLAIMED.
