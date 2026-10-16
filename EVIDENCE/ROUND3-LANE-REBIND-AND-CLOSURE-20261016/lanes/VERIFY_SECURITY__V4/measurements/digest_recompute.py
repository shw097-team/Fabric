"""Recompute the frozen-subject tree digest over the byte-identical COPY in this lane.

Replicates digest_subject.py exactly: per-dir sha256 over sorted rglob('*') files (suffix != .pyc,
no __pycache__ part), concatenating raw bytes; aggregate over all files concatenated in dir order
(scripts, src, tests, config). Reports both full and first-16-hex forms.
"""
import hashlib
import json
from pathlib import Path

SUB = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject")

rows = {}
agg = hashlib.sha256()
counts = {}
for d in ("scripts", "src", "tests", "config"):
    files = sorted(p for p in (SUB / d).rglob("*") if p.is_file()
                   and p.suffix not in (".pyc",) and "__pycache__" not in p.parts)
    h = hashlib.sha256()
    for p in files:
        b = p.read_bytes()
        h.update(b)
        agg.update(b)
    rows[d] = h.hexdigest()
    counts[d] = len(files)

# alternative: path:sha256 lines (freeze_candidate style) over the whole copy
agg2 = hashlib.sha256()
allf = []
for d in ("scripts", "src", "tests", "config"):
    for p in sorted((SUB / d).rglob("*")):
        if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
            rel = str(p.relative_to(SUB)).replace("\\", "/")
            allf.append((rel, hashlib.sha256(p.read_bytes()).hexdigest()))
for rel, sh in allf:
    agg2.update((rel + ":" + sh + "\n").encode("utf-8"))

print(json.dumps({
    "per_dir_counts": counts,
    "per_dir_digest": rows,
    "aggregate_concat_sha256": agg.hexdigest(),
    "aggregate_concat_first16": agg.hexdigest()[:16],
    "aggregate_pathsha_sha256": agg2.hexdigest(),
    "aggregate_pathsha_first16": agg2.hexdigest()[:16],
    "total_files": sum(counts.values()),
}, indent=1))
