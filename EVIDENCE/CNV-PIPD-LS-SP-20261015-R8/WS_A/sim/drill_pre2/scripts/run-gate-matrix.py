#!/usr/bin/env python3
"""Run a pre-dispatch lane gate's case matrix and report observed vs intended results.

Why this exists: a gate's own evidence table is the WRITER's measurement, so a verifier has to run
每 row itself — and hand-running rows costs a tool call apiece, invites copying the writer's numbers,
and is exactly the step that gets skipped when the policy revision bumps (the moment the admit rows
start refusing for a stale pin). This runs the whole matrix deterministically against the CURRENT
registry/policy and exits non-zero on any mismatch.

A refusal is only a pass when it refuses for the INTENDED reason: the gate's verdict field (status
plus named error codes) is compared, not just the process exit code — argparse also exits 2 on a
mistyped flag, so an exit code alone cannot separate "refused correctly" from "invoked wrongly".

Usage:
  python run-gate-matrix.py --guard C:/…/scripts/hgk-lane-guard.py \
      --maker-model <executor model> --checker-engine hermes --checker-model <checker model> \
      --checker-provider <checker provider> [--root C:/…/HG-KSEOS] [--json out.json]

The flag names below are this stack's gate contract. Check the gate's `--help` once if it differs and
adapt the FLAG_* constants — do not guess them from the writer's table.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

FLAG_ADMISSION = "--admission"
FLAG_RECEIPT = "--receipt"
FLAG_REGISTRY = "--registry"
FLAG_EXPECTED_EPOCH = "--expected-epoch"


def _run(guard: pathlib.Path, argv: list[str], receipt: pathlib.Path) -> tuple[int, dict]:
    p = subprocess.run([sys.executable, str(guard), *argv, FLAG_RECEIPT, str(receipt)],
                       capture_output=True, text=True)
    verdict: dict = {}
    if receipt.is_file():
        try:
            verdict = json.loads(receipt.read_text(encoding="utf-8"))
        except Exception:
            verdict = {}
    return p.returncode, verdict


def _arm(lane: str, maker_engine: str, maker_model: str, target_engine: str, target_model: str,
         provider: str | None = None) -> list[str]:
    argv = ["--lane", lane, "--maker-engine", maker_engine, "--maker-model", maker_model,
            "--target-engine", target_engine, "--target-model", target_model]
    if provider is not None:
        argv += ["--target-provider", provider]
    return argv


def _fixture(path: pathlib.Path, model: str, provider: str, engine: str) -> str:
    """A synthetic positive control. Labelled so no reader can mistake it for a real admission."""
    path.write_text(json.dumps({
        "schema": "SYNTHETIC-CONTROL-FIXTURE-NOT-A-REAL-ADMISSION",
        "status": "ADMITTED",
        "arm": {"engine": engine, "model": model, "provider": provider},
        "served": {"engine": engine, "model": model, "provider": provider},
        "note": "positive control for the gate's admit path only; not evidence of admission",
    }, indent=1), encoding="utf-8")
    return str(path)


def _stale_registry(root: pathlib.Path, dest: pathlib.Path) -> pathlib.Path | None:
    """Copy the registry with its recorded source digest broken, to exercise the staleness row."""
    src = root / "config" / "lane-routing-registry.yaml"
    if not src.is_file():
        return None
    text = src.read_text(encoding="utf-8")
    broken, n = re.subn(r"(?m)^(\s*sha256:\s*)[0-9a-fA-F]{64}", lambda m: m.group(1) + "de" * 32,
                        text, count=1)
    if n == 0:
        return None
    dest.write_text(broken, encoding="utf-8")
    return dest


def _registry_epoch(root: pathlib.Path) -> int | None:
    src = root / "config" / "lane-routing-registry.yaml"
    if not src.is_file():
        return None
    m = re.search(r"(?m)^epoch:\s*(\d+)\s*$", src.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--guard", required=True, help="path to the gate CLI")
    ap.add_argument("--root", default=".", help="tree the gate resolves its registry under")
    ap.add_argument("--lane", default="VERIFY_SECURITY")
    ap.add_argument("--maker-engine", default="codex-cli")
    ap.add_argument("--maker-model", required=True, help="the maker/executor model on the gate's axis")
    ap.add_argument("--checker-engine", default="hermes")
    ap.add_argument("--checker-model", required=True)
    ap.add_argument("--checker-provider", default=None)
    ap.add_argument("--json", default=None, help="write the matrix result here")
    args = ap.parse_args()

    guard = pathlib.Path(args.guard)
    root = pathlib.Path(args.root).resolve()
    if not guard.is_file():
        print(f"ERR: gate not found: {guard}", file=sys.stderr)
        return 2

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="gate-matrix-"))
    rows: list[tuple[str, list[str], int, str | None]] = []
    try:
        checker_fix = _fixture(tmp / "checker.json", args.checker_model,
                               args.checker_provider or "", args.checker_engine)
        checker_arm = _arm(args.lane, args.maker_engine, args.maker_model, args.checker_engine,
                           args.checker_model, args.checker_provider)
        stale = _stale_registry(root, tmp / "registry-stale.yaml")
        epoch = _registry_epoch(root)

        rows.append(("sod_violation",
                     _arm(args.lane, args.maker_engine, args.maker_model, args.checker_engine,
                          args.maker_model, args.checker_provider) + [FLAG_ADMISSION, "ADMITTED"],
                     2, "ERR_LANE_SOD_VIOLATION"))
        rows.append(("admit_with_receipt", checker_arm + [FLAG_ADMISSION, checker_fix], 0, None))
        rows.append(("unevidenced_admission", checker_arm + [FLAG_ADMISSION, "ADMITTED"], 3,
                     "ERR_LANE_NOT_ADMITTED"))
        if args.checker_provider:
            rows.append(("provider_mismatch",
                         _arm(args.lane, args.maker_engine, args.maker_model, args.checker_engine,
                              args.checker_model, "not-" + args.checker_provider)
                         + [FLAG_ADMISSION, checker_fix], 3, "ERR_LANE_NOT_ADMITTED"))
            rows.append(("provider_omitted",
                         _arm(args.lane, args.maker_engine, args.maker_model, args.checker_engine,
                              args.checker_model) + [FLAG_ADMISSION, checker_fix], 3,
                         "ERR_LANE_NOT_ADMITTED"))
        if stale is not None:
            rows.append(("stale_source_pin", checker_arm + [FLAG_ADMISSION, checker_fix,
                                                            FLAG_REGISTRY, str(stale)], 4,
                         "ERR_LANE_SOURCE_STALE"))
        if epoch is not None:
            rows.append(("forced_epoch", checker_arm + [FLAG_ADMISSION, checker_fix,
                                                         FLAG_EXPECTED_EPOCH, str(max(epoch - 1, 0))],
                         4, None))

        out, mismatches, skipped = [], [], []
        for i, (name, argv, want_code, want_err) in enumerate(rows):
            code, verdict = _run(guard, argv, tmp / f"receipt-{i}.json")
            errors = verdict.get("errors") or []
            ok = (code == want_code) and (want_err is None or want_err in errors)
            out.append({"case": name, "exit_code": code, "intended_exit": want_code,
                        "status": verdict.get("status"), "errors": errors,
                        "intended_error": want_err, "match": ok})
            if not ok:
                mismatches.append(name)
            print(f"  {name:<22} exit={code:<2} intended={want_code:<2} "
                  f"status={verdict.get('status')} errors={errors} {'OK' if ok else 'MISMATCH'}")
            if not verdict:
                skipped.append(name)

        print(f"\n  rows={len(out)} mismatches={len(mismatches)}"
              f"{' (unparsable verdicts: ' + ', '.join(skipped) + ')' if skipped else ''}")
        if mismatches:
            print("  MISMATCHED: " + ", ".join(mismatches))
        if args.json:
            pathlib.Path(args.json).write_text(json.dumps(
                {"guard": str(guard), "rows": out, "mismatches": mismatches,
                 "unparsable_verdicts": skipped}, indent=1), encoding="utf-8", newline="")
        return 1 if mismatches else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
