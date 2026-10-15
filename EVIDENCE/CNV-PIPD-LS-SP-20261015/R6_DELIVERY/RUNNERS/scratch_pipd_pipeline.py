"""Scratch (throwaway) driver to exercise the pipd 13-command pipeline on a
scratch root. Not a delivered probe; used only to learn the real output shapes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
            "R6_DELIVERY/RAW/scratch_pipd").resolve()

from pipd_ls_sp import cli  # noqa: E402


def run(args: list[str]) -> int:
    print(f"\n### pipd {' '.join(args)}")
    rc = cli.main(["--root", str(ROOT), *args])
    print(f"### exit={rc}")
    return rc


if __name__ == "__main__":
    run(["init"])
    run(["intake", "--goal", "converge PIPD-LS-SP under HG-KSEOS",
         "--source", "PKG.md", "--constraint", "LOCAL_CEILING",
         "--non-goal", "production"])
    run(["profile", "--profile", "LITE"])
    for p in ("intent_card.json", "intent.json", "card.json"):
        f = ROOT / p
        if f.is_file():
            print("FOUND", p)
    print("ROOT TREE:")
    for f in sorted(ROOT.rglob("*")):
        if f.is_file():
            print("  ", f.relative_to(ROOT))
    # dump whatever intake/profile produced so we can build compile-pi args
    for f in sorted(ROOT.rglob("*.json")):
        try:
            print("\n---", f.name, "---")
            print(json.dumps(json.loads(f.read_text(encoding="utf-8")),
                             ensure_ascii=False)[:900])
        except Exception as exc:  # noqa: BLE001
            print("ERR", exc)
