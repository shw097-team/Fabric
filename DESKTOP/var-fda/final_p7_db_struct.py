# -*- coding: utf-8 -*-
"""FINAL P7: DB check for probe strategies + full radar window structure."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
user32 = ctypes.windll.user32

# 1. DB: any FDAPaperProbe strategies in XSStrategyCenter?
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("tables:", tables)
for t in tables:
    try:
        cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})").fetchall()]
        if any("Name" in col or "Enable" in col for col in cols):
            rows = c.execute(f"SELECT * FROM {t} LIMIT 3").fetchall()
            print(f"--- {t} ({len(rows)} shown) cols={cols}")
            for r in rows:
                print("   ", [str(x)[:25] for x in r][:8])
    except Exception as e:
        pass
c.close()

# 2. full radar window children dump (all)
RADAR = 0x110d96
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    cid = user32.GetDlgCtrlID(ch)
    r = wt.RECT()
    user32.GetWindowRect(ch, ctypes.byref(r))
    out.append({"hwnd": ch, "text": t.value[:30], "class": cls.value[:22], "cid": cid,
                "x": r.left, "y": r.top, "w": r.right - r.left, "h": r.bottom - r.top})
    return True
user32.EnumChildWindows(RADAR, cb, 0)
print(f"=== radar children: {len(out)} ===")
for c in out:
    print(f"  {hex(c['hwnd'])} id={c['cid']} {c['class']!r} '{c['text']}' ({c['x']},{c['y']},{c['w']}x{c['h']})")
