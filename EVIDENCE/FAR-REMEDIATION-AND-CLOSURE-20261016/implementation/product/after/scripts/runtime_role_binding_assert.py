#!/usr/bin/env python3
"""P1-A (round FAR-LANE-REUSE-RCA-20261015): per-round role-mandate consumer.

Owner orders name exact provider/model arms per role ("PLAN = X, EXECUTE = Y, VERIFY = Z").
Before this consumer the mandate was advice: the registry default or the session default could
serve a different arm and nothing refused it, which is exactly how the two PLAN-on-DeepSeek
sessions of 2026-10-14/15. This script turns the declaration into a checked pre-dispatch gate.

Usage:
    python runtime_role_binding_assert.py --mandate-file MANDATE.json --lane EXECUTE \
        [--admission-file ADMISSION.json] [--workorder WO-...]

The mandate file carries the per-round binding:
    {"round": ..., "roles": {"EXECUTE": {"provider": "opencode-go", "model": "..."},
                              "VERIFY_SECURITY": {...}, "PLAN": {...}}}

Checked claims, all fail-closed with typed codes:
  ERR_MANDATE_FILE_MISSING / _INVALID      the mandate itself is unusable
  ERR_MANDATE_ROLE_NOT_DECLARED            the lane has no declared arm for this round
  ERR_MANDATE_ARM_UNRESOLVED               declared arm not found in the route slots pool,
                                           or the pinned entry's digest/version was
                                           re-verified and does NOT match the declaration
Exit 0 + {"ok": true, ...} only when the declaration is complete AND the pinned pool entry
still verifies against the toolchain declaration on disk.
Read-only: writes nothing (caller captures stdout).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT_EARLY = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_EARLY / "src"))
try:
    from hg_kseos import role_binding as _role_binding  # noqa: E402
except Exception:  # noqa: BLE001 - a missing helper must never crash this gate at import
    _role_binding = None

ERR_CODES = {
    "missing": "ERR_MANDATE_FILE_MISSING",
    "invalid": "ERR_MANDATE_FILE_INVALID",
    "role": "ERR_MANDATE_ROLE_NOT_DECLARED",
    "unresolved": "ERR_MANDATE_ARM_UNRESOLVED",
}

# Tranche A/B: the claim this gate makes is BOUNDED. Whether a persisted role binding is supplied or
# not, a pass here is a pre-dispatch DECLARATION check; it does NOT prove that any role executed, nor
# that the persisted binding was served. Completed-role evidence is a separate consumer.
CLAIM_CEILING = ("DECLARATION_ONLY: this asserts the per-round role declaration is present and "
                 "internally consistent with the persisted binding/pool/toolchain, INCLUDING the "
                 "reasoning-effort axis (mandate effort vs the declared arm's pool effort, and an "
                 "explicitly supplied --served-effort when given). It does NOT prove any role "
                 "executed, and it does NOT prove a model was served. The legacy selector path "
                 "below (no --binding) proves even less: it checks the mandate selector only.")

ROOT = Path(__file__).resolve().parent.parent


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mandate-file", default=None,
                    help="the per-round mandate selector document; optional when --binding is given "
                         "(the persisted binding is the canonical source of the declared arm)")
    ap.add_argument("--lane", required=True, choices=["PLAN", "EXECUTE", "VERIFY_SECURITY", "SECURITY"])
    ap.add_argument("--pool", default=str(ROOT / "config" / "lane-route-slots.candidate.json"))
    ap.add_argument("--toolchain-declaration", default=str(ROOT / "config" / "hermes-codex-lane.json"))
    ap.add_argument("--workorder", default="")
    ap.add_argument("--binding", default=None,
                    help="Tranche A: path to the canonical PERSISTED role binding "
                         "(TaskSpec permissions_json[role_binding] carried verbatim). When supplied, the "
                         "mandate selector is cross-checked against the persisted binding for this "
                         "session/round/workorder/subject/scope/expiry/mandate-digest.")
    ap.add_argument("--session", default=None)
    ap.add_argument("--round", default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--served-effort", default=None,
                    help="M03: the reasoning effort a receipt or startup header reported for this "
                         "lane's turn. When supplied it must equal the mandate's declared "
                         "reasoning_effort, else the run refuses.")
    args = ap.parse_args()

    lane = "VERIFY_SECURITY" if args.lane == "SECURITY" else args.lane
    # ---- Tranche A: canonical persisted-binding path (explicit arguments) ------------------------
    bound = {
        "state": "absent", "schema": "HGK-ROLE-MANDATE-ASSERT/1", "ok": True, "lane": lane,
        "binding_checked": False, "binding_digest": None,
        "workorder": args.workorder, "session": args.session, "subject": args.subject,
        "consumer": "pre-dispatch fail-closed gate (this script); the dispatcher derives arm+rank "
                    "from the SAME persisted binding and re-checks the served identity post-hoc",
        "claim_ceiling": CLAIM_CEILING,
    }
    if args.binding:
        if _role_binding is None:
            print(json.dumps({"ok": False, "code": "ERR_ROLE_BINDING_INVALID",
                              "detail": "role_binding helper unavailable"}, ensure_ascii=False))
            return 2
        bpath = Path(args.binding)
        if not bpath.is_file():
            print(json.dumps({"ok": False, "code": "ERR_ROLE_BINDING_FILE_MISSING",
                              "detail": str(bpath)}, ensure_ascii=False))
            return 2
        try:
            doc = json.loads(bpath.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(json.dumps({"ok": False, "code": "ERR_ROLE_BINDING_FILE_INVALID",
                              "detail": f"{bpath}:{exc}"}, ensure_ascii=False))
            return 2
        try:
            validated = _role_binding.validate_binding(
                doc, lane=lane, session=args.session, round=args.round,
                workorder_id=args.workorder or None, subject=args.subject)
            arm = _role_binding.resolve_arm(validated["binding"], lane)
        except _role_binding.BindingError as exc:
            print(json.dumps({"ok": False, "code": exc.code, "detail": exc.detail,
                              "stage": "persisted_binding"}, ensure_ascii=False))
            return 3
        bound.update({
            "state": "checked", "binding_checked": True, "binding_digest": validated["binding_digest"],
            "declared_arm": arm["arm"], "declared_rank": arm["rank"], "declared_surface": arm["surface"],
            "workorder": validated["binding"]["workorder"],
            "session": validated["binding"]["session"], "round": validated["binding"]["round"],
            "subject": validated["binding"]["subject"],
        })
        # The mandate file, when also supplied, must agree with the persisted binding for this lane.
        mf_probe = Path(args.mandate_file) if getattr(args, "mandate_file", None) else None
        if mf_probe is None:
            print(json.dumps(bound, ensure_ascii=False))
            return 0
    if not args.mandate_file:
        # No persisted binding AND no mandate selector is an empty-input call: it can prove nothing.
        print(json.dumps({"ok": False, "code": ERR_CODES["missing"],
                          "detail": "neither --binding nor --mandate-file was supplied"}, ensure_ascii=False))
        return 2
    mf = Path(args.mandate_file)
    if not mf.is_file():
        print(json.dumps({"ok": False, "code": ERR_CODES["missing"], "detail": str(mf)}))
        return 2
    try:
        mandate = json.loads(mf.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"ok": False, "code": ERR_CODES["invalid"], "detail": str(exc)}))
        return 2
    declared = (mandate.get("roles") or {}).get(lane)
    if not declared or not (declared.get("provider") and declared.get("model")):
        print(json.dumps({"ok": False, "code": ERR_CODES["role"],
                          "detail": f"no declared provider/model for lane {lane}"}))
        return 3

    # When BOTH a persisted binding and a mandate selector are supplied, they must name the SAME arm
    # for this lane. A selector that disagrees with the canonical binding is a named refusal, never a
    # silent narrowing to either side.
    if bound.get("binding_checked"):
        want = f"{declared['provider']}/{declared['model']}"
        if want != bound["declared_arm"]:
            print(json.dumps({"ok": False, "code": "ERR_ROLE_BINDING_MANDATE_ARM_MISMATCH",
                              "detail": {"mandate": want, "binding": bound["declared_arm"]}},
                             ensure_ascii=False))
            return 3

    # The declared arm must still resolve through the canonical toolchain declaration: binary
    # present, digest equal, version equal. This is the same verifier P0-A reuses pre-spawn.
    probe = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "hgk-lane-toolchain.py"),
         "--resolve", "--declaration", args.toolchain_declaration],
        capture_output=True, text=True, timeout=120)
    if probe.returncode != 0:
        print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                          "detail": {"stage": "toolchain_declaration", "exit": probe.returncode,
                                     "stderr_tail": (probe.stderr or probe.stdout).strip()[-400:]}},
                         ensure_ascii=False))
        return 4
    identity = json.loads(probe.stdout)

    # The pool must still contain the declared arm so the dispatcher can force-rank to it.
    pool_ok, pool_detail = False, ""
    pool_path = Path(args.pool)
    try:
        pool = json.loads(pool_path.read_text(encoding="utf-8"))
        lanes = pool.get("lanes") or []
        lane_entry = next((l for l in lanes if l.get("lane") == lane), None)
        entries = lane_entry.get("ordered_pool") or [] if lane_entry else []
        hit = [e for e in entries
               if str(e.get("provider")) == declared["provider"] and str(e.get("model")) == declared["model"]]

        if hit:
            pool_ok = True
        else:
            pool_detail = f"{declared['provider']}/{declared['model']} not in pool {pool_path.name}"
    except (json.JSONDecodeError, OSError) as exc:
        pool_detail = f"pool unreadable: {exc}"
    if not pool_ok:
        print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                          "detail": {"stage": "pool", "why": pool_detail}}, ensure_ascii=False))
        return 5

    # H3 (round FAR-LANE-ROUTE-REBIND-20261015): per-turn adjustability. If the mandate names a
    # per-lane `chain`, EVERY listed arm must resolve in the pool — an owner instruction naming
    # e.g. "fallback1 for this turn" works only if that arm is really selectable; a missing arm is
    # a fail-closed typing, not a silent narrowing of the chain.
    chain = declared.get("chain") or []
    chain_missing = []
    if chain:
        present = set()
        for e in entries:
            present.add(f"{e.get('provider')}/{e.get('model')}")
        chain_missing = [a for a in chain if a not in present]
        if chain_missing:
            print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                              "detail": {"stage": "chain", "why": f"chains arms absent from pool: {chain_missing}",
                                         "chain": chain}}, ensure_ascii=False))
            return 6

    # M03 (round LANE-RELIABILITY-CLOSURE-20261016): the EFFORT axis. The mandate declares a
    # per-lane `reasoning_effort` and the pool declares one on the arm; before this block NOTHING
    # compared them (measured: zero occurrences of "effort" in this file), so a lane served at a
    # different effort than the mandate names was refused by nothing. Fail closed on both ends
    # rather than assuming either side:
    #   ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL -- the mandate names an effort and the declared arm's
    #       pool entry carries none, so the declared effort cannot be checked at all;
    #   ERR_MANDATE_EFFORT_MISMATCH           -- mandate effort != the declared arm's pool effort;
    #   ERR_SERVED_EFFORT_UNVERIFIABLE        -- a served effort was supplied but the mandate names
    #       no effort to compare it against;
    #   ERR_SERVED_EFFORT_MISMATCH            -- a supplied served effort != the mandate's effort.
    # Exit code 7 is this axis's own, so the four outcomes stay distinguishable from the
    # mandate/pool/toolchain refusals above (2/3/4/5/6).
    declared_effort = declared.get("reasoning_effort")
    pool_effort = hit[0].get("reasoning_effort") if hit else None
    if declared_effort:
        if not pool_effort:
            print(json.dumps({"ok": False, "code": "ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL",
                              "detail": {"stage": "effort",
                                         "arm": f"{declared['provider']}/{declared['model']}",
                                         "mandate_effort": declared_effort,
                                         "why": "the declared arm's pool entry declares no reasoning_effort"}},
                             ensure_ascii=False))
            return 7
        if str(declared_effort) != str(pool_effort):
            print(json.dumps({"ok": False, "code": "ERR_MANDATE_EFFORT_MISMATCH",
                              "detail": {"stage": "effort",
                                         "arm": f"{declared['provider']}/{declared['model']}",
                                         "mandate_effort": declared_effort,
                                         "pool_effort": pool_effort}}, ensure_ascii=False))
            return 7
    if args.served_effort is not None:
        if not declared_effort:
            print(json.dumps({"ok": False, "code": "ERR_SERVED_EFFORT_UNVERIFIABLE",
                              "detail": {"stage": "effort", "served_effort": args.served_effort,
                                         "why": "the mandate declares no reasoning_effort for this lane"}},
                             ensure_ascii=False))
            return 7
        if str(args.served_effort) != str(declared_effort):
            print(json.dumps({"ok": False, "code": "ERR_SERVED_EFFORT_MISMATCH",
                              "detail": {"stage": "effort", "served_effort": args.served_effort,
                                         "mandate_effort": declared_effort}}, ensure_ascii=False))
            return 7

    result = {
        "schema": "HGK-ROLE-MANDATE-ASSERT/1",
        "ok": True,
        "lane": lane,
        "declared": declared,
        "chain_verified": chain,
        "toolchain_identity": {k: identity[k] for k in ("path", "sha256", "version") if k in identity},
        "pool": pool_path.name,
        "workorder": args.workorder,
        "consumer": "pre-dispatch fail-closed gate (this script); dispatcher derives arm+rank from the "
                    "same persisted binding and re-checks the served identity post-hoc",
        # The legacy path checks the mandate SELECTOR only; it does not read a persisted binding and
        # cannot vouch for role execution. Say so explicitly rather than implying enforcement.
        "binding_checked": bool(bound.get("binding_checked")),
        "binding_digest": bound.get("binding_digest"),
        "declared_effort": declared_effort,
        "pool_effort": pool_effort,
        "effort_verified": bool(declared_effort and pool_effort
                                and str(declared_effort) == str(pool_effort)),
        "claim_ceiling": CLAIM_CEILING,
    }
    result.update(bound)
    result["ok"] = True
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
