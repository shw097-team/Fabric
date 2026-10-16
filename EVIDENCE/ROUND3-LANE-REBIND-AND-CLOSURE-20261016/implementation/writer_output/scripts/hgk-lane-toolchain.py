#!/usr/bin/env python3
"""T1 - canonical lane-toolchain resolver.

Resolves the lane's Codex CLI binary from ONE declared identity: a declared
absolute ``codex_executable`` path, an expected ``codex_version`` string and an
expected ``codex_sha256``. It never searches PATH, never calls ``find`` or
``command -v``, and carries no hard-coded fallback binary path.

Prints ``path``, ``sha256`` and ``version`` (as a JSON document on stdout, plus a
one-line human summary on stderr). Fails closed with a typed non-zero exit and a
message that NAMES the offending build (path + version) when the resolved
build's version OR digest differs from the declared one.

Modes / invocation forms
  --resolve [DECLARATION]   print the identity JSON (exit 0 only when ok)
  --verify  [DECLARATION]   same computation, fail closed on any mismatch
  --check-bin [DECLARATION] print just the resolved binary path (for callers)

The declaration may be given positionally (the documented form) or with an
explicit ``--declaration``. When neither is given the default is
``<repo>/config/hermes-codex-lane.json``, discovered by walking up from this
file's own location (never from the current working directory).

Typed errors (non-zero exit; machine-readable JSON on stdout):
  ERR_LANE_TOOLCHAIN_DECLARATION_MISSING   exit 2
  ERR_LANE_TOOLCHAIN_BINARY_MISSING        exit 3
  ERR_LANE_TOOLCHAIN_VERSION_MISMATCH      exit 4
  ERR_LANE_TOOLCHAIN_DIGEST_MISMATCH       exit 5

Read-only: this script writes nothing anywhere.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ERR_DECLARATION_MISSING = "ERR_LANE_TOOLCHAIN_DECLARATION_MISSING"
ERR_BINARY_MISSING = "ERR_LANE_TOOLCHAIN_BINARY_MISSING"
ERR_VERSION_MISMATCH = "ERR_LANE_TOOLCHAIN_VERSION_MISMATCH"
ERR_DIGEST_MISMATCH = "ERR_LANE_TOOLCHAIN_DIGEST_MISMATCH"

EXIT_OK = 0
EXIT_DECLARATION_MISSING = 2
EXIT_BINARY_MISSING = 3
EXIT_VERSION_MISMATCH = 4
EXIT_DIGEST_MISMATCH = 5

# The Codex CLI prints ``codex-cli <semver>`` for ``--version``; a few builds
# print a bare semver. Require a semver-shaped token so unrelated x.y.z text in
# other output is not mistaken for the build's self-reported version.
_VERSION_RE = re.compile(
    r"codex-cli\s+([0-9]+\.[0-9]+\.[0-9]+[0-9A-Za-z.+\-]*)",
    re.IGNORECASE,
)
_BARE_VERSION_RE = re.compile(r"([0-9]+\.[0-9]+\.[0-9]+[0-9A-Za-z.+\-]*)")

# Relative location of the declaration inside the product root.
_DECLARATION_RELATIVE = ("config", "hermes-codex-lane.json")


def default_declaration_path() -> Path:
    """``<product-root>/config/hermes-codex-lane.json`` from this file's location.

    Walk up from the script's own directory and return the first ancestor that
    actually contains the declaration. This is location-derived (never the
    current working directory) and survives being copied to a different depth.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent.joinpath(*_DECLARATION_RELATIVE)
        if candidate.is_file():
            return candidate
    # No ancestor carries the declaration (e.g. a detached copy): return the
    # would-be location under the nearest plausible root so the caller gets the
    # typed DECLARATION_MISSING error instead of a silent success.
    parents = here.parents
    root = parents[3] if len(parents) > 3 else here.parent
    return root.joinpath(*_DECLARATION_RELATIVE)


def sha256_of(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk_size), b""):
            h.update(block)
    return h.hexdigest().upper()


def measure_version(exe: Path, timeout: int = 30) -> str | None:
    """Ask the binary for its own version. ``None`` when it cannot be measured."""
    try:
        proc = subprocess.run(
            [str(exe), "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    match = _VERSION_RE.search(text) or _BARE_VERSION_RE.search(text)
    return match.group(1) if match else None


def load_declaration(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(declaration_path: Path, version_timeout: int = 30) -> tuple[dict, int]:
    """Compute the identity record. Returns ``(record, exit_code)``.

    Fail-closed ordering: declaration present and readable -> declared binary
    present -> version matches the declaration -> digest matches the
    declaration. Every failure names the offending build (path + measured
    version) in ``detail``.
    """
    record: dict = {
        "declaration_path": str(declaration_path),
        "declared_path": None,
        "declared_version": None,
        "declared_sha256": None,
        "path": None,
        "version": None,
        "sha256": None,
        "ok": False,
        "error": None,
        "detail": None,
    }

    if not declaration_path.is_file():
        record["error"] = ERR_DECLARATION_MISSING
        record["detail"] = f"declaration file not found: {declaration_path}"
        return record, EXIT_DECLARATION_MISSING

    try:
        declaration = load_declaration(declaration_path)
    except (OSError, ValueError) as exc:
        record["error"] = ERR_DECLARATION_MISSING
        record["detail"] = f"declaration unreadable or invalid JSON: {exc}"
        return record, EXIT_DECLARATION_MISSING

    declared_path = declaration.get("codex_executable")
    declared_version = declaration.get("codex_version")
    declared_sha256 = declaration.get("codex_sha256")
    record["declared_path"] = declared_path
    record["declared_version"] = declared_version
    record["declared_sha256"] = declared_sha256

    if not declared_path:
        record["error"] = ERR_DECLARATION_MISSING
        record["detail"] = "declaration has no codex_executable field"
        return record, EXIT_DECLARATION_MISSING

    exe = Path(declared_path)
    record["path"] = str(exe)

    if not exe.is_file():
        record["error"] = ERR_BINARY_MISSING
        record["detail"] = f"declared binary does not exist: {exe}"
        return record, EXIT_BINARY_MISSING

    measured_version = measure_version(exe, timeout=version_timeout)
    measured_sha = sha256_of(exe)
    record["version"] = measured_version
    record["sha256"] = measured_sha

    if measured_version is None:
        record["error"] = ERR_VERSION_MISMATCH
        record["detail"] = (
            f"could not measure --version of offending build "
            f"path={exe} measured_version=<unmeasurable> declared={declared_version!r}"
        )
        return record, EXIT_VERSION_MISMATCH

    if measured_version != declared_version:
        record["error"] = ERR_VERSION_MISMATCH
        record["detail"] = (
            f"offending build path={exe} version={measured_version!r} "
            f"!= declared_version={declared_version!r}"
        )
        return record, EXIT_VERSION_MISMATCH

    if declared_sha256 is None or measured_sha != str(declared_sha256).upper():
        record["error"] = ERR_DIGEST_MISMATCH
        record["detail"] = (
            f"offending build path={exe} version={measured_version!r} "
            f"sha256={measured_sha} != declared_sha256={declared_sha256}"
        )
        return record, EXIT_DIGEST_MISMATCH

    record["ok"] = True
    return record, EXIT_OK


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--resolve", action="store_true", help="print identity JSON")
    group.add_argument("--verify", action="store_true", help="fail closed on mismatch")
    group.add_argument(
        "--check-bin",
        action="store_true",
        help="print only the resolved binary path on stdout (for callers)",
    )
    parser.add_argument(
        "--declaration",
        default=None,
        help="path to hermes-codex-lane.json (default: <root>/config/hermes-codex-lane.json)",
    )
    parser.add_argument(
        "declaration_positional",
        nargs="?",
        default=None,
        metavar="DECLARATION",
        help="declaration path given positionally (documented invocation form)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.declaration and args.declaration_positional:
        parser.error(
            "give the declaration either positionally or with --declaration, not both"
        )

    declared = args.declaration or args.declaration_positional
    declaration_path = Path(declared) if declared else default_declaration_path()

    record, code = resolve(declaration_path)

    if args.check_bin:
        if code == EXIT_OK:
            print(record["path"])
        return code

    print(json.dumps(record, indent=2))
    if code == EXIT_OK:
        print(
            f"OK: path={record['path']} sha256={record['sha256']} "
            f"version={record['version']}",
            file=sys.stderr,
        )
    else:
        print(f"{record['error']}: {record['detail']}", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
