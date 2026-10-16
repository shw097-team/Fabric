"""Tranche A/B: role-binding enforcement + typed role-evidence completion consumer.

These are BEHAVIORAL tests. They exercise the real pre-spawn rejection of the dispatcher (a typed
refusal + NO spawn, asserted end-to-end) and the real typed ``record_workorder_result`` consumer in a
temporary SQLite spine. They never call a live model and never assert on source text.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
HGK_PY = pathlib.Path(
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
    r"hermes-agent/venv/Scripts/python.exe"
)
_spec = importlib.util.spec_from_file_location("hgk_lane_dispatch", ROOT / "scripts" / "hgk-lane-dispatch.py")
disp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disp)

sys.path.insert(0, str(ROOT / "src"))
from hg_kseos import role_binding  # noqa: E402
from hg_kseos.errors import InvariantViolation  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402

REAL_POOL = ROOT / "config" / "lane-route-slots.candidate.json"
ROUND = "LANE-ENFORCEMENT-APPLY-20261015"
SESSION = "20261015_092659_25bac4"
WO = "WO-LANE-ENFORCE-20261015-BUILD"
BASE = "903e47cddeceb40cb8f5f5793105533b3988a463"
SUBJECT = "hgk/src/hg_kseos/role_binding.py"
EXPIRY = "2099-01-01T00:00:00+00:00"


def _mandate_digest() -> str:
    return "sha256:" + hashlib.sha256(b"mandate").hexdigest()


def _binding(**over) -> dict:
    doc = {
        "schema": role_binding.ROLE_BINDING_SCHEMA,
        "round": ROUND,
        "session": SESSION,
        "workorder": WO,
        "base_head": BASE,
        "subject": SUBJECT,
        "scope": ["hgk/src/hg_kseos/role_binding.py", "hgk/scripts/hgk-lane-dispatch.py"],
        "expiry": EXPIRY,
        "mandate_digest": _mandate_digest(),
        "roles": {
            "EXECUTE": {"provider": "opencode-go", "model": "deepseek-v4.1-flash",
                        "surface": "codex-cli", "rank": 1, "reasoning_effort": "medium"},
            "VERIFY_SECURITY": {"provider": "opencode-go", "model": "glm-5.3-flash",
                                "surface": "codex-cli", "rank": 2},
            "PLAN": {"provider": "openai-codex", "model": "gpt-6.1-sol",
                     "surface": "Hermes-internal", "rank": 1, "reasoning_effort": "medium"},
        },
    }
    doc.update(over)
    return doc


def _evidence(**over) -> dict:
    doc = {
        "workorder": WO, "session": SESSION, "round": ROUND, "subject": SUBJECT,
        "mandate_digest": _mandate_digest(), "role": "VERIFY_SECURITY", "surface": "codex-cli",
        "artifact_digest": "sha256:" + hashlib.sha256(b"artifact").hexdigest(),
        "checker_identity": "codex-cli-independent-glm", "guard": "CLEAN",
        "lane_receipt": {"ok": True, "code": None, "served_arm": "opencode-go/glm-5.3-flash",
                         "receipt_path": "TEST_RESULTS/verify.receipt.json",
                         "receipt_digest": "sha256:" + hashlib.sha256(b"receipt").hexdigest()},
        "log_refs": [{"path": "TEST_RESULTS/verify.stdout.txt",
                      "sha256": hashlib.sha256(b"stdout").hexdigest()}],
    }
    doc.update(over)
    return doc


class PureValidator(unittest.TestCase):
    def test_negative_no_empty_input_pass(self):
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.validate_binding(None)
        self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_MISSING")

    def test_negative_each_missing_field_refuses(self):
        for field in role_binding.REQUIRED_BINDING_FIELDS:
            doc = _binding()
            doc.pop(field)
            with self.assertRaises(role_binding.BindingError, msg=field):
                role_binding.validate_binding(doc)

    def test_negative_bad_expiry(self):
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.validate_binding(_binding(expiry="2000-01-01T00:00:00+00:00"))
        self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_EXPIRED")
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_binding(_binding(expiry="not-a-date"))

    def test_negative_wrong_session_round_wo_subject_surface(self):
        cases = [
            ({"session": "other-session"}, "ERR_ROLE_BINDING_SESSION_MISMATCH"),
            ({"round": "other-round"}, "ERR_ROLE_BINDING_ROUND_MISMATCH"),
            ({"workorder_id": "WO-OTHER"}, "ERR_ROLE_BINDING_WORKORDER_MISMATCH"),
            ({"subject": "other-subject"}, "ERR_ROLE_BINDING_SUBJECT_MISMATCH"),
        ]
        for kw, code in cases:
            with self.assertRaises(role_binding.BindingError, msg=kw) as ctx:
                role_binding.validate_binding(_binding(), lane="EXECUTE", **kw)
            self.assertEqual(ctx.exception.code, code)
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.validate_binding(_binding(), lane="EXECUTE", surface="Hermes-internal")
        self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_SURFACE_MISMATCH")
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_binding(_binding(), lane="EXECUTE", model="gpt-6.1-sol")

    def test_positive_resolves_arm_and_rank_from_same_binding(self):
        out = role_binding.validate_binding(_binding(), lane="EXECUTE", session=SESSION, round=ROUND)
        arm = role_binding.resolve_arm(out["binding"], "EXECUTE")
        self.assertEqual((arm["provider"], arm["model"], arm["rank"]), ("opencode-go", "deepseek-v4.1-flash", 1))

    def test_negative_evidence_bad_guards(self):
        binding = _binding()
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.validate_role_evidence(binding, _evidence(guard="VOID"), role="VERIFY_SECURITY")
        self.assertEqual(ctx.exception.code, "ERR_ROLE_EVIDENCE_GUARD_NOT_CLEAN")
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_role_evidence(binding, _evidence(workorder="WO-OTHER"), role="VERIFY_SECURITY")
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_role_evidence(binding, _evidence(surface="Hermes-internal"), role="VERIFY_SECURITY")
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_role_evidence(binding, _evidence(subject="changed"), role="VERIFY_SECURITY")
        bad = _evidence(lane_receipt={"ok": False, "code": "ERR_X", "receipt_path": "p", "receipt_digest": "d"})
        with self.assertRaises(role_binding.BindingError):
            role_binding.validate_role_evidence(binding, bad, role="VERIFY_SECURITY")


class SpineConsumer(unittest.TestCase):
    def _seed(self, permissions):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-rb-", dir=str(ROOT.parent / "TEST_RESULTS")))
        spine = SharedSpine(tmp / "spine.db")
        spine.initialize()
        spine.create_project()
        spine.register_requirement("REQ-RB", "src#1", "role binding", "ACC-RB", "oracle", "t", "neg")
        spine.acquire_lease("REQ-RB", "maker", "tok")
        spine.transition_requirement("REQ-RB", "FROZEN", "maker", "tok", 0, "E1", "K1")
        spine.create_taskspec("TS-RB", "REQ-RB", "do", "maker", tmp, permissions, ["unit"], "evidence")
        spine.create_workorder(WO, "TS-RB", "writer-a", tmp, BASE)
        return spine

    def test_negative_bound_wo_refuses_empty_evidence(self):
        spine = self._seed({role_binding.ROLE_BINDING_KEY: _binding()})
        with self.assertRaises(InvariantViolation):
            spine.record_workorder_result(WO, "writer-a", "glm-checker", "PASS", ["E1"])

    def test_negative_bound_wo_refuses_replayed_foreign_receipt(self):
        spine = self._seed({role_binding.ROLE_BINDING_KEY: _binding()})
        for bad in (_evidence(workorder="WO-FOREIGN"), _evidence(session="old-session")):
            with self.assertRaises(InvariantViolation):
                spine.record_workorder_result(WO, "writer-a", "glm-checker", "PASS", ["E1"], role_evidence=bad)

    def test_negative_self_checker_and_no_delivery(self):
        spine = self._seed({role_binding.ROLE_BINDING_KEY: _binding()})
        with self.assertRaises(InvariantViolation):
            spine.record_workorder_result(WO, "writer-a", "glm-checker", "PASS", ["E1"],
                                          role_evidence=_evidence(checker_identity="writer-a"))
        with self.assertRaises(InvariantViolation):
            spine.record_workorder_result(WO, "writer-a", "glm-checker", "PASS", ["E1"],
                                          role_evidence=_evidence(artifact_digest=""))

    def test_positive_bound_wo_verified_with_exact_evidence(self):
        spine = self._seed({role_binding.ROLE_BINDING_KEY: _binding()})
        result = spine.record_workorder_result(WO, "writer-a", "glm-checker", "PASS", ["E1"],
                                               role_evidence=_evidence())
        self.assertEqual(result["role_evidence"]["arm"], "opencode-go/glm-5.3-flash")
        with spine.connect() as c:
            state = c.execute("SELECT state FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
        self.assertEqual(state["state"], "VERIFIED")

    def test_legacy_non_governed_row_unchanged(self):
        spine = self._seed({"network": "OFF"})
        spine.record_workorder_result(WO, "writer-a", "checker-b", "PASS", ["E1"])
        with spine.connect() as c:
            state = c.execute("SELECT state FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
        self.assertEqual(state["state"], "VERIFIED")


class DispatcherPreSpawn(unittest.TestCase):
    def _run(self, extra, tmpdir, spine_db=None):
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
               "--json-out", str(tmpdir / "receipt.json"),
               "--relay-home", str(tmpdir / "no-such-relay-home")] + extra
        env = dict(os.environ)
        if spine_db:
            # The persisted binding on this throwaway spine (under TEST_RESULTS) is the AUTHORITY;
            # the supplied --role-binding-file is only a projection that must match it byte-for-byte.
            env["HGK_SPINE_DB"] = str(spine_db)
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", stdin=subprocess.DEVNULL, timeout=120,
                              cwd=str(ROOT), env=env)

    def _write_binding(self, tmpdir, **over):
        p = tmpdir / "binding.json"
        p.write_text(json.dumps(_binding(**over)), encoding="utf-8")
        return p

    def _persist_spine(self, tmpdir, **over):
        """Persist the binding on an admitted WorkOrder in a temp spine (TEST_RESULTS only).

        Reuses the SAME spine-persist helpers the passing ``SpineConsumer`` tests use, so the
        dispatcher reads the canonical binding rather than trusting the supplied projection file.
        """
        spine = SharedSpine(tmpdir / "spine.db")
        spine.initialize()
        spine.create_project()
        spine.register_requirement("REQ-RB", "src#1", "role binding", "ACC-RB", "oracle", "t", "neg")
        spine.acquire_lease("REQ-RB", "maker", "tok")
        spine.transition_requirement("REQ-RB", "FROZEN", "maker", "tok", 0, "E1", "K1")
        spine.create_taskspec("TS-RB", "REQ-RB", "do", "maker", tmpdir,
                              {role_binding.ROLE_BINDING_KEY: _binding(**over)}, ["unit"], "evidence")
        spine.create_workorder(WO, "TS-RB", "writer-a", tmpdir, BASE)
        return tmpdir / "spine.db"

    def test_prespawn_require_arm_mismatch_refused_no_spawn(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-rb-e2e-", dir=str(ROOT.parent / "TEST_RESULTS")))
        bf = self._write_binding(tmp)
        db = self._persist_spine(tmp)
        p = self._run(["--role-binding-file", str(bf), "--workorder", WO,
                       "--require-arm", "openai-codex/gpt-6.1-sol"], tmp, spine_db=db)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], disp.ERR_ROLE_BINDING_ARM_MISMATCH)
        self.assertEqual(list(tmp.glob("*.logs")), [])

    def test_prespawn_expired_binding_refused(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-rb-e2e-", dir=str(ROOT.parent / "TEST_RESULTS")))
        bf = self._write_binding(tmp, expiry="2000-01-01T00:00:00+00:00")
        db = self._persist_spine(tmp, expiry="2000-01-01T00:00:00+00:00")
        p = self._run(["--role-binding-file", str(bf), "--workorder", WO], tmp, spine_db=db)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertFalse(r["ok"])
        # EXPIRY specifically -- the test can no longer pass via the workorder-required branch.
        self.assertEqual(r["code"], "ERR_ROLE_BINDING_EXPIRED")

    def test_prespawn_require_arm_omission_derives_mandatory_arm(self):
        """A bound round with no --require-arm must STILL force the binding's arm/rank."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-rb-e2e-", dir=str(ROOT.parent / "TEST_RESULTS")))
        # D2c: a BOUND round now gates completion on a declared deliverable, so the fixture must
        # declare one that actually exists under --cwd (the admitted writable root).
        deliverable = b"bound round deliverable that really landed\n"
        (tmp / "deliverable.py").write_bytes(deliverable)
        bf = self._write_binding(tmp, deliverable={
            "path": "deliverable.py", "sha256": hashlib.sha256(deliverable).hexdigest()})
        db = self._persist_spine(tmp, deliverable={
            "path": "deliverable.py", "sha256": hashlib.sha256(deliverable).hexdigest()})
        scratch = tmp / "usage.jsonl"
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(db)
        env["HGK_STUB_MODE"] = "clean"
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200})
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "deterministic binding omission case",
               "--role-binding-file", str(bf),
               "--workorder", WO,
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(scratch), "--json-out", str(tmp / "receipt.json"),
               "--cwd", str(tmp),
               "--relay-home", str(tmp / "no-such-relay-home")]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", stdin=subprocess.DEVNULL, timeout=180, cwd=str(ROOT), env=env)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(r["required_arm"], "opencode-go/deepseek-v4.1-flash")
        self.assertEqual(r["binding_forced_rank"], 1)
        self.assertEqual(r["role_binding_served_arm"], "opencode-go/deepseek-v4.1-flash")
        self.assertEqual(r["session"], SESSION)
        self.assertEqual(r["round"], ROUND)
        self.assertEqual(r["subject"], SUBJECT)


class CompletionEvidenceVerification(unittest.TestCase):
    """D2a: ``verify_completion_evidence`` is the fail-closed COMPLETE gate.

    The FAR finding: a matching usage receipt (a nonce in raw stdout) with ZERO deliverable must NOT
    be allowed to complete a lane turn. These tests call the REAL helper imported from the production
    module; they never assert on source text.
    """

    def _raw(self) -> bytes:
        return b'{"status": 200, "nonce": "LANE-ENFORCE-BUILDD-5", "receipt": "usage-ok"}\n'

    def test_positive_receipt_real_deliverable_correct_digest_is_allowed(self):
        deliverable = b"def verify_completion_evidence(*, raw_stdout, deliverable_bytes, deliverable_digest_hex, binding):\n    return None\n"
        digest = hashlib.sha256(deliverable).hexdigest()
        out = role_binding.verify_completion_evidence(
            raw_stdout=self._raw(),
            deliverable_bytes=deliverable,
            deliverable_digest_hex=digest,
            binding=_binding(),
        )
        self.assertIsNone(out)

    def test_negative_zero_deliverable_with_receipt_in_raw_refuses(self):
        out = role_binding.verify_completion_evidence(
            raw_stdout=self._raw(),
            deliverable_bytes=b"",
            deliverable_digest_hex=hashlib.sha256(b"").hexdigest(),
            binding=_binding(),
        )
        self.assertEqual(out, "ERR_COMPLETION_NO_DELIVERABLE")

    def test_negative_wrong_digest_refuses(self):
        out = role_binding.verify_completion_evidence(
            raw_stdout=self._raw(),
            deliverable_bytes=b"real deliverable bytes that were actually written",
            deliverable_digest_hex="0" * 64,
            binding=_binding(),
        )
        self.assertEqual(out, "ERR_COMPLETION_DIGEST_MISMATCH")


class DispatcherCompletionEvidence(unittest.TestCase):
    """D2c: the dispatcher's COMPLETION gate must consume ``_resolve_completion_evidence``.

    The FAR case: an attempt with exit 0 + nonce + a matching usage receipt but ZERO deliverable must
    NOT be selected. These call the REAL production helper (imported from the real dispatcher module)
    and then apply the EXACT selection predicate the dispatcher uses; they never assert on source text
    and never inject a stub.
    """

    def _select(self, att, binding, root):
        # Mirror of the dispatcher's completion block, driven by the REAL helper.
        used = None
        completion_evidence = {"checked": False}
        if att.get("exit") == 0 and att.get("nonce_present") and att.get("usage_receipt_ok"):
            _ce = disp._resolve_completion_evidence(att, binding, root=root)
            completion_evidence = {"checked": True, "refusal": _ce}
            if _ce is None:
                used = att
        return used, completion_evidence

    def _mkdir(self):
        return tempfile.mkdtemp(prefix="hgk-rb-d2c-")

    def _attempt(self, tmp):
        raw = (pathlib.Path(tmp) / "attempt-1-stdout.txt")
        raw.write_bytes(b'{"status": 200, "nonce": "LANE-ENFORCE-BUILDD-5", "receipt": "usage-ok"}\n')
        return {"rank": 1, "exit": 0, "nonce_present": True, "usage_receipt_ok": True,
                "stdout_path": str(raw)}

    def test_negative_receipt_but_missing_deliverable_is_not_selected(self):
        tmp = self._mkdir()
        # binding declares a deliverable path that is MISSING on disk -> fail closed.
        binding = _binding(deliverable={"path": "does-not-exist.py", "sha256": "0" * 64})
        used, ce = self._select(self._attempt(tmp), binding, pathlib.Path(tmp))
        self.assertEqual(ce["refusal"], "ERR_COMPLETION_NO_DELIVERABLE")
        self.assertIsNone(used)
        self.assertFalse(bool(used is not None))   # receipt["ok"] would be False

    def test_positive_real_deliverable_correct_digest_is_selected(self):
        tmp = self._mkdir()
        deliverable = b"real work landed on disk\n"
        rel = "deliverable.py"
        (pathlib.Path(tmp) / rel).write_bytes(deliverable)
        binding = _binding(deliverable={"path": rel, "sha256": hashlib.sha256(deliverable).hexdigest()})
        used, ce = self._select(self._attempt(tmp), binding, pathlib.Path(tmp))
        self.assertIsNone(ce["refusal"])
        self.assertIsNotNone(used)
        self.assertTrue(bool(used is not None))    # receipt["ok"] would be True


class SessionBindingLookup(unittest.TestCase):
    """P2a: ``find_session_binding`` -- a PURE session -> active governed-binding lookup.

    The guard payload carries only a ``session_id`` (no role/round), so the governed runtime
    controller must resolve the session's binding itself. Behavioural: every case is driven against
    a real TEMP SharedSpine (the same fixture the ``SpineConsumer`` tests use); nothing here asserts
    on source text or injects a stub.
    """

    _SEQ = 0

    def _seed(self, specs):
        """One FROZEN requirement + one ADMITTED TaskSpec/WorkOrder per ``(ts, wo, session)``."""
        SessionBindingLookup._SEQ += 1
        n = SessionBindingLookup._SEQ
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"hgk-rb-sess-{n}-",
                                            dir=str(ROOT.parent / "TEST_RESULTS")))
        spine = SharedSpine(tmp / "spine.db")
        spine.initialize()
        spine.create_project()
        req = f"REQ-RB-S{n}"
        spine.register_requirement(req, f"src#{n}", "session lookup", f"ACC-RB-S{n}",
                                   "oracle", "t", "neg")
        spine.acquire_lease(req, "maker", "tok")
        spine.transition_requirement(req, "FROZEN", "maker", "tok", 0, "E1", "K1")
        for i, (ts, wo, session) in enumerate(specs):
            binding = _binding(session=session, workorder=wo)
            spine.create_taskspec(ts, req, "do", "maker", tmp,
                                  {role_binding.ROLE_BINDING_KEY: binding}, ["unit"], "evidence")
            spine.create_workorder(wo, ts, f"writer-{i}", tmp, BASE)
        return spine

    def test_negative_unknown_session_returns_none_no_exception(self):
        spine = self._seed([("TS-1", "WO-1", "session-A")])
        self.assertIsNone(role_binding.find_session_binding(spine, "no-such-session"))

    def test_negative_blank_session_is_a_typed_refusal(self):
        # Fail-closed style of the module: a blank identifier is a refusal, not a silent "unbound".
        spine = self._seed([("TS-1", "WO-1", "session-A")])
        for blank in ("", "   ", None):
            with self.assertRaises(role_binding.BindingError) as ctx:
                role_binding.find_session_binding(spine, blank)
            self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_SESSION_REQUIRED")

    def test_negative_missing_spine_is_a_typed_refusal(self):
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.find_session_binding(None, "session-A")
        self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_CANONICAL_SPINE")

    def test_negative_two_live_workorders_same_session_refuse_no_pick(self):
        spine = self._seed([("TS-A", "WO-A", "shared"), ("TS-B", "WO-B", "shared")])
        with self.assertRaises(role_binding.BindingError) as ctx:
            role_binding.find_session_binding(spine, "shared")
        self.assertEqual(ctx.exception.code, "ERR_ROLE_BINDING_AMBIGUOUS_SESSION")
        self.assertEqual(sorted(ctx.exception.detail), ["WO-A", "WO-B"])

    def test_positive_single_live_match_returns_wo_and_binding_with_matching_digest(self):
        spine = self._seed([("TS-S", "WO-S", "sess-P")])
        out = role_binding.find_session_binding(spine, "sess-P")
        self.assertIsNotNone(out)
        self.assertEqual(out["workorder"], "WO-S")
        self.assertEqual(out["binding"]["session"], "sess-P")
        self.assertEqual(out["binding"]["workorder"], "WO-S")
        self.assertEqual(role_binding.binding_digest(out["binding"]),
                         role_binding.binding_digest(_binding(session="sess-P", workorder="WO-S")))
        # The session-keyed lookup resolves to the SAME persisted document the WO-keyed loader reads.
        canonical = role_binding.load_canonical_binding(spine, "WO-S")
        self.assertEqual(role_binding.binding_digest(out["binding"]),
                         role_binding.binding_digest(canonical["binding"]))

    def test_negative_different_session_workorder_is_not_returned_for_s(self):
        spine = self._seed([("TS-1", "WO-1", "sess-1"), ("TS-2", "WO-2", "sess-2")])
        out = role_binding.find_session_binding(spine, "sess-1")
        self.assertEqual(out["workorder"], "WO-1")
        self.assertEqual(out["binding"]["session"], "sess-1")
        self.assertEqual(role_binding.find_session_binding(spine, "sess-2")["workorder"], "WO-2")


if __name__ == "__main__":
    unittest.main()
