# -*- coding: utf-8 -*-
"""Sync RR8 authority receipt into bundle + manifest; then rebuild RR8 MD with CORRECT manifest sha."""
import hashlib
import json
import shutil
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"

# 1. sync authority receipt into bundle
src = FDA / "evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"
dst = BUNDLE / "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(src, dst)
print("authority receipt synced to bundle")

# 2. manifest: add authority receipt if missing
m = json.load(open(MAN, encoding="utf-8"))
rel = "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"
paths = {a["path"] for a in m["artifacts"]}
if rel not in paths:
    data = dst.read_bytes()
    m["artifacts"].append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
    m["artifact_count"] = len(m["artifacts"])
    json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"manifest updated: {m['artifact_count']} entries")
else:
    print("authority receipt already in manifest")

mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print(f"manifest sha: {mh}")
