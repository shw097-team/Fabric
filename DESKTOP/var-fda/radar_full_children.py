# -*- coding: utf-8 -*-
"""Enumerate radar window FULL children — find tabs, grid, tree (win32, read-only)."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
RADAR = 0x80fc8
out = []

@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    cid = u.GetDlgCtrlID(ch)
    out.append((ch, cls.value, t.value, cid))
    return True

u.EnumChildWindows(RADAR, cb, 0)
print(f"children: {len(out)}")
# group by class
from collections import Counter
cls_counts = Counter(c for _, c, _, _ in out)
print("classes:", dict(cls_counts))
# print tab-like and grid/tree-like controls
for h, c, t, cid in out:
    if any(k in c for k in ("Tab", "Tree", "Grid", "SysTab", "MFC")) or "tab" in c.lower():
        print(f"  {hex(h)} | {c[:35]} | cid={cid} | '{t[:30]}'")
# print all with text (control labels)
print("\n=== controls with text ===")
for h, c, t, cid in out:
    if t.strip():
        print(f"  {hex(h)} | {c[:30]} | cid={cid} | '{t[:35]}'")
