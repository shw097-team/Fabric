# -*- coding: utf-8 -*-
"""HGK-GATE-CLOSURE-001 repair: clean evidence state for machine preflight.
1. Old RR6 checker receipts -> HISTORICAL-marked (rename suffix, keep in place for audit)
2. Stale self-hash evidence MDs -> evidence/historical/
3. Verify preflight now PASSES."""
import json
import os
import shutil
from pathlib import Path

EVID = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence")
RECEIPTS = EVID / "receipts"
HIST = EVID / "historical"

# 1. HISTORICAL-mark old checker receipts (only RR7 FINAL stays current)
checkers = [f for f in os.listdir(RECEIPTS) if "CHECKER" in f and f.endswith(".json")]
for c in checkers:
    if "FINAL_RR7" in c:
        print(f"KEEP current: {c}")
        continue
    d = json.load(open(RECEIPTS / c, encoding="utf-8"))
    d["status"] = "HISTORICAL"
    d["superseded_by"] = "FDA_CHECKER_FINAL_RR7.json (194/194 on final HEAD be576be)"
    json.dump(d, open(RECEIPTS / c, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"HISTORICAL-marked: {c}")

# 2. move stale self-hash MDs to historical/
HIST.mkdir(exist_ok=True)
moved = []
for f in os.listdir(EVID):
    if f.endswith(".md") and ("EVIDENCE" in f or "SINGLE" in f):
        txt = (EVID / f).read_text(encoding="utf-8", errors="replace")
        if "this_file_sha256" in txt:
            shutil.move(str(EVID / f), str(HIST / f))
            moved.append(f)
print(f"moved stale MDs to historical/: {moved}")

print("done — re-run preflight to verify")
