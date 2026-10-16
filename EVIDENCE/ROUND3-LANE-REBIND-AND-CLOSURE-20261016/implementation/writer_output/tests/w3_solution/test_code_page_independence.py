"""Regression: child output bytes must not make the classifier code-page dependent.

The fixture stub emits a lone ``0xA4`` byte. That byte is a legal lead byte in
this host's legacy cp950 code page and is invalid as a UTF-8 start byte. The
preflight and toolchain captures must therefore pin UTF-8 with replacement
decoding instead of inheriting the ambient preferred encoding.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

from conftest import preflight
from lane_harness import write_declaration


pytestmark = pytest.mark.skipif(os.name != "nt", reason="needs a cmd.exe batch stub")

DECLARED_MODEL = "gpt-6.1-sol"
INVALID_UTF8 = bytes([0xA4])


def _write_byte_stub(tmp_path: Path) -> tuple[Path, str]:
    helper = tmp_path / "emit_codepage_bytes.py"
    helper.write_bytes(
        b"import sys\n"
        b"if '--version' in sys.argv:\n"
        b"    payload = b'codex-cli 9.9.9\\n' + bytes([0xA4]) + b'\\n'\n"
        b"else:\n"
        b"    payload = (b'OpenAI Codex v9.9.9\\n'\n"
        b"               b'model: gpt-6.1-sol\\n'\n"
        b"               b'provider: openai\\n'\n"
        b"               + bytes([0xA4]) + b'\\nOK\\n')\n"
        b"sys.stdout.buffer.write(payload)\n"
        b"sys.stdout.buffer.flush()\n"
    )
    stub = tmp_path / "codex-codepage-stub.bat"
    stub.write_text(
        "@echo off\r\n"
        f'"{sys.executable}" "{helper}" %*\r\n'
        "exit /b %ERRORLEVEL%\r\n",
        encoding="ascii",
    )
    return stub, hashlib.sha256(stub.read_bytes()).hexdigest().upper()


def test_invalid_utf8_child_bytes_do_not_change_preflight_classification(tmp_path):
    """A valid banner plus one invalid UTF-8 byte must still classify as LANE_OK."""
    stub, sha = _write_byte_stub(tmp_path)
    decl = write_declaration(tmp_path, stub, "9.9.9", sha)
    scratch = tmp_path / "scratch_outside"
    log = tmp_path / "out" / "preflight.log"
    receipt = tmp_path / "out" / "preflight.receipt.json"

    rc = preflight.main([
        "--model", DECLARED_MODEL,
        "--scratch", str(scratch),
        "--log", str(log),
        "--receipt", str(receipt),
        "--declaration", str(decl),
    ])

    assert rc == preflight.EXIT_OK
    doc = json.loads(receipt.read_text(encoding="utf-8"))
    assert doc["error_class"] == preflight.LANE_OK
    assert doc["served_model"] == DECLARED_MODEL
    assert "\ufffd" in doc["preflight_raw"]
    assert INVALID_UTF8.decode("cp950", errors="ignore") in doc["preflight_raw"]
