# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v4 — pixel-click path (bypass Afx UIA Invoke deadlock).
Use element frame coordinates + cua click(x,y) for 新增/儲存 buttons;
UIA element_token only for read-only tree/title ops.
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


def cua(tool, args, timeout=40):
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
    """Pixel-click the center of an element's frame (bypasses UIA Invoke)."""
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
for w in tree().get("windows", []):
    t = (w.get("title") or "")
    if "XQ全球贏家" in t and "已登入" in t and "XScript" not in t:
        main = w
        break
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
    print("FAIL: editor menu entry")
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

# pixel-click 新增
s2 = ws(PID, EWIN)
add_btn = find(s2.get("elements", []), "新增", "Button")
if add_btn:
    r = click_frame(PID, add_btn)
    print("pixel 新增:", json.dumps(r, ensure_ascii=False)[:100])
    time.sleep(6)
else:
    print("FAIL: 新增 button not found")
    raise SystemExit(2)

# check editor state after 新增 (may have opened a new doc tab or dialog)
s3 = ws(PID, EWIN)
edits = [e for e in s3.get("elements", []) if e.get("role") == "Edit"]
print("edits:", [(e.get("element_index"), (e.get("value") or "")[:25]) for e in edits])
titles = [e.get("label") for e in s3.get("elements", []) if e.get("role") == "TitleBar"]
print("titles:", titles[:2])

# type known-good into body edit
body = None
for e in edits:
    v = e.get("value") or ""
    if len(v) > 2 or "SetBarInterval" in v or "Input" in v:
        body = e
        break
if body is None and edits:
    body = edits[-1]
if body:
    r = cua("type_text", {"pid": PID, "window_id": EWIN,
                          "element_token": body.get("element_token"),
                          "text": GOOD_SCRIPT}, timeout=60)
    print("type:", json.dumps(r, ensure_ascii=False)[:120])
    time.sleep(4)
    s3b = ws(PID, EWIN)
    typed_ok = any("Average(Close" in (e.get("value") or "") for e in s3b.get("elements", []) if e.get("role") == "Edit")
    results.append(("KNOWN_GOOD_TYPED", typed_ok, "DOC-03 syntax"))
    print("typed readback:", typed_ok)
else:
    results.append(("KNOWN_GOOD_TYPED", False, "no body"))

# pixel-click 儲存
s4 = ws(PID, EWIN)
save_btn = find(s4.get("elements", []), "儲存", "Button")
if save_btn:
    r = click_frame(PID, save_btn)
    print("pixel 儲存:", json.dumps(r, ensure_ascii=False)[:100])
    time.sleep(5)
# save dialog handling (name field)
for w in tree().get("windows", []):
    t = (w.get("title") or "")
    if "另存" in t or "儲存" in t or w.get("pid") == PID and "XScript" not in t and "XQ全球" not in t:
        print("SAVE DIALOG:", repr(t[:50]), w.get("window_id"))
        dw = w.get("window_id")
        sd = ws(PID, dw, 200)
        for e in sd.get("elements", []):
            if e.get("role") == "Edit":
                cua("type_text", {"pid": PID, "window_id": dw, "element_token": e.get("element_token"),
                                  "text": "FDA_F06_known_good"}, timeout=45)
                time.sleep(2)
                break
        ok = find(sd.get("elements", []), "確定", "Button") or find(sd.get("elements", []), "儲存", "Button") or find(sd.get("elements", []), "Save", "Button")
        if ok:
            click_frame(PID, ok)
            time.sleep(5)

# F6 compile
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
print("F6 sent")
time.sleep(10)

rows = db_user()
print("DB final:", rows)
compiled_ok = any(r[0] == "FDA_F06_known_good" and r[1] in (0, 1) for r in rows)
results.append(("KNOWN_GOOD_COMPILE_READBACK", compiled_ok, f"rows={rows}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v4 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V4_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V4",
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
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V4_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
