#!/usr/bin/env python3
"""Freeze a verification subject and prove its boundary in one deterministic pass.

Emits ONE json receipt with:
  subject  per-file sha256 + size for every file under each --subject-root
  guard    per --guard path: digest, mtime, and modified_during_window, where the
           window is DERIVED from a live PID or an explicit ISO stamp and never
           hand-typed -- a wrong epoch literal inverts every guard row at once
  pairs    per --pair PRE:CAND: numstat plus the hunk headers, so "the candidate
           differs by exactly N edits" is CHECKED rather than asserted

Deliberately stdlib-only (psutil used for the PID window when importable).

Usage:
  freeze-subject-and-guard.py \
      --subject-root /abs/subject \
      --guard /abs/repo/config/a.json --guard /abs/repo/scripts/b.ps1 \
      --window-pid 2380 \
      --pair /abs/pre.ps1:/abs/cand.ps1 \
      --out /abs/verify/SUBJECT_DIGESTS.json

Exit codes: 0 ok, 2 a named path was missing, 3 bad arguments.
Missing paths are REPORTED, never silently skipped -- a freeze receipt that
omits what it could not read is worse than one that says so.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def stamp(epoch: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch))


def walk_root(root: Path) -> dict:
    out = {}
    if not root.exists():
        return out
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[p.as_posix()] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    return out


def resolve_window(args) -> tuple:
    if args.window_pid:
        try:
            import psutil  # noqa: WPS433 - optional on purpose
            created = psutil.Process(args.window_pid).create_time()
            return created, f"pid:{args.window_pid}"
        except Exception as exc:  # noqa: BLE001 - report, do not guess
            print(f"WARN: could not read pid {args.window_pid} create_time ({exc}); "
                  f"falling back to --window-start", file=sys.stderr)
    if args.window_start:
        epoch = time.mktime(time.strptime(args.window_start, "%Y-%m-%d %H:%M:%S"))
        return epoch, f"explicit:{args.window_start}"
    return None, "none"


def pair_report(pre: Path, cand: Path) -> dict:
    missing = [str(p) for p in (pre, cand) if not p.exists()]
    if missing:
        return {"pre": str(pre), "cand": str(cand), "error": f"missing: {missing}"}
    base = ["git", "diff", "--no-index", "--", str(pre), str(cand)]
    # git diff --no-index exits 1 whenever the files differ: expected, not a failure.
    numstat = subprocess.run(base[:3] + ["--numstat"] + base[3:],
                             capture_output=True, text=True).stdout.strip()
    unified = subprocess.run(base[:3] + ["-U0"] + base[3:],
                             capture_output=True, text=True).stdout
    hunks = [ln for ln in unified.splitlines() if ln.startswith("@@")]
    added = deleted = None
    if numstat:
        parts = numstat.split("\t")
        if len(parts) >= 2:
            added, deleted = parts[0], parts[1]
    return {
        "pre": str(pre),
        "cand": str(cand),
        "pre_sha256": sha256(pre),
        "cand_sha256": sha256(cand),
        "numstat": numstat or "(identical)",
        "added": added,
        "deleted": deleted,
        "hunk_count": len(hunks),
        "hunk_headers": hunks,
        "note": "hunk_count is the checkable form of 'the candidate differs by exactly N edits'",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject-root", action="append", default=[], required=True)
    ap.add_argument("--guard", action="append", default=[])
    ap.add_argument("--pair", action="append", default=[],
                    help="PRE:CAND, native paths")
    ap.add_argument("--window-pid", type=int)
    ap.add_argument("--window-start", help="'YYYY-MM-DD HH:MM:SS' local")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    window, window_src = resolve_window(args)
    receipt = {
        "frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "window": {"start_epoch": window, "start": stamp(window) if window else None,
                   "source": window_src},
        "subject": {},
        "guard": {},
        "pairs": [],
        "missing": [],
        "claim_ceiling": "SUBJECT FREEZE ONLY - not acceptance, not promotion",
    }
    rc = 0

    for root in args.subject_root:
        root_p = Path(root)
        walked = walk_root(root_p)
        receipt["subject"][root_p.as_posix()] = walked
        if not walked:
            receipt["missing"].append(root_p.as_posix())
            rc = max(rc, 2)
        print(f"subject {root_p.as_posix()}: {len(walked)} files")

    for g in args.guard:
        p = Path(g)
        if not p.exists():
            receipt["guard"][p.as_posix()] = {"error": "missing"}
            receipt["missing"].append(p.as_posix())
            rc = max(rc, 2)
            continue
        mt = p.stat().st_mtime
        row = {"sha256": sha256(p), "mtime": stamp(mt),
               "modified_during_window": (mt > window) if window else None}
        receipt["guard"][p.as_posix()] = row
        print(f"guard   {p.as_posix():<60} {row['mtime']}  "
              f"modified_during_window={row['modified_during_window']}")

    for spec in args.pair:
        if ":" not in spec:
            print(f"bad --pair {spec!r}, want PRE:CAND", file=sys.stderr)
            return 3
        pre, cand = spec.split(":", 1)
        row = pair_report(Path(pre), Path(cand))
        receipt["pairs"].append(row)
        print(f"pair    {pre} -> {cand}: hunks={row.get('hunk_count')} "
              f"numstat={row.get('numstat')}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"WROTE {out}")
    if receipt["missing"]:
        print(f"MISSING (reported, not skipped): {receipt['missing']}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
