from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


EXPECTED = {"skills": 18, "agents": 10, "prompts": 12, "workflows": 8, "state-machines": 6}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def files(root: Path) -> list[Path]:
    return sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix().casefold())


def category_count(root: Path, category: str) -> int:
    category_root = root / category
    if category == "skills":
        return len(list(category_root.glob("*/SKILL.md")))
    prefix = {"agents": "AP-", "prompts": "PC-", "workflows": "WF-", "state-machines": "SM-"}[category]
    return len(list(category_root.glob(f"{prefix}*.md")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    project = args.project_root.resolve(strict=True)
    destination = project / "control"
    if destination.exists():
        raise SystemExit("ERR_CONTROL_DESTINATION_EXISTS")
    if any(item.is_symlink() for item in source.rglob("*")):
        raise SystemExit("ERR_CONTROL_SOURCE_LINK")
    observed = {key: category_count(source, key) for key in EXPECTED}
    if observed != EXPECTED:
        raise SystemExit(f"ERR_CONTROL_DENOMINATOR:{observed}")
    source_rows = [(item.relative_to(source).as_posix(), digest(item), item.stat().st_size) for item in files(source)]
    shutil.copytree(source, destination, copy_function=shutil.copy2)
    destination_rows = [
        (item.relative_to(destination).as_posix(), digest(item), item.stat().st_size) for item in files(destination)
    ]
    if source_rows != destination_rows:
        raise SystemExit("ERR_CONTROL_READBACK_MISMATCH")
    manifest = project / "registries" / "CONTROL_MATERIALIZATION_MANIFEST.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(("relative_path", "sha256", "bytes"))
        writer.writerows(destination_rows)
    receipt = {
        "captured_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "source": str(source),
        "destination": str(destination),
        "counts": observed,
        "physical_files": len(destination_rows),
        "manifest": str(manifest),
        "manifest_sha256": digest(manifest),
        "readback": "PASS",
        "runtime_admission": "NOT_CLAIMED",
    }
    receipt_path = project / "evidence" / "wave-08" / "CONTROL_MATERIALIZATION_RECEIPT.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
