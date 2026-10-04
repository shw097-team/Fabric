# -*- coding: utf-8 -*-
"""FINAL P3b: run community xq_alert.py against radar window (already open)."""
import subprocess
import sys

PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"
SCRIPT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq-auto-skill\.agents\skills\xq-xscript-compiler\scripts\xq_alert.py"
env = {"PYTHONPATH": r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages"}

cmd = [PY, SCRIPT,
       "--script-name", "FDA_PAPER_ALERT",
       "--product-code", "2330",
       "--product-readback", "台積電(2330)",
       "--parameter-label", "1觸發，0不觸發",
       "--timeout", "30",
       "--strategy-prefix", "FDAPaperProbe"]
print("running xq_alert.py ...")
r = subprocess.run(cmd, capture_output=True, timeout=420, env=env, text=True)
print("exit:", r.returncode)
print("stdout:", r.stdout[-3500:])
if r.stderr.strip():
    print("stderr:", r.stderr[-600:])
