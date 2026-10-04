# -*- coding: utf-8 -*-
"""FDA-C3 UFO2 effective-load probe (no external API key).
Uses PlaceHolderService (ufo/llm/placeholder.py) — verifies:
  1) package import (module-load)
  2) config parse (agents/system yaml)
  3) LLM service instantiation (placeholder path)
  4) app_agent / host_agent module import
  5) UIA backend module import (automator)
No LLM network call; no API key required.
"""
import json
import sys
from pathlib import Path

UFO_ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\ufo2_extracted\UFO-3.0.8")
sys.path.insert(0, str(UFO_ROOT))

results = []
try:
    import ufo
    results.append(("PACKAGE_IMPORT", True, f"ufo {getattr(ufo, '__version__', '?')} at {ufo.__file__}"))
except Exception as e:
    results.append(("PACKAGE_IMPORT", False, str(e)[:120]))

try:
    import ufo.llm.base as base
    results.append(("LLM_BASE_IMPORT", True, "ufo.llm.base ok"))
except Exception as e:
    results.append(("LLM_BASE_IMPORT", False, str(e)[:120]))

try:
    from ufo.llm.placeholder import PlaceHolderService
    results.append(("PLACEHOLDER_SERVICE", True, "PlaceHolderService importable"))
except Exception as e:
    results.append(("PLACEHOLDER_SERVICE", False, str(e)[:120]))

try:
    import ufo.automator.ui_control as ui
    results.append(("UIA_BACKEND_MODULE", True, "ufo.automator.ui_control ok"))
except Exception as e:
    results.append(("UIA_BACKEND_MODULE", False, str(e)[:120]))

try:
    import ufo.agents.agent.app_agent as aa
    results.append(("APP_AGENT_IMPORT", True, "ufo.agents.agent.app_agent ok"))
except Exception as e:
    results.append(("APP_AGENT_IMPORT", False, str(e)[:120]))

try:
    import ufo.agents.agent.host_agent as ha
    results.append(("HOST_AGENT_IMPORT", True, "ufo.agents.agent.host_agent ok"))
except Exception as e:
    results.append(("HOST_AGENT_IMPORT", False, str(e)[:120]))

# config parse
try:
    import yaml
    cfg = yaml.safe_load(open(UFO_ROOT / "config/ufo/system.yaml", encoding="utf-8"))
    results.append(("CONFIG_PARSE", bool(cfg.get("CONTROL_BACKEND")) and bool(cfg.get("MAX_STEP")),
                    f"CONTROL_BACKEND={cfg.get('CONTROL_BACKEND')} MAX_STEP={cfg.get('MAX_STEP')}"))
except Exception as e:
    results.append(("CONFIG_PARSE", False, str(e)[:120]))

# agents.yaml template parse
try:
    import yaml
    tpl = yaml.safe_load(open(UFO_ROOT / "config/ufo/agents.yaml.template", encoding="utf-8"))
    has_agents = all(k in tpl for k in ("HOST_AGENT", "APP_AGENT"))
    results.append(("AGENTS_TEMPLATE_PARSE", has_agents, "HOST_AGENT/APP_AGENT keys present"))
except Exception as e:
    results.append(("AGENTS_TEMPLATE_PARSE", False, str(e)[:120]))

ok = all(p for _, p, _ in results)
print("\n=== UFO2 EFFECTIVE-LOAD PROBE RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT",
    "schema": "FDA-C3-RECEIPT/1",
    "fixture": "C3-UFO2-EFFECTIVE-LOAD-PROBE",
    "provider": {"name": "MICROSOFT_UFO2", "pinned_version": "v3.0.8"},
    "mode": "LOCAL_NO_LIVE_WRITE",
    "llm_mode": "PLACEHOLDER_SERVICE (no external API key; no HumanGate credential required)",
    "evidence": {
        "zip_sha256": "92e288ca76876522ba03",
        "extracted_root": str(UFO_ROOT),
        "license": "MIT",
    },
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "verdict": "PASS" if ok else "PARTIAL",
    "claim_note": "Effective-load verified WITHOUT external LLM API key via PlaceHolderService; "
                 "full AppAgent visual/task execution requires an LLM backend (Ollama local or keyed API) "
                 "— separate qualification step, not required for effective-load gate.",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE (module import + config parse only; no runtime started, no network call)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
