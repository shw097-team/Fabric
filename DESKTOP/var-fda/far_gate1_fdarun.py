# -*- coding: utf-8 -*-
"""FAR research (Gate 1): does putting 'fda_run.py as sole execution path' into the
fabric-desktop-automation blueprint (Step 6 execution surface) have substantive value?
3-source evidence: (1) on-disk blueprint Step 6 text, (2) skill routing authority,
(3) execution reality (which path scripts actually use today)."""
from pathlib import Path

BLUEPRINT = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\fabric-desktop-automation_藍圖_v2026.08.13-r2.md")
SKILL = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation\SKILL.md")
VFD = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")

print("=== 源1: 藍圖 Step 6 執行面 ===")
if BLUEPRINT.exists():
    txt = BLUEPRINT.read_text(encoding="utf-8", errors="replace")
    # find Step 6 section
    import re
    for m in re.finditer(r"Step 6|STEP 6|步驟 6", txt):
        s = max(0, m.start() - 50)
        print(f"  ...{txt[s:m.start()+150].replace(chr(10),' | ')[:200]}")
        break
    print(f"  藍圖含 fda_run 字樣: {'fda_run' in txt}")
    print(f"  藍圖含 screen_state_check 字樣: {'screen_state_check' in txt}")
else:
    print("  藍圖檔不存在!")

print("\n=== 源2: FDA skill 執行路徑權威 ===")
if SKILL.exists():
    t = SKILL.read_text(encoding="utf-8", errors="replace")
    print(f"  skill 含 fda_run.py: {'fda_run.py' in t}")
    print(f"  skill 含 '必須經' / '唯一執行': {'必須經' in t or '唯一' in t}")
else:
    print("  skill 檔不存在!")

print("\n=== 源3: 執行現況 — 最近腳本是否走 fda_run ===")
import os, time
now = time.time()
via_run = 0
direct = 0
for p in sorted(VFD.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
    age = (now - p.stat().st_mtime) / 60
    print(f"  {p.name}  {age:.0f} 分前")
print(f"\n  主目錄腳本總數: {len(list(VFD.glob('*.py')))}")
print(f"  fda_run.py 存在: {(VFD/'fda_run.py').exists()}")
print(f"  screen_state_check.py 存在: {(VFD/'screen_state_check.py').exists()}")
print(f"  fda_script_guard.py 存在: {(VFD/'fda_script_guard.py').exists()}")
