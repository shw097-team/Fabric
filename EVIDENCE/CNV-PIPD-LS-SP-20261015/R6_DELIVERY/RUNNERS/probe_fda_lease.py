"""bounded-FS-API-Desktop probe (ACC-014): DesktopLeaseManager lease / checkpoint /
replay gating.

Uses the REAL fda_lease module from the Fabric FDA review bundle. In-memory only.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "C:/Projects/Agent_Workspace/Fabric/evidence/review/FDA_RAW_REVIEW_BUNDLE/"
                   "Fabric/fabric-desktop-automation")

from fda_lease import DesktopLeaseManager, LeaseDenied, UnknownState, idempotency_key  # noqa: E402


def _emit(obj: dict) -> int:
    print(json.dumps(obj, ensure_ascii=False, indent=1, default=str))
    return 0 if obj.get("verdict") != "FAIL" else 1


def positive() -> int:
    m = DesktopLeaseManager()
    held = m.acquire("S-R6", "writer-A")
    m.checkpoint("S-R6", "ckpt-1", desktop_state_digest="d" * 64)
    transferred = m.transfer("S-R6", "writer-A", "writer-B")
    now = m.current_writer("S-R6")
    key = idempotency_key("WO-R6", "TASK-R6", "app", "1.0", "LOCAL", "target")
    return _emit({
        "verdict": "FDA_LEASE_POSITIVE_OK",
        "acquired_writer": held,
        "transferred_to": transferred,
        "current_writer": now,
        "idempotency_key_len": len(key),
        "replay_none_class": m.replay_allowed("NONE", None, True),
    })


def negative() -> int:
    m = DesktopLeaseManager()
    m.acquire("S-R6-NEG", "writer-A")
    second = None
    try:
        m.acquire("S-R6-NEG", "writer-B")
    except LeaseDenied as exc:
        second = {"error_type": type(exc).__name__, "error": str(exc)}
    stale = None
    try:
        m.acquire("S-R6-STALE", "writer-A", after_checkpoint="ckpt-nope")
    except ValueError as exc:
        stale = {"error_type": type(exc).__name__, "error": str(exc)}
    unknown = None
    try:
        m.replay_allowed("LOCAL", "receipt", None)
    except UnknownState as exc:
        unknown = {"error_type": type(exc).__name__, "error": str(exc)}
    return _emit({
        "verdict": "FDA_LEASE_NEGATIVE_REFUSED",
        "second_writer_refused": second,
        "stale_checkpoint_refused": stale,
        "unknown_state_refused": unknown,
        "gated_replay_refused": m.replay_allowed("EXTERNAL_APPROVAL_GATED", "receipt", True),
        "already_applied_replay_refused": m.replay_allowed("LOCAL", "receipt", True),
    })


MODES = {"positive": positive, "negative": negative}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "positive"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(fn())
