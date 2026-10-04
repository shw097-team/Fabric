# Adjudication and Resume Contract

## When Internal Oracle and External Challenger agree

- If both support the gate and no blocking evidence gap remains: recommend `CONTINUE` or final Meta-Oracle disposition.
- If both identify a defect: route the smallest affected repair.

## When they disagree

Create a disagreement record:

```yaml
disagreement:
  disagreement_id: DCR-000
  gate_ids: []
  internal_oracle_verdict: ""
  external_challenge_verdict: ""
  disputed_predicates: []
  deterministic_evidence: []
  unresolved_authority: []
  suspected_cause: STALE_SUBJECT|EVIDENCE_GAP|INTERPRETATION|ORACLE_DEFECT|CHALLENGER_DEFECT|PRODUCT_DEFECT
  next_route: RECHECK_EVIDENCE|META_ORACLE|DOMAIN_OWNER|HITL|RESUME_SMALLEST_REPAIR
```

Prefer deterministic resolution before model-vs-model debate.

## Smallest repair handoff

A repair recommendation must include:

- failed predicate/finding IDs;
- earliest owning component;
- exact allowed change scope;
- forbidden unaffected scope;
- focused reproduction;
- focused test;
- affected regression set;
- fresh independent recheck;
- rollback/checkpoint reference.

Do not reopen sealed unrelated gates without a dependency invalidation reason.
