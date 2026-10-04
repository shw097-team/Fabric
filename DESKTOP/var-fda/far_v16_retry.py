# -*- coding: utf-8 -*-
"""FAR v16: close editor (win32 WM_CLOSE), then re-run xq_alert.py."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import subprocess
import time
from pywinauto import Desktop

# 1. close XScript editor if open
d32 = Desktop(backend="win32")
for w in d32.windows():
    try:
        if w.is_visible() and "XScript 編輯器" in w.window_text():
            w.close()
            print("closed editor:", w.window_text()[:40])
            time.sleep(2)
    except Exception:
        pass

# 2. re-run xq_alert.py
PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"
SCRIPT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq-auto-skill\.agents\skills\xq-xscript-compiler\scripts\xq_alert.py"
env = {"PYTHONPATH": r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages"}
cmd = [PY, SCRIPT,
       "--script-name", "FDA_PAPER_ALERT",
       "--product-code", "2330",
       "--product-readback", "台積電(2330)",
       "--timeout", "25",
       "--strategy-prefix", "FDAPaperProbe"]
r = subprocess.run(cmd, capture_output=True, timeout=300, env=env, text=True)
print("exit:", r.returncode)
print("stdout:", r.stdout[-2500:])
