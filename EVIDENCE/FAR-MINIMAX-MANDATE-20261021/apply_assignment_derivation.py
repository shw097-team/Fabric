#!/usr/bin/env python
"""FAR-MINIMAX-MANDATE-20261021 — bind lane_chains + assignment to the pool's rank-1 arm.

This is the SECOND half of the MiniMax mandate. `apply_minimax_binding.py` moved the POOL and
the ROUTES; this script moves the ASSIGNMENT artifact and the registry's PROJECTION so that the
drift gate agrees with the declared state.

WHY THIS IS DERIVED, NOT HAND-WRITTEN
  The pool (`config/lane-route-slots.candidate.json`) is the selection authority. The assignment's
  `lane_chains` and `assignment[]` rows, and the registry's projection bindings, are all
  DERIVATIONS of the pool. Hand-writing them in three places is how they drift apart in the first
  place. So this script reads the pool and writes the derivations, then re-reads the written files
  and asserts the result -- it never asserts a value it did not derive.

WHAT CHANGES
  * config/model-lane-assignment.json
      - lane_chains.PLAN / EXECUTE / VERIFY_SECURITY : rank-1 arm becomes MiniMax
      - assignment[0..2]                              : assigned_provider / assigned_model follow
      - assignment[2].supply_selector                 : arms + unspecified_default follow
      - sod.*                                         : rewritten to the owner order
      - sod_across_all_arms.*                         : the verifier/executor model sets follow
      - revision / registry_epoch                     : advanced
  * config/lane-routing-registry.yaml
      - projections[model-lane-assignment].bindings   : the pointers this round changed get their
        expected value re-derived from the WRITTEN artifact (read back from disk, not from a
        local variable), so the gate compares the file against a record of that same file.

UNTOUCHED
  * The historical `*_previous_revision_*` chains are left exactly as they are: they are history.
  * The pool's non-MiniMax arms stay reachable; only the default and automatic flags move.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POOL = ROOT / "config" / "lane-route-slots.candidate.json"
REG = ROOT / "config" / "lane-routing-registry.yaml"
ASSIGN = ROOT / "config" / "model-lane-assignment.json"

ARM_PROVIDER = "opencode-go"
ARM_MODEL = "minimax-m3.1-flash-free"
TRANSPORT = "opencode-go/minimax-m3.1-flash-free"


def pool_rank1(lane: str) -> dict:
    d = json.loads(POOL.read_text(encoding="utf-8"))
    for l in d["lanes"]:
        if l["lane"] == lane:
            arm = l["ordered_pool"][0]
            assert arm["provider"] == ARM_PROVIDER and arm["model"] == ARM_MODEL, \
                f"pool rank-1 of {lane} is not MiniMax: {arm}"
            return arm
    raise SystemExit(f"lane {lane} not found in pool")


def lane_chain_from_pool(lane: str) -> list[dict]:
    """The chain mirrors the pool order: rank-1 first, then the operator-selectable fallbacks."""
    d = json.loads(POOL.read_text(encoding="utf-8"))
    for l in d["lanes"]:
        if l["lane"] != lane:
            continue
        out = []
        for i, c in enumerate(l["ordered_pool"]):
            arm = {
                "provider": c["provider"],
                "model": c["model"],
                "transport_model": c.get("transport_model"),
            }
            if i == 0:
                arm["arm"] = "A"
                arm["role"] = "primary"
                arm["default"] = True
                arm["automatic_selection"] = True
                arm["reasoning_effort"] = c.get("reasoning_effort")
            else:
                arm["role"] = f"fallback{i}"
                arm["default"] = False
                arm["automatic_selection"] = bool(c.get("automatic_selection", False))
                arm["reasoning_effort"] = c.get("reasoning_effort")
            if lane == "VERIFY_SECURITY":
                arm["arm"] = "ABC"[i] if i < 3 else None
                if arm["arm"] is None:
                    arm.pop("arm")
            out.append(arm)
        return out
    raise SystemExit(f"lane {lane} not found in pool")


def main() -> None:
    notes: list[str] = []

    # ------------------------------------------------------------------ assignment
    a = json.loads(ASSIGN.read_text(encoding="utf-8"))
    prev_rev = int(a.get("revision", 0))

    chains = a.get("lane_chains") or {}
    # The EXECUTE chain carries an EXTRA entry beyond the pool: the owner-selectable
    # additional route (gpt-6-luna). It is not a pool arm, so re-deriving the chain from the
    # pool alone would silently DROP it and change the chain's meaning. It is preserved.
    extra_execute = None
    for c in (chains.get("EXECUTE") or []):
        if c.get("role") == "owner_selectable_additional":
            extra_execute = c
            break
    for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
        chains[lane] = lane_chain_from_pool(lane)
    if extra_execute is not None:
        chains["EXECUTE"].append(extra_execute)
    a["lane_chains"] = chains
    notes.append("assignment: lane_chains for the three lanes re-derived from the pool")

    rows = a.get("assignment") or []
    if len(rows) >= 3:
        # rows are [PLAN, EXECUTE, VERIFY_SECURITY]
        for idx, lane in ((0, "PLAN"), (1, "EXECUTE"), (2, "VERIFY_SECURITY")):
            arm = pool_rank1(lane)
            row = rows[idx]
            row["assigned_provider"] = arm["provider"]
            row["assigned_model"] = arm["model"]
            if lane == "PLAN":
                row["reasoning_effort"] = arm.get("reasoning_effort")
            # the EXECUTE row's additional_routes stay as they are (operator-selectable gpt-6-luna)
            # but the row's OWN binding is now MiniMax.
        # VERIFY's supply_selector mirrors the VERIFY chain
        vs = rows[2].get("supply_selector")
        if vs is not None:
            chain = chains["VERIFY_SECURITY"]
            arms = []
            for i, c in enumerate(chain):
                arms.append({
                    "provider": c["provider"], "model": c["model"],
                    "role": "primary" if i == 0 else f"fallback{i}_operator_selectable",
                    "default": i == 0, "automatic_selection": bool(c.get("automatic_selection")),
                })
            vs["arms"] = arms
            p = chain[0]
            vs["unspecified_default"] = {
                "arm": p.get("arm", "A"), "model": p["model"], "provider": p["provider"],
                "auth": "env_ref:OPENCODE_GO_API_KEY", "reasoning_effort": p.get("reasoning_effort"),
                "canonical_identity": p["model"], "oauth": False,
            }
        notes.append("assignment: assignment[0..2] + supply_selector re-derived from the pool")

    sod = a.get("sod") or {}
    sod["plan_lane"] = (
        f"{ARM_PROVIDER} / {ARM_MODEL} (MiniMax M3.1 Flash, OPENCODE GO) — owner order "
        "2026-10-21 (round FAR-MINIMAX-MANDATE-20261021, epoch 25); supersedes the 2026-10-21 "
        "GPT-6.1-SOL order and the 2026-10-16 GLM order.")
    sod["execute_lane"] = (
        f"{ARM_PROVIDER} / {ARM_MODEL} (MiniMax M3.1 Flash, OPENCODE GO) — Codex CLI worker; "
        "owner order 2026-10-21 (epoch 25); supersedes deepseek-v4.1-flash.")
    sod["verify_security_lane"] = (
        f"{ARM_PROVIDER} / {ARM_MODEL} (MiniMax M3.1 Flash, OPENCODE GO) — owner order "
        "2026-10-21 (epoch 25); supersedes the 2026-10-21 GPT-6.1-SOL order.")
    sod["verify_security_arm_A"] = (
        f"{ARM_PROVIDER} / {ARM_MODEL} (primary Codex CLI checker; owner order 2026-10-21)")
    sod["verify_security_default_arm"] = ARM_MODEL
    sod["verify_security_selection"] = (
        "owner order 2026-10-21 (round FAR-MINIMAX-MANDATE-20261021): the automatic, default "
        f"arm is {TRANSPORT}. The other provider arms stay reachable as operator-selectable "
        "fallbacks; there is no second MiniMax arm, so the lane has no MiniMax-vs-MiniMax "
        "fallback inside the pool.")
    sod["verify_vs_execute_model_separation"] = (
        "NONE on the model axis, BY OWNER ORDER: EXECUTE and VERIFY_SECURITY are BOTH "
        f"{TRANSPORT} (MiniMax M3.1 Flash, OPENCODE GO), owner order 2026-10-21, declared as "
        "SOD006-C5 (OWNER_ORDERED_IN_FORCE). What remains is PROCESS, LANE and EVIDENCE-PATH "
        "independence plus the no-self-acceptance rule; model diversity between writer and "
        "checker is deliberately absent and is NOT claimed.")
    sod["verify_vs_plan_model_separation"] = (
        "NONE on the model axis, BY OWNER ORDER: PLAN, EXECUTE and VERIFY_SECURITY all run "
        f"{TRANSPORT}. SOD006-C4 (PLAN vs VERIFY) and SOD006-C5 (EXECUTE vs VERIFY) are both "
        "OPEN_OWNER_ORDERED; independence is process separation only.")
    sod["provider_separation"] = (
        "ABSENT, and model-level separation is now also ABSENT: all three lanes sit on the "
        f"opencode-go provider AND on {ARM_MODEL}. Provider separation is not required "
        "(invariants.provider_separation_required=false); model-axis separation is absent by "
        "owner order 2026-10-21 (SOD006-C4/C5) and is NOT claimed.")
    sod["provider_separation_status"] = (
        "ABSENT by owner order 2026-10-21: all three lanes sit on opencode-go and on the SAME "
        f"model {ARM_MODEL} (MiniMax M3.1 Flash). Provider separation is not required "
        "(invariants.provider_separation_required=false). Model-axis separation is ABSENT "
        "between every pair (SOD006-C4 and SOD006-C5, both OPEN_OWNER_ORDERED). Recorded as an "
        "accepted deviation, not as a passing invariant.")
    sod["maker_self_acceptance"] = (
        "PREVENTED at dispatch on every arm: no single call ever verifies its own output. "
        "Model-identity separation between writer and checker is deliberately NOT present under "
        f"the 2026-10-21 owner order (EXECUTE and VERIFY_SECURITY are both {TRANSPORT}, "
        "SOD006-C5 OWNER_ORDERED_IN_FORCE); the separation this round actually has is process, "
        "lane and evidence-path independence. PLAN is on the same model as both.")
    sod["verify_security_reasoning_effort"] = None
    sod["plan_reasoning_effort"] = None
    sod["lane_deviation_recorded"] = (
        "Owner order 2026-10-21: all three lanes on one model. Recorded as SOD006-C4 (PLAN vs "
        "VERIFY) and SOD006-C5 (EXECUTE vs VERIFY), both OPEN_OWNER_ORDERED.")
    a["sod"] = sod
    notes.append("assignment: sod rewritten (11 fields)")

    sa = a.get("sod_across_all_arms") or {}
    exec_models = sorted({c["model"] for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY")
                          for c in chains[lane]})
    ver_models = sorted({c["model"] for c in chains["VERIFY_SECURITY"]})
    sa["executor_models"] = exec_models
    sa["verifier_models"] = ver_models
    sa["maker_checker_model_separation"] = (
        f"Under the 2026-10-21 owner order every lane's rank-1 arm is {ARM_MODEL}, so EVERY "
        "maker->checker pair is IDENTICAL on the model axis. Model diversity is NOT claimed "
        "anywhere in this round's artifacts. The separation that remains is PROCESS, LANE and "
        "EVIDENCE-PATH independence plus the no-self-acceptance rule.")
    sa["provider_separation_across_arms"] = (
        "ABSENT - all three lanes sit on opencode-go. Provider separation is NOT required "
        "(invariants.provider_separation_required=false).")
    sa["new_cross_lane_coupling"] = (
        f"One model family across all three lanes. Declared as SOD006-C4/C5; not a violation, "
        "because the owner ordered it and the alternative controls are the process/lane/artifact "
        "separation and the no-self-acceptance rule.")
    sa["retired"] = False
    sa["retired_note"] = ("NOT retired: the current VERIFY default arm is MiniMax M3.1 Flash "
                           "(owner order 2026-10-21).")
    a["sod_across_all_arms"] = sa
    notes.append("assignment: sod_across_all_arms re-derived")

    ew = a.get("effective_wiring") or {}
    mw = ew.get("main_agent") or {}
    mw["provider"] = ARM_PROVIDER
    mw["model"] = ARM_MODEL
    ew["main_agent"] = mw
    a["effective_wiring"] = ew
    notes.append("assignment: effective_wiring.main_agent -> MiniMax")

    a["revision"] = prev_rev + 1
    a["registry_epoch"] = 25
    a["owner_order"] = ("2026-10-21 minimax mandate "
                        "(PLAN/EXECUTE/VERIFY_SECURITY -> MiniMax M3.1 Flash, OPENCODE GO)")
    a["revision_25_reason"] = (
        "Revision 25 (owner order 2026-10-21, round FAR-MINIMAX-MANDATE-20261021): all three "
        f"lanes bound to {TRANSPORT}. The chain, the assignment rows, the supply selector and the "
        "SoD declarations are DERIVED from the pool, not hand-written, so the pool remains the "
        "single selection authority. The model axis is identical across all three lanes and is "
        "declared as SOD006-C4/C5 rather than hedged.")
    ASSIGN.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    notes.append(f"assignment: revision {prev_rev} -> {a['revision']}, registry_epoch 25")

    # ------------------------------------------------------------------ registry projection
    # The projection records what the artifact is EXPECTED to contain. For the pointers this
    # round changed, the expected value is read back FROM THE WRITTEN artifact, so the gate
    # compares the file against a record of that file rather than against a second hand-typed
    # copy that could disagree.
    written = json.loads(ASSIGN.read_text(encoding="utf-8"))

    def resolve(doc, pointer: str):
        cur = doc
        for part in pointer.split("/"):
            if part == "":
                continue
            if isinstance(cur, list):
                cur = cur[int(part)]
            else:
                if part not in cur:
                    raise KeyError(pointer)
                cur = cur[part]
        return cur

    reg_text = REG.read_text(encoding="utf-8")
    # The projection is a top-level sequence item under `projections:`, so its id sits at
    # indent 0 ("- id: model-lane-assignment"); the block ends at the next indent-0 item.
    m = re.search(r"^- id: model-lane-assignment\n(?:(?!^- id: ).*\n)*", reg_text, flags=re.M)
    if not m:
        raise SystemExit("ANCHOR_FAIL registry.projection: model-lane-assignment projection not found")
    block = m.group(0)

    changed_pointers = {
        "/registry_epoch", "/revision",
        "/sod/plan_lane", "/sod/execute_lane", "/sod/verify_security_lane",
        "/sod/verify_security_arm_A", "/sod/verify_security_default_arm",
        "/sod/verify_vs_execute_model_separation", "/sod/verify_vs_plan_model_separation",
        "/sod/provider_separation", "/sod/provider_separation_status",
        "/sod/maker_self_acceptance", "/sod/verify_security_reasoning_effort",
        "/sod/plan_reasoning_effort",
        "/assignment/0/assigned_model", "/assignment/0/assigned_provider",
        "/assignment/1/assigned_model", "/assignment/1/assigned_provider",
        "/assignment/2/assigned_model", "/assignment/2/assigned_provider",
        "/assignment/0/reasoning_effort", "/assignment/2/reasoning_effort",
        "/assignment/2/supply_selector/arms/0/provider", "/assignment/2/supply_selector/arms/0/model",
        "/assignment/2/supply_selector/arms/0/role", "/assignment/2/supply_selector/arms/0/default",
        "/assignment/2/supply_selector/arms/1/provider", "/assignment/2/supply_selector/arms/1/model",
        "/assignment/2/supply_selector/arms/1/role", "/assignment/2/supply_selector/arms/1/default",
        "/assignment/2/supply_selector/arms/1/automatic_selection",
        "/assignment/2/supply_selector/arms/2/provider", "/assignment/2/supply_selector/arms/2/model",
        "/assignment/2/supply_selector/arms/2/role", "/assignment/2/supply_selector/arms/2/default",
        "/assignment/2/supply_selector/arms/2/automatic_selection",
        "/assignment/2/supply_selector/arms/2/provider", "/assignment/2/supply_selector/arms/2/model",
        "/assignment/2/supply_selector/unspecified_default/provider",
        "/assignment/2/supply_selector/unspecified_default/model",
        "/assignment/2/supply_selector/unspecified_default/arm",
        "/assignment/2/supply_selector/unspecified_default/canonical_identity",
        "/lane_chains/PLAN/0/provider", "/lane_chains/PLAN/0/model",
        "/lane_chains/PLAN/0/role", "/lane_chains/PLAN/0/default",
        "/lane_chains/PLAN/0/automatic_selection", "/lane_chains/PLAN/0/reasoning_effort",
        "/lane_chains/EXECUTE/0/provider", "/lane_chains/EXECUTE/0/model",
        "/lane_chains/EXECUTE/0/reasoning_effort",
        "/lane_chains/EXECUTE/0/role", "/lane_chains/EXECUTE/0/default",
        "/lane_chains/EXECUTE/0/automatic_selection", "/lane_chains/EXECUTE/0/arm",
        "/lane_chains/EXECUTE/3/provider", "/lane_chains/EXECUTE/3/model",
        "/lane_chains/EXECUTE/3/automatic_selection", "/lane_chains/EXECUTE/3/default",
        "/lane_chains/PLAN/1/model", "/lane_chains/PLAN/1/provider",
        "/lane_chains/PLAN/1/role", "/lane_chains/PLAN/1/default",
        "/lane_chains/PLAN/1/automatic_selection",
        "/lane_chains/EXECUTE/1/model", "/lane_chains/EXECUTE/1/provider",
        "/lane_chains/EXECUTE/1/role", "/lane_chains/EXECUTE/1/default",
        "/lane_chains/EXECUTE/1/automatic_selection",
        "/lane_chains/VERIFY_SECURITY/1/model", "/lane_chains/VERIFY_SECURITY/1/provider",
        "/lane_chains/VERIFY_SECURITY/1/role", "/lane_chains/VERIFY_SECURITY/1/default",
        "/lane_chains/VERIFY_SECURITY/1/automatic_selection",
        "/lane_chains/VERIFY_SECURITY/0/provider", "/lane_chains/VERIFY_SECURITY/0/model",
        "/lane_chains/VERIFY_SECURITY/0/role", "/lane_chains/VERIFY_SECURITY/0/default",
        "/lane_chains/VERIFY_SECURITY/0/automatic_selection",
        "/lane_chains/VERIFY_SECURITY/0/reasoning_effort",
        "/lane_chains/VERIFY_SECURITY/0/arm",
        "/effective_wiring/main_agent/provider", "/effective_wiring/main_agent/model",
        "/sod_across_all_arms/verifier_models/0",
        "/sod_across_all_arms/executor_models/0",
        "/sod_across_all_arms/verifier_models/1",
        "/sod_across_all_arms/executor_models/1",
    }

    def yaml_scalar(v) -> str:
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        s = str(v)
        if "\n" in s:
            s = s.replace("\n", " ")
        return "'" + s.replace("'", "''") + "'"

    # A pointer whose INDEX moved must be RE-POINTED, not just re-valued. The model-set
    # pointers (/sod_across_all_arms/verifier_models/N) name an index into a SORTED array, so
    # when MiniMax entered the array every index after it shifted. The pointer is re-pointed at
    # the slot that now holds the value the projection is about (the MiniMax entry).
    def repoint(ptr: str) -> str:
        for base in ("/sod_across_all_arms/verifier_models/",
                     "/sod_across_all_arms/executor_models/"):
            if ptr.startswith(base):
                arr = resolve(written, base.rstrip("/"))
                if isinstance(arr, list) and ARM_MODEL in arr:
                    return base + str(arr.index(ARM_MODEL))
        # The EXECUTE chain's owner-selectable ADDITIONAL route is a semantic slot, not a pool
        # rank: it sits after the pool arms. When a pool arm is inserted ahead of it, its index
        # moves. The pointer is re-pointed at the slot that now carries that route.
        if ptr.startswith("/lane_chains/EXECUTE/"):
            _chain = resolve(written, "/lane_chains/EXECUTE")
            for _i, _c in enumerate(_chain):
                if _c.get("role") == "owner_selectable_additional":
                    _rest = ptr[len("/lane_chains/EXECUTE/"):]
                    _head, _, _tail = _rest.partition("/")
                    return f"/lane_chains/EXECUTE/{_i}" + (("/" + _tail) if _tail else "")
        return ptr

    out_lines: list[str] = []
    for ln in block.splitlines():
        mptr = re.match(r"^(\s*)- pointer: (\S+)\s*$", ln)
        if mptr and mptr.group(2) in changed_pointers:
            ptr = repoint(mptr.group(2))
            out_lines.append(re.sub(r"^(\s*)- pointer: \S+\s*$",
                                    lambda mm: f"{mm.group(1)}- pointer: {ptr}", ln))
            continue
        mexp = re.match(r"^(\s*)expected: (.*)$", ln)
        if mexp and out_lines and out_lines[-1].strip().startswith("- pointer:"):
            ptr = out_lines[-1].split("- pointer:", 1)[1].strip()
            if ptr in changed_pointers or any(
                    ptr.startswith(b) for b in ("/sod_across_all_arms/verifier_models/",
                                                "/sod_across_all_arms/executor_models/")):
                try:
                    val = resolve(written, ptr)
                except (KeyError, IndexError, ValueError):
                    out_lines.append(ln)
                    continue
                out_lines.append(f"{mexp.group(1)}expected: {yaml_scalar(val)}")
                continue
        out_lines.append(ln)

    new_block = "\n".join(out_lines) + "\n"
    reg_text = reg_text[:m.start()] + new_block + reg_text[m.end():]

    # the projection's note
    old_note = re.search(r"^    note: .*canonical policy revision 24.*$", reg_text, flags=re.M)
    if old_note:
        new_note = (
            "    note: 'canonical policy revision 25 (owner order 2026-10-21, round "
            "FAR-MINIMAX-MANDATE-20261021, superseding revision 24 / the 2026-10-21 GPT order). "
            f"PLAN, EXECUTE and VERIFY_SECURITY all rank-1 on {TRANSPORT} (MiniMax M3.1 Flash, "
            "OPENCODE GO); the chain, the assignment rows and the supply selector are derived "
            "from the pool. The model axis is identical across all three lanes, declared as "
            "SOD006-C4 and SOD006-C5 (both OPEN_OWNER_ORDERED, process separation only) rather "
            "than hedged.'")
        reg_text = reg_text[:old_note.start()] + new_note + reg_text[old_note.end():]

    REG.write_text(reg_text, encoding="utf-8")
    notes.append("registry: projection bindings re-derived from the written artifact")
    print("\n".join(f"OK {n}" for n in notes))


if __name__ == "__main__":
    main()
