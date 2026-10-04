# -*- coding: utf-8 -*-
"""Focus name edit + type via SendInput (real keyboard). Close dup dialogs first."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
WM_CLOSE = 0x0010
BM_CLICK = 0x00F5

# close the older dialog 0x30f88 (keep the newest 0x5110e)
user32.PostMessageW(0x30f88, WM_CLOSE, 0, 0)
time.sleep(1)

# enumerate new dialog 0x5110e children to get fresh handles
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

DLG = 0x5110e
for c in enum_children(DLG):
    if c["class"] == "Edit" or "加入" in c["text"] or "取消" in c["text"]:
        print(f"hwnd={hex(c['hwnd'])} class={c['class']!r} text={c['text']!r}")

# find first Edit (名稱)
edits = [c for c in enum_children(DLG) if c["class"] == "Edit"]
print("edits:", [hex(c["hwnd"]) for c in edits])

# focus via SetFocus (same thread issue) — instead click into it with SendInput mouse
# Simpler: use SetForegroundWindow + click coordinates via SendInput
# Get dialog rect
r = wt.RECT()
user32.GetWindowRect(DLG, ctypes.byref(r))
print("dlg rect:", r.left, r.top, r.right, r.bottom)

# name edit position — need GetWindowRect of edit
er = wt.RECT()
if edits:
    user32.GetWindowRect(edits[0]["hwnd"], ctypes.byref(er))
    cx = (er.left + er.right) // 2
    cy = (er.top + er.bottom) // 2
    print("name edit center:", cx, cy)
