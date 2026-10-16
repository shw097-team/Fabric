"""WS-B guarded overlay apply (non-destructive).

Policy (brief WS-R9-B step 2-3):
  * candidate path present in dst with different bytes -> action=replaced
  * candidate path absent from dst                      -> action=added
  * candidate path byte-identical to dst                -> skipped (not recorded, no write)
  * dst path absent from candidate                      -> action=retained_untouched

Every recorded row gets before_sha256; replaced/added rows also get after_sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--apply", action="store_true", help="write bytes; default is receipt-only")
    a = ap.parse_args()
    src, dst = Path(a.src), Path(a.dst)
    sf, df = files(src), files(dst)
    rows: list[dict] = []
    for rel in sorted(sf):
        sb = sf[rel].read_bytes()
        tgt = dst / rel
        if rel in df:
            db = df[rel].read_bytes()
            if db == sb:
                continue
            row = {"path": rel, "action": "replaced",
                   "before_sha256": sha256(db), "before_bytes": len(db),
                   "after_sha256": sha256(sb), "after_bytes": len(sb)}
        else:
            row = {"path": rel, "action": "added",
                   "before_sha256": None, "before_bytes": 0,
                   "after_sha256": sha256(sb), "after_bytes": len(sb)}
        if a.apply:
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_bytes(sb)
        rows.append(row)
    for rel in sorted(df):
        if rel in sf:
            continue
        db = df[rel].read_bytes()
        rows.append({"path": rel, "action": "retained_untouched",
                     "before_sha256": sha256(db), "before_bytes": len(db),
                     "after_sha256": sha256(db), "after_bytes": len(db)})
    counts = {"added": 0, "replaced": 0, "retained_untouched": 0}
    for r in rows:
        counts[r["action"]] += 1
    receipt = {
        "schema": "WS_R9B/APPLY-RECEIPT/1",
        "src": str(src), "dst": str(dst), "applied": a.apply,
        "src_files_total": len(sf), "dst_files_total": len(df),
        "target_paths_total": len(rows), "counts": counts, "paths": rows,
    }
    Path(a.receipt).write_text(json.dumps(receipt, indent=1), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in
                      ("applied", "src_files_total", "dst_files_total",
                       "target_paths_total", "counts")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
