# Compiling a task through the canonical construction-acceptance prompt compiler

Before any mutation in a governed construction order, the canonical
`construction-acceptance-prompt-compiler` bundle must compile the task as exactly one contract and return
`PROMPT_COMPILE_PASS`. A `PROMPT_COMPILE_BLOCKED` means stop with that state — do not handwrite around the
compiler.

## Locate the bundle first

The knowledge-base path is often nested one level deeper than expected
(`.../construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler/`). Do not conclude
`PROMPT_COMPILE_BLOCKED` from a missing file at the shallow path — search the tree for
`scripts/prompt_contract_compiler.py` and run the bundle's own suite from the directory that contains
`tests/` and `references/`.

## Procedure

1. Read the schema's `required` top-level keys from `references/prompt-contract.schema.json`.
2. **Mirror a shipped clean-linting reference contract from `scripts/*_contract.json` — do NOT hand-author
   from the JSON Schema.** The schema is a coarse gate; the compiler enforces a much deeper contract, and a
   hand-authored contract fails lint with a long error list. Copy a shipped contract and replace only the
   CONTENT, preserving its structural conventions and enum values.
3. Run the validators in order and capture each exit code into a receipt:
   `lint <contract>` → `activation <contract>` → `acceptance <contract>` →
   `compile --out-dir <DIR> <contract>` → `duplication <RENDERED_PROMPT> --source <SOURCE_FILE>`.
4. Run the bundle's own suite as a health check: `python -m unittest discover -s tests -t tests`.
5. Record `PROMPT_COMPILE_PASS` only when every validator AND the self-test exit 0. Capture the compiler's
   `contract_sha256` from the compile verdict as the receipt's immutable identity.

## CLI shapes that differ from expectation

- `compile` takes `--out-dir <DIRECTORY>` (not `--out <file>`). It writes `thin-prompt.md`,
  `compiler-report.json`, and `compiler-receipt.json` into that directory.
- `duplication` takes the **RENDERED PROMPT FILE** (from the compile output) as its positional argument,
  and `--source` must be a **FILE**. Passing a directory to `--source` raises `PermissionError`
  (`read_text` on a directory); passing a different file raises `FileNotFoundError`. Both surface as a
  traceback, not a clean verdict — a traceback here means a wrong argument shape, not a blocked compile.
- A validator exiting 2 with the verdict printed on stdout means **lint failed and it is reporting a JSON
  error list** — parse stdout, do not assume an argparse usage error.

## Contract constraints that actually bite

- **Exactly one `source_scan.reviewed` entry per required source family.** A second entry reusing a family
  (even for a legitimate extra source) fails with `duplicate=True`. Move extra sources into
  `authority.sources` instead, which is not family-checked.
- **An acceptance edge is required for EVERY capability in `execution_scope`, EVERY id in
  `intent.active_requirement_ids`, EVERY id in `intent.requested_delivery`, and EVERY `journey_id`.** Each
  needs an `acceptance[]` entry whose `subject_type`/`subject_id` matches. Omit one class and you get a
  `lacks acceptance edge` error per member.
- Requirement and delivery ids must belong to THIS task — a mirrored reference contract carries its
  predecessor's ids and will demand acceptance edges for them.
- Every `evidence[]` gate needs `maker != checker`. A self-produced gate read back by the same id fails;
  use a distinct readback id for self-produced gates.
- `termination.checkpoint_fields` must carry the canonical field set (mirror the reference's list and
  extend it), not an arbitrary set — too short is an error.
- Enumerated fields reject free text. Values observed as valid: `execution_scope[].action` ∈
  {NONE, DESIGN, QUALIFY, INSTALL, ENABLE, USE_NATIVE, DEFER, PROHIBIT};
  `current_execution_disposition` ∈ {ACTIVE_REQUIRED, ACTIVE_SELECTED, STANDBY, OPTIONAL,
  DEFERRED_SOURCE_BACKED, DONOR_ONLY, NATIVE_SUBSTITUTED, NOT_APPLICABLE_SOURCE_BACKED, PROHIBITED};
  `acceptance[].subject_type` ∈ {CAPABILITY, JOURNEY, DELIVERABLE, REQUIREMENT};
  `required_depth` ∈ {L0_STATIC_EXISTENCE, L1_SCHEMA_CONTRACT, L2_UNIT_BEHAVIOR, L3_INTEGRATION_RUNTIME,
  L4_FAILURE_RECOVERY, L5_REAL_LIFECYCLE_SIDE_EFFECT};
  `evidence[].claim_level` ∈ {LOCAL, PACKAGE, EXTERNAL_ACCEPTANCE, PRODUCTION};
  `rerun_rule` ∈ {affected-only, full}; `runtime_readiness[].current_verdict` ∈ {NOT_READY, RUNTIME_READY}.
- Fields that read as prose are typed: `journeys[].expected_automatic_behavior`, `expected_manual_behavior`,
  `negative_behavior`, `failure_recovery` are **arrays**; `authority.sources[].rank` is a **string**
  (e.g. `R1`), `governs` is a **boolean**; `evidence[].tracked_subject` is a **boolean**,
  `candidate_binding` is an **object**, `invalidation` is an **array**, `independent_checker` is a
  **string**; `runtime_readiness[].work_required` is an **array** and `lifecycle` is an **object** of stage
  keys.

## Why mirroring beats authoring

The compiler's effective contract is not discoverable from its published JSON Schema, and each wrong guess
returns a large undifferentiated error list. Reading a shipped contract that already lints clean transfers
~130 constraints in one step. When lint still fails, fix the residual errors by category (family duplicate,
missing edges, maker==checker, checkpoint fields, enum) rather than re-authoring.
