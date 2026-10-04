from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from hg_kseos.recovery import restore_database


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    manifests = sorted((root / "var" / "backups").glob("*.manifest.json"))
    if not manifests:
        raise SystemExit("ERR_BACKUP_MANIFEST_MISSING")
    manifest_path = manifests[-1]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    backup = Path(manifest["backup"])
    destination = root / "worktrees" / "restore-drill" / f"restored-{time.time_ns()}-{backup.name}"
    if destination.exists():
        raise SystemExit(f"ERR_RESTORE_DESTINATION_EXISTS:{destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    result = restore_database(backup, manifest["sha256"], destination)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    with sqlite3.connect(destination) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        schema_version = connection.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0]
        requirements = connection.execute("SELECT COUNT(*) FROM requirements").fetchone()[0]
        providers = connection.execute("SELECT COUNT(*) FROM provider_bindings").fetchone()[0]
    report = {
        "schema": "HGK-RESTORE-DRILL/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "backup_manifest": str(manifest_path.relative_to(root)).replace("\\", "/"),
        "backup_sha256": manifest["sha256"],
        "restore_result": result,
        "destination": str(destination.relative_to(root)).replace("\\", "/"),
        "rto_observed_ms": elapsed_ms,
        "integrity": integrity,
        "schema_version": schema_version,
        "requirements": requirements,
        "providers": providers,
        "status": "RESTORE_DRILL_PASS" if integrity == "ok" and requirements == 499 and providers == 79 else "FAIL",
        "claim_ceiling": "Project-local SQLite restore drill; no production disaster-recovery claim.",
    }
    output = root / "evidence" / "wave-16" / "RESTORE_DRILL_REPORT.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))
    return 0 if report["status"] == "RESTORE_DRILL_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
