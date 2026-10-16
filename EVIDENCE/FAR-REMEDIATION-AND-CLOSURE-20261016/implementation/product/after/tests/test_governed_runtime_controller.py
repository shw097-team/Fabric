"""P2b: behavioral tests for the governed-runtime controller adapter.

The controller (``scripts/hgk-governed-runtime-controller.py``) is the thin JSON-stdin adapter the
Hermes ``mandatory_tool_guard.check_tool_call`` contract calls: it reads a JSON payload on stdin and
answers with a single JSON object on stdout, allowing ONLY on exit 0 with ``{"action":"allow"}``.

These tests drive the REAL script as a subprocess against a throwaway Shared Spine (exactly the way
the guard invokes it) and assert on the raw exit code + stdout. They never import the controller and
never assert on its source text.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTROLLER = ROOT / "scripts" / "hgk-governed-runtime-controller.py"
HGK_PY = pathlib.Path(
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
    r"hermes-agent/venv/Scripts/python.exe"
)

sys.path.insert(0, str(ROOT / "src"))
from hg_kseos import role_binding  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402

BASE = "903e47cddeceb40cb8f5f5793105533b3988a463"
WO = "WO-LANE-ENFORCE-20261015-BUILD"


def _binding(session, wo):
    return {
        "schema": role_binding.ROLE_BINDING_SCHEMA,
        "round": "LANE-ENFORCEMENT-APPLY-20261015",
        "session": session,
        "workorder": wo,
        "base_head": BASE,
        "subject": "hgk/src/hg_kseos/role_binding.py",
        "scope": ["hgk/src/hg_kseos/role_binding.py"],
        "expiry": "2099-01-01T00:00:00+00:00",
        "mandate_digest": "sha256:" + hashlib.sha256(b"mandate").hexdigest(),
        "roles": {"EXECUTE": {"provider": "opencode-go", "model": "deepseek-v4.1-flash",
                              "surface": "codex-cli", "rank": 1}},
    }


class GovernedRuntimeController(unittest.TestCase):
    """One real controller subprocess per case; raw exit + stdout are the oracle."""

    def _workspace(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-grc-", dir=str(ROOT.parent / "TEST_RESULTS")))
        protected = tmp / "protected"
        protected.mkdir()
        hermes_home = tmp / "hermes_home"
        hermes_home.mkdir()
        (hermes_home / "config.yaml").write_text(
            "governed_runtime:\n"
            "  controller_command: [python, controller.py]\n"
            "  timeout_seconds: 5\n"
            "  protected_roots:\n"
            f"    - {protected.as_posix()}\n",
            encoding="utf-8",
        )
        return tmp, protected, hermes_home

    def _seed_spine(self, tmp, specs):
        """One FROZEN requirement + one ADMITTED TaskSpec/WorkOrder per (ts, wo, session, roles)."""
        spine_db = tmp / "spine.db"
        spine = SharedSpine(spine_db)
        spine.initialize()
        spine.create_project()
        spine.register_requirement("REQ-GRC", "src#1", "controller", "ACC-GRC", "oracle", "t", "neg")
        spine.acquire_lease("REQ-GRC", "maker", "tok")
        spine.transition_requirement("REQ-GRC", "FROZEN", "maker", "tok", 0, "E1", "K1")
        for i, (ts, wo, session, roles) in enumerate(specs):
            doc = _binding(session, wo)
            doc["roles"] = roles
            spine.create_taskspec(ts, "REQ-GRC", "do", "maker", tmp,
                                  {role_binding.ROLE_BINDING_KEY: doc}, ["unit"], "evidence")
            spine.create_workorder(wo, ts, f"writer-{i}", tmp, BASE)
        return spine_db

    def _run(self, payload, spine_db, hermes_home):
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(spine_db)
        env["HGK_SPINE_SCHEMA"] = str(ROOT / "src" / "hg_kseos" / "schema.sql")
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        return subprocess.run(
            [str(HGK_PY), str(CONTROLLER)],
            input=body, capture_output=True,
            cwd=str(ROOT), env=env, timeout=120, check=False,
        )

    def _payload(self, function_name, function_args, session_id, hermes_home):
        return {
            "session_id": session_id,
            "session_cwd": str(ROOT),
            "turn_id": "turn-1",
            "api_request_id": "req-1",
            "function_name": function_name,
            "function_args": function_args,
            "hermes_home": str(hermes_home),
        }

    def _json(self, proc):
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return json.loads(proc.stdout.decode("utf-8"))

    def test_pos_ordinary_read_allowed(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [])
        proc = self._run(self._payload("read_file", {"path": str(protected / "x.py")},
                                       "sess-read", home), db, home)
        self.assertEqual(self._json(proc)["action"], "allow")
        self.assertEqual(proc.returncode, 0)

    def test_pos_non_governed_session_write_allowed(self):
        tmp, protected, home = self._workspace()
        # A live governed round exists for a DIFFERENT session; this session is unbound -> ordinary.
        db = self._seed_spine(tmp, [("TS-OTHER", "WO-OTHER", "sess-other",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")},
                                       "sess-unbound", home), db, home)
        self.assertEqual(self._json(proc)["action"], "allow")

    def test_neg_maker_write_inside_protected_denied(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")},
                                       "sess-maker", home), db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny")
        self.assertEqual(proc.returncode, 0)
        self.assertIn(WO, body["reason"])

    def test_neg_maker_terminal_mentioning_protected_root_denied(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        cmd = f"copy /Y nada.txt {protected.as_posix()}/x.py"
        proc = self._run(self._payload("terminal", {"command": cmd}, "sess-maker", home), db, home)
        self.assertEqual(self._json(proc)["action"], "deny")

    def test_pos_write_outside_protected_allowed(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        outside = "C:/definitely-outside-any-root/nope.txt"
        proc = self._run(self._payload("write_file", {"path": outside}, "sess-maker", home), db, home)
        self.assertEqual(self._json(proc)["action"], "allow")

    def test_neg_malformed_stdin_nonzero_and_not_bare_allow(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [])
        proc = self._run(b"{ this is not json", db, home)
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(proc.stdout.decode("utf-8", "replace").strip(), '{"action":"allow"}')

    def test_pos_checker_write_allowed(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-C", "WO-CHK", "sess-checker",
                                     {"VERIFY_SECURITY": {"provider": "p", "model": "m",
                                                          "surface": "s", "rank": 2}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")},
                                       "sess-checker", home), db, home)
        self.assertEqual(self._json(proc)["action"], "allow")


    def test_neg_maker_relative_path_under_protected_cwd_denied(self):
        """A relative target written from a protected cwd resolves INTO the protected root."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        payload = self._payload("write_file", {"path": "x.py"}, "sess-maker", home)
        payload["session_cwd"] = protected.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"relative path escaped: {body}")
        self.assertIn(WO, body["reason"])

    def test_neg_maker_dotdot_escape_to_protected_denied(self):
        """`outside/../protected/x.py` normalizes INTO the protected root and must be denied."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        outside = protected.parent / "outside"
        outside.mkdir()
        sneaky = f"{outside.as_posix()}/../protected/x.py"
        payload = self._payload("write_file", {"path": sneaky}, "sess-maker", home)
        payload["session_cwd"] = protected.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"dotdot path escaped: {body}")
        self.assertIn(WO, body["reason"])


    def test_neg_maker_terminal_relative_write_under_protected_cwd_denied(self):
        """A free-text shell write from a protected cwd cannot be path-resolved; it must fail CLOSED."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        payload = self._payload("terminal", {"command": "echo x > x.py"}, "sess-maker", home)
        payload["session_cwd"] = protected.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"free-text relative write escaped: {body}")
        self.assertIn(WO, body["reason"])

    def test_neg_maker_execute_code_under_protected_cwd_denied(self):
        """Inline code from a protected cwd is likewise unresolvable and must fail CLOSED."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        payload = self._payload("execute_code", {"code": "open('x.py','w').write('x')"}, "sess-maker", home)
        payload["session_cwd"] = protected.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"inline code escaped: {body}")
        self.assertIn(WO, body["reason"])


    def test_neg_maker_terminal_relative_from_parent_cwd_denied(self):
        """Free text cannot be path-resolved: a relative destination reaches the root from its PARENT."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        payload = self._payload("terminal", {"command": f"echo x > {protected.name}/x.py"}, "sess-maker", home)
        payload["session_cwd"] = protected.parent.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"parent-cwd free-text escaped: {body}")
        self.assertIn(WO, body["reason"])

    def test_neg_maker_execute_code_relative_from_parent_cwd_denied(self):
        """Same for inline code: an unresolvable write from the root's parent must fail CLOSED."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m", "surface": "s", "rank": 1}})])
        payload = self._payload("execute_code",
                                {"code": f"open('{protected.name}/x.py','w').write('x')"}, "sess-maker", home)
        payload["session_cwd"] = protected.parent.as_posix()
        proc = self._run(payload, db, home)
        body = self._json(proc)
        self.assertEqual(body["action"], "deny", f"parent-cwd inline code escaped: {body}")
        self.assertIn(WO, body["reason"])


    def test_pos_absent_session_id_is_answered_not_an_outage(self):
        """CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED: a blank session id must be ANSWERED.

        The guard sends ``getattr(agent,"session_id","") or ""``; ``find_session_binding`` refuses a
        blank id by design, and mapping that to exit 3 made the guard refuse EVERY mutating call for
        any agent without a session id. This case asserts the ANSWER and its OWN reason string.
        POSITIVE CONTROL on the SAME fixture: ``test_neg_maker_write_inside_protected_denied``
        presents a REAL session id and must still deny.
        """
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")}, "", home),
                         db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")

    def test_pos_null_session_id_is_answered_not_an_outage(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")}, None, home),
                         db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")

    def test_pos_absent_session_id_free_text_is_answered_not_an_outage(self):
        """The unresolvable free-text class is answered the same way, not turned into a refusal."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("terminal", {"command": "echo x > x.py"}, "", home), db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")


if __name__ == "__main__":
    unittest.main()
