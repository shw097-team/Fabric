"""M11 (+ M17 reinforcement): the mandatory tool guard's FAIL-CLOSED contract.

The guard is now ACTIVE in the governed profile, so every one of its refusal paths is a
production path: a fault in the controller must refuse the call, never silently allow it.
These cases drive ``mandatory_tool_guard.check_tool_call`` against stub controllers that
behave badly on purpose -- the guard is judged on what it does when the boundary is broken,
not when it works.

M11: hook missing / exception / timeout / malformed  => governed FAIL-CLOSED.
M17: no ``governed_runtime`` in the profile          => ordinary behaviour, allowed.

The guard module is resolved relative to this file's repo root (``<root>/hermes/agent``), so
the same suite runs in the candidate tree and in a frozen copy. ``HERMES_AGENT_SRC`` overrides.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _guard_path() -> pathlib.Path:
    """Locate ``mandatory_tool_guard.py`` regardless of which tree this suite is running in.

    Three layouts are real on this host: the candidate tree and a frozen copy place the guard at
    ``<root>/hermes/agent/`` beside the hgk repo, while the DEPLOYED product keeps it inside the
    Hermes install (``<HERMES_HOME>/hermes-agent/agent/``). Resolving only the first makes the suite
    pass in the candidate tree and fail to import once applied -- exactly the mistake this function
    must not repeat.
    """
    override = os.environ.get("HERMES_AGENT_SRC")
    if override:
        return pathlib.Path(override) / "agent" / "mandatory_tool_guard.py"
    candidates = [ROOT.parent / "hermes" / "agent" / "mandatory_tool_guard.py"]
    home = os.environ.get("HERMES_HOME")
    if home:
        candidates.append(pathlib.Path(home) / "hermes-agent" / "agent" / "mandatory_tool_guard.py")
    candidates.append(pathlib.Path(
        r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local"
        r"\hermes\hermes-agent\agent\mandatory_tool_guard.py"))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise unittest.SkipTest(
        "mandatory_tool_guard.py not found in any known layout; set HERMES_AGENT_SRC")


def _load_guard():
    spec = importlib.util.spec_from_file_location("hgk_guard_under_test", _guard_path())
    module = importlib.util.module_from_spec(spec)
    sys.modules["hgk_guard_under_test"] = module
    spec.loader.exec_module(module)
    return module


class Agent:
    """Minimal stand-in for the agent object the guard reads attributes off."""

    session_id = "sess-m11"
    session_cwd = "C:/somewhere/else"
    _current_turn_id = "turn-1"
    _current_api_request_id = "req-1"


class GuardFailClosed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard = _load_guard()
        cls.tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m11-"))
        cls.roots = [str(cls.tmp)]

    def _run(self, controller_body: str, *, timeout=5, binding=None):
        """Write a stub controller, point the binding at it, and call the guard once."""
        script = self.tmp / "controller_stub.py"
        script.write_text(controller_body, encoding="utf-8")
        raw = binding if binding is not None else {
            "protected_roots": self.roots,
            "controller_command": [sys.executable, str(script)],
            "timeout_seconds": timeout,
        }
        with mock.patch.object(self.guard, "_load_config", return_value={"governed_runtime": raw}):
            return self.guard.check_tool_call(Agent(), "write_file", {"path": str(self.tmp / "x.py")})

    # M11 -- every broken-boundary case must REFUSE, never return None (None means "allowed").
    def test_controller_nonzero_exit_refuses(self):
        block = self._run("import sys; sys.exit(7)")
        self.assertEqual(block, "mandatory_guard_controller_failed", block)

    def test_controller_exception_refuses(self):
        block = self._run("raise SystemExit(1)")
        self.assertEqual(block, "mandatory_guard_controller_failed", block)

    def test_controller_malformed_json_refuses(self):
        block = self._run("print('not json at all')")
        self.assertEqual(block, "mandatory_guard_controller_malformed", block)

    def test_controller_non_object_json_refuses(self):
        block = self._run("print('[1,2,3]')")
        self.assertEqual(block, "mandatory_guard_controller_malformed", block)

    def test_controller_silent_refuses(self):
        """Exit 0 with empty stdout is NOT an allow."""
        block = self._run("pass")
        self.assertEqual(block, "mandatory_guard_controller_malformed", block)

    def test_missing_controller_command_refuses(self):
        raw = {"protected_roots": self.roots,
               "controller_command": [str(self.tmp / "does-not-exist-xyz.exe")],
               "timeout_seconds": 5}
        block = self._run("pass", binding=raw)
        self.assertIsNotNone(block, "a missing controller must refuse, not allow")
        self.assertTrue(str(block).startswith("mandatory_guard_controller_error"), block)

    def test_controller_timeout_refuses(self):
        block = self._run("import time; time.sleep(30)", timeout=1)
        self.assertIsNotNone(block, "a hung controller must refuse, not allow")
        self.assertTrue(str(block).startswith("mandatory_guard_controller_error"), block)

    def test_deny_action_returns_a_named_block(self):
        block = self._run("import json; print(json.dumps({'action':'deny','reason':'maker-write'}))")
        self.assertEqual(block, "mandatory_guard_denied: maker-write", block)

    def test_allow_action_is_the_only_allow(self):
        block = self._run("import json; print(json.dumps({'action':'allow'}))")
        self.assertIsNone(block, block)

    def test_unknown_action_refuses(self):
        block = self._run("import json; print(json.dumps({'action':'maybe'}))")
        self.assertTrue(str(block).startswith("mandatory_guard_denied"), block)

    # Binding validation: a present-but-invalid binding must refuse (never silently empty roots).
    def test_empty_protected_roots_refuses(self):
        raw = {"protected_roots": [], "controller_command": [sys.executable, "-c", "print('{}')"],
               "timeout_seconds": 5}
        self.assertEqual(self._run("pass", binding=raw), "mandatory_guard_invalid_binding")

    def test_non_list_protected_roots_refuses(self):
        raw = {"protected_roots": "C:/x", "controller_command": [sys.executable, "-c", "print('{}')"],
               "timeout_seconds": 5}
        self.assertEqual(self._run("pass", binding=raw), "mandatory_guard_invalid_binding")

    def test_relative_protected_root_refuses(self):
        raw = {"protected_roots": ["relative/path"], "controller_command": [sys.executable, "-c", "print('{}')"],
               "timeout_seconds": 5}
        self.assertEqual(self._run("pass", binding=raw), "mandatory_guard_invalid_binding")

    def test_timeout_above_ceiling_refuses(self):
        raw = {"protected_roots": self.roots, "controller_command": [sys.executable, "-c", "print('{}')"],
               "timeout_seconds": 999}
        self.assertEqual(self._run("pass", binding=raw), "mandatory_guard_invalid_binding")

    def test_non_positive_timeout_refuses(self):
        raw = {"protected_roots": self.roots, "controller_command": [sys.executable, "-c", "print('{}')"],
               "timeout_seconds": 0}
        self.assertEqual(self._run("pass", binding=raw), "mandatory_guard_invalid_binding")

    def test_non_mapping_binding_refuses(self):
        self.assertEqual(self._run("pass", binding=["not", "a", "mapping"]),
                         "mandatory_guard_invalid_binding")

    # The guard's stated contract: a CONFIGURED profile always asks the controller, even when the
    # cwd is outside the protected roots (a bound/resumed session may retain obligations).
    def test_configured_profile_always_consults_the_controller(self):
        calls = []
        body = ("import sys, json\n"
                "open(r'" + str(self.tmp / 'was-called.flag') + "', 'a').close()\n"
                "print(json.dumps({'action':'allow'}))\n")
        self.assertIsNone(self._run(body))
        self.assertTrue((self.tmp / "was-called.flag").is_file(),
                        "the controller must be consulted even with a cwd outside the roots")

    # M17 -- no governed_runtime => ordinary behaviour.
    def test_absent_binding_allows(self):
        for cfg in ({}, {"model": {"default": "x"}}):
            with mock.patch.object(self.guard, "_load_config", return_value=cfg):
                self.assertIsNone(self.guard.check_tool_call(Agent(), "write_file", {"path": "/x"}))

    def test_config_error_refuses(self):
        with mock.patch.object(self.guard, "_load_config", side_effect=RuntimeError("boom")):
            block = self.guard.check_tool_call(Agent(), "write_file", {"path": "/x"})
        self.assertTrue(str(block).startswith("mandatory_guard_config_error"), block)


if __name__ == "__main__":
    unittest.main()
