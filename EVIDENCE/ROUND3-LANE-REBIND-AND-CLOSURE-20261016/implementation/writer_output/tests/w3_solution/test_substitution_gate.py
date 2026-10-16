"""T4.3 - the substitution gate: refused under MISMATCH, permitted under
MODEL_REFUSED. Uses stubbed binaries only (no network, no real model)."""

import json
import os
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

MISMATCH_BODY = "\n".join([
    "2026-10-12T04:18:08.297877Z ERROR codex_models_manager::cache: "
    "failed to load models cache: missing field `supports_parallel_tool_calls` "
    "at line 139 column 5",
    "OpenAI Codex v9.9.9",
    "model: gpt-6.1-sol",
    "provider: openai",
    "warning: Model metadata for `gpt-6.1-sol` not found. Defaulting to fallback metadata.",
    'ERROR: {"type":"error","status":400,"error":{"type":"invalid_request_error",'
    '"message":"The \'gpt-6.1-sol\' model is not supported when using Codex with a ChatGPT account."}}',
])

REFUSED_BODY = "\n".join([
    "OpenAI Codex v9.9.9",
    "model: gpt-6.1-sol",
    "provider: openai",
    'ERROR: {"type":"error","status":403,"error":{"type":"invalid_request_error",'
    '"message":"The gpt-6.1-sol model is not supported when using Codex with a ChatGPT account."}}',
])


def _setup(tmp_path, body, exit_code):
    deliverable = copy_deliverable(tmp_path / "deliverable")
    stub, sha = write_stub(tmp_path / "deliverable", version="9.9.9", body=body,
                           exit_code=exit_code)
    decl = write_declaration(tmp_path / "deliverable", stub, "9.9.9", sha)
    brief = tmp_path / "brief.md"
    brief.write_text("Reply with exactly OK\n", encoding="utf-8")
    log = tmp_path / "out" / "lane.log"
    scratch_base = tmp_path / "scratch_base"
    return deliverable, decl, brief, log, scratch_base


def test_mismatch_refuses_to_substitute_and_writes_no_deviation(tmp_path):
    deliverable, decl, brief, log, scratch_base = _setup(tmp_path, MISMATCH_BODY, 1)
    proc = run_launcher(deliverable=deliverable, lane="mismatch-lane",
                        model=DECLARED_MODEL, effort="medium", brief=brief, log=log,
                        declaration=decl, scratch_base=scratch_base)
    assert proc.returncode == 91, proc.stderr
    assert "LANE_TOOLCHAIN_MISMATCH" in proc.stderr
    # names the offending build
    assert "codex-stub.bat" in proc.stderr
    assert not Path(str(log) + ".model-deviation-required.json").exists()
    assert not log.exists(), "the long lane must NOT run on a toolchain mismatch"


def test_model_refused_may_open_a_declared_deviation_with_receipt_fields(tmp_path):
    deliverable, decl, brief, log, scratch_base = _setup(tmp_path, REFUSED_BODY, 1)
    proc = run_launcher(deliverable=deliverable, lane="refused-lane",
                        model=DECLARED_MODEL, effort="medium", brief=brief, log=log,
                        declaration=decl, scratch_base=scratch_base)
    assert proc.returncode == 92, proc.stderr
    assert "LANE_MODEL_REFUSED" in proc.stderr
    record = Path(str(log) + ".model-deviation-required.json")
    assert record.exists(), proc.stderr
    doc = json.loads(record.read_text(encoding="utf-8"))
    assert doc["class"] == "LANE_MODEL_REFUSED"
    # the deviation record carries the T2 receipt fields
    for key in ("codex_cli", "codex_cli_version", "declared_model", "served_model",
                "error_class", "preflight_raw"):
        assert key in doc, f"deviation record must carry {key}"
    assert doc["declared_model"] == DECLARED_MODEL
    assert doc["error_class"] == "LANE_MODEL_REFUSED"
    assert not log.exists(), "the long lane must NOT run inline on a refusal"


def test_resolver_failure_refuses_before_any_deviation_or_lane(tmp_path):
    deliverable = copy_deliverable(tmp_path / "deliverable")
    stub, sha = write_stub(tmp_path / "deliverable", version="9.9.9",
                           body="OpenAI Codex v9.9.9\nmodel: gpt-6.1-sol\nprovider: openai\nOK\n",
                           exit_code=0)
    # Declaration with the WRONG digest forces a typed resolver failure.
    decl = write_declaration(tmp_path / "deliverable", stub, "9.9.9", "0" * 64)
    brief = tmp_path / "brief.md"
    brief.write_text("Reply with exactly OK\n", encoding="utf-8")
    log = tmp_path / "out" / "lane.log"
    scratch_base = tmp_path / "scratch_base"
    proc = run_launcher(deliverable=deliverable, lane="bad-decl", model=DECLARED_MODEL,
                        effort="medium", brief=brief, log=log, declaration=decl,
                        scratch_base=scratch_base)
    assert proc.returncode == 90, proc.stderr
    assert "ERR_LANE_TOOLCHAIN" in proc.stderr
    assert not Path(str(log) + ".model-deviation-required.json").exists()
    assert not log.exists()
    assert not scratch_base.exists(), "a resolver failure must not create the scratch"

