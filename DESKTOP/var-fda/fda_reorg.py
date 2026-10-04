# -*- coding: utf-8 -*-
"""FDA folder reorg — snapshot hashes BEFORE move, then move, then verify hashes stable.
Frozen-identity/product/normative stay at root; evidence receipts -> evidence/receipts/;
governance contracts -> governance/. Content unchanged -> sha256 stable."""
import hashlib
import json
import os
import shutil
import time
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SNAP = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\fda_reorg_snapshot.json"

# ---- classify ----
STAY_ROOT = {
    "TEAM.md", "FDA_DESKTOP_CAPABILITY_MATRIX.yaml", "FDA_EXECUTION_BINDING.json",
    "FDA_IMPLEMENTATION_EVIDENCE.md", "FDA_USER_GUIDE.md",
    "fda_router.py", "fda_lease.py", "xq_native_adapter.py",
    "independent_checker.py", "WO_FDA_XQ_002.yaml",
    "test_xq_build_drift.py", "test_xq_native_adapter.py", "test_xq_action_router.py",
}
RECEIPTS = {  # evidence/receipts/
    "FDA_C0_READBACK_RECEIPT.json", "FDA_C2_CUA_QUALIFICATION_RECEIPT.json",
    "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json", "FDA_C3_UFO2_QUALIFICATION_RECEIPT.json",
    "FDA_C4_XQ_QUALIFICATION_RECEIPT.json", "FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
    "FDA_F01_LIVE_FIXTURE_RECEIPT.json", "FDA_F03_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F04_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_CLOSURE_V3_RECEIPT.json", "FDA_F06_CLOSURE_V4_RECEIPT.json",
    "FDA_F06_CLOSURE_V5_RECEIPT.json", "FDA_F06_CLOSURE_V6_RECEIPT.json",
    "FDA_F06_CLOSURE_V7_RECEIPT.json", "FDA_F06_CLOSURE_V8_RECEIPT.json",
    "FDA_F06_COMPILE_RECEIPT.json", "FDA_F06_COMPILE_TOOLBAR_RECEIPT.json",
    "FDA_F06_EXPORT_RECEIPT.json", "FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_LIVE_FIXTURE_RECEIPT.json", "FDA_F06_SYSTEM_PATH_RECEIPT.json",
    "FDA_F06_TEN_RUN_RECEIPT.json", "FDA_F09_RADAR_RECEIPT.json",
    "FDA_F09B_PAPER_RUNTIME_RECEIPT.json", "FDA_F10_F11_READBACK_RECEIPT.json",
    "FDA_BOUNDED_CONTROL_LIVE_PROBE.json",
    "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json", "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
    "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
}
GOVERNANCE = {  # governance/
    "FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml", "FDA_INTEROP_DISPOSITION.yaml",
    "FDA_ROUTE_CHECK.yaml", "FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml",
}

# ---- 1. snapshot hashes ----
snap = {}
for f in os.listdir(FDA):
    p = FDA / f
    if p.is_file():
        snap[f] = hashlib.sha256(p.read_bytes()).hexdigest()
json.dump(snap, open(SNAP, "w", encoding="utf-8"), indent=2)
print(f"snapshot: {len(snap)} files")

# ---- 2. move ----
moved = {"receipts": [], "governance": []}
for d, files in (("evidence/receipts", RECEIPTS), ("governance", GOVERNANCE)):
    dest = FDA / d
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        src = FDA / f
        if src.exists():
            shutil.move(str(src), str(dest / f))
            moved[d.split("/")[-1]].append(f)

print(f"moved receipts: {len(moved['receipts'])} | governance: {len(moved['governance'])}")
print("missing (already moved?):", [f for f in RECEIPTS | GOVERNANCE if not (FDA / f).exists()])

# ---- 3. verify hashes stable post-move ----
bad = []
for f, h in snap.items():
    for sub in ("", "evidence/receipts", "governance"):
        p = FDA / sub / f
        if p.exists():
            if hashlib.sha256(p.read_bytes()).hexdigest() != h:
                bad.append(f)
            break
print("hash-stable verify:", "ALL OK" if not bad else f"BAD: {bad}")

# ---- 4. new tree ----
tree = []
for root, dirs, files in os.walk(FDA):
    dirs.sort()
    rel = os.path.relpath(root, FDA)
    depth = 0 if rel == "." else rel.count(os.sep) + 1
    tree.append("  " * depth + os.path.basename(root) + "/")
    for f in sorted(files):
        tree.append("  " * (depth + 1) + f)
print("\n=== NEW TREE ===")
print("\n".join(tree))
open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_DIRECTORY_TREE.txt", "w", encoding="utf-8").write("\n".join(tree))
print("\ntree saved -> FDA_DIRECTORY_TREE.txt")
