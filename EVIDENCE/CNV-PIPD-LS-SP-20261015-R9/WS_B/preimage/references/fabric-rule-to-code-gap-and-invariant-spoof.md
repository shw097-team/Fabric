# Ratified policy is not implemented policy; free-text fields are not invariants

## Before claiming a governance rule is enforced, map rule -> code
A Fabric `control/*.yaml` `hard_rules` entry can be ratified for months with **zero** implementing code. Verify by grepping `src/` for a reader of that YAML; if nothing reads it, the rule is documentation. `ACCEPTANCE_POLICY.yaml`'s `missing_required_raw_evidence: FAIL_CLOSED` and `subject_digest_mismatch: FAIL_CLOSED` were both unimplemented while `resolve_acceptance` accepted any registered evidence.

Why it matters: 'implementing the ratified rule' reads as low-resistance conformance, but the first time a rule becomes executable it is a **new canonical mechanism** and carries the full ChangeSet + independent-acceptance burden. Do not let the 'already ratified' label shrink the process.

## Never build an invariant on a free-text column
`SharedSpine.register_evidence` validates only `len(sha256) == 64`; `kind`, `producer` and `checker` are unvalidated text. An invariant of the form `requires kind == 'INDEPENDENT_VERIFY_VERDICT'` is therefore **spoofable by one INSERT**. Before writing any such check, ask what binds the row to reality and state it explicitly as one of: re-hash the file at `locator` and compare to `sha256` (tamper-evidence only), a policy-declared positive identity whitelist (check whether one exists - `AUTHORITY_MATRIX.yaml` may only list object owners, not verifier roles), or a subject digest (usually absent). If none is enforceable without a migration, say so rather than shipping a forgeable 'enforced' claim into canonical - a fake guarantee is worse than none.

## Budget the companion fixture ChangeSet before applying a strengthened invariant
Tightening a canonical choke point (`record_workorder_result`, `resolve_acceptance`) breaks every existing fixture that calls it with ordinary evidence. Measured on one change: **15 of 24 canonical acceptance tests (2 failures + 13 errors)** because fixtures register non-file-backed evidence with constant sha256 values. This is an intended fail-closed divergence, not a bug - but it must be disclosed in the closeout as an explicit 'do not apply as-is' item, together with the choice it forces: align the fixtures, or scope the invariant (e.g. a per-requirement governed marker) instead of applying it to every workorder result.

## Two verb quirks on this host
- `hermes kanban` has no `update` verb; use `complete <id> --result '<what was done>'`. An empty completion is refused by design ('an empty completion is not evidence'), and a child cannot complete while a parent is blocked - complete parents first.
- A candidate round must record its own verdict evidence as `kind=INDEPENDENT_VERIFY_VERDICT` with `producer` **and** `checker` set to the officer (never `None`, never the writer): that is exactly the shape the strengthened invariant will demand after the migration lands.
