# External Focused Re-Review Repair: Track A Normalization + Track B Subject Rebind

## RR3 extension (evidence packaging closure, verified 2026-08-14, EXT-FDA-RR3)

Third FAIL_CHALLENGE round added these rules:

**Loop-free single-direction binding (THE key fix):** evidence MD embeds the final
manifest sha256; the manifest NEVER records the MD's sha and never lists the MD or
itself as a row → updating the MD does NOT change the manifest sha (verified: MD
update kept manifest sha stable). Reviewer recomputes MD sha from submitted bytes.
`evidence_reducer_sha256` inside a manifest = self-referential trap → never emit it.

**Exact-set contract (RR3-002) — unambiguous and rehashable:**
```
payload_entries   = manifest rows (evidence payload; EXCLUDES manifest itself AND evidence MD)
manifest_entries  = payload_entries + 1 (the manifest JSON physically present, not self-listed)
bundle_files      = physical recursive file count in the bundle dir
self_entry_policy = manifest excludes itself AND the evidence reducer MD (loop breaker);
                    MD references manifest by sha256 (single direction)
```
Folder reorgs silently desync the bundle: after ANY reorg, re-sync EVERY file
(root + DOC/ + tests/ + evidence/receipts/ + governance/) into the bundle, then
regenerate the manifest — 10 receipts went missing during the FDA reorg (RR3-003).
`find <dir> -name "<file>"` before assuming where a file lives (guide ended up in DOC/).

**Timestamp labeling (RR3-004):** `generated_at_utc` must be real UTC
(`datetime.now(timezone.utc)`); a +12h future value = UTC/local labeling error;
or name the field `generated_at_local` with +08:00.

**Placeholder rule:** `<REBOUND_MANIFEST_SHA>`-style placeholders are BLOCKING —
final manifest sha must be real 64-hex; `grep -c` for the placeholder before freeze.


Verified 2026-08-14 on FDA (external focused re-review r2 → FAIL_CHALLENGE with
EXT-FDA-RR2-001..008 → smallest repair → re-submission package).

## When this applies

An external challenge review came back FAIL_CHALLENGE (not PARTIAL) because the
submitted evidence itself carries **deterministic contradictions** — multiple
final-state values for the same truth, mixed lineage roots, ambiguous
denominators. The fix is NOT a product rebuild and NOT a broad rerun — it is a
two-track evidence-only repair.

## The 6 contradiction classes that trigger FAIL (all seen in one file)

1. **Evidence identity mismatch** — claimed final file/hash ≠ bytes actually
   submitted (HERMES claimed `FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md`
   f9606a61; reviewer received `FDA_IMPLEMENTATION_EVIDENCE(1).md` fdb0bfcf).
   This is a hard identity gate failure: the exact bytes the reviewer receives
   MUST be the exact bytes you claim. Verify the actual attachment, not what you
   generated.
2. **Single truth, multiple values** — same file says UFO² `QUALIFIED 7/7` AND
   `BLOCKED_HITL` AND `runtime not installed`; PAPER runtime `pending` AND
   `PASS` AND `BLOCKED_SUBSCRIPTION`. Old prose from earlier rounds was never
   removed when the state flipped.
3. **Checker denominator conflict** — `144 single current` and `174/174 current`
   in the same document. Only ONE current denominator may exist; older values
   must be explicitly labeled `SUPERSEDED_PRE_<PATCH>`.
4. **Subject lineage mixing** — 72cb450 / fa192ab / 1308eb1 all referenced as
   "the root" without a single post-patch rebind. Old roots are history; one
   current frozen root must bind everything.
5. **Ambiguous artifact denominators** — 40 vs 42 vs 52 vs 53 with no scope
   names. Every count needs an explicit scope label
   (`manifest_entry_count` / `evidence_md_artifact_rows` / `external_bundle_count`).
6. **Over-generalized qualification claims** — FN01 10/10 + FN03 locate 1/1
   promoted as "pywinauto first-choice for ALL MFC/Afx actions". Qualification
   is per action-class; a locate-only result never covers invoke.

## Track A — Final Evidence Reducer Normalization

Goal: ONE file, ONE value per truth, no stale superseded prose.

1. Rewrite the evidence MD fresh (write_file full replacement, not patch —
   patches leave old lines behind).
2. For every state pick the single current value from the LATEST raw receipt and
   delete all superseded variants (grep for them afterwards; 0 hits required).
3. Define artifact denominators with explicit scope names in one block.
4. Mark old checker counts `SUPERSEDED_PRE_<PATCH>` inline where they must be
   mentioned; better: don't mention them at all.
5. Narrow any qualification claim to exactly the rows actually qualified.
6. Verify with `grep -c "BLOCKED_HITL\|BLOCKED_SUBSCRIPTION\|not executed\|144 single\|<old-root-hash>"` → 0.

## Track B — Post-Patch Final Subject Rebind (strict order)

Order is a contract; the reviewer explicitly requires "no ChangeSet appended
after manifest regeneration".

```
1.  freeze final post-patch HEAD        (git rev-parse HEAD)
2.  freeze raw runtime receipts          (DB extracts, fixture receipts)
3.  freeze affected tests                (run them, record count)
4.  run ONE fresh checker                (single current denominator)
5.  create/update SubjectManifest        (subject_root = frozen HEAD, single)
6.  create/update EvidenceManifest       (rehash ALL rows from bundle bytes,
                                         0 missing, 0 hash mismatch)
7.  render the final evidence MD LAST    (after ALL facts frozen)
8.  mirror byte-identical               (evidence MD 4-way, re-review MD 3-way)
9.  generate mirror readback receipt     (hashes + equality flags)
10. submit the EXACT bytes + raw bundle  (hash in the header must match the file)
```

Pitfalls verified:

- **Manifest before final MD = drift bug.** Any generator/checker run after the
  review MD was generated desyncs embedded hashes. EvidenceManifest is
  regenerated BEFORE rendering the final MD, never after.
- **Rehash from bundle bytes, not from workspace copies.** Copy artifacts into
  the raw bundle first, then hash what is physically in the bundle; verify every
  manifest row resolves to an existing bundle file (missing rows are FAILs).
- **The add-success/notice dialog can masquerade as something innocent**
  (XQ's `時間：[HH:MM:SS]` dialog is a strategy-add-success notice; it sits above
  the radar and swallows coordinate clicks). On ANY anomaly, run the
  screen-state check first (see fda-desktop-automation-cua.md §15) — do not
  retry blindly.
- **SensorLog is the execution truth, not the radar grid.** XQ radar grid
  (MFCGridCtrl 17001/17002) is UIA-invisible; the authoritative runtime evidence
  is `DAQXQLITE_SHW097_SensorLog.sqlite` Table_YYYYMMDD (columns AND values are
  CP950 bytes — decode both; `dict(zip(cols,row))` keys must be str). State
  machine: XSSensorState 2(executing)→3(calc)→1(done), ExecState 1→8,
  SymbolID=2330.TW, TriggerTime=HHMMSS. Full detail:
  `references/xq-radar-paper-runtime.md`.
- **Keep `FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED`** until the external verdict;
  the repair package is SUBMITTED, not self-approved.

## RR4-RR6 extensions (raw-edge closure, verified 2026-08-14, EXT-FDA-RR4/RR5/RR6)

After the reducer is normalized, the reviewer goes after the RAW edges. Lessons:

**RR4 (FAIL):** reducer itself must be machine-generated LAST with exact counters
`manifest_row_count == payload_file_count` (every row = exactly one filesystem path —
grouped/abbreviated rows are a confirmed defect), `bundle_file_count`,
`reducer_in_manifest=false`, `manifest_self_entry=false`. ONE current checker
denominator only; ALL older counts (144/174/175/176…) labeled HISTORICAL +
superseded_by in a `checker_history` array. Two-commit model: artifacts-freeze
commit (subject_root) + evidence-packaging commit; both must exist and be
readback-able; the reducer embeds the artifacts commit. Run checker EXACTLY ONCE on
the frozen tree, then render reducer; NO mutation after Final.

**RR5 → PARTIAL (progress):** when only raw delivery is missing, the verdict
improves from FAIL to PARTIAL. Deliver a single fully-embedded raw MD with the
minimum external set: manifest full body, checker raw stdout, UFO² receipt, PAPER
runtime receipt, SensorLog/SensorList raw extract, wrong/silent-wrong receipts,
broker_write=0 negative, git subject readback.

**RR6 → FAIL again — the raw-edge traps that reopen closure:**

1. **Stale-subject receipt trap (RR6-001):** the F01 receipt bound XQ **3.18.02/260102**
   while the final subject is **3.20.02/260811** — old-build 10/10 does NOT close the
   current-build action class (build drift → requalify). Before embedding any receipt,
   check its `target.product_version`/window-title readback against the final subject.
   A current-build receipt already existed (`FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json`
   FN01 260811 10/10) — look for it instead of re-running. Also: a receipt claiming
   `login_state=NOT_LOGGED_IN` while run titles show `SHW097:已登入` is
   receipt-local metadata contradiction — normalize target metadata.
2. **Row-count ≠ fresh-run denominator (RR6-002):** 56 SensorLog internal rows or 8
   ExecState=1 starts do NOT equal "10 fresh runs". DoD-17 needs explicit run_id
   1..10 per applicable action class with per-run readback. Never let log-row counts
   stand in for fresh-run denominators; embed the FULL extract (first-30-rows
   truncation was noted).
3. **Identical LastCompileTime proves nothing (RR6-003):** a "10-run" compile receipt
   whose ten `last_compile` values are byte-identical (same ms) cannot prove 10 fresh
   compiles. Each run needs a distinct invocation/readback (unique marker comment →
   LastCompileTime advances). XS editor must have a NAMED script for F6 to compile —
   see `references/xq-radar-paper-runtime.md` §9 for the full failure path.
4. **Truncated checker stdout is an EVIDENCE_GAP (RR6-004):** embedding only the
   tail (`stdout[-3000:]`) of the checker output is NOT a raw receipt — the reviewer
   needs the complete untruncated stdout (or a full JSON receipt) with the summary
   line. Capture the full output to a receipt file (full body embedded), not a slice.
5. **Self-hash mismatch inside the container (RR6-005, non-blocking):** a raw MD that
   embeds its own sha256 can't be stable — filling the header with the pre-fill hash
   guarantees a mismatch vs the final bytes. Either remove the self-hash or publish
   the container hash via sidecar/mirror receipt. Same rule as the reducer.
6. **Count wording (non-blocking):** "SensorList 6 strategies" where 6 = total rows
   but only 5 are FDA-created → say "total rows = 6, FDA-created = 5".

Focused-edge repair pattern (RR6 smallest legal repair): do NOT rebuild — patch only
the affected edges (current-build F01 receipt / F06 fresh compiles / PAPER explicit
10 runs / full checker stdout), then re-submit the single raw MD.

## Output shape

- Normalized evidence MD (single-valued, no stale prose) — 4-way mirror equal.
- Single re-review evidence artifact (exact filename + header hash = file hash) —
  3-way mirror equal.
- EvidenceManifest rehashed from bundle (entries count + sha256 in readback).
- Mirror readback receipt JSON with equality flags.
- One git commit freezing everything (subject_root = that commit).
