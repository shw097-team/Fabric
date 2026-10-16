"""Recompute the frozen-subject digest exactly and compare to SUBJECT_DIGEST.json declared value.

Derived algorithm (matches recorded 76ec42a0f4c8962c): sha256 of the concatenation of each file's
sha256 HEX STRING, files taken in dir order (scripts, src, tests, config), each dir sorted by rglob('*'),
excluding *.pyc and __pycache__ parts. Runs over the lane COPY; also cross-checks the frozen subject.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
COPY = ROOT / "lanes" / "VERIFY_SECURITY" / "V4" / "work" / "subject"
FROZEN = ROOT / "subject"
DIRS = ("scripts", "src", "tests", "config")


def digest(base):
    h = hashlib.sha256()
    per = {}
    counts = {}
    for d in DIRS:
        files = [p for p in sorted((base / d).rglob("*"))
                 if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts]
        counts[d] = len(files)
        inner = hashlib.sha256()
        for p in files:
            sh = hashlib.sha256(p.read_bytes()).hexdigest()
            h.update(sh.encode())
            inner.update(p.read_bytes())
        per[d] = inner.hexdigest()
    return h.hexdigest(), per, counts


declared = json.loads((ROOT / "SUBJECT_DIGEST.json").read_text(encoding="utf-8"))
copy_dg, copy_per, copy_cnt = digest(COPY)
frozen_dg, frozen_per, frozen_cnt = digest(FROZEN)
print(json.dumps({
    "declared": declared["digest"],
    "declared_total": declared["total"],
    "declared_counts": declared["counts"],
    "copy_digest_full": copy_dg,
    "copy_digest_first16": copy_dg[:16],
    "copy_matches_declared": copy_dg[:16] == declared["digest"],
    "frozen_digest_full": frozen_dg,
    "frozen_matches_declared": frozen_dg[:16] == declared["digest"],
    "copy_counts": copy_cnt,
    "copy_equals_frozen": copy_dg == frozen_dg,
}, indent=1))
