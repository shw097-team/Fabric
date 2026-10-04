# -*- coding: utf-8 -*-
"""FINAL P2d: enumerate 說明 dialog children (win32) — find clickable control."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
d32 = Desktop(backend="win32")
dlg = d32.window(handle=0x100d96)

# win32 descendants with control ids + classes
for c in dlg.descendants():
    try:
        ci = c.element_info.control_id() if hasattr(c.element_info, "control_id") else "?"
        cls = c.class_name()
        txt = c.window_text()[:25]
        rect = c.rectangle()
        print(f"  id={ci} {cls[:22]} '{txt}' rect=({rect.left},{rect.top},{rect.width()}x{rect.height()})")
    except Exception as e:
        pass
