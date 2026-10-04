# -*- coding: utf-8 -*-
"""FAR evidence: audit this session's XQ anomaly-handling against the fixed route
(screen_state_check FIRST before any disposition). Reconstruct from receipts/timestamps."""
import json
import os
import time
from pathlib import Path

RECEIPTS = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts")
VFD = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")

print("=== 本輪 PAPER 10x 嘗試時間線（receipt + 腳本 mtime）===")
for p in sorted(RECEIPTS.glob("FDA_XQ_PAPER_10RUN*"), key=lambda x: x.stat().st_mtime):
    t = time.strftime("%H:%M:%S", time.localtime(p.stat().st_mtime))
    sz = p.stat().st_size
    verdict = ""
    try:
        d = json.load(open(p, encoding="utf-8"))
        verdict = d.get("verdict", "?")
        runs = d.get("runs", [])
        ok = sum(1 for r in runs if r.get("status") == "OK" or r.get("sensorlist_persisted"))
        verdict = f"{verdict} ({len(runs)} runs, {ok} persisted)"
    except Exception as e:
        verdict = f"read-err {e}"
    print(f"  {t}  {p.name}  {sz}B  {verdict}")

print("\n=== 相關腳本建立時間 ===")
for name in ["rr6_paper_10x.py", "rr6_paper_10x_v2.py", "rr6_paper_10x_v3.py",
             "rr6_paper_10x_v4.py", "rr6_f01_current.py", "rr6_open_radar.py",
             "rr6_close_leftover_dlgs.py"]:
    p = VFD / name
    if p.exists():
        t = time.strftime("%H:%M:%S", time.localtime(p.stat().st_mtime))
        print(f"  {t}  {name}")

print("\n=== screen_state_check.py 本輪是否被調用？（無直接記錄，只能看 mtime）===")
p = VFD / "screen_state_check.py"
if p.exists():
    t = time.strftime("%H:%M:%S", time.localtime(p.stat().st_mtime))
    print(f"  screen_state_check.py mtime: {t} (08-14)")
