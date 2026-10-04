# Finding Contract

Use one record per finding.

```yaml
finding:
  finding_id: FCR-000
  title: ""
  classification: CONFIRMED_DEFECT|EVIDENCE_GAP|ORACLE_DISAGREEMENT|NON_BLOCKING_OBSERVATION|OUT_OF_SCOPE
  severity: CRITICAL|HIGH|MEDIUM|LOW|INFO
  gate_ids: []
  acceptance_ids: []
  subject_identity: ""
  source_locators: []
  evidence_ids: []
  observed: ""
  expected: ""
  contradiction: ""
  reproducibility: REPRODUCED|EVIDENCE_ONLY|NOT_REPRODUCIBLE|NOT_APPLICABLE
  claim_impact: ""
  earliest_owner: ""
  smallest_repair_scope: ""
  retest_required: []
  regression_required: []
  oracle_disposition: AGREE|DISAGREE|NOT_APPLICABLE
  status: OPEN|RESOLVED|QUARANTINED
```

## Quality bar

A blocking finding must name the violated predicate and connect it to raw evidence or a missing required evidence edge. Avoid style-only findings in final acceptance unless the frozen acceptance contract makes them material.
