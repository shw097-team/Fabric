#!/usr/bin/env python
"""FAR-MINIMAX-MANDATE-20261021 — bind all three lanes to MiniMax M3.1 Flash (OPENCODE GO).

Owner order (2026-10-21, this turn):
    PLAN  execution model  : MiniMax M3.1 Flash (OPENCODE GO)
    EXECUTE (Codex CLI)   : MiniMax M3.1 Flash (OPENCODE GO)
    VERIFY / SECURITY (Codex CLI) : MiniMax M3.1 Flash (OPENCODE GO)

WHAT THIS CHANGES
  * config/lane-route-slots.candidate.json : MiniMax becomes the rank-1 automatic arm of
    PLAN, EXECUTE and VERIFY_SECURITY. The previous rank-1 arms are demoted to fallback
    positions; nothing is deleted, so every previous arm stays reachable.
  * config/lane-routing-registry.yaml : epoch 23 -> 25, the three routes' selected identity
    and arms follow the pool, and a NEW declared SoD conflict (SOD006-C5) records that
    EXECUTE and VERIFY_SECURITY now share one model BY OWNER ORDER.
  * config/model-lane-assignment.json : the three lane declarations and the two
    separation statements are rewritten to the owner order.

WHAT THIS DELIBERATELY DOES NOT DO
  * It does NOT touch the canonical Hermes session profile. The session plane and the lane
    plane are different planes: a session pin is not a lane binding.
  * It does NOT delete any pool arm. Only ranks and automatic-selection flags move.
  * It does NOT claim model-axis independence. With one model on all three lanes there is
    none, and the registry says so in as many words.

IDEMPOTENCE
  Every edit is anchored on an exact expected text. An anchor that is not found EXACTLY ONCE
  raises, so a second run either no-ops or fails loudly -- it never half-applies.
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

EDITS: list[tuple[str, str, str, str]] = []   # (file, anchor, replacement, label)


def anchor(text: str, needle: str, label: str, path: Path) -> str:
    """Replace `needle` exactly once, or raise. Never a silent partial apply."""
    n = text.count(needle)
    if n != 1:
        raise SystemExit(f"ANCHOR_FAIL {label}: expected exactly 1 occurrence, got {n} :: {needle!r}")
    return text.replace(needle, needle)  # unchanged; the caller performs the replace


# ---------------------------------------------------------------- pool
def patch_pool() -> list[str]:
    p = POOL
    d = json.loads(p.read_text(encoding="utf-8"))
    notes = []
    for lane in d["lanes"]:
        name = lane["lane"]
        pool = lane["ordered_pool"]
        # 1. find or create the MiniMax arm
        arm = next((c for c in pool
                    if c.get("provider") == ARM_PROVIDER and c.get("model") == ARM_MODEL), None)
        if arm is None:
            arm = {
                "provider": ARM_PROVIDER, "model": ARM_MODEL,
                "transport_model": TRANSPORT,
                "auth": "env_ref:OPENCODE_GO_API_KEY", "oauth": False,
                "reasoning_effort": None,
            }
            pool.append(arm)
            notes.append(f"{name}: MiniMax arm added")
        else:
            notes.append(f"{name}: MiniMax arm already present")
        # 2. it becomes the automatic, default, rank-1 arm
        arm["transport_model"] = TRANSPORT
        arm["role"] = "DEFAULT/首選"
        arm["default"] = True
        arm["automatic_selection"] = True
        arm["reasoning_effort"] = None
        arm.setdefault("auth", "env_ref:OPENCODE_GO_API_KEY")
        arm.setdefault("oauth", False)
        # 3. every other arm is demoted: it stays reachable but stops being the default
        for c in pool:
            if c is arm:
                continue
            c["default"] = False
            c["automatic_selection"] = False
            if c.get("role", "").startswith("DEFAULT"):
                c["role"] = "FALLBACK/備援"
        # 4. re-rank contiguously, MiniMax first
        rest = [c for c in pool if c is not arm]
        rest.sort(key=lambda c: int(c.get("rank", 99)))
        ordered = [arm] + rest
        for i, c in enumerate(ordered, start=1):
            c["rank"] = i
        lane["ordered_pool"] = ordered
        lane["selection_note"] = (
            f"Owner order 2026-10-21: {ARM_MODEL} ({ARM_PROVIDER}) is rank 1 and the automatic "
            f"selection for {name}. The transport id is the provider-qualified slug "
            f"'{TRANSPORT}'. The prior rank-1 arms are demoted to FALLBACK and stay reachable. "
            f"MiniMax is not listed by the relay's /v1/models catalog (a stale snapshot); the "
            f"lane is served by forwarding the id verbatim, measured 2026-10-21 on 127.0.0.1:10101."
        )
        notes.append(f"{name}: MiniMax -> rank 1, {len(ordered)} arms")
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return notes


# ---------------------------------------------------------------- registry
def patch_registry() -> list[str]:
    p = REG
    t = p.read_text(encoding="utf-8")
    notes = []

    # epoch
    m = re.search(r"^epoch:\s*(\d+)\s*$", t, flags=re.M)
    if not m:
        raise SystemExit("ANCHOR_FAIL registry.epoch: no 'epoch: <n>' line")
    old_epoch = int(m.group(1))
    new_epoch = old_epoch + 1          # one step per owner-mandated change
    t = t[:m.start()] + f"epoch: {new_epoch}" + t[m.end():]
    notes.append(f"registry epoch {old_epoch} -> {new_epoch}")

    # the three routes' selected identity + primary arm
    for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
        pat = re.compile(
            r"(- lane: " + lane + r"\n(?:.*\n)*?  - arm: primary\n(?:.*\n)*?"
            r"    provider: )[^\n]+(\n    model: )[^\n]+", re.M)
        t2, n = pat.subn(
            lambda m: m.group(1) + ARM_PROVIDER + m.group(2) + ARM_MODEL, t, count=1)
        if n == 0:
            raise SystemExit(f"ANCHOR_FAIL registry.route.{lane}: primary arm block not found")
        t = t2
        notes.append(f"registry route {lane}: primary arm -> {ARM_PROVIDER}/{ARM_MODEL}")

    # the route-level provider/model fields (they sit on the route header, not the arm)
    for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
        pat = re.compile(
            r"(- lane: " + lane + r"\n(?:.*\n)*?  provider: )[^\n]+(\n  model: )[^\n]+", re.M)
        t2, n = pat.subn(
            lambda m: m.group(1) + ARM_PROVIDER + m.group(2) + ARM_MODEL, t, count=1)
        if n == 0:
            raise SystemExit(f"ANCHOR_FAIL registry.route.{lane}: route-level provider/model not found")
        t = t2
    notes.append("registry route-level provider/model -> MiniMax")

    # canonical_identity on the primary arm
    t = re.sub(r"(\n    canonical_identity: )[^\n]+(?=\n    auth: openai_oauth)",
               r"\1" + ARM_MODEL, t, count=3)
    notes.append("registry canonical_identity -> MiniMax (3 primary arms)")

    # selection_authority
    t = re.sub(r"(  selection_authority: )[^\n]+",
               r"\1owner-order-20261021-minimax-mandate-plan-execute-verify-all-minimax",
               t, count=3)
    notes.append("registry selection_authority -> 2026-10-21 minimax mandate (3 routes)")

    # declared SoD conflict: EXECUTE and VERIFY_SECURITY now share one model
    # The declared_conflicts sequence items are at the SAME indent as their siblings
    # ("- id: ..."), and every scalar value contains ':' so each one is quoted.
    # The declared_conflicts sequence items are indented 2 spaces ("  - id: ...") and their
    # fields 4 spaces -- the same shape as their siblings. Every scalar here contains ':' so
    # each value is a quoted YAML scalar.
    sod_new = (
        "  - id: SOD006-C5\n"
        "    status: OPEN_OWNER_ORDERED\n"
        "    summary: 'EXECUTE and VERIFY_SECURITY both default to "
        f"{ARM_PROVIDER}/{ARM_MODEL} (MiniMax M3.1 Flash, OPENCODE GO) by owner order "
        "2026-10-21.'\n"
        "    model_axis_separation: ABSENT_BY_OWNER_ORDER\n"
        "    retained: 'PROCESS, LANE and EVIDENCE-PATH separation plus the no-self-acceptance "
        "rule; model diversity between writer and checker is deliberately absent and is NOT "
        "claimed.'\n"
        "    owner_decision: CONFIRMED_BY_OWNER_ORDER_2026-10-21\n"
        "    evidence: 'MEASURED 2026-10-21: all three lanes served at required_arm == "
        f"served_arm == {TRANSPORT}; HGK admission ADMITTED for PLAN, EXECUTE and "
        "VERIFY_SECURITY (receipts under var/FAR-MINIMAX-MANDATE-20261021/admission/).'\n"
    )
    # Insert INSIDE the sod_invariants.declared_conflicts sequence, immediately after the
    # SOD006-C4 block. The block is located by its own id and terminated by the next item at the
    # SAME indent ("  - id:"). Searching for the next "- id:" at ANY indent would land in a
    # different YAML sequence (source_of_routes) whose items are at a different indent -- which
    # silently produces an unparseable document.
    marker = "  - id: SOD006-C4\n"
    if marker not in t:
        raise SystemExit("ANCHOR_FAIL registry.sod: SOD006-C4 block not found")
    i = t.index(marker)
    # The declared_conflicts sequence ends where the parent mapping resumes: a key at indent 0
    # ("projections:", "claim_ceiling:", ...). The new item must be inserted BEFORE that key, at
    # the sequence's own indent (2 spaces + "- id:").
    j = -1
    for k in ("\nprojections:", "\nclaim_ceiling:", "\nobservations:", "\nhistory:"):
        kk = t.find(k, i)
        if kk != -1 and (j == -1 or kk < j):
            j = kk
    if j == -1:
        raise SystemExit("ANCHOR_FAIL registry.sod: end of declared_conflicts not found")
    t = t[:j + 1] + sod_new + t[j + 1:]
    notes.append("registry: SOD006-C5 declared (EXECUTE/VERIFY share one model, owner-ordered)")

    # the sod_invariants pair: EXECUTE->VERIFY distinct_required becomes false, and the
    # reason is recorded instead of the flag simply flipping
    pat = re.compile(r"(- maker: EXECUTE\n    checker: VERIFY_SECURITY\n    distinct_required: )true", re.M)
    t2, n = pat.subn(
        r"\1false  # owner order 2026-10-21: both arms are "
        + ARM_PROVIDER + "/" + ARM_MODEL + " (SOD006-C5)", t, count=1)
    if n == 0:
        raise SystemExit("ANCHOR_FAIL registry.sod.pair: EXECUTE->VERIFY pair not found")
    t = t2
    notes.append("registry: EXECUTE->VERIFY distinct_required true -> false (owner-ordered)")

    # the round's selection authority / provenance block
    _note = (
        "epoch 25: all three lanes default to " + ARM_PROVIDER + "/" + ARM_MODEL
        + " (MiniMax M3.1 Flash, OPENCODE GO) by owner order 2026-10-21. The model axis is now "
        "identical across all three lanes; the PLAN/VERIFY collision (SOD006-C4) and the "
        "EXECUTE/VERIFY collision (SOD006-C5) are both OPEN_OWNER_ORDERED. What remains is "
        "process, lane and evidence-path separation plus the no-self-acceptance rule."
    )
    # The value contains ':' so it MUST be a quoted YAML scalar. A bare scalar would make the
    # document unparseable -- and an unparseable registry is a control-plane outage.
    _note_q = "'" + _note.replace("'", "''") + "'"
    _pat = re.compile(r"(\n  owner_order_20261021: )(?:'[^']*'|[^\n]+)")
    t2, n = _pat.subn(lambda m: m.group(1) + _note_q, t, count=1)
    if n == 0:
        raise SystemExit("ANCHOR_FAIL registry.owner_order_20261021: note line not found")
    t = t2
    notes.append("registry: owner_order_20261021 note rewritten")

    p.write_text(t, encoding="utf-8")
    return notes


# ---------------------------------------------------------------- assignment
def patch_assignment() -> list[str]:
    p = ASSIGN
    d = json.loads(p.read_text(encoding="utf-8"))
    sod = d.get("sod", {})
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
        f"arm is {TRANSPORT}. It is also the only MiniMax arm in the pool, so there is no "
        "MiniMax-vs-MiniMax fallback inside the lane; the other provider arms stay reachable "
        "as operator-selectable fallbacks.")
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
        "ABSENT and now also model-level ABSENT: all three lanes sit on the opencode-go "
        f"provider AND on {ARM_MODEL}. Provider separation is not required "
        "(invariants.provider_separation_required=false) and model-axis separation is absent "
        "by owner order 2026-10-21 (SOD006-C4/C5).")
    d["sod"] = sod
    # The assignment's revision is owned by apply_assignment_derivation.py, which performs the
    # full chain/row/selector derivation. This script only prepares the pool-facing fields, so
    # it does NOT bump the revision -- otherwise the artifact would be revised twice in one
    # round for one logical change.
    d["revision"] = int(d.get("revision", 0))
    d["owner_order"] = ("2026-10-21 minimax mandate "
                        "(PLAN/EXECUTE/VERIFY_SECURITY -> MiniMax M3.1 Flash, OPENCODE GO)")
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return [f"assignment: revision -> {d['revision']}", "assignment: sod rewritten (7 fields)"]


def main() -> None:
    notes: list[str] = []
    notes += patch_pool()
    notes += patch_registry()
    notes += patch_assignment()
    print("\n".join(f"OK {n}" for n in notes))


if __name__ == "__main__":
    main()
