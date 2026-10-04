"""Independent TST-092 checker: reopen the exact package at the exact HEAD,
re-derive the payload manifest from git ls-files, and verify byte-exact set/hash
equality. Read-only: never modifies the repo or the package.

Usage: python check_package_local.py --root <canonical_root>
Exit 0 = INDEPENDENT_CASE_PASS; 1 = FAIL; 2 = precondition drift.
"""
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


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    ).stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)

    head = git(root, "rev-parse", "HEAD").strip()
    branch = git(root, "branch", "--show-current").strip()
    status = git(root, "status", "--porcelain", "--untracked-files=all").strip()

    receipt_path = root / "evidence" / "wave-18" / "LOCAL_PACKAGE_READBACK.json"
    if not receipt_path.is_file():
        print(json.dumps({"verdict": "FAIL", "reason": "maker receipt missing"}))
        return 1
    maker = json.loads(receipt_path.read_text(encoding="utf-8"))
    package = root / maker["package"].replace("/", "\\")
    if not package.is_file():
        print(json.dumps({"verdict": "FAIL", "reason": f"package missing {package}"}))
        return 1

    # 1) Same HEAD + same package identity
    same_head = maker["canonical_head"] == head
    same_package = maker["package_sha256"] == sha256_bytes(package.read_bytes())

    # 2) Re-derive expected payload from git ls-files (same rule as packager)
    tracked = [
        p for p in git(root, "ls-files", "-z").split("\0") if p and not p.startswith("evidence/wave-18/")
    ]
    expected_paths = sorted(tracked, key=lambda p: p.casefold())

    # 3) Reopen zip and verify exact set + hashes
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        manifest_csv = archive.read("PAYLOAD_MANIFEST.csv").decode("utf-8")
        rows = list(csv.DictReader(io.StringIO(manifest_csv)))
        exact_set = names == expected_paths + ["PAYLOAD_MANIFEST.csv"]
        manifest_paths = [row["path"] for row in rows]
        mismatches = [
            row["path"]
            for row in rows
            if sha256_bytes(archive.read(row["path"])) != row["sha256"]
        ]
        manifest_bytes_match = csv.DictReader(
            io.StringIO(manifest_csv)
        ).fieldnames == ["path", "bytes", "sha256"]
        line_count_ok = len(rows) == len(expected_paths)

    result = {
        "schema": "HGK-TST-092-INDEPENDENT-READBACK/1",
        "checker": "INDEPENDENT_CHECKER (fresh read-only context; not the packager maker)",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "head": head,
        "branch": branch,
        "git_status_clean": not status,
        "package": str(package.relative_to(root)).replace("\\", "/"),
        "package_sha256": sha256_bytes(package.read_bytes()),
        "maker_receipt": "evidence/wave-18/LOCAL_PACKAGE_READBACK.json",
        "maker_verdict": maker.get("verdict"),
        "same_head_as_maker": same_head,
        "same_package_bytes_as_maker": same_package,
        "expected_payload_count": len(expected_paths),
        "manifest_row_count": len(rows),
        "manifest_count_matches": line_count_ok,
        "archive_exact_set": exact_set,
        "hash_mismatches": mismatches,
        "manifest_fieldnames_ok": manifest_bytes_match,
        "verdict": (
            "INDEPENDENT_CASE_PASS"
            if (
                same_head
                and same_package
                and not status
                and exact_set
                and not mismatches
                and manifest_bytes_match
                and line_count_ok
            )
            else "FAIL"
        ),
        "claim_ceiling": "TST-092 independent case verdict only; not a release claim.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "INDEPENDENT_CASE_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
