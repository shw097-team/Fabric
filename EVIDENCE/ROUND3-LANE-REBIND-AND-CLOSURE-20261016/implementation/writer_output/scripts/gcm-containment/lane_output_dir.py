#!/usr/bin/env python3
"""Per-lane, per-attempt output directories for HGK lanes (round HGK-GCM-REPAIR-20261013, Phase C1).

Recorded defect this closes
---------------------------
In round HGK-GCM-APPLY-20261013 two lanes (X3 and X3b) wrote the SAME deliverable paths
concurrently; the surviving frozen artifact was the weaker of the two (an ``X3_windows.jsonl`` with
3 lines overwrote an 8-line stream). The recorded cause is not "a lane was careless": two lanes
were handed the same output path and nothing made the second writer fail. This module makes that
collision loud.

Contract
--------
* A lane's attempt output lives at ``var/<round>/<lane>/attempt-<n>-<utc-ts>``.
* The attempt number ``n`` is derived from the existing attempt markers already present under
  ``var/<round>/<lane>/`` (``max(existing)+1``) or supplied explicitly by the caller.
* Creating the directory uses ``exist_ok=False``. If the directory already exists it is a LOUD
  failure (:class:`LaneOutputCollision`), never a silent reuse. Two lanes that race onto the same
  attempt number + timestamp therefore collide instead of sharing a path.

What this does NOT cover
------------------------
* It does not make the attempt number globally unique across *processes* by itself; the timestamp
  is second-granular, so two lanes starting in different seconds with the same logical attempt
  number would get DIFFERENT directories (distinct writes that happen to be mis-numbered). The
  loud-collision guarantee is over "this exact path already exists".
* It is not a scheduler and not a lock service. Single-use coordination is the Spine lease's job
  (see ``authorization_claim.py``); this module only owns the directory NAME and its loud creation.
"""
from __future__ import annotations

import ctypes
import json
import os
import stat
from datetime import UTC, datetime
from pathlib import Path

SCHEMA = "HGK-LANE-OUTPUT-DIR/1"
ATTEMPT_MARKER_SCHEMA = "HGK-LANE-ATTEMPT-MARKER/1"
ATTEMPT_MARKER_NAME = "attempt.marker.json"

# GetExitCodeProcess returns this while the process is still running.
_STILL_ACTIVE = 259
_PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
_ERROR_INVALID_PARAMETER = 87
_ERROR_ACCESS_DENIED = 5


class LaneOutputCollision(RuntimeError):
    """The attempt output directory already exists; refuse rather than reuse it."""

    def __init__(self, path):
        super().__init__(f"ERR_LANE_OUTPUT_DIR_EXISTS:{path}")
        self.path = str(path)


def utc_stamp(now: datetime | None = None) -> str:
    """A UTC stamp with second granularity, e.g. ``20261013T061012Z`` (matches ``var/`` names)."""
    now = now or datetime.now(UTC)
    return now.strftime("%Y%m%dT%H%M%SZ")


def round_root(repo_root, round_name: str, output_root=None) -> Path:
    """``<output_root>/<round>`` when an output root is given, else ``<repo_root>/var/<round>``."""
    base = Path(output_root) if output_root else Path(repo_root) / "var"
    return base / round_name


def lane_root(repo_root, round_name: str, lane: str, output_root=None) -> Path:
    return round_root(repo_root, round_name, output_root) / lane


_ATTEMPT_PREFIX = "attempt-"


def _attempt_number_of(name: str) -> int | None:
    """Parse ``attempt-<n>-<ts>`` -> ``n``; ``None`` for anything else."""
    if not name.startswith(_ATTEMPT_PREFIX):
        return None
    rest = name[len(_ATTEMPT_PREFIX):]
    num, _, _ = rest.partition("-")
    try:
        return int(num)
    except ValueError:
        return None


def existing_attempt_numbers(lane_root_path) -> list[int]:
    d = Path(lane_root_path)
    if not d.is_dir():
        return []
    found = []
    for child in d.iterdir():
        n = _attempt_number_of(child.name)
        if n is not None:
            found.append(n)
    return sorted(found)


def next_attempt_number(lane_root_path, supplied: int | None = None) -> int:
    """The attempt number to use: the caller's explicit value, else ``max(existing)+1`` (or 1)."""
    if supplied is not None:
        if supplied < 1:
            raise ValueError(f"attempt number must be >= 1, got {supplied!r}")
        return supplied
    existing = existing_attempt_numbers(lane_root_path)
    return (max(existing) + 1) if existing else 1


def derive_output_dir(repo_root, round_name: str, lane: str, *, attempt: int | None = None,
                      ts: str | None = None, output_root=None) -> Path:
    """The directory a lane/attempt must write to: ``var/<round>/<lane>/attempt-<n>-<ts>``."""
    n = next_attempt_number(lane_root(repo_root, round_name, lane, output_root), attempt)
    return lane_root(repo_root, round_name, lane, output_root) / f"attempt-{n}-{ts or utc_stamp()}"


def create_output_dir(path) -> Path:
    """Create the attempt directory, FAILING LOUDLY if it already exists (``exist_ok=False``)."""
    p = Path(path)
    try:
        p.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise LaneOutputCollision(p) from exc
    return p


def write_attempt_marker(out_dir, *, round_name: str, lane: str, attempt: int,
                         pid: int | None = None, process_create_time: float | None = None,
                         log_path=None, nonce: str | None = None, run_id: str | None = None) -> Path:
    """Record who owns this attempt dir, so a later reader can test process liveness (Phase C3)."""
    d = Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)
    create_time = process_create_time
    if create_time is None:
        create_time = _process_create_time(pid if pid is not None else os.getpid())
    marker = {
        "schema": ATTEMPT_MARKER_SCHEMA,
        "round": round_name,
        "lane": lane,
        "attempt": attempt,
        "dir": str(d),
        "pid": pid if pid is not None else os.getpid(),
        "process_create_time": create_time,
        "run_id": run_id,
        "nonce": nonce,
        "log_path": str(log_path) if log_path else None,
        "started_utc": datetime.now(UTC).isoformat(),
    }
    target = d / ATTEMPT_MARKER_NAME
    target.write_text(json.dumps(marker, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def read_attempt_marker(out_dir) -> dict | None:
    p = Path(out_dir) / ATTEMPT_MARKER_NAME
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def _process_create_time(pid: int | None) -> float | None:
    if pid is None:
        return None
    try:
        import psutil
    except Exception:
        return None
    try:
        return float(psutil.Process(pid).create_time())
    except Exception:
        return None


def process_liveness(pid: int | None, create_time: float | None = None) -> dict:
    """Strongest honest liveness check available on this host.

    Returns a dict with ``checked`` (did we reach a verdict?) and ``alive`` (True/False/None). The
    ``method`` and ``note`` fields say exactly which mechanism produced the verdict, and any caveat.
    This is pid-based: it cannot see a recycled pid unless ``create_time`` was recorded on the
    attempt marker (psutil path). It is NOT a process-tree check.
    """
    info: dict = {"pid": pid, "checked": False, "alive": None, "method": None, "note": ""}
    if pid is None or int(pid) <= 0:
        info["method"] = "none"
        info["note"] = "no pid recorded on the attempt marker"
        return info

    try:
        import psutil
    except Exception:
        psutil = None
    if psutil is not None:
        try:
            if not psutil.pid_exists(int(pid)):
                info.update(checked=True, alive=False, method="psutil.pid_exists")
                return info
            try:
                ct = float(psutil.Process(int(pid)).create_time())
            except Exception:
                ct = None
            if create_time is not None and ct is not None and abs(ct - float(create_time)) > 1.0:
                info.update(checked=True, alive=False, method="psutil.create_time_mismatch",
                            note=f"pid {pid} exists but create_time {ct} != recorded {create_time} "
                                 f"(pid reuse): treated as GONE")
                return info
            info.update(checked=True, alive=True, method="psutil",
                        process_create_time=ct)
            return info
        except Exception as exc:  # fall through to the ctypes path
            info["note"] = f"psutil path failed: {type(exc).__name__}: {exc}"

    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if handle:
            code = ctypes.c_ulong()
            ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
            kernel32.CloseHandle(handle)
            if ok:
                info.update(checked=True, alive=(code.value == _STILL_ACTIVE),
                            method="ctypes.GetExitCodeProcess")
                return info
            info.update(checked=False, alive=None, method="ctypes",
                        note="GetExitCodeProcess failed")
            return info
        err = ctypes.get_last_error()
        if err == _ERROR_INVALID_PARAMETER:
            info.update(checked=True, alive=False, method="ctypes.OpenProcess",
                        note="OpenProcess -> ERROR_INVALID_PARAMETER (no such process)")
            return info
        if err == _ERROR_ACCESS_DENIED:
            info.update(checked=True, alive=True, method="ctypes.OpenProcess",
                        note="OpenProcess -> ERROR_ACCESS_DENIED (process exists, not queryable)")
            return info
        info.update(checked=False, alive=None, method="ctypes.OpenProcess",
                    note=f"OpenProcess -> WinError {err}")
        return info

    # POSIX fallback
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        info.update(checked=True, alive=False, method="os.kill(0)")
        return info
    except PermissionError:
        info.update(checked=True, alive=True, method="os.kill(0)",
                    note="EPERM (exists, not signalable)")
        return info
    except OSError as exc:
        info.update(checked=False, alive=None, method="os.kill(0)",
                    note=f"{type(exc).__name__}: {exc}")
        return info
    info.update(checked=True, alive=True, method="os.kill(0)")
    return info


def live_attempt_in(out_dir) -> dict:
    """Inspect an existing attempt dir: is its recorded process still alive? (Phase C1/C3)."""
    p = Path(out_dir)
    result: dict = {"dir": str(p), "exists": p.exists(), "marker": None, "liveness": None}
    if not p.exists():
        return result
    marker = read_attempt_marker(p)
    result["marker"] = marker
    if marker is None:
        result["liveness"] = {"checked": False, "alive": None, "method": "no-marker",
                              "note": "directory exists but carries no attempt marker; liveness unknown"}
        return result
    result["liveness"] = process_liveness(marker.get("pid"), marker.get("process_create_time"))
    return result


def _mode_ok(path) -> bool:
    try:
        return stat.S_ISDIR(Path(path).stat().st_mode)
    except OSError:
        return False


if __name__ == "__main__":  # tiny self-check / probe
    import argparse

    ap = argparse.ArgumentParser(prog="lane_output_dir.py")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--round", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--attempt", type=int, default=None)
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    d = derive_output_dir(args.repo_root, args.round, args.lane, attempt=args.attempt)
    out = {"schema": SCHEMA, "dir": str(d), "attempt_number": _attempt_number_of(d.name)}
    if args.create:
        try:
            create_output_dir(d)
            out["created"] = True
        except LaneOutputCollision as exc:
            out["created"] = False
            out["collision"] = str(exc)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(out["dir"])
