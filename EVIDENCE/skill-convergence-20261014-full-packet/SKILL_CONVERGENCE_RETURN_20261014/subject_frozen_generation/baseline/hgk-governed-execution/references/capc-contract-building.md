# Building a CAPC contract that passes lint/activation/acceptance

Verified 2026-08-12 (A-3 Gate A3-0). The construction-acceptance-prompt-compiler
(`HG-KSEOS\實作執行\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler`,
also mirrored in Fabric `Oracle\工程基座\...`) validates a contract JSON
(`CAPC-PROMPT-CONTRACT/1`) with schema checks PLUS semantic rules in
`scripts/prompt_contract_compiler.py` (`lint_contract`). A new task contract modeled on
`scripts/evo005r7_contract.json` will hit the traps below — fix them in the generator,
not by weakening the compiler.

## Schema traps (fail as PL-SCHEMA)

1. `runtime_readiness[].lifecycle` must be an OBJECT of 16 stages
   (`identify, pin, install_materialize, configure, discover, bind, route,
   effective_load, doctor_health, positive_pilot, negative_security, fallback,
   rollback_uninstall, independent_qualification, certify, enable`), each with an enum
   value: `PASS | OPEN | FAIL | BLOCKED_HITL | BLOCKED_EXTERNAL | NOT_APPLICABLE_SOURCE_BACKED`.
   A string like `"KANBAN+SWARM"` crashes `lint_contract` with
   `AttributeError: 'str' object has no attribute 'get'`.
2. `runtime_readiness[].current_verdict` enum: only `NOT_READY | RUNTIME_READY`.
3. `acceptance[].required_depth` enum: `L0_STATIC_EXISTENCE, L1_SCHEMA_CONTRACT,
   L2_UNIT_BEHAVIOR, L3_INTEGRATION_RUNTIME, L4_FAILURE_RECOVERY,
   L5_REAL_LIFECYCLE_SIDE_EFFECT`. (Runtime subjects with L0/L1 are additionally
   rejected by PL-010.)
4. `evidence[].rerun_rule` enum: only `affected-only | full`.
5. `journeys[]`: `expected_automatic_behavior`, `expected_manual_behavior`,
   `negative_behavior`, `failure_recovery` must be ARRAYS of strings, not strings.
6. `termination.checkpoint_fields` must be a SUPERSET of the exact 7 names:
   `task_id, source_hashes, current_candidate, completed_gates, open_gates,
   next_work_order, rollback_pointer` (minItems 7; using `next_gate` or
   `evidence_refs` instead fails PL-016/PL-SCHEMA).

## Semantic traps (fail as PL-003/PL-006/PL-007/PL-009/PL-013/PL-014)

- `source_scan.required_source_families` must equal the SET of `reviewed[].source_family`
  values with NO duplicates — two reviewed rows cannot share a family (split
  `product_authority` into `product_authority` + `domain_authority` for HGK vs SQS).
- Every ACTIVE execution_scope capability needs an acceptance row whose `subject_id`
  EXACTLY equals the capability name (`subjects` = set of acceptance.subject_id).
  Same for journeys (subject_id == journey_id), `active_requirement_ids`, and every
  `requested_delivery` string — each needs a matching acceptance row
  (subject_type CAPABILITY/JOURNEY/REQUIREMENT/DELIVERABLE).
- `runtime_required=true` acceptance rows need `terminal_states` ∩
  {INDEPENDENT_CASE_PASS, INDEPENDENT_CASE_FAIL, BLOCKED_HITL, BLOCKED_EXTERNAL}
  (PL-010), `raw_evidence_required=true` (PL-011), `independent_checker_required=true`
  (PL-012).
- `evidence[].tracked_subject` is a BOOLEAN; when true, `candidate_binding` must be an
  object with `head`, `package_sha256`, `source_hashes` (PL-013).
- `evidence[].claim_level` and `intent.claim_ceiling` come from
  {LOCAL, PACKAGE, EXTERNAL_ACCEPTANCE, PRODUCTION}; gate claims cannot exceed the
  ceiling (PL-014).
- `authority.current_control_plane_id` must be in `native_control_plane_ids` (PL-018).
- `execution_scope` active capabilities with `runtime_required_now=true` need a
  matching `runtime_readiness` row (PL-007) whose `acceptance_ids` all exist.
- **Activation-bridge booleans are OR'd — a DEFERRED row must set ALL FOUR false (PL-006).**
  `selected` = `any(current_profile_selected, canonical_flow_referenced,
  automatic_route_target, user_experience_required)`. Leaving `canonical_flow_referenced: true`
  (an easy schema-fill habit) while declaring `current_execution_disposition:
  DEFERRED_SOURCE_BACKED` fires "Activation Bridge mismatch" for EVERY deferred capability.
  Set all four `false` on DEFER/STANDBY/OPTIONAL/PROHIBITED rows and `true` only on
  ACTIVE_REQUIRED/ACTIVE_SELECTED rows.
- **An `equal_rank: true` conflict MUST carry `decision: RESOLVED` (PL-004).** A `QUARANTINE`
  decision on an equal-rank conflict IS the blocker — the compiler treats an unresolved
  equal-rank conflict as a hard stop. A source-quality/polarity quarantine is not a two-source
  equal-rank conflict: record it as its own gate row (e.g. the source-quality gate), or use
  `equal_rank: false` with `decision: RESOLVED`.
- **`evidence[].producer` must differ from `independent_checker` even on non-subject rows
  (PL-012).** Placeholders like `producer: "n/a", independent_checker: "n/a"` on deferred gate
  rows trip "maker equals checker"; give them distinct descriptive strings.
- **`lifecycle` needs non-empty `discover|bind|route|effective_load` (PL-008)** in addition to
  the 16-key shape — `OPEN` is accepted (truthy), omitting the key is not.
- **`current_verdict: RUNTIME_READY` while any lifecycle stage is `OPEN` and `work_required`
  is non-empty is internally inconsistent** — an adversarial verification lane WILL flag it.
  A reused capability whose independent-qualification stage is still open should read
  `NOT_READY` + explicit `work_required`; the engine's liveness belongs in the reuse map
  (or the doctor receipt), not in this readiness field.
- **Unselected capabilities must not request `INSTALL`/`QUALIFY`/`ENABLE` (PL-017)** — use
  `DEFER` or `PROHIBIT`.
- Compiler verbs: `lint`, `activation`, `acceptance`, `render`, `compile`, `hash`,
  `duplication`. `compile --out-dir` emits `thin-prompt.md` + `compiler-report.json` +
  `compiler-receipt.json`; read the contract sha from the report/receipt (not from
  `compiler-receipt.json`'s sibling fields), and keep the rendered prompt under
  `render_policy.max_prompt_chars`.

## Full field shapes for NEW_IMPLEMENTATION contracts (verified 2026-08-13 FAR)

The traps above are necessary but not sufficient — these exact fields unblock lint
(PL-003/PL-006/PL-007/PL-009 fired when they were missing). Build with a generator
script (`var/<task>/capc/gen_contract.py`) and iterate lint → fix → lint:

- `authority.sources[]`: `id, rank, path, sha256, locator, role, governs` (PL-003 wants
  `locator` on every NORMATIVE source).
- `execution_scope[]` rows: `capability, source_disposition, current_execution_disposition`
  (DISPOSITIONS enum: ACTIVE_REQUIRED/ACTIVE_SELECTED/STANDBY/OPTIONAL/
  DEFERRED_SOURCE_BACKED/DONOR_ONLY/NATIVE_SUBSTITUTED/NOT_APPLICABLE_SOURCE_BACKED/
  PROHIBITED — PL-006), `current_profile_selected, canonical_flow_referenced,
  automatic_route_target, user_experience_required, runtime_required_now, action
  (INSTALL), source_locators[], external_method, control_authority`.
- `runtime_readiness[]`: `capability, runtime_id, required_now, current_verdict,
  work_required[]` (PL-007 wants `required_now` + `work_required`), `lifecycle` (16
  stages), `acceptance_ids[]` (must exist in acceptance).
- `journeys[]`: `journey_id, required, user_goal, expected_visible_result, description,
  expected_automatic_behavior[], expected_manual_behavior[], allowed_hitl[],
  required_capabilities[] (names of execution_scope capabilities), negative_behavior[],
  failure_recovery[], source_expectation_ids[], source_locators[]` (PL-009).
- `acceptance[]` rows: `acceptance_id, subject_id, subject_type, source_locators[],
  required_depth, positive_fixture, negative_fixture, recovery_fixture,
  runtime_required, raw_evidence_required, independent_checker_required,
  terminal_states[] (when runtime_required), pass_condition`. subject_id must EXACTLY
  match the capability/journey/requirement/deliverable name; acceptance_id is the id
  referenced by runtime_readiness.
- `evidence[]` rows: `evidence_id, tracked_subject (bool; true ⇒ candidate_binding
  {head, package_sha256, source_hashes}), subject, kind, rerun_rule, claim_level,
  checker`.
- `termination`: `terminal_states[], non_terminal_pause[], checkpoint_required,
  checkpoint_fields (7 exact names), retry_budget, rollback_pointer_required`.
- `render_policy`: `control_corpus_restatement, embedded_control_bodies[],
  max_prompt_chars, output_language`.

## Receipt hygiene (verified on a pre-construction qualification round)

- **`lint`, `activation` and `acceptance` receipts are BYTE-IDENTICAL when all three return
  `PROMPT_COMPILE_PASS` with `error_count: 0`** — the compiler emits the same
  `{verdict, error_count, errors}` body regardless of stage. An independent lane WILL flag a
  G5 "4/4 validators" claim whose four receipts carry no per-stage identity. Write each receipt
  back with its own `stage`, the `validator` path, and `contract_sha256` (hash of the contract
  file) added, so the stage is provable from the artifact rather than from your narrative.
- **`claim_ceiling` lives in `compiler-report.json`, not `compiler-receipt.json`** — the receipt
  carries only `contract_sha256` + verdict. Attribute it correctly when citing; a lane reading
  the receipt for a ceiling you claimed there will report it missing.
- Take the contract sha from the report/receipt output, never from a sibling field you filled
  yourself; and confirm the rendered prompt length against `render_policy.max_prompt_chars`.

## Successor-round contracts (NARROW_REPAIR cloned from its passing predecessor)

When a new repair round has no contract of its own, generate it by cloning the previous round's PASSING contract and re-targeting it. Two traps that cost real rounds:

- **`authority.sources[]` requires `path` AND a BOOLEAN `governs`** — `id, rank, path, sha256, locator, role, governs` where `governs` is `true/false`, not a prose string, and `path` must be present. The role enum is CLOSED: `NORMATIVE | STATE_EVIDENCE | SUPPORT` only — do not invent `NORMATIVE_EQUAL_RANK_CONFLICT`; a two-report equal-rank conflict enters as two separate NORMATIVE sources (one per report) plus an `authority.conflicts[]` row.
- **A `SUPPORT` source cannot `govern` normative behavior (PL-004).** A source that is one leg of an adjudication authority is NORMATIVE, not SUPPORT.
- **`authority.conflicts[]` row shape is EXACT**: `conflict_id, sources[>=2], tt_id, equal_rank, decision` — no `description`, no `subject`, no extra keys (schema is `additionalProperties: false`). An `equal_rank: true` row MUST carry `decision: RESOLVED` (PL-004; QUARANTINE is itself the blocker). The `sources` field must name the two report source IDs (min 2).

- **Clone-then-retarget blows the duplication gate.** A NARROW successor whose acceptance fixtures / journey prose are copied verbatim from the predecessor trips `duplication --source <predecessor>` at ratio > 0.25 (observed 0.263). Fix in the generator, not by weakening threshold: rewrite `intent.explicit_constraints` / `non_goals`, and make EVERY acceptance row's `positive_fixture/negative_fixture/recovery_fixture` round-specific (name the subject_id in each), so the rendered thin-prompt is genuinely different while the schema shape stays copied. After diversifying, rerun all five verbs and re-check the ratio is < 0.25 (landed 0.166).

## Reading the compiler's errors (do this BEFORE editing the contract)

The compiler returns a JSON body `{verdict, error_count, errors:[{code, message, path}]}`. Do not fix one
message at a time:

- **Group by code first** (`Counter(e["code"] for e in errors)`) — a single schema mistake fans out into
  dozens of `PL-SCHEMA` lines, so the real cause count is the NUMBER OF DISTINCT CODES, not `error_count`.
  The first run of a fresh contract was 24-36 errors that collapsed to ~5 causes.
- **Dump the schema for the section you got wrong instead of guessing keys**:
  `references/prompt-contract.schema.json` → that section's `items.required`, its `properties`, and
  `$defs.lifecycle.required` (the exact 16-stage list). `PL-SCHEMA path=/runtime_readiness/0` with "'X' is a
  required property" means a required field is missing; "Additional properties are not allowed" means the
  schema is `additionalProperties: false` and you added a helpful extra (readiness rows allow ONLY
  `capability, required_now, lifecycle, current_verdict, work_required, acceptance_ids`).
- **Faster still: clone the EXACT row shape from the newest contract that already passes.** Dump its
  `runtime_readiness[0]` and `acceptance[0]` and copy the shape rather than reconstructing from prose — this
  is why the `lifecycle` object must be copied whole (16 keys) and why `current_verdict` sits beside
  `work_required` and `acceptance_ids`.
- `PL-007 "<subject> readiness references unknown acceptance IDs"` = you invented an id; every entry of
  `acceptance_ids` must exist as an `acceptance[].acceptance_id`. Likewise each ACTIVE capability AND each
  `active_requirement_ids` entry needs its own acceptance row (subject_type `CAPABILITY` / `REQUIREMENT`) —
  an active capability with no acceptance edge is PL-007, a requirement with none is PL-009.
- `duplication` returns `results[].ratio` per `--source` plus an overall verdict; a low ratio (e.g. 0.008)
  against the RBWI + SKILL.md is the expected shape for a genuinely new task contract, not a copy.

## Working flow

1. Model the contract on the newest sealed contract in `scripts/` (evo005r7…).
2. Iterate: `lint` → `activation` → `acceptance` (all must return
   `PROMPT_COMPILE_PASS`, 0 errors); `duplication --source <prior contract>` to prove
   no copy (A-3 ratio 0.025); `hash` to pin; `compile --out-dir` to emit
   thin-prompt/report/receipt.
3. The compiler verdict is NOT runtime PASS — it is Gate A3-0 evidence only.
4. Keep the contract generator + contract in gitignored `var/a3/` (task tooling).
