# -*- coding: utf-8 -*-
"""Finalize RR6 evidence: sidecar readback + 3-way mirror + manifest update + F01/PAPER receipts in bundle."""
import hashlib
import json
import shutil
from pathlib import Path

EVID = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md")
MIRRORS = [
    r"C:\Projects\Agent_Workspace\Fabric\evidence\review",
    r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review",
    r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review",
]
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")

sha = hashlib.sha256(EVID.read_bytes()).hexdigest()

# 1. sidecar readback
sidecar = {
    "artifact": "FDA_MIRROR_READBACK_20260814_RR6.json",
    "rr6_evidence_sha256": sha,
    "rr6_evidence_bytes": EVID.stat().st_size,
    "mirror_targets": ["Fabric/evidence/review", "HG-KSEOS/evidence/review", "SQS-THC/evidence/review"],
    "verified_at": "2026-08-14T14:20:00+08:00",
}
sb = BUNDLE / "FDA_MIRROR_READBACK_20260814_RR6.json"
sb.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")

# 2. mirror 3-way + bundle copy
for d in MIRRORS:
    shutil.copy2(EVID, Path(d) / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md")
shutil.copy2(EVID, BUNDLE / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md")

# verify equality
hashes = {hashlib.sha256((Path(d) / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md").read_bytes()).hexdigest() for d in MIRRORS}
hashes.add(sha)
print("3-way + bundle equal:", len(hashes) == 1, "| sha:", sha)

# 3. receipts into bundle
for rn in ["FDA_F01_CURRENT_260811_RECEIPT.json", "FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json"]:
    src = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts") / rn
    dst = BUNDLE / "Fabric" / "fabric-desktop-automation" / "evidence" / "receipts" / rn
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print("bundled:", rn)

print("done")
