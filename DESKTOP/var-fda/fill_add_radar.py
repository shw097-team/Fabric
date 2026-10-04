# -*- coding: utf-8 -*-
"""Fill 新增策略雷達 dialog: name + click 加入(A) via PostMessage.
Name edit 0x30f98, 加入 btn 0x30f92.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
WM_SETTEXT = 0x000C
BM_CLICK = 0x00F5

EDIT_NAME = 0x30f98
BTN_ADD = 0x30f92
DLG = 0x30f88

# 1. set name
name = "FDA_PAPER_ALERT"
buf = ctypes.create_unicode_buffer(name)
r = user32.PostMessageW(EDIT_NAME, WM_SETTEXT, 0, ctypes.cast(buf, ctypes.c_void_p))
print("set name:", r)
time.sleep(1)

# read back
t = ctypes.create_unicode_buffer(128)
user32.GetWindowTextW(EDIT_NAME, t, 128)
print("name now:", repr(t.value[:40]))

# 2. click 加入(A)
r2 = user32.PostMessageW(BTN_ADD, BM_CLICK, 0, 0)
print("click 加入:", r2)
time.sleep(5)

# 3. check windows + strategy DB
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t2 = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t2, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 20252 and t2.value.strip() and "XQ全球" not in t2.value:
        out.append((hex(hwnd), t2.value[:60]))
    return True
user32.EnumWindows(cb, 0)
for h, t2 in out:
    print("WIN:", h, "|", t2)

import sqlite3
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite")
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptType FROM XSTradeStrategyDTO WHERE Name LIKE '%FDA%' OR Name LIKE '%PAPER%'").fetchall()
print("DB strategies:", rows)
c.close()
