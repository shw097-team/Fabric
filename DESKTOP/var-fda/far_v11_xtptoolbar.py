# -*- coding: utf-8 -*-
"""FAR v11: win32 backend — enumerate XTPToolBar buttons (command ids)."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
editor = d32.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# XTPToolBar children
for tb in editor.children(class_name="XTPToolBar"):
    print(f"XTPToolBar {hex(tb.handle)} rect={tb.rectangle()}")
    try:
        for i in range(tb.button_count()):
            b = tb.button(i)
            try:
                info = b.info
                print(f"  [{i}] id={info.idCommand} state={info.fsState} text={info.text[:12]!r}")
            except Exception as e:
                print(f"  [{i}] err {str(e)[:40]}")
    except Exception as e:
        print("  button_count err:", str(e)[:60])
    print()
