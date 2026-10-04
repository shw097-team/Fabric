# -*- coding: utf-8 -*-
"""FAR v10: open FDA_PAPER_ALERT via 開啟 dialog (pywinauto uia for toolbar, win32 for dialog)."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

du = Desktop(backend="uia")
editor = du.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# 1. click 開啟 toolbar button (uia)
open_btn = [b for b in editor.descendants(control_type="Button")
            if b.window_text().strip() == "開啟" and b.is_visible()]
print("開啟 buttons:", len(open_btn))
if not open_btn:
    raise SystemExit(2)
try:
    open_btn[0].click()
    print("clicked 開啟")
except Exception as e:
    print("click err:", str(e)[:80])
time.sleep(3)

# 2. find 開啟 dialog (win32)
d32 = Desktop(backend="win32")
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        t = w.window_text()
        if t.strip() == "開啟":
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    print("no 開啟 dialog; listing #32770 with text:")
    for w in d32.windows(class_name="#32770"):
        try:
            t = w.window_text()
            if t.strip():
                print("  ", repr(t[:30]))
        except Exception:
            pass
    raise SystemExit(2)
print("開啟 dialog:", hex(dlg.handle))

# 3. enumerate dialog structure (buttons: 指標/選股/警示/交易/函數/確認)
du2 = Desktop(backend="uia")
dlg_uia = du2.window(handle=dlg.handle)
for b in dlg_uia.descendants(control_type="Button"):
    t = b.window_text().strip()
    if t:
        print("  btn:", repr(t[:15]))
