# -*- coding: utf-8 -*-
"""Open editor via pywinauto uia menu (community pattern), then FN03 locate 新增."""
import json
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

du = Desktop(backend="uia")
main = du.window(class_name="DAQXQLITEMainWnd")
print("main exists:", main.exists(timeout=3))
if not main.exists(timeout=2):
    raise SystemExit(2)

# 策略(D) menu item (uia)
try:
    items = main.descendants(control_type="MenuItem")
    print("menu items:", len(items))
    for it in items[:25]:
        t = it.window_text()
        if t.strip():
            print("  ", repr(t[:30]))
except Exception as e:
    print("menu enum err:", str(e)[:80])
