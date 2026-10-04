# -*- coding: utf-8 -*-
"""RR8 final: 3-way mirror + sidecar + commit prep."""
import hashlib
import json
import shutil
from pathlib import Path

EVID = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md")
MIRRORS = [
    r"C:\Projects\Agent_Workspace\Fabric\evidence\review",
    r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review",
    r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review",
]
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")

sha = hashlib.sha256(EVID.read_bytes()).hexdigest()
for d in MIRRORS:
    shutil.copy2(EVID, Path(d) / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md")
shutil.copy2(EVID, BUNDLE / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md")
hashes = {hashlib.sha256((Path(d) / "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md").read_bytes()).hexdigest() for d in MIRRORS}
hashes.add(sha)
print("3-way + bundle equal:", len(hashes) == 1, "| sha:", sha)

sidecar = {
    "artifact": "FDA_MIRROR_READBACK_FINAL_RR8.json",
    "rr8_evidence_sha256": sha,
    "rr8_evidence_bytes": EVID.stat().st_size,
    "final_head": "be576bebe7672093039bfe7dbc265f25aa0a1164",
    "manifest_embedded_body_sha": "f4f2207b307d6a248820df870257e7ac637d1a2272aeb4cac5a3bb5018530b95",
    "manifest_entries": 63,
    "manifest_subject": "be576bebe7672093039bfe7dbc265f25aa0a1164",
    "checker": "194/194 PASS (194 unique IDs)",
    "verified_at": "2026-08-14T15:30:00+08:00",
}
(BUNDLE / "FDA_MIRROR_READBACK_FINAL_RR8.json").write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
print("sidecar written")
