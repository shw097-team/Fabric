# -*- coding: utf-8 -*-
"""bg v6: fresh enumerate 開啟 dialog 0x100f76, click 警示 tab (PostMessage),
then read list via LVM. If list empty, click the 自訂 tree node first.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 0x100f76


def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:50], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


kids = enum_children(DLG)
print("=== children ===")
for c in kids:
    print(f"{hex(c['hwnd'])} {c['class']!r} {c['text']!r}")

# click 警示 tab
alert = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
print("\n警示 tab:", hex(alert["hwnd"]) if alert else None)
if alert:
    user32.PostMessageW(alert["hwnd"], 0x00F5, 0, 0)
    print("posted")
    time.sleep(2)

# read lists
LVM_GETITEMCOUNT = 0x1004
LVM_GETITEMTEXT = 0x1073
LVIF_TEXT = 0x0001

class LVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("iItem", ctypes.c_int), ("iSubItem", ctypes.c_int),
                ("state", wt.UINT), ("stateMask", wt.UINT),
                ("pszText", ctypes.c_wchar_p), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("lParam", wt.LPARAM),
                ("iIndent", ctypes.c_int), ("iGroupId", ctypes.c_int),
                ("cColumns", wt.UINT), ("puColumns", wt.LPVOID),
                ("piColFmt", wt.LPVOID), ("iGroup", ctypes.c_int)]

def lv_items(hwnd, maxn=80):
    n = user32.SendMessageW(hwnd, LVM_GETITEMCOUNT, 0, 0)
    out = []
    for i in range(min(n, maxn)):
        buf = ctypes.create_unicode_buffer(128)
        item = LVITEM(LVIF_TEXT, i, 0, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 128, 0, 0, 0, 0, 0, None, None, 0)
        user32.SendMessageW(hwnd, LVM_GETITEMTEXT, i, ctypes.byref(item))
        if buf.value.strip():
            out.append((i, buf.value))
    return out

lvs = [c["hwnd"] for c in kids if "SysListView32" in c["class"]]
print("\nlists:", [hex(l) for l in lvs])
for lv in lvs:
    items = lv_items(lv)
    print(f"--- {hex(lv)} ({len(items)}) ---")
    for i, t in items[:30]:
        print("   ", i, t[:70])
