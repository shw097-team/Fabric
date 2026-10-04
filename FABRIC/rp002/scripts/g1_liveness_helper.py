# -*- coding: utf-8 -*-
"""G1 liveness canary helper — inject env-ref credential and drive kanban worker."""
import os, re, subprocess, sys, time

HOME = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home"
HERMES = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe"
DESKTOP_ENV = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", ".env")

def load_env_ref(name):
    if not os.path.exists(DESKTOP_ENV):
        return None
    for line in open(DESKTOP_ENV, encoding="utf-8", errors="replace"):
        line = line.strip().strip('"')
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"')
    return None

def run(args, timeout=180):
    env = os.environ.copy()
    env["HERMES_HOME"] = HOME
    key = load_env_ref("OPENCODE_GO_API_KEY")
    if key:
        env["OPENCODE_GO_API_KEY"] = key
    p = subprocess.run([HERMES] + args, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

mode = sys.argv[1] if len(sys.argv) > 1 else "status"
if mode == "status":
    rc, out = run(["kanban", "show", "t_e3abb7d8"])
    print("SHOW_RC", rc)
    print(out[:2000])
elif mode == "reclaim":
    rc, out = run(["kanban", "reclaim", "t_e3abb7d8"])
    print("RECLAIM_RC", rc)
    print(out[:1500])
elif mode == "dispatch":
    rc, out = run(["kanban", "dispatch", "--max", "1"])
    print("DISPATCH_RC", rc)
    print(out[:1500])
