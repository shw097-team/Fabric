# R7-0 validator hardening — what changed, per blind spot

ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`. Bounded writer, EXECUTE lane
(Codex CLI, provider/model `opencode-go/deepseek-v4.1-flash`). Claim ceiling **LOCAL /
candidate-only** — this document is a candidate description of the change; it carries no acceptance,
no checker verdict, and no Gate PASS.

The change is to the bound PIPD validator only. It strengthens existing predicates, weakens none,
and the whole validation path stays deterministic (no LLM, no network, no clock). `R7_VALIDATOR_DIFF.patch`
is the authoritative diff; the line numbers below index the post-change files.

## Root cause (EIA-R6-04)

All three blind spots are the same defect class: a *tampered body that keeps a valid-looking
identity*. The release-bound families already recompute their own digest (`_body_hash`) and refuse
a body edited without re-issuing identity, but three identity-bearing sub-records were **not** in
that set. Each mutation edits exactly such an unchecked field while leaving the record's
`content_hash` intact:

| id | record | field tampered | observed (R6) |
|----|--------|----------------|---------------|
| M16 | `TraceLink` (11 fields) | `to_hash` → 64×`f` | ACCEPT |
| M06 | `RequirementAtom` | `risk_guard.oracle.expected` → `999` | ACCEPT |
| M04 | `ProfileBinding` | `assurance` → `[deterministic_validator]`, `artifact_depth` → `L1_SCHEMA_CONTRACT` | ACCEPT |

The measured hash rule (probe `RAW/probe_hashcheck.stdout.txt`) is
`content_hash == sha256(canonical_json(record minus {subject_id, version, content_hash, schema_version, trace, _profile_meta}))`,
confirmed for PI-PKG, RequirementAtom, TraceLink and ProfileBinding. That is the first-layer hook.
A *second*, stronger layer binds the tampered value to its frozen reference, so the fix is not
merely "the digest moved": an attacker who re-issues identity after tampering is still refused.

## Blind spot 1 — M16 `TraceLink` trace-atom digest

- **Predicate (self-digest):** `validate.py:95` — `if contract in DIGEST_BOUND and ch and len(record) > 4: if ch != _body_hash(record): …`. `DIGEST_BOUND` (`validate.py:22`) extends `RELEASE_BOUND` with `RequirementAtom`, `ProfileBinding`, `TraceLink`.
- **Predicate (frozen reference):** `validate.py:153`–`176` — each `TraceLink` endpoint hash is compared to the frozen subject→digest map (`frozen_context["trace_endpoint_hashes"]`); a missing map fails closed (`validate.py:166`).
- **Reasoning.** A `TraceLink` carries `from_hash`/`to_hash` that reference *other* atoms. In the M16 construction the validator is handed only the single `TraceLink` (`validate.validate_bundle({"TraceLink": trace0}, SCHEMAS)`), so there is nothing to recompute the endpoint from locally. Two layers are therefore required: (1) the link's own `content_hash` must cover its body, catching the in-place `to_hash` edit; (2) when a frozen subject→digest map *is* available the recorded endpoint hash must equal the frozen digest, catching a tamper that re-issues identity. With no frozen map the endpoint binding is unprovable, so the validator emits `UNBOUND_FROZEN_CONTEXT` rather than passing — a missing binding is not a pass.

## Blind spot 2 — M06 domain-oracle `expected`

- **Predicate:** `validate.py:178`–`200`. `oracle.expected` must equal the value derived from the atom's own clause polarity (`POLARITY_EXPECTED`, `validate.py:27`: `MUST → required`, `MUST NOT → forbidden`); when the frozen `oracle_expected` map is present the value must also match it.
- **Reasoning.** `expected` is not a free-standing number — `requirements.compile_requirements` derives it from the clause polarity (`'required' if polarity == 'MUST' else 'forbidden'`). Binding `expected` back to that polarity means a foreign value such as `999` is a deterministic mismatch, regardless of whether identity was re-issued. The optional frozen `oracle_expected` map additionally ties the value to the frozen acceptance source; the polarity binding alone closes the M06 case deterministically from data already on the atom.

## Blind spot 3 — M04 profile assurance downgrade

- **Predicate:** `validate.py:202`–`240`. A `ProfileBinding`'s `assurance` must not be weaker than the frozen requirement for its profile, and `artifact_depth` must equal it. When the profile has **no** frozen requirement the validator FAILS CLOSED with `UNBOUND_FROZEN_CONTEXT` (`validate.py:213`, `:229`).
- **Reasoning.** `profiles.PROFILES` is the frozen requirement table (ASSURED → `L4_FAILURE_RECOVERY` + four assurance axes; LITE → `L1_SCHEMA_CONTRACT` + one). Requiring `assurance` to be a superset of the frozen set means `ASSURED→LITE` is refused by missing axis (`negative_security`, `adversarial`, `independent_checker`) and the depth floor is refused separately. The fail-closed branch is deliberate: if the frozen requirement is unavailable (unknown/absent profile) the validator cannot prove the assurance is adequate, so it refuses rather than silently passing.

## Wiring (deterministic, additive)

- `semantic_invariants(contract, record, frozen_context=None)` — `validate.py:64`. New optional, purely additive argument; `frozen_context=None` preserves every prior predicate exactly.
- `validate_bundle(bundle, schemas_dir=None, frozen_context=None)` — `validate.py:244`; threads the context into `semantic_invariants` (`validate.py:260`).
- `validate.derive_frozen_context(source, …)` — `validate.py:266`. Assembles the context from data the caller already holds: a PI package yields the trace-endpoint map and the oracle-expected map from its own atoms/links; the profile requirement comes from the frozen `PROFILES` table. A map whose source is absent is *omitted*, so the corresponding fail-closed branch still fires.
- `pipeline.frozen_validation_context(pi)` — `pipeline.py:192`, and `pipeline.validate_pi(pi, schemas_dir=None)` — `pipeline.py:203`. The pipeline-level entrypoint that validates the PI package (PI-PKG + ProfileBinding + every RequirementAtom + every TraceLink) against the self-derived frozen context.
- `cli.py:166`–`172` — the `validate` command derives a frozen context from an embedded `PI-PKG` when present and passes it, so the binding actually reaches the CLI surface.

## Determinism / non-regression evidence

- `RAW/probe_r7_validator.py` → three blind spots FAIL, positives PASS, `validate_pi` PASS/0 findings.
- `RAW/probe_r7_strong.py` → the *stronger* attacker who re-issues identity is still refused by the frozen-reference layer (trace digest / oracle polarity / profile requirement), and the unknown-profile case fails closed with `UNBOUND_FROZEN_CONTEXT`.
- `RAW/r7_run_mutations.stdout.txt` + `R7_MUTATIONS_18_RERUN.json` → 10/10 executed REJECT, 8 NOT_RUN.
- `pytest` on `test_s1_lite_slice`, `test_negative_and_rollback`, `test_technology_admission`, `test_tqaep_design_positive`, `test_cli_typed_errors` → 44 passed. Full suite shows 7 failures that also fail on the unmodified pre-change snapshot (Windows `copytree` on venv junctions), i.e. pre-existing environmental, not caused by this change.
