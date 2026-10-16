"""R6 bounded-writer probe harness.

Runs real subprocess probes, captures command/cwd/UTC/exit/stdout/stderr verbatim,
and writes one raw capture per probe under RAW/. Never invents output.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
RAW = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/RAW")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def capture(probe_id: str, cmd: list[str], cwd: str, env_extra: dict | None = None,
            timeout: int = 300, stdin_text: str | None = None) -> dict:
    """Execute one probe; write RAW/<probe_id>.{stdout,stderr,json}."""
    RAW.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    started = utc_now()
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout,
            input=(stdin_text.encode() if stdin_text is not None else None),
        )
        out, err, code = proc.stdout, proc.stderr, proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or b""
        err = (exc.stderr or b"") + b"\n[PROBE_TIMEOUT]"
        code = None
        timed_out = True
    except FileNotFoundError as exc:
        out = b""
        err = f"[PROBE_FILE_NOT_FOUND] {exc}".encode()
        code = None
        timed_out = False
    ended = utc_now()

    (RAW / f"{probe_id}.stdout.txt").write_bytes(out)
    (RAW / f"{probe_id}.stderr.txt").write_bytes(err)
    record = {
        "probe_id": probe_id,
        "command": cmd,
        "cwd": cwd,
        "started_utc": started,
        "ended_utc": ended,
        "exit_code": code,
        "timed_out": timed_out,
        "stdout_file": f"RAW/{probe_id}.stdout.txt",
        "stderr_file": f"RAW/{probe_id}.stderr.txt",
        "stdout_sha256": sha256_bytes(out),
        "stderr_sha256": sha256_bytes(err),
        "stdout_bytes": len(out),
        "stderr_bytes": len(err),
    }
    (RAW / f"{probe_id}.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    return record


if __name__ == "__main__":
    # usage: python probe_lib.py <probe_id> <cwd> -- cmd args...
    args = sys.argv[1:]
    pid = args[0]
    cwd = args[1]
    rest = args[2:]
    if rest and rest[0] == "--":
        rest = rest[1:]
    rec = capture(pid, rest, cwd)
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    sys.exit(0)
