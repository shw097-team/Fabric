# -*- coding: utf-8 -*-
"""FAR v17: minimal repro of open_radar's exact window lookup."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

t0 = time.monotonic()
try:
    d = Desktop(backend="uia")
    w = d.window(class_name="DAQXQLITEMainWnd")
    print("window object created in", round(time.monotonic() - t0, 2), "s")
    print("exists:", w.exists(timeout=2))
except Exception as e:
    print("EXC:", type(e).__name__, str(e)[:120], "in", round(time.monotonic() - t0, 2), "s")
