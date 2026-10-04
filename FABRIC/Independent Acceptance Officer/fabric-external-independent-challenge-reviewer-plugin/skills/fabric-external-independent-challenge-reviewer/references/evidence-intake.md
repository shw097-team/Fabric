# Evidence Intake Contract

## Classification

Classify every input as one of:

- `NORMATIVE`: frozen authority or acceptance rule.
- `STATE`: exact current candidate/runtime identity.
- `RAW_EVIDENCE`: diff, test log, command output, trace, receipt, checksum, readback.
- `SUMMARY_CLAIM`: maker/Oracle prose summary; never sufficient alone for a runtime PASS.
- `SUPPORT`: explanatory material without authority.
- `UNVERIFIED`: cannot be authenticated/read back.

## Minimum review identity

Record, when applicable:

```yaml
review_subject:
  project_id: ""
  task_id: ""
  gate_ids: []
  candidate_commit: ""
  candidate_package_sha256: ""
  profile_distribution_digest: ""
  evidence_manifest_sha256: ""
  oracle_identity: ""
  oracle_package_digest: ""
  checkpoint_id: ""
```

A missing field is not automatically blocking if the frozen contract does not require it. A required-but-missing identity field is `MISSING_CRITICAL_INPUT`.

## Rawness rules

A statement such as "all tests passed" is a summary unless the evidence bundle exposes the command, denominator, exit status, and raw/immutable log or equivalent receipt.

A screenshot may support a UI state but does not replace machine evidence for code/runtime/package claims where machine evidence is available.

Do not infer runtime readiness from file existence, configuration presence, installed package presence, or a self-reported status string.
