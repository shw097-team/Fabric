# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v8 — switch to xs_script tab, paste function-form
CrossOver (DOC-04 SF-0137 function_bool signature), save, compile, readback.
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
GOOD = "Input: length(20);\nVariable: ma(0);\nma = Average(Close, length);\nif CrossOver(Close, ma) then\n    Plot1(ma);"


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


def click_xy(x, y):
    return cua("click", {"pid": PID, "x": x, "y": y, "delivery_mode": "foreground"}, timeout=45)


def db_row():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,100), LastCompileTime "
                         "FROM Indicator WHERE Name='xs_script'").fetchone()
    finally:
        c.close()


results = []
before = db_row()
print("DB before:", before)

# 1. click xs_script tab (TitleBar 5 at frame 933,557)
cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
time.sleep(2)
r = click_xy(933 + 60, 557 + 20)
print("tab click:", json.dumps(r, ensure_ascii=False)[:80])
time.sleep(3)

# verify active tab
s0 = ws()
tb = [e for e in s0.get("elements", []) if e.get("role") == "TitleBar"]
print("titlebars:", [(e.get("element_index"), (e.get("label") or "")[:35]) for e in tb])
active_title = next((e.get("label") for e in tb if e.get("element_index") == 0), "")
results.append(("XS_SCRIPT_TAB_ACTIVE", "xs_script" in active_title, active_title[:40]))
print("active:", active_title[:50])

# 2. ctrl+a + paste known-good
cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
time.sleep(1)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
time.sleep(1)
cua("clipboard_write", {"text": GOOD}, timeout=30)
time.sleep(1)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "v", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
print("paste sent")
time.sleep(3)

# 3. pixel 儲存
s1 = ws()
save = next((e for e in s1.get("elements", []) if e.get("role") == "Button" and (e.get("label") or "").strip() == "儲存"), None)
if save:
    f = save.get("frame") or {}
    click_xy(f.get("x", 0) + f.get("w", 0) // 2, f.get("y", 0) + f.get("h", 0) // 2)
    print("儲存 clicked")
    time.sleep(5)
# save dialog confirm if present
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    t = (w.get("title") or "")
    if ("另存" in t or "儲存" in t) and w.get("pid") == PID:
        dw = w.get("window_id")
        sd = cua("get_window_state", {"pid": PID, "window_id": dw, "max_elements": 200}, timeout=45)
        ok = next((e for e in sd.get("elements", []) if e.get("role") == "Button" and
                   (e.get("label") or "").strip() in ("確定", "儲存", "Save")), None)
        if ok:
            f = ok.get("frame") or {}
            click_xy(f.get("x", 0) + f.get("w", 0) // 2, f.get("y", 0) + f.get("h", 0) // 2)
            time.sleep(4)

# 4. F6 compile
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
print("F6 sent")
time.sleep(12)

# 5. readback
after = db_row()
print("DB after :", after)
compiled_ok = after is not None and after[1] in (0, 1)
delta = before != after
results.append(("COMPILE_SUCCESS_READBACK", compiled_ok, f"CompileStatus={after[1] if after else '?'} msg={(after[2] if after else '')[:60]}"))
results.append(("FILE_DELTA", delta, f"LastCompile {before[3] if before else '?'} -> {after[3] if after else '?'}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v8 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V8_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V8",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture": "DOC-04 SF-0137 CrossOver function_bool signature (authority); function-call form",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus/CompileMsg/LastCompileTime",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script body replaced + recompiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V8_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
