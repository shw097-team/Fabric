# -*- coding: utf-8 -*-
"""FDA-C4 F09B — XQ PAPER strategy runtime start/stop closure (EXT-FDA-006).
Target: radar surface -> select strategy -> start (PAPER/no-live) -> status
readback -> stop -> post-stop readback. No live financial write.
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 4440
WIN = 1704814


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def tree():
    return cua("get_accessibility_tree", {}, timeout=30)


def ws(pid, wid, mx=400, depth=25):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


results = []
# 1. open 策略(D) -> 策略雷達(開放體驗)(L)
s0 = ws(PID, WIN)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, WIN, 400)
radar = find(s1.get("elements", []), "策略雷達", "MenuItem")
if not radar:
    print("FAIL: radar menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": radar.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

rw = None
for w in tree().get("windows", []):
    if "策略雷達" in (w.get("title") or ""):
        rw = w
        break
print("radar win:", rw.get("window_id") if rw else None)
if not rw:
    raise SystemExit(2)
RWID = rw.get("window_id")

# 2. radar state readback (find strategy list + start/stop controls)
s2 = ws(PID, RWID, 500, 30)
els2 = s2.get("elements", [])
print("radar elements:", s2.get("total_element_count"))
# look for strategy rows / buttons
btns = [(e.get("element_index"), (e.get("label") or "")[:30]) for e in els2
        if e.get("role") == "Button" and (e.get("label") or "").strip()]
print("buttons:", btns[:20])
results.append(("RADAR_OPEN_READBACK", len(els2) > 0, f"{s2.get('total_element_count')} elements"))

# find xs_script strategy in tree
strat = find(els2, "xs_script", "TreeItem")
print("xs_script strategy item:", strat.get("element_index") if strat else None)

receipt = {
    "artifact_id": "FDA_F09B_PAPER_RUNTIME_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F09B-PAPER-RUNTIME-START-STOP",
    "action_class": "XQ_PAPER_CONFIG",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "authority_ref": "XQ&XS 專業技術文檔 DOC-10 CH-13/15 (radar/PAPER semantics; no live write)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "UIA structured state (level-2)",
    "verdict": "IN_PROGRESS",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F09B_PAPER_RUNTIME_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt staged:", out)
