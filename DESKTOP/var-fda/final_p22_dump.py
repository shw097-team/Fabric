# -*- coding: utf-8 -*-
"""FINAL P22: uia full dump of radar window — find FDAPaperProbe234930 anywhere."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

du = Desktop(backend="uia")
RADAR = 0x110d96
ru = du.window(handle=RADAR)
print("radar uia exists:", ru.exists(timeout=3))

# full descendants scan (bounded) — collect all text-bearing controls
found = []
try:
    for c in ru.descendants():
        try:
            t = c.window_text()
            if t and t.strip():
                found.append((c.control_type(), t.strip()[:60]))
        except Exception:
            pass
except Exception as e:
    print("scan err:", str(e)[:80])

print(f"total text controls: {len(found)}")
# search for our strategy
hits = [x for x in found if "FDAPaper" in x[1] or "Probe" in x[1]]
print("FDAPaper hits:", hits)
# show unique first 40
seen = set()
for ct, t in found:
    if t not in seen:
        seen.add(t)
        print(f"  {ct}: {t}")
    if len(seen) > 45:
        print("  ... (truncated)")
        break
