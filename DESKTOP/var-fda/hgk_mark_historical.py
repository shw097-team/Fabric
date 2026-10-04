# -*- coding: utf-8 -*-
"""Mark old checker receipts HISTORICAL (in place) — keeps audit trail, fixes single-denominator."""
import json
import os
from pathlib import Path

RECEIPTS = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts")
checkers = [f for f in os.listdir(RECEIPTS) if "CHECKER" in f and f.endswith(".json")]
for c in checkers:
    if "FINAL_RR7" in c:
        print(f"KEEP current: {c}")
        continue
    p = RECEIPTS / c
    d = json.load(open(p, encoding="utf-8"))
    if d.get("status") == "HISTORICAL":
        print(f"already historical: {c}")
        continue
    d["status"] = "HISTORICAL"
    d["superseded_by"] = "FDA_CHECKER_FINAL_RR7.json (194/194 on final HEAD be576be)"
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"HISTORICAL-marked: {c}")
print("done")
