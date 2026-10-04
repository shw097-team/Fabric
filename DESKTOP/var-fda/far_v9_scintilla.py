# -*- coding: utf-8 -*-
"""FAR v9: inspect editor Scintilla control + current state."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
editor = d32.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)
print("editor:", editor.window_text()[:60])

# enumerate children classes
classes = {}
for c in editor.children():
    cls = c.class_name()
    classes[cls] = classes.get(cls, 0) + 1
print("children classes:", classes)

# find Scintilla
scis = editor.children(class_name="Scintilla")
print("Scintilla:", len(scis))
if scis:
    import win32gui
    sci = scis[0]
    # SCI_GETTEXTLENGTH = 2183
    length = win32gui.SendMessage(sci.handle, 2183, 0, 0)
    print("scintilla text length:", length)
    # SCI_GETCURRENTPOS / line count
    print("scintilla rect:", sci.rectangle())
