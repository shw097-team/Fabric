# -*- coding: utf-8 -*-
"""Sync WO-FDA-XQ-002 artifacts INTO the raw bundle, then rehash ALL from bundle bytes."""
import hashlib
import json
import os
import shutil

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")

# 1. copy new artifacts into bundle (overwrite matrix/checker/evidence MD with current)
new_files = [
    "WO_FDA_XQ_002.yaml",
    "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
    "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
    "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
    "xq_native_adapter.py",
    "test_xq_build_drift.py",
    "test_xq_native_adapter.py",
    "test_xq_action_router.py",
    "FDA_DESKTOP_CAPABILITY_MATRIX.yaml",
    "independent_checker.py",
    "FDA_IMPLEMENTATION_EVIDENCE.md",
]
for fn in new_files:
    src = os.path.join(FDA, fn)
    dst = os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation", fn)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print("copied:", fn)

# 2. rehash ALL manifest artifacts from bundle bytes
m = json.load(open(MAN, encoding="utf-8"))
fixed = []
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if os.path.exists(p):
        data = open(p, "rb").read()
        a["sha256"] = hashlib.sha256(data).hexdigest()
        a["size"] = len(data)
        fixed.append(a["path"])
    else:
        print("MISSING in bundle:", a["path"])

json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"rehashed {len(fixed)} artifacts from bundle bytes")

# 3. verify ALL match
bad = 0
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if not os.path.exists(p):
        print("  missing:", a["path"]); bad += 1
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != a["sha256"]:
        print("  MISMATCH:", a["path"]); bad += 1
print(f"verify: {len(m['artifacts'])} artifacts, {bad} bad")
