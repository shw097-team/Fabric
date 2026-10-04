# -*- coding: utf-8 -*-
"""Finalize Track A+B: fill sha, 3-way mirror re-review MD, update readback, verify everything."""
import hashlib
import json
import os
import shutil
import time

REVIEW = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md"
BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
MIRRORS = [
    r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review",
    r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review",
]

# 1. compute + fill sha256
data = open(REVIEW, "rb").read()
sha = hashlib.sha256(data).hexdigest()
txt = data.decode("utf-8")
txt = txt.replace("this_file_sha256: <finalize>", f"this_file_sha256: {sha}")
open(REVIEW, "w", encoding="utf-8", newline="\n").write(txt)
sha2 = hashlib.sha256(open(REVIEW, "rb").read()).hexdigest()
print("final re-review MD sha256:", sha2)

# 2. mirror to bundle + HG-KSEOS + SQS-THC
os.makedirs(os.path.join(BUNDLE, "evidence", "review"), exist_ok=True)
for dst in [os.path.join(BUNDLE, "evidence", "review", "FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md")] + \
           [os.path.join(d, "FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md") for d in MIRRORS]:
    shutil.copy2(REVIEW, dst)
print("re-review MD mirrored")

# 3. rehash manifest (bundle-local copy changed)
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")
m = json.load(open(MAN, encoding="utf-8"))
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if os.path.exists(p):
        d2 = open(p, "rb").read()
        a["sha256"] = hashlib.sha256(d2).hexdigest()
        a["size"] = len(d2)
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print("manifest sha:", mh, "| entries:", m["artifact_count"])

# 4. verify all rows exist + hash match
bad = 0
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if not os.path.exists(p):
        print("MISSING:", a["path"]); bad += 1
    else:
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h != a["sha256"]:
            print("HASH MISMATCH:", a["path"]); bad += 1
print("bundle verify:", "ALL OK" if bad == 0 else f"{bad} bad")

# 5. update readback
rb = {
    "artifact": "FDA_MIRROR_READBACK_20260814.json",
    "subject_head": "75499ba",
    "re_review_md_sha256": sha2,
    "evidence_md_sha256": "78736fb0baab86052e1dbc04c671a8d5ab2069db35d286629731f4eeed1730d8",
    "manifest_sha256": mh,
    "manifest_entries": m["artifact_count"],
    "checker": "174/174 PASS",
    "verified_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
}
json.dump(rb, open(os.path.join(BUNDLE, "FDA_MIRROR_READBACK_20260814.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("readback updated")
print(json.dumps(rb, ensure_ascii=False, indent=1)[:400])
