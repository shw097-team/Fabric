# -*- coding: utf-8 -*-
"""Classify violations: REAL_CALL (code executes banned API) vs STRING_ONLY (banned text in
docstring/comment/assert message). Quarantine REAL_CALL files."""
import re
import shutil
from pathlib import Path

D = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
Q = D / "quarantined_violations"

REAL_PATTERNS = [
    r"\.click_input\s*\(", r"\.set_focus\s*\(", r"\.send_keystrokes\s*\(", r"\.send_keys\s*\(",
    r"SetCursorPos\s*\(", r"SendInput\s*\(", r"SetForegroundWindow\s*\(",
    r"mouse_event\s*\(", r"keybd_event\s*\(", r"bring_to_front",
    r"delivery_mode\s*=\s*['\"]foreground",
]
# string-style API calls — VIOLATION only for foreground delivery / bring_to_front
STRING_STYLE_PATTERNS = [
    r"['\"]bring_to_front['\"]", r"['\"]foreground['\"]",
    r"['\"]delivery_mode['\"]\s*:\s*['\"]foreground",
]

def classify(path: Path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    real = []
    for i, line in enumerate(lines, 1):
        # pass 1: string-style API calls (cua/json arg form) — check BEFORE stripping strings
        for pat in STRING_STYLE_PATTERNS:
            if re.search(pat, line):
                real.append((i, line.strip()[:80], pat))
                break
        else:
            # pass 2: strip strings for REAL call detection
            code = re.sub(r"(['\"]).*?\1", '""', line)
            code = re.sub(r"#.*$", "", code)
            for pat in REAL_PATTERNS:
                if re.search(pat, code):
                    real.append((i, line.strip()[:80], pat))
                    break
    return real

real_files = {}
string_only = []
for p in sorted(D.glob("*.py")):
    if p.name == "fda_script_guard.py":
        continue
    real = classify(p)
    if real:
        real_files[p.name] = real
    else:
        # still flag if banned text appears anywhere (informational)
        txt = p.read_text(encoding="utf-8", errors="replace").lower()
        if any(k in txt for k in ["click_input", "set_focus", "sendinput", "setcursorpos", "send_keystrokes"]):
            string_only.append(p.name)

print(f"REAL_CALL files: {len(real_files)}")
for name, hits in sorted(real_files.items()):
    for ln, txt, pat in hits:
        print(f"  {name}:{ln} [{pat}] {txt}")
print(f"\nSTRING_ONLY (docstring/assert mention, no real call): {len(string_only)}")
for n in string_only:
    print(f"  {n}")

# quarantine REAL_CALL files
Q.mkdir(exist_ok=True)
for name in real_files:
    shutil.copy2(D / name, Q / name)
print(f"\nquarantined {len(real_files)} files -> {Q}")
