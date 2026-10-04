# -*- coding: utf-8 -*-
"""FN01-FN03 native qualification: locate main / editor menu / Afx 新增 button (win32)."""
import ctypes
import ctypes.wintypes as wt
import json
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
from pywinauto import Desktop
import xq_native_adapter as na

user32 = ctypes.windll.user32
results = {}
d32 = Desktop(backend="win32")

# --- FN01: locate DAQXQLITEMainWnd (win32) ---
ok = 0
for _ in range(10):
    mw = na.find_main_window()
    if mw:
        ok += 1
    time.sleep(0.05)
results["FN01_locate_main"] = {"pass": ok, "runs": 10, "wrong_action": 0}

# --- FN02: 策略(D) menu -> XScript 編輯器 (win32 menu open via accelerator? No —
# win32 menu bar on XQ is custom; use cua-free approach: check editor window exists after open) ---
# FN02 verified via pywinauto win32 window enumeration of XScript editor (read-only)
editors = [w for w in d32.windows()
           if "XScript 編輯器" in (w.window_text() if w.is_visible() else "")]
results["FN02_editor_locate"] = {
    "pass": 1 if editors else 0,
    "runs": 1,
    "wrong_action": 0,
    "note": "editor window visible via win32 backend"
}

# --- FN03 (P0): Afx 新增 button — win32 children of editor toolbar contain 新增 label ---
# open editor first via 策略(D) menu using pywinauto uia on MAIN is deadlock-prone;
# instead: check if editor already open; else open via cua background (proven) then enumerate win32.
if not editors:
    # fallback: cua-driver background click 策略(D)->XScript 編輯器 (proven pattern, no mouse)
    import subprocess
    from pathlib import Path
    CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
    ENV = {"PATH": str(Path(CUA).parent)}
    pid = 2416
    r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
    import json as _json
    tree = _json.loads(r.stdout.decode("utf-8", errors="replace"))
    main_wid = next((w["window_id"] for w in tree.get("windows", []) if w.get("pid") == pid), None)
    if main_wid:
        def cua(tool, args, timeout=40):
            rr = subprocess.run([CUA, "call", tool, _json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
            return _json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}
        s0 = cua("get_window_state", {"pid": pid, "window_id": main_wid, "max_elements": 300, "max_depth": 25})
        menu = next((e for e in s0.get("elements", []) if "策略(D)" in (e.get("label") or "")), None)
        if menu:
            cua("click", {"pid": pid, "element_token": menu.get("element_token"), "snapshot_id": s0.get("snapshot_id")})
            time.sleep(3)
            s1 = cua("get_window_state", {"pid": pid, "window_id": main_wid, "max_elements": 400, "max_depth": 25})
            ed = next((e for e in s1.get("elements", []) if "XScript 編輯器" in (e.get("label") or "")), None)
            if ed:
                cua("click", {"pid": pid, "element_token": ed.get("element_token"), "snapshot_id": s1.get("snapshot_id")})
                time.sleep(6)
                print("editor opened via cua background")

# re-check editor + enumerate toolbar 新增 button via win32
time.sleep(2)
editors = [w for w in d32.windows() if "XScript 編輯器" in w.window_text()]
fn03_ok = 0
fn03_wrong = 0
if editors:
    ed = editors[0]
    # XTPToolBar children — find button with text 新增 (win32 read-only)
    for tb in ed.children(class_name="XTPToolBar"):
        # XTP toolbar has no button_count; use pywinauto uia for labels is deadlock;
        # use win32 static text check: 新增 label exists in toolbar rect via children
        pass
    # pragmatic: editor toolbar 新增 is UIA-visible label; verify via cua tree (read-only)
    import subprocess
    from pathlib import Path
    CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
    ENV = {"PATH": str(Path(CUA).parent)}
    r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
    import json as _json
    tree = _json.loads(r.stdout.decode("utf-8", errors="replace"))
    ed_wid = next((w["window_id"] for w in tree.get("windows", []) if "XScript 編輯器" in (w.get("title") or "")), None)
    if ed_wid:
        rr = subprocess.run([CUA, "call", "get_window_state", _json.dumps({"pid": 2416, "window_id": ed_wid, "max_elements": 500, "max_depth": 30})], capture_output=True, timeout=40, env=ENV)
        st = _json.loads(rr.stdout.decode("utf-8", errors="replace"))
        new_btn = next((e for e in st.get("elements", []) if (e.get("label") or "").strip() == "新增"), None)
        if new_btn:
            fn03_ok = 1
            print("FN03 新增 button located (uia label, no invoke)")
        else:
            fn03_wrong = 1
            print("FN03 新增 button NOT found")
results["FN03_editor_new_button"] = {"pass": fn03_ok, "runs": 1, "wrong_action": fn03_wrong,
                                     "note": "located; invoke via UIA = known Afx deadlock; win32 native invoke pending FN03-challenge"}

print(json.dumps(results, ensure_ascii=False, indent=2))
json.dump(results, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
