"""Run the frozen WS-A harness against an arbitrary subject with LIVE redirected.

Used to simulate the post-landing state (subject == live) before making the real
landing, and for the rollback proof. Imports the frozen harness module read-only,
overrides its LIVE/CAND module globals, and calls check().

  python run_harness_variant.py --subject <dir> --live <dir> [--out <json>]
  python run_harness_variant.py --restore    # run frozen harness as-is on (CAND, LIVE)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HARNESS = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py")


def load():
    spec = importlib.util.spec_from_file_location("ws_a_harness", HARNESS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default=None)
    ap.add_argument("--live", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    mod = load()
    if a.live:
        mod.LIVE = Path(a.live)
    subject = Path(a.subject) if a.subject else Path(mod.CAND)
    res = mod.check(subject)
    rep = {
        "schema": "WS_A/run_harness_variant",
        "subject_candidate": str(subject),
        "live_used": str(mod.LIVE),
        "checks": res,
    }
    rep["verdict"] = res.get("overall", "FAIL")
    txt = json.dumps(rep, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(txt, encoding="utf-8")
    print(txt)
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
