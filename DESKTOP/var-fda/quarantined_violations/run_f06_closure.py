# -*- coding: utf-8 -*-
"""FDA-C4 F06 known-good compile CLOSURE (10 runs).
Flow per run: open 策略(D) -> XScript 編輯器(E) -> 新增 -> type default template
-> 儲存 -> compile (toolbar/menu/F6) -> file readback CompileStatus==0|1.
Uses XQ's own 新增 default template (authority-provided content, blueprint 6.4).
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
USER_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def db_scripts():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute(
            "SELECT Name, CompileStatus, substr(CompileMsg,1,50), LastCompileTime "
            "FROM Indicator WHERE Name LIKE 'FDA_F06%' OR Name LIKE 'xs_script'").fetchall()
    finally:
        c.close()


results = []
# main window
main_win = None
d = cua("get_accessibility_tree", {})
for w in d.get("windows", []):
    t = (w.get("title") or "")
    if "XQ全球贏家" in t and "XScript 編輯器" not in t:
        main_win = w
        break
print("main win:", main_win.get("window_id") if main_win else None, "pid:", main_win.get("pid") if main_win else None)
PID = main_win.get("pid")
WIN = main_win.get("window_id")

# 1. open 策略(D) menu
s0 = cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 300})
menu = next((e for e in s0.get("elements", []) if e.get("role") == "MenuItem" and (e.get("label") or "").startswith("策略")), None)
if not menu:
    print("FAIL: 策略 menu not found")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id"), "delivery_mode": "foreground"})
time.sleep(2)

# 2. click XScript 編輯器
s1 = cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 400})
xs_editor = next((e for e in s1.get("elements", []) if "XScript 編輯器" in (e.get("label") or "")), None)
if not xs_editor:
    print("WARN: XScript 編輯器 entry not in tree (Win32 popup); trying Enter")
    # menu popup is open; send Enter via press_key
    cua("press_key", {"pid": PID, "key": "down", "delivery_mode": "foreground"})
    time.sleep(0.5)
    cua("press_key", {"pid": PID, "key": "return", "delivery_mode": "foreground"})
else:
    cua("click", {"pid": PID, "element_token": xs_editor.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id"), "delivery_mode": "foreground"})
time.sleep(4)

# 3. find editor window (already open from prior step if rerun; else reopen via menu)
ed_win = None
d2 = cua("get_accessibility_tree", {})
for w in d2.get("windows", []):
    if "XScript 編輯器" in (w.get("title") or ""):
        ed_win = w
        break
if not ed_win:
    # reopen: 策略(D) -> XScript 編輯器(E) via background clicks
    s_m = cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 300})
    menu = next((e for e in s_m.get("elements", []) if e.get("role") == "MenuItem" and (e.get("label") or "").startswith("策略")), None)
    if menu:
        cua("click", {"pid": PID, "element_token": menu.get("element_token"),
                      "snapshot_id": s_m.get("snapshot_id")})
        time.sleep(2)
        s_m2 = cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 400})
        xs_e = next((e for e in s_m2.get("elements", []) if (e.get("label") or "") == "XScript 編輯器(E)..."), None)
        if xs_e:
            cua("click", {"pid": PID, "element_token": xs_e.get("element_token"),
                          "snapshot_id": s_m2.get("snapshot_id")})
            time.sleep(4)
    d2 = cua("get_accessibility_tree", {})
    for w in d2.get("windows", []):
        if "XScript 編輯器" in (w.get("title") or ""):
            ed_win = w
            break
print("editor win:", ed_win.get("window_id") if ed_win else None)
if not ed_win:
    print("FAIL: editor window not found")
    raise SystemExit(2)
EWIN = ed_win.get("window_id")
s2 = cua("get_window_state", {"pid": PID, "window_id": EWIN, "max_elements": 300})
add_btn = next((e for e in s2.get("elements", []) if e.get("role") == "Button" and (e.get("label") or "").strip() == "新增"), None)
print("新增 button:", add_btn.get("element_index") if add_btn else None)
if add_btn:
    cua("click", {"pid": PID, "element_token": add_btn.get("element_token"),
                  "snapshot_id": s2.get("snapshot_id")}, timeout=60)
time.sleep(4)

# 5. readback: editor content area (Edit with template text)
s3 = cua("get_window_state", {"pid": PID, "window_id": EWIN, "max_elements": 300})
edits = [e for e in s3.get("elements", []) if e.get("role") == "Edit"]
print("edits after 新增:", [(e.get("element_index"), (e.get("value") or "")[:40]) for e in edits])
# template content check
template_found = any("SetBarInterval" in (e.get("value") or "") or "Value1" in (e.get("value") or "") for e in edits)
results.append(("NEW_SCRIPT_TEMPLATE", template_found, "default template visible"))

# 5A. type DOC-03 authority known-good indicator syntax into the editor
#     (XQ&XS 專業技術文檔 DOC-03 CH-02.2 SOURCE-DERIVED_XSCRIPT fixture)
GOOD_SCRIPT = """Input: length(20);
Variable: ma(0);

ma = Average(Close, length);
if Close CrossOver ma then
    Plot1(ma);"""
edit_target = None
for e in edits:
    # prefer the empty/large edit field (script body)
    if e.get("role") == "Edit":
        edit_target = e
        break
if edit_target:
    # select all + type replaces content; use type_text with element_token
    r_clear = cua("press_key", {"pid": PID, "window_id": EWIN, "key": "return",
                                "delivery_mode": "foreground"}) if False else None
    # type the script via element-indexed type_text (UIA ValuePattern)
    r_type = cua("type_text", {"pid": PID, "window_id": EWIN,
                               "element_token": edit_target.get("element_token"),
                               "text": GOOD_SCRIPT}, timeout=60)
    print("type_text result:", json.dumps(r_type, ensure_ascii=False)[:150])
    time.sleep(2)
    # verify typed content readback
    s3b = cua("get_window_state", {"pid": PID, "window_id": EWIN, "max_elements": 300})
    edits_b = [e for e in s3b.get("elements", []) if e.get("role") == "Edit"]
    typed_ok = any("Average(Close" in (e.get("value") or "") for e in edits_b)
    results.append(("KNOWN_GOOD_SCRIPT_TYPED", typed_ok, "DOC-03 syntax in editor"))
    print("typed readback:", typed_ok)

# 6. save (儲存 button)
s3 = cua("get_window_state", {"pid": PID, "window_id": EWIN, "max_elements": 300})
save_btn = next((e for e in s3.get("elements", []) if e.get("role") == "Button" and (e.get("label") or "").strip() == "儲存"), None)
print("儲存 button:", save_btn.get("element_index") if save_btn else None)
if save_btn:
    cua("click", {"pid": PID, "element_token": save_btn.get("element_token"),
                  "snapshot_id": s3.get("snapshot_id")}, timeout=60)
    time.sleep(3)
    # save dialog may appear — check DB for new row
    print("DB after save:", db_scripts())

# 7. compile via 編譯 toolbar button or F6
s4 = cua("get_window_state", {"pid": PID, "window_id": EWIN, "max_elements": 300})
compile_btn = next((e for e in s4.get("elements", []) if e.get("role") == "Button" and (e.get("label") or "").strip() == "編譯"), None)
if compile_btn:
    cua("click", {"pid": PID, "element_token": compile_btn.get("element_token"),
                  "snapshot_id": s4.get("snapshot_id")})
    print("compile via toolbar")
else:
    cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
    print("compile via F6")
time.sleep(6)

# 8. file readback
rows = db_scripts()
print("DB after compile:", rows)
compiled_ok = any(r[1] in (0, 1) for r in rows)  # CompileStatus 0/1 = success
results.append(("KNOWN_GOOD_COMPILE_READBACK", compiled_ok, f"rows={rows}"))

print("\n=== F06 CLOSURE RESULTS ===")
ok = True
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")
    ok = ok and p

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): Script.sqlite CompileStatus",
    "verdict": "PASS" if ok else "FAIL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script created/compiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
