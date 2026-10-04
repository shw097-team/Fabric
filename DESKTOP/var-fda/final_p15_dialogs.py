# -*- coding: utf-8 -*-
"""FINAL P15: enumerate all visible dialogs after 加入."""
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            cls = w.class_name()
            if t.strip() and cls == "#32770":
                print(hex(w.handle), "|", t[:60])
    except Exception:
        pass
