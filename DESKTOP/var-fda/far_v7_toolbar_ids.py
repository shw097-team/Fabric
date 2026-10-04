# -*- coding: utf-8 -*-
"""FAR v7: win32 backend — enumerate editor toolbar buttons + command ids."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
editor = d32.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# find ToolbarWindow32 children
for tb in editor.children(class_name="ToolbarWindow32"):
    print(f"toolbar {hex(tb.handle)} buttons: {tb.button_count()}")
    for i in range(tb.button_count()):
        try:
            b = tb.button(i)
            info = b.info
            print(f"  [{i}] id={info.idCommand} state={info.fsState} text={info.text[:15]!r}")
        except Exception as e:
            print(f"  [{i}] err {str(e)[:40]}")
    break
