# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v6 — final known-good compile attempt.
Load existing user script xs_script (tree dbl-click, proven) -> ctrl+a ->
clipboard paste DOC-03 known-good -> pixel 儲存 -> F6 -> FILE readback only
(UIA readback of Afx syntax editor is unreliable; file is truth).
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 3376
EWIN = 1248626
USER_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
GOOD_SCRIPT = "Input: length(20);\nVariable: ma(0);\nma = Average(Close, length);\nif Close CrossOver ma then\n    Plot1(ma);"


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(mx=400, depth=25):
    return cua("get_window_state", {"pid": PID, "window_id": EWIN,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def click_frame(e, pid=PID):
    f = e.get("frame") or {}
    x = f.get("x", 0) + f.get("w", 0) // 2
    y = f.get("y", 0) + f.get("h", 0) // 2
    return cua("click", {"pid": pid, "x": x, "y": y, "delivery_mode": "foreground"}, timeout=45)


def db_user():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
                         "FROM Indicator WHERE Name LIKE 'xs_script' OR Name LIKE 'FDA_F06%'").fetchall()
    finally:
        c.close()


results = []
before = db_user()
print("DB before:", before)

# 1. expand 自訂 (1) via pixel dbl-click (tree ops proven via element click before;
#    use frame + count=2 through element_token which worked in earlier sessions)
s0 = ws()
custom = find(s0.get("elements", []), "自訂 (1)", "TreeItem")
if not custom:
    print("FAIL: 自訂 tree")
    raise SystemExit(2)
r = cua("click", {"pid": PID, "element_token": custom.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id"), "count": 2}, timeout=60)
print("自訂 dbl:", json.dumps(r, ensure_ascii=False)[:80])
time.sleep(4)

# 2. find xs_script under 自訂 and dbl-click load
s1 = ws(500, 30)
xs = find(s1.get("elements", []), "xs_script", "TreeItem")
print("xs_script item:", xs.get("element_index") if xs else None)
if not xs:
    print("FAIL: xs_script not visible (self-created scripts may be under 自訂; listing)")
    for e in s1.get("elements", []):
        if e.get("role") == "TreeItem" and e.get("depth", 0) >= 6:
            print("   ", e.get("depth"), (e.get("label") or "")[:30])
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": xs.get("element_token"),
              "snapshot_id": s1.get("snapshot_id"), "count": 2}, timeout=60)
time.sleep(4)

# 3. editor now shows xs_script; ctrl+a + clipboard paste
cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
time.sleep(2)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
time.sleep(1)
cua("clipboard_write", {"text": GOOD_SCRIPT}, timeout=30)
time.sleep(1)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "v", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
print("paste sent")
time.sleep(3)

# 4. pixel 儲存
s2 = ws()
save_btn = find(s2.get("elements", []), "儲存", "Button")
if save_btn:
    click_frame(save_btn)
    print("儲存 pixel clicked")
    time.sleep(5)

# save dialog if any: type name + confirm
import subprocess as sp
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    t = (w.get("title") or "")
    if ("另存" in t or "儲存" in t) and w.get("pid") == PID:
        print("DLG:", repr(t[:40]))
        dw = w.get("window_id")
        sd = cua("get_window_state", {"pid": PID, "window_id": dw, "max_elements": 200}, timeout=45)
        for e in sd.get("elements", []):
            if e.get("role") == "Edit":
                cua("type_text", {"pid": PID, "window_id": dw, "element_token": e.get("element_token"),
                                  "text": "xs_script", "delivery_mode": "foreground"}, timeout=45)
                time.sleep(1)
                break
        ok = find(sd.get("elements", []), "確定", "Button") or find(sd.get("elements", []), "儲存", "Button")
        if ok:
            click_frame(ok)
            time.sleep(5)

# 5. F6 compile
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
print("F6 sent")
time.sleep(12)

# 6. FILE readback (truth)
after = db_user()
print("DB after :", after)
compiled_ok = after is not None and any(r[1] in (0, 1) for r in after)
delta = before != after
results.append(("FILE_READBACK_COMPILE_STATUS", compiled_ok, f"rows={after}"))
results.append(("FILE_DELTA", delta, f"before={before} after={after}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v6 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V6_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V6",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture": "DOC-03 CH-02.2 known-good indicator syntax (authority)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus (UIA readback unreliable on Afx editor)",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script xs_script body replaced + recompiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V6_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
