"""T4.1 - resolver: a matching declared identity resolves; a mismatch fails closed."""

import ast
import json
import subprocess
import sys

from conftest import SCRIPTS, toolchain


def _measured():
    record, code = toolchain.resolve(toolchain.default_declaration_path())
    assert code == 0, record
    return record


def _write_declaration(tmp_path, **overrides):
    base = {
        "codex_executable": _measured()["path"],
        "codex_version": _measured()["version"],
        "codex_sha256": _measured()["sha256"],
    }
    base.update(overrides)
    path = tmp_path / "hermes-codex-lane.json"
    path.write_text(json.dumps(base), encoding="utf-8")
    return path


def test_matching_identity_resolves_and_prints_path_sha_version():
    record, code = toolchain.resolve(toolchain.default_declaration_path())
    assert code == 0
    assert record["ok"] is True
    assert record["path"] and record["sha256"] and record["version"]
    assert record["version"] == record["declared_version"]
    assert record["sha256"] == record["declared_sha256"].upper()


def test_version_mismatch_fails_closed_and_names_offending_build(tmp_path):
    decl = _write_declaration(tmp_path, codex_version="0.0.0-alpha.0")
    record, code = toolchain.resolve(decl)
    assert code == toolchain.EXIT_VERSION_MISMATCH
    assert record["error"] == toolchain.ERR_VERSION_MISMATCH
    # The offending build is named by path + version.
    assert record["path"] in record["detail"]
    assert "0.0.0-alpha.0" in record["detail"]


def test_digest_mismatch_fails_closed_and_names_offending_build(tmp_path):
    decl = _write_declaration(tmp_path, codex_sha256="0" * 64)
    record, code = toolchain.resolve(decl)
    assert code == toolchain.EXIT_DIGEST_MISMATCH
    assert record["error"] == toolchain.ERR_DIGEST_MISMATCH
    assert record["path"] in record["detail"]
    assert record["version"] in record["detail"]


def test_missing_declaration_and_binary_fail_closed(tmp_path):
    record, code = toolchain.resolve(tmp_path / "absent.json")
    assert code == toolchain.EXIT_DECLARATION_MISSING
    assert record["error"] == toolchain.ERR_DECLARATION_MISSING

    decl = _write_declaration(tmp_path, codex_executable=str(tmp_path / "nope" / "codex.exe"))
    record, code = toolchain.resolve(decl)
    assert code == toolchain.EXIT_BINARY_MISSING
    assert record["error"] == toolchain.ERR_BINARY_MISSING


def test_cli_accepts_positional_declaration_and_typed_exit_codes(tmp_path):
    decl = _write_declaration(tmp_path, codex_sha256="0" * 64)
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "hgk-lane-toolchain.py"), "--verify", str(decl)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(tmp_path),
    )
    assert proc.returncode == toolchain.EXIT_DIGEST_MISMATCH, proc.stderr
    assert toolchain.ERR_DIGEST_MISMATCH in proc.stdout


def test_cli_check_bin_prints_only_the_path(tmp_path):
    decl = _write_declaration(tmp_path)
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "hgk-lane-toolchain.py"), "--check-bin", str(decl)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(tmp_path),
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == _measured()["path"]


def test_resolver_and_callers_do_no_find_or_path_search():
    """No `find` / `command -v` / PATH search anywhere in the resolver source."""
    text = (SCRIPTS / "hgk-lane-toolchain.py").read_text(encoding="utf-8")
    tree = ast.parse(text)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    # No PATH/env discovery helpers and no hard-coded fallback path.
    assert "shutil" not in imported
    assert "os" not in imported
    # No discovery invocation in code: assert on the AST, not on docstring prose
    # (the module docstring legitimately says it "never calls command -v").
    module_docstring_node = (
        tree.body[0].value if tree.body and isinstance(tree.body[0], ast.Expr) else None
    )
    code_strings = [
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
        and node is not module_docstring_node
    ]
    assert not any(("command -v" in s) or ("shutil.which" in s) for s in code_strings)
    strings = [
        node.value for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]
    assert not any("codex.exe" in s.lower() for s in strings)

