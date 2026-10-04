# -*- coding: utf-8 -*-
"""FINAL P3d: probe 選擇使用腳本 dialog tree via uia (small scope) — find script nodes."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

# close 新增策略雷達 (keep 選擇使用腳本 open for probing)
d32 = Desktop(backend="win32")
try:
    d32.window(handle=0xe0f56).close()
    print("closed 新增策略雷達")
except Exception as e:
    print("close err:", str(e)[:60])
time.sleep(1)

du = Desktop(backend="uia")
dlg = du.window(handle=0x11354)
print("dlg exists:", dlg.exists(timeout=2))
if not dlg.exists(timeout=1):
    print("  (dialog gone)")
    raise SystemExit(0)

# list all tree items (uia, scoped to dialog)
trees = dlg.descendants(control_type="Tree")
print("trees:", len(trees))
for tv in trees[:2]:
    print("--- tree:", tv.window_text()[:20])
    try:
        for item in tv.descendants(control_type="TreeItem"):
            try:
                txt = item.window_text()[:40]
                print("   TI:", repr(txt))
            except Exception:
                pass
    except Exception as e:
        print("   tree err:", str(e)[:60])
