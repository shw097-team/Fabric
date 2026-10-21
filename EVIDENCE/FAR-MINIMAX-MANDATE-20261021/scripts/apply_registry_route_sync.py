#!/usr/bin/env python
"""Synchronise the registry's own route rows with the canonical pool.

The pool (`config/lane-route-slots.candidate.json`) is the single source of truth for
which arms exist and in what order.  The assignment projection
(`config/model-lane-assignment.json`) is derived from the pool.  The registry
(`config/lane-routing-registry.yaml`) declares the routes, but its `routes[]` rows
carry their own copies of:

  * ``fallbacks[]``          - the chain *minus* the head
  * ``canonical_identity``  - the head arm's identity
  * ``arms[]``              - the full chain with arm roles
  * ``selected_arm_identity`` / ``selected_arm`` - the head
  * ``admission_status``    - measured admission state
  * ``admission_evidence``  - what was actually measured

``check_drift`` compares the registry's *projections* against the live sites.  It
does NOT compare the registry's internal route rows against the pool.  That gap is
how a route row can keep advertising a superseded model (e.g. ``gpt-6.1-sol``)
while the pool and the assignment both say ``minimax-m3.1-flash-free`` - and the
drift checker still reports no findings.

This script closes that gap: it rewrites the registry route rows FROM the pool,
then records the admission state that was actually measured for the head arm.

It is deliberately conservative:
  * it never touches the pool or the assignment (those are inputs, not outputs);
  * it never invents an admission status - if the measured evidence for the new
    head arm is absent, the status becomes UNPROVEN rather than ADMITTED;
  * it preserves every field it does not own.

Usage:
    python var/FAR-MINIMAX-MANDATE-20261021/apply_registry_route_sync.py --dry-run
    python var/FAR-MINIMAX-MANDATE-20261021/apply_registry_route_sync.py --apply
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml

HG = Path(__file__).resolve().parents[2]
POOL = HG / "config" / "lane-route-slots.candidate.json"
REGISTRY = HG / "config" / "lane-routing-registry.yaml"
ASSIGNMENT = HG / "config" / "model-lane-assignment.json"
ADMISSION_DIR = HG / "var" / "FAR-MINIMAX-MANDATE-20261021" / "admission"

LANE_OF_GROUP = {
    "PLAN": "PLAN",
    "EXECUTE": "EXECUTE",
    "VERIFY_SECURITY": "VERIFY_SECURITY",
}


def load_pool() -> dict[str, dict[str, Any]]:
    doc = json.loads(POOL.read_text(encoding="utf-8"))
    lanes = doc["lanes"] if isinstance(doc, dict) and "lanes" in doc else doc
    out: dict[str, dict[str, Any]] = {}
    for lane in lanes:
        name = lane.get("lane") or lane.get("id") or lane.get("name")
        if name:
            out[name] = lane
    return out


def arm_from_pool_entry(entry: dict[str, Any], role: str, default: bool) -> dict[str, Any]:
    """Build a registry arm record from a pool entry.

    The pool entry is authoritative for provider/model/transport.  The registry
    additionally records auth and reasoning effort, which the pool does not carry
    for every arm, so we keep whatever the registry already had for that identity
    when it is available and only fall back to a conservative default.
    """
    provider = entry["provider"]
    model = entry["model"]
    arm: dict[str, Any] = {
        "arm": role,
        "provider": provider,
        "model": model,
        "canonical_identity": model,
        "auth": entry.get("auth", "env_ref:OPENCODE_GO_API_KEY"),
        "oauth": bool(entry.get("oauth", False)),
        "default": default,
        "automatic_selection": bool(entry.get("automatic_selection", default)),
    }
    if entry.get("reasoning_effort"):
        arm["reasoning_effort"] = entry["reasoning_effort"]
    elif entry.get("transport_model"):
        arm["transport_model"] = entry["transport_model"]
    return arm


def sync_route(route: dict[str, Any], pool_lane: dict[str, Any]) -> list[str]:
    """Rewrite one registry route row from the pool.  Returns a list of changes."""
    changes: list[str] = []
    entries = list(pool_lane.get("ordered_pool", []))
    if not entries:
        return changes

    head = entries[0]
    rest = entries[1:]
    # the pool is authoritative for the auth posture too; a pool entry may omit it, in which
    # case the existing registry value is kept (see arm_from_pool_entry)

    # --- head arm -----------------------------------------------------------
    head_model = head["model"]
    head_provider = head["provider"]

    if route.get("canonical_identity") != head_model:
        changes.append(
            f"canonical_identity {route.get('canonical_identity')!r} -> {head_model!r}"
        )
        route["canonical_identity"] = head_model
    if route.get("provider") != head_provider:
        changes.append(f"provider {route.get('provider')!r} -> {head_provider!r}")
        route["provider"] = head_provider
    if route.get("model") != head_model:
        changes.append(f"model {route.get('model')!r} -> {head_model!r}")
        route["model"] = head_model

    # --- route-level auth posture -------------------------------------------
    # The route row also carries its own auth posture at the TOP level, next to provider/model.
    # That copy was NOT covered by the arms[] rewrite, so after a re-binding to a key-auth arm
    # the route could still advertise `auth: openai_oauth, oauth: true, reasoning_effort: medium`
    # while the pool's rank-1 arm is `env_ref:OPENCODE_GO_API_KEY, oauth: false`.  An independent
    # acceptance officer caught exactly this.  The route-level posture must follow the pool.
    for key, want in (("auth", head.get("auth")),
                      ("oauth", bool(head.get("oauth", False))),
                      ("reasoning_effort", head.get("reasoning_effort"))):
        if key not in route:
            continue
        have = route.get(key)
        if have != want:
            changes.append(f"{key} {have!r} -> {want!r} (route-level posture must follow the pool)")
            route[key] = want

    # --- arms[] -------------------------------------------------------------
    new_arms: list[dict[str, Any]] = []
    old_by_identity = {
        a.get("canonical_identity"): a
        for a in route.get("arms", [])
        if isinstance(a, dict)
    }
    for idx, entry in enumerate(entries):
        role = "primary" if idx == 0 else f"fallback{idx}"
        # Prefer the registry's existing record for this identity (it carries
        # auth / reasoning-effort detail the pool lacks), but the provider/model
        # and the selection flags always come from the pool.
        prior = old_by_identity.get(entry["model"], {})
        arm = arm_from_pool_entry(entry, role, default=(idx == 0))
        if prior:
            for key in ("auth", "oauth", "reasoning_effort"):
                if key in prior and key not in entry:
                    arm[key] = prior[key]
        new_arms.append(arm)

    if new_arms != route.get("arms"):
        changes.append(f"arms[] rewritten ({len(route.get('arms', []))} -> {len(new_arms)} entries)")
        route["arms"] = new_arms

    # --- fallbacks[] --------------------------------------------------------
    new_fallbacks: list[dict[str, Any]] = []
    for entry in rest:
        prior = old_by_identity.get(entry["model"], {})
        fb = {
            "provider": entry["provider"],
            "model": entry["model"],
            "canonical_identity": entry["model"],
            "auth": entry.get("auth", prior.get("auth", "env_ref:OPENCODE_GO_API_KEY")),
            "oauth": bool(entry.get("oauth", prior.get("oauth", False))),
        }
        new_fallbacks.append(fb)
    if new_fallbacks != route.get("fallbacks"):
        changes.append(
            f"fallbacks[] rewritten ({len(route.get('fallbacks', []))} -> {len(new_fallbacks)} entries)"
        )
        route["fallbacks"] = new_fallbacks

    # --- selected arm -------------------------------------------------------
    for key in ("selected_arm_identity", "selected_arm"):
        if key in route:
            want = head_model if key.endswith("identity") else "A"
            if route.get(key) != want:
                changes.append(f"{key} {route.get(key)!r} -> {want!r}")
                route[key] = want

    return changes


def measured_admission() -> dict[str, dict[str, Any]]:
    """Read the measured HGK lane-admission receipts for this round.

    Each receipt is `HGK-LANE-ADMISSION/1` and records the served identity plus the
    dispatcher evidence reference (required_arm == served_arm, exit code, nonce and
    tool-echo outcome).  A lane with no receipt is UNPROVEN, never ADMITTED.
    """
    out: dict[str, dict[str, Any]] = {}
    if not ADMISSION_DIR.is_dir():
        return out
    for path in sorted(ADMISSION_DIR.glob("*.json")):
        if path.name == "admission_summary.json":
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        lane = doc.get("lane")
        if lane:
            out[lane] = doc
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the registry back")
    ap.add_argument("--dry-run", action="store_true", help="report only (default)")
    args = ap.parse_args()

    pool = load_pool()
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    reg = copy.deepcopy(reg)
    receipts = measured_admission()

    report: list[dict[str, Any]] = []
    for route in reg.get("routes", []):
        lane = route.get("lane")
        pool_lane = pool.get(lane)
        if not pool_lane:
            report.append({"lane": lane, "changes": ["NO POOL ENTRY - left untouched"]})
            continue
        before = copy.deepcopy(route)
        changes = sync_route(route, pool_lane)

        # admission: only record what was measured for THIS head arm.
        receipt = receipts.get(lane)
        head_model = pool_lane["ordered_pool"][0]["model"]
        if receipt:
            served = receipt.get("served") or {}
            served_id = f"{served.get('provider')}/{served.get('model')}"
            exercise = receipt.get("lane_exercise") or {}
            evidence_ref = exercise.get("evidence_ref")
            status = receipt.get("status")
            if status == "ADMITTED" and served.get("model") == head_model and evidence_ref:
                evidence = (
                    f"MEASURED 2026-10-21 (HGK-LANE-ADMISSION/1, probe {receipt.get('probe_id')}): "
                    f"served identity {served_id}; lane-shaped exercise completed "
                    f"(model calls={exercise.get('completed_model_calls')}, tools={exercise.get('completed_tools')}); "
                    f"dispatcher evidence: {evidence_ref}"
                )
                if route.get("admission_status") != "ADMITTED":
                    changes.append(
                        f"admission_status {route.get('admission_status')!r} -> 'ADMITTED'"
                    )
                    route["admission_status"] = "ADMITTED"
                if route.get("admission_evidence") != evidence:
                    changes.append("admission_evidence replaced (it still advertised a superseded arm)")
                    route["admission_evidence"] = evidence
            else:
                if route.get("admission_status") == "ADMITTED":
                    changes.append(
                        f"admission_status 'ADMITTED' -> 'UNPROVEN' (receipt status={status!r}, "
                        f"served={served_id!r})"
                    )
                    route["admission_status"] = "UNPROVEN"
                route["admission_evidence"] = (
                    f"NO MEASURED RECEIPT for the current head arm {head_model}; "
                    f"last receipt status={status!r}"
                )
        else:
            if route.get("admission_status") == "ADMITTED":
                changes.append(
                    f"admission_status 'ADMITTED' -> 'UNPROVEN' (no measured receipt on file)"
                )
                route["admission_status"] = "UNPROVEN"
            route["admission_evidence"] = (
                f"NO MEASURED RECEIPT for the current head arm {head_model}"
            )

        report.append({"lane": lane, "changes": changes, "before": before, "after": route})

    total = sum(len(r["changes"]) for r in report)
    print(json.dumps({"total_changes": total, "lanes": [
        {"lane": r["lane"], "changes": r["changes"]} for r in report]}, indent=1, ensure_ascii=False))

    if not args.apply:
        print("\nDRY RUN - registry not written")
        return 0

    if total:
        REGISTRY.write_text(
            yaml.safe_dump(reg, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        print(f"\nWROTE {REGISTRY}")
    else:
        print("\nNo change needed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
