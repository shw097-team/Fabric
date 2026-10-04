# -*- coding: utf-8 -*-
"""FAR v18: monkeypatch-test open_radar replacement BEFORE patching repo file."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq-auto-skill\.agents\skills\xq-xscript-compiler\scripts")
import time
from pywinauto import Desktop

RADAR_TITLE = "策略雷達 - XQ全球贏家(個人版)"

def open_radar_patched():
    """Patched open_radar: title-based lookup with retry."""
    import win32con
    import win32gui
    desktop32 = Desktop(backend="win32")
    existing = desktop32.window(title=RADAR_TITLE)
    if existing.exists(timeout=0.5):
        wrapper = existing.wrapper_object()
        opened = not wrapper.is_visible()
        if opened:
            win32gui.ShowWindow(wrapper.handle, win32con.SW_SHOW)
        existing.wait("visible enabled", timeout=10)
        return existing, opened
    # open via menu — title match on main window (more robust than class_name)
    desktop = Desktop(backend="uia")
    main = desktop.window(title_re="XQ全球贏家.*")
    if not main.exists(timeout=5):
        raise RuntimeError("XQ main window not found by title")
    strategy = [i for i in main.descendants(control_type="MenuItem")
                if i.window_text() == "策略(D)" and i.is_visible()]
    if not strategy:
        raise RuntimeError("策略(D) menu not found")
    strategy[0].click_input()
    time.sleep(0.5)
    radar_items = [i for i in main.descendants(control_type="MenuItem")
                   if "策略雷達" in i.window_text() and i.is_visible()]
    if not radar_items:
        raise RuntimeError("策略雷達 menu not found")
    radar_items[0].click_input()
    window = desktop32.window(title=RADAR_TITLE)
    window.wait("visible enabled", timeout=10)
    return window, True

# test
try:
    radar, opened = open_radar_patched()
    print("open_radar OK, opened:", opened)
except Exception as e:
    print("EXC:", type(e).__name__, str(e)[:200])
