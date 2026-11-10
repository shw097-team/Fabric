# FHS workspace hygiene — 2026-11-10 (candidate record)

**Claim ceiling: CANDIDATE / LOCAL_MEASURED. Not merged, not CI-verified, not a native reader result,
not an HGK admission, not a release.** This file records a bounded local workspace-hygiene round and the
numbers that round actually measured. It is published as a PR candidate; `main` was not written.

## Scope

| field | value |
|---|---|
| control package | `FHS-WORKSPACE-HYGIENE-THIN-CONTROL-20261110` r1, sha256 `19ff3edf3dc13f1912e479a2174a6cd85020f65f570f0e76b4ae02ae5c32aade` |
| mode | same-volume native MOVE only (no COPY / ZIP / TAR / large staging) |
| workspace root | local engineering workspace named `FHS` (absolute path intentionally not published) |
| archive root | sibling of the workspace root on the **same volume** (device-id equality asserted before the first MOVE) |
| executing runtime | local Hermes gateway `0.23.0` @ `786a3156d1db06bd9fc014c014cea4c8023653fd` (`v0.23.0-1-g786a3156d1`), read from the gateway's own state file and cross-checked against `git rev-parse HEAD` in the code root |
| identity drift noted | the control package states `0.23.3`; the serving runtime measured `0.23.0`. The measured value is used; the document was not treated as host proof. |

## What was measured

| metric | value |
|---|---|
| files enumerated pre-move (read-only streaming walk, `.git` internals aggregated) | 1,320,623 files + 290,342 aggregated `.git` entries, 318,923 directories |
| bytes enumerated pre-move | 62.45 GiB |
| paths refused by ACL during the pre-move walk | 3,739 (recorded, all held in place) |
| pre-move workspace size | 62.45 GiB |
| post-move workspace size | 18.07 GiB (335,974 files) |
| post-move archive size | 41.39 GiB (841,799 files) |
| MOVE operations attempted / succeeded / failed | 140 / 140 / 0 |
| bytes moved to the archive | 44.16 GiB (1,166,383 files) |
| trees whose post-move identity re-derived equal to the pre-move identity | 124 of 140 exactly; 13 of the 16 first-pass differences re-derived equal under pre-move scanning semantics (`\\?\` long paths + junction traversal); 3 remain **destination-superset** (see below) |
| regenerable cleanup (untracked `__pycache__` / `.pytest_cache`) | 14,644 files / 219.0 MiB removed, 1 tree(s) held on access-denied |
| archive volume free bytes before / after the round | 39,140,323,328 / 39,118,602,240 |

**Same-volume MOVE does not free capacity.** The workspace volume's free space is essentially unchanged by
this round by design: the archived originals still occupy the same volume until the user moves the archive
directory to the external volume. Any statement that this round "reclaimed" that space would be false.

### Identity readback, stated precisely

A single rename per tree is atomic, so a destination can be equal to, but not smaller than, the source.
The first readback pass used `os.walk` + `os.stat`, which cannot stat paths beyond `MAX_PATH` and does not
descend junction/reparse subtrees; the pre-move inventory used `os.scandir`, which did descend them and
recorded **3,739 path refusals**. Re-deriving the 16 differing trees with pre-move semantics gives:

- 13 trees exactly equal (files **and** bytes);
- 3 trees where the destination holds **more** entries than the pre-move inventory recorded — that is the
  direction a rename cannot produce by itself, and it matches the paths the pre-scan could not stat:

| tree | pre-move inventory | post-move readback | delta | entries missing at destination |
|---|---|---|---|---|
| `SBL/_handover` | 335,291 | 351,057 | +15,766 | 0 |
| `var` | 285,889 | 285,901 | +12 | 0 |
| `wg` | 37,162 | 37,168 | +6 | 0 |

No tree is smaller than its pre-move measurement, and no entry recorded before the move is absent after it.
The claim this supports is therefore narrow and exact: **the archive holds at least everything the pre-move
inventory saw, and never less** — not "the two numbers are identical for all 140 trees".

## Disposition histogram (one class per candidate, no overlaps)

| disposition | items | files | GiB |
|---|---|---|---|
| `ARCHIVE_ELIGIBLE` | 140 | 1,157,724 | 43.4 |
| `ACTIVE_LOCKED` | 3 | 1,041,239 | 37.99 |
| `UNCLASSIFIED_EXPORTABLE` | 4 | 8,663 | 0.75 |
| `HOLD_IN_PLACE` | 3 | 3,837 | 0.12 |
| `CURRENT_KEEP` | 7 | 1,241 | 0.03 |

Classification rules actually applied:

1. A candidate is `ACTIVE_LOCKED` if it is a git work tree holding tracked content, `.git`, a registered
   worktree, a stash or unpushed commits. Tracked content is never removed from a work tree.
2. Inside those work trees only **untracked** sub-trees were candidates, and only when no tracked file in
   the same repository referenced that sub-tree by relative path (`git grep -l -F '<name>/' HEAD` = 0).
   Any count above 0 became `HOLD_IN_PLACE`.
3. No tracked file in any of the three repositories references the workspace root by absolute path
   (measured: 0 files), so the workspace-level trees have no in-repo consumer path.
4. `HOLD_IN_PLACE` is used for: signed/acceptance surfaces still in force, receipt stores, SQLite registry
   and its rollback backups, ACL-refused subtrees, git-tracked or git-modified files, and any tree whose
   consumption could not be bounded this round.

## Held in place (named, not cleared)

| tree | reason |
|---|---|
| `hgkrcpt` | receipt store (3,702 files, 2 .pem) - Reader/receipt originals; consumer proof not available this round |
| `_handover` | ROOT-level handover with receipts/snapshot; consumer proof not available this round |
| `verdict` | empty dir, no content to move (0 files) |
| `SBL/PIPD` | nested clone of the PIPD canonical-writer location, 8 tracked references, own worktrees |
| `SBL/_sbl_src_mirror`, `SBL/_sbl_r4`, `SBL/_sbl_verify`, `SBL/_sbl_checker_env`, `SBL/_sbl_round_artifacts`, `SBL/_sbl_release_011rc1`, `SBL/_sbl_r9_candidate` | referenced by tracked SBL files (1–23 refs each) |
| `SBL/evidence/compiler/*.stdout.txt`, `SBL/contracts/compiled/thin-prompt.md` | git-tracked and modified in the work tree — never removed |
| `HG-KSEOS/var/shared-spine` | the live Shared Spine registry database (+ WAL/SHM) |
| `HG-KSEOS/var/backups` | rollback / pre-image database material (2.3 GiB) |
| `HG-KSEOS/var/far-lane-sod-003` (4.6 GiB), `HG-KSEOS/var/workbench`, `HG-KSEOS/var/hgk-solution-apply-20261012`, `HG-KSEOS/var/LANE-ENFORCEMENT-APPLY-20261015`, `HG-KSEOS/var/opencodex-backup`, `HG-KSEOS/var/hermes-disposable` | referenced by tracked HG-KSEOS files (2–8 refs each) |
| `HG-KSEOS/worktrees`, `HG-KSEOS/fhs_msc_handoff_20261030` | 31 and 32 tracked references |
| `Fabric` untracked working material (`stage/`, `Fabric-rebind-publish/`, `fabric-autonomous-research/`) | belongs to the current Fabric branch |
| 3,739 ACL-refused paths (mostly HG-KSEOS checker scratch) | not readable, therefore not provably safe to move |

HOLD is a result, not a failure. Nothing was force-cleared to make the round look complete.

## What this record does not claim

- Not a re-run of any wave work package, gate, quorum, owner ACK or signature.
- Not an assertion that the archived material is unreferenced for all time — only that no consumer path
  was found by the checks above, and that the originals are preserved.
- Not a statement about the external archive volume: moving the archive off this volume is the user's step,
  and no external-volume verification happened here.
