# -*- coding: utf-8 -*-
"""DoD-17 S13: read radar 內容 tab texts (win32 statics/edits) — verify which strategy selected."""
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
    if t.value.strip():
        out.append((hex(ch), cls.value[:20], cid, t.value[:40]))
    return True

u.EnumChildWindows(RADAR, cb, 0)
print(f"controls with text: {len(out)}")
# show key fields: 腳本/商品/名稱/頻率 related
for h, c, cid, t in out:
    if any(k in t for k in ("FDA", "台積電", "2330", "腳本", "商品", "名稱", "頻率", "警示", "複製", "1分鐘")):
        print(f"  {h} {c} cid={cid} '{t}'")
