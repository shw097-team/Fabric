# -*- coding: utf-8 -*-
"""FAR FULL-SEARCH: inventory every tool/asset/skill produced or fixed this session
(RR6→r11 external acceptance). Compare against the 4 docs + routing + skills."""
from pathlib import Path
import os

VFD = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SK = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development")

print("=== A. var/fda 工具/腳本（本 session 產出）===")
vfd_tools = []
for f in sorted(VFD.glob("*.py")):
    # session-produced tooling (by name pattern)
    if any(k in f.name for k in ["screen_state", "preflight", "fda_run", "asset", "reseal",
                                 "finalize", "build_rr", "verify", "hgk_", "skill_guard",
                                 "atomic", "mark_historical", "sync_rr", "manifest_rr",
                                 "rr6_", "rr7_", "rr8_", "final_", "docs_", "far_"]):
        vfd_tools.append(f.name)
print(f"  {len(vfd_tools)} tools: {', '.join(sorted(set(vfd_tools))[:40])}")

print("\n=== B. Fabric/fabric-desktop-automation 資產 ===")
fab_assets = sorted(os.listdir(FDA))
print(f"  {len(fab_assets)} items: {', '.join(fab_assets[:25])}")

print("\n=== C. receipts（evidence/receipts）===")
rec = FDA / "evidence" / "receipts"
if rec.exists():
    receipts = sorted(os.listdir(rec))
    print(f"  {len(receipts)} receipts")
    for r in receipts:
        print(f"    {r}")
else:
    print("  (no receipts dir)")

print("\n=== D. SKILLS ===")
for s in ["fda-desktop-automation", "hgk-governed-execution", "force-pause-after-4-failures"]:
    p = SK / s / "SKILL.md"
    if p.exists():
        size = p.stat().st_size
        refs = [f.name for f in (SK / s / "references").glob("*.md")] if (SK / s / "references").exists() else []
        scr = [f.name for f in (SK / s / "scripts").glob("*.py")] if (SK / s / "scripts").exists() else []
        print(f"  {s}: {size}B | refs={len(refs)} {refs[:4]} | scripts={scr}")
