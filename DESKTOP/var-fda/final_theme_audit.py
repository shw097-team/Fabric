# -*- coding: utf-8 -*-
"""FINAL GAP AUDIT: verify 3 mandatory themes across 4 docs + 2 skills.
Theme A: 異常→查螢幕實況→確認小視窗→避免直接判卡死
Theme B: 不和用戶搶鍵盤滑鼠（零滑鼠/零焦點/background）
Theme C: 整合成功 XQ 操作流程經驗（完整路由可復用）"""
import re
import sys
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SKILLS = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development")
docs = {
    "README.md": FDA / "README.md",
    "AGENTS.md": FDA / "AGENTS.md",
    "TEAM.md": FDA / "TEAM.md",
    "docs/FDA_USER_GUIDE.md": FDA / "docs/FDA_USER_GUIDE.md",
}
skills = {
    "fda-desktop-automation": SKILLS / "fda-desktop-automation" / "SKILL.md",
    "hgk-governed-execution": SKILLS / "hgk-governed-execution" / "SKILL.md",
}

# Theme A keywords: screen check first, popup/小視窗, NOT assume frozen
A_POS = ["screen_state_check", "螢幕", "小視窗", "NEEDS_CONFIRM", "卡死", "直接重試", "hidden"]
# Theme B: no mouse/keyboard steal
B_POS = ["click_input", "set_focus", "SendInput", "foreground", "零滑鼠", "background", "搶"]
# Theme C: full XQ flow / reuse
C_POS = ["流程路由", "QUICKSTART", "control ID", "17551", "17555", "SensorLog", "SensorList", "adapter", "REUSE"]

targets = {**{f"DOC:{k}": v for k, v in docs.items()}, **{f"SKILL:{k}": v for k, v in skills.items()}}
print("=== THEME COVERAGE AUDIT (A=異常查螢幕 B=不搶滑鼠 C=流程整合) ===")
summary = {}
for label, p in targets.items():
    if not p.exists():
        print(f"  [MISSING FILE] {label}")
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    a_hits = sum(1 for k in A_POS if k in txt)
    b_hits = sum(1 for k in B_POS if k in txt)
    c_hits = sum(1 for k in C_POS if k in txt)
    summary[label] = (a_hits, b_hits, c_hits)
    flag_a = "OK" if a_hits >= 3 else "WEAK"
    flag_b = "OK" if b_hits >= 2 else "WEAK"
    flag_c = "OK" if c_hits >= 3 else "WEAK"
    print(f"  [{flag_a}/{flag_b}/{flag_c}] {label}: A={a_hits}/7 B={b_hits}/6 C={c_hits}/7")

print("\n=== DETAIL: what's MISSING per doc ===")
for label, p in targets.items():
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    miss_a = [k for k in A_POS if k not in txt]
    miss_b = [k for k in B_POS if k not in txt]
    miss_c = [k for k in C_POS if k not in txt]
    print(f"  {label}: missA={miss_a or '-'} missB={miss_b or '-'} missC={miss_c or '-'}")
