"""M03 (round LANE-RELIABILITY-CLOSURE-20261016): the EFFORT axis of the pre-dispatch gate.

``scripts/runtime_role_binding_assert.py`` is the per-round role-mandate consumer: the owner order
names PLAN = ``gpt-6.1-sol`` MEDIUM and VERIFY/SECURITY = ``gpt-6.1-sol`` MEDIUM. Before this round
the script contained ZERO occurrences of ``effort``, so a lane served at a different reasoning effort
than the mandate declares was refused by NOTHING.

These tests drive the REAL script as a subprocess with synthetic mandate/pool fixtures -- the way the
dispatcher calls it -- and assert on the raw exit code and the typed code in stdout. They never import
the script and never assert on its source text.

Fixture shape: one lane (VERIFY_SECURITY) whose mandate declares ``medium`` and whose declared arm's
pool entry carries the effort under test. Every NEGATIVE asserts its OWN typed refusal code, and
``test_pos_matching_effort_passes`` is the POSITIVE CONTROL on the SAME fixture, so a refusal can
never pass for a reason other than the one the test names.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSERT = ROOT / "scripts" / "runtime_role_binding_assert.py"
TOOLCHAIN = ROOT / "config" / "hermes-codex-lane.json"
PY = sys.executable

PROVIDER = "openai-codex"
MODEL = "gpt-6.1-sol"


def _mandate(effort):
    role = {"provider": PROVIDER, "model": MODEL}
    if effort is not None:
        role["reasoning_effort"] = effort
    return {"schema": "HGK-ROLE-MANDATE/1", "round": "LANE-RELIABILITY-CLOSURE-20261016",
            "roles": {"VERIFY_SECURITY": role}}


def _pool(effort):
    entry = {"rank": 1, "provider": PROVIDER, "model": MODEL}
    if effort is not None:
        entry["reasoning_effort"] = effort
    return {"schema": "HGK-LANE-ROUTE-SLOTS/1",
            "lanes": [{"lane": "VERIFY_SECURITY", "ordered_pool": [entry]}]}


class LaneEffortEnforcement(unittest.TestCase):
    """One real assert-script subprocess per case; raw exit code + stdout are the oracle."""

    def _run(self, mandate_effort, pool_effort, served_effort=None):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-effort-", dir=str(ROOT.parent / "TEST_RESULTS")))
        mandate_file = tmp / "mandate.json"
        pool_file = tmp / "pool.json"
        mandate_file.write_text(json.dumps(_mandate(mandate_effort)), encoding="utf-8")
        pool_file.write_text(json.dumps(_pool(pool_effort)), encoding="utf-8")
        argv = [PY, "-B", str(ASSERT), "--mandate-file", str(mandate_file),
                "--lane", "VERIFY_SECURITY", "--pool", str(pool_file),
                "--toolchain-declaration", str(TOOLCHAIN)]
        if served_effort is not None:
            argv += ["--served-effort", served_effort]
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT),
                              timeout=300, check=False)
        try:
            body = json.loads(proc.stdout.strip().splitlines()[-1])
        except Exception:  # a non-JSON stdout is reported as-is, never masked
            body = {"raw_stdout_tail": proc.stdout[-400:]}
        return proc, body

    def test_pos_matching_effort_passes(self):
        """POSITIVE CONTROL: the same fixture the negatives use must SUCCEED."""
        proc, body = self._run("medium", "medium")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("declared_effort"), "medium")
        self.assertTrue(body.get("effort_verified"))

    def test_neg_mandate_effort_absent_from_pool_is_refused(self):
        proc, body = self._run("medium", None)
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL")

    def test_neg_effort_mismatch_is_refused(self):
        proc, body = self._run("medium", "high")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_MANDATE_EFFORT_MISMATCH")

    def test_neg_served_effort_without_a_mandate_effort_is_unverifiable(self):
        proc, body = self._run(None, None, served_effort="medium")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_SERVED_EFFORT_UNVERIFIABLE")

    def test_neg_served_effort_mismatch_is_refused(self):
        proc, body = self._run("medium", "medium", served_effort="high")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_SERVED_EFFORT_MISMATCH")

    def test_pos_lane_without_a_declared_effort_stays_a_pass_through(self):
        """The EXECUTE shape: a lane whose mandate names no effort is not silently failed."""
        proc, body = self._run(None, None)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(body.get("ok"))
        self.assertFalse(body.get("effort_verified"))


if __name__ == "__main__":
    unittest.main()
