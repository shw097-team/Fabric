#!/usr/bin/env python3
"""Deterministic lane child: exercises the dispatch's non-mutation guard with NO model.

Point the dispatcher at this file with ``--codex-executable <this path>``; it ignores the codex argv
it is handed and does exactly one thing, chosen by ``HGK_STUB_MODE``:

    clean   emit a conforming assistant message + usage row   (positive control: SHOULD stand)
    mutate  rewrite $HGK_STUB_TARGET, then the above
    remove  delete  $HGK_STUB_TARGET, then the above
    create  create  $HGK_STUB_TARGET, then the above

It emits BOTH carriers the dispatcher accepts on -- the nonce inside an
``item.completed``/``agent_message`` item (the only carrier ``nonce_in_agent_message`` reads) and a
matching usage row appended to ``$HGK_STUB_USAGE`` -- so the attempt satisfies every acceptance
condition and a mutation is what voids it. That is the whole point: the guard has to void a verdict
that would otherwise PASS, not merely fail a turn that was already failing.

The usage row goes to a SCRATCH ledger supplied by the caller, never the real relay ledger: no
relay/transport claim is made by this probe, only a guard claim. The stub is not codex and is not
inside the codex sandbox -- it can write anywhere its OS user can, which is exactly why a detection
mechanism is needed in addition to any sandbox expectation.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

NONCE = "HGK_LANE_NONCE_OK"


def emitted_nonce(argv: list[str]) -> str:
    """The nonce this child presents to the dispatcher.

    Default is the fixed ``NONCE``: the M06/M07 fixtures DEPEND on it not matching the nonce the
    dispatcher expects, which is how they drive an ``ERR_NO_ARM_EMITTED_NONCE`` refusal. A caller that
    needs the nonce to MATCH -- so that the SURFACE of the usage receipt is the only defect (M08 and
    its correct-arm control) -- sets ``HGK_STUB_EMIT_NONCE`` to the same value it passes to the
    dispatcher's ``--nonce``. ``argv`` is NOT consulted: ``--nonce`` is the DISPATCHER's flag and is
    never forwarded to this child.
    """
    override = (os.environ.get("HGK_STUB_EMIT_NONCE") or "").strip()
    return override or NONCE


def mutate(mode: str, target: str) -> str:
    if not target:
        return ""
    p = pathlib.Path(target)
    if mode == "mutate":
        p.write_bytes(p.read_bytes() + b"\n# mutated-by-deterministic-stub\n")
        return f"mutated {p}"
    if mode == "remove":
        existed = p.exists()
        if existed:
            p.unlink()
        return f"removed {p} existed={existed}"
    if mode == "create":
        p.write_text("stub-created\n", encoding="utf-8")
        return f"created {p}"
    return ""


def emit_usage() -> str:
    """Append a matching usage row so the attempt's usage receipt is OK. Scratch ledger only."""
    path = (os.environ.get("HGK_STUB_USAGE") or "").strip()
    line = (os.environ.get("HGK_STUB_USAGE_LINE") or "").strip()
    if not path or not line:
        return "no-usage-row"
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(json.loads(line), ensure_ascii=False) + "\n")
    return "usage-row-appended"


def main() -> int:
    mode = (os.environ.get("HGK_STUB_MODE") or "clean").strip().lower()
    note = mutate(mode, (os.environ.get("HGK_STUB_TARGET") or "").strip())
    usage = emit_usage()
    text = f"STUB {mode} {note} {usage} {emitted_nonce(sys.argv)}".strip()
    print(json.dumps({"type": "item.completed",
                      "item": {"type": "agent_message", "text": text}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
