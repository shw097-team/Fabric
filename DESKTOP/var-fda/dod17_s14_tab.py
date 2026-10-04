# -*- coding: utf-8 -*-
"""DoD-17 S14: read SysTabControl32 (17003) — get tab count + names, switch to 內容 tab (TCM msg)."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
RADAR = 0x80fc8
TAB = 0x70ace  # SysTabControl32 cid=17003

# TCM messages
TCM_GETITEMCOUNT = 0x1304
TCM_GETITEM = 0x1305 + 1  # TCM_GETITEMW = 0x130C
TCM_SETCURSEL = 0x130C - 1  # TCM_SETCURSELW = 0x130B
TCIF_TEXT = 1

class TCITEMW(ctypes.Structure):
    _fields_ = [
        ("mask", ctypes.c_uint),
        ("dwState", ctypes.c_uint),
        ("dwStateMask", ctypes.c_uint),
        ("pszText", ctypes.c_wchar_p),
        ("cchTextMax", ctypes.c_int),
        ("iImage", ctypes.c_int),
        ("lParam", ctypes.c_void_p),
    ]

count = u.SendMessageW(TAB, TCM_GETITEMCOUNT, 0, 0)
print("tab count:", count)
names = []
for i in range(count):
    buf = ctypes.create_unicode_buffer(64)
    item = TCITEMW()
    item.mask = TCIF_TEXT
    item.pszText = ctypes.cast(buf, ctypes.c_wchar_p)
    item.cchTextMax = 64
    u.SendMessageW(TAB, TCM_GETITEM, i, ctypes.byref(item))
    names.append(buf.value)
print("tabs:", names)

# switch to 內容 tab (index 0) via TCM_SETCURSEL (message, no mouse)
if names and "內容" in names:
    idx = names.index("內容")
    r = u.SendMessageW(TAB, TCM_SETCURSEL, idx, 0)
    print(f"switched to 內容 (idx {idx}), rc={r}")
