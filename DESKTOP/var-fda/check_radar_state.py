# -*- coding: utf-8 -*-
"""Check radar state: selected strategy content (win32 read)."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
RADAR = 0x32112a
out = []

@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip():
        out.append((hex(ch), cls.value[:18], cid, t.value[:40]))
    return True
u.EnumChildWindows(RADAR, cb, 0)
print(f"controls: {len(out)}")
for h, c, cid, t in out:
    if any(k in t for k in ("FDA", "台積電", "2330", "警示", "複製", "1分鐘", "腳本", "名稱", "新增", "請複製", "執行中", "策略")):
        print(f"  {h} {c} cid={cid} '{t}'")
