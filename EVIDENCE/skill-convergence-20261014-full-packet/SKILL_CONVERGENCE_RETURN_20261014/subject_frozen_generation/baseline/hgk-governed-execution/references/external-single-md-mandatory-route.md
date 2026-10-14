# External Single-MD Mandatory Route (Step 6C) — full recipe

外部驗收證據提交：**單一 evidence MD = FULLY EMBEDDED，不是 pointers**（2026-08-14 user-mandated）。

## Why (verified twice by external reviews)
- FAR R7/R8 rule: the external reviewer's environment CANNOT open MEDIA attachments
  or local paths — the message body / single MD is the ONLY readable channel.
- External r2 (EXT-FDA-RR2-001) failed exactly because the claimed final file was
  NOT the file the reviewer received, and the submitted MD was pointer-rich
  (referenced SensorLog paths / receipt filenames instead of embedding raw bodies).

## MANDATORY ROUTE

1. **One file, one identity:** single final MD filename + sha256 in its header;
   the exact bytes you claim MUST be the bytes submitted (attachment identity check).
2. **Embed full raw bodies, not names:** every blocking receipt's CONTENT inline
   (checker verdict + denominator + pass/fail; F01/F03/F06/F07/F09/F10/F11 receipts;
   UFO² effective-load; PAPER runtime SensorLog/SensorList raw extracts; DoD-36 rows;
   claim ceiling; artifact hash table). External reviewer never opens a path.
3. **Single-valued truth:** one current value per state (UFO² / PAPER / checker
   denominator / subject root / artifact counts) — no stale superseded prose
   (Track A normalization; label old counts SUPERSEDED_PRE_<PATCH>).
4. **Freeze order:** freeze HEAD → freeze receipts → freeze tests → fresh checker →
   SubjectManifest → EvidenceManifest → render final MD LAST → mirror byte-identical
   → readback receipt → submit exact bytes.
5. **Never append a ChangeSet after manifest regeneration.**

## Execution tooling
`pack_external_single_md.py` (in this skill's references/ or var/fda/) reads
EvidenceManifest + receipts + runtime DBs and emits ONE self-contained MD with all
raw bodies inlined. Run it automatically at the internal→external handoff boundary.

## Master payload steps (per acceptance contract)

1. Render ONE master evidence payload (sections A..L per the acceptance contract) to a
   temp file. Do NOT embed the file's own final SHA in its body (self-referential hash loop).
2. Run a deterministic read-only independent checker (fresh readback of every fact, never
   trusting maker output; keep it in gitignored `var/a2/`).
3. `cp` the exact same bytes to `HGK\evidence\review\`, `SQS\evidence\review\`,
   `Fabric\evidence\review\` (same filename). Compute SHA-256 at all three locations;
   require equality. Do not edit any copy after hashing.
