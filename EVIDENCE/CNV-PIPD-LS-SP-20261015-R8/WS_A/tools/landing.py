"""WS-A step 7: guarded landing of the repaired candidate into the live skill dir.

Semantics (brief step 7):
  * add files the candidate has and the live tree lacks          -> action=added
  * replace files whose bytes differ                             -> action=replaced
  * never delete a live file the candidate lacks                 -> action=retained_untouched
  * every pre-existing target path gets a pre-image byte copy + sha256 + size

  python landing.py --src <candidate> --dst <live> --preimage <dir> --receipt <json>
                    [--dry-run]

--dry-run applies into the given --dst (which may be a simulation copy) and writes the
receipt, but skips pre-image capture. The real landing omits --dry-run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel_files(root: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in root.rglob("*"):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = p
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--preimage", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    src, dst = Path(a.src), Path(a.dst)
    pre = Path(a.preimage)

    src_files = rel_files(src)
    dst_files = rel_files(dst)
    pre.mkdir(parents=True, exist_ok=True)

    # pre-image every pre-existing target path (byte copy), before any write
    if not a.dry_run:
        manifest = []
        for rel, d in sorted(dst_files.items()):
            db = d.read_bytes()
            pim = pre / rel
            pim.parent.mkdir(parents=True, exist_ok=True)
            pim.write_bytes(db)
            manifest.append({"path": rel, "bytes": len(db), "sha256": sha256(db)})
        (pre / "PREIMAGE_MANIFEST.json").write_text(
            json.dumps({"schema": "WS_A/PREIMAGE-MANIFEST/1", "dst": str(dst),
                        "entries": manifest}, indent=1), encoding="utf-8")

    rows: list[dict] = []
    for rel in sorted(src_files):
        s = src_files[rel]
        sb = s.read_bytes()
        d = dst / rel
        if rel in dst_files:
            db = d.read_bytes()
            if db == sb:
                rows.append({"path": rel, "action": "retained_untouched",
                             "before_bytes": len(db), "before_sha256": sha256(db),
                             "after_bytes": len(sb), "after_sha256": sha256(sb)})
                continue
            action = "replaced"
            before_bytes, before_sha = len(db), sha256(db)
        else:
            action = "added"
            before_bytes, before_sha = 0, None
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(sb)
        rows.append({"path": rel, "action": action,
                     "before_bytes": before_bytes, "before_sha256": before_sha,
                     "after_bytes": len(sb), "after_sha256": sha256(sb)})

    # live-only files: retained untouched
    for rel in sorted(dst_files):
        if rel in src_files:
            continue
        db = (dst / rel).read_bytes()
        rows.append({"path": rel, "action": "retained_untouched",
                     "before_bytes": len(db), "before_sha256": sha256(db),
                     "after_bytes": len(db), "after_sha256": sha256(db)})

    counts = {"added": 0, "replaced": 0, "retained_untouched": 0}
    for r in rows:
        counts[r["action"]] += 1
    receipt = {
        "schema": "WS_A/APPLY-RECEIPT/1",
        "src": str(src), "dst": str(dst), "dry_run": a.dry_run,
        "target_paths_total": len(rows),
        "src_files_total": len(src_files),
        "dst_files_total": len(dst_files),
        "counts": counts,
        "paths": rows,
    }
    Path(a.receipt).write_text(json.dumps(receipt, indent=1), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in
                      ("dry_run", "target_paths_total", "src_files_total",
                       "dst_files_total", "counts")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
