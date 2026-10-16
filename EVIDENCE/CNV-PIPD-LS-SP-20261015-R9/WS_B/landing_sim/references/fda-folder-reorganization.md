# FDA / FAR folder reorganization recipe (verified 2026-08-14, FDA folder tidy-up)

User request class: 「重新整理 <profile-team> 資料夾的目錄樹和檔案擺放,目前非常雜亂」.
Applies to fabric-desktop-automation (FDA) and fabric-autonomous-research (FAR) profile-team
folders. Same governance rules as the FAR folder reorg pitfall, with FDA-specific detail below.

## Classification (what stays at root vs moves)

| 留在 root | 移到 evidence/receipts/ | 移到 governance/ |
|---|---|---|
| TEAM.md (frozen identity) | 全部 `*_RECEIPT.json`（C0/C2/C3×2/C4/C5、F01/F03/F04/F06×10/F09/F09B/F10F11、XQ_*、BOUNDED_CONTROL_LIVE_PROBE） | FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml |
| FDA_DESKTOP_CAPABILITY_MATRIX.yaml (canonical routing truth) | | FDA_INTEROP_DISPOSITION.yaml |
| FDA_EXECUTION_BINDING.json | | FDA_ROUTE_CHECK.yaml |
| FDA_IMPLEMENTATION_EVIDENCE.md (evidence) | | FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml |
| FDA_USER_GUIDE.md (operability) | | |
| fda_router.py / fda_lease.py / xq_native_adapter.py (product code) | | |
| independent_checker.py + tests/ | | |
| WO_*.yaml (WorkOrder) | | |

Principle: root keeps anything the checker / external acceptance treats as an IDENTITY
(frozen artifacts, canonical matrix, binding, evidence MD) + product code + WO.
Move only pure evidence receipts and governance contracts — content unchanged → sha256 stable.

## Execution sequence (verified end-to-end)

1. **Snapshot hashes BEFORE move** (script): `{f: sha256} for all root files`.
2. **Move** via `shutil.move` into `evidence/receipts/` and `governance/`
   (`mkdir(parents=True, exist_ok=True)` — pathlib mkdir does NOT create multi-level parents).
3. **Verify hash stability**: for every snapshotted file, locate it in root or a subdir and
   compare sha256 — must be ALL OK. (git will show `rename ... (100%)` = zero-content-change proof.)
4. **Patch independent_checker.py paths**: every `FDA / "FILE"` for moved files becomes
   `FDA / "evidence/receipts/FILE"` or `FDA / "governance/FILE"`. Stale-root refs remaining
   after patching must be files that legitimately stay at root (matrix/binding) — verify each.
5. **Re-run checker** — expect PASS, checks count may grow (+1/+2 from new predicates).
6. **Update EvidenceManifest paths** (Fabric/evidence/review/FDA_RAW_REVIEW_BUNDLE/):
   for each artifact row whose basename is in the moved sets, rewrite `path` to the subdir
   form, then rehash ALL rows from bundle bytes (also physically move the bundle copies).
   Verify `missing rows: (none)`.
7. **Append reorg section to evidence MD** (§12 folder reorganization, keep it terse),
   write `FDA_FOLDER_REORGANIZATION_RECEIPT.json` (root_kept list, moved counts,
   content_unchanged_sha256_stable: true, checker_after, manifest sha, bound_into),
   generate `FDA_DIRECTORY_TREE.txt` (os.walk sorted), add a tree pointer line to the
   user guide references section.
8. **Mirror** guide + evidence MD + receipt + tree to the 3 review roots
   (Fabric/evidence/review, HG-KSEOS, SQS-THC) — byte-identical.
9. **git commit** with `git add -A <profile-folder>/` so renames are recorded as renames.

## Pitfalls
- `dest.mkdir(exist_ok=True)` fails for nested `evidence/receipts` — use `parents=True`.
- Moving files breaks `independent_checker.py` (`FDA / "FILE"` root refs) AND the
  EvidenceManifest rows — patch both, then re-run checker; a PASS with the OLD paths is
  impossible once files moved, so re-run after patch.
- Never move: TEAM.md, canonical matrix, binding, evidence MD, user guide, product code,
  checker, tests, WO — their digests are referenced as identity by acceptance artifacts.
- Bundle mirrors the folder structure: move the copies under FDA_RAW_REVIEW_BUNDLE too,
  and delete stale root copies there, or manifest rows resolve to nothing.
- Reorg receipt + directory tree are themselves new evidence artifacts — mirror them and
  bind into evidence MD so the tidy-up is auditable.
