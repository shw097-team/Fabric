# -*- coding: utf-8 -*-
"""FDA docs internal acceptance — verify all 4 files carry correct r11-acceptance state."""
import re
import sys
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
files = {
    "README.md": FDA / "README.md",
    "AGENTS.md": FDA / "AGENTS.md",
    "TEAM.md": FDA / "TEAM.md",
    "docs/FDA_USER_GUIDE.md": FDA / "docs/FDA_USER_GUIDE.md",
}
checks = []
def chk(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

for label, p in files.items():
    chk(f"{label} exists", p.exists())
    if not p.exists():
        continue
    txt = p.read_text(encoding="utf-8")
    # r11 acceptance markers
    if label == "TEAM.md":
        chk("TEAM external_acceptance GRANTED", "external_acceptance: GRANTED" in txt)
        chk("TEAM profile_team_active PASS", "profile_team_active: PASS" in txt)
        chk("TEAM candidate_root", "be576bebe767" in txt)
        chk("TEAM evaluator", "9009713fd7" in txt)
        chk("TEAM SQS NOT_AUTHORIZED", "SQS_LIVE_TRADING = NOT_AUTHORIZED" in txt or "NOT_AUTHORIZED" in txt)
    elif label == "AGENTS.md":
        chk("AGENTS skill load", "fda-desktop-automation" in txt)
        chk("AGENTS fda_run", "fda_run.py" in txt)
        chk("AGENTS screen_state", "screen_state_check" in txt)
        chk("AGENTS zero-mouse", "FORBIDDEN" in txt and "click_input" in txt)
        chk("AGENTS r11 PASS", "r11 ALL PASS" in txt or "EXTERNAL_ACCEPTANCE GRANTED" in txt)
        chk("AGENTS claim ceiling", "NOT_AUTHORIZED" in txt)
    elif label == "README.md":
        chk("README r11 PASS", "r11 ALL PASS" in txt or "EXTERNAL ACCEPTANCE GRANTED" in txt)
        chk("README profile PASS", "FDA_PROFILE_TEAM_ACTIVE" in txt and "PASS" in txt)
        chk("README assets", "FDA_DESKTOP_CAPABILITY_MATRIX" in txt and "xq_native_adapter" in txt)
        chk("README quickstart", "screen_state_check" in txt and "fda_run" in txt)
        chk("README ceiling", "SQS_LIVE_TRADING" in txt and "NOT_AUTHORIZED" in txt)
    elif label == "docs/FDA_USER_GUIDE.md":
        chk("GUIDE r11 GRANTED", "GRANTED" in txt and "R11_ALL_PASS" in txt)
        chk("GUIDE profile PASS", "profile_team_active: PASS" in txt)
        chk("GUIDE checker 194", "194/194" in txt)
        chk("GUIDE evaluator", "9009713fd7" in txt)
        chk("GUIDE no stale 174", "174/174" not in txt or "174/174" in txt and "final checker 194" in txt)
        chk("GUIDE manifest sha", "a3496336" in txt)
        chk("GUIDE ceiling", "NOT_AUTHORIZED" in txt)

print(f"{'='*56}")
passed = sum(1 for _, ok, _ in checks if ok)
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {detail}")
print(f"{'='*56}")
print(f"RESULT: {passed}/{len(checks)} PASS")
sys.exit(0 if passed == len(checks) else 1)
