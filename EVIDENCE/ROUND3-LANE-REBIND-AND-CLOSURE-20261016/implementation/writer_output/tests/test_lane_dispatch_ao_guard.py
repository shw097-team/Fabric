"""Regression tests for the AO-lane independence guards (round FAR-AO-INDEPENDENCE-20261010).

Each test names the defect it locks down:
  D-1  the dispatch kept only a 400-char stdout tail, so an AO verdict outside the tail was
       unrecoverable (receipt E3 -> ADVISORY_INCONCLUSIVE_FROM_RECORD)
  D-2  an arm that cannot work without a human was spawned anyway, so the failure surfaced as a
       modal window instead of a typed refusal
  D-3  an escalated-sandbox checker could in principle write the subject it was judging, with
       nothing measuring it
All tests are deterministic and spawn NO model turn: the refusal paths are asserted end-to-end
because they are exactly the paths that must not reach the CLI.
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
_spec = importlib.util.spec_from_file_location("hgk_lane_dispatch", ROOT / "scripts" / "hgk-lane-dispatch.py")
disp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(disp)

REAL_POOL = ROOT / "config" / "lane-route-slots.candidate.json"

OAUTH_ARM = {"rank": 4, "provider": "openai-codex", "model": "gpt-6.1-sol"}
KEY_ARM = {"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash"}


def _empty_home():
    return pathlib.Path(tempfile.mkdtemp(prefix="hgk-home-empty-"))


class GateIdentityRequirement(unittest.TestCase):
    """D-2: which identity an arm actually needs, and the refusal when it is absent."""

    def test_key_arm_needs_no_human_even_with_an_empty_lane_home(self):
        """Locks the corrected belief: the lane home being `Not logged in` must NOT refuse a key arm."""
        home = _empty_home()
        v = disp.identity_check(KEY_ARM, "VERIFY_SECURITY", home, _empty_home())
        self.assertEqual(v["requirement"], disp.IDENTITY_NONE)
        self.assertTrue(v["ok"], v)

    def test_oauth_arm_needs_the_relay_pool_not_the_lane_home(self):
        """Locks the measured mechanism: an arm routed via the relay consumes the RELAY credential."""
        self.assertEqual(disp.default_identity_requirement(OAUTH_ARM, "VERIFY_SECURITY"), disp.IDENTITY_RELAY_POOL)

    def test_oauth_arm_is_refused_when_the_relay_credential_is_absent(self):
        v = disp.identity_check(OAUTH_ARM, "VERIFY_SECURITY", _empty_home(), _empty_home())
        self.assertFalse(v["ok"])
        self.assertEqual(v["code"], disp.ERR_RELAY_OAUTH_NEEDS_REAUTH)

    def test_oauth_arm_passes_when_the_relay_credential_can_refresh(self):
        home = _empty_home()
        (home / "codex-accounts.json").write_text(json.dumps(
            {"chatgpt-1": {"refreshToken": "FIXTURE-NOT-A-REAL-TOKEN"}}), encoding="utf-8")
        v = disp.identity_check(OAUTH_ARM, "VERIFY_SECURITY", _empty_home(), home)
        self.assertTrue(v["ok"], v)
        self.assertIn("refreshable", v["detail"])

    def test_expired_access_token_is_not_a_failure(self):
        """Boundary: only the ABSENCE of refresh material is a failure, never expiry."""
        home = _empty_home()
        (home / "auth.json").write_text(json.dumps(
            {"tokens": {"accessToken": "FIXTURE", "refreshToken": "FIXTURE",
                        "expiresAt": "2020-01-01T00:00:00Z"}}), encoding="utf-8")
        ok, detail = disp.probe_relay_pool_health(home)
        self.assertTrue(ok, detail)

    def test_declared_cli_login_arm_is_refused_without_a_credential(self):
        arm = dict(KEY_ARM, identity_requirement=disp.IDENTITY_CLI_LOGIN)
        v = disp.identity_check(arm, "EXECUTE", _empty_home(), _empty_home())
        self.assertFalse(v["ok"])
        self.assertEqual(v["code"], disp.ERR_IDENTITY_NOT_PREAUTHORIZED)

    def test_cli_login_arm_passes_with_tokens_present(self):
        home = _empty_home()
        (home / "auth.json").write_text(json.dumps({"tokens": {"accessToken": "FIXTURE"}}), encoding="utf-8")
        ok, detail = disp.probe_cli_login(home)
        self.assertTrue(ok, detail)

    def test_unknown_requirement_is_typed_not_ignored(self):
        """A typo in the pool artifact must refuse, never silently pass."""
        arm = dict(KEY_ARM, identity_requirement="relay_pool ")
        v = disp.identity_check(arm, "EXECUTE", _empty_home(), _empty_home())
        self.assertFalse(v["ok"])
        self.assertEqual(v["code"], "ERR_LANE_IDENTITY_UNKNOWN")

    def test_declared_requirement_wins_over_the_provider_default(self):
        arm = dict(OAUTH_ARM, identity_requirement=disp.IDENTITY_CLI_LOGIN)
        self.assertEqual(disp.default_identity_requirement(arm, "VERIFY_SECURITY"), disp.IDENTITY_CLI_LOGIN)


class NonMutationGuard(unittest.TestCase):
    """D-3: an escalated-sandbox checker must be measurably non-mutating."""

    def test_changed_file_voids_and_added_file_does_not(self):
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-subject-"))
        (d / "keep.txt").write_text("v1", encoding="utf-8")
        before = disp.snapshot_subject([d])
        (d / "new.txt").write_text("verdict", encoding="utf-8")
        after_add = disp.snapshot_subject([d])
        m_add = disp.diff_subject(before, after_add)
        self.assertFalse(m_add["mutated"], m_add)
        self.assertEqual(m_add["added"], [str(d / "new.txt").replace("\\", "/")])
        (d / "keep.txt").write_text("v2", encoding="utf-8")
        m_chg = disp.diff_subject(before, disp.snapshot_subject([d]))
        self.assertTrue(m_chg["mutated"], m_chg)

    def test_removal_voids_the_verdict(self):
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-subject-"))
        (d / "gone.txt").write_text("x", encoding="utf-8")
        before = disp.snapshot_subject([d])
        (d / "gone.txt").unlink()
        self.assertTrue(disp.diff_subject(before, disp.snapshot_subject([d]))["mutated"])

    def test_snapshot_covers_nested_files_and_a_bare_file_root(self):
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-subject-"))
        (d / "sub").mkdir()
        (d / "sub" / "deep.txt").write_text("x", encoding="utf-8")
        self.assertEqual(len(disp.snapshot_subject([d])), 1)
        self.assertEqual(len(disp.snapshot_subject([d / "sub" / "deep.txt"])), 1)

    def test_snapshot_digest_is_stable_and_content_sensitive(self):
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-subject-"))
        (d / "f.txt").write_text("a", encoding="utf-8")
        s1 = disp.snapshot_subject([d])
        dg1 = hashlib.sha256(json.dumps(sorted(s1.items())).encode()).hexdigest()
        s2 = disp.snapshot_subject([d])
        dg2 = hashlib.sha256(json.dumps(sorted(s2.items())).encode()).hexdigest()
        self.assertEqual(dg1, dg2)
        (d / "f.txt").write_text("b", encoding="utf-8")
        s3 = disp.snapshot_subject([d])
        self.assertNotEqual(dg1, hashlib.sha256(json.dumps(sorted(s3.items())).encode()).hexdigest())


class AttemptPersistence(unittest.TestCase):
    """D-1: the full attempt output must survive on disk, with a digest, outside the 400-char tail."""

    def test_full_stdout_is_written_with_bytes_and_digest(self):
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-logs-"))
        long_text = ("{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\","
                     "\"text\":\"" + ("VERDICT " * 400) + "TAIL_ONLY_HERE\"}}\n")
        meta = disp.persist_attempt_logs(d, 4, long_text, "err-line")
        self.assertTrue(meta["stdout_path"].endswith("attempt-4-stdout.txt"))
        self.assertEqual(meta["stdout_bytes"], len(long_text.encode("utf-8")))
        stored = pathlib.Path(meta["stdout_path"]).read_text(encoding="utf-8")
        self.assertEqual(stored, long_text)
        self.assertEqual(meta["stdout_sha256"], hashlib.sha256(long_text.encode()).hexdigest())
        # the evidence is much larger than the receipt's own tail, which is the whole point
        self.assertGreater(meta["stdout_bytes"], 400)

    def test_no_log_dir_returns_a_placeholder_and_writes_nothing(self):
        meta = disp.persist_attempt_logs(None, 1, "out", "err")
        self.assertIsNone(meta["attempt_log_dir"])
        self.assertNotIn("stdout_path", meta)


class GateEndToEndRefusal(unittest.TestCase):
    """D-2 end-to-end: a refused arm must produce a typed refusal and spawn NOTHING."""

    def _run(self, extra):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-e2e-"))
        json_out = tmp / "receipt.json"
        cmd = [sys.executable, str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "VERIFY_SECURITY", "--prompt", "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
               "--json-out", str(json_out), "--relay-home", str(tmp / "no-such-relay-home")]
        cmd += extra
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           stdin=subprocess.DEVNULL, timeout=120, cwd=str(ROOT))
        return p, json_out, tmp

    def test_required_arm_refused_fails_closed_instead_of_degrading(self):
        p, json_out, tmp = self._run(["--require-arm", "openai-codex/gpt-6.1-sol"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads(json_out.read_text(encoding="utf-8"))
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], disp.ERR_RELAY_OAUTH_NEEDS_REAUTH)
        self.assertTrue(r["identity_gate"]["degraded"])
        self.assertEqual(list(tmp.glob("*.logs")), [], "a refusal must not create attempt logs")

    def test_required_arm_absent_from_the_pool_is_typed(self):
        p, json_out, _ = self._run(["--require-arm", "openai-codex/definitely-not-a-model"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"], "ERR_LANE_REQUIRED_ARM_ABSENT")

    def test_guard_root_that_does_not_resolve_is_refused(self):
        """MEASURED (probe E5b): an unresolvable guard root produced a zero-file snapshot and the
        receipt still read 'mutated: false'. A vacuous guard must refuse, never bless."""
        p, json_out, tmp = self._run(["--guard-subject", str(tmp := pathlib.Path(tempfile.mkdtemp()) / "absent-dir")])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads(json_out.read_text(encoding="utf-8"))
        self.assertEqual(r["code"], "ERR_GUARD_ROOT_MISSING")
        self.assertIn("vacuous guard", r["say"])

    def test_all_arms_refused_refuses_wholesale_with_no_spawn(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-e2e-"))
        pool = json.loads(REAL_POOL.read_text(encoding="utf-8"))
        for lane in pool["lanes"]:
            if lane["lane"] == "VERIFY_SECURITY":
                kept = [e for e in lane["ordered_pool"] if e["provider"] in ("openai-codex", "openai")]
                # the resolver refuses a rank GAP, so renumber contiguously from 1
                lane["ordered_pool"] = [dict(e, rank=i + 1) for i, e in enumerate(kept)]
        fixture = tmp / "pool-oauth-only.json"
        fixture.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")
        json_out = tmp / "r.json"
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
                            "--lane", "VERIFY_SECURITY", "--pool", str(fixture), "--prompt", "PLACEHOLDER",
                            "--json-out", str(json_out), "--relay-home", str(tmp / "absent")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           stdin=subprocess.DEVNULL, timeout=120, cwd=str(ROOT))
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads(json_out.read_text(encoding="utf-8"))
        self.assertEqual(r["code"], disp.ERR_RELAY_OAUTH_NEEDS_REAUTH)
        self.assertIn("nothing was spawned", r["say"])
        self.assertEqual(list(tmp.glob("*.logs")), [])

    def test_healthy_relay_home_lets_the_oauth_arm_survive_the_gate(self):
        """No spawn: the gate decision is asserted directly, the same function the e2e path calls."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-e2e-"))
        (tmp / "auth.json").write_text(json.dumps({"tokens": {"refreshToken": "FIXTURE"}}), encoding="utf-8")
        v = disp.identity_check(OAUTH_ARM, "VERIFY_SECURITY", tmp, tmp)
        self.assertTrue(v["ok"], v)


class HostileReviewRegression(unittest.TestCase):
    """Every test here locks down a defect an adversarial review found in the first version.

    The review's findings are named F1..F13 in round FAR-AO-INDEPENDENCE-20261010; only the ones this
    change actually fixed are asserted here, and the unfixed ones stay disclosed in the report.
    """

    def _dispatch(self, extra, relay_home=None, guard_own_tmp=False):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-"))
        json_out = tmp / "receipt.json"
        cmd = [sys.executable, str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "VERIFY_SECURITY", "--prompt", "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
               "--json-out", str(json_out),
               "--relay-home", str(relay_home if relay_home else tmp / "no-such-relay-home")]
        if guard_own_tmp:
            # the guard root MUST be the same directory the harness writes its own output into,
            # otherwise the containment check is not what is being exercised (and the run would
            # proceed to spawn a real turn).
            # G3: the root must be NON-EMPTY, else it would (correctly) refuse as ERR_GUARD_ROOT_EMPTY
            # before the containment check and this test would no longer exercise containment.
            (tmp / "sentinel.txt").write_text("subject\n", encoding="utf-8")
            cmd += ["--guard-subject", str(tmp), "--allow-unguarded-escalation"]
        p = subprocess.run(cmd + extra, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", stdin=subprocess.DEVNULL, timeout=120, cwd=str(ROOT))
        return p, json_out, tmp

    @staticmethod
    def _pool_with_verify_arm(tmp, mutate):
        pool = json.loads(REAL_POOL.read_text(encoding="utf-8"))
        for lane in pool["lanes"]:
            if lane["lane"] == "VERIFY_SECURITY":
                # keep exactly ONE arm and renumber it contiguously: the resolver refuses a rank gap
                # and also refuses duplicate ranks, so a naive filter-then-rank=1 renumbers twice.
                kept = [e for e in lane["ordered_pool"] if e["provider"] == "opencode-go"][:1]
                lane["ordered_pool"] = [dict(e, rank=i + 1) for i, e in enumerate(kept)]
                mutate(lane["ordered_pool"][0])
        f = tmp / "pool-fixture.json"
        f.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")
        return f

    def test_F2_a_declared_cli_login_requirement_is_honoured_end_to_end(self):
        """First version dropped identity_requirement when building entries, so the pool's declaration
        was decorative and the gate only ever used the provider heuristic."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-"))
        pool = self._pool_with_verify_arm(tmp, lambda e: e.update(identity_requirement="cli_login"))
        p, json_out, _ = self._dispatch(["--pool", str(pool)])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"],
                         disp.ERR_IDENTITY_NOT_PREAUTHORIZED)

    def test_F2_a_misspelled_requirement_is_refused_end_to_end(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-"))
        pool = self._pool_with_verify_arm(tmp, lambda e: e.update(identity_requirement="relay_pool "))
        p, json_out, _ = self._dispatch(["--pool", str(pool)])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"], "ERR_LANE_IDENTITY_UNKNOWN")

    def test_F1_no_identity_gate_does_not_switch_off_require_arm(self):
        """The require-arm block was nested inside `if not args.no_identity_gate`, so one flag turned
        the fail-closed guarantee off and let the run degrade to another arm."""
        p, json_out, _ = self._dispatch(["--no-identity-gate", "--require-arm", "openai-codex/gpt-6.1-sol"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"],
                         disp.ERR_RELAY_OAUTH_NEEDS_REAUTH)

    def test_F4_an_escalated_lane_without_a_guard_is_refused(self):
        """danger-full-access has no sandbox root, so an unguarded escalated checker was unbounded
        while the receipt still reported ok:true."""
        p, json_out, _ = self._dispatch(["--sandbox", "danger-full-access", "--allow-sandbox-escalation"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"],
                         "ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER")

    def test_F6_a_guard_root_containing_harness_output_is_refused(self):
        """If the harness's own writes land inside a guard root they register as subject changes."""
        p, json_out, _ = self._dispatch([], guard_own_tmp=True)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(json.loads(json_out.read_text(encoding="utf-8"))["code"],
                         "ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT")

    def test_F9_a_negative_max_candidates_is_a_typed_refusal(self):
        """It used to empty the candidate list and crash the gate with IndexError (exit 1)."""
        p, _, _ = self._dispatch(["--max-candidates", "-5"])
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertEqual(json.loads(p.stdout.strip().splitlines()[-1])["code"], "ERR_MAX_CANDIDATES_NEGATIVE")

    def test_F3_null_or_empty_refresh_material_is_not_healthy(self):
        """The probe was a substring test: `"refreshToken" in raw` passed on null, empty and
        needs-reauth credentials."""
        cases = [
            {"chatgpt-1": {"status": "needs-reauth", "refreshToken": None}},
            {"tokens": {"accessToken": "x", "refreshToken": ""}},
            {"tokens": {"refreshToken": "   "}},
            {"chatgpt-1": {"status": "reauth_required", "refreshToken": "non-empty"}},
        ]
        for i, doc in enumerate(cases):
            home = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-relay-"))
            (home / "codex-accounts.json").write_text(json.dumps(doc), encoding="utf-8")
            ok, detail = disp.probe_relay_pool_health(home)
            self.assertFalse(ok, f"case {i} wrongly healthy: {detail}")
        good = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-relay-"))
        (good / "codex-accounts.json").write_text(json.dumps({"r": {"refreshToken": "abc"}}), encoding="utf-8")
        self.assertTrue(disp.probe_relay_pool_health(good)[0])

    def test_F3_an_empty_cli_credential_is_not_a_login(self):
        home = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-home-"))
        (home / "auth.json").write_text(json.dumps({"tokens": {"accessToken": ""}}), encoding="utf-8")
        self.assertFalse(disp.probe_cli_login(home)[0])

    def test_F7_non_utf8_bytes_are_persisted_exactly(self):
        """text=True + errors="replace" destroyed bytes BEFORE the file was written, so
        'byte-identical' was untrue for any non-UTF-8 output."""
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-logs-"))
        raw = b'{"text":"caf\xe9 \xff\xfe"}\r\n'
        meta = disp.persist_attempt_logs(d, 1, raw.decode("utf-8", "replace"), "", run_id="r1", out_bytes=raw)
        self.assertTrue(meta["stdout_byte_exact"])
        self.assertEqual(pathlib.Path(meta["stdout_path"]).read_bytes(), raw)
        self.assertEqual(meta["stdout_bytes"], len(raw))

    def test_F8_attempt_logs_do_not_collide_across_runs(self):
        """Same rank + same log dir used to overwrite the previous run's whole log."""
        d = pathlib.Path(tempfile.mkdtemp(prefix="hgk-hr-logs-"))
        a = disp.persist_attempt_logs(d, 4, "RUN-ONE", "", run_id="r1", out_bytes=b"RUN-ONE")
        b = disp.persist_attempt_logs(d, 4, "RUN-TWO", "", run_id="r2", out_bytes=b"RUN-TWO")
        self.assertNotEqual(a["stdout_path"], b["stdout_path"])
        self.assertEqual(pathlib.Path(a["stdout_path"]).read_bytes(), b"RUN-ONE")
        self.assertEqual(pathlib.Path(b["stdout_path"]).read_bytes(), b"RUN-TWO")


class DeterministicGuardNegative(unittest.TestCase):
    """LIVE negative matrix for the non-mutation guard, with NO model in the loop.

    The owner asked for this path to be closed deterministically after three model-driven attempts
    (E5/E5b/E5c) all failed to produce a live negative. A stub child (tests/fixtures/stub_lane_child
    .py) is pointed at with --codex-executable; it emits BOTH carriers the dispatcher accepts (the
    nonce inside an agent_message item, and a matching usage row) and then performs the mutation.
    So the attempt satisfies every acceptance condition and the GUARD is what voids it -- a genuine
    would-have-PASSED attempt, not a turn that was already failing.
    """

    FIXTURE = "tests/fixtures/stub_lane_child.py"
    SCRATCH = None  # set per-case inside a temp dir

    def _case(self, mode, *, subject="file", target=None):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-neg-"))
        scratch = tmp / "usage.jsonl"
        if subject == "file":
            guarded = tmp / "subject.txt"
            guarded.write_text("base\n", encoding="utf-8")
            subject_path = guarded
            default_target = guarded
        else:
            guarded = tmp / "subjectdir"
            guarded.mkdir()
            # G3: seed the subject so the guard root is NON-EMPTY; an empty snapshot now (correctly)
            # refuses as ERR_GUARD_ROOT_EMPTY before the turn, so this test would stop exercising the
            # "an added file is recorded but not fatal" rule it names.
            (guarded / "sentinel.txt").write_text("base\n", encoding="utf-8")
            subject_path = guarded
            # the stub must CREATE a file INSIDE the guarded dir; writing to the directory path
            # itself raises PermissionError and the new file is what the guard reports as `added`.
            default_target = guarded / "stub-created.txt"
        env = dict(os.environ)
        env["HGK_STUB_MODE"] = mode
        env["HGK_STUB_TARGET"] = str(target or default_target)
        env["HGK_STUB_USAGE"] = str(scratch)
        # usage line tracks the VERIFY rank-1 arm from the pool file (single source of truth;
        # the stub answers AS the arm the dispatcher will pick on --force-rank 1)
        slots_doc = json.loads((ROOT / "config" / "lane-route-slots.candidate.json").read_text(encoding="utf-8"))
        v_lane = next(l for l in slots_doc["lanes"] if l["lane"] == "VERIFY_SECURITY")
        v_r1 = v_lane["ordered_pool"][0]
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": v_r1["provider"], "model": v_r1["model"], "status": 200})
        json_out = tmp / "receipt.json"
        cmd = [sys.executable, str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(ROOT / self.FIXTURE),
               "--usage", str(scratch), "--guard-subject", str(subject_path),
               "--attempt-log-dir", str(tmp / "logs"), "--json-out", str(json_out),
               "--timeout", "120", "--prompt", "deterministic stub case"]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                           cwd=str(ROOT), env=env)
        self.assertTrue(json_out.is_file(), p.stdout + p.stderr)
        return p.returncode, json.loads(json_out.read_text(encoding="utf-8"))

    def test_E11a_a_conforming_attempt_stands(self):
        rc, r = self._case("clean")
        self.assertEqual(rc, 0, r)
        self.assertTrue(r["ok"])
        self.assertFalse(r["subject_mutation"]["mutated"])
        self.assertTrue(r["attempts"][0]["nonce_present"])

    def test_E11b_mutation_voids_a_would_have_passed_attempt(self):
        rc, r = self._case("mutate")
        self.assertEqual(rc, 3, r)
        self.assertEqual(r["code"], "ERR_CHECKER_MUTATED_SUBJECT")
        # the attempt itself satisfied every acceptance condition -> the guard, not a failed turn
        self.assertTrue(r["attempts"][0]["nonce_present"])
        self.assertTrue(r["attempts"][0]["usage_receipt_ok"])
        self.assertEqual(r["attempts"][0]["exit"], 0)
        self.assertTrue(r["subject_mutation"]["changed"])

    def test_E11c_removal_voids_a_would_have_passed_attempt(self):
        rc, r = self._case("remove")
        self.assertEqual(rc, 3, r)
        self.assertEqual(r["code"], "ERR_CHECKER_MUTATED_SUBJECT")
        self.assertTrue(r["subject_mutation"]["removed"])

    def test_E11d_an_added_file_is_recorded_but_not_fatal(self):
        rc, r = self._case("create", subject="dir")
        self.assertEqual(rc, 0, r)
        self.assertTrue(r["ok"])
        self.assertTrue(r["subject_mutation"]["added"])
        self.assertFalse(r["subject_mutation"]["mutated"])


# ---------------------------------------------------------------------------------------------
# FAR-LANE-HEALTH-REPAIR-20261011 (WO-LANE-HEALTH-013-EXEC)
#   C1  the receipt conflated "no arm emitted the nonce" with "no arm was reachable at all"
#   C2  a declared capability (feasibility/dispatchable) with no consumer
#   C3  the identity gate asserted "no human-attended identity" without reading the resolved home
# All deterministic: the child is the stub (fixtures/stub_lane_child.py); nothing here touches the
# network, a real model, the relay, or the developer's real Codex home.
# ---------------------------------------------------------------------------------------------


def _lane_pool(tmp, lane, entries, *, renumber=False):
    """Write a fixture pool holding only `lane` with the given raw ordered_pool entries.

    The resolver refuses a rank gap and duplicate tokens, so callers either supply already-valid ranks
    or ask for a contiguous renumber.
    """
    pool = json.loads(REAL_POOL.read_text(encoding="utf-8"))
    for ln in pool["lanes"]:
        if ln["lane"] == lane:
            ln["ordered_pool"] = ([dict(e, rank=i + 1) for i, e in enumerate(entries)]
                                  if renumber else entries)
    f = pathlib.Path(tmp) / "pool-fixture.json"
    f.write_text(json.dumps(pool, ensure_ascii=False), encoding="utf-8")
    return f


def _hermetic_verify_pool(tmp):
    """VERIFY pool whose rank 1 is an env-credentialed arm (opencode-go), so nonce/guard tests never
    depend on the OAuth relay home. Post-rebind the real rank 1 is openai-codex (relay_pool)."""
    entries = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                "feasibility": "DISPATCHABLE", "transport_model": "opencode-go/deepseek-v4.1-flash",
                "identity_requirement": "none"}]
    return _lane_pool(tmp, "VERIFY_SECURITY", entries)

def _run_dispatch(cmd_extra, *, env=None, timeout=120):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-"))
    json_out = tmp / "receipt.json"
    cmd = [sys.executable, str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
           "--json-out", str(json_out), "--relay-home", str(tmp / "no-such-relay-home")]
    p = subprocess.run(cmd + cmd_extra, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", stdin=subprocess.DEVNULL, timeout=timeout,
                       cwd=str(ROOT), env=env)
    rec = json.loads(json_out.read_text(encoding="utf-8")) if json_out.is_file() else None
    return p, rec, tmp


def _stub_env(tmp, provider="opencode-go", model="deepseek-v4.1-flash"):
    env = dict(os.environ)
    env["HGK_STUB_MODE"] = "clean"
    env["HGK_STUB_USAGE"] = str(tmp / "usage.jsonl")
    env["HGK_STUB_USAGE_LINE"] = json.dumps({"provider": provider, "model": model, "status": 200})
    return env


class C1FailureDisposition(unittest.TestCase):
    """The failure code must separate a nonce-less answered run from a wholly-unreachable one."""

    def test_answered_but_no_nonce_is_named(self):
        a = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
              "exit": 0, "usage_receipt_ok": True, "nonce_present": False}]
        d = disp.failure_disposition(a)
        self.assertEqual(d["code"], "ERR_NO_ARM_EMITTED_NONCE")
        self.assertEqual(d["nonce_absent_arms"], ["opencode-go/deepseek-v4.1-flash"])
        self.assertNotIn("timed_out_arms", d)

    def test_all_timed_out_is_named(self):
        a = [{"rank": 1, "provider": "nvidia", "model": "deepseek-ai/deepseek-v4.1-flash",
              "exit": "TIMEOUT", "usage_receipt_ok": False, "nonce_present": False}]
        d = disp.failure_disposition(a)
        # The frozen oracle rules that the GENERIC code is used whenever no arm produced an acceptable
        # turn -- including the all-timeout case. The timeout is still MEASURED via timed_out_arms.
        self.assertEqual(d["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertEqual(d["timed_out_arms"], ["nvidia/deepseek-ai/deepseek-v4.1-flash"])
        self.assertNotEqual(d["code"], "ERR_NO_ARM_EMITTED_NONCE")
        self.assertNotEqual(d["code"], "ERR_ALL_ATTEMPTS_TIMED_OUT")

    def test_fallback_boundary_is_the_generic_code(self):
        cases = [
            [],                                                    # no attempts at all
            [{"exit": 1, "usage_receipt_ok": False, "nonce_present": False,
              "provider": "opencode-go", "model": "deepseek-v4.1-flash"}],  # plain failure
            [{"exit": 0, "usage_receipt_ok": False, "nonce_present": False,
              "provider": "opencode-go", "model": "deepseek-v4.1-flash"}],  # exit 0 but NO receipt
        ]
        for i, a in enumerate(cases):
            self.assertEqual(disp.failure_disposition(a)["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED",
                             f"case {i}")

    def test_end_to_end_no_nonce_run_reads_the_new_code(self):
        """A stub that answers with usage but emits no nonce -> ERR_NO_ARM_EMITTED_NONCE, ok:false."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c1-"))
        env = _stub_env(tmp)
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool),
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--nonce", "A-NONCE-THE-STUB-WILL-NOT-EMIT",
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=env)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE", p.stdout + p.stderr)
        self.assertEqual(rec["nonce_absent_arms"], ["opencode-go/deepseek-v4.1-flash"])


class C2DispatchableConsumer(unittest.TestCase):
    """The artifact's dispatchable/feasibility must actually gate the spawn."""

    GOOD = {"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
            "feasibility": "DISPATCHABLE", "transport_model": "opencode-go/deepseek-v4.1-flash",
            "identity_requirement": "none"}
    DEAD = {"rank": 2, "provider": "nvidia", "model": "deepseek-ai/deepseek-v4.1-flash",
            "feasibility": "UNREACHABLE_MEASURED_20261011", "dispatchable": False,
            "transport_model": "nvidia/deepseek-ai/deepseek-v4.1-flash",
            "identity_requirement": "none"}

    def test_helper_rule(self):
        self.assertFalse(disp._is_dispatchable({"dispatchable": False}))
        self.assertFalse(disp._is_dispatchable({"feasibility": "UNREACHABLE_MEASURED_20261011"}))
        self.assertFalse(disp._is_dispatchable({"feasibility": "CONFIG_COMPLETE_NOT_ACTIVATED"}))
        self.assertTrue(disp._is_dispatchable({"feasibility": "DISPATCHABLE"}))
        self.assertTrue(disp._is_dispatchable({}))

    def test_declared_not_dispatchable_arm_is_skipped_with_no_spawn(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c2-"))
        pool = _lane_pool(tmp, "VERIFY_SECURITY", [self.GOOD, self.DEAD])
        logs = tmp / "logs"
        cmd = ["--lane", "VERIFY_SECURITY", "--pool", str(pool),
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--attempt-log-dir", str(logs), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(rec["skipped_arms"],
                         [{"rank": 2, "arm": "nvidia/deepseek-ai/deepseek-v4.1-flash",
                           "reason": "UNREACHABLE_MEASURED_20261011"}], p.stdout + p.stderr)
        spawned = [f.name for f in logs.glob("attempt-*")] if logs.is_dir() else []
        self.assertFalse(any("-2-" in name for name in spawned), spawned)
        self.assertEqual([a["rank"] for a in rec["attempts"]], [1])

    def test_force_rank_reaches_a_skipped_rank(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c2f-"))
        pool = _lane_pool(tmp, "VERIFY_SECURITY", [self.GOOD, self.DEAD])
        cmd = ["--lane", "VERIFY_SECURITY", "--pool", str(pool), "--force-rank", "2",
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp, provider="nvidia",
                                                     model="deepseek-ai/deepseek-v4.1-flash"))
        self.assertEqual([a["rank"] for a in rec["attempts"]], [2], p.stdout + p.stderr)
        self.assertEqual(rec["used_rank"], 2)

    def test_declared_dispatchable_arm_is_never_skipped(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c2n-"))
        good = dict(self.GOOD, dispatchable=True)
        pool = _lane_pool(tmp, "VERIFY_SECURITY", [good])
        cmd = ["--lane", "VERIFY_SECURITY", "--pool", str(pool),
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(rec["skipped_arms"], [], p.stdout + p.stderr)
        self.assertEqual(rec["used_rank"], 1)
        self.assertTrue(rec["ok"])

    def test_all_arms_skipped_reports_the_skip_list_and_fails_closed(self):
        """The skip must not crash the no-candidates path: it reports the skipped arms and refuses."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c2e-"))
        pool = _lane_pool(tmp, "VERIFY_SECURITY", [dict(self.DEAD, rank=1)], renumber=True)
        p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--pool", str(pool),
                                   "--prompt", "x"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["skipped_arms"],
                         [{"rank": 1, "arm": "nvidia/deepseek-ai/deepseek-v4.1-flash",
                           "reason": "UNREACHABLE_MEASURED_20261011"}])


class C3LaneHomeIsolation(unittest.TestCase):
    """The identity gate must read the resolved home before certifying 'no human-attended identity'."""

    def test_helper_classification(self):
        declared = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-declared-"))
        v = disp.lane_home_isolation(declared, declared)
        self.assertTrue(v["codex_home_is_declared_lane_home"])
        self.assertFalse(v["non_isolated"])
        other = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-other-"))
        (other / "auth.json").write_text("{}", encoding="utf-8")
        v2 = disp.lane_home_isolation(other, declared)
        self.assertFalse(v2["codex_home_is_declared_lane_home"])
        self.assertTrue(v2["non_isolated"])

    def test_non_isolated_home_without_flag_refuses_with_exit_4_and_zero_attempts(self):
        home = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c3-"))
        (home / "auth.json").write_text(json.dumps({"OPENAI_API_KEY": "FIXTURE"}), encoding="utf-8")
        p, rec, tmp = _run_dispatch(["--lane", "VERIFY_SECURITY", "--codex-home", str(home),
                                     "--prompt", "x"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["code"], "ERR_LANE_HOME_NOT_ISOLATED")
        self.assertIn("auth.json", rec["detail"])
        self.assertNotIn("attempts", rec)
        self.assertFalse(list(tmp.glob("*.logs")))

    def test_flag_acknowledges_and_records_then_proceeds(self):
        home = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c3a-"))
        (home / "auth.json").write_text(json.dumps({"OPENAI_API_KEY": "FIXTURE"}), encoding="utf-8")
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-lhr-c3a-run-"))
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--codex-home", str(home), "--prompt", "x",
               "--allow-human-home-transport", "--pool", str(pool), "--force-rank", "1",
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertTrue(rec["human_home_transport_acknowledged"])
        self.assertFalse(rec["codex_home_is_declared_lane_home"])
        self.assertTrue(rec["ok"])

    def test_declared_isolated_lane_home_is_never_refused(self):
        """The module's own declared lane home is always accepted, whatever it holds."""
        v = disp.lane_home_isolation(disp.DEFAULT_LANE_HOME, disp.DEFAULT_LANE_HOME)
        self.assertTrue(v["codex_home_is_declared_lane_home"])
        self.assertFalse(v["non_isolated"])


class R2Repair(unittest.TestCase):
    """FAR-LANE-HEALTH-REPAIR-20261011 pass 2 -- the five fixes the independent FAIL named."""

    STUB = "tests/fixtures/stub_lane_child.py"

    # --- FIX 2 (C2): a skipped arm never carries a null reason ---------------------------------
    def test_dispatchable_false_without_feasibility_still_carries_a_reason(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-skip-"))
        good = {"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                "feasibility": "DISPATCHABLE", "transport_model": "opencode-go/deepseek-v4.1-flash",
                "identity_requirement": "none"}
        dead = {"rank": 2, "provider": "nvidia", "model": "deepseek-ai/deepseek-v4.1-flash",
                "dispatchable": False, "transport_model": "nvidia/deepseek-ai/deepseek-v4.1-flash",
                "identity_requirement": "none"}
        pool = _lane_pool(tmp, "VERIFY_SECURITY", [good, dead])
        cmd = ["--lane", "VERIFY_SECURITY", "--pool", str(pool),
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(len(rec["skipped_arms"]), 1, p.stdout + p.stderr)
        self.assertEqual(rec["skipped_arms"][0]["rank"], 2)
        self.assertIsNotNone(rec["skipped_arms"][0]["reason"])
        self.assertTrue(rec["skipped_arms"][0]["reason"])
        self.assertIn("not dispatchable", rec["skipped_arms"][0]["reason"])
        self.assertEqual([a["rank"] for a in rec["attempts"]], [1])

    # --- FIX 3 (C3a): EVERY receipt -- including refusals -- records the home fields ------------
    def test_refusal_receipt_carries_both_home_fields(self):
        p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--prompt", "x",
                                   "--require-arm", "openai-codex/gpt-6.1-sol"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        self.assertIn("codex_home", rec)
        self.assertIn("codex_home_is_declared_lane_home", rec)
        self.assertEqual(rec["codex_home"], str(disp.DEFAULT_LANE_HOME.resolve()))
        self.assertTrue(rec["codex_home_is_declared_lane_home"])

    def test_guard_refusal_receipt_also_carries_both_home_fields(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-home-"))
        p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--prompt", "x",
                                   "--guard-subject", str(tmp / "absent-dir")])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_GUARD_ROOT_MISSING")
        self.assertIn("codex_home", rec)
        self.assertIn("codex_home_is_declared_lane_home", rec)

    # --- FIX 4 (C3b): a relative --codex-home is recorded RESOLVED ------------------------------
    def test_relative_codex_home_is_recorded_resolved(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-rel-"))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--codex-home", ".",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertNotEqual(rec.get("codex_home"), ".")
        self.assertTrue(pathlib.Path(rec["codex_home"]).is_absolute())
        self.assertEqual(rec["codex_home"], str(ROOT.resolve()))
        self.assertFalse(rec["codex_home_is_declared_lane_home"])

    # --- FIX 5: a blank nonce certifies nothing ------------------------------------------------
    def test_blank_nonce_refuses_pre_spawn_with_a_typed_code(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-nonce-"))
        for blank in ("", "   ", "\t"):
            cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--nonce", blank,
                   "--codex-executable", str(ROOT / self.STUB),
                   "--usage", str(tmp / "usage.jsonl"), "--prompt", "x"]
            p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
            self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
            self.assertFalse(rec["ok"])
            self.assertEqual(rec["code"], disp.ERR_NONCE_EMPTY)
            self.assertNotIn("attempts", rec)
            self.assertFalse(list(tmp.glob("*.logs")))

    def test_blank_nonce_stub_would_have_been_a_false_green(self):
        """The checker's constructed false green: an empty nonce made the substring test vacuously
        true. With the gate in place the SAME no-nonce stub now refuses instead of certifying."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-fg-"))
        stub = tmp / "no_nonce_stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "p = pathlib.Path(os.environ['HGK_STUB_USAGE']); p.parent.mkdir(parents=True, exist_ok=True)\n"
            "p.open('a', encoding='utf-8').write(json.dumps(json.loads(os.environ['HGK_STUB_USAGE_LINE'])) + '\\n')\n"
            "print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',\n"
            "  'text': 'NO-NONCE STUB usage-row-appended'}}))\n"
            "sys.exit(0)\n",
            encoding="utf-8")
        env = dict(os.environ)
        env["HGK_STUB_USAGE"] = str(tmp / "usage.jsonl")
        # usage line tracks the VERIFY rank-1 arm from the pool file (single source of truth;
        # the stub answers AS the arm the dispatcher will pick on --force-rank 1)
        slots_doc = json.loads((ROOT / "config" / "lane-route-slots.candidate.json").read_text(encoding="utf-8"))
        v_lane = next(l for l in slots_doc["lanes"] if l["lane"] == "EXECUTE")
        v_r1 = v_lane["ordered_pool"][0]
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": v_r1["provider"], "model": v_r1["model"], "status": 200})
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--nonce", "",
               "--codex-executable", str(stub), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "15", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=env, timeout=60)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["code"], disp.ERR_NONCE_EMPTY)

    def test_non_blank_nonce_still_behaves_as_before(self):
        """The nonce mechanism is NOT redesigned: a non-blank nonce that the arm fails to emit still
        yields ERR_NO_ARM_EMITTED_NONCE, exactly as before the empty-string gate was added."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r2-ok-"))
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool), "--nonce", "A-REAL-NONCE",
               "--codex-executable", str(ROOT / self.STUB),
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE", p.stdout + p.stderr)


class R3Repair(unittest.TestCase):
    """FAR-LANE-HEALTH-REPAIR-20261011 pass 3 -- the three mechanism-level defects the second
    independent checker returned Overall FAIL for. Every test is deterministic: the child is a stub
    (or the fixture), and nothing touches the network, a real model, the relay, or a real Codex home.
    """

    STUB = "tests/fixtures/stub_lane_child.py"

    @staticmethod
    def _text_stub(tmp, text_literal):
        """A stub emitting exactly one item.completed/agent_message with the given RAW text JSON, plus
        a matching usage row, so the turn is 'answered' and the ONLY missing thing is the nonce."""
        stub = tmp / "text_stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "p = pathlib.Path(os.environ['HGK_STUB_USAGE']); p.parent.mkdir(parents=True, exist_ok=True)\n"
            "p.open('a', encoding='utf-8').write(json.dumps(json.loads(os.environ['HGK_STUB_USAGE_LINE'])) + '\\n')\n"
            "sys.stdout.write(" + repr(text_literal) + " + chr(10))\n"
            "sys.exit(0)\n",
            encoding="utf-8")
        return stub

    def _guard_case(self, mode):
        """Drive the non-mutation guard over a NON-EMPTY subject dir, deterministically."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r3-guard-"))
        guarded = tmp / "subjectdir"
        guarded.mkdir()
        (guarded / "subject.txt").write_text("base\n", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_MODE"] = mode
        target = guarded / ("stub-created.txt" if mode == "create" else "subject.txt")
        env["HGK_STUB_TARGET"] = str(target)
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool),
               "--guard-subject", str(guarded),
               "--codex-executable", str(ROOT / self.STUB),
               "--usage", str(tmp / "usage.jsonl"), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=env)
        return p.returncode, rec

    # --- G1: the nonce must never be satisfied by text the child did not emit -------------------
    def test_G1_null_text_is_not_searchable(self):
        """`str(None)` turned a JSON null into the string 'None' and 'satisfied' --nonce None."""
        line = '{"type": "item.completed", "item": {"type": "agent_message", "text": null}}'
        self.assertFalse(disp.nonce_in_agent_message(line, "None"))

    def test_G1_non_string_text_is_not_searchable(self):
        for text in ('{"a": 1}', "[1, 2]", "0", "true"):
            line = '{"type": "item.completed", "item": {"type": "agent_message", "text": %s}}' % text
            self.assertFalse(disp.nonce_in_agent_message(line, "None"), text)
            self.assertFalse(disp.nonce_in_agent_message(line, "1"), text)

    def test_G1_a_real_string_carrier_still_passes(self):
        # S3 (REQ-STRICT-DECLARATION-014): a carrier is a COMPLETE, LF/CRLF-terminated, strictly
        # UTF-8-decodable JSON line. A bare fragment with NO terminator is NOT a row, so the string
        # carrier is supplied with its terminator -- exactly the shape the real child emits.
        line = ('{"type": "item.completed", "item": {"type": "agent_message", '
                '"text": "ok HGK_LANE_NONCE_OK done"}}\n')
        self.assertTrue(disp.nonce_in_agent_message(line, "HGK_LANE_NONCE_OK"))

    def test_G1_null_text_child_cannot_pass_with_nonce_None_end_to_end(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r3-g1-"))
        stub = self._text_stub(
            tmp, '{"type": "item.completed", "item": {"type": "agent_message", "text": null}}')
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool), "--nonce", "None",
               "--codex-executable", str(stub), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertFalse(rec["ok"], p.stdout + p.stderr)
        # answered (exit 0 + usage) but no nonce -> the nonce-less-turn code, never a pass
        self.assertEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE", p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)
        self.assertFalse(rec["attempts"][0]["nonce_present_raw_stdout"])

    def test_G1_object_text_child_cannot_pass_with_nonce_None_end_to_end(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r3-g1o-"))
        stub = self._text_stub(
            tmp, '{"type": "item.completed", "item": {"type": "agent_message", "text": {"a": 1}}}')
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool), "--nonce", "None",
               "--codex-executable", str(stub), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertFalse(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE", p.stdout + p.stderr)

    def test_G1_the_two_nonce_signals_agree_and_the_normal_case_still_passes(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r3-g1a-"))
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool), "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        a = rec["attempts"][0]
        self.assertTrue(a["nonce_present"])
        self.assertTrue(a["nonce_present_raw_stdout"])
        self.assertEqual(a["nonce_present"], a["nonce_present_raw_stdout"])

    # --- G2: an empty feasibility is not a reason ----------------------------------------------
    def test_G2_skip_reason_helper_shapes(self):
        self.assertEqual(disp._skip_reason({"feasibility": "UNREACHABLE_X"}), "UNREACHABLE_X")
        for empty in (None, "", "   ", "\t", [], ["x"], 0, {}, True):
            self.assertEqual(disp._skip_reason({"feasibility": empty}),
                             disp.SKIP_REASON_NO_FEASIBILITY, empty)
        self.assertEqual(
            disp._skip_reason({"dispatchable": False}, declared_not_dispatchable=True),
            "declared not dispatchable (dispatchable: false)")

    def test_G2_empty_feasibility_shapes_still_yield_a_real_reason(self):
        for label, val in (("empty-string", ""), ("whitespace", "   "), ("empty-array", [])):
            tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"hgk-r3-g2-{label}-"))
            dead = {"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                    "dispatchable": False, "feasibility": val,
                    "transport_model": "opencode-go/deepseek-v4.1-flash",
                    "identity_requirement": "none"}
            pool = _lane_pool(tmp, "VERIFY_SECURITY", [dead])
            p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--pool", str(pool), "--prompt", "x"])
            sk = [s for s in (rec.get("skipped_arms") or []) if s.get("rank") == 1]
            self.assertTrue(sk, f"{label}: {p.stdout + p.stderr}")
            self.assertIsInstance(sk[0]["reason"], str, label)
            self.assertTrue(sk[0]["reason"].strip(), f"{label}: empty reason")

    # --- G3: a guard that guards nothing must not report "clean" --------------------------------
    def test_G3_empty_guard_root_refuses_pre_spawn(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r3-g3-"))
        empty = tmp / "empty-subject"
        empty.mkdir()
        pool = _hermetic_verify_pool(tmp)
        p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool),
                                   "--guard-subject", str(empty), "--prompt", "x"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["code"], "ERR_GUARD_ROOT_EMPTY")
        self.assertNotEqual(rec["code"], "ERR_GUARD_ROOT_MISSING")
        self.assertNotIn("attempts", rec)

    def test_G3_non_empty_guard_root_still_snapshots_and_compares(self):
        rc, r = self._guard_case("clean")
        self.assertEqual(rc, 0, r)
        self.assertTrue(r["ok"])
        self.assertGreaterEqual(r["subject_mutation"]["files_before"], 1)
        self.assertFalse(r["subject_mutation"]["mutated"])

    def test_G3_added_file_does_not_void_but_changed_and_removed_do(self):
        rc_add, r_add = self._guard_case("create")
        self.assertEqual(rc_add, 0, r_add)
        self.assertTrue(r_add["ok"])
        self.assertTrue(r_add["subject_mutation"]["added"])
        self.assertFalse(r_add["subject_mutation"]["mutated"])
        rc_chg, r_chg = self._guard_case("mutate")
        self.assertEqual(rc_chg, 3, r_chg)
        self.assertEqual(r_chg["code"], disp.ERR_CHECKER_MUTATED_SUBJECT)
        self.assertTrue(r_chg["subject_mutation"]["changed"])
        rc_rm, r_rm = self._guard_case("remove")
        self.assertEqual(rc_rm, 3, r_rm)
        self.assertEqual(r_rm["code"], disp.ERR_CHECKER_MUTATED_SUBJECT)
        self.assertTrue(r_rm["subject_mutation"]["removed"])


class R4Repair(unittest.TestCase):
    """FAR-LANE-HEALTH-REPAIR-20261011 pass 4 -- the ONE systemic cause behind the three new vacuous
    passes: a verdict must never be satisfiable through a LOSSY REPRESENTATION (a re-decoded string,
    a coerced type, a substituted character) or a LOOSE COMPARISON. Every test is deterministic: a
    stub child, NO model, NO network, NO relay, NO real Codex home.
    """

    STUB = "tests/fixtures/stub_lane_child.py"

    @staticmethod
    def _raw_stub(tmp, stdout_bytes, *, usage_status=200, name="raw_stub.py"):
        """A child that writes EXACT raw stdout bytes and appends one (matching) usage row, so the
        turn is otherwise 'answered' and the only variable is the carrier bytes."""
        stub = tmp / name
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "p = pathlib.Path(os.environ['HGK_STUB_USAGE']); p.parent.mkdir(parents=True, exist_ok=True)\n"
            "p.write_text(json.dumps(json.loads(os.environ['HGK_STUB_USAGE_LINE'])) + chr(10), encoding='utf-8')\n"
            "sys.stdout.buffer.write(" + repr(stdout_bytes) + ")\n"
            "sys.exit(0)\n", encoding="utf-8")
        return stub

    def _run_raw(self, stdout_bytes, nonce, *, usage_status=200, env=None):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-"))
        stub = self._raw_stub(tmp, stdout_bytes, usage_status=usage_status)
        env = dict(env or _stub_env(tmp))
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": usage_status})
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", nonce,
               "--codex-executable", str(stub), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        return _run_dispatch(cmd, env=env)

    # --- H1: the nonce is decided on the preserved BYTES ---------------------------------------
    def test_H1_unit_a_substituted_character_is_not_the_nonce(self):
        """S3: a carrier line that is not strictly UTF-8-decodable is NOT a row, so neither a
        substituted character (U+FFFD) nor a lone surrogate (\udcff) can stand in for it. The invalid
        line is DROPPED and COUNTED (`carrier_lines_undecodable`)."""
        raw = b'{"type":"item.completed","item":{"type":"agent_message","text":"\xff"}}\n'
        surrogate = raw.decode("utf-8", "surrogateescape")
        self.assertFalse(disp.nonce_in_agent_message(surrogate, "\ufffd"))
        self.assertEqual(disp.agent_message_texts(surrogate), [])
        # a strictly-decodable carrier line IS still extracted (no over-blocking)
        good = '{"type":"item.completed","item":{"type":"agent_message","text":"ok \u00e9"}}\n'
        self.assertEqual(disp.agent_message_texts(good), ["ok \u00e9"])
        # the rule is applied uniformly: bytes and the surrogate text agree, and the invalid line is
        # counted rather than substituted.
        self.assertEqual(disp.carrier_line_texts(raw), ([], 1))
        self.assertEqual(disp.carrier_line_texts(surrogate), ([], 1))

    def test_H1_negative_a_0xFF_carrier_cannot_satisfy_U_FFFD_end_to_end(self):
        raw = b'{"type":"item.completed","item":{"type":"agent_message","text":"\xff"}}\n'
        p, rec, _ = self._run_raw(raw, "\ufffd")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        a = rec["attempts"][0]
        self.assertIsNot(a["nonce_present"], True)
        self.assertEqual(a["nonce_present"], a["nonce_present_raw_stdout"])

    def test_H1_positive_an_ordinary_carrier_with_the_real_nonce_still_passes(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h1p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        a = rec["attempts"][0]
        self.assertTrue(a["nonce_present"])
        self.assertTrue(a["nonce_present_raw_stdout"])

    def test_H1_boundary_a_real_U_FFFD_carrier_still_matches(self):
        """The byte check is not over-strict: an actually-emitted U+FFFD (EF BF BD) still matches."""
        line = json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "\ufffd"}},
                          ensure_ascii=False).encode("utf-8") + b"\n"
        p, rec, _ = self._run_raw(line, "\ufffd")
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertTrue(rec["attempts"][0]["nonce_present"])
        self.assertTrue(rec["attempts"][0]["nonce_present_raw_stdout"])

    # --- H2: the usage status is validated STRICTLY --------------------------------------------
    def test_H2_unit_status_shapes(self):
        entry = {"provider": "opencode-go", "model": "deepseek-v4.1-flash"}
        ok = {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200}
        self.assertEqual(disp.receipt_reject_reason(entry, ok), "")
        self.assertTrue(disp.receipt_matches(entry, ok))
        for bad in (200.0, 200.9, "200", True, False, None, [], {}, 199, 201):
            self.assertNotEqual(disp.receipt_reject_reason(entry, dict(ok, status=bad)), "", bad)
            self.assertFalse(disp.receipt_matches(entry, dict(ok, status=bad)), bad)
        # the reason is recorded, never empty for a rejected row
        self.assertTrue(disp.receipt_reject_reason(entry, dict(ok, status=200.9)))

    def test_H2_negative_a_fractional_status_is_not_a_usage_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h2-"))
        env = _stub_env(tmp)
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200.9})
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=env)
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        a = rec["attempts"][0]
        self.assertIsNot(a["usage_receipt_ok"], True)
        self.assertEqual(a["usage_status"], 200.9)
        self.assertTrue(a["usage_receipt_reason"])

    def test_H2_positive_an_integer_200_is_still_a_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h2p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertTrue(rec["attempts"][0]["usage_receipt_ok"])

    # --- H3: a truncated ledger must not revive a stale row -------------------------------------
    def test_H3_unit_a_shrunken_ledger_yields_no_rows(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h3u-"))
        led = tmp / "usage.jsonl"
        led.write_text("stale\n", encoding="utf-8")
        self.assertEqual(disp.usage_rows_since(led, led.stat().st_size + 500), [])

    def test_H3_negative_a_truncated_ledger_cannot_revive_a_stale_row(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h3-"))
        scratch = tmp / "usage.jsonl"
        stale = json.dumps({"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200})
        scratch.write_text(stale + "\n" + ("# padding line to lengthen the ledger\n" * 20),
                           encoding="utf-8")
        stub = tmp / "trunc_stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "b = led.read_bytes()\n"
            "led.write_bytes(b.split(b'\\n')[0] + b'\\n')\n"
            "print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
            " 'text': 'TRUNC HGK_LANE_NONCE_OK'}}))\n"
            "sys.exit(0)\n", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_TARGET"] = str(scratch)
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_USAGE_LINE"] = stale
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(stub), "--usage", str(scratch), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=env)
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["usage_receipt_ok"], True)
        self.assertTrue(rec["attempts"][0]["usage_ledger_rewritten"])
        # J4 (pass-6): the top-level code is the requirement's generic exhausted code. The rewritten
        # ledger is a per-attempt DETAIL (`usage_ledger_rewritten` + `usage_receipt_reason`), never a
        # top-level code -- a diagnostic can never outrank the frozen requirement's classification.
        self.assertEqual(rec["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertNotEqual(rec["code"], disp.ERR_USAGE_LEDGER_REWRITTEN)

    def test_H3_positive_an_appended_row_still_binds(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h3p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertFalse(rec["attempts"][0]["usage_ledger_rewritten"])

    # --- H4: per-root guard validation + an inconclusive empty comparison ------------------------
    def test_H4_unit_an_empty_comparison_is_inconclusive(self):
        d = disp.diff_subject({}, {})
        self.assertTrue(d["inconclusive"])
        self.assertFalse(d["mutated_known"])
        self.assertEqual(d["verdict"], "INCONCLUSIVE")
        self.assertTrue(d["inconclusive_reason"])
        # the point of the marker: nothing about this comparison licenses a CLEAN verdict
        self.assertNotEqual(d["verdict"], "CLEAN")

    def test_H4_boundary_a_measured_removal_still_voids(self):
        """An empty `after` that follows a real removal is VOID, not INCONCLUSIVE."""
        d = disp.diff_subject({"a": "h"}, {})
        self.assertTrue(d["mutated"])
        self.assertEqual(d["verdict"], "VOID")
        self.assertTrue(d["removed"])

    def test_H4_negative_an_empty_root_is_refused_even_with_a_non_empty_sibling(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h4-"))
        empty = tmp / "empty-root"
        empty.mkdir()
        nonempty = tmp / "nonempty.txt"
        nonempty.write_text("x", encoding="utf-8")
        pool = _hermetic_verify_pool(tmp)
        p, rec, _ = _run_dispatch(["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool),
                                   "--guard-subject", str(empty), "--guard-subject", str(nonempty),
                                   "--prompt", "x"])
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_GUARD_ROOT_EMPTY")
        self.assertIn(str(empty), rec["empty_guard_roots"])
        self.assertNotIn("attempts", rec)

    def test_H4_positive_two_non_empty_roots_still_compare(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h4p-"))
        a = tmp / "a.txt"
        b = tmp / "b.txt"
        a.write_text("1", encoding="utf-8")
        b.write_text("2", encoding="utf-8")
        pool = _hermetic_verify_pool(tmp)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1", "--pool", str(pool),
               "--guard-subject", str(a), "--guard-subject", str(b),
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["subject_mutation"]["files_before"], 2)
        self.assertFalse(rec["subject_mutation"]["inconclusive"])

    # --- H5: a wrong-shaped carrier yields a TYPED refusal, not a crash -------------------------
    def test_H5_unit_a_wrong_shaped_carrier_yields_no_text_and_no_crash(self):
        for carrier in ('{"type": "item.completed", "item": true}',
                        '{"type": "item.completed", "item": 5}',
                        '{"type": "item.completed", "item": "x"}',
                        '{"type": "item.completed", "item": [1, 2]}'):
            self.assertEqual(disp.agent_message_texts(carrier), [], carrier)
            self.assertFalse(disp.nonce_in_agent_message(carrier, "HGK_LANE_NONCE_OK"), carrier)

    def test_H5_negative_a_wrong_shaped_carrier_produces_a_typed_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h5-"))
        stub = tmp / "bad_shape_stub.py"
        stub.write_text("import sys\n"
                        "sys.stdout.write('{\"type\": \"item.completed\", \"item\": true}' + chr(10))\n"
                        "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(stub), "--usage", str(tmp / "usage.jsonl"),
                                   "--timeout", "30", "--prompt", "x"], env=_stub_env(tmp))
        self.assertIsNotNone(rec, p.stdout + p.stderr)     # a receipt exists: no uncaught crash
        self.assertIsNot(rec["ok"], True)
        self.assertTrue(rec["code"])
        # J4 (pass-6): no arm produced an acceptable turn (no usage row at all), so the top-level code
        # is the requirement's GENERIC exhausted code. The carrier-shape diagnostic is recorded as a
        # per-attempt DETAIL (`carrier_shape_invalid`), never as the top-level code.
        self.assertEqual(rec["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertTrue(rec["attempts"][0]["carrier_shape_invalid"])
        self.assertEqual(p.returncode, 3, p.stdout + p.stderr)

    def test_H5_positive_a_well_shaped_carrier_still_passes(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r4-h5p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertNotIn("carrier_shape_invalid", rec["attempts"][0])


class R5Repair(unittest.TestCase):
    """FAR-LANE-HEALTH-REPAIR-20261011 pass 5 -- the three findings a fourth independent VERIFY/SECURITY
    review of the PASS-4 bytes returned FAIL on. Every test is deterministic: a stub child, NO model,
    NO network, NO relay, NO real Codex home.

      I1  a ledger rewritten by CONTENT (prefix shifted, a stale row copied PAST the offset, file GROWS)
          must be detected -- a size-only check cannot see it
      I2  a USAGE ROW of a wrong shape (a nonempty array, `true`, a string, an integer) must be a typed
          rejection (skipped + COUNTED, with a receipt), never an AttributeError crash with no receipt
      I3  the frozen oracle's C1 classification TAKES PRECEDENCE over the pass-4 carrier-shape code
    """

    STUB = "tests/fixtures/stub_lane_child.py"

    def _run(self, cmd, *, env=None):
        return _run_dispatch(cmd, env=env)

    # --- I1: content-based rewrite detection ----------------------------------------------------
    def test_I1_unit_prefix_digest_is_content_sensitive(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i1u-"))
        led = tmp / "usage.jsonl"
        led.write_bytes(b"ABCDEFGHIJ")
        d5 = disp.usage_prefix_digest(led, 5)
        self.assertEqual(d5, hashlib.sha256(b"ABCDE").hexdigest())
        led.write_bytes(b"XBCDEFGHIJ")      # same SIZE, different content in [0:5)
        self.assertNotEqual(disp.usage_prefix_digest(led, 5), d5)

    def test_I1_negative_the_reviewers_shift_and_copy_cannot_yield_a_valid_receipt(self):
        """The exact control: seed a 255-byte ledger with an earlier matching row plus filler, then
        have the child prepend a space, shift every pre-offset byte, and copy the stale row PAST the
        offset. The file GROWS (255 -> 330); the size check sees nothing, so only the prefix digest
        catches it."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i1-"))
        scratch = tmp / "usage.jsonl"
        stale = json.dumps({"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200})
        # pad to exactly 255 bytes: the stale row + newline + filler
        body = (stale + "\n").encode("utf-8")
        scratch.write_bytes(body + b"#" * (255 - len(body)))
        self.assertEqual(scratch.stat().st_size, 255)
        stub = tmp / "shift_stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "ledger = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "old = ledger.read_bytes()\n"
            "stale = old.split(b'\\n')[0] + b'\\n'\n"
            "ledger.write_bytes(b' ' + old[1:] + stale)\n"
            "print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
            " 'text': 'SHIFT HGK_LANE_NONCE_OK'}}))\n"
            "sys.exit(0)\n", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_TARGET"] = str(scratch)
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_USAGE_LINE"] = stale
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(stub), "--usage", str(scratch),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=env)
        # the file GREW -- this is exactly what the size-only check could not see
        self.assertGreater(scratch.stat().st_size, 255)
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["usage_receipt_ok"], True)
        self.assertEqual(rec["attempts"][0]["usage_offset"], 255)
        self.assertTrue(rec["attempts"][0]["usage_ledger_rewritten"])
        # J2 (pass-6): the shifted ledger leaves byte offset-1 NOT a newline, so the region is a
        # continuation of a pre-existing line and yields ZERO rows (a partially/anchor-invalid region
        # is never mined for a row). The rewrite is still recorded as a per-attempt detail.
        self.assertEqual(rec["attempts"][0]["usage_rows_after_offset"], 0)
        # J4 (pass-6): the top-level code is the requirement's generic exhausted code, not the detail.
        self.assertEqual(rec["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertNotEqual(rec["code"], disp.ERR_USAGE_LEDGER_REWRITTEN)

    def test_I1_positive_an_ordinary_append_still_yields_a_valid_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i1p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertTrue(rec["attempts"][0]["usage_receipt_ok"])
        self.assertFalse(rec["attempts"][0]["usage_ledger_rewritten"])

    # --- I2: a wrong-shaped usage row is a typed rejection, not a crash -------------------------
    def test_I2_unit_row_shape_guard(self):
        for bad in ([1, 2], [], True, False, "200", 200, 200.0, None):
            self.assertFalse(disp.is_usage_row_shaped(bad), bad)
        self.assertTrue(disp.is_usage_row_shaped({"status": 200}))
        self.assertTrue(disp.is_usage_row_shaped({}))

    def test_I2_negative_every_wrong_shaped_row_yields_a_receipt_and_is_counted(self):
        """The reviewer supplied rows shaped as a nonempty array, `true`, a string and an integer:
        EACH exited 1 with NO receipt and an AttributeError. Each must now emit a typed receipt with
        the row COUNTED in `usage_rows_shape_invalid`."""
        for label, row in (("array", [1, 2]), ("bool", True), ("string", "200"), ("int", 200)):
            tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"hgk-r5-i2-{label}-"))
            scratch = tmp / "usage.jsonl"
            scratch.write_text("", encoding="utf-8")
            env = _stub_env(tmp)
            env["HGK_STUB_USAGE"] = str(scratch)
            env["HGK_STUB_USAGE_LINE"] = json.dumps(row)
            cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                   "--codex-executable", str(ROOT / self.STUB), "--usage", str(scratch),
                   "--timeout", "30", "--prompt", "x"]
            p, rec, _ = self._run(cmd, env=env)
            self.assertIsNotNone(rec, f"{label}: no receipt was written\n{p.stdout + p.stderr}")
            self.assertIsNot(rec["ok"], True, label)
            self.assertTrue(rec.get("code"), label)
            self.assertEqual(rec["usage_rows_shape_invalid"], 1, label)
            self.assertEqual(rec["attempts"][0]["usage_rows_shape_invalid"], 1, label)
            self.assertIsNot(rec["attempts"][0]["usage_receipt_ok"], True, label)
            # it is NOT a real receipt and NOT a clean pass
            self.assertNotEqual(p.returncode, 0, label)

    def test_I2_positive_a_well_shaped_row_is_still_a_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i2p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["usage_rows_shape_invalid"], 0)

    # --- I3: the frozen oracle's C1 classification takes precedence -----------------------------
    def test_I3_unit_nonced_absent_classification_precedes_the_shape_code(self):
        """Direct on failure_disposition: an answered attempt with a wrong-shaped carrier and no nonce
        is ERR_NO_ARM_EMITTED_NONCE + nonce_absent_arms, whatever the carrier shape was."""
        a = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash", "exit": 0,
              "usage_receipt_ok": True, "nonce_present": False, "carrier_shape_invalid": True}]
        d = disp.failure_disposition(a)
        self.assertEqual(d["code"], "ERR_NO_ARM_EMITTED_NONCE")
        self.assertEqual(d["nonce_absent_arms"], ["opencode-go/deepseek-v4.1-flash"])
        self.assertNotEqual(d["code"], disp.ERR_CARRIER_SHAPE_INVALID)
        # and the shape code does apply when NO arm produced an acceptable turn
        b = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash", "exit": 0,
              "usage_receipt_ok": False, "nonce_present": False, "carrier_shape_invalid": True}]
        # J4 (pass-6): the shape diagnostic is a per-attempt DETAIL, never a top-level code. When NO
        # arm produced an acceptable turn the requirement's GENERIC exhausted code is used.
        self.assertEqual(disp.failure_disposition(b)["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertNotEqual(disp.failure_disposition(b)["code"], disp.ERR_CARRIER_SHAPE_INVALID)

    def test_I3_negative_the_reviewers_exact_control_reads_the_C1_classification(self):
        """Wrong-shaped carrier (`item:true`) + a separately verified matching integer-200 usage row +
        no nonce anywhere -> ERR_NO_ARM_EMITTED_NONCE with nonce_absent_arms, NOT the shape code."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i3-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_text("", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_USAGE"] = str(scratch)
        # usage line tracks the VERIFY rank-1 arm from the pool file (single source of truth;
        # the stub answers AS the arm the dispatcher will pick on --force-rank 1)
        slots_doc = json.loads((ROOT / "config" / "lane-route-slots.candidate.json").read_text(encoding="utf-8"))
        v_lane = next(l for l in slots_doc["lanes"] if l["lane"] == "EXECUTE")
        v_r1 = v_lane["ordered_pool"][0]
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": v_r1["provider"], "model": v_r1["model"], "status": 200})
        stub = tmp / "bad_carrier_stub.py"
        # the child appends a SEPARATELY VALID integer-200 usage row AND emits a wrong-shaped carrier,
        # exactly as the reviewer's control did.
        stub.write_text("import json, os, pathlib, sys\n"
                        "p = pathlib.Path(os.environ['HGK_STUB_USAGE'])\n"
                        "p.parent.mkdir(parents=True, exist_ok=True)\n"
                        "p.write_text(json.dumps(json.loads(os.environ['HGK_STUB_USAGE_LINE'])) + chr(10),"
                        " encoding='utf-8')\n"
                        "sys.stdout.write('{\"type\": \"item.completed\", \"item\": true}' + chr(10))\n"
                        "sys.exit(0)\n", encoding="utf-8")
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "A-NONCE-THE-CHILD-WILL-NOT-EMIT",
               "--codex-executable", str(stub), "--usage", str(scratch), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=env)
        self.assertFalse(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE", p.stdout + p.stderr)
        self.assertEqual(rec["nonce_absent_arms"], ["opencode-go/deepseek-v4.1-flash"])
        # the usage MEASUREMENT is not overwritten by the shape diagnostic
        self.assertTrue(rec["attempts"][0]["usage_receipt_ok"], rec["attempts"][0])
        self.assertTrue(rec["attempts"][0]["carrier_shape_invalid"])

    def test_I3_boundary_a_wrong_shaped_carrier_with_no_valid_receipt_does_not(self):
        """A wrong-shaped carrier with NO valid usage receipt must NOT read ERR_NO_ARM_EMITTED_NONCE,
        and must NOT promote the carrier-shape diagnostic to a top-level code (J4): the requirement's
        generic exhausted code is used, with the shape recorded as a per-attempt detail."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i3b-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_text("", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_USAGE"] = str(scratch)
        stub = tmp / "bad_carrier_stub.py"
        stub.write_text("import sys\n"
                        "sys.stdout.write('{\"type\": \"item.completed\", \"item\": true}' + chr(10))\n"
                        "sys.exit(0)\n", encoding="utf-8")
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(stub), "--usage", str(scratch), "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=env)
        self.assertFalse(rec["ok"], p.stdout + p.stderr)
        self.assertNotEqual(rec["code"], "ERR_NO_ARM_EMITTED_NONCE")
        self.assertEqual(rec["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")
        self.assertNotEqual(rec["code"], disp.ERR_CARRIER_SHAPE_INVALID)
        self.assertTrue(rec["attempts"][0]["carrier_shape_invalid"])
        self.assertIsNot(rec["attempts"][0]["usage_receipt_ok"], True)

    def test_I3_positive_a_conforming_turn_is_unaffected(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r5-i3p-"))
        cmd = ["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
               "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = self._run(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertNotIn("carrier_shape_invalid", rec["attempts"][0])


class R6Repair(unittest.TestCase):
    """FAR-LANE-HEALTH-REPAIR-20261011 pass 6 -- the CLASS-LEVEL repairs J1-J4. Five
    instance-by-instance passes did not close the class, so this pass closes it by construction:

      J1  strict decoding EVERYWHERE: a ledger line that is not valid UTF-8 is skipped and COUNTED
          (`usage_rows_undecodable`); it is never substituted (no U+FFFD) and never compared
      J2  only COMPLETE, line-boundary-anchored lines are evidence: a non-line-boundary offset or an
          unterminated tail yields ZERO rows
      J3  exact typing, no coercion: a `str` field equals only a `str` (JSON integer 7 != "7")
      J4  the requirement's precedence table owns the TOP-LEVEL code; the carrier-shape and
          rewritten-ledger diagnostics are per-attempt DETAILS, never codes

    Every test is deterministic: a stub child, NO model, NO network, NO relay, NO real Codex home.
    """

    STUB = "tests/fixtures/stub_lane_child.py"

    # --- J1: strict decoding everywhere ---------------------------------------------------------
    def test_J1_unit_an_undecodable_line_is_skipped_and_counted(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j1u-"))
        led = tmp / "usage.jsonl"
        good = json.dumps({"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200})
        led.write_bytes(good.encode("utf-8") + b"\n"
                        + b'{"provider":"opencode-go","model":"deepseek-v4.1-flash","status":200,"n":"\xff"}\n')
        spans = disp.usage_spans_since(led, 0)
        rows, undecodable = disp.decode_usage_spans(spans)
        self.assertEqual(len(rows), 1)                 # only the valid line is a row
        self.assertEqual(undecodable, 1)               # the invalid-UTF-8 line is counted, not substituted
        # the decoded row set contains NO U+FFFD-derived value
        self.assertNotIn("\ufffd", json.dumps(rows))

    def test_J1_negative_an_invalid_utf8_ledger_line_is_never_a_receipt(self):
        """The reviewer's exact control: the ONLY appended row is invalid UTF-8, so strict decoding
        finds ZERO rows and the turn cannot be a receipt."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j1-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "utf8bad_stub.py"
        stub.write_text("import json, os, pathlib, sys\n"
                        "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
                        "led.write_bytes(b'{\"provider\":\"opencode-go\",\"model\":"
                        "\"deepseek-v4.1-flash\",\"status\":200,\"note\":\"\\xff\"}' + b'\\n')\n"
                        "print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
                        " 'text': 'UTF8BAD HGK_LANE_NONCE_OK'}}))\n"
                        "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(stub), "--usage", str(scratch),
                                   "--timeout", "30", "--prompt", "x"], env={"HGK_STUB_TARGET": str(scratch)})
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["usage_receipt_ok"], True)
        self.assertEqual(rec["usage_rows_undecodable"], 1)
        self.assertEqual(rec["attempts"][0]["usage_rows_after_offset"], 0)

    def test_J1_positive_a_valid_utf8_row_is_still_a_receipt(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j1p-"))
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
                                   "--timeout", "30", "--prompt", "x"], env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["usage_rows_undecodable"], 0)

    # --- J2: only complete lines are evidence ---------------------------------------------------
    def test_J2_unit_offset_inside_a_line_yields_no_rows(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j2u-"))
        led = tmp / "usage.jsonl"
        led.write_bytes(b'{"unfinished":' + json.dumps(
            {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "status": 200}).encode() + b"\n")
        # the offset at 14 sits INSIDE the first (unterminated) line: byte 13 is not a newline
        self.assertEqual(disp.usage_spans_since(led, 14), [])
        # a clean offset (0) still reads the trailing complete line
        self.assertEqual(len(disp.usage_spans_since(led, 0)), 1)

    def test_J2_unit_an_unterminated_tail_is_not_a_line(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j2t-"))
        led = tmp / "usage.jsonl"
        led.write_bytes(b'{"a":1}\n{"unterminated":')
        spans = disp.usage_spans_since(led, 0)
        self.assertEqual(len(spans), 1)                # the complete line only
        self.assertEqual(spans[0][1], b'{"a":1}')

    def test_J2_negative_an_unfinished_prefix_is_not_a_receipt(self):
        """The reviewer initialized the ledger with exactly `b'{"unfinished":'` (no newline), then the
        stub appended its normal matching row. The appended suffix is a continuation of the unfinished
        line, so it is NOT a row."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j2-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b'{"unfinished":')
        self.assertEqual(scratch.stat().st_size, 14)
        env = _stub_env(tmp)
        env["HGK_STUB_USAGE"] = str(scratch)
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(ROOT / self.STUB), "--usage", str(scratch),
                                   "--timeout", "30", "--prompt", "x"], env=env)
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["usage_receipt_ok"], True)
        self.assertEqual(rec["attempts"][0]["usage_rows_after_offset"], 0)
        self.assertEqual(rec["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")

    def test_J2_positive_a_complete_line_after_a_newline_still_binds(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j2p-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_text("", encoding="utf-8")
        env = _stub_env(tmp)
        env["HGK_STUB_USAGE"] = str(scratch)
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(ROOT / self.STUB), "--usage", str(scratch),
                                   "--timeout", "30", "--prompt", "x"], env=env)
        self.assertTrue(rec["ok"], p.stdout + p.stderr)

    # --- J3: exact typing, no coercion ----------------------------------------------------------
    def test_J3_unit_type_mismatch_is_rejected(self):
        entry = {"provider": "opencode-go", "model": "7"}
        # a JSON integer 7 must NOT equal the declared string "7"
        self.assertNotEqual(disp.receipt_reject_reason(
            entry, {"provider": "opencode-go", "model": 7, "status": 200}), "")
        self.assertFalse(disp.receipt_matches(
            entry, {"provider": "opencode-go", "model": 7, "status": 200}))
        # the genuinely-string "7" DOES match
        self.assertEqual(disp.receipt_reject_reason(
            entry, {"provider": "opencode-go", "model": "7", "status": 200}), "")
        # a non-string provider can never alias into a match
        self.assertNotEqual(disp.receipt_reject_reason(
            {"provider": "openai-codex", "model": "m"},
            {"provider": 7, "model": "m", "status": 200}), "")

    def test_J3_negative_a_json_integer_model_never_matches_a_string_model(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j3-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "intmodel_stub.py"
        stub.write_text("import json, os, pathlib, sys\n"
                        "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
                        "with led.open('a', encoding='utf-8') as fh:\n"
                        "    fh.write(json.dumps({'provider': 'opencode-go', 'model': 7, 'status': 200})"
                        " + chr(10))\n"
                        "print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
                        " 'text': 'INTMODEL HGK_LANE_NONCE_OK'}}))\n"
                        "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(stub), "--usage", str(scratch),
                                   "--timeout", "30", "--prompt", "x"], env={"HGK_STUB_TARGET": str(scratch)})
        self.assertIsNot(rec["usage_receipt_ok"], True, p.stdout + p.stderr)

    # --- J4: the requirement's precedence table owns the top-level code --------------------------
    def test_J4_unit_acceptable_turn_and_no_nonce_is_the_C1_code(self):
        a = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash", "exit": 0,
              "usage_receipt_ok": True, "nonce_present": False, "carrier_shape_invalid": True}]
        d = disp.failure_disposition(a)
        self.assertEqual(d["code"], "ERR_NO_ARM_EMITTED_NONCE")
        self.assertEqual(d["nonce_absent_arms"], ["opencode-go/deepseek-v4.1-flash"])

    def test_J4_unit_no_acceptable_turn_is_always_the_generic_code(self):
        # every shape that is NOT "an acceptable turn" collapses to the generic code, and the shape/
        # rewrite diagnostics are never promoted to a code
        cases = [
            [],
            [{"rank": 1, "provider": "p", "model": "m", "exit": 0, "usage_receipt_ok": False,
              "nonce_present": False, "carrier_shape_invalid": True}],
            [{"rank": 1, "provider": "p", "model": "m", "exit": 0, "usage_receipt_ok": False,
              "nonce_present": False, "usage_ledger_rewritten": True}],
            [{"rank": 1, "provider": "p", "model": "m", "exit": "TIMEOUT", "usage_receipt_ok": False,
              "nonce_present": False}],
            [{"rank": 1, "provider": "p", "model": "m", "exit": 1, "usage_receipt_ok": False,
              "nonce_present": False}],
        ]
        for i, a in enumerate(cases):
            d = disp.failure_disposition(a)
            self.assertEqual(d["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED", f"case {i}: {d}")
            self.assertNotEqual(d.get("code"), disp.ERR_CARRIER_SHAPE_INVALID, f"case {i}")
            self.assertNotEqual(d.get("code"), disp.ERR_USAGE_LEDGER_REWRITTEN, f"case {i}")

    def test_J4_positive_a_conforming_turn_still_reports_ok(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r6-j4p-"))
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(ROOT / self.STUB), "--usage", str(tmp / "usage.jsonl"),
                                   "--timeout", "30", "--prompt", "x"], env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertNotIn("code", rec)


class R7StrictDeclaration(unittest.TestCase):
    """FAR-STRICT-DECLARATION-20261011 (REQ-STRICT-DECLARATION-014) -- S1/S2/S3.

    The operative rule: a declared value is admitted only at its EXACT JSON type, and a record counts
    as evidence only when it is a COMPLETE, LF/CRLF-terminated, strictly UTF-8-decodable JSON value
    read in full. Every test here is deterministic: a scratch pool artifact, a scratch ledger and a
    deterministic stub child. NO model, NO network, NO relay, NO real Codex home.
    """

    @staticmethod
    def _resolver():
        import hg_kseos.lane_route_resolver as L
        return L

    def _load(self, entry):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r7-pool-"))
        L = self._resolver()
        doc = {"schema": L.SCHEMA, "status": "CANDIDATE",
               "lanes": [{"lane": "EXECUTE", "transport": "t", "engine": "e", "ordered_pool": [entry]}]}
        p = tmp / "pool.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        return L.load_pool(str(p))

    # --- S1: the resolver refuses a wrongly-typed declaration, never coercing it -----------------
    def test_S1_unit_the_type_guard_excludes_bool_from_int(self):
        L = self._resolver()
        self.assertEqual(L._require_json_int(3, "e", "rank"), 3)
        for bad in (True, False):
            with self.assertRaises(L.LaneRouteError) as cm:
                L._require_json_int(bad, "e", "rank")
            self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE)
        for bad in (1.9, "1", None, [1], {}):
            with self.assertRaises(L.LaneRouteError) as cm:
                L._require_json_int(bad, "e", "rank")
            self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE)

    def test_S1_negative_a_wrongly_typed_rank_is_a_TYPE_refusal(self):
        L = self._resolver()
        for bad in (1.9, "1", True, None, [1]):
            with self.assertRaises(L.LaneRouteError) as cm:
                self._load({"rank": bad, "provider": "opencode-go", "model": "deepseek-v4.1-flash"})
            self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE, bad)

    def test_S1_negative_a_wrongly_typed_provider_or_model_is_a_TYPE_refusal(self):
        L = self._resolver()
        for entry in ({"rank": 1, "provider": "opencode-go", "model": 7},
                      {"rank": 1, "provider": True, "model": "deepseek-v4.1-flash"},
                      {"rank": 1, "provider": "opencode-go", "model": None},
                      {"rank": 1, "provider": "", "model": "deepseek-v4.1-flash"},
                      {"rank": 1, "provider": "opencode-go", "model": ""}):
            with self.assertRaises(L.LaneRouteError) as cm:
                self._load(entry)
            self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE, entry)

    def test_S1_negative_a_present_but_non_string_optional_field_is_a_TYPE_refusal(self):
        L = self._resolver()
        with self.assertRaises(L.LaneRouteError) as cm:
            self._load({"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash", "role": 5})
        self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE)

    def test_S1_a_missing_key_keeps_the_MALFORMED_code_not_the_type_code(self):
        L = self._resolver()
        with self.assertRaises(L.LaneRouteError) as cm:
            self._load({"rank": 1, "provider": "opencode-go"})      # no model
        self.assertEqual(cm.exception.code, "ERR_SLOT_POOL_ENTRY_MALFORMED")

    def test_S1_positive_a_well_typed_pool_takes_the_identical_path(self):
        lanes = self._load({"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash"})
        e = lanes["EXECUTE"][0]
        self.assertEqual((e.rank, e.provider, e.model, e.transport, e.engine),
                         (1, "opencode-go", "deepseek-v4.1-flash", "t", "e"))
        # an ABSENT optional field is still admitted (present-but-wrong is the defect, absent is fine)
        lanes2 = self._load({"rank": 1, "provider": "nvidia", "model": "m", "role": "r"})
        self.assertEqual(lanes2["EXECUTE"][0].role, "r")

    # --- S2: the dispatcher's raw-pool read applies the same typing (no int() coercion) ----------
    @staticmethod
    def _pool_doc(entry):
        return {"schema": "HGK-LANE-ROUTE-SLOTS/1", "status": "CANDIDATE",
                "lanes": [{"lane": "EXECUTE", "transport": "t", "engine": "e", "ordered_pool": [entry]}]}

    def _dispatch_with_pool(self, entry, prefix):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
        pool = tmp / "pool.json"
        pool.write_text(json.dumps(self._pool_doc(entry)), encoding="utf-8")
        return _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--pool", str(pool),
                              "--codex-executable", str(ROOT / "tests" / "fixtures" / "stub_lane_child.py"),
                              "--usage", str(tmp / "usage.jsonl"), "--prompt", "x"], env=_stub_env(tmp))

    def test_S2_negative_a_fractional_rank_pool_is_refused_with_no_attempt(self):
        p, rec, _ = self._dispatch_with_pool(
            {"rank": 1.9, "provider": "opencode-go", "model": "deepseek-v4.1-flash"}, "hgk-r7-s2-")
        self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        out = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertIsNot(out.get("ok"), True)
        self.assertFalse(out.get("attempts"), out.get("attempts"))
        self.assertEqual(out["code"], self._resolver().ERR_SLOT_POOL_ENTRY_TYPE)

    def test_S2_negative_a_boolean_rank_pool_is_refused_with_no_attempt(self):
        p, rec, _ = self._dispatch_with_pool(
            {"rank": True, "provider": "opencode-go", "model": "deepseek-v4.1-flash"}, "hgk-r7-s2b-")
        self.assertNotEqual(p.returncode, 0)
        out = json.loads(p.stdout.strip().splitlines()[-1])
        self.assertFalse(out.get("attempts"))
        self.assertEqual(out["code"], self._resolver().ERR_SLOT_POOL_ENTRY_TYPE)

    def test_S2_positive_an_integer_rank_pool_still_dispatches(self):
        p, rec, _ = self._dispatch_with_pool(
            {"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash"}, "hgk-r7-s2p-")
        self.assertTrue(rec["ok"], p.stdout + p.stderr)

    # --- S3: only a complete, LF/CRLF-terminated, strictly-UTF-8 JSON line counts -----------------
    def test_S3_unit_unterminated_tail_is_not_a_row(self):
        self.assertEqual(disp.carrier_line_texts(b'{"a":1}\n{"b":2}'), (['{"a":1}'], 0))

    def test_S3_unit_crlf_is_terminated_and_one_cr_is_stripped(self):
        self.assertEqual(disp.carrier_line_texts(b'{"a":1}\r\n'), (['{"a":1}'], 0))

    def test_S3_unit_invalid_utf8_line_is_dropped_and_counted(self):
        texts, undecodable = disp.carrier_line_texts(b'{"a":1}\n' + b'{"b":"\xff"}\n')
        self.assertEqual(texts, ['{"a":1}'])
        self.assertEqual(undecodable, 1)

    def test_S3_unit_a_u2028_separator_does_not_invent_a_line_boundary(self):
        # U+2028 = E2 80 A8; str.splitlines() would split here, bytes split on b"\n" must not.
        raw = '{"a":1}\u2028{"b":2}'.encode("utf-8")
        self.assertEqual(disp.carrier_line_texts(raw), ([], 0))

    def test_S3_unit_the_non_string_argument_is_rejected_not_silently_accepted(self):
        with self.assertRaises(TypeError):
            disp.carrier_line_texts(12345)

    def _carrier_run(self, term_expr, text, prefix):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "led.write_text(json.dumps({'provider': 'opencode-go', 'model': 'deepseek-v4.1-flash',"
            " 'status': 200}) + chr(10), encoding='utf-8')\n"
            "sys.stdout.write(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
            " 'text': '" + text + "'}}) + " + term_expr + ")\n"
            "sys.exit(0)\n", encoding="utf-8")
        return _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                              "--codex-executable", str(stub), "--usage", str(scratch), "--prompt", "x"],
                             env={"HGK_STUB_TARGET": str(scratch)})

    def test_S3_negative_a_u2028_terminated_carrier_does_not_succeed(self):
        p, rec, _ = self._carrier_run("chr(0x2028)", "U2028 HGK_LANE_NONCE_OK", "hgk-r7-s3-")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_S3_negative_an_unterminated_carrier_does_not_succeed(self):
        p, rec, _ = self._carrier_run("''", "UNTERM HGK_LANE_NONCE_OK", "hgk-r7-s3u-")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_S3_negative_an_invalid_utf8_carrier_line_is_counted_and_does_not_succeed(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r7-s3b-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "badutf8_stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "led.write_text(json.dumps({'provider': 'opencode-go', 'model': 'deepseek-v4.1-flash',"
            " 'status': 200}) + chr(10), encoding='utf-8')\n"
            "sys.stdout.buffer.write(b'{\"type\":\"item.completed\",\"item\":{\"type\":"
            "\"agent_message\",\"text\":\"BAD \\xff HGK_LANE_NONCE_OK\"}}' + b'\\n')\n"
            "sys.stdout.buffer.flush()\n"
            "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                                   "--codex-executable", str(stub), "--usage", str(scratch), "--prompt", "x"],
                                  env={"HGK_STUB_TARGET": str(scratch)})
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)
        self.assertEqual(rec["attempts"][0]["carrier_lines_undecodable"], 1)

    def test_S3_positive_lf_and_crlf_carriers_both_succeed(self):
        for label, term in (("LF", "chr(10)"), ("CRLF", "chr(13) + chr(10)")):
            p, rec, _ = self._carrier_run(term, label + " HGK_LANE_NONCE_OK", f"hgk-r7-s3p-{label}-")
            self.assertTrue(rec["ok"], f"{label}: {p.stdout + p.stderr}")
            self.assertEqual(rec["attempts"][0]["carrier_lines_undecodable"], 0, label)


class R8StrictDeclarationPass2(unittest.TestCase):
    """FAR-STRICT-DECLARATION-20261011 pass 2 (REQ-STRICT-DECLARATION-014) -- T1/T2/T3.

    Pass 1 was green on its own gates, but five further carrier shapes still reported success. Each
    test here locks one of the three mechanisms behind those five shapes:
      T1  the line's bytes are the bytes between the terminators: NO unrestricted pre-cleaning strip,
          only at most ONE trailing CR may be removed (so CRLF still parses).
      T2  a strict JSON parse rejects the non-JSON constants NaN / Infinity / -Infinity.
      T3  text containing a surrogate code point (U+D800-U+DFFF) never decides a verdict: skip+count.
    Every test is deterministic: a scratch ledger and a deterministic stub child. NO model, NO network,
    NO relay, NO real Codex home.
    """

    # --- T2 unit: the strict parse rejects the non-JSON constants ---------------------------------
    def test_T2_unit_naN_infinity_minus_infinity_raise(self):
        for text in ("NaN", "Infinity", "-Infinity", '{"a": NaN}', '{"a": Infinity}',
                     '{"a": -Infinity}'):
            with self.assertRaises(ValueError, msg=text):
                disp.strict_json_loads(text)
        # ordinary JSON -- including its own insignificant whitespace -- still parses (no over-block)
        self.assertEqual(disp.strict_json_loads('  {"a": 1} \t\r\n'), {"a": 1})
        self.assertEqual(disp.strict_json_loads("[1, 2, 3]"), [1, 2, 3])

    def test_T2_unit_the_resolver_strict_parse_also_rejects_them(self):
        import hg_kseos.lane_route_resolver as L
        with self.assertRaises(ValueError):
            L._strict_json_loads('{"schema": NaN}')

    # --- T1 unit: only ONE trailing CR is removed; no other byte is pre-cleaned --------------------
    def test_T1_unit_only_one_trailing_cr_is_removed(self):
        self.assertEqual(disp.carrier_line_texts(b'{"a":1}\r\n'), (['{"a":1}'], 0))
        # TWO trailing CRs: the first is removed, the second reaches the parser and makes it fail
        self.assertEqual(disp.carrier_line_texts(b'{"a":1}\r\r\n'), (['{"a":1}\r'], 0))

    def test_T1_unit_the_line_is_not_stripped(self):
        # a trailing U+2028, a leading NEL (U+0085) and a trailing vertical tab (U+000B) are NOT JSON
        # whitespace and must survive to the parser (which will reject them). They must NOT be deleted.
        for raw in ('{"a":1}\u2028\n'.encode("utf-8"),
                    '\u0085{"a":1}\n'.encode("utf-8"),
                    '{"a":1}\u000b\n'.encode("utf-8")):
            texts, undecodable = disp.carrier_line_texts(raw)
            self.assertEqual(undecodable, 0)
            self.assertEqual(len(texts), 1)
            with self.assertRaises(ValueError):
                disp.strict_json_loads(texts[0])

    def test_T1_unit_an_empty_line_is_dropped_without_any_strip(self):
        self.assertEqual(disp.carrier_line_texts(b'\n\n{"a":1}\n'), (['{"a":1}'], 0))

    # --- T3 unit: a surrogate-bearing text is skipped and counted ---------------------------------
    def test_T3_unit_has_surrogate(self):
        self.assertTrue(disp.has_surrogate("\ud800"))
        self.assertTrue(disp.has_surrogate("ok \udfff tail"))
        self.assertFalse(disp.has_surrogate("ordinary \u00e9 text"))
        self.assertFalse(disp.has_surrogate(""))

    def test_T3_unit_a_surrogate_escaped_carrier_yields_no_text_and_is_counted(self):
        # json.loads turns the escape \ud800 into a lone surrogate code point in the decoded text
        carrier = ('{"type":"item.completed","item":{"type":"agent_message",'
                   '"text":"surrogate \\ud800 HGK_LANE_NONCE_OK"}}\n')
        disp.reset_carrier_surrogate_count()
        self.assertEqual(disp.agent_message_texts(carrier), [])
        self.assertEqual(disp.carrier_surrogate_count(), 1)
        self.assertFalse(disp.nonce_in_agent_message(carrier, "HGK_LANE_NONCE_OK"))
        # a carrier with a real (non-surrogate) astral character is still extracted (no over-block)
        good = ('{"type":"item.completed","item":{"type":"agent_message",'
                '"text":"astral \U0001F600 HGK_LANE_NONCE_OK"}}\n')
        disp.reset_carrier_surrogate_count()
        self.assertEqual(disp.agent_message_texts(good), ["astral \U0001F600 HGK_LANE_NONCE_OK"])
        self.assertEqual(disp.carrier_surrogate_count(), 0)

    def test_T3_unit_the_resolver_rejects_a_declared_surrogate_string(self):
        import hg_kseos.lane_route_resolver as L
        with self.assertRaises(L.LaneRouteError) as cm:
            L._require_json_string("bad\ud800", "e", "provider")
        self.assertEqual(cm.exception.code, L.ERR_SLOT_POOL_ENTRY_TYPE)

    # --- end-to-end: the five measured false successes (P29-P33) -----------------------------------
    def _carrier_run(self, term_expr, text, prefix):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix=prefix))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "led.write_text(json.dumps({'provider': 'opencode-go', 'model': 'deepseek-v4.1-flash',"
            " 'status': 200}) + chr(10), encoding='utf-8')\n"
            "sys.stdout.write(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message',"
            " 'text': '" + text + "'}}) + " + term_expr + ")\n"
            "sys.exit(0)\n", encoding="utf-8")
        return _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce", "HGK_LANE_NONCE_OK",
                              "--codex-executable", str(stub), "--usage", str(scratch), "--prompt", "x"],
                             env={"HGK_STUB_TARGET": str(scratch)})

    def test_T1_negative_a_trailing_u2028_carrier_does_not_succeed(self):
        p, rec, _ = self._carrier_run("chr(0x2028) + chr(10)", "U2028 HGK_LANE_NONCE_OK", "hgk-r8-t1a-")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_T1_negative_a_leading_nel_carrier_does_not_succeed(self):
        # a leading NEL (U+0085) is not JSON whitespace and must reach the parser unchanged (T1)
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r8-t1b-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "led.write_text(json.dumps({'provider': 'opencode-go', 'model': 'deepseek-v4.1-flash',"
            " 'status': 200}) + chr(10), encoding='utf-8')\n"
            "sys.stdout.write(chr(0x85) + json.dumps({'type': 'item.completed', 'item':"
            " {'type': 'agent_message', 'text': 'NEL HGK_LANE_NONCE_OK'}}) + chr(10))\n"
            "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce",
                                   "HGK_LANE_NONCE_OK", "--codex-executable", str(stub),
                                   "--usage", str(scratch), "--prompt", "x"],
                                  env={"HGK_STUB_TARGET": str(scratch)})
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_T1_negative_a_trailing_vertical_tab_carrier_does_not_succeed(self):
        p, rec, _ = self._carrier_run("chr(0x0b) + chr(10)", "VTAB HGK_LANE_NONCE_OK", "hgk-r8-t1c-")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_T2_negative_a_naN_payload_does_not_succeed(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-r8-t2-"))
        scratch = tmp / "usage.jsonl"
        scratch.write_bytes(b"")
        stub = tmp / "stub.py"
        stub.write_text(
            "import json, os, pathlib, sys\n"
            "led = pathlib.Path(os.environ['HGK_STUB_TARGET'])\n"
            "led.write_text(json.dumps({'provider': 'opencode-go', 'model': 'deepseek-v4.1-flash',"
            " 'status': 200}) + chr(10), encoding='utf-8')\n"
            "sys.stdout.write('{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\","
            "\"text\":\"HGK_LANE_NONCE_OK\"},\"extra\":NaN}' + chr(10))\n"
            "sys.exit(0)\n", encoding="utf-8")
        p, rec, _ = _run_dispatch(["--lane", "EXECUTE", "--force-rank", "1", "--nonce",
                                   "HGK_LANE_NONCE_OK", "--codex-executable", str(stub),
                                   "--usage", str(scratch), "--prompt", "x"],
                                  env={"HGK_STUB_TARGET": str(scratch)})
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)

    def test_T3_negative_an_escaped_surrogate_carrier_does_not_succeed_and_is_counted(self):
        p, rec, _ = self._carrier_run("chr(10)", "SURROGATE \\ud800 HGK_LANE_NONCE_OK", "hgk-r8-t3-")
        self.assertIsNot(rec["ok"], True, p.stdout + p.stderr)
        self.assertIsNot(rec["attempts"][0]["nonce_present"], True)
        self.assertEqual(rec["attempts"][0]["carrier_lines_surrogate"], 1)

    # --- no over-blocking control (P28) -----------------------------------------------------------
    def test_T1_T2_T3_positive_lf_crlf_and_ordinary_json_whitespace_still_succeed(self):
        for label, term in (("LF", "chr(10)"), ("CRLF", "chr(13) + chr(10)")):
            p, rec, _ = self._carrier_run(term, label + " HGK_LANE_NONCE_OK", f"hgk-r8-pos-{label}-")
            self.assertTrue(rec["ok"], f"{label}: {p.stdout + p.stderr}")
            self.assertEqual(rec["attempts"][0]["carrier_lines_surrogate"], 0)
            self.assertEqual(rec["attempts"][0]["carrier_lines_undecodable"], 0)


if __name__ == "__main__":
    unittest.main()
