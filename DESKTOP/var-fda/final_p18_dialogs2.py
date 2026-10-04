# -*- coding: utf-8 -*-
"""FINAL P18: enumerate BOTH 新增策略雷達 dialogs fully (texts) — find error/notice."""
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible():
            t = w.window_text()
            if "新增策略雷達" in t or "策略" in t:
                print(f"=== {hex(w.handle)} '{t[:40]}' ===")
                for c in w.descendants():
                    try:
                        txt = c.window_text().strip()
                        cls = c.class_name()[:20]
                        if txt:
                            print(f"  {cls} '{txt[:60]}'")
                    except Exception:
                        pass
    except Exception:
        pass
