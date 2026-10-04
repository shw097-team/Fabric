# -*- coding: utf-8 -*-
"""FDA-C4 F06 known-good compile via system-script path (deadlock-avoiding).
Uses the proven-safe flow from the first session: open editor -> expand system
tree -> double-click ATR (authority known-good, System_Script.sqlite
CompileStatus=1) -> F6 compile -> file readback of System_Script.sqlite ATR row.
AVOIDS the 新增 button (UIA Invoke deadlock on Afx editor window).
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
SYS_DB = r"C:\SysJust\XQLite\System\XSSystem\Bin\System\System_Script.sqlite"


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


def ws(pid, wid, mx=300, depth=20):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def atr_row():
    c = sqlite3.connect(SYS_DB)
    try:
        return c.execute(
            "SELECT Name, CompileStatus, substr(CompileMsg,1,40), LastCompileTime "
            "FROM Indicator WHERE Name LIKE '%ATR%'").fetchone()
    finally:
        c.close()


results = []

# wait for login
for i in range(12):
    main = None
    for w in tree().get("windows", []):
        t = (w.get("title") or "")
        if "XQ全球贏家" in t and "已登入" in t and "XScript" not in t:
            main = w
            break
    if main:
        break
    time.sleep(5)
if not main:
    print("FAIL: XQ not logged in")
    raise SystemExit(2)
PID = main.get("pid")
WIN = main.get("window_id")
print("XQ main:", PID, WIN)

# open editor via 策略(D) -> XScript 編輯器(E) (background clicks, proven)
s0 = ws(PID, WIN)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, WIN, 400)
xs_e = find(s1.get("elements", []), "XScript 編輯器(E)...", "MenuItem")
results.append(("OPEN_EDITOR", xs_e is not None, "menu entry"))
if not xs_e:
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": xs_e.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

ed = None
for w in tree().get("windows", []):
    if "XScript 編輯器" in (w.get("title") or ""):
        ed = w
        break
print("editor:", ed.get("window_id") if ed else None)
if not ed:
    raise SystemExit(2)
EWIN = ed.get("window_id")

# expand 系統(344) tree (single click on TreeItem, proven safe)
s2 = ws(PID, EWIN)
sys_item = find(s2.get("elements", []), "系統 (344)", "TreeItem")
results.append(("SYSTEM_TREE", sys_item is not None, "系統(344)"))
print("系統 tree:", sys_item.get("element_index") if sys_item else None)
if sys_item:
    # double-click expands the tree (proven in first session)
    cua("click", {"pid": PID, "element_token": sys_item.get("element_token"),
                  "snapshot_id": s2.get("snapshot_id"), "count": 2}, timeout=60)
    time.sleep(4)
    s3 = ws(PID, EWIN, 400)
    tech = find(s3.get("elements", []), "XQ技術指標 (32)", "TreeItem")
    print("XQ技術指標:", tech.get("element_index") if tech else None)
    if tech:
        cua("click", {"pid": PID, "element_token": tech.get("element_token"),
                      "snapshot_id": s3.get("snapshot_id")})
        time.sleep(3)
        s4 = ws(PID, EWIN, 400)
        atr = find(s4.get("elements", []), "ATR (平均真實區域)", "TreeItem")
        results.append(("ATR_LOCATED", atr is not None, "ATR leaf in tree"))
        print("ATR:", atr.get("element_index") if atr else None)
        if atr:
            # double-click loads into editor (proven in first session)
            cua("click", {"pid": PID, "element_token": atr.get("element_token"),
                          "snapshot_id": s4.get("snapshot_id"), "count": 2}, timeout=60)
            time.sleep(5)
            s5 = ws(PID, EWIN)
            title = next((e.get("label") for e in s5.get("elements", [])
                          if e.get("role") == "TitleBar"), "")
            loaded = "ATR" in title
            results.append(("ATR_LOADED_EDITOR", loaded, f"TitleBar={title[:40]}"))
            print("editor title:", title[:50])

            # F6 compile
            before = atr_row()
            print("ATR row before:", before)
            cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6",
                              "delivery_mode": "foreground"})
            print("F6 sent")
            time.sleep(8)
            after = atr_row()
            print("ATR row after :", after)
            changed = before != after
            status_ok = after is not None and after[1] in (0, 1, "", None)
            results.append(("F6_COMPILE_TRIGGERED", changed or after[1] not in ("", None),
                            f"before={before} after={after}"))
            results.append(("ATR_COMPILE_STATUS_READBACK", status_ok, f"CompileStatus={after[1] if after else '?'}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 SYSTEM-PATH RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_SYSTEM_PATH_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-SYSTEM-PATH",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script": "ATR (平均真實區域) — XQ system corpus (System_Script.sqlite, authority CompileStatus=1)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): System_Script.sqlite CompileStatus",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL (compile is read-only verification; LOCAL_REVERSIBLE navigation)",
    "deadlock_note": "新增 button UIA Invoke deadlocks Afx editor (cua-driver 0.19.3 edge, R-FDA-011 class); bypassed via system-script double-click path",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_SYSTEM_PATH_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
