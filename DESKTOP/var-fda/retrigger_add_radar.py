# -*- coding: utf-8 -*-
"""Re-trigger 加入雷達: find button hwnd under editor, PostMessage BM_CLICK.
Then enumerate new dialog, fill name via SendInput, click 加入.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
BM_CLICK = 0x00F5
WM_CLOSE = 0x0010

EDITOR = 0x2210b8e


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


# find 加入雷達 button
btn = None
for c in enum_children(EDITOR):
    if "加入雷達" in c["text"]:
        btn = c
        break
print("加入雷達 btn:", hex(btn["hwnd"]) if btn else None)
if btn:
    user32.PostMessageW(btn["hwnd"], BM_CLICK, 0, 0)
    print("clicked")
    time.sleep(4)

# find 新增策略雷達 dialog
dlg = None
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 20252 and "新增策略雷達" in t.value:
        out.append(hwnd)
    return True
user32.EnumWindows(cb2, 0)
print("新增策略雷達 dialogs:", [hex(h) for h in out])
if out:
    dlg = out[0]
    kids = enum_children(dlg)
    edits = [c for c in kids if c["class"] == "Edit"]
    add_btn = next((c for c in kids if "加入" in c["text"]), None)
    print("edits:", [hex(c["hwnd"]) for c in edits])
    print("加入 btn:", hex(add_btn["hwnd"]) if add_btn else None)
    # show all kids briefly
    for c in kids[:20]:
        print(f"  {hex(c['hwnd'])} {c['class']!r} {c['text']!r}")
