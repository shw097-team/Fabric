# -*- coding: utf-8 -*-
"""test_xq_native_adapter.py — xq_native_adapter contract tests (WO-FDA-XQ-002).

Static contract + live FN01 (main window locate) verification.
All operations read-only / message-only — never moves the user's cursor.
"""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
import xq_native_adapter as na

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" | {detail}" if detail and not cond else ""))


# --- static contract ---
src = open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\xq_native_adapter.py", encoding="utf-8").read()
for fn in ("find_main_window", "find_window_by_title", "enum_children", "find_child",
           "invoke_button", "set_edit_text", "get_edit_text", "press_toolbar",
           "toolbar_button_count", "is_button_enabled", "close_window"):
    check(f"adapter_has_{fn}", f"def {fn}(" in src)

# no mouse-input API calls anywhere
check("no_click_input_call", "click_input(" not in src)
check("no_setcursorpos_call", "SetCursorPos(" not in src)
check("no_sendinput_call", "SendInput(" not in src)
check("no_setforeground_call", "SetForegroundWindow(" not in src)

# --- live: main window locate (FN01 contract) ---
ok = 0
runs = 10
for _ in range(runs):
    if na.find_main_window():
        ok += 1
    time.sleep(0.03)
check("FN01_live_10x", ok == runs, f"{ok}/{runs}")

# live: main window class is DAQXQLITEMainWnd
import ctypes
import ctypes.wintypes as wt
hwnd = na.find_main_window()
if hwnd:
    cls = ctypes.create_unicode_buffer(64)
    ctypes.windll.user32.GetClassNameW(hwnd, cls, 64)
    check("main_class_DAQXQLITEMainWnd", cls.value == "DAQXQLITEMainWnd", cls.value)

print(f"\nRESULT: {len(PASS)} PASS / {len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
