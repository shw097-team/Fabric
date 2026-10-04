# -*- coding: utf-8 -*-
"""FAR evidence: which XQ automation scripts reference screen_state_check (the fixed route)."""
from pathlib import Path

D = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
Q = D / "quarantined_violations"

print("=== 主目錄腳本引用 screen_state_check 統計 ===")
total = 0
with_ref = 0
for p in sorted(D.glob("*.py")):
    if p.name in ("fda_script_guard.py", "quarantine_real.py", "screen_state_check.py"):
        continue
    total += 1
    txt = p.read_text(encoding="utf-8", errors="replace")
    if "screen_state_check" in txt:
        with_ref += 1
print(f"主目錄腳本: {total} 個, 引用 screen_state_check: {with_ref} 個")

print("\n=== 隔離區(rr6/run 系列)引用統計 ===")
total2 = 0
with_ref2 = 0
for p in sorted(Q.glob("*.py")):
    total2 += 1
    txt = p.read_text(encoding="utf-8", errors="replace")
    if "screen_state_check" in txt:
        with_ref2 += 1
print(f"隔離區腳本: {total2} 個, 引用 screen_state_check: {with_ref2} 個")

print("\n=== 引用 screen_state_check 的腳本清單(主目錄) ===")
for p in sorted(D.glob("*.py")):
    if p.name in ("fda_script_guard.py", "quarantine_real.py", "screen_state_check.py"):
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    if "screen_state_check" in txt:
        n = txt.count("screen_state_check")
        print(f"  {p.name} ({n} 次)")

print("\n=== 最近修改的 XQ 操作腳本 (10 分鐘內, 主目錄) ===")
import os, time
now = time.time()
recent = []
for p in sorted(D.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True)[:15]:
    age = (now - p.stat().st_mtime) / 60
    ref = "HAS screen_state_check" if "screen_state_check" in p.read_text(encoding="utf-8", errors="replace") else "NO ref"
    print(f"  {p.name}  {age:.0f} 分前  {ref}")
