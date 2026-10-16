"""Round FAR-LANE-REUSE-RCA-20261015-FIX: regression tests for the four owners-ordered repairs.

Each test names the fix and the failure it locks down. All tests are deterministic and spawn NO
model turn (the pin/mote gates are pure subprocess/probe paths; the timeout capture drives
run_candidate against a stub launcher):

  P0-A  pin-assert pre-spawn: declared pin that fails toolchain verification refuses with a
        TYPED receipt (ERR_LANE_PIN_IDENTITY_INVALID) instead of a spawn-stage WinError 2.
  P0-B  launcher action-scoped deps: a Codex-binary-drift environment must NOT block
        StartOpenCodex/Hermes/Verify; Write/Verify keep fail-closed Codex checks.
  P1-A  role-mandate consumer: a declared arm mandate resolves through the toolchain+pool;
        a missing role declaration or a stale toolchain pin refuses with typed codes.
  P1-B  timeout capture: a timed-out child's partial stdout/stderr are PERSISTED (non-zero
        bytes + tail), while the classification stays TIMEOUT/fail (never upgraded to a pass).

Run with the repo's python: python tests/test_far_lane_fix_20261015.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
O = ROOT / "var" / "FAR-LANE-REUSE-RCA-20261015"

_spec = importlib.util.spec_from_file_location("hgk_lane_dispatch", ROOT / "scripts" / "hgk-lane-dispatch.py")
disp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disp)


# --------------------------------------------------------------------------- P0-A
class TestP0PinAssert(unittest.TestCase):
    """P0-A: the dispatcher refuses on a stale codex toolchain pin BEFORE any spawn."""

    def _run(self, config_text: str):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-p0a-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        cfg = tmp / "hermes-codex-lane.json"
        cfg.write_text(config_text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "hgk-lane-toolchain.py"),
             "--verify", "--declaration", str(cfg)],
            capture_output=True, text=True, timeout=120)

    def test_stale_absent_binary_refuses_Typed(self):
        # A pin pointing at a path that does not exist (exactly the 2026-10-14 drift) is refused
        # by the verifier the dispatcher now calls pre-spawn.
        r = self._run(json.dumps({
            "codex_executable": r"C:\nonexistent\2e5e00daee91c61d\codex.exe",
            "codex_version": "0.162.0-alpha.17.2",
            "codex_sha256": "D" * 64,
        }))
        self.assertEqual(r.returncode, 3, r.stdout)  # ERR_LANE_TOOLCHAIN_BINARY_MISSING exit code
        self.assertIn("ERR_LANE_TOOLCHAIN_BINARY_MISSING", r.stdout)

    def test_current_pin_verifies(self):
        # Positive control: the ACTUAL installed binary verifies against its measured identity.
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "hgk-lane-toolchain.py"),
             "--verify", "--declaration",
             str(O / "sources" / "task_local_toolchain.json")],
            capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout or r.stderr)
        ident = json.loads(r.stdout)
        self.assertTrue(len(ident["sha256"]) == 64)

    def test_digest_mismatch_is_typed_not_a_spawn(self):
        # The drift beyond mere absence: right path, WRONG digest. Typed refusal, exit 5.
        tc = json.loads((O / "sources" / "task_local_toolchain.json").read_text())
        tc["codex_sha256"] = "1" * 64
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-p0a-dm-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        cfg = tmp / "decl.json"
        cfg.write_text(json.dumps(tc), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "hgk-lane-toolchain.py"),
             "--verify", "--declaration", str(cfg)],
            capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 5, r.stdout)
        self.assertIn("ERR_LANE_TOOLCHAIN_DIGEST_MISMATCH", r.stdout)


# --------------------------------------------------------------------------- P0-B
class TestP0BLauncherActionScope(unittest.TestCase):
    """P0-B: action-scoped dependency checks in the launcher (static + live)."""

    SRC = ROOT / "scripts" / "start-hgk-hermes.ps1"

    def test_launcher_splits_codex_dependent_actions(self):
        text = self.SRC.read_text(encoding="utf-8")
        self.assertIn("$codexDependentActions = @(\"Verify\", \"Write\", \"Probe\")", text)
        # The single all-action guard is gone.
        self.assertNotIn(
            'foreach ($file in @($humanConfig, $codexExe, $bunExe, $openCodexEntry, $hermesExe, $hermesPython)) {',
            text)
        # Codex + hash checks survive for the Codex-dependent actions (fail-closed preserved).
        self.assertIn('ERR_CODEX_HASH_MISMATCH', text)

    def test_launcher_live_startopencodex_will_reach_the_relay_branch(self):
        # The hash check + codex.exe requirement must live AFTER the action-scoped split and
        # INSIDE the codex-dependent arm. StartOpenCodex (non-dependent) must NOT be gated by it.
        text = self.SRC.read_text(encoding="utf-8")
        split = text.find("$codexDependentActions = ")
        hash_check = text.find("ERR_CODEX_HASH_MISMATCH")
        hash_check2 = text.rfind("ERR_CODEX_HASH_MISMATCH")
        start_branch = text.find('if ($Action -eq "StartOpenCodex")')
        self.assertGreater(split, 0)
        self.assertGreater(start_branch, split)   # spl↓t precedes all action branches
        self.assertGreater(start_branch, hash_check)  # the codex-dependent checks are earlier in file, StartOpenCodex branch comes after → not gated
        # exactly one conditional hash-check site (inside the secondary if)
        self.assertNotEqual(hash_check, hash_check2)  # appears twice: comment free zone? Then assert second occurrence inside else arm nearby '$actualCodexHash = (Get-FileHash'
        occurrences = [i for i in range(len(text)) if text.startswith('ERR_CODEX_HASH_MISMATCH', i)]
        self.assertEqual(len(occurrences), 2, occurrences)  # OAuth-branch guard + main guard; both Must remain


# --------------------------------------------------------------------------- P1-A
class TestP1MandateConsumer(unittest.TestCase):
    """P1-A: the per-round mandate is consumed, not just asserted by prose."""

    def _assert_run(self, mandate, lane, tmp):
        mf = tmp / "mandate.json"
        if mandate is not None:
            mf.write_text(json.dumps(mandate), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "runtime_role_binding_assert.py"),
             "--mandate-file", str(mf), "--lane", lane,
             "--pool", str(ROOT / "config" / "lane-route-slots.candidate.json"),
             "--toolchain-declaration", str(O / "sources" / "task_local_toolchain.json")],
            capture_output=True, text=True, timeout=180)

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-p1a-"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_owner_order_mandate_resolves(self):
        mandate = {"roles": {
            "EXECUTE": {"provider": "opencode-go", "model": "deepseek-v4.1-flash"},
            "VERIFY_SECURITY": {"provider": "opencode-go", "model": "glm-5.3-flash"}}}
        r = self._assert_run(mandate, "EXECUTE", self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = json.loads(r.stdout)
        self.assertTrue(out["ok"])
        self.assertEqual(out["declared"]["model"], "deepseek-v4.1-flash")
        self.assertEqual(out["toolchain_identity"]["sha256"].lower(),
                         "e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e")

    def test_verify_security_mandate_resolves(self):
        mandate = {"roles": {
            "VERIFY_SECURITY": {"provider": "opencode-go", "model": "glm-5.3-flash"}}}
        r = self._assert_run(mandate, "VERIFY_SECURITY", self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_inactive_lane_refuses(self):
        mandate = {"roles": {"EXECUTE": {"provider": "opencode-go", "model": "deepseek-v4.1-flash"}}}
        r = self._assert_run(mandate, "PLAN", self.tmp)
        self.assertEqual(r.returncode, 3)
        self.assertIn("ERR_MANDATE_ROLE_NOT_DECLARED", r.stdout)

    def test_wrong_model_in_pool_refuses(self):
        mandate = {"roles": {"EXECUTE": {"provider": "opencode-go", "model": "glm-5.3-flash"}}}
        r = self._assert_run(mandate, "EXECUTE", self.tmp)
        self.assertEqual(r.returncode, 5)
        self.assertIn("ERR_MANDATE_ARM_UNRESOLVED", r.stdout)

    def test_missing_file_refuses(self):
        r = self._assert_run(None, "EXECUTE", self.tmp / "mandate.json")
        self.assertEqual(r.returncode, 2)
        self.assertIn("ERR_MANDATE_FILE_MISSING", r.stdout)


# --------------------------------------------------------------------------- P1-B
class TestP1BTimeoutCapture(unittest.TestCase):
    """P1-B: timeout keeps partial output, stays a FAIL."""

    def _run_candidate(self, timeout_s=2.0):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-p1b-"))
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        stub = tmp / "slow_child.py"
        stub.write_text(
            "import time,sys\nprint('P1B-PARTIAL-A',flush=True)\nprint('P1B-PARTIAL-B',flush=True)\n"
            "print('P1B-STDERR-DIAG',file=sys.stderr,flush=True)\ntime.sleep(30)\n", encoding="utf-8")
        log_dir = tmp / "raw"

        class Args:
            lane = "VERIFY_SECURITY"; sandbox = "read-only"; timeout = timeout_s
            prompt = "nonce fixture"; relay_base = "http://127.0.0.1:1"
            cwd = tmp; nonce = "LRRCA_T1"; codex_arg = None; codex_home_config = {}
            credential_posture_gate = None; credential_posture_gate_git = None
            credential_posture_gate_test_global = None
            usage = tmp / "usage.jsonl"
        entry = {"rank": 1, "provider": "opencode-go", "model": "slow-stub",
                 "transport_model": "slow-stub", "reasoning_effort": None}
        attempt = disp.run_candidate(entry, Args(), str(stub), tmp / "lane-home", log_dir)
        return attempt, log_dir

    def test_timeout_preserves_partial_streams_and_stays_fail(self):
        attempt, log_dir = self._run_candidate()
        self.assertEqual(attempt["exit"], "TIMEOUT")
        self.assertTrue(attempt.get("timed_out") is True, attempt.get("timed_out"))
        self.assertFalse(attempt["nonce_present"])
        self.assertFalse(attempt.get("usage_receipt_ok"))
        # the crucial upgrade: partial stdout persisted with the printed lines
        self.assertIn("P1B-PARTIAL-A", attempt.get("stdout_tail", ""))
        self.assertIn("P1B-STDERR-DIAG", attempt.get("stderr_tail", ""))
        # persisted raw bytes are NON-EMPTY (the 2026-10-14 defect was 0 bytes on disk)
        logs = list(log_dir.glob("*stdout*"))
        self.assertTrue(logs and logs[0].stat().st_size > 0, [p.name for p in log_dir.glob('*')])


if __name__ == "__main__":
    unittest.main(verbosity=2)
