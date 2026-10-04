# -*- coding: utf-8 -*-
"""FAR v15: check XQ main window class name + retry conditions."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if "XQ全球" in t:
                print("MAIN win32:", hex(w.handle), "class:", w.class_name(), "|", t[:50])
    except Exception:
        pass

du = Desktop(backend="uia")
try:
    main = du.window(class_name="DAQXQLITEMainWnd")
    print("uia DAQXQLITEMainWnd exists:", main.exists(timeout=3))
except Exception as e:
    print("uia err:", str(e)[:100])

# also try title match
try:
    m2 = du.window(title_re="XQ全球贏家.*")
    print("uia title exists:", m2.exists(timeout=3), "class:", m2.class_name() if m2.exists(timeout=0.5) else "?")
except Exception as e:
    print("uia title err:", str(e)[:100])
