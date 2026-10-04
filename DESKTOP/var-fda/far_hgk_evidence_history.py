# -*- coding: utf-8 -*-
"""FAR source-1: evidence mutation history — how manifest/checker/root evolved across RR6-8.
Look for: stale fields carried forward, manual edits, non-atomic regeneration."""
import hashlib
import json
import os
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
out = []

# 1. manifest history: current manifest vs git history
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
if MAN.exists():
    m = json.load(open(MAN, encoding="utf-8"))
    out.append(f"=== CURRENT MANIFEST (on disk) ===")
    out.append(f"  subject_root: {m.get('subject_root', {}).get('git_head')}")
    out.append(f"  entries: {m.get('artifact_count')}")
    out.append(f"  checker note: {str(m.get('checker', {}).get('note'))[:100]}")
    # count entries whose sha could be stale (no file or size mismatch)
    stale = 0
    for a in m["artifacts"]:
        p = BUNDLE / a["path"]
        if not p.exists():
            stale += 1
            out.append(f"  STALE-ENTRY (missing file): {a['path']}")
        else:
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            if sha != a["sha256"]:
                stale += 1
                out.append(f"  STALE-ENTRY (hash mismatch): {a['path']}")
    out.append(f"  stale entries: {stale}/{len(m['artifacts'])}")
else:
    out.append("NO MANIFEST on disk")

# 2. git history of manifest (was it regenerated fresh or edited?)
os.chdir(r"C:\Projects\Agent_Workspace\Fabric")
import subprocess
r = subprocess.run(["git", "log", "--oneline", "-15", "--", "evidence/review/FDA_RAW_REVIEW_BUNDLE/FDA_EVIDENCE_MANIFEST.json"],
                   capture_output=True, text=True)
out.append(f"=== MANIFEST GIT HISTORY (last 15) ===")
out.append(r.stdout or "(no manifest commits in repo?)")

# 3. checker history — multiple checker receipts?
rec = FAB / "evidence/receipts"
checkers = sorted([f for f in os.listdir(rec) if "CHECKER" in f and f.endswith(".json")])
out.append(f"=== CHECKER RECEIPTS ON DISK ({len(checkers)}) ===")
for c in checkers:
    try:
        d = json.load(open(rec / c, encoding="utf-8"))
        out.append(f"  {c}: total={d.get('total_checks')} subject={str(d.get('subject_root'))[:12]} verdict={d.get('verdict')}")
    except Exception as e:
        out.append(f"  {c}: UNPARSEABLE {str(e)[:40]}")

# 4. evidence MDs — how many single-evidence files, which is current?
ev = FAB / "evidence"
mds = sorted([f for f in os.listdir(ev) if f.startswith("FDA_EXTERNAL") or "EVIDENCE" in f])
out.append(f"=== EVIDENCE MDs ({len(mds)}) ===")
for md in mds:
    p = ev / md
    out.append(f"  {md}: {p.stat().st_size}B")
    # check self-hash field presence (RR6-005 defect pattern)
    txt = p.read_text(encoding="utf-8", errors="replace")
    if "this_file_sha256" in txt:
        out.append(f"    -> has this_file_sha256 (self-hash defect pattern)")

print("\n".join(out))
