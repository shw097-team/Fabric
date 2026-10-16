"""Shared test bootstrap for the W3 solution suite.

Two jobs, both required by the brief:

1. Load the candidate modules by ABSOLUTE PATH (never by the current working
   directory) so the suite passes when run from any directory.
2. Guarantee the suite writes NOTHING inside the tree under test AND nothing in
   the system temp dir. ``sys.dont_write_bytecode`` is set before the modules are
   loaded (so no ``__pycache__`` lands in ``scripts/``), and ``pytest_configure``
   redirects ``--basetemp`` / the cache to a CALLER-OWNED scratch root OUTSIDE the
   deliverable. The caller owns that root via ``HGK_SOLUTION_SCRATCH``; when it is
   not set we derive one NEXT TO the deliverable (a sibling, never inside it and
   never under the OS temp dir).

Scope note (repair leg 2, fixes F23/F24). This module keeps TWO distinct notions
that used to be one:

* ``REPO_ROOT`` (derived from ``__file__``, parents[2]) is where the *frozen
  landing* lives. It is used ONLY to locate ``SCRIPTS`` / ``FIXTURES`` / the
  scratch sibling, never as a subject to walk.
* ``SUBJECT_FILES`` names the bounded *subject*: the delivered file set this
  change is about. Tests materialize it with ``lane_harness.copy_deliverable``
  and walk THAT copy, never ``REPO_ROOT``. The repository is huge, contains live
  agent-home paths under ``var/...``, and exceeds the Windows legacy path limit
  with LongPathsEnabled=0, so walking it as a subject is slow and fails outright.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

# Suppress bytecode BEFORE importing anything from the tree under test.
sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

# The bounded SUBJECT: the delivered file set (relative to the deliverable root).
# This is the ONLY thing the suite may treat as "the thing under test"; a test
# that needs to walk or bind a subject materializes exactly these files with
# ``lane_harness.copy_deliverable`` and hashes that bounded copy.
SUBJECT_FILES = (
    "scripts/lane_launcher.sh",
    "scripts/hgk-lane-toolchain.py",
    "scripts/hgk-lane-preflight.py",
)

# Import-time guard (W3 layout repair): the suite now lives two levels below the
# repo root (``tests/w3_solution/``), so ``REPO_ROOT`` must resolve to the
# repo root (``parents[2]``) for ``SCRIPTS`` to reach ``scripts/`` and for
# ``FIXTURES`` to reach the moved ``fixtures/``. Fail loudly at import, and print
# both resolved roots so the working invocation is visible in the raw output.
assert SCRIPTS.is_dir(), f"SCRIPTS is not an existing directory: {SCRIPTS}"
assert FIXTURES.is_dir(), f"FIXTURES is not an existing directory: {FIXTURES}"
print(f"[w3_solution] REPO_ROOT={REPO_ROOT}")
print(f"[w3_solution] SCRIPTS={SCRIPTS}")
print(f"[w3_solution] FIXTURES={FIXTURES}")


def scratch_root() -> Path:
    """The caller-owned scratch root: OUTSIDE the deliverable and OUTSIDE the OS
    temp dir. ``HGK_SOLUTION_SCRATCH`` overrides; otherwise a sibling of the
    deliverable (``<round>/scratch-w3/``) is used."""
    env = os.environ.get("HGK_SOLUTION_SCRATCH")
    if env:
        root = Path(env)
    else:
        root = REPO_ROOT.parent / "scratch-w3"
    root.mkdir(parents=True, exist_ok=True)
    return root


def _is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def pytest_configure(config):
    """Force every pytest temp/cache write OUTSIDE the tree under test.

    A caller may pass ``--basetemp`` (or ``PYTEST_ADDOPTS``) that resolves inside
    the deliverable OR under the system temp dir; both are redirected to a fresh
    caller-owned directory."""
    base = scratch_root() / "pytest"
    base.mkdir(parents=True, exist_ok=True)
    config.option.basetemp = str(base)
    config.option.cache_dir = str(base / "cache")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


toolchain = _load("hgk_lane_toolchain", SCRIPTS / "hgk-lane-toolchain.py")
preflight = _load("hgk_lane_preflight", SCRIPTS / "hgk-lane-preflight.py")


# ---- fixture provenance helpers -------------------------------------------

def fixture_lines(fixture_name: str) -> list[str]:
    """Raw lines (without trailing newline) of a fixture, 1-indexed by list pos."""
    text = (FIXTURES / fixture_name).read_text(encoding="utf-8")
    return text.splitlines()


def line_at(fixture_name: str, line_no: int) -> str:
    """The exact literal at ``line_no`` (1-indexed) of a fixture."""
    return fixture_lines(fixture_name)[line_no - 1]


def provenance(fixture_name: str, line_no: int) -> str:
    """A 'file:line' provenance label pointing at the recorded source."""
    return f"{fixture_name}:{line_no}"
