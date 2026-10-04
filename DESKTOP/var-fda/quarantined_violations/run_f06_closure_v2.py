# -*- coding: utf-8 -*-
"""FDA-C4 F06 known-good compile CLOSURE v2 (slow-paced, UIA-deadlock-safe).
Per DOC-01 XS editor is ADOPTED_AS_PRIMARY_COMPILER_UI; per DOC-03 CH-02.2 the
known-good indicator syntax fixture is:
  Input: length(20); Variable: ma(0); ma = Average(Close, length);
  if Close CrossOver ma then Plot1(ma);
Flow: open editor -> 新增 -> select-all -> type known-good -> 儲存 -> 編譯 -> file readback.
Every step: fresh snapshot + long sleep; never fire two actions back-to-back.
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


def find_main():
    for w in tree().get("windows", []):
        t = (w.get("title") or "")
        if "XQ全球贏家" in t and "XScript" not in t:
            return w
    return None


def ws(pid, wid, mx=300):
    return cua("get_window_state", {"pid": pid, "window_id": wid, "max_elements": mx})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def db_state():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute(
            "SELECT Name, CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
            "FROM Indicator WHERE Name LIKE 'FDA_F06%' OR Name LIKE 'FDA%'").fetchall()
    finally:
        c.close()


results = []
main = find_main()
PID = main.get("pid")
WIN = main.get("window_id")
print("main:", PID, WIN)

# ============ STEP 1: open 策略(D) menu (background click — proven to reveal items) ====
s0 = ws(PID, WIN)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, WIN, 400)
xs_e = find(s1.get("elements", []), "XScript 編輯器(E)...", "MenuItem")
results.append(("OPEN_EDITOR_MENU", xs_e is not None, "XScript 編輯器(E) visible"))
print("xs entry:", xs_e.get("element_index") if xs_e else None)
if not xs_e:
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": xs_e.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

# editor window
ed = None
for w in tree().get("windows", []):
    if "XScript 編輯器" in (w.get("title") or ""):
        ed = w
        break
print("editor:", ed.get("window_id") if ed else None)
if not ed:
    raise SystemExit(2)
EWIN = ed.get("window_id")

# ============ STEP 2: 新增 ============
s2 = ws(PID, EWIN)
add_btn = find(s2.get("elements", []), "新增", "Button")
results.append(("NEW_BUTTON", add_btn is not None, "新增 button"))
print("新增:", add_btn.get("element_index") if add_btn else None)
if not add_btn:
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": add_btn.get("element_token"),
              "snapshot_id": s2.get("snapshot_id")}, timeout=60)
time.sleep(6)

# ============ STEP 3: locate script body edit field + type known-good ============
s3 = ws(PID, EWIN)
edits = [e for e in s3.get("elements", []) if e.get("role") == "Edit"]
print("edits:", [(e.get("element_index"), (e.get("value") or "")[:25]) for e in edits])
body = None
for e in edits:
    v = e.get("value") or ""
    if "SetBarInterval" in v or "Value1" in v or "Input" in v or len(v) > 2:
        body = e
        break
if body is None and edits:
    body = edits[-1]  # fallback: last edit field
results.append(("SCRIPT_BODY_FOUND", body is not None, "edit field"))
if body:
    r = cua("type_text", {"pid": PID, "window_id": EWIN,
                          "element_token": body.get("element_token"),
                          "text": GOOD_SCRIPT}, timeout=60)
    print("type:", json.dumps(r, ensure_ascii=False)[:140])
    time.sleep(4)
    s3b = ws(PID, EWIN)
    typed_ok = any("Average(Close" in (e.get("value") or "") for e in s3b.get("elements", []) if e.get("role") == "Edit")
    results.append(("KNOWN_GOOD_TYPED", typed_ok, "DOC-03 syntax in body"))
    print("typed readback:", typed_ok)

# ============ STEP 4: 儲存 ============
s4 = ws(PID, EWIN)
save_btn = find(s4.get("elements", []), "儲存", "Button")
if save_btn:
    cua("click", {"pid": PID, "element_token": save_btn.get("element_token"),
                  "snapshot_id": s4.get("snapshot_id")}, timeout=60)
    time.sleep(5)
    print("DB after save:", db_state())
# save dialog may need name entry — check windows
d5 = tree()
dlg = [w for w in d5.get("windows", []) if w.get("pid") == PID and "XScript" not in (w.get("title") or "")]
for w in d5.get("windows", []):
    t = (w.get("title") or "")
    if "另存" in t or "儲存" in t or "新增" in t:
        print("SAVE DIALOG:", repr(t[:50]), "wid:", w.get("window_id"))
        dlg_wid = w.get("window_id")
        sd = ws(PID, dlg_wid, 200)
        name_edit = find(sd.get("elements", []), "", "Edit")
        # find any Edit and type name
        for e in sd.get("elements", []):
            if e.get("role") == "Edit":
                cua("type_text", {"pid": PID, "window_id": dlg_wid,
                                  "element_token": e.get("element_token"),
                                  "text": "FDA_F06_known_good"}, timeout=45)
                time.sleep(2)
                break
        ok_btn = find(sd.get("elements", []), "確定", "Button") or find(sd.get("elements", []), "儲存", "Button")
        if ok_btn:
            cua("click", {"pid": PID, "element_token": ok_btn.get("element_token"),
                          "snapshot_id": sd.get("snapshot_id")}, timeout=45)
            time.sleep(5)

# ============ STEP 5: 編譯 (F6) ============
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
print("F6 sent")
time.sleep(8)

# ============ STEP 6: file readback ============
rows = db_state()
print("DB final:", rows)
compiled_ok = any(r[1] in (0, 1) and r[0] == "FDA_F06_known_good" for r in rows)
results.append(("KNOWN_GOOD_COMPILE_READBACK", compiled_ok, f"rows={rows}"))

print("\n=== F06 CLOSURE v2 RESULTS ===")
ok = True
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")
    ok = ok and p

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V2_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V2",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture_source": "XQ&XS 專業技術文檔 DOC-03 CH-02.2 SOURCE-DERIVED_XSCRIPT (authority)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): Script.sqlite CompileStatus/CompileMsg",
    "verdict": "PASS" if ok else "FAIL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script created/compiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V2_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
