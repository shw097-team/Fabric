# Finding Contract

Use exactly one classification: `CONFIRMED_DEFECT`, `EVIDENCE_GAP`, `ORACLE_DISAGREEMENT`, `NON_BLOCKING_OBSERVATION`, or `OUT_OF_SCOPE`.

Required fields:

```yaml
finding_id: stable identifier
classification: one of the five values
severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
candidate_digest: exact frozen subject digest
acceptance_id: exact predicate identifier or NOT_APPLICABLE
evidence_id: exact evidence identifier or MISSING
source_locator: exact frozen authority locator
observed: evidence-grounded observation
expected: frozen predicate
impact: bounded claim impact
earliest_owner: first component legally able to repair
smallest_repair: minimal authorized scope; never an executed patch
focused_retest: exact retest for the repaired predicate
affected_regression: bounded neighborhood regression
status: OPEN | TEMP_CLOSED | ROUTED | NON_BLOCKING
```

For `CRITICAL`, `HIGH`, or any finding that blocks the verdict, `acceptance_id`, `evidence_id`, `earliest_owner`, `smallest_repair`, `focused_retest`, and `affected_regression` cannot be empty. Use `MISSING` only for an `EVIDENCE_GAP`, never to disguise a confirmed product defect.

Do not merge different earliest owners into one broad repair. Do not report implementation instructions that grant the reviewer write authority.

All blocking `acceptance_id` and all non-`MISSING` `evidence_id` values must resolve to the canonical intake; blocking rows cannot use `NOT_APPLICABLE`. `source_locator` is `NORMATIVE_EVIDENCE_ID#ACCEPTANCE_ID` and must resolve to bound `NORMATIVE` bytes. `MISSING` is legal only for `EVIDENCE_GAP`. Finding IDs are unique, nested fields are closed, `blocking` is a required boolean, and `status` is exactly `OPEN`, `TEMP_CLOSED`, `ROUTED`, or `NON_BLOCKING`. `CONFIRMED_DEFECT` always blocks, uses only `OPEN` or `ROUTED`, and requires subject-bound raw evidence plus a matching objectively failing `CONTRADICTED` evidence edge. `NON_BLOCKING_OBSERVATION` and `OUT_OF_SCOPE` alone use `NON_BLOCKING`; no other classification may use it.

Verdict and claim ceiling are a fixed pair: `PASS_CHALLENGE → SKILL_CANDIDATE_QUALIFIED`, `PARTIAL_CHALLENGE → PARTIAL_LOCAL_CHALLENGE`, `TEMP_CLOSED_CHALLENGE → TEMP_CLOSED_LOCAL_CHALLENGE`, and `FAIL_CHALLENGE → FAIL_LOCAL_CHALLENGE`. PASS requires complete raw supported acceptance coverage and cannot contain a defect/gap/disagreement. FAIL requires a blocking raw-evidence `CONFIRMED_DEFECT` and `RESUME_SMALLEST_REPAIR`. PARTIAL requires an unresolved or contradicted edge/finding. TEMP_CLOSED requires an `EVIDENCE_GAP` or `ORACLE_DISAGREEMENT` with `TEMP_CLOSED` status.
