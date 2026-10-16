#!/usr/bin/env python
"""hgk-lane-route.py - call-site CLI over the production lane-route resolver.

Design split (FAR-LANE-ROUTE-SLOTS-012 wiring):
  * the resolver (src/hg_kseos/lane_route_resolver.py) owns POLICY: pool validation,
    typed refusals, rank order, override resolution;
  * the CALL SITE owns MEASUREMENT: it runs the real probe (a codex turn) per candidate
    and advances on runtime failure, exactly as the resolver specifies.

Modes
  --mode candidates   emit the ordered candidate list for a lane (no probing). Exit 0, or
                      exit 2 with a typed {"ok": false, "code": "ERR_..."} on refusal.
  --mode selfcheck    validate the pool artifact and print a digest receipt.

Every refusal is a typed code on stdout; nothing is ever guessed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hg_kseos.lane_route_resolver import LaneRouteError, load_pool, resolve  # noqa: E402

SCHEMA = "HGK-LANE-ROUTE-CANDIDATES/1"
DEFAULT_POOL = "config/lane-route-slots.candidate.json"


def _emit(payload: dict, code: int) -> int:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return code


def _entry(e) -> dict:
    return {"rank": e.rank, "role": e.role, "provider": e.provider, "model": e.model,
            "token": e.token, "transport": e.transport, "engine": e.engine}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hgk-lane-route.py")
    ap.add_argument("--lane", default=None)
    ap.add_argument("--pool", default=DEFAULT_POOL)
    ap.add_argument("--override", default=None)
    ap.add_argument("--mode", choices=("candidates", "selfcheck"), default="candidates")
    args = ap.parse_args(argv)
    if args.mode != "selfcheck" and not args.lane:
        ap.error("--lane is required unless --mode selfcheck")

    pool_path = Path(args.pool)
    if not pool_path.is_absolute():
        pool_path = Path(__file__).resolve().parents[1] / pool_path

    try:
        lanes = load_pool(pool_path)
        if args.mode == "selfcheck":
            return _emit({"schema": SCHEMA, "ok": True, "mode": "selfcheck",
                          "pool": str(pool_path),
                          "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
                          "lanes": {name: len(v) for name, v in sorted(lanes.items())}}, 0)

        if args.override is not None:
            # policy resolution (rank order, override legality, ambiguity) comes from the resolver;
            # the call site then measures that single entry - no fallback, an instruction is binding
            res = resolve(lanes, args.lane, override=args.override, probe=lambda _e: {"ok": True})
            return _emit({"schema": SCHEMA, "ok": True, "lane": res.lane, "mode": "override",
                          "candidates": [_entry(res.selected)],
                          "attempts": res.attempts}, 0)

        if args.lane not in lanes:
            raise LaneRouteError("ERR_SLOT_LANE_UNKNOWN", str(args.lane))
        entries = lanes[args.lane]
        return _emit({"schema": SCHEMA, "ok": True, "lane": args.lane, "mode": "pool",
                      "candidates": [_entry(e) for e in entries],
                      "pool": str(pool_path),
                      "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest()}, 0)
    except LaneRouteError as exc:
        return _emit({"schema": SCHEMA, "ok": False, "code": exc.code, "detail": exc.detail,
                      "lane": args.lane}, 2)
    except Exception as exc:  # a raw traceback must never reach the call site
        return _emit({"schema": SCHEMA, "ok": False, "code": "ERR_LANE_ROUTE_CLI_FAILURE",
                      "detail": f"{type(exc).__name__}:{exc}", "lane": args.lane}, 3)


if __name__ == "__main__":
    raise SystemExit(main())
