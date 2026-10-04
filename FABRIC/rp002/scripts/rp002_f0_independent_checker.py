# -*- coding: utf-8 -*-
"""RP-002 F0 — INDEPENDENT checker (fresh read-only; maker != checker)."""
import json, subprocess, sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
CONSUMER = FAB / "fabric" / "consumers" / "hgk_policy_consumer.py"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

ev = json.loads((FAB / "rp002" / "F0" / "RP002_F0_EVIDENCE.json").read_text(encoding="utf-8"))
check("F0I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# re-run consumer selfcheck fresh
p = subprocess.run([sys.executable, str(CONSUMER), "selfcheck"], capture_output=True, text=True,
                   encoding="utf-8", errors="replace", timeout=120)
check("F0I_CONSUMER_RERUN", p.returncode == 0 and "CONSUMER_OK" in (p.stdout or ""), (p.stdout or "")[-80:])

# contracts non-empty
for c in ("AUTHORITY_MATRIX.yaml", "RISK_CLASSES.yaml", "PROMOTION_POLICY.yaml"):
    check(f"F0I_{c.split('.')[0]}", (FAB / "fabric" / c).stat().st_size > 200, c)

# router canonical artifact exists (single route truth)
check("F0I_ROUTER_CANONICAL", "ORACLE_TO_HGK" in (FAB / "rp002" / "RP002_CHANGE_CLASS_ROUTER.yaml").read_text(encoding="utf-8"), "router")

# every required canary class has a binding trace in maker evidence
traces = ev.get("binding_traces", {})
for cls in ("RUNTIME_TRANSIENT", "CONFIG_PREAPPROVED", "PROFILE_CHANGE", "SKILL_CHANGE",
            "PIPELINE_CHANGE", "STACK_CHANGE", "PROVIDER_UPGRADE", "DOMAIN_CHANGE", "CONSTITUTIONAL_CHANGE"):
    check(f"F0I_TRACE_{cls}", traces.get(cls, {}).get("verdict") == "ROUTE_OK", json.dumps(traces.get(cls, {}))[:80])

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_F0_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(FAB / "rp002" / "F0" / "RP002_F0_INDEPENDENT_CHECKER.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
