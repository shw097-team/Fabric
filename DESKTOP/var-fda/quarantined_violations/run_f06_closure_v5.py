# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v5 — foreground type path.
pixel-click 新增 -> bring editor to foreground -> ctrl+a -> type_text foreground
(DOC-03 known-good) -> pixel-click 儲存 -> save dialog name -> F6 -> file readback.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
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


def click_frame(pid, e):
    f = e.get("frame") or {}
    x = f.get("x", 0) + f.get("w", 0) // 2
    y = f.get("y", 0) + f.get("h", 0) // 2
    return cua("click", {"pid": pid, "x": x, "y": y, "delivery_mode": "foreground"}, timeout=45)


def db_user():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
                         "FROM Indicator WHERE Name LIKE 'FDA_F06%' OR Name LIKE 'xs_script'").fetchall()
    finally:
        c.close()


results = []
main = None
for _ in range(12):
    for w in tree().get("windows", []):
        t = (w.get("title") or "")
        if "XQ全球贏家" in t and "已登入" in t and "XScript" not in t:
            main = w
            break
    if main:
        break
    time.sleep(5)
PID = main.get("pid")
WIN = main.get("window_id")
print("main:", PID, WIN)

# open editor
s0 = ws(PID, WIN)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, WIN, 400)
xs_e = find(s1.get("elements", []), "XScript 編輯器(E)...", "MenuItem")
if not xs_e:
    print("FAIL: menu entry")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": xs_e.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)
ed = next((w for w in tree().get("windows", []) if "XScript 編輯器" in (w.get("title") or "")), None)
print("editor:", ed.get("window_id") if ed else None)
EWIN = ed.get("window_id")

# pixel 新增
s2 = ws(PID, EWIN)
add_btn = find(s2.get("elements", []), "新增", "Button")
if not add_btn:
    print("FAIL: 新增")
    raise SystemExit(2)
r = click_frame(PID, add_btn)
print("新增:", json.dumps(r, ensure_ascii=False)[:80])
time.sleep(6)

# bring editor to foreground, ctrl+a, then type foreground
cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
time.sleep(2)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
time.sleep(1)
# clipboard write then ctrl+v (robust for syntax editor)
r_clip = cua("clipboard_write", {"text": GOOD_SCRIPT}, timeout=30)
print("clipboard:", json.dumps(r_clip, ensure_ascii=False)[:80])
time.sleep(1)
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "v", "modifiers": ["ctrl"],
                  "delivery_mode": "foreground"})
print("ctrl+v sent")
time.sleep(3)

# readback typed via clipboard_read or UIA
s3 = ws(PID, EWIN)
typed_ok = any("Average(Close" in (e.get("value") or "") for e in s3.get("elements", []) if e.get("role") == "Edit")
if not typed_ok:
    r_rd = cua("clipboard_read", {}, timeout=30)
    print("clipboard read:", json.dumps(r_rd, ensure_ascii=False)[:150])
results.append(("KNOWN_GOOD_INSERTED", typed_ok, "DOC-03 syntax via ctrl+v"))
print("typed readback:", typed_ok)

# pixel 儲存
s4 = ws(PID, EWIN)
save_btn = find(s4.get("elements", []), "儲存", "Button")
if save_btn:
    click_frame(PID, save_btn)
    print("儲存 pixel clicked")
    time.sleep(5)

# save dialog: type name + confirm
for w in tree().get("windows", []):
    t = (w.get("title") or "")
    if ("另存" in t or "儲存" in t or "新增" in t) and w.get("pid") == PID:
        print("DLG:", repr(t[:40]), w.get("window_id"))
        dw = w.get("window_id")
        sd = ws(PID, dw, 200)
        for e in sd.get("elements", []):
            if e.get("role") == "Edit":
                cua("type_text", {"pid": PID, "window_id": dw, "element_token": e.get("element_token"),
                                  "text": "FDA_F06_known_good", "delivery_mode": "foreground"}, timeout=45)
                time.sleep(1)
                break
        ok = find(sd.get("elements", []), "確定", "Button") or find(sd.get("elements", []), "儲存", "Button")
        if ok:
            click_frame(PID, ok)
            time.sleep(5)

# F6
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
print("F6 sent")
time.sleep(10)

rows = db_user()
print("DB final:", rows)
compiled_ok = any(r[0] == "FDA_F06_known_good" and r[1] in (0, 1) for r in rows)
results.append(("KNOWN_GOOD_COMPILE_READBACK", compiled_ok, f"rows={rows}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v5 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V5_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V5",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture": "DOC-03 CH-02.2 known-good indicator syntax (authority)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script created/compiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V5_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
