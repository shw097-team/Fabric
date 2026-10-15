"""Negative probe: requirements.project_id FK must be satisfied (fail-closed).

Registers a requirement under a project_id that was NOT created -> the spine's FK
constraint must refuse. This is the observation that was discovered during probe
development and is recorded here verbatim.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/HG-KSEOS/src")

RAW = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
           "R6_CHECKER/COPIES/probes/RAW")
DB = RAW / "spine_fk_scratch.sqlite"

from hg_kseos.spine import SharedSpine  # noqa: E402


def run() -> int:
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB) + suffix)
        if p.exists():
            p.unlink()
    spine = SharedSpine(DB)
    spine.initialize()
    spine.create_project("HGK-P0", "FK probe")
    try:
        spine.register_requirement(
            requirement_id="REQ-FK-001",
            source_locator="RAW/spine_probe_source.md#clause-1",
            wording="FK probe requirement",
            acceptance_id="ACC-FK-001",
            oracle="deterministic assertion",
            threshold="EXPLICIT_ORACLE_PASS",
            negative_fixture="fixtures/negative",
            priority="P0",
            project_id="CNV-R6-NOT-CREATED",
        )
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "SPINE_FK_REFUSED",
                          "error_type": type(exc).__name__, "error": str(exc)},
                         ensure_ascii=False, indent=1))
        for suffix in ("", "-wal", "-shm"):
            p = Path(str(DB) + suffix)
            if p.exists():
                p.unlink()
        return 0
    print(json.dumps({"verdict": "FAIL", "probe": "spine-fk",
                      "detail": "unregistered project_id was accepted"}))
    return 1


if __name__ == "__main__":
    raise SystemExit(run())
