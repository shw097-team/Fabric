# -*- coding: utf-8 -*-
"""FAR v2: create FDA_PAPER_ALERT2 alert script via pywinauto (uia backend).
Editor 檔案(F) menu -> 新增(N) -> dialog: click 警示, set name, confirm.
"""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

desktop = Desktop(backend="uia")
main = desktop.window(class_name="DAQXQLITEMainWnd")

# 1. open XScript editor if not open
editor = desktop.window(title_re=".*XScript 編輯器.*")
if not editor.exists(timeout=1):
    strategy = [i for i in main.descendants(control_type="MenuItem")
                if i.window_text() == "策略(D)" and i.is_visible()]
    if not strategy:
        raise RuntimeError("策略(D) menu not found")
    strategy[0].click_input()
    time.sleep(0.5)
    ed_item = [i for i in main.descendants(control_type="MenuItem")
               if i.window_text() == "XScript 編輯器(E)" and i.is_visible()]
    if not ed_item:
        # try partial match
        ed_item = [i for i in main.descendants(control_type="MenuItem")
                   if "XScript 編輯器" in i.window_text() and i.is_visible()]
    if not ed_item:
        raise RuntimeError("XScript 編輯器 menu not found")
    ed_item[0].click_input()
    time.sleep(4)
    editor = desktop.window(title_re=".*XScript 編輯器.*")
    editor.wait("exists visible", timeout=10)
print("editor:", editor.window_text()[:60])

# 2. 檔案(F) menu -> 新增(N)
fmenu = [i for i in editor.descendants(control_type="MenuItem")
         if i.window_text().startswith("檔案") and i.is_visible()]
if not fmenu:
    raise RuntimeError("檔案 menu not found in editor")
fmenu[0].click_input()
time.sleep(0.8)
new_item = [i for i in editor.descendants(control_type="MenuItem")
            if i.window_text().startswith("新增") and i.is_visible()]
if not new_item:
    raise RuntimeError("新增 menu not found")
new_item[0].click_input()
time.sleep(1.5)

# 3. find 新增腳本 dialog (win32 backend for control ids)
d32 = Desktop(backend="win32")
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        if "新增腳本" in w.window_text():
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    raise RuntimeError("新增腳本 dialog not found")
print("dialog:", dlg.window_text())

# 4. click 警示 type button — find by text via uia
dlg_uia = Desktop(backend="uia").window(handle=dlg.handle)
# find 警示 button (it's a Button with text)
warn_btn = [b for b in dlg_uia.descendants(control_type="Button")
            if b.window_text() == "警示"]
if warn_btn:
    warn_btn[0].click_input()
    print("clicked 警示")
    time.sleep(0.8)

# 5. set name edit (control 17500? or first edit after 名稱：) via uia
# use win32 control ids: find Edit children
edits = dlg.children(class_name="Edit")
print("edits:", [(e.element_info.control_id(), e.window_text()) for e in edits])
