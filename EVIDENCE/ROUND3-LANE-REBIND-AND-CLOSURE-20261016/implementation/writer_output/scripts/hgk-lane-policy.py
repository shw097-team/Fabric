#!/usr/bin/env python
"""hgk-lane-policy.py — CLI for the HG-KSEOS lane-routing registry (CANDIDATE).

Subcommands:
  validate              drift check of the live projection sites; exit 1 on any fatal drift
  generate --out PATH   emit the projected policy document (default: inside this round dir)
  diff-live             show what would change between the registry and the live sites
  epoch                 print the current policy epoch

Read-only for all site traffic; `generate` writes only to the --out target. Everything is
CANDIDATE. No live install, canonical policy, or Shared Spine path is written.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_ROOT = _HERE.parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from hg_kseos import lane_policy as lp  # noqa: E402

DEFAULT_OUT = _ROOT / "var" / "far-lane-sod-003" / "evidence" / "lane-policy-projected.json"


def _registry(args) -> tuple[dict, Path]:
    path = Path(args.registry) if args.registry else lp.DEFAULT_REGISTRY
    return lp.load_registry(path), path


def cmd_epoch(args) -> int:
    registry, _ = _registry(args)
    print(lp.registry_epoch(registry))
    return 0


def _run_drift(args) -> tuple[dict, Path, list]:
    registry, path = _registry(args)
    root = Path(args.root) if args.root else None
    findings = lp.check_drift(path, root=root, registry=registry)
    return registry, path, findings


def cmd_validate(args) -> int:
    registry, path, findings = _run_drift(args)
    receipt = lp.render_receipt(
        registry=registry,
        findings=findings,
        checked_sites=lp.count_checked_sites(registry),
        extra={
            "registry_path": str(path),
            "registry_sha256": lp._sha256_file(path) if path.exists() else None,
            "fatal_errors": [f for f in findings if f["severity"] == "error"],
            "debt": [f for f in findings if f["severity"] == "warn"],
        },
    )
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if lp.drift_is_fatal(findings) else 0


def cmd_diff_live(args) -> int:
    registry, path, findings = _run_drift(args)
    diff = {
        "schema": "HGK-LANE-DIFF/1",
        "status": "CANDIDATE",
        "epoch": lp.registry_epoch(registry),
        "changes": [
            {
                "id": f.get("id"),
                "path": f.get("path"),
                "pointer": f.get("pointer"),
                "expected": f.get("expected"),
                "actual": f.get("actual"),
                "code": f.get("code"),
            }
            for f in findings
        ],
        "fatal": lp.drift_is_fatal(findings),
    }
    print(json.dumps(diff, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if lp.drift_is_fatal(findings) else 0


def cmd_generate(args) -> int:
    registry, path = _registry(args)
    out = Path(args.out) if args.out else DEFAULT_OUT
    doc = lp.project_policy(registry, registry_path=path)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(doc, ensure_ascii=False, sort_keys=True, indent=2)
    out.write_text(payload + "\n", encoding="utf-8", newline="\n")
    summary = {
        "schema": "HGK-LANE-GENERATE/1",
        "status": "CANDIDATE",
        "out": str(out),
        "bytes": out.stat().st_size,
        "sha256": lp._sha256_file(out),
        "epoch": doc["epoch"],
        "claim_ceiling": "CANDIDATE_ONLY",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hgk-lane-policy.py", description=__doc__)
    parser.add_argument("--registry", default=None, help="path to the registry (default: repo config)")
    parser.add_argument("--root", default=None, help="base dir for relative projection paths (default: repo root)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="drift-check the live projection sites")
    sub.add_parser("diff-live", help="show what would change")
    sub.add_parser("epoch", help="print the current policy epoch")

    gen = sub.add_parser("generate", help="emit the projected policy document")
    gen.add_argument("--out", default=None, help="output path (default: round evidence dir)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dispatch = {
        "validate": cmd_validate,
        "diff-live": cmd_diff_live,
        "epoch": cmd_epoch,
        "generate": cmd_generate,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
