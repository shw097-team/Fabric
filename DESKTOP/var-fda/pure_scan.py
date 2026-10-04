# -*- coding: utf-8 -*-
"""PURE-MESSAGE: scan for any XQ dialog (ALL classes) + verify strategy in DB.
Zero mouse, zero focus change. Read-only."""
import ctypes
import ctypes.wintypes as wt
import sqlite3

u = ctypes.windll.user32
PID = 23456

# 1. ALL XQ top-level windows (any class)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value != PID:
        return True
    t = ctypes.create_unicode_buffer(256)
    u.GetWindowTextW(hwnd, t, 256)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(hwnd, cls, 64)
    if u.IsWindowVisible(hwnd):
        out.append((hwnd, cls.value, t.value))
    return True
u.EnumWindows(cb, 0)
print("=== XQ windows (all classes) ===")
for h, c, t in out:
    print(f"  {hex(h)} | {c[:35]} | '{t[:55]}'")
    # child buttons (dialog action buttons)
    btns = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb2(ch, lp):
        tc = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(ch, tc, 128)
        cc = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(ch, cc, 64)
        if "Button" in cc.value and tc.value.strip():
            btns.append(tc.value[:20])
        return True
    u.EnumChildWindows(h, cb2, 0)
    if btns:
        print("     buttons:", btns[:6])

# 2. strategy in DB?
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
print("\n=== SensorList ===")
for n, s, y, ct in rows:
    print(f"  {dec(n)[:35]} | {dec(s)[:25]} | {dec(y)[:15]} | {dec(ct)}")
c.close()
