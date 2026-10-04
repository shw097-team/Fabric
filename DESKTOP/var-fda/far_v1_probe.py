# -*- coding: utf-8 -*-
"""FAR v1: pywinauto probe — close stale dialogs, verify XQ connectivity."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

# close stale 新增腳本 dialogs via win32 backend
d = Desktop(backend="win32")
closed = []
for w in d.windows(class_name="#32770"):
    try:
        t = w.window_text()
        if "新增腳本" in t:
            w.close()
            closed.append(t[:30])
            time.sleep(0.3)
    except Exception:
        pass
print("closed dialogs:", closed)

# verify XQ main window reachable via uia backend
du = Desktop(backend="uia")
try:
    main = du.window(class_name="DAQXQLITEMainWnd")
    print("main exists:", main.exists(timeout=2))
except Exception as e:
    print("main err:", str(e)[:100])

# verify editor window
try:
    ed = du.window(title_re=".*XScript 編輯器.*")
    print("editor exists:", ed.exists(timeout=2))
except Exception as e:
    print("editor err:", str(e)[:100])
