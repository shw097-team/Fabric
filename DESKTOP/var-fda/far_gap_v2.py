# -*- coding: utf-8 -*-
"""FAR GAP COMPARISON v2 — corrected (per-item any-key match) + tool-presence + discoverability checks."""
from pathlib import Path

FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SK = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development")

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

items = {
    "SSC-V2 (dynamic pid/hidden/NEEDS_CONFIRM)": ["SSC-V2", "NEEDS_CONFIRM", "hidden"],
    "skill oversized → split+route + guarded slim": ["OVERSIZED SKILL ROUTE", "skill_guard", "拆分"],
    "checker_history 194 ONLY CURRENT": ["194", "HISTORICAL", "CURRENT"],
    "atomic reseal / machine-generated manifest": ["reseal", "machine-generat", "SINGLE_CANONICAL"],
    "candidate_root be576be": ["be576bebe767"],
    "evaluator 9009713 structured": ["9009713"],
    "exact_set derived counters": ["exact_set", "manifest_row_count", "payload_file_count"],
    "generated_at > bound evidence": ["generated_at", "chronology"],
}

print("=== v2 CORRECTED MATRIX (any-key per item) ===")
for item, keys in items.items():
    found = [label for label, txt in corpus.items() if any(k in txt for k in keys)]
    print(f"  {'OK ' if found else 'GAP'} {item}: {found if found else 'NOWHERE'}")

print("\n=== TOOL PRESENCE (do referenced tools exist where docs claim?) ===")
tool_checks = [
    ("screen_state_check.py @ var/fda", Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\screen_state_check.py")),
    ("screen_state_check.py @ fda skill refs", SK / "fda-desktop-automation" / "references" / "screen_state_check.py"),
    ("FDA_PREFLIGHT_GUARD.py @ var/fda", Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\fda_script_guard.py")),
    ("FDA_PREFLIGHT_GUARD.py @ fda skill refs", SK / "fda-desktop-automation" / "references" / "fda_script_guard.py"),
    ("fda_run.py @ var/fda", Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\fda_run.py")),
    ("fda_run.py @ fda skill scripts", SK / "fda-desktop-automation" / "scripts" / "fda_run.py"),
    ("hgk_evidence_preflight.py @ var/fda", Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\hgk_evidence_preflight.py")),
    ("hgk_evidence_preflight.py @ hgk skill", SK / "hgk-governed-execution" / "scripts" / "hgk_evidence_preflight.py"),
    ("skill_guard.py @ var/fda", Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\skill_guard.py")),
    ("skill_guard.py @ hgk skill", SK / "hgk-governed-execution" / "scripts" / "skill_guard.py"),
    ("FDA_ASSET_REGISTRY.json", FDA / "FDA_ASSET_REGISTRY.json"),
    ("xq_native_adapter.py", FDA / "xq_native_adapter.py"),
    ("independent_checker.py", FDA / "independent_checker.py"),
]
for label, p in tool_checks:
    print(f"  {'OK ' if p.exists() else 'MISSING'} {label}")

print("\n=== DISCOVERABILITY (would a new session find these?) ===")
# fda skill description (system prompt shows first 57 chars)
fd = (SK / "fda-desktop-automation" / "SKILL.md").read_text(encoding="utf-8")
import re
m = re.search(r"^description: (.+)$", fd, re.M)
print(f"  fda skill description: {m.group(1) if m else 'MISSING'}")
hg = (SK / "hgk-governed-execution" / "SKILL.md").read_text(encoding="utf-8")
m2 = re.search(r"^description: (.+)$", hg, re.M)
print(f"  hgk skill description: {m2.group(1) if m2 else 'MISSING'}")
