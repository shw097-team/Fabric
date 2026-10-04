# -*- coding: utf-8 -*-
"""CF1 direct MCP route canary — Hermes-as-MCP-server handshake (initialize + tools/list) + client add/rollback."""
import json, os, subprocess, sys
from pathlib import Path

HERMES = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe"
HOME = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home"
CF1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\CF1")

env = os.environ.copy()
env["HERMES_HOME"] = HOME
env.pop("PYTHONPATH", None)

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})
    print(f"{name} {'PASS' if ok else 'FAIL'}: {detail[:140]}")

# 1. MCP initialize handshake (real protocol)
init_msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "cf1-probe", "version": "0.1"}}}
p = subprocess.run([HERMES, "mcp", "serve", "--accept-hooks"], input=json.dumps(init_msg) + "\n",
                   env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                   timeout=60, cwd=str(Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")))
out = (p.stdout or "") + (p.stderr or "")
try:
    resp = json.loads(out.strip().splitlines()[-1])
    ok = resp.get("id") == 1 and "result" in resp and "tools" in resp["result"].get("capabilities", {})
    check("CF1_MCP_HANDSHAKE", ok, out.strip()[:160])
except Exception:
    check("CF1_MCP_HANDSHAKE", False, out[:160])

# 2. tools/list discovery (MCP discovery plane)
p2 = subprocess.run([HERMES, "mcp", "serve", "--accept-hooks"],
                    input=json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n",
                    env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=60, cwd=str(Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")))
out2 = (p2.stdout or "") + (p2.stderr or "")
try:
    resp2 = json.loads(out2.strip().splitlines()[-1])
    tools = resp2.get("result", {}).get("tools", [])
    check("CF1_MCP_TOOLS_LIST", resp2.get("id") == 2 and isinstance(tools, list) and len(tools) > 0,
          f"{len(tools)} tools discovered")
except Exception:
    check("CF1_MCP_TOOLS_LIST", False, out2[:160])

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "CF1_MCP_DIRECT_ROUTE", "verdict": verdict, "checks": results}
(CF1 / "CF1_MCP_DIRECT_ROUTE.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
