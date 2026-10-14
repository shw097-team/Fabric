# External-challenge evidence closure round (FAR EXT-FAR-001..010, verified 2026-08-13)

Extends `external-evidence-closure.md` (R1–R6) with the full EVIDENCE_ONLY closure
round as practiced on the FAR external PARTIAL_CHALLENGE. An external reviewer returns
findings classified EVIDENCE_GAP / CONFIRMED_DEFECT with
`RESUME_SMALLEST_REPAIR / EVIDENCE_ONLY_CLOSURE`; the maker must rebind + repackage raw
evidence, never rebuild product. Verified: FAR review findings EXT-FAR-001..010 all
closed in one round; focused re-review packet materialized as a single zip.

## The 8 closure workstreams (what the reviewer actually demands)

1. **Exact subject root** — `FAR_SUBJECT_ROOT_MANIFEST.json`: tree of
   `(relative_path + file_sha256)` over the implementation surface ONLY (exclude
   evidence-bundle, manifests, MDs, AO/closure receipts — those live under the
   evidence root); `subject_root_digest` = sha256 over sorted payload. The fresh AO
   lane must be able to RECOMPUTE this digest independently.
2. **Evidence manifest root** — `FAR_EVIDENCE_MANIFEST.json`: every raw entry with
   file_sha256 + role; **excludes itself** (pre-self-row rule) or its hash changes on
   every regen.
3. **Raw review bundle** — `evidence-bundle/`: raw-tests (see stderr trap below),
   raw-spine (fresh sqlite readback: WOs/REQs/TS/EVT/EVD/result_json), raw-kanban
   (final snapshots per board), raw-receipts (copies), raw-canary (run artifacts).
4. **Closure receipt per finding** — `CLOSURE-<FINDING_ID>.json` with
   classification / status CLOSED / smallest_repair / focused_retest predicates /
   bound_into / verdict. **Filenames use HYPHEN** (`CLOSURE-EXT-FAR-001.json`) —
   an underscore in the generator silently produces an empty closure table.
5. **Fresh AO for Q10** — blueprint requires fresh AO + blockers=0, NOT swarm
   agreement. Lane must be subject-bound (recompute merkle digest), maker-separated,
   no-write; Swarm/challenger evidence is input, never the final receipt.
6. **Real-invocation receipt (Q4-class)** — execute the pinned method workflow on a
   REAL local corpus (network DENY per WorkOrder), record method identity
   (commit + skill sha), input, execution trace, output digest; state
   `no_meta_apply_authority_import: true` and `reviewer_not_ao: true`.
7. **Regression crosswalk** — map every T0xxx predicate → exact evidence locator
   (92 rows for FAR); blocking contradiction must be 0.
8. **Post-freeze separate ChangeSets** — a later dogfood/self-upgrade round
   (e.g. FAR_FIRST_USE) is a SEPARATE subject with its own manifest digest; never
   absorb it into the older frozen core subject without explicit rebind.

## Evidence-MD generator hygiene (the three defects the reviewer caught)

1. **`None` in the generated MD** — reading NESTED receipt fields with top-level
   `.get()` (e.g. `ao.get("delegation_id")` when the id lives under
   `ao["lane_1_fresh_ao"]["delegation_id"]`) emits the literal string `None` into
   the evidence MD. **Always grep the generated MD for `None` before mirroring.**
   Materialize the full post-repair chain (lane1 FAIL → finding → repair → lane2
   PASS → final blockers=0), never a bare summary.
2. **Empty table from filename mismatch** — generator wrote
   `f"CLOSURE_{fid}.json"` (underscore) while files were `CLOSURE-{fid}.json`
   (hyphen) → 0-row closure table with no error. **Verify table row count ==
   expected denominator** after generation (`grep -c '^| EXT-FAR-'`).
3. **0-byte stdout evidence file** — `unittest` writes its output to STDERR;
   `subprocess.run(capture_output=True)` then writing only `r.stdout` produces an
   empty stdout evidence file (AO-FINDING-FAR-002). Capture merged output:
   `python -m unittest discover -s tests -t . > stdout.txt 2>&1` (+ append EXIT).
   A fresh AO lane WILL flag the 0-byte file; the fix is regenerating with merged
   capture, then a focused retest lane.

## Freeze order (drift-proof, as verified)

```text
1. complete ALL mutations (closures, receipts, gates receipt regen)
2. regenerate evidence manifest LAST among mutable artifacts (any receipt regen
   desyncs hashes embedded earlier)
3. register superseding EVD rows for regenerated receipts (EVD-*-R2 pattern)
4. generate the evidence MD LAST (read hashes FROM manifests — no transcription)
5. mirror byte-identical to HGK/Fabric/SQS evidence\review, hash all copies, require equality
6. no edits after hashing; MD never embeds its own hash (single-direction binding:
   MD references mirror-receipt by path; receipt carries MD hash)
```

## Package the focused re-review packet

A single zip (`FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`) containing bundle + manifests +
closure receipts + evidence MD + mirror receipt, with a package receipt carrying the
zip sha256 (single-direction). The external reviewer's focused re-review then checks
~14 conditions (subject root, manifest root, bundle hashes, MD consistency, Q4/Q10
receipts, crosswalk, EVD denominator, mirror readback, zero blockers).

## Kanban/execution surfaces still apply

Closure round still rides a kanban board (`far-external-closure`) + claim/complete;
remember `unset HERMES_DELEGATED_CHILD_CONTEXT` after every delegate_task batch
(re-set on each batch; blocks kanban CLI).
