# -*- coding: utf-8 -*-
"""FINAL P3g: check all windows now."""
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if t.strip() and ("策略" in t or "腳本" in t or "選擇" in t or "新增" in t or "XQ全球" in t):
                print(hex(w.handle), w.class_name()[:25], "|", t[:55])
    except Exception:
        pass
