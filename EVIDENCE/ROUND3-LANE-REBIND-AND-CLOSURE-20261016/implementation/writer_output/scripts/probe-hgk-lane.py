#!/usr/bin/env python
"""probe-hgk-lane.py — lane-shaped admission probe (CANDIDATE).

Performs a bounded, lane-shaped exercise of ONE arm and records what actually served it by reading
the Hermes agent.log session line (`model=... provider=...`). It records the direct-completion
result SEPARATELY and never sets ADMITTED from a direct completion alone.

`--dry-run` performs no network I/O and leaves the arm UNPROVEN: it emits the request envelope and
the exact commands it WOULD run, so the kit is testable and reviewable offline.

A live (non-dry) run is only meaningful once the launcher/relay hardening in the adoption guide is
admitted; running it here would dispatch through the sealed lane. The probe therefore defaults to
dry-run and fails closed (exit 3 / UNPROVEN) if asked to run live without a real binding.

Everything is CANDIDATE.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_ROOT = _HERE.parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from hg_kseos import lane_admission as la  # noqa: E402
from hg_kseos import lane_policy as lp  # noqa: E402

DEFAULT_AGENT_LOG = Path(
    r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\logs\agent.log"
)
_SESSION_RE = None


def _session_line_pattern():
    import re

    return re.compile(
        r"model=(?P<model>[\w.\-/]+)\s+provider=(?P<provider>[\w.\-]+)"
    )


def parse_served_from_log(log_path: Path, *, session_id: str | None = None,
                          tail_bytes: int = 200_000) -> dict:
    """Read the tail of agent.log and return the last `model=... provider=...` line.

    Read-only. If session_id is given, prefer lines that carry it.
    """
    pattern = _session_line_pattern()
    if not log_path.exists():
        return {"found": False, "reason": "ERR_LANE_LOG_MISSING", "log": str(log_path)}
    size = log_path.stat().st_size
    with log_path.open("rb") as handle:
        if size > tail_bytes:
            handle.seek(size - tail_bytes)
        blob = handle.read().decode("utf-8", "replace")
    matches = []
    for line in blob.splitlines():
        m = pattern.search(line)
        if m:
            matches.append((line, m.group("model"), m.group("provider")))
    if not matches:
        return {"found": False, "reason": "ERR_LANE_LOG_NO_SESSION_LINE", "log": str(log_path)}
    chosen = matches[-1]
    if session_id:
        for cand in reversed(matches):
            if session_id in cand[0]:
                chosen = cand
                break
    return {
        "found": True,
        "log": str(log_path),
        "model": chosen[1],
        "provider": chosen[2],
        "line": chosen[0][-400:],
    }


def build_record(args) -> la.LaneAdmission:
    registry = lp.load_registry(Path(args.registry) if args.registry else lp.DEFAULT_REGISTRY)
    epoch = lp.registry_epoch(registry)
    record = la.LaneAdmission(
        lane=args.lane,
        arm={"provider": args.provider, "model": args.model, "engine": args.engine},
        policy_epoch=epoch,
        request_profile={"mode": "production" if args.request_envelope == "production" else "compact",
                         "stream": True, "thinking": "same-as-production"},
    )
    return record


def run_dry(args, record: la.LaneAdmission) -> dict:
    """Offline: emit the exercise plan and the commands; do not touch the network."""
    record.record_start()
    plan = {
        "phase": 1,
        "direct_completion": {
            "status": "NOT_RUN_DRY_RUN",
            "command": (
                "# would issue one bounded completion via the arm's provider client; "
                "result recorded separately and NEVER sufficient for ADMITTED"
            ),
        },
        "lane_exercise": {
            "status": "NOT_RUN_DRY_RUN",
            "command": (
                f"pwsh -NoProfile -File {_ROOT / 'scripts' / 'start-hgk-hermes.ps1'} "
                f"-Action Write -ModelChain {args.model} -Prompt \"read a random nonce with a tool, "
                f"hash it, emit bounded JSON only\""
            ),
            "required": ">=1 completed model call AND >=1 completed tool AND served identity matches",
            "evidence": "agent.log session line model=... provider=...",
        },
    }
    record.decide()  # remains UNPROVEN
    result = record.to_dict()
    result["mode"] = "DRY_RUN"
    result["plan"] = plan
    result["agent_log_path"] = str(args.agent_log)
    return result


def run_live(args, record: la.LaneAdmission) -> dict:
    """Live lane-shaped exercise. Fails closed without a real binding and without the launcher."""
    record.record_start()
    if not args.binding or not Path(args.binding).exists():
        record.set_failure("ERR_LANE_NO_BINDING")
        record.decide()
        out = record.to_dict()
        out["mode"] = "LIVE"
        out["note"] = ("live bound exercise requires an admitted ExecutionBinding and the hardened "
                       "sealed launcher; refusing to dispatch")
        return out
    # The genuine dispatch is intentionally NOT implemented in this candidate kit: it would run the
    # sealed lane. Record it as NOT_DONE and remain UNPROVEN rather than fake an admission.
    record.set_failure("ERR_LANE_LIVE_EXERCISE_NOT_IMPLEMENTED")
    record.decide()
    out = record.to_dict()
    out["mode"] = "LIVE"
    out["served_from_log"] = parse_served_from_log(Path(args.agent_log))
    out["note"] = ("live lane-shaped dispatch is staged only: implement under an admitted execution "
                   "WorkOrder; direct completion alone would never be sufficient")
    return out


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="probe-hgk-lane.py", description=__doc__)
    parser.add_argument("--lane", required=True, choices=list(lp.LANE_ORDER))
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--engine", required=True, choices=["hermes", "codex-cli"])
    parser.add_argument("--binding", default=None, help="ExecutionBinding path (live only)")
    parser.add_argument("--deadline-seconds", type=int, default=300)
    parser.add_argument("--request-envelope", default="production", choices=["production", "compact"])
    parser.add_argument("--agent-log", default=str(DEFAULT_AGENT_LOG))
    parser.add_argument("--output-root", default=str(_ROOT / "var" / "far-lane-sod-003" / "evidence" / "lane-admission"))
    parser.add_argument("--receipt", default=None, help="write the admission receipt here")
    parser.add_argument("--registry", default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    record = build_record(args)
    result = run_dry(args, record) if args.dry_run else run_live(args, record)

    receipt_path = args.receipt
    if receipt_path is None:
        key = la.admission_key(lane=args.lane, arm={"provider": args.provider,
                                                   "model": args.model, "engine": args.engine})
        receipt_path = str(Path(args.output_root) / key / "receipt.json")
    Path(receipt_path).parent.mkdir(parents=True, exist_ok=True)
    Path(receipt_path).write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                                  encoding="utf-8", newline="\n")
    result["receipt_path"] = receipt_path
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))

    if result.get("status") == la.ADMITTED:
        return 0
    if result.get("status") == la.REFUSED:
        return 2
    return 3  # UNPROVEN (including dry-run) is not an admission


if __name__ == "__main__":
    raise SystemExit(main())
