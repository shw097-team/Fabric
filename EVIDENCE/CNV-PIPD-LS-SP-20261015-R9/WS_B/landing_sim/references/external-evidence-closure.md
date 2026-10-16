# External-challenge evidence closure (EVIDENCE_ONLY Contract A)

Verified 2026-08-12 on RP-002 v2.0 Stage-1: external reviewer returned
`PARTIAL_CHALLENGE` with 3 blocking `EVIDENCE_GAP` findings
(EXT-S1-EG-001/002/003) that were closed in one evidence-only round.

## When this applies

An external acceptance report returns `PARTIAL_CHALLENGE` (not PASS, not FAIL)
with findings classified `EVIDENCE_GAP` / `blocking_for_external_pass: true`,
plus a repair recipe like `RESUME_SMALLEST_REPAIR` / `EVIDENCE_ONLY_CLOSURE`.
Typical root causes: missing content digest on a claimed-frozen artifact, raw
receipt not delivered, artifact absent from the raw evidence index.

## Rules that govern the round

1. **Separate EVIDENCE_ONLY compiler contract.** Never merge closure work into
   the next stage's UPGRADE contract. Task id like
   `RP002-STAGE1-EVIDENCE-CLOSURE-CONTRACT-A-<date>`, `changeset.class =
   EVIDENCE_ONLY`, `product_mutation_allowed = false`, `tracked_mutation = false`.
   Compile with the same current local compiler; require PROMPT_COMPILE_PASS.
2. **Terminal** = `PENDING_STAGE1_EXTERNAL_META_ACCEPTANCE` (or the stage's own
   PENDING variant). Do NOT issue the seal, do NOT enter the next stage, do NOT
   rerun full gates unless a fresh digest check proves a specific edge stale.
3. **Focused retest per finding**, never a broad rerun. Reopen only the exact
   acceptance edge named by the finding.

## R1–R6 recipe (as practiced)

- **R1 — Tool/artifact matrix digest**: fresh-read file; parse; verify exact row
  count (35/35), unique capability IDs, required fields complete; compute
  SHA-256 from final bytes; bind digest into exact-set + review MD + raw index.
- **R2 — Contract exact-set digest**: fresh parse; verify required policy count
  (13), tool rows (35), KP rows (20), required G0/G1 evidence refs present, all
  hard_counts == 0; compute SHA-256; add to raw evidence index.
- **R3 — Raw independent checker receipt**: deliver the full machine-readable
  body (schema, checker identity, producer, checker-vs-producer separation,
  overlap evidence, every check with pass/fail + computed values + notes,
  verdict, isolation/no-write statement) plus its SHA-256. Hash+summary alone
  does NOT close this finding.
- **R4 — Regenerate review MD**: include closure receipts inline (§3 of the
  MD), bind all digests, then copy byte-identical to the mirror root; verify
  SHA256 equality across all copies.
- **R5** is the external reviewer's focused re-review (not local work).
- **R6** happens only AFTER external PASS: materialize the stage seal with the
  full content-addressed field set, generate the stage→next-stage handoff, STOP.

## Closure receipt shape (per finding)

```json
{
  "finding": "EXT-S1-EG-001",
  "classification": "EVIDENCE_GAP",
  "status": "CLOSED",
  "smallest_repair": "FRESH_HASH_READBACK_AND_INDEX_UPDATE",
  "focused_retest": {
    "file_exists": true, "parses": true,
    "row_count": 35, "required_row_count": 35, "row_count_exact": true,
    "unique_capability_ids": true, "required_fields_complete": true,
    "sha256_from_final_bytes": "<hex>"
  },
  "bound_into": ["STAGE1_CONTRACT_EXACT_SET.yaml", "review MD §11", "raw evidence index"],
  "verdict": "CLOSED"
}
```

## Freeze-order discipline (the drift bug we hit)

Symptom: review MD §raw-index embedded `fab4b137…` for
`INDEPENDENT_CHECKER_RECEIPT.json` but the file's current SHA was `e4401149…`.
Cause: the independent checker was re-run AFTER the review MD had already been
generated; the MD kept the stale embedded hash while the artifact bytes changed.

Correct order:
```text
1. freeze ALL mutable artifacts (receipts, checker output, checkpoint, closures)
2. regenerate the review MD LAST (it hashes everything, including checkpoint)
3. mirror byte-identical copies
4. hash all copies; require equality
5. do not touch any artifact after hashing
```
If the checkpoint itself must embed nothing about the MD (see next rule), the
MD's embedded checkpoint hash stays valid forever.

## Single-direction hash binding

Two artifacts that embed each other's hashes form a self-referential loop:
editing either breaks the other's binding. Convention:
- the **outer index** (external review MD) hashes every inner artifact;
- **inner artifacts** (RESUME_CHECKPOINT.yaml, receipts) reference the MD by
  PATH ONLY, never by its SHA.

## Pointer-file semantics (MASTER_REF case)

`MASTER_REF.yaml` is a pointer: its own file hash (`bc1ebc1b…`) and the
referenced Master content digest (`3bc4ad6c…`) are distinct by design. A checker
predicate requiring pointer-file self-hash == referenced digest is a wrong
predicate, not a defect. Adjudicate as semantic note; verify the referenced
digest against the referenced artifact's actual bytes instead.

## Verification pass after closure

Fresh readback of every closure fact (never trust maker output):
- mirror equality across all copies
- each CLOSURE_<id>.json exists with status CLOSED
- MD contains each fresh digest (tool matrix, exact-set, checker receipt)
- no "SHA MISSING" placeholder remains
- embedded digests == actual file digests (no drift)
- no secret-leak pattern in the MD (use `sk-[A-Za-z0-9_-]{20,}` etc., NOT bare
  `sk-` which false-positives on strings like `task-0`)

## R7 — Single acceptance MD delivery + evidence-MD generator self-checks (FAR, 2026-08-13)

When an external reviewer returns the finding class "declared native raw files were not
actually delivered as readable attachments" (EXT-FAR-R5-001), the fix is a **single
consolidated acceptance MD with FULL raw content embedded** — and the delivery-channel
reality determines the shape:

- **Delivery channel reality (verified by the reviewer this round):** `MEDIA:` attachments
  render as `[Open ...](#)` in the reviewer's environment and are NOT openable; local paths
  (e.g. `/mnt/data`, `C:\...`) are not visible to them. The ONLY readable channel is the
  message body itself. ZIP is explicitly NOT required; raw evidence IS required. Therefore:
  build ONE acceptance MD embedding the full raw content of every load-bearing edge — Q4/Q10
  receipts verbatim (JSON bodies), the complete crosswalk table (all 92 rows), the complete
  subject tree (all 95 relpath+sha rows so the reviewer can recompute the merkle digest), the
  full evidence-manifest entries, spine rows (WO/REQ/EVD), kanban snapshot text, test stdout +
  exit, mirror receipt, and all closure receipts — then present that MD's content inline.
  Model: `FAR_FINAL_ACCEPTANCE_EVIDENCE.md` (sha 55709e74…). No excerpts, no hash-only, no
  path dependencies. (Mirror the MD to the 3 roots anyway for the local record.)

- **Generator self-checks BEFORE delivering an evidence MD** (v2 defects the reviewer caught):
  1. grep the MD for `None` — reading a nested receipt field at top level
     (`.get("delegation_id")` when the field lives under `lane_1_fresh_ao`) silently emits
     `None` rows; always read from the exact nested path.
  2. count table rows with the actual row prefix (`grep -c '^| EXT-FAR-'`); a filename
     separator mismatch (`CLOSURE_{fid}.json` underscore vs actual `CLOSURE-{fid}.json`
     hyphen) silently empties the closure table — verify real filenames (`ls | grep CLOSURE`)
     before generating. Row-count predicates must also cover all IDs (a Python
     `count('| EXT-FAR-00')` matches 001–009 but not 010 — use a pattern covering every row).
  3. verify every embedded hash against current bytes. A stale embedded hash (index captured
     BEFORE a later edit to a hashed external file, e.g. a skill reference) must be refreshed
     in the PCIV-F01 superseding pattern: regenerate the index → regenerate dependent evidence
     MD(s) → recompute dependent subject-manifest digest → update closure receipts that embed
     it → regenerate the acceptance MD → re-mirror → re-hash. Record the superseded digest and
     reason in the manifest (`supersedes:` block) instead of silently replacing.
  4. pre-self-row rule applies to EVERY index file (not just the canonical artifact index):
     an index that includes its own entry has an unstable self-hash. Generate scope-precise
     indexes (exclude evidence-bundle/ and the index itself).
  5. full-field receipt updates: re-pointing a receipt to a new subject (v2→v3) means updating
     ALL fields (`mirror_locations`, freeze-order prose), not just `sha256`/`subject` — one
     stale path inside the receipt is itself a reviewer finding.
  6. `unittest` stdout capture (AO-FINDING-FAR-002): Python
     `subprocess.run(capture_output=True)` puts unittest output on **stderr**, leaving the
     named stdout evidence file empty (exit 0 + "OK" present in stderr). Capture merged output
     (`> file 2>&1` or combine streams) into the stdout evidence file; state the fix in the
     closure record.
  7. gate-check completeness before the freeze: an internal ALL-PASS gate that enumerates
     every CLOSURE-*.json (all 10) + verifies "no MISSING / no None / mirror equality" caught
     the missing EXT-FAR-007 closure receipt before delivery — run it, fix, then re-run the
     whole freeze chain (manifest → MD → mirror → hash).

## R8 — r6 round addendum: canonical single-hash audit, wrapper-exclusion, negative receipt (FAR, 2026-08-13)

After R7's single acceptance MD was delivered (sha 55709e74…), the next focused re-review
(r6) still blocked PASS_CHALLENGE on two EVIDENCE_ONLY findings. Their fixes are now the
hardened final steps:

### EXT-FAR-R6-001 — canonical single hash per path (stale-binding audit)

Before ANY final submission, every path must carry ONE current sha across ALL bindings
simultaneously: delivery-manifest table, evidence-manifest entries, spine EVD rows, and the
MD's embedded sections. Observed triple-identity defect: mirror receipt had
`1d564301…` (delivery) vs `94b04ab3…` (evidence manifest) vs `cde255d0…` (EVD row) — the
evidence manifest had been generated BEFORE later fixes to the receipt and closure-009.
Rules:
- never mutate an artifact after the evidence manifest is generated;
- if a later fix is unavoidable, re-run the FULL chain: fix artifact → regenerate evidence
  manifest from current bytes → regenerate wrapper MD → mirror → hash;
- register superseding EVD rows for EVERY regenerated/fixed artifact
  (EVD-FAR-EVIDENCE-MANIFEST-R2, EVD-FAR-MIRROR-R2, EVD-FAR-ACCEPTANCE-MD-R2/R3…);
- audit grep: `grep -c '<stale-hash>' <acceptance MD>` must be 0 for every superseded hash.

### Wrapper-MD / manifest self-exclusion (loop breaker)

If the acceptance MD embeds the evidence manifest's entries, the manifest MUST exclude the
wrapper MD itself (plus itself, pre-self-row) from its entries. Otherwise every MD regen
changes the manifest's content → changes the MD → infinite regeneration loop. Outer index
hashes inner artifacts; inner artifacts reference the outer by PATH ONLY. (FAR evidence
manifest excludes `FAR_FINAL_ACCEPTANCE_EVIDENCE.md`; the MD's own identity is carried by
its EVD row + delivery manifest, registered AFTER the spine capture.)

### EXT-FAR-R6-002 — negative side-effect receipt (final stop conditions 12–14)

Reviewers refuse summary-only negative claims ("= 0" in a claim ceiling is not proof).
Provide ONE compact subject-bound `<SCOPE>_NEGATIVE_SIDE_EFFECT_RECEIPT.json`:
- `subject_bound.subject_root_digest` = the FROZEN digest — do NOT regenerate the subject
  manifest for this (the receipt is an acceptance/evidence artifact; the digest stays valid);
- each negative edge = 0 WITH a deterministic check description + evidence locator:
  - unauthorized_side_effects: `find <product-paths> -newermt '<window-start>' -type f`
    returns EMPTY; evidence-manifest locators all inside allowed roots;
  - sqs_financial_truth_mutation: Financial-Truth marker mtime < window start
    (`stat -c '%y'`); product paths show zero window modifications;
  - live_broker_write: `find <repo> -iname '*broker*'` (excluding .git/.venv) is EMPTY;
    product code has no order-path references;
- checker_identity, run_denominator (WO ids/states, test counts, canary runs), raw_locator,
  generated_at_utc. Embed the receipt's full JSON in the acceptance MD (§10A) and register
  EVD-FAR-NEG-SIDE-EFFECT.

### Verifier-script identity trap

`all(v is True for ...)` is FALSE for int counts (`92 is True` → False) — a count-valued
gate check prints all-True lines yet reports ALL_PASS=False, sending you on a phantom-defect
hunt. Use truthiness or explicit equality (`all(bool(v)...) and rows == <expected>`).

### Spine-capture vs EVD self-registration timing

The spine readback embedded in the MD is a point-in-time snapshot; the acceptance MD's own
EVD row is registered AFTER the capture (self-registration), so the embedded EVD count is
N-1 vs current. State this explicitly in the MD (§7 note) instead of re-capturing forever —
re-capturing creates an infinite chase (each regen registers another EVD).

## Raw-log regeneration, frozen-subject completeness, and the handover bundle

- **Regenerating raw logs must NOT clobber sibling artifacts.** If you `rmtree` the evidence
  output dir and re-run the log generator, every non-log artifact already written there
  (adjudication JSON, closure projection, checker receipt) is DELETED. A fresh reviewer then
  reports a false `EVIDENCE_GAP` for a file that genuinely existed when first produced. Either
  regenerate logs into the dir WITHOUT deleting siblings, or re-run the ENTIRE artifact set
  after any rmtree.
- **Frozen-subject completeness check before you freeze.** Enumerate the files the reviewer's
  checklist names and assert each exists in the exact evidence commit
  (`git show <evc>:<path>` / `git ls-tree -r <evc>`). A file present on disk but absent from the
  commit (or committed but regenerated since) is the failure mode above.
- **The handover bundle ships the INPUTS, not just the outputs.** A compiled prompt + compiler
  receipt is not independently auditable without the compiler CONTRACT bytes; a sha256 in the
  repo for the contract is not enough. Ship as support artifacts: the contract JSON, a compiler
  bundle manifest (sha256+bytes of every bundle file), the duplication source, and the repro
  scripts (log generator, manifest generator, handover-MD generator).
- **Oversized / unreproducible inputs: withhold by rule, disclose honestly.** A multi-hundred-MB
  state db is not publishable. Do not silently omit it: state the withholding reason (size /
  no-content-value for this edge — NOT secrecy), give an alternate verification path (schema
  fingerprint sha256 + the projection artifact that reproduces the edge), and keep it OUT of the
  acceptance-subject commit.
- **Support-artifact placement.** Put handover/repro bundles in a SEPARATE top-level path
  (e.g. `acceptance/handover/<round>/`) as their own `NON_SUBJECT_POINTER_ONLY` support commit,
  so the immutable evidence-subject commit's tree stays byte-stable and its Return Pack is never
  touched post-freeze. The readset should declare later branch commits are non-subject pointers.
