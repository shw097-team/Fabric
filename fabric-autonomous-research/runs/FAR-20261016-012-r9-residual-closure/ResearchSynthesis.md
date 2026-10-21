# ResearchSynthesis — FAR-20261016-012-r9-residual-closure

## decision_summary
Eight residual/decision items were adjudicated against the governing package and the external report. Two are
**executed** this round as bounded, reversible repairs: (1) the R8-0 validator hardening is adapted to the newer
`main` contract by two hunks confined to `validate.py`, with the M04/M06/M16 mutations kept as the negative
control; (2) the blocked `hgk-governed-execution` slim candidate is repaired (two lost reference texts restored,
plus a third discovered by re-measurement) and applied by non-destructive overlay. One item is **resolved by the
governing text itself** ("10/6" = AVR ten pieces + HGK six pieces in `ACC-RQ06`). Two of this mission's own earlier
claims are **withdrawn/recalibrated** (a non-reproducing drift claim; a size "cap" that the PKG never states).
Five items remain **owner actions**, each written as a single action with a named authority.

## claim_source_map
- CL-01/CL-02/CL-03 → this round's own execution of the named tests and probes on the `r8-wt` worktree (`SRC-09`).
- CL-04 → the dispatch receipt's `attempts[]` and `identity_gate.arms[]` (`SRC-08`).
- CL-05 → the repository's own `lane_policy.check_drift` plus the registry's `routes[]`/`projections[]`/`notes` (`SRC-10`).
- CL-06/CL-09/CL-10 → the round's C1–C6 harness run three times (the worker's insertion, the orchestrator's
  reproduction, and the orchestrator's re-run against the successor candidate) (`SRC-13`).
- CL-07/CL-08 → verbatim extraction from the PKG and the external report (`SRC-01`, `SRC-02`).

## confidence_by_claim
CL-01..CL-04 HIGH (re-executed); CL-05 HIGH (own API call); CL-06/CL-09 HIGH (three independent runs agreeing);
CL-07 HIGH (verbatim quotes at byte intervals); CL-08 HIGH; CL-10 HIGH (a code-reading defect reproduced twice).

## supporting_evidence
`ExtractionLedger.jsonl` (11 records), the three harness JSONs, the two test runs, the three probe JSONs, the
receipt's attempts rows, the `check_drift` result, and the PKG byte-interval extracts.

## counterevidence
- The FAR worker's repair measurement claimed 112 live references and 0 lost; the canonical tree carries 113 and
  one was absent → the worker's denominator was one short (CL-09).
- The R8 round recorded the served arm as unprovable; the receipt carries it (CL-04).
- The R8 record claimed a registry drift; the repository's own check disagrees (CL-05).
- The R8 record framed a 100000-byte cap as a governing limit; the PKG contains no such clause (CT-02).

## unresolved_disagreement
None outstanding inside this run: the three live disagreements (DG-01..DG-03) were each resolved by re-execution.
The owner-declared SoD residual (PLAN and VERIFY on the same model family) is **not** a disagreement to resolve
here — it is an accepted, recorded owner position.

## missing_unverified
- The loader-parity leg of `ACC-RQ06` ("exact_equal_to_trusted_observation_after_replay") is NOT discharged: no
  pinned trusted observation exists to replay against.
- The provider-side attestation of which model served which turn is not available; attribution is receipt-bound.
- The 221 planned acceptance cases, the eight Gates and Fresh G1 were not executed.
- The system's own skill-size enforcement was not invoked as a live refusal probe (it was read as source).

## cost_operational_tradeoff
The executed repairs cost one bounded writer lane and one refused apply attempt; the cheapest available path was
reuse (the R8 harness, the R8 apply/rollback helpers, the existing openspec proposal for the registry rebind).
No new harness, lane, database or pipeline was introduced.

## recommended_disposition
`RESEARCH_PARTIAL`. Execute the two repairs (done, pending the successor apply's own gate), hand the five owner
actions over as prepared one-action records, and carry the corrections into the same change as the new findings.

## nonclaims
No acceptance, no Gate PASS, no AO verdict, no release, no production effect, no authority to mutate the control
plane, and no claim of independence between PLAN and VERIFY while both may run on the same model family.
