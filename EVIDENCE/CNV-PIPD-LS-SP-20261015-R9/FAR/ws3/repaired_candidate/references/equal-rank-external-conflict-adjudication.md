# Equal-rank external-review conflict adjudication

Use when two same-rank external challenge reports bind the SAME immutable subject tuple but
disagree (e.g. Report A `PASS_CHALLENGE / NON_BLOCKING`, Report B `FAIL_CHALLENGE / S3
blocker`, same exact source/evidence SHA). The compiler contract quarantines unresolved
equal-rank conflict: you must NOT silently select either report.

## Decide by deterministic repro, never by preference

- Do NOT resolve by report preference, majority, chronology, test count, or model judgment.
- Resolve from: (1) frozen canonical authority (the PI/PD source the reports name), and
  (2) exact current code + real reachability — probed on the EXACT frozen bytes.
- Materialize an `*_ADJUDICATION.json` with per-predicate raw evidence BEFORE any product write.

## Gate sequence

1. **Baseline identity freeze** — `git rev-parse HEAD` must equal the report's subject source SHA;
   the subject evidence SHA must resolve; worktree serial. A mismatch -> `TEMP_CLOSED_BASELINE_*`;
   never adjudicate on drifted bytes.
2. **Frozen canonical authority** — grep the named PI/PD doc for the literal required semantics
   at their cited lines (e.g. PI-PKG-06 DOC-03: CRITICAL->AAC3, `required_authn_assurance`
   REQUIRED). Record the exact line locators.
3. **Reachability inventory** — grep the WHOLE source tree (not just tests) for every occurrence
   of the disputed selector/field. Classify: public export surface, production call sites,
   test-only sites, schema/JSON ingress, docs. Do not equate "no in-repo consumer" with
   "unreachable" if the accepted public/API contract itself exposes the field.
4. **Full-route counterexample, not helper-only** — drive the disputed request through the real
   production caller (e.g. `assert_human_gate_satisfied`) with a valid signed token chain
   (reuse the test module's own valid-token fixtures), not a synthetic helper call. Capture
   floor resolution + verifier result, plus a CONTRAST control (same request minus the disputed
   selector).
5. **Deterministic branch** — `BLOCKER_CONFIRMED` requires EVERY predicate true
   (selector exposed on current scope/public surface; caller controls it without trusted
   provenance; missing canonical floor reaches verifier; compatibility path substitutes the
   weaker assurance; the protected semantics can be under-enforced; no higher source authorizes
   the downgrade). If ANY cannot be proven -> `TEMP_CLOSED_*`, no mutation.

## Branch A (blocker confirmed) — smallest repair

- Remove the request-controlled compatibility selection from the canonical verifier boundary;
  a canonical request must carry an explicit validated floor or fail closed (None -> DENY).
- Do NOT replace `adapter_kind`/`local_adapter` with a renamed caller-controlled `trusted_*`
  flag — that is the same bug. Prefer deletion over inventing compatibility policy.
- Only after: focused adversarial acceptance (floor lattice + bypass attempts), full no-shrink
  regression with the new SHA, fresh-context VERIFY_ONLY checker, exact-subject HGK checkpoint,
  distinct evidence commit, external re-challenge. New source SHA required; freeze it.
- The probe fixtures must come from the canonical field-value domain, never hand-invented.

## Branch B (nonblocking current scope) — no mutation

- No product source change, no dummy SHA. Keep the disputed selector on a TT
  (`TT-W3-<ADAPTER>-BOUNDARY`) that blocks only the first affected journey that activates it.
- Terminal claim: `READY_FOR_FRESH_EXTERNAL_CONFLICT_RESOLUTION_ON_UNCHANGED_TUPLE`; a fresh
  external reviewer reconciles and returns `PASS_CHALLENGE` before W3.

## Termination

- `TEMP_CLOSED_EQUAL_RANK_EXTERNAL_CONFLICT` when reachability/ownership cannot be proven
  safely. Never self-issue `PASS_CHALLENGE`; never self-dispatch W3. Report with the five-block
  shape (decision / adjudication / blockers-TT-CR / handoff / non-claims), SHA-256 every final
  artifact referenced.
