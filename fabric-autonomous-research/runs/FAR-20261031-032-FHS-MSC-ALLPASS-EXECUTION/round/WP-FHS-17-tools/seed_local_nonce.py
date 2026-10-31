#!/usr/bin/env python3
"""Fixture step for the replay negative: put a nonce in the WP-local ledger.

Reproduce (from C:/wg/queue/WP-FHS-17):
    python tools/seed_local_nonce.py --grant fixtures/replay-regrant.json \
        --ledger evidence/nonce-consumed.jsonl

This is fixture setup, not a receiver result and not a Host effect. It records
in the work package's own consumption ledger that a nonce was already spent, so
that the next `gate` call presents an already-consumed nonce and must refuse
with ERR_NONCE_REPLAY. The row is written by the receiver's own
`consume_nonce()`, imported from tools/wp17_receiver.py, so the fixture cannot
drift from the shape the gate itself writes.

Idempotent: if the nonce is already present, nothing is appended.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_receiver():
    spec = importlib.util.spec_from_file_location("wp17_receiver", ROOT / "tools" / "wp17_receiver.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grant", required=True)
    ap.add_argument("--ledger", required=True)
    a = ap.parse_args(argv)
    grant = json.loads(Path(a.grant).read_text(encoding="utf-8"))
    nonce = grant.get("nonce")
    if not nonce:
        print(json.dumps({"verdict": "REFUSED", "code": "GRANT_HAS_NO_NONCE"}, ensure_ascii=False))
        return 3
    ledger = Path(a.ledger)
    rec = load_receiver()
    prior = rec.nonce_consumed(ledger, nonce)
    before = sha_file(ledger) if ledger.is_file() else None
    if prior is None:
        rec.consume_nonce(ledger, nonce, {
            "operation": grant.get("operation"),
            "subject": grant.get("subject"),
            "candidate_sha256": grant.get("candidate_sha256"),
            "grant_sha256": sha_file(Path(a.grant)),
            "fixture": "replay-negative: pre-existing consumption of this nonce",
        })
    after = sha_file(ledger) if ledger.is_file() else None
    print(json.dumps({
        "verdict": "SEEDED" if prior is None else "ALREADY_PRESENT",
        "nonce": nonce,
        "ledger": str(ledger),
        "ledger_sha256_before": before,
        "ledger_sha256_after": after,
        "grant_sha256": sha_file(Path(a.grant)),
        "note": "fixture only; the gate must now refuse this nonce as ERR_NONCE_REPLAY",
        "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
