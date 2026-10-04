# -*- coding: utf-8 -*-
"""FAR v14: run community xq_alert.py probe against FDA_PAPER_ALERT (no params yet)."""
import subprocess
import sys
import time

# use the venv python
PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"
SCRIPT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\xq-auto-skill\.agents\skills\xq-xscript-compiler\scripts\xq_alert.py"

# inject site-packages
env = {"PYTHONPATH": r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages"}

cmd = [
    PY, SCRIPT,
    "--script-name", "FDA_PAPER_ALERT",
    "--product-code", "2330",
    "--product-readback", "台積電(2330)",
    "--parameter-label", "1觸發，0不觸發",
    "--timeout", "25",
    "--strategy-prefix", "FDAPaperProbe",
]
print("running:", " ".join(cmd[-14:]))
r = subprocess.run(cmd, capture_output=True, timeout=300, env=env, text=True)
print("exit:", r.returncode)
print("stdout:", r.stdout[-3000:])
print("stderr:", r.stderr[-500:])
