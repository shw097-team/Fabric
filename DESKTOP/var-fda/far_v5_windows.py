# -*- coding: utf-8 -*-
"""FAR v5: check current windows; retry 新增 click if needed."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
# list all visible top windows
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if t.strip():
                print(f"  {hex(w.handle)} {t[:50]} {w.class_name()[:25]}")
    except Exception:
        pass
