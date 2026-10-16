"""WS-B classification helper (read-only).

For every canonical-only path, report whether its bytes appear verbatim in
  (a) the candidate SKILL.md alone, and
  (b) the candidate corpus (MARKER-stripped SKILL.md + every other .md in the tree),
which is exactly what the R8 harness C6 builds. A path may be removed only when (b) holds.
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


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    canon, cand = Path(sys.argv[1]), Path(sys.argv[2])
    cf, kf = files(canon), files(cand)
    skill_main = (cand / "SKILL.md").read_bytes()
    parts = [MARKER.sub(b"", skill_main)]
    for rel, p in kf.items():
        if rel == "SKILL.md" or not rel.endswith(".md"):
            continue
        parts.append(p.read_bytes())
    corpus = b"\n".join(parts)
    rows = []
    for rel in sorted(set(cf) - set(kf)):
        b = cf[rel].read_bytes()
        rows.append({
            "path": rel, "bytes": len(b), "sha256": sha256(b),
            "in_candidate_skill_md": b in skill_main,
            "in_candidate_corpus": b in corpus,
        })
    out = {
        "canonical_only_count": len(rows),
        "removable_certified_in_corpus": sorted(r["path"] for r in rows if r["in_candidate_corpus"]),
        "must_retain": sorted(r["path"] for r in rows if not r["in_candidate_corpus"]),
        "rows": rows,
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
