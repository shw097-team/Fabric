# -*- coding: utf-8 -*-
"""Track B fix: place re-review MD correctly in bundle + render FINAL re-review evidence with rebind facts."""
import hashlib
import json
import os
import shutil

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
REVIEW_SRC = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md"

# 1. copy re-review MD into bundle under evidence/review/ (manifest-consistent path)
dst_dir = os.path.join(BUNDLE, "evidence", "review")
os.makedirs(dst_dir, exist_ok=True)
dst = os.path.join(dst_dir, "FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md")
shutil.copy2(REVIEW_SRC, dst)
print("re-review MD ->", dst)

# 2. rehash manifest + ensure both re-review rows point to real files
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")
m = json.load(open(MAN, encoding="utf-8"))
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if os.path.exists(p):
        data = open(p, "rb").read()
        a["sha256"] = hashlib.sha256(data).hexdigest()
        a["size"] = len(data)
    else:
        print("STILL MISSING:", a["path"])
# add the bundle-local re-review row if absent
rel = "evidence/review/FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md"
if not any(a["path"] == rel for a in m["artifacts"]):
    data = open(dst, "rb").read()
    m["artifacts"].append({"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
m["artifact_count"] = len(m["artifacts"])
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print("manifest entries:", m["artifact_count"], "| sha:", mh)

# 3. verify ALL rows exist
missing = [a["path"] for a in m["artifacts"] if not os.path.exists(os.path.join(BUNDLE, a["path"]))]
print("missing rows:", missing if missing else "(none)")
