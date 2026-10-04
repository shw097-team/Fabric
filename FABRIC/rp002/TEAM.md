# RP002 TEAM — Project Composition

team_id: RP002_FABRIC_BOOTSTRAP
project_id: HGK-REFERENCE-PROJECT-002
execution_graph: rp002/RP002_EXECUTION_GRAPH.yaml
gate_catalog: rp002/RP002_GATE_CATALOG.yaml

## Members
- bootstrap_executor: CURRENT_CERTIFIED_HGK_RUNTIME (G0~C1)
- post_h1_profiles: [hgk-orchestrator, hgk-knowledge-factory, hgk-document-factory, hgk-coding-factory, construction-acceptance-oracle]
- post_sqp1_profiles: [sqs-orchestrator, sqs-data-analysis, sqs-risk]

## Constraints
- self_hosting_required_after: F1
- live_broker_write: false
- fabric_authority_matrix_is_external_to_team_md: true
- G0~C1 executed by current certified HGK runtime; profile team not assumed before H1
- internal Oracle candidate null until O1 (external frozen bootstrap oracle before)
