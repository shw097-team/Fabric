## Step 6D — EVIDENCE CLOSURE PIPELINE: machine-generated, freeze-order-enforced (FAR self-evolution 2026-08-14, RR4 root-cause)

**WHY (FAR root-cause, 4 external rounds, 0 product defects):** FDA external reviews
failed 4× on evidence-lifecycle defects only. Recurring root causes (never product):
A. freeze-order violation (mutation after reducer rendered) — r1/r3/r4
B. denominator management (old values not marked historical) — r1/r3/r4
C. hand-written reducer tables vs machine manifest mismatch — r1..r4
D. raw bundle never actually submitted to the reviewer — r1..r4 (ALL FOUR)
E. subject-root drift after folder reorg (no rebind) — r2/r3/r4

**MANDATORY PIPELINE (one pass, no mutation after Final):**
```
Track A  freeze: complete ALL folder moves FIRST → verify FDA tree clean
                  (git status --short <team>/ <evidence>/ == empty) → freeze HEAD
Track B  manifest: regenerate EvidenceManifest FROM FINAL PATHS (every row = exactly
                  ONE filesystem path; NO grouped rows); exact counters:
                  manifest_row_count == payload_file_count; bundle_file_count;
                  reducer_in_manifest=false; manifest_self_entry=false
Track C  checker: run independent_checker EXACTLY ONCE on final HEAD → ONE current
                  denominator; mark ALL prior denominators HISTORICAL + subject-bound
                  (144/174/175/176 style) in checker_history
Track D  reducer: render final evidence MD LAST from machine outputs (manifest rows +
                  checker receipt); never hand-write artifact tables
Track E  submit: mirror byte-identical → readback → commit → UPLOAD raw bundle
                  (reducer + manifest + bundle files) — D is the one that failed 4×
```

**HARD RULES (learned from RR4):**
1. NO candidate mutation after the reducer is rendered (folder moves, path patches,
   checker patches = Track A, before Track B).
2. Loop-free single-direction binding: reducer embeds manifest sha; manifest NEVER
   records reducer sha and never lists reducer/itself (verified: reducer update does
   not change manifest sha).
3. Every manifest row = exactly one filesystem path (grouped rows are a confirmed
   defect, RR4-002).
4. One current checker denominator ONLY; all older counts labeled HISTORICAL +
   superseded_by (RR4-001).
5. Raw bundle MUST be part of the submission (zip or attached) — referencing paths is
   an evidence gap every single round (RR4-004).
6. Two-commit model: artifacts freeze commit (subject_root) + evidence packaging
   commit; both exist and are readback-able; reducer embeds the artifacts commit.
Full recipe: `references/external-rereview-normalization-rebind.md` (RR3+RR4 sections).
## POST-SEAL AMENDMENT WHEN AN AO RETURNS PARTIAL (learned 2026-08-20, WO-HGK-CODEX-COLLAB-001 — 3-round AO dance)

A fresh-context independent AO can (and should) return PARTIAL even after the maker thinks a round
is closed. Two real governance gaps were caught this way in back-to-back rounds; both are
**evidence-lifecycle**, not product. The recurring discipline when you must EDIT the sealed evidence
MD to answer an AO finding:

1. **Every edit re-hashes the MD — re-mirror ALL THREE roots AND re-bind the spine evidence hash.**
   `register_evidence` is UNIQUE on evidence_id, so re-binding means UPDATE the `evidence_refs` row
   (crafted `sha256=` to the new on-disk hash), NOT re-registering. Round-2 PARTIAL happened exactly
   because only the HGK primary was edited while Fabric/SQS-THC kept the old bytes AND the spine
   evidence hash still pointed at the old version → §"byte-identical" claim became false. Fix order:
   edit primary → `sha256sum` → cp to the other 2 roots → UPDATE spine `evidence_refs.sha256` →
   verify on-disk hash == spine hash == all 3 mirrors.
2. **Never write "→ PASS" into the MD before the AO actually verifies.** Writing
   `ACCEPTANCE_OFFICER_VERDICT = PASS` preemptively (or "三輪後 PASS") is premature self-assertion —
   the exact self-approval the user forbids (COV-11-06). Write the AO's REAL verdict (PARTIAL +
   finding + your fix) at the level you've actually reached; leave a forward pointer ("final AO verdict
   see §N") and fill it in only after the independent AO returns. Round-1 PARTIAL was partly caused by
   a premature PASS claim in the MD + a WO-state field the recorder had already advanced.
3. **Sequence the AO to actually run:** when you claim "re-verified → PASS", dispatch a real
   fresh-context AO lane for it — never self-report it. This session ran 3 rounds (PARTIAL → fix →
   PARTIAL → fix → PASS), each AO `read-only`/`mode=ro`, each catching a real gap.
4. **AO may hash a different algo than you:** one AO verified mirrors with `md5sum` (`9d4d21f7…`)
   while the maker used `sha256sum` (`47314f04…`) — same bytes, different algorithm, NOT a mismatch.
   Before treating an AO hash difference as a defect, check it's the same bytes under both algos
   (and that the spine bound the ON-DISK hash, which is the authoritative value).
5. **Resolve "CREATED vs VERIFIED" honestly:** `record_workorder_result` (WO CREATED→VERIFIED) is a
   standard closure step, but if it runs mid-AO-window the AO will flag "state not frozen for review."
   It's a legit workflow note, not fraud — document the closure step + timestamp in the MD (§9-style)
   so the next AO round can promote, rather than deleting the record.

Pattern after a PARTIAL: fix → re-mirror+re-bind → update MD verdict text to actual → re-run AO →
record PASS in §N only after AO returns. This is the evidence-side twin of Step 6D's freeze rules for
post-seal amendments.

## EXTERNAL SUBMISSION GATES (2026-08-14, external 5-defect root-cause): machine preflight
(`var/fda/hgk_evidence_preflight.py`, PASS=precondition) + one-time regeneration (manifest from
scratch, old receipts status=HISTORICAL in body) + CLOSED authority gate (receipt cited by path).
Full: `references/external-submission-gates.md`.
**OVERSIZED SKILL ROUTE (2026-08-14, FAR-on-FAR):** SKILL >100KB → split+route FIRST (mechanical
splitter, never hand-slim); if unsplittable → GUARDED SLIM only: `scripts/skill_guard.py <dir> pre|post`
+ content-grep test + pre/post compare, ALL PASS before release. Full:
`references/oversized-skill-handling-route.md`.
**TRIGGER (hard route):** every time an internal acceptance round completes and the
next step is external review, you MUST automatically consolidate ALL external-review
evidence into ONE single evidence MD that embeds full raw content. Do not wait to be
asked; do not deliver pointer/index-style MDs to an external reviewer.

**Why (verified twice by external reviews):**
- FAR R7/R8 rule: the external reviewer's environment CANNOT open MEDIA attachments
  or local paths — the message body / single MD is the ONLY readable channel.
- External r2 (EXT-FDA-RR2-001) failed exactly because the claimed final file was
  NOT the file the reviewer received, and the submitted MD was pointer-rich
  (referenced SensorLog paths / receipt filenames instead of embedding raw bodies).

**MANDATORY ROUTE (single evidence MD = FULLY EMBEDDED, not pointers):**
1. **One file, one identity:** single final MD filename + sha256 in its header;
   the exact bytes you claim MUST be the bytes submitted (attachment identity check).
2. **Embed full raw bodies, not names:** every blocking receipt's CONTENT inline
   (checker verdict + denominator + pass/fail; F01/F03/F06/F07/F09/F10/F11 receipts;
   UFO² effective-load; PAPER runtime SensorLog/SensorList raw extracts; DoD-36 rows;
   claim ceiling; artifact hash table). External reviewer never opens a path.
3. **Single-valued truth:** one current value per state (UFO² / PAPER / checker
   denominator / subject root / artifact counts) — no stale superseded prose
   (Track A normalization; label old counts SUPERSEDED_PRE_<PATCH>).
4-5. Freeze order + no-append-after-manifest: see HARD RULES 1-6 below + gates 7-9 (references/external-submission-gates.md).

**Execution tooling:** `pack_external_single_md.py` (in this skill's references/ or
`var/fda/`) reads EvidenceManifest + receipts + runtime DBs and emits ONE
self-contained MD with all raw bodies inlined. Run it automatically at the
internal→external handoff boundary.

Full recipe: `references/external-single-md-mandatory-route.md`.

1. Render ONE master evidence payload (sections A..L per the acceptance contract) to a
   temp file. Do NOT embed the file's own final SHA in its body (self-referential hash loop).
2. Run a deterministic read-only independent checker (fresh readback of every fact, never
   trusting maker output; keep it in gitignored `var/a2/`).
3. `cp` the exact same bytes to `HGK\evidence\review\`, `SQS\evidence\review\`,
   `Fabric\evidence\review\` (same filename). Compute SHA-256 at all three locations;
   require equality. Do not edit any copy after hashing.
4. Mirror any dedicated checker/canary receipts too (HGK+SQS each pair with a Fabric copy).
5. Final response carries the hash; STOP, wait for external acceptance.

