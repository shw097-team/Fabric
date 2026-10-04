from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(*argv: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-root", type=Path, required=True)
    parser.add_argument("--uv", type=Path, required=True)
    parser.add_argument("--installer", type=Path, required=True)
    parser.add_argument("--uv-archive", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--expected-tag", required=True)
    args = parser.parse_args()

    install_root = args.install_root.resolve()
    hermes = install_root / "venv" / "Scripts" / "hermes.exe"
    python = install_root / "venv" / "Scripts" / "python.exe"
    uv_lock = install_root / "uv.lock"
    pyproject = install_root / "pyproject.toml"
    git = Path(r"C:\Program Files\Git\cmd\git.exe")

    required = [install_root, hermes, python, args.uv, args.installer, args.uv_archive, uv_lock, pyproject, git]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"missing required paths: {missing}")

    head = run(str(git), "-c", f"safe.directory={install_root}", "-C", str(install_root), "rev-parse", "HEAD")
    tag = run(str(git), "-c", f"safe.directory={install_root}", "-C", str(install_root), "describe", "--tags", "--exact-match", "HEAD")
    status = run(str(git), "-c", f"safe.directory={install_root}", "-C", str(install_root), "status", "--porcelain=v1")
    if head != args.expected_commit or tag != args.expected_tag or status:
        raise SystemExit({"head": head, "tag": tag, "status": status})

    version = run(str(hermes), "--version")
    imports = run(
        str(python),
        "-c",
        "import fastapi, hermes_cli, mcp, openai; print('IMPORTS_OK')",
    )
    packages = json.loads(run(str(args.uv), "pip", "list", "--python", str(python), "--format", "json"))
    packages.sort(key=lambda item: item["name"].lower())

    args.output_dir.mkdir(parents=True, exist_ok=True)
    captured_at = datetime.now(timezone.utc).isoformat()
    package_path = args.output_dir / "HERMES_INSTALLED_PACKAGES.json"
    package_path.write_text(json.dumps(packages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = {
        "schema": "HGK-HERMES-INSTALL-RECEIPT/1",
        "captured_at_utc": captured_at,
        "result": "PASS_LOCAL_CORE_NO_PROVIDER",
        "claim_ceiling": "Pinned local native-Windows core install and import smoke test only; no provider, OAuth, API key, gateway, remote CI, deploy, production, or independent acceptance claim.",
        "install_root": str(install_root),
        "release": {
            "product_version": version.splitlines()[0],
            "tag": tag,
            "commit": head,
            "repository_clean": True,
            "source": "https://github.com/NousResearch/hermes-agent.git",
        },
        "installer": {
            "path": str(args.installer.resolve()),
            "sha256": sha256(args.installer),
            "executed_modes": ["MANIFEST_ONLY"],
            "full_installer_executed": False,
            "reason": "Manual staged install avoided floating fallback and installer global-Git mutation.",
        },
        "uv": {
            "path": str(args.uv.resolve()),
            "sha256": sha256(args.uv),
            "archive_path": str(args.uv_archive.resolve()),
            "archive_sha256": sha256(args.uv_archive),
            "sync_command": "uv sync --extra all --locked",
            "unlocked_fallback_used": False,
        },
        "locks": {
            "uv_lock_sha256": sha256(uv_lock),
            "pyproject_sha256": sha256(pyproject),
        },
        "runtime": {
            "python": run(str(python), "--version"),
            "imports": imports,
            "installed_package_count": len(packages),
            "package_manifest": package_path.name,
            "package_manifest_sha256": sha256(package_path),
        },
        "mutations": {
            "user_path_modified": False,
            "global_git_config_modified": False,
            "config_template_installed": False,
            "gateway_installed": False,
            "provider_credentials_configured": False,
        },
        "open_next_steps": [
            "Run permission-negative and rollback tests in an isolated test home.",
            "Provider setup requires explicit human OAuth/API-key input.",
            "Run independent NRTV after provider-bound pilot evidence exists.",
        ],
    }
    receipt_path = args.output_dir / "HERMES_INSTALL_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tool_lock = {
        "schema": "HGK-TOOL-LOCK/1",
        "generated_at_utc": captured_at,
        "tools": [
            {
                "id": "HERMES_AGENT",
                "version": "0.18.2",
                "tag": tag,
                "commit": head,
                "install_root": str(install_root),
                "uv_lock_sha256": sha256(uv_lock),
            },
            {
                "id": "UV",
                "version": "0.11.29",
                "executable": str(args.uv.resolve()),
                "sha256": sha256(args.uv),
                "archive_sha256": sha256(args.uv_archive),
            },
        ],
    }
    (args.output_dir / "TOOL_LOCK.json").write_text(
        json.dumps(tool_lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"receipt": str(receipt_path), "packages": len(packages), "head": head}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
