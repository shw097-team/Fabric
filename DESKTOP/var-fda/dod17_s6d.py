# -*- coding: utf-8 -*-
"""DoD-17 S6d: pywinauto uia read radar window WITH 自訂 — use cua click then re-read.
Key fix: radar hwnd via win32 title match, then uia descendants read-only."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")

# radar hwnd (win32)
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
print("radar hwnd:", hex(radar_hwnd) if radar_hwnd else None)

# uia full descendants of radar — dump ALL labels (limit to avoid deadlock)
ru = du.window(handle=radar_hwnd)
try:
    els = ru.descendants()
    print("total descendants:", len(els))
    # find 自訂 TreeItem
    customs = [e for e in els if (e.window_text() or "").strip() == "自訂" or "自訂" in (e.window_text() or "")]
    print("自訂 items:", len(customs))
    for c in customs[:3]:
        print("  ", repr(c.window_text()[:30]), c.element_info.control_type)
except Exception as e:
    print("desc err:", str(e)[:80])
