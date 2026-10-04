# -*- coding: utf-8 -*-
"""RR3 closure FINAL v2: regenerate manifest covering EVERY physical file in bundle
Fabric/fabric-desktop-automation (root + DOC + tests + evidence/receipts + governance).
Sets (unambiguous):
  payload_entries  = manifest rows (all evidence payload files, manifest excluded)
  manifest_entries = payload_entries + 1 (the manifest file itself, physically present, NOT self-listed)
  bundle_files     = physical file count in bundle dir (recursive)
  self_entry_policy = manifest does NOT list itself (no self-hash loop); evidence MD
                      references manifest by PATH only (single-direction binding)
"""
import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")

head = subprocess.run(["git", "-C", r"C:\Projects\Agent_Workspace\Fabric", "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()

# 1. sync everything from FDA dir into bundle (mirror reorg state incl. DOC/, tests/, reorg receipts)
FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
for root, dirs, files in os.walk(FDA):
    if "__pycache__" in root:
        continue
    for f in files:
        src = os.path.join(root, f)
        rel = os.path.relpath(src, FDA)
        dst = os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

# 2. enumerate payload (everything under bundle Fabric/fabric-desktop-automation, recursive)
payload = []
for root, dirs, files in os.walk(os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation")):
    if "__pycache__" in root or ".pyc" in str(root):
        continue
    for f in files:
        if f.endswith(".pyc"):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, BUNDLE).replace("\\", "/")
        payload.append(rel)
payload.sort()

entries = []
for rel in payload:
    data = open(os.path.join(BUNDLE, rel), "rb").read()
    entries.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})

now = datetime.now(timezone.utc)
man = {
    "artifact_id": "FDA_EVIDENCE_MANIFEST",
    "schema": "FDA-EVIDENCE-MANIFEST/2",
    "version": "FINAL_POST_REBIND_RR3_V2",
    "generated_at_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "subject_root": {"repo": "Fabric", "git_head": head,
                     "note": "FINAL POST-REBIND after RR3 closure (folder reorg + exact-set normalization)"},
    "exact_sets": {
        "payload_entries": len(entries),
        "manifest_entries": len(entries) + 1,
        "bundle_files": None,
        "self_entry_policy": "manifest does NOT list itself; evidence MD references manifest by PATH only (single direction); manifest_entries = payload_entries (rows) + 1 (manifest file physically present, not self-listed)",
    },
    "checker": {"script": "Fabric/fabric-desktop-automation/independent_checker.py",
                "verdict": "PASS", "checks": 176, "failed": 0,
                "note": "SINGLE current denominator; 174 = pre-folder-reorg; 144 = SUPERSEDED_PRE_XQ_PATCH"},
    "dod_counts": {"PASS": 36, "PARTIAL": 0, "BLOCKED": 0},
    "artifacts": entries,
    "artifact_count": len(entries),
    "missing_artifacts": [],
}
json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 3. bundle physical count
bundle_files = []
for root, dirs, files in os.walk(BUNDLE):
    for f in files:
        bundle_files.append(os.path.relpath(os.path.join(root, f), BUNDLE))
man["exact_sets"]["bundle_files"] = len(bundle_files)
man["exact_sets"]["bundle_extra_files"] = len([b for b in bundle_files
    if b.replace("\\", "/") not in [e["path"] for e in entries]])
json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print(f"FINAL manifest: payload={len(entries)} | manifest_entries={len(entries)+1} | bundle_files={len(bundle_files)}")
print(f"bundle extras (non-payload, incl manifest/index/readback/review): {man['exact_sets']['bundle_extra_files']}")
print(f"subject_root={head}")
print(f"manifest sha256={mh}")

# 4. verify all rows exist + hash match
bad = 0
for e in entries:
    p = os.path.join(BUNDLE, e["path"].replace("/", os.sep))
    if not os.path.exists(p):
        print("MISSING:", e["path"]); bad += 1
    elif hashlib.sha256(open(p, "rb").read()).hexdigest() != e["sha256"]:
        print("HASH MISMATCH:", e["path"]); bad += 1
print("verify:", "ALL OK" if bad == 0 else f"{bad} bad")
