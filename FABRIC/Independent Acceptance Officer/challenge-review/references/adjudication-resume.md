# Adjudication and Resume Contract

## Disagreement routing

1. Name the exact disputed acceptance predicate and evidence IDs.
2. Recheck subject digests, command/log binding, and deterministic results.
3. Classify a missing or stale edge as `EVIDENCE_GAP`.
4. Classify a candidate contradiction as `CONFIRMED_DEFECT` only when frozen authority and raw evidence establish it.
5. Classify a checker/evaluator interpretation conflict as `ORACLE_DISAGREEMENT`.
6. Route deterministic evidence mismatch to the evidence/Oracle owner. Route unresolved domain truth to the domain owner. Route unresolved high-risk or authority conflict to Meta-Oracle/HITL.

Disagreement is never automatically a candidate failure and never authorizes the reviewer to edit the evaluator.

## Resume packet

A `RESUME_SMALLEST_REPAIR` handoff contains the exact candidate digest, finding and acceptance IDs, earliest owner, smallest authorized repair scope, prohibited paths, focused retest, affected regression, rollback, evidence to regenerate, and requirement for a fresh checker. Resume only against a newly frozen candidate identity; do not reuse the prior verdict.
