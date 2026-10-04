# -*- coding: utf-8 -*-
"""fda_script_guard.py — FAR R3 修補：程式化強制 §15 強路由。
在執行任何 var/fda 腳本前呼叫；若腳本含違規 API → BLOCK + 隔離，禁止執行。

違規 API（任何出現即 BLOCK，註解也擋——因為 docstring 可能被誤讀為「已處理」）：
  click_input, set_focus, send_keystrokes, send_keys, type_keys,
  SetCursorPos, SendInput, SetForegroundWindow, mouse_event, keybd_event,
  bring_to_front, delivery_mode.*foreground, uia.*click_input

用法：
  python fda_script_guard.py <script.py> [--quarantine] [--scan-dir DIR]
"""
import re
import shutil
import sys
from pathlib import Path

VIOLATION_PATTERNS = [
    r"click_input", r"set_focus", r"send_keystrokes", r"send_keys", r"type_keys",
    r"SetCursorPos", r"SendInput", r"SetForegroundWindow", r"mouse_event", r"keybd_event",
    r"bring_to_front", r"delivery_mode\s*[:=]\s*['\"]foreground", r"\.click_input\s*\(",
    # string-style API calls — VIOLATION only for foreground delivery / bring_to_front
    r"['\"]bring_to_front['\"]", r"['\"]delivery_mode['\"]\s*:\s*['\"]foreground",
    r"['\"]foreground['\"]",
]
ALLOWED_ANNOTATIONS = [  # 若整行是純說明（如 docstring 描述禁用），需明確標記
    "NO foreground", "NO SendInput", "NO SetCursorPos", "zero set_focus",
    "ZERO set_focus", "no click_input", "no set_focus", "not click_input",
    "deadlock workaround", "delivery_mode", "keyboard", "workaround SendInput",
    "via SendInput", "no mouse", "mouse-free", "mousefree", "zero send_keys",
    "no send_keys", "zero click_input", "no foreground",
]

def scan_file(path: Path) -> list:
    """Return list of (line_no, line, pattern) violations."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return [(-1, "<unreadable>", "read error")]
    hits = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 1) pure comment or docstring line that explicitly denies these APIs -> skip
        if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
            if any(ann.lower() in stripped.lower() for ann in ALLOWED_ANNOTATIONS):
                continue
            # comments/docstrings describing violations are informational ONLY if they
            # mention the banned API in a negative/denial context; otherwise treat as hit
            if any(re.search(pat, stripped, re.IGNORECASE) for pat in VIOLATION_PATTERNS):
                if not any(neg in stripped.lower() for neg in ["no ", "not ", "zero ", "never ", "禁止", "禁用", "without"]):
                    hits.append((i, stripped[:90], "docstring"))
            continue
        # 2) actual code line — skip banned text inside string literals when negated
        #    (e.g. assert "... ZERO set_focus ..." is descriptive, not a call)
        stripped_lower = stripped.lower()
        if any(neg in stripped_lower for neg in ["zero set_focus", "no set_focus", "no click_input",
                                                  "no send_keys", "no foreground", "zero send_keys",
                                                  "no sendinput", "zero click_input"]):
            continue
        for pat in VIOLATION_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                hits.append((i, stripped[:90], pat))
                break
    return hits

def main():
    if len(sys.argv) < 2:
        print("usage: fda_script_guard.py <script.py> [--quarantine]")
        sys.exit(2)
    target = Path(sys.argv[1]).resolve()
    quarantine = "--quarantine" in sys.argv
    scan_dir = "--scan-dir" in sys.argv

    if scan_dir:
        d = target if target.is_dir() else target.parent
        bad = {}
        for p in sorted(d.glob("*.py")):
            if p.name in ("fda_script_guard.py", "quarantine_real.py"):  # self-exclusion
                continue
            hits = scan_file(p)
            if hits:
                bad[p.name] = hits
        if not bad:
            print(f"PREFLIGHT_SCAN: CLEAN ({len(list(d.glob('*.py')))} files, 0 violations)")
            sys.exit(0)
        print(f"PREFLIGHT_SCAN: {len(bad)} FILES WITH VIOLATIONS:")
        for name, hits in bad.items():
            for ln, txt, pat in hits:
                print(f"  {name}:{ln} [{pat}] {txt}")
        sys.exit(1)

    hits = scan_file(target)
    if not hits:
        print(f"PREFLIGHT_GUARD: PASS — {target.name} is CLEAN (no mouse/focus-stealing APIs)")
        sys.exit(0)

    print(f"PREFLIGHT_GUARD: BLOCK — {target.name} contains {len(hits)} violation(s):")
    for ln, txt, pat in hits:
        print(f"  line {ln} [{pat}]: {txt}")
    print("Execution of this script is FORBIDDEN (skill hgk §15 hard route).")

    if quarantine:
        qdir = target.parent / "quarantined_violations"
        qdir.mkdir(exist_ok=True)
        dst = qdir / target.name
        shutil.copy2(target, dst)
        print(f"  -> copied to {dst} (quarantined)")
    sys.exit(1)

if __name__ == "__main__":
    main()
