# External acceptance: single-MD closure with embedded raw evidence (FAR EXT-FAR r1→r7, 2026-08-13)

Verified end-to-end on fabric-autonomous-research (FAR): three external review rounds
(r1 PARTIAL_CHALLENGE with EXT-FAR-001..010 → r4/r6 narrow evidence gaps → r7
PASS_CHALLENGE / FAR-R1 PASS). The reviewer's rules: `existing PASS = claim`;
`PASS_CHALLENGE = no blocking contradiction AND every required raw edge reviewed`;
`PRODUCT_REBUILD_REQUIRED=NO / BROAD_RERUN_REQUIRED=NO` → evidence-only smallest repair.

## 1. Delivery transport: single acceptance MD with FULL inline raw content

Clean-room reviewers may NOT be able to open MEDIA attachments (renders as `[Open](#)`)
or local paths (they check their own `/mnt/data`). The ONLY reliable transport is the
message content itself.

- Deliver ONE acceptance MD (`FAR_FINAL_ACCEPTANCE_EVIDENCE.md` style) that EMBEDS every
  load-bearing raw edge inline:
  - Q4/Q10 receipts: full JSON bodies (never summaries)
  - crosswalk: ALL rows (ID|predicate|locator) — "92/92 independently reviewed" is only
    legal when all 92 rows are in the message; samples got flagged as EVIDENCE_GAP
  - subject root: ALL (relpath|sha256) rows so the reviewer can recompute the merkle digest
  - evidence manifest: ALL entries; spine readback: all WO rows incl. result_json + all EVD rows
  - kanban snapshots: full text; test stdout + exit code: full text; closure receipts: full JSON ×N
- Excerpts / hash-only / sample tables → new EVIDENCE_GAP finding (EXT-FAR-R5-001 class).

## 2. Freeze chain when the acceptance MD embeds the manifest

- The evidence manifest MUST exclude the acceptance MD from its entries (else regen loop:
  MD embeds manifest rows; manifest hashes MD).
- Single-direction binding: acceptance MD embeds manifest rows + references manifest by
  path; manifest references the MD by path only.
- ANY receipt change (NBO fix, new receipt, doc add) → full chain:
  1. fix artifact → 2. regenerate manifest (current bytes; excludes self + acceptance MD)
  → 3. regenerate acceptance MD → 4. mirror ×4 (FAR root + HGK/Fabric/SQS evidence\review)
  → 5. SHA-256 equality → 6. register SUPERSEDING EVD (R2/R3/R4…; never rewrite old rows).

## 3. Negative side-effect receipt (EXT-FAR-R6-002 class)

Locator-only negative claims (`"spine readback + evidence (no broker adapter)"`) get flagged.
Provide a subject-bound receipt with ALL of:
- exact `subject_root_digest` binding (must NOT change the frozen subject — it's an
  acceptance artifact, excluded from the subject tree)
- `unauthorized_side_effects=0` + run denominator (WOs/tests/canaries) + deterministic
  check (`find -newermt <window-start> <product paths>` = empty; evidence manifest locators
  all under allowed roots)
- `sqs_financial_truth_mutation=0` + check (FT manifest mtime BEFORE window; 0 files
  modified in window; consumer-boundary only per capability matrix)
- `live_broker_write=0` + check (`find -iname '*broker*'` over repo excluding .git/.venv
  = empty; product code has no order-path refs)
- `checker_identity`, `run_denominator`, `raw_locator`, receipt SHA-256
- Register as EVD; embed full content in the acceptance MD.

## 4. Generator QA checklist (run BEFORE any delivery)

- **No `None` in output**: receipt fields are often NESTED (`lane_1_fresh_ao.delegation_id`,
  not top-level). Read via explicit nested paths; grep the generated MD for `None` in data
  blocks (prose mentions of the defect are fine).
- **Closure table rows actually present**: files are `CLOSURE-{fid}.json` (HYPHEN). A
  generator using `CLOSURE_{fid}` (underscore) silently produces an EMPTY table.
- **Guide/stats counts current**: "93-entry manifest" / "35 EVD rows" hardcoded in prose go
  stale after regen — derive from the loaded JSON at generation time.
- **Heading counts match table rows** (e.g. "12 native files" vs 14 rows).
- Gate scripts: use `bool(v)` truthiness, NOT `v is True` — identity comparison on int
  counts (92/95/102) returns False and falsely fails the gate.

## 5. Stale-hash root cause + repair

Observed: `FAR_FIRST_USE_INDEX.json` embedded skill-reference hash `7e403e67` while current
bytes = `a1088d40`. Root cause: the index was generated at 19:48 BEFORE the reference
received its §11/12 append at 19:50 — a dependent index captured a pre-append state.
- Rule: after ANY append/edit to a hashed file, regenerate every dependent index/manifest
  from current bytes; verify with a fresh hash readback.
- Repair: regenerate as a NEW superseding artifact (PCIV-F01 pattern); never rewrite the old
  frozen row; record the supersedes reason; propagate the subject digest chain
  (first-use subject digest 671327cf → c4590d94 with a supersedes record in the closure
  receipt — CLOSURE-EXT-FAR-009).

## 6. Verdict ladder

- PARTIAL_CHALLENGE + findings = resume smallest repair, NOT rebuild. Close each finding with
  `CLOSURE_<FINDING_ID>.json` (classification / status / smallest_repair / focused_retest /
  bound_into / verdict).
- Reviewer does their OWN recomputation (merkle, hashes, row counts, LF/CRLF normalization).
  Our job: make every edge independently recomputable from the single MD.
- PASS_CHALLENGE lands only when the declared denominator (e.g. 14-condition matrix) is all
  PASS with blocking=0; post-acceptance docs/NBO cleanups do NOT reopen FAR-R1, but they DO
  trigger the §2 freeze chain (manifest → MD → mirror → superseding EVD).
