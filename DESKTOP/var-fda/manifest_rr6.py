# -*- coding: utf-8 -*-
"""Update EvidenceManifest with RR6 artifacts (correct bundle-relative paths)."""
import hashlib
import json
import os
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
m = json.load(open(MAN, encoding="utf-8"))

# map rel -> actual file (verify each exists)
candidates = {
    "evidence/review/FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md": BUNDLE / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md",
    "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md": BUNDLE / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md",
    "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F01_CURRENT_260811_RECEIPT.json":
        BUNDLE / "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F01_CURRENT_260811_RECEIPT.json",
    "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json":
        BUNDLE / "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json",
    "FDA_MIRROR_READBACK_20260814_RR6.json": BUNDLE / "FDA_MIRROR_READBACK_20260814_RR6.json",
}

paths = {a["path"] for a in m["artifacts"]}
added = 0
for rel, fp in candidates.items():
    if rel in paths:
        continue
    if fp.exists():
        data = fp.read_bytes()
        m["artifacts"].append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
        added += 1
        print(f"added {rel} ({len(data)}B)")
    else:
        print(f"MISSING {rel}")

m["artifact_count"] = len(m["artifacts"])
m["subject_root"] = {
    "repo": "Fabric", "git_head": "34fbbd3",
    "note": "RR6 repair package (F01 current 260811 10/10 + PAPER 10 verified + F06 fresh 10x + checker 179 raw); subject bound post-repair"
}
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print(f"manifest entries: {m['artifact_count']} | added {added} | sha: {mh[:16]}")
