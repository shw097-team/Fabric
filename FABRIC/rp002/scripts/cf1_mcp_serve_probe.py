# -*- coding: utf-8 -*-
"""CF1 probe — run `hermes mcp serve` (Hermes as MCP server) and verify it speaks MCP over stdio."""
import json, os, subprocess, sys, time
from pathlib import Path

HERMES = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe"
HOME = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home"

env = os.environ.copy()
env["HERMES_HOME"] = HOME
env.pop("PYTHONPATH", None)

p = subprocess.Popen([HERMES, "mcp", "serve", "--accept-hooks"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     env=env, text=True, encoding="utf-8", errors="replace")

def send(msg):
    p.stdin.write(json.dumps(msg) + "\n")
    p.stdin.flush()

def read_line(timeout=20):
    import select
    if hasattr(select, "poll"):
        import errno
        poll = select.poll()
        poll.register(p.stdout, select.POLLIN)
        if not poll.poll(timeout * 1000):
            return None
    return p.stdout.readline().strip()

try:
    # MCP initialize handshake
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                     "clientInfo": {"name": "cf1-probe", "version": "0.1"}}})
    resp = read_line(30)
    print("INIT", resp[:300] if resp else "TIMEOUT")
    # tools/list discovery
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    resp2 = read_line(30)
    print("TOOLS", (resp2 or "TIMEOUT")[:300])
    ok = resp and '"result"' in resp and resp2 and ("tools" in resp2 or "error" in resp2)
    print("CF1_MCP_SERVE_OK", bool(ok))
finally:
    try:
        p.stdin.close()
    except Exception:
        pass
    try:
        p.terminate()
    except Exception:
        pass
    try:
        p.wait(timeout=10)
    except Exception:
        p.kill()
    sys.exit(0 if ok else 1)
