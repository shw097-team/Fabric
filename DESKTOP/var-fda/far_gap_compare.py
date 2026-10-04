# -*- coding: utf-8 -*-
"""FAR GAP COMPARISON: session knowledge inventory vs what's landed in docs/skills.
Enumerate ALL knowledge items produced this session (from git history + receipts + tools)
and check each appears in: 4 docs / fda skill / hgk skill / force-pause skill."""
import re
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SK = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development")

# collect all text from docs + skills
corpus = {}
for label, p in [
    ("README", FDA / "README.md"),
    ("AGENTS", FDA / "AGENTS.md"),
    ("TEAM", FDA / "TEAM.md"),
    ("GUIDE", FDA / "docs" / "FDA_USER_GUIDE.md"),
    ("SKILL:fda", SK / "fda-desktop-automation" / "SKILL.md"),
    ("SKILL:hgk", SK / "hgk-governed-execution" / "SKILL.md"),
    ("SKILL:pause", SK / "force-pause-after-4-failures" / "SKILL.md"),
]:
    corpus[label] = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

# knowledge items from this session (RR6→r11), grouped
items = {
    # A. runtime/qualification facts
    "F01 current 260811 10/10": ["F01_CURRENT", "260811", "10/10"],
    "F06 fresh 10x distinct timestamps": ["F06_FRESH", "F06", "fresh"],
    "UFO2 effective-load 7/7": ["UFO", "7/7"],
    "PAPER single-wash 10x": ["PAPER", "single-wash", "10x"],
    "PAPER STOP semantics authority": ["STOP_SEMANTICS", "AUTHORITY_RR8", "authority"],
    "checker 194/194 evaluator 9009713": ["194/194", "9009713"],
    # B. operational traps (verified)
    "toolbar TB_PRESSBUTTON ineffective → pywinauto click": ["TB_PRESSBUTTON", "pywinauto", "tb.button"],
    "XTP self-drawn button → WM_CLOSE": ["WM_CLOSE", "XTP"],
    "SensorList flush delay >15s": ["flush", "15s", "SensorList"],
    "SensorLog needs LIKE query": ["LIKE", "XQSensorName"],
    "single-wash terminal state 2->3 exec 1->5": ["2", "3", "1", "5", "state", "exec"],
    "new-success dialog title 時間：[HH:MM:SS]": ["時間", "HH:MM:SS"],
    "error dialog same title → 加入(&A) distinguish": ["加入(&A)", "該名稱已被使用"],
    "radar open via 警示提示 策略雷達(&A) button": ["策略雷達(&A)", "警示提示"],
    "main window startswith match": ["startswith", "XQ全球贏家"],
    "cua background click ineffective on XTP grid → engine truth": ["engine truth", "SensorLog", "uia"],
    "STOP effect: state 0/exec 527 appears": ["527", "state 0"],
    # C. governance/routing knowledge
    "SSC-V2 dynamic pid + hidden + NEEDS_CONFIRM": ["SSC-V2", "NEEDS_CONFIRM", "hidden", "dynamic"],
    "zero-mouse hard route": ["click_input", "set_focus", "SendInput", "foreground"],
    "REUSE-FIRST asset registry": ["REUSE-FIRST", "FDA_ASSET_REGISTRY"],
    "fda_run.py unified executor": ["fda_run"],
    "preflight guard": ["PREFLIGHT_GUARD"],
    "hgk_evidence_preflight machine gate": ["hgk_evidence_preflight"],
    "manifest one-time regeneration + HISTORICAL in body": ["HISTORICAL", "superseded_by", "regenerat"],
    "CLOSED authority gate (receipt cited)": ["CLOSED", "receipt", "authority"],
    "skill oversized → split+route, guarded slim": ["oversized", "split", "skill_guard", "瘦身"],
    "force-pause → FAR Gate 1 before proposing": ["FAR Gate 1", "呈報", "force-pause"],
    "single evidence MD full-embed no self-hash": ["self-hash", "raw body", "embedded"],
}

print("=== KNOWLEDGE × PLACEMENT MATRIX ===")
print("(✓=found in that source, ·=missing)")
gaps = []
for item, keys in items.items():
    found_in = []
    for label, txt in corpus.items():
        if all(k in txt for k in keys):
            found_in.append(label)
    if not found_in:
        gaps.append(item)
    print(f"  {'OK ' if found_in else 'GAP'} {item}: {found_in if found_in else 'NOWHERE'}")

print(f"\n=== TOTAL: {len(items)} items, {len(gaps)} GAPS ===")
for g in gaps:
    print(f"  GAP: {g}")
