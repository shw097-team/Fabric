"""Independently verify the rollback drill result against the receipt + pre-image."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    rec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pre = Path(sys.argv[2])
    dst = Path(rec["dst"])
    df = files(dst)
    problems, restored, deleted = [], [], []
    for row in rec["paths"]:
        rel, act, before = row["path"], row["action"], row["before_sha256"]
        tgt = dst / rel
        if act in ("replaced", "retained_untouched"):
            if not tgt.is_file():
                problems.append(f"missing after rollback: {rel}")
            elif sha256(tgt.read_bytes()) != before:
                problems.append(f"sha mismatch after rollback: {rel}")
            else:
                restored.append(rel)
        elif act == "added":
            if tgt.exists():
                problems.append(f"added file still present: {rel}")
            else:
                deleted.append(rel)
    # whole-tree equality vs preimage (excluding the manifest file the drill tree may lack)
    pf = files(pre)
    extra = sorted(set(df) - set(pf) - {"PREIMAGE_MANIFEST.json"})
    missing = sorted(set(pf) - set(df) - {"PREIMAGE_MANIFEST.json"})
    mismatched = sorted(r for r in set(df) & set(pf)
                        if r != "PREIMAGE_MANIFEST.json"
                        and df[r].read_bytes() != pf[r].read_bytes())
    out = {
        "rollback_verdict": "OK" if not problems else "FAIL",
        "restored_sha_matches": len(restored),
        "added_files_deleted": len(deleted),
        "problems": problems,
        "tree_vs_preimage": {"extra_files": extra, "missing_files": missing,
                             "mismatched_files": mismatched,
                             "identical": not extra and not missing and not mismatched},
    }
    print(json.dumps(out, indent=1))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
