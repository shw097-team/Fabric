"""T5 - additive receipt schema; an existing consumer matching the OLD fallback
code keeps working."""

import json

from conftest import preflight


DECLARED_MODEL = "gpt-6.1-sol"

ADDITIVE_FIELDS = (
    "codex_cli",
    "codex_cli_version",
    "declared_model",
    "served_model",
    "error_class",
    "preflight_raw",
)


def _toolchain_record():
    record, code = preflight._toolchain.resolve(preflight._toolchain.default_declaration_path())
    assert code == 0, record
    return record


def _old_fallback_consumer(doc) -> str:
    """A stand-in for the EXISTING consumer: it reads the receipt and maps the
    pre-existing fallback code (``LANE_MODEL_REFUSED``) to a decision. It must
    keep working against the new, additive receipt."""
    return {"LANE_MODEL_REFUSED": "OPEN_DEVIATION"}.get(
        doc.get("error_class"), "NO_DEVIATION"
    )


def test_preflight_receipt_carries_all_additive_fields(tmp_path, monkeypatch):
    """A real preflight run (spawn stubbed IN-PROCESS) writes a receipt carrying
    every additive field; served_model is set, and null when no turn served."""
    record = _toolchain_record()
    scratch = tmp_path / "scratch_outside"
    log = tmp_path / "out" / "preflight.log"
    receipt = tmp_path / "out" / "preflight.receipt.json"
    seed = tmp_path / "auth.json"
    seed.write_text('{"token":"PLACEHOLDER-NOT-A-REAL-CREDENTIAL"}', encoding="utf-8")

    real_run = preflight.subprocess.run

    def fake_run(cmd, **kwargs):
        class P:
            returncode = 0
            stdout = f"OpenAI Codex v{record['version']}\nmodel: {DECLARED_MODEL}\nprovider: fake\nOK\n"
            stderr = ""
        return P() if "exec" in cmd else real_run(cmd, **kwargs)

    monkeypatch.setattr(preflight.subprocess, "run", fake_run)
    rc = preflight.main([
        "--model", DECLARED_MODEL, "--scratch", str(scratch),
        "--log", str(log), "--receipt", str(receipt), "--seed-auth", str(seed),
    ])
    assert rc == 0
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    for field in ADDITIVE_FIELDS:
        assert field in doc, f"receipt must carry additive field {field}"
    assert doc["declared_model"] == DECLARED_MODEL
    assert doc["served_model"] == DECLARED_MODEL
    assert doc["error_class"] == preflight.LANE_OK
    assert doc["codex_cli"] == record["path"]
    assert doc["codex_cli_version"] == record["version"]
    assert "OpenAI Codex v" in doc["preflight_raw"]


def test_served_model_is_null_when_no_turn_is_served(tmp_path):
    """A toolchain-unresolved run writes served_model=null (no turn served)."""
    bad_decl = tmp_path / "bad.json"
    bad_decl.write_text(json.dumps({
        "codex_executable": str(tmp_path / "nope" / "codex.exe"),
        "codex_version": "0.0.0",
        "codex_sha256": "0" * 64,
    }), encoding="utf-8")
    scratch = tmp_path / "scratch_outside"
    log = tmp_path / "out" / "preflight.log"
    receipt = tmp_path / "out" / "preflight.receipt.json"
    rc = preflight.main([
        "--model", DECLARED_MODEL, "--scratch", str(scratch),
        "--log", str(log), "--receipt", str(receipt), "--declaration", str(bad_decl),
    ])
    assert rc == preflight.EXIT_TOOLCHAIN_UNRESOLVED
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["served_model"] is None
    for field in ADDITIVE_FIELDS:
        assert field in doc


def test_old_fallback_consumer_keeps_working_on_the_new_receipt(tmp_path):
    """Additive only: a consumer matching the OLD fallback code is unaffected by
    the new fields. The old code (LANE_MODEL_REFUSED) still decides."""
    old_receipt = {"error_class": "LANE_MODEL_REFUSED"}          # pre-change shape
    new_receipt = dict(old_receipt)
    # Additive means NEW keys are added; a key already present (error_class) keeps
    # its value. Simulate the real receipt: the new fields appear alongside it.
    new_receipt.update({f: None for f in ADDITIVE_FIELDS if f not in old_receipt})
    assert _old_fallback_consumer(old_receipt) == "OPEN_DEVIATION"
    assert _old_fallback_consumer(new_receipt) == "OPEN_DEVIATION"
    # and a non-refusal still maps to NO_DEVIATION
    assert _old_fallback_consumer({"error_class": "LANE_TOOLCHAIN_MISMATCH"}) == "NO_DEVIATION"
