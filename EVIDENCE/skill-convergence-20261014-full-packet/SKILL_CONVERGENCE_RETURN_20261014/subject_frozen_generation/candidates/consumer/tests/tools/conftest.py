"""Candidate-first import harness (NON-APPLYABLE bootstrap).

Classified as harness/bootstrap, NOT part of the applyable write set
(tools/skill_manager_tool.py, tools/skill_manager_batch.py, tests/tools/*).

The candidate copy under test is only ``tools/skill_manager_tool.py`` and
``tools/skill_manager_batch.py``; every other module (``agent``,
``hermes_constants``, ``utils``, ``tools.registry``, ``tools.skill_usage`` ...)
is a read-only canonical dependency. This conftest puts the read-only runtime
root on ``sys.path`` and then pins the candidate ``tools`` package dir FIRST on
``tools.__path__`` so the suite provably loads the candidate module and never
the canonical original by accident.
"""

import hashlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATE_ROOT = os.path.dirname(os.path.dirname(_HERE))
_CANDIDATE_TOOLS = os.path.join(_CANDIDATE_ROOT, "tools")

# Read-only canonical dependency root (the live Hermes venv checkout).
_RUNTIME_ROOT = os.environ.get(
    "HERMES_SKCV_RUNTIME",
    r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0"
    r"\LocalCache\Local\hermes\hermes-agent",
)

if _RUNTIME_ROOT and _RUNTIME_ROOT not in sys.path:
    sys.path.insert(0, _RUNTIME_ROOT)

import tools  # noqa: E402  (resolved from the runtime root)

if _CANDIDATE_TOOLS not in tools.__path__:
    tools.__path__.insert(0, _CANDIDATE_TOOLS)


def _candidate_digest(rel_path: str) -> str:
    with open(os.path.join(_CANDIDATE_ROOT, rel_path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pytest_report_header(config):
    """Emit candidate import identity (paths + source digests) per the WO."""
    import tools.skill_manager_tool as _smt
    import tools.skill_manager_batch as _smb
    return [
        "SKCV candidate import identity:",
        f"  runtime_root = {_RUNTIME_ROOT}",
        f"  skill_manager_tool = {_smt.__file__}",
        f"  skill_manager_batch = {_smb.__file__}",
        f"  sha256 skill_manager_tool.py = {_candidate_digest('tools/skill_manager_tool.py')}",
        f"  sha256 skill_manager_batch.py = {_candidate_digest('tools/skill_manager_batch.py')}",
    ]
