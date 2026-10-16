"""WS-A step 2: strip SKCV-SLICE marker lines from the repaired candidate SKILL.md.

Operates only on WS_A/repaired_candidate/SKILL.md. Removes every line matching
^=+\\s*SKCV-SLICE.*$ (line-content match after stripping CR/LF), preserving all other
bytes and the original newline style, then asserts the loader contract.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")
SKILL = W / "repaired_candidate/SKILL.md"
MARKER = re.compile(r"^=+\s*SKCV-SLICE.*$")


def frontmatter(b: bytes) -> dict | None:
    if not b.startswith(b"---"):
        return None
    end = b.find(b"\n---", 3)
    if end < 0:
        return None
    out: dict[str, str] = {}
    for line in b[3:end].decode("utf-8", "replace").splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def main() -> int:
    before = SKILL.read_bytes()
    kept: list[bytes] = []
    removed = 0
    for raw in before.splitlines(keepends=True):
        content = raw.rstrip(b"\r\n")
        if MARKER.match(content.decode("utf-8", "replace")):
            removed += 1
            continue
        kept.append(raw)
    after = b"".join(kept)
    SKILL.write_bytes(after)

    assert after.startswith(b"---"), "result does not start with frontmatter delimiter"
    fm = frontmatter(after)
    assert fm is not None, "frontmatter did not parse"
    assert fm.get("name") == "adversarial-verification-rounds", f"bad name: {fm.get('name')!r}"
    assert fm.get("version") == "1.0.0", f"bad version: {fm.get('version')!r}"

    rec = {
        "step": "s2_repair_skill_md",
        "before_bytes": len(before),
        "after_bytes": len(after),
        "marker_lines_removed": removed,
        "before_sha256": hashlib.sha256(before).hexdigest(),
        "after_sha256": hashlib.sha256(after).hexdigest(),
        "starts_with_frontmatter": after.startswith(b"---"),
        "frontmatter_name": fm.get("name"),
        "frontmatter_version": fm.get("version"),
        "remaining_marker_lines": len(MARKER.findall(after.decode("utf-8", "replace"))),
    }
    (W / "s2_repair_result.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print(json.dumps(rec, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
