"""Local tests for dispatch_r10.py - the two repairs, provable with NO live lane and NO network.

Run: C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -m pytest -q test_dispatch_r10.py
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("dispatch_r10", HERE / "dispatch_r10.py")
d10 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d10)

R9 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9")
REAL_RECEIPT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/lane_runs/"
                    "VERIFY_SECURITY_dispatch_receipt_attempt1.json")
REAL_BRIEF = R9 / "R9_VERIFIER_BRIEF.md"


def _receipt(tmp: Path, stdout_text: str, code="ERR_NO_ARM_EMITTED_NONCE", nonce_present=False) -> dict:
    so = tmp / "attempt-1-stdout.txt"
    so.write_text(stdout_text, encoding="utf-8", newline="\n")
    return {"schema": "HGK-LANE-RESOLUTION/1", "lane": "EXECUTE", "code": code,
            "used_rank": None, "used_transport_model": None, "nonce_absent_arms": ["opencode-go/deepseek-v4.1-flash"],
            "attempts": [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                          "exit": 0, "seconds": 512.0, "timed_out": False, "nonce_present": nonce_present,
                          "nonce_source": "item.completed/agent_message",
                          "stdout_path": str(so), "stdout_bytes": len(stdout_text.encode())}]}


def test_receipt_paths_are_per_turn_and_immutable():
    a = d10.receipt_paths("EXECUTE", "1", "20261016T130000Z")
    b = d10.receipt_paths("EXECUTE", "2", "20261016T130500Z")
    c = d10.receipt_paths("EXECUTE", "1", "20261016T131000Z")
    assert a["receipt"] != b["receipt"], "two turns of one lane must not share a receipt path"
    assert a["receipt"] != c["receipt"], "a second run of the same turn must not overwrite the first"
    assert "turn1" in a["receipt"] and "turn2" in b["receipt"]
    assert a["attempt_log_dir"] != b["attempt_log_dir"]


def test_extract_expected_nonce_from_a_brief():
    brief = "Ask the lane to echo `R9V-CHECKER-NONCE-5c1d84` as the first line and the last line.\n"
    assert d10.extract_expected_nonce(brief) == "R9V-CHECKER-NONCE-5c1d84"
    assert d10.extract_expected_nonce("no token here") is None


def test_attest_finds_the_nonce_in_a_surface_the_dispatcher_recorded(tmp_path):
    nonce = "R10X-WRITER-NONCE-abcdef"
    brief = f"echo `{nonce}` when done\n"
    receipt = _receipt(tmp_path, '{"type":"item.completed"}\n{"agent_message":"done ' + nonce + '"}\n')
    att = d10.attest(receipt, brief, [], str(tmp_path))
    assert att["verdict"] == "NONCE_PRESENT_DESPITE_DISPATCHER_CODE"
    assert len(att["nonce_found_in"]) == 1
    assert att["arms_from_attempts"][0]["model"] == "deepseek-v4.1-flash"
    assert att["dispatcher_claim"]["used_rank"] is None, "the null used_* fields must be reported as given"


def test_attest_reads_a_declared_artifact_root(tmp_path):
    nonce = "R10X-CHECKER-NONCE-123456"
    artifacts = tmp_path / "artifacts"
    (artifacts / "sub").mkdir(parents=True)
    (artifacts / "sub" / "DONE.txt").write_text(f"nonce: {nonce}\n", encoding="utf-8", newline="\n")
    receipt = _receipt(tmp_path, '{"type":"turn.completed"}\n')
    att = d10.attest(receipt, f"echo `{nonce}`\n", [str(artifacts)], str(tmp_path))
    assert att["verdict"] == "NONCE_PRESENT_DESPITE_DISPATCHER_CODE"
    assert att["nonce_found_in"][0]["path"].endswith("DONE.txt")


def test_attest_reports_absent_when_truly_absent(tmp_path):
    receipt = _receipt(tmp_path, '{"type":"turn.completed"}\n')
    att = d10.attest(receipt, "echo `R10X-ABSENT-NONCE-999999`\n", [], str(tmp_path))
    assert att["verdict"] == "NONCE_NOT_FOUND_IN_ANY_RECORDED_SURFACE"
    assert att["nonce_found_in"] == []


def test_attest_without_attempts_is_not_a_pass(tmp_path):
    receipt = {"lane": "EXECUTE", "code": "ERR_LANE_ALL_ROUTES_EXHAUSTED", "attempts": []}
    att = d10.attest(receipt, "echo `R10X-X-NONCE-1`\n", [], str(tmp_path))
    assert att["verdict"] == "NO_ATTEMPTS_RECORDED"
    assert "not an acceptance" in att["claim_ceiling"]


def test_recovery_on_the_REAL_r9_receipt_and_brief(tmp_path):
    """Regression against the real transcript of the R9 VERIFY turn: the defect and its repair, no live lane."""
    if not (REAL_RECEIPT.is_file() and REAL_BRIEF.is_file()):
        pytest.skip("the R9 receipt/brief are absent on this host; nothing to re-derive")
    receipt = json.loads(REAL_RECEIPT.read_text(encoding="utf-8"))
    att = d10.attest(receipt, REAL_BRIEF.read_text(encoding="utf-8"), [], str(tmp_path))
    assert receipt["code"] == "ERR_NO_ARM_EMITTED_NONCE"
    assert receipt["attempts"][0]["nonce_present"] is False
    assert att["verdict"] == "NONCE_PRESENT_DESPITE_DISPATCHER_CODE", \
        "the repair must find the nonce the dispatcher recorded as absent"
    assert att["expected_nonce_present_in_brief"] is True
    assert att["nonce_found_in"], "at least one recorded surface must carry it"


def test_snapshot_copies_receipt_and_attempt_log(tmp_path):
    receipt = tmp_path / "EXECUTE_turn1_x_dispatch_receipt.json"
    receipt.write_text("{}", encoding="utf-8")
    ald = tmp_path / "logs"
    ald.mkdir()
    (ald / "EXECUTE_turn1.attempts.ndjson").write_text('{"rank":1}\n', encoding="utf-8", newline="\n")
    snap = d10.snapshot(str(receipt), str(ald), str(tmp_path / "round"), "EXECUTE", "1", "20261016T130000Z")
    names = sorted(Path(c["to"]).name for c in snap["copied"])
    assert len(names) == 2
    assert any(n.endswith("_dispatch_receipt.json") for n in names)
    assert any(n.endswith(".ndjson") for n in names)
    for c in snap["copied"]:
        assert len(c["sha256"]) == 64
