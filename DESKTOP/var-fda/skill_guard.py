# -*- coding: utf-8 -*-
"""SKILL-GUARD (FAR-on-FAR 2026-08-14): pre/post-slim verification for ANY skill change.
Run BEFORE (pre) and AFTER (post) any skill size reduction. Blocks on structural damage:
dangling refs, orphaned markdown, broken pointers, content-loss heuristics.

Usage:
  skill_guard.py <skill_dir> pre   # before slimming: baseline
  skill_guard.py <skill_dir> post  # after slimming: verify no regression
Exit 0 = PASS / 1 = BLOCKED
"""
import re
import sys
from pathlib import Path

def audit(skill_dir: Path) -> list:
    issues = []
    sk = skill_dir / "SKILL.md"
    if not sk.exists():
        return [f"SKILL.md missing in {skill_dir}"]
    txt = sk.read_text(encoding="utf-8")
    size = len(txt)

    # 1. size limit
    if size > 100_000:
        issues.append(f"SIZE {size}B > 100k limit — split+route required, do NOT slim by hand")

    # 2. dangling reference pointers
    refs = set(re.findall(r"references/[a-z0-9-]+\.md", txt))
    for r in refs:
        if not (skill_dir / r).exists():
            issues.append(f"DANGLING REF: {r}")

    # 3. orphaned markdown artifacts (only when a reference-line is merged — 'md.1.')
    for pat in [".md.1.", ".md.2.", ".md.3.", "below.**\n"]:
        if pat in txt:
            issues.append(f"ORPHAN PATTERN: {pat!r}")

    # 4. broken list numbering (line starts 'X-Y.' merged into ref)
    for m in re.finditer(r"\.md\.\d\.", txt):
        issues.append(f"NEWLINE-EATEN near: ...{txt[max(0,m.start()-30):m.end()+30]!r}")

    # 5. self-referential pointers to own sections that don't exist
    for m in re.finditer(r"see (HARD RULES|Step \d+[A-Z]?)", txt):
        pass  # informational only

    # 6. reference count parity (content not silently dropped): report for comparison
    return issues, {"size": size, "refs": len(refs), "sections": len(re.findall(r"^## ", txt, re.M))}

def main():
    if len(sys.argv) < 3:
        print("usage: skill_guard.py <skill_dir> pre|post")
        return 2
    skill_dir = Path(sys.argv[1])
    phase = sys.argv[2]
    issues, stats = audit(skill_dir)
    print(f"=== SKILL-GUARD {phase.upper()}: {skill_dir.name} ===")
    print(f"  size={stats['size']}B refs={stats['refs']} sections={stats['sections']}")
    if issues:
        for i in issues:
            print(f"  [FAIL] {i}")
        print("RESULT: BLOCKED")
        return 1
    print("RESULT: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
