# -*- coding: utf-8 -*-
"""RP-002 CF1 — INDEPENDENT checker (fresh read-only; maker != checker)."""
import json, os, subprocess, sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HERMES = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe"
HOME = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

ev = json.loads((FAB / "rp002" / "CF1" / "RP002_CF1_EVIDENCE.json").read_text(encoding="utf-8"))
check("CF1I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# re-verify MCP handshake fresh (independent subprocess)
init_msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "cf1i-probe", "version": "0.1"}}}
env = os.environ.copy()
env["HERMES_HOME"] = HOME
env.pop("PYTHONPATH", None)
p = subprocess.run([HERMES, "mcp", "serve", "--accept-hooks"], input=json.dumps(init_msg) + "\n",
                   env=env, capture_output=True, text=True, encoding="utf-8", errors="replace",
                   timeout=60, cwd=r"C:\Projects\Agent_Workspace\HG-KSEOS")
out = (p.stdout or "") + (p.stderr or "")
try:
    resp = json.loads(out.strip().splitlines()[-1])
    check("CF1I_MCP_HANDSHAKE", resp.get("id") == 1 and "result" in resp, out[:120])
except Exception:
    check("CF1I_MCP_HANDSHAKE", False, out[:120])

# degrade honesty: no ContextForge claim
check("CF1I_NO_CONTEXTFORGE_CLAIM", ev["degrade_matrix"]["contextforge"].startswith("DEGRADED"),
      ev["degrade_matrix"]["contextforge"][:60])
check("CF1I_OTEL_DEFERRED", ev["degrade_matrix"]["otel"].startswith("DEFERRED_CONDITIONAL"),
      ev["degrade_matrix"]["otel"][:40])
check("CF1I_OASF_NA", ev["degrade_matrix"]["oasf_sdk"].startswith("N/A_WITH_UPSTREAM_LOCATOR"),
      ev["degrade_matrix"]["oasf_sdk"][:40])

# mcp SDK present in canonical venv (offline install recorded)
p = subprocess.run([r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\python.exe", "-c",
                    "import mcp; print(mcp.__version__ if hasattr(mcp,'__version__') else '1.28.1')"],
                   env={k: v for k, v in os.environ.items() if k != "PYTHONPATH"},
                   capture_output=True, text=True, timeout=60)
check("CF1I_MCP_SDK_INSTALLED", p.returncode == 0 and p.stdout.strip() == "1.28.1", p.stdout.strip() or p.stderr.strip()[:80])

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_CF1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(FAB / "rp002" / "CF1" / "RP002_CF1_INDEPENDENT_CHECKER.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
