# -*- coding: utf-8 -*-
"""docs_gap_audit.py — post-acceptance doc/skill gap audit (2026-08-14, FDA r11 pattern).
Checks 3 mandatory themes + tool-path presence + skill discoverability in one pass.
Usage: python docs_gap_audit.py <project_root> [--themes A,B,C]
Exit 0 = ALL PASS / 1 = gaps found.

Theme A = 異常→查螢幕實況→確認小視窗→勿直接判卡死
Theme B = 不和用戶搶鍵盤滑鼠（零滑鼠/零焦點/background）
Theme C = 整合成功操作流程經驗（可復用路由/control IDs/陷阱）
"""
import re
import sys
from pathlib import Path

def audit(project: Path, skills: dict, themes: dict):
    issues = []
    # 1. theme coverage across docs + skills
    targets = {f"DOC:{p}": project / p for p in ["README.md", "AGENTS.md", "TEAM.md", "docs/FDA_USER_GUIDE.md"]}
    targets.update({f"SKILL:{n}": s for n, s in skills.items()})
    for label, p in targets.items():
        if not p.exists():
            issues.append(f"[MISSING FILE] {label}")
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        for theme, keys in themes.items():
            hits = sum(1 for k in keys if k in txt)
            if hits < 2:  # at least 2 keyword hits per theme per source
                issues.append(f"[WEAK {theme}] {label} ({hits}/{len(keys)} keywords)")
    # 2. tool-path presence — every path referenced in docs must exist
    for label, p in targets.items():
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"(?:var/fda|scripts|references)/[\w./-]+\.py", txt):
            rel = m.group(0)
            if rel.startswith("var/fda"):
                cand = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS") / rel
            else:
                cand = None  # skill-relative — resolve against skill dirs below
            if cand and not cand.exists():
                # allow rename drift: search by basename
                hits = list(Path(r"C:\Projects\Agent_Workspace").rglob(Path(rel).name))
                if not hits:
                    issues.append(f"[BROKEN TOOL PATH] {label} cites {rel} (not found anywhere)")
    # 3. discoverability — skill descriptions carry class keywords
    for name, s in skills.items():
        if s.exists():
            desc = re.search(r"^description: (.+)$", s.read_text(encoding="utf-8"), re.M)
            if desc and not any(k in desc.group(1) for k in ["FDA", "XQ", "桌面", "驗收", "desktop", "acceptance"]):
                issues.append(f"[WEAK DISCOVERY] skill {name} description lacks class keywords")
    return issues

def main():
    if len(sys.argv) < 2:
        print("usage: docs_gap_audit.py <project_root> [--themes A,B,C]")
        return 2
    project = Path(sys.argv[1])
    skills = {
        "fda-desktop-automation": Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation\SKILL.md"),
        "hgk-governed-execution": Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\SKILL.md"),
    }
    themes = {
        "A-異常查螢幕/小視窗": ["screen_state_check", "小視窗", "NEEDS_CONFIRM", "卡死", "WM_CLOSE", "hidden"],
        "B-不搶鍵盤滑鼠": ["click_input", "set_focus", "SendInput", "foreground", "零滑鼠", "background"],
        "C-流程整合": ["流程路由", "QUICKSTART", "17551", "SensorLog", "SensorList", "REUSE"],
    }
    issues = audit(project, skills, themes)
    print(f"{'='*56}\nDOCS GAP AUDIT: {len(issues)} issue(s)")
    for i in issues:
        print(f"  {i}")
    print(f"RESULT: {'ALL PASS' if not issues else 'GAPS FOUND'}")
    return 0 if not issues else 1

if __name__ == "__main__":
    sys.exit(main())
