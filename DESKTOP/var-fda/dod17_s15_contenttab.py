# -*- coding: utf-8 -*-
"""DoD-17 S15: uia select 內容 TabItem (pattern) -> verify content tab shows strategy list."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x80fc8
ru = du.window(handle=RADAR)

# 1. read tabs via uia
try:
    tabs = ru.descendants(control_type="TabItem")
    print("tabs:", [t.window_text().strip() for t in tabs if t.window_text().strip()])
    content = next((t for t in tabs if t.window_text().strip() == "內容"), None)
    if content:
        content.select()
        print("selected 內容 tab (pattern)")
        time.sleep(3)
except Exception as e:
    print("tab err:", str(e)[:80])

# 2. read radar content texts again — should show strategy list / selected strategy info
u = ctypes.windll.user32
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip():
        out.append((hex(ch), cls.value[:18], cid, t.value[:38]))
    return True
u.EnumChildWindows(RADAR, cb, 0)
print("\nafter 內容 tab:")
for h, c, cid, t in out:
    if any(k in t for k in ("FDA", "台積電", "2330", "警示", "複製", "1分鐘", "腳本", "名稱", "新增")):
        print(f"  {h} {c} cid={cid} '{t}'")
