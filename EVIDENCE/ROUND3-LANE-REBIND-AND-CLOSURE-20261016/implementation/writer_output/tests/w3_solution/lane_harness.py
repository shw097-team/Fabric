"""Shared harness for the launcher/substitution tests.

Builds a throwaway deliverable tree (a copy of scripts/) and stub Codex binaries
so no test touches the real deliverable, the real Codex binary, a real model, the
relay, or the developer's Codex home.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

from conftest import REPO_ROOT, SCRIPTS, SUBJECT_FILES


def find_git_bash() -> str | None:
    for cand in (
        Path(r"C:\Program Files\Git\usr\bin\bash.exe"),
        Path(r"C:\Program Files\Git\bin\bash.exe"),
    ):
        if cand.is_file():
            return str(cand)
    return shutil.which("bash")


GIT_BASH = find_git_bash()


def posix(path) -> str:
    if os.name == "nt":
        cyg = shutil.which("cygpath")
        if cyg:
            return subprocess.run([cyg, "-u", str(path)], capture_output=True,
                                  text=True, encoding="utf-8",
                                  errors="replace").stdout.strip()
    return str(path)


def copy_deliverable(dest: Path) -> Path:
    """Copy the bounded delivered file set into a disposable deliverable tree.

    ``SUBJECT_FILES`` (from ``conftest``) names exactly the delivered files, so
    the copy IS the bounded subject: small, free of the live agent-home paths and
    long paths that make a repository-wide walk fail on Windows.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for rel in SUBJECT_FILES:
        src = REPO_ROOT / rel
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return dest


def _batch_echo_lines(body: str) -> list[str]:
    lines = []
    for line in body.splitlines():
        escaped = line.replace("^", "^^").replace("&", "^&").replace("|", "^|")
        escaped = escaped.replace("<", "^<").replace(">", "^>")
        lines.append("echo " + escaped)
    return lines


def write_stub(dest: Path, *, version: str, body: str, exit_code: int,
               preflight_body: str | None = None,
               preflight_exit_code: int | None = None,
               preflight_marker: str | None = None) -> tuple[Path, str]:
    """Write a .bat stub whose --version prints ``codex-cli <version>`` and whose
    exec prints ``body`` then exits ``exit_code``. Returns (path, sha256).

    When ``preflight_body`` is supplied, the stub emits that body instead for the
    short preflight invocation. ``preflight_marker`` is the substring the launcher
    includes only in the preflight command line (the scratch path).
    """
    stub = dest / "codex-stub.bat"
    lines = [
        "@echo off",
        'if "%1"=="--version" (echo codex-cli ' + version + ' & exit /b 0)',
    ]
    # Body lines are ECHOED (not executed): the stub stands in for the CLI's
    # captured stdout/stderr. Batch metacharacters are escaped so the literal
    # text survives.
    if preflight_body is not None:
        if not preflight_marker:
            raise ValueError("preflight_marker is required with preflight_body")
        marker = preflight_marker.replace('"', '""')
        lines.append('set "ARGS=%*"')
        lines.append(f'echo %ARGS% | findstr /C:"{marker}" >nul')
        lines.append("if not errorlevel 1 goto preflight_body")
        lines.extend(_batch_echo_lines(body))
        lines.append(f"exit /b {exit_code}")
        lines.append(":preflight_body")
        lines.extend(_batch_echo_lines(preflight_body))
        if preflight_exit_code is None:
            preflight_exit_code = exit_code
        lines.append(f"exit /b {preflight_exit_code}")
    else:
        lines.extend(_batch_echo_lines(body))
        lines.append(f"exit /b {exit_code}")
    stub.write_text("\r\n".join(lines) + "\r\n", encoding="ascii")
    sha = hashlib.sha256(stub.read_bytes()).hexdigest().upper()
    return stub, sha


def write_declaration(dest: Path, exe: Path, version: str, sha: str) -> Path:
    import json
    decl = dest / "declaration.json"
    decl.write_text(json.dumps({
        "codex_executable": str(exe),
        "codex_version": version,
        "codex_sha256": sha,
    }), encoding="utf-8")
    return decl


def run_launcher(*, deliverable: Path, lane, model, effort, brief: Path, log: Path,
                 declaration: Path, scratch_base: Path, extra_env=None):
    env = {**os.environ}
    env["HGK_LANE_PYTHON"] = sys.executable
    env["HGK_LANE_DECLARATION"] = str(declaration)
    env["HGK_LANE_SCRATCH"] = str(scratch_base)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [GIT_BASH, posix(deliverable / "scripts" / "lane_launcher.sh"),
         lane, model, effort, posix(brief), posix(log)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env,
    )


def run_preflight_script(deliverable: Path, *args) -> subprocess.CompletedProcess:
    """Run the BOUNDED copy's own preflight entry point as a script.

    Because the script is executed from inside the disposable deliverable copy,
    its location-derived ``default_subject_root()`` IS that bounded copy - never
    the repository root. No ``--subject-root`` override is needed (and none may
    narrow the derived root, by design).
    """
    cmd = [
        sys.executable,
        str(deliverable / "scripts" / "hgk-lane-preflight.py"),
        *(str(a) for a in args),
    ]
    return subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def tree_sha256_map(root: Path, exclude=()) -> dict:
    """sha256 of every file under ``root`` (excluding names in ``exclude``)."""
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(root))
            if any(rel == e or rel.startswith(e) for e in exclude):
                continue
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out
