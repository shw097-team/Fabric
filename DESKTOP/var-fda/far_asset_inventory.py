# -*- coding: utf-8 -*-
"""FAR source-1: what qualified assets exist that I skipped this round?
matrix rows / adapter functions / fingerprint / router — the 'verify-and-CALL' inventory."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import yaml

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
MATRIX = FDA / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml"
ADAPTER = FDA / "xq_native_adapter.py"
RECEIPTS = FDA / "evidence" / "receipts"

print("=== 1. Capability Matrix: action classes + status ===")
if MATRIX.exists():
    m = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    actions = m.get("action_classes", m.get("actions", {}))
    if isinstance(actions, dict):
        for k, v in actions.items():
            st = v.get("qualification", {}).get("status") if isinstance(v, dict) else "?"
            qr = v.get("qualification", {}) if isinstance(v, dict) else {}
            print(f"  {k}: status={st} runs={qr.get('fresh_runs','?')}")
    elif isinstance(actions, list):
        for a in actions:
            print(f"  {a.get('action_class','?')}: {a.get('qualification',{}).get('status','?')}")
else:
    print("  MATRIX NOT FOUND at", MATRIX)

print("\n=== 2. xq_native_adapter.py functions ===")
if ADAPTER.exists():
    import re
    src = ADAPTER.read_text(encoding="utf-8")
    funcs = re.findall(r"^def (\w+)\(|^    def (\w+)\(", src, re.M)
    print("  functions:", [f[0] or f[1] for f in funcs])
else:
    print("  ADAPTER NOT FOUND at", ADAPTER)

print("\n=== 3. router file ===")
ROUTER = FDA / "fda_router.py"
if ROUTER.exists():
    print("  fda_router.py exists,", ROUTER.stat().st_size, "bytes")
else:
    print("  fda_router.py NOT at", ROUTER)
    # search
    for p in FDA.rglob("*.py"):
        if "router" in p.name.lower():
            print("  found router:", p)

print("\n=== 4. receipts inventory (evidence/receipts) ===")
if RECEIPTS.exists():
    for p in sorted(RECEIPTS.glob("*.json")):
        print(f"  {p.name} ({p.stat().st_size}B)")
else:
    print("  RECEIPTS dir missing")

print("\n=== 5. WO-FDA-XQ-002 yaml ===")
WO = FDA / "WO_FDA_XQ_002.yaml"
print("  exists:", WO.exists())
