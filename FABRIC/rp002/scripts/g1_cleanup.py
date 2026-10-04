# -*- coding: utf-8 -*-
"""G1 helper — archive leftover kanban tasks."""
import os, subprocess, sys

HOME = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home"
HERMES = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe"

def run(args):
    env = os.environ.copy()
    env["HERMES_HOME"] = HOME
    env.pop("PYTHONPATH", None)
    p = subprocess.run([HERMES] + args, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=120)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

for t in ["t_24e57de1", "t_47548ffb", "t_e3abb7d8", "t_e52f058b"]:
    rc, out = run(["kanban", "archive", t])
    print(t, rc, out.strip()[:100])
