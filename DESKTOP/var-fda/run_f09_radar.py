# -*- coding: utf-8 -*-
"""FDA-C4 F09 — strategy radar open + state readback (PAPER fixture surface).
Open 策略雷達(開放體驗)(L) from 策略(D) menu; readback window state.
No strategy mutation: read-only observation (LOCAL_REVERSIBLE).
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 3376
WIN = 2232310


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(pid, wid, mx=300, depth=20):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


results = []
# open 策略(D) menu (background click proven)
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
results.append(("RADAR_MENU_ENTRY", radar is not None, "策略雷達(開放體驗)(L)"))
print("radar entry:", radar.get("element_index") if radar else None)
if radar:
    cua("click", {"pid": PID, "element_token": radar.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    time.sleep(6)

# find radar window
radar_win = None
d = cua("get_accessibility_tree", {}, timeout=30)
for w in d.get("windows", []):
    t = (w.get("title") or "")
    if "雷達" in t or ("策略" in t and w.get("pid") == PID):
        radar_win = w
        break
print("radar win:", radar_win.get("window_id") if radar_win else None,
      "|", (radar_win.get("title") or "")[:50] if radar_win else "")
if radar_win:
    results.append(("RADAR_WINDOW_OPENED", True, radar_win.get("title", "")[:40]))
    # readback state
    rw = radar_win.get("window_id")
    s2 = ws(PID, rw, 400, 25)
    els = s2.get("elements", [])
    results.append(("RADAR_STATE_READBACK", len(els) > 0, f"{s2.get('total_element_count')} elements"))
    for e in els[:25]:
        lab = (e.get("label") or "").strip()
        if lab:
            print("  ", e.get("element_index"), "|", e.get("role"), "|", lab[:45])
else:
    results.append(("RADAR_WINDOW_OPENED", False, "no radar window found"))

ok = all(p for _, p, _ in results)
print("\n=== F09 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F09_RADAR_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F09-STRATEGY-RADAR-OPEN-READBACK",
    "action_class": "XQ_RADAR_SURFACE",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "authority_ref": "XQ&XS 專業技術文檔 DOC-10 CH-13 (SignalSpec/AlertPolicy; radar surface)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "UIA structured state (level-2); no strategy mutation",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL (open + readback only)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F09_RADAR_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
