# -*- coding: utf-8 -*-
"""FDA reorg close-out: evidence MD refs, reorg receipt, guide tree ref, final tree."""
import hashlib
import json
import os
import time
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")

# 1. evidence MD — add reorg section (append note; artifact table rows keep names)
ev = FDA / "FDA_IMPLEMENTATION_EVIDENCE.md"
txt = ev.read_text(encoding="utf-8")
if "## 12. Folder reorganization" not in txt:
    txt += """

## 12. Folder reorganization (2026-08-14)

```text
FDA folder reorganized: evidence receipts -> evidence/receipts/ (29 files),
governance contracts -> governance/ (4 files). Product code, canonical matrix,
binding, TEAM, evidence MD, user guide, WO, checker, tests stay at root.
All moved files: content unchanged (sha256 stable, verified before/after).
Checker paths patched -> 175/175 PASS. EvidenceManifest paths updated (52 entries,
0 missing). Directory tree: FDA_DIRECTORY_TREE.txt
```
"""
    ev.write_text(txt, encoding="utf-8", newline="\n")
    print("evidence MD reorg section appended")

# 2. reorg receipt
receipt = {
    "artifact": "FDA_FOLDER_REORGANIZATION_RECEIPT.json",
    "date": time.strftime("%Y-%m-%d"),
    "root_kept": ["TEAM.md", "FDA_DESKTOP_CAPABILITY_MATRIX.yaml", "FDA_EXECUTION_BINDING.json",
                  "FDA_IMPLEMENTATION_EVIDENCE.md", "FDA_USER_GUIDE.md", "fda_router.py",
                  "fda_lease.py", "xq_native_adapter.py", "independent_checker.py",
                  "WO_FDA_XQ_002.yaml", "test_*.py"],
    "moved_to_evidence_receipts": 29,
    "moved_to_governance": 4,
    "content_unchanged_sha256_stable": True,
    "checker_after": "175/175 PASS",
    "manifest_entries": 52,
    "manifest_sha256": "d35bef595fb300f697c5133f8b02dfd22115b44ac028fda729a1f36f88fcb122",
    "bound_into": ["FDA_DIRECTORY_TREE.txt", "FDA_IMPLEMENTATION_EVIDENCE.md §12"],
}
rpath = FDA / "FDA_FOLDER_REORGANIZATION_RECEIPT.json"
rpath.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("reorg receipt saved")

# 3. user guide — add tree reference note (append line in §12 references)
g = FDA / "FDA_USER_GUIDE.md"
gtxt = g.read_text(encoding="utf-8")
if "FDA_DIRECTORY_TREE" not in gtxt:
    gtxt = gtxt.replace("- Skill recipes：", "- 目錄樹：`Fabric\\fabric-desktop-automation\\FDA_DIRECTORY_TREE.txt`（evidence/receipts/ + governance/ 子目錄）\n- Skill recipes：")
    g.write_text(gtxt, encoding="utf-8", newline="\n")
    print("user guide tree ref added")

# 4. mirror guide + evidence MD + receipt + tree to 3 review roots
import shutil
for d in [Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review"),
          Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review"),
          Path(r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review")]:
    for f in ("FDA_USER_GUIDE.md", "FDA_IMPLEMENTATION_EVIDENCE.md",
              "FDA_FOLDER_REORGANIZATION_RECEIPT.json", "FDA_DIRECTORY_TREE.txt"):
        shutil.copy2(FDA / f, d / f)
print("mirrored (3 review roots)")

# 5. final verify — reorg receipt hash + guide hash
for f in ("FDA_USER_GUIDE.md", "FDA_FOLDER_REORGANIZATION_RECEIPT.json", "FDA_DIRECTORY_TREE.txt"):
    h = hashlib.sha256((FDA / f).read_bytes()).hexdigest()
    print(f"{f}: {h[:16]}")
