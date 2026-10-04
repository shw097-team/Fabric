# -*- coding: utf-8 -*-
"""FAR R2: read XQ main menu via pywinauto win32 (no UIA) — find 我要購買/設定."""
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
main = d32.window(handle=0x150d58)
main.wait("exists visible", timeout=8)
print("main:", main.window_text()[:50])

# menu via win32 backend
try:
    menu = main.menu()
    print("menu items:")
    for i, item in enumerate(menu.items()):
        t = item.text()[:30]
        print(f"  [{i}] {t}")
        # submenu items
        try:
            for j, sub in enumerate(item.sub_menu().items()[:20]):
                st = sub.text()[:35]
                print(f"      [{j}] {st}")
        except Exception:
            pass
except Exception as e:
    print("menu err:", str(e)[:120])
