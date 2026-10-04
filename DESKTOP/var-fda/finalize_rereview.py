# -*- coding: utf-8 -*-
"""Finalize external re-review evidence: compute sha256, fill in, sync mirrors, update manifest root."""
import hashlib
import json
import os
import shutil
import time

SRC = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md"
BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
MIRRORS = [
    r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review",
    r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review",
]

# 1. compute sha256 of current file
data = open(SRC, "rb").read()
sha = hashlib.sha256(data).hexdigest()
print("evidence sha256:", sha)

# 2. fill in sha (replace placeholder both in header yaml and §9.2)
txt = data.decode("utf-8")
txt = txt.replace("evidence_sha256: <computed-below>", f"evidence_sha256: {sha}")
txt = txt.replace("- 此單一證據檔的 sha256：<finalize at freeze>", f"- 此單一證據檔的 sha256：{sha}")
open(SRC, "w", encoding="utf-8", newline="\n").write(txt)
data2 = open(SRC, "rb").read()
sha2 = hashlib.sha256(data2).hexdigest()
print("final sha256:", sha2)

# 3. update manifest subject_root -> cf24b65 (current HEAD)
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")
m = json.load(open(MAN, encoding="utf-8"))
m["subject_root"] = {
    "repo": "Fabric",
    "git_head": "cf24b65",
    "note": "git HEAD after DoD-17 PAPER runtime closure; canonical frozen subject for external re-review",
}
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("manifest subject_root -> cf24b65")

# 4. add re-review evidence to manifest artifacts
rel = "evidence/review/FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md"
bpath = os.path.join(BUNDLE, "FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md")
shutil.copy2(SRC, bpath)
if not any(a["path"] == rel for a in m["artifacts"]):
    m["artifacts"].append({"path": rel, "sha256": sha2, "size": len(data2)})
    m["artifact_count"] = len(m["artifacts"])
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("manifest artifacts:", m["artifact_count"])

# 5. sync mirrors (Fabric evidence/review + HG-KSEOS + SQS-THC)
for d in MIRRORS:
    dst = os.path.join(d, "FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md")
    shutil.copy2(SRC, dst)
    print("mirrored:", dst)

# 6. 4-way evidence MD mirror (keep evidence MD in sync across repos)
ev = os.path.join(FDA, "FDA_IMPLEMENTATION_EVIDENCE.md")
for d in MIRRORS + [r"C:\Projects\Agent_Workspace\Fabric\evidence\review"]:
    dst = os.path.join(d, "FDA_IMPLEMENTATION_EVIDENCE.md")
    if os.path.exists(dst):
        shutil.copy2(ev, dst)
print("evidence MD mirrored (4-way)")
print("done", time.strftime("%H:%M:%S"))
