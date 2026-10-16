"""T7/T8 - served-vs-declared identity assertion on the LONG lane.

Deterministic, model-free tests. The stub returns a clean preflight banner for the
short preflight turn and a chosen long-lane banner for the real lane so the
assertion itself is what decides the result.
"""

import json
from pathlib import Path

import pytest

from conftest import preflight
from lane_harness import (
    GIT_BASH,
    copy_deliverable,
    run_launcher,
    write_declaration,
    write_stub,
)


pytestmark = pytest.mark.skipif(not GIT_BASH, reason="needs a POSIX shell (git-bash)")

DECLARED_MODEL = "gpt-6.1-sol"
OLDER_MODEL = "gpt-5.6-sol"


def _banner(model: str) -> str:
    return "\n".join([
        "OpenAI Codex v9.9.9",
        "--------",
        "workdir: C:\\scratch",
        f"model: {model}",
        "provider: openai",
        "approval: never",
        "sandbox: read-only",
        "reasoning effort: medium",
        "reasoning summaries: none",
        "session id: 00000000-0000-0000-0000-000000000000",
        "--------",
    ])


def _preflight_body() -> str:
    return _banner(DECLARED_MODEL) + "\nuser\nReply with exactly OK\n\ncodex\nOK\n"


def _setup(tmp_path, *, lane_body: str, lane_exit_code: int = 0):
    deliverable = copy_deliverable(tmp_path / "deliverable")
    scratch_base = tmp_path / "scratch_base"
    stub, sha = write_stub(
        tmp_path / "deliverable",
        version="9.9.9",
        body=lane_body,
        exit_code=lane_exit_code,
        preflight_body=_preflight_body(),
        preflight_marker=str(scratch_base / "identity-lane"),
    )
    decl = write_declaration(tmp_path / "deliverable", stub, "9.9.9", sha)
    brief = tmp_path / "brief.md"
    brief.write_text("Reply with exactly OK\n", encoding="utf-8")
    log = tmp_path / "out" / "lane.log"
    return deliverable, decl, brief, log, scratch_base


def test_primary_acceptance_long_lane_mismatch_fails_closed_with_receipt(tmp_path):
    """Owner amendment 01: long lane exits 0 but its banner says the older model."""
    deliverable, decl, brief, log, scratch_base = _setup(
        tmp_path,
        lane_body=_banner(OLDER_MODEL) + "\nuser\nwork\n\ncodex\nDONE\n",
    )
    proc = run_launcher(
        deliverable=deliverable,
        lane="identity-lane",
        model=DECLARED_MODEL,
        effort="medium",
        brief=brief,
        log=log,
        declaration=decl,
        scratch_base=scratch_base,
    )

    assert proc.returncode == 98, proc.stderr
    assert "ERR_LANE_MODEL_IDENTITY_MISMATCH" in proc.stderr
    assert f"declared={DECLARED_MODEL}" in proc.stderr
    assert f"served={OLDER_MODEL}" in proc.stderr

    receipt = Path(str(log) + ".identity.receipt.json")
    assert receipt.exists(), proc.stderr
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["identity_ok"] is False
    assert doc["status"] == "IDENTITY_MISMATCH"
    assert doc["declared_model"] == DECLARED_MODEL
    assert doc["served_model"] == OLDER_MODEL
    assert doc["error_class"] == "ERR_LANE_MODEL_IDENTITY_MISMATCH"
    assert doc["extraction"] == "anchored_startup_banner_only"


def test_negative_control_body_mentions_older_model_but_banner_matches_passes(tmp_path):
    """A body mention must never satisfy or break the identity assertion."""
    body_mentions = "\n".join(
        f"body note {i}: model: {OLDER_MODEL}" for i in range(12)
    )
    deliverable, decl, brief, log, scratch_base = _setup(
        tmp_path,
        lane_body=(
            _banner(DECLARED_MODEL)
            + "\nuser\nwrite notes\n\ncodex\n"
            + body_mentions
            + "\nuser\n"
            + "\n".join(f"model: {OLDER_MODEL}" for _ in range(8))
            + "\ncodex\nDONE\n"
        ),
    )
    proc = run_launcher(
        deliverable=deliverable,
        lane="identity-lane",
        model=DECLARED_MODEL,
        effort="medium",
        brief=brief,
        log=log,
        declaration=decl,
        scratch_base=scratch_base,
    )

    assert proc.returncode == 0, proc.stderr
    receipt = Path(str(log) + ".identity.receipt.json")
    assert receipt.exists(), proc.stderr
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["identity_ok"] is True
    assert doc["status"] == "IDENTITY_OK"
    assert doc["declared_model"] == DECLARED_MODEL
    assert doc["served_model"] == DECLARED_MODEL


def test_vacuous_pass_control_unreadable_banner_fails_closed(tmp_path):
    """A clean exit with no readable banner must not count as identity OK."""
    deliverable, decl, brief, log, scratch_base = _setup(
        tmp_path,
        lane_body="user\nno banner here\n\ncodex\nDONE\n",
    )
    proc = run_launcher(
        deliverable=deliverable,
        lane="identity-lane",
        model=DECLARED_MODEL,
        effort="medium",
        brief=brief,
        log=log,
        declaration=decl,
        scratch_base=scratch_base,
    )

    assert proc.returncode == 98, proc.stderr
    assert "ERR_LANE_MODEL_IDENTITY_MISMATCH" in proc.stderr
    assert f"declared={DECLARED_MODEL}" in proc.stderr
    assert "served=UNREADABLE" in proc.stderr

    receipt = Path(str(log) + ".identity.receipt.json")
    assert receipt.exists(), proc.stderr
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["identity_ok"] is False
    assert doc["status"] == "IDENTITY_UNREADABLE"
    assert doc["served_model"] is None
    assert doc["error_class"] == "ERR_LANE_MODEL_IDENTITY_MISMATCH"


def test_extract_banner_model_ignores_agent_body_model_lines():
    """T8 unit: only the first CLI startup banner is authoritative."""
    lines = (
        _banner(DECLARED_MODEL)
        + "\nuser\n"
        + "\n".join(f"model: {OLDER_MODEL}" for _ in range(10))
        + "\ncodex\nDONE\n"
    ).splitlines()
    assert preflight.extract_banner_model(lines) == DECLARED_MODEL
    assert preflight.served_from_header(lines)[0] == DECLARED_MODEL


def test_extract_banner_model_absent_returns_none():
    lines = ["model: gpt-5.6-sol", "provider: openai", "user", "model: gpt-6.1-sol"]
    assert preflight.extract_banner_model(lines) is None
    assert preflight.served_from_header(lines)[0] is None
