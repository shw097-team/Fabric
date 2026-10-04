from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_text(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return result.stdout.strip()


def tracked_payload_files(root: Path) -> list[Path]:
    status = git_text(root, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise RuntimeError("ERR_PACKAGE_REQUIRES_CLEAN_HEAD")
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    relative_paths = [Path(value.decode("utf-8")) for value in result.stdout.split(b"\0") if value]
    files = []
    for relative in relative_paths:
        relative_posix = relative.as_posix()
        if relative_posix.startswith("evidence/wave-18/"):
            continue
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"ERR_TRACKED_PAYLOAD_NOT_FILE:{relative_posix}")
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix().casefold())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    head = git_text(root, "rev-parse", "HEAD")
    branch = git_text(root, "branch", "--show-current")
    files = tracked_payload_files(root)
    rows = []
    for path in files:
        data = path.read_bytes()
        rows.append({"path": path.relative_to(root).as_posix(), "bytes": len(data), "sha256": sha256_bytes(data)})
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=["path", "bytes", "sha256"], lineterminator="\n")
    writer.writeheader(); writer.writerows(rows)
    manifest_bytes = buffer.getvalue().encode("utf-8")
    release = root / "release"
    release.mkdir(exist_ok=True)
    manifest_path = release / "PAYLOAD_MANIFEST.csv"
    manifest_path.write_bytes(manifest_bytes)

    output_dir = root / "var" / "releases"
    output_dir.mkdir(parents=True, exist_ok=True)
    package = output_dir / "HG-KSEOS_LOCAL_CANDIDATE.zip"
    timestamp = (2026, 8, 8, 0, 0, 0)
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, row in zip(files, rows, strict=True):
            info = zipfile.ZipInfo(row["path"], timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
        info = zipfile.ZipInfo("PAYLOAD_MANIFEST.csv", timestamp)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, manifest_bytes)

    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        exact_set = names == [row["path"] for row in rows] + ["PAYLOAD_MANIFEST.csv"]
        mismatches = [row["path"] for row in rows if sha256_bytes(archive.read(row["path"])) != row["sha256"]]
        manifest_match = archive.read("PAYLOAD_MANIFEST.csv") == manifest_bytes
    acceptance = json.loads((root / "evidence" / "wave-15" / "MAKER_ACCEPTANCE_REPORT.json").read_text(encoding="utf-8"))
    receipt = {
        "schema": "HGK-LOCAL-PACKAGE-READBACK/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "canonical_head": head,
        "canonical_branch": branch,
        "git_status": "CLEAN",
        "package": str(package.relative_to(root)).replace("\\", "/"),
        "package_bytes": package.stat().st_size,
        "package_sha256": sha256_bytes(package.read_bytes()),
        "payload_files": len(rows),
        "archive_entries": len(names),
        "payload_manifest": "release/PAYLOAD_MANIFEST.csv",
        "payload_manifest_sha256": sha256_bytes(manifest_bytes),
        "exact_set": exact_set,
        "hash_mismatches": mismatches,
        "manifest_readback": manifest_match,
        "maker_acceptance": acceptance["counts"],
        "verdict": "LOCAL_PACKAGE_READBACK_PASS_WITH_TT" if exact_set and not mismatches and manifest_match else "FAIL",
        "claim_ceiling": "Canonical local candidate only; remote CI, deploy, and production remain unclaimed.",
    }
    evidence = root / "evidence" / "wave-18"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "LOCAL_PACKAGE_READBACK.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt))
    return 0 if receipt["verdict"].startswith("LOCAL_PACKAGE_READBACK_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
