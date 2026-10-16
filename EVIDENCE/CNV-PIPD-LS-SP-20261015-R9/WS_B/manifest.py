"""WS-B manifest/diff helper (read-only on the two trees).

Emits a JSON manifest for a tree and a path-by-path diff between canonical and candidate,
including whether each canonical-only file's bytes are present verbatim in the candidate corpus
(the same corpus the R8 harness C6 check builds: SKILL.md with slice markers stripped, plus every
other .md file in the tree).
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

MARKER = re.compile(rb"^=+\s*SKCV-SLICE[^\n]*\n", re.M)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def manifest(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(root)).replace("\\", "/")
            b = p.read_bytes()
            out[rel] = {"bytes": len(b), "sha256": sha256(b)}
    return out


def corpus(root: Path) -> bytes:
    sk = (root / "SKILL.md").read_bytes()
    parts = [MARKER.sub(b"", sk)]
    for p in sorted(root.rglob("*.md")):
        if p.name == "SKILL.md":
            continue
        parts.append(p.read_bytes())
    return b"\n".join(parts)


def main() -> int:
    canon = Path(sys.argv[1])
    cand = Path(sys.argv[2])
    mc, mk = manifest(canon), manifest(cand)
    cc = corpus(cand)
    both_same, replaced, added, canon_only = [], [], [], []
    for rel, m in mk.items():
        if rel in mc and mc[rel]["sha256"] == m["sha256"]:
            both_same.append(rel)
        elif rel in mc:
            replaced.append({"path": rel, "before": mc[rel], "after": m})
        else:
            added.append({"path": rel, "after": m})
    for rel, m in mc.items():
        if rel not in mk:
            in_corpus = False
            try:
                in_corpus = (canon / rel).read_bytes() in cc
            except OSError:
                in_corpus = False
            canon_only.append({"path": rel, "before": m, "bytes_in_candidate_corpus": in_corpus})
    report = {
        "canonical_root": str(canon),
        "candidate_root": str(cand),
        "counts": {
            "canonical_files": len(mc),
            "candidate_files": len(mk),
            "both_identical": len(both_same),
            "replaced": len(replaced),
            "added": len(added),
            "canonical_only": len(canon_only),
            "canonical_only_certified_in_corpus": sum(1 for r in canon_only if r["bytes_in_candidate_corpus"]),
        },
        "both_identical": both_same,
        "replaced": replaced,
        "added": added,
        "canonical_only": canon_only,
    }
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
