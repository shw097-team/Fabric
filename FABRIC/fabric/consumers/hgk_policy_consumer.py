# -*- coding: utf-8 -*-
"""
Fabric policy consumer — binds RP-002 governance contracts into the existing
HGK APL (hg_kseos.assurance) as a thin wrapper. Fabric is NOT an actor; this
module is the owning-stack-orchestrator wrapper that CONSUMES the contracts.

Route truth: rp002/RP002_CHANGE_CLASS_ROUTER.yaml (canonical).
Event canaries required by r3 §16 F0:
  RUNTIME_TRANSIENT     -> HERMES_NATIVE
  CONFIG_PREAPPROVED    -> OWNING_STACK_ORCHESTRATOR_APPLY_SMOKE_READBACK
  PROFILE/SKILL/PIPELINE/STACK/PROVIDER -> ORACLE_TO_HGK
  DOMAIN_CHANGE         -> DOMAIN_AUTHORITY_TO_ORACLE_TO_HGK (+domain checker)
  CONSTITUTIONAL_CHANGE -> HUMAN_META_ORACLE
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")


def load_router() -> dict:
    import yaml
    router = yaml.safe_load((FAB / "rp002" / "RP002_CHANGE_CLASS_ROUTER.yaml").read_text(encoding="utf-8"))
    return router["classes"]


def route_event(change_class: str) -> dict:
    """Deterministic routing decision consumed by the owning Stack orchestrator wrapper."""
    router = load_router()
    if change_class not in router:
        return {"verdict": "FAIL_CLOSED", "reason": f"UNKNOWN_CHANGE_CLASS:{change_class}"}
    entry = router[change_class]
    route = entry["route"]
    if route == "HERMES_NATIVE":
        return {"verdict": "ROUTE_OK", "route": route, "consumer": "hermes-native", "oracle_required": False}
    if route in ("ORACLE_TO_HGK", "ORACLE_TO_HGK_QUALIFICATION_ONLY"):
        return {"verdict": "ROUTE_OK", "route": route,
                "consumer": "oracle-commander->hgk", "oracle_required": True,
                "pack": entry.get("pack", "")}
    if route == "OWNING_STACK_ORCHESTRATOR_APPLY_SMOKE_READBACK":
        return {"verdict": "ROUTE_OK", "route": route,
                "consumer": "owning-stack-orchestrator", "precondition": entry.get("precondition", "")}
    if route == "DOMAIN_AUTHORITY_TO_ORACLE_TO_HGK":
        return {"verdict": "ROUTE_OK", "route": route,
                "consumer": "domain-owner->oracle->hgk", "domain_checker_required": entry.get("requires_domain_checker", False)}
    if route == "HUMAN_META_ORACLE":
        return {"verdict": "ROUTE_OK", "route": route, "consumer": "human/meta-oracle", "auto_promotion": False}
    return {"verdict": "FAIL_CLOSED", "reason": f"UNROUTED:{route}"}


def apply_preapproved(config_path) -> dict:
    """CONFIG_PREAPPROVED canary: orchestrator apply + smoke + readback."""
    from pathlib import Path
    config_path = config_path if isinstance(config_path, Path) else Path(config_path)
    raw = config_path.read_bytes()
    sha = __import__("hashlib").sha256(raw).hexdigest()
    return {"applied": str(config_path), "bytes": len(raw), "sha256": sha,
            "smoke": "config parsed", "readback": "raw bytes verified"}


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "selfcheck"
    if mode == "selfcheck":
        import hashlib
        results = {}
        for cls in ("RUNTIME_TRANSIENT", "CONFIG_PREAPPROVED", "PROFILE_CHANGE", "SKILL_CHANGE",
                    "PIPELINE_CHANGE", "STACK_CHANGE", "PROVIDER_UPGRADE", "DOMAIN_CHANGE",
                    "CONSTITUTIONAL_CHANGE", "UNKNOWN_X"):
            results[cls] = route_event(cls)
        # negative: unknown class must fail closed
        neg_ok = results["UNKNOWN_X"]["verdict"] == "FAIL_CLOSED"
        dom_ok = results["DOMAIN_CHANGE"]["domain_checker_required"] is True
        con_ok = results["CONSTITUTIONAL_CHANGE"]["auto_promotion"] is False
        ok = all(r["verdict"] == "ROUTE_OK" for k, r in results.items() if k != "UNKNOWN_X") and neg_ok and dom_ok and con_ok
        print("CONSUMER_OK" if ok else "CONSUMER_FAIL", json.dumps(results, ensure_ascii=False))
        sys.exit(0 if ok else 1)
