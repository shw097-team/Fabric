"""Deterministic tests for the Phase C dispatch/authorization boundary
(round HGK-GCM-REPAIR-20261013, REQ-HGK-GCM-REPAIR-001).

Every test names the recorded defect it locks down:
  C1  two concurrent lanes (X3/X3b) wrote the SAME deliverable paths; an 8-line stream was
      overwritten by a 3-line one. -> derived per-attempt dirs + loud collision (exist_ok=False)
  C2  ONE authorized live-measurement window was consumed TWICE (2 vs 1) because a repair lane was
      dispatched before the prior attempt ended. -> single-use claim on the EXISTING Spine leases
      table (SharedSpine.acquire_lease / release_lease). A second concurrent claim MUST fail.
  C3  a repair was dispatched before the prior attempt was confirmed ended. -> pre-spawn refusal
      unless the prior process is gone AND its log carries an EXIT= terminal marker.
  C4  a research/verify lane is not authorized to write a remote. -> DETECTION_ONLY pre-spawn check
      of the lane brief for remote-write markers, unless a publication WorkOrder is attached.

All tests are deterministic and spawn NO model, NO relay, NO live lane, NO network and NO credential
probe. The dispatcher is exercised through its real CLI with the deterministic stub child
(tests/fixtures/stub_lane_child.py) as --codex-executable, and through direct imports of its helpers.
"""
from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from datetime import UTC, datetime, timedelta

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
GCM = SCRIPTS / "gcm-containment"
STUB = ROOT / "tests" / "fixtures" / "stub_lane_child.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


disp = _load("hgk_lane_dispatch", SCRIPTS / "hgk-lane-dispatch.py")
lod = _load("lane_output_dir", GCM / "lane_output_dir.py")
authz = _load("authorization_claim", GCM / "authorization_claim.py")


def _scratch_spine():
    """A throwaway Spine DB with the REAL schema, so the lease table is the production one."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c-spine-"))
    db = tmp / "spine.db"
    spine = authz._load_spine(ROOT)(db, ROOT / "src" / "hg_kseos" / "schema.sql")
    spine.initialize()
    return spine, db, tmp


def _stub_env(tmp, provider="opencode-go", model="deepseek-v4.1-flash"):
    env = dict(os.environ)
    env["HGK_STUB_MODE"] = "clean"
    env["HGK_STUB_USAGE"] = str(tmp / "usage.jsonl")
    env["HGK_STUB_USAGE_LINE"] = json.dumps({"provider": provider, "model": model, "status": 200})
    return env


def _authorized_env(tmp):
    """A stub env plus an isolated Spine DB (via HGK_SPINE_DB) so the D4 dispatch tests never touch
    the canonical Shared Spine. Returns (env, spine, db)."""
    env = _stub_env(tmp)
    spine, db, _ = _scratch_spine()
    env["HGK_SPINE_DB"] = str(db)
    return env, spine, db


def _run_dispatch(cmd_extra, *, env=None, timeout=120):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c-disp-"))
    json_out = tmp / "receipt.json"
    cmd = [sys.executable, str(SCRIPTS / "hgk-lane-dispatch.py"),
           "--json-out", str(json_out), "--relay-home", str(tmp / "no-such-relay-home")]
    p = subprocess.run(cmd + cmd_extra, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", stdin=subprocess.DEVNULL, timeout=timeout,
                       cwd=str(ROOT), env=env)
    rec = json.loads(json_out.read_text(encoding="utf-8")) if json_out.is_file() else None
    return p, rec, tmp


class C2SingleUseAuthorizationClaim(unittest.TestCase):
    """The recorded 2-vs-1 overrun: two claimants race ONE resource; exactly one may win."""

    def test_two_concurrent_claimants_exactly_one_wins(self):
        """REQUIRED headline: two threads race the SAME Spine resource; exactly one wins."""
        spine, db, tmp = _scratch_spine()
        resource = "gcm-live-measurement-HGK-GCM-REPAIR-20261013"
        barrier = threading.Barrier(2)
        outcomes: dict[str, str] = {}
        claims: dict[str, object] = {}

        def racer(name, holder, token):
            barrier.wait()  # force true concurrency: both arrive, then both fire at once
            try:
                c = authz.claim(spine, resource, holder, token, ttl_seconds=60)
                claims[name] = c
                outcomes[name] = "claimed"
            except Exception as exc:  # LeaseConflict (ERR_DUAL_WRITER)
                outcomes[name] = f"conflict:{exc}"

        threads = [threading.Thread(target=racer, args=("a", "lane-a-attempt-1", "tok-a")),
                   threading.Thread(target=racer, args=("b", "lane-b-attempt-1", "tok-b"))]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)

        verdicts = sorted(outcomes[k].split(":")[0] for k in ("a", "b"))
        self.assertEqual(verdicts, ["claimed", "conflict"], outcomes)
        loser = "b" if outcomes["a"].startswith("claimed") else "a"
        self.assertIn("ERR_DUAL_WRITER", outcomes[loser])
        winner = "a" if loser == "b" else "b"
        status = authz.lease_status(spine, resource)
        self.assertTrue(status["held"])
        self.assertEqual(status["holder"], claims[winner].holder)
        # release frees it for the next (legitimate) single-use window
        self.assertTrue(claims[winner].release())
        self.assertFalse(authz.lease_status(spine, resource)["held"])
        # a now-free resource is claimable again
        again = authz.claim(spine, resource, "lane-c-attempt-1", "tok-c", ttl_seconds=60)
        self.assertTrue(again.acquired)

    def test_context_manager_releases_on_normal_exit(self):
        spine, db, tmp = _scratch_spine()
        resource = "r-normal"
        with authz.AuthorizationClaim(spine, resource, "h", "t") as c:
            self.assertTrue(c.acquired)
            self.assertTrue(authz.lease_status(spine, resource)["held"])
        self.assertFalse(authz.lease_status(spine, resource)["held"])

    def test_context_manager_releases_on_exception_exit(self):
        """The claim must not deadlock the round when the body raises."""
        spine, db, tmp = _scratch_spine()
        resource = "r-exc"
        with self.assertRaises(RuntimeError):
            with authz.AuthorizationClaim(spine, resource, "h", "t"):
                raise RuntimeError("body failed")
        self.assertFalse(authz.lease_status(spine, resource)["held"])

    def test_release_is_idempotent_and_holder_scoped(self):
        spine, db, tmp = _scratch_spine()
        resource = "r-idem"
        c = authz.claim(spine, resource, "h", "t")
        self.assertTrue(c.release())
        self.assertFalse(c.release())  # second release is a no-op, not a crash
        # a non-holder release is a no-op (fails closed inside the spine, swallowed here)
        c2 = authz.claim(spine, resource, "other", "tok")
        self.assertFalse(authz.release(spine, resource, "wrong-holder", "tok"))
        self.assertTrue(authz.lease_status(spine, resource)["held"])
        self.assertTrue(c2.release())

    def test_ttl_is_a_deadlock_bound(self):
        """A holder that never releases must not hold forever: an expired lease is reclaimable."""
        spine, db, tmp = _scratch_spine()
        resource = "r-ttl"
        authz.claim(spine, resource, "crashed-holder", "t", ttl_seconds=0)
        # ttl=0 -> already expired -> a different holder can take the window
        nxt = authz.claim(spine, resource, "next-holder", "t2", ttl_seconds=60)
        self.assertTrue(nxt.acquired)
        self.assertEqual(authz.lease_status(spine, resource)["holder"], "next-holder")

    def test_cli_second_claim_exits_nonzero_with_typed_code(self):
        spine, db, tmp = _scratch_spine()
        resource = "gcm-live-measurement-CLI"
        base = [sys.executable, str(GCM / "authorization_claim.py"),
                "--hgk-root", str(ROOT), "--db", str(db), "--resource", resource, "--json"]
        # Hold the window in a SECOND PROCESS while we try to claim from this one.
        first = subprocess.Popen(base + ["--holder", "h1", "--token", "t1", "--ttl", "120",
                                         "--hold-seconds", "30"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                 cwd=str(ROOT))
        try:
            held = False
            for _ in range(100):
                if authz.lease_status(spine, resource)["held"]:
                    held = True
                    break
                time.sleep(0.05)
            self.assertTrue(held, "the first claim never took the resource")
            second = subprocess.run(base + ["--holder", "h2", "--token", "t2"],
                                    capture_output=True, text=True, cwd=str(ROOT), timeout=60)
            self.assertEqual(second.returncode, 3, second.stdout + second.stderr)
            self.assertIn("ERR_AUTHORIZATION_CLAIM_REFUSED", second.stdout)
        finally:
            first.kill()
            first.wait(timeout=30)


class C1LaneOutputDir(unittest.TestCase):
    """The X3/X3b collision: two lanes racing one path must collide LOUDLY, never silently reuse."""

    def test_name_shape_and_parent(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1-"))
        d = lod.derive_output_dir(ROOT, "R1", "VERIFY_SECURITY", output_root=tmp)
        self.assertEqual(d.parent, tmp / "R1" / "VERIFY_SECURITY")
        self.assertRegex(d.name, r"^attempt-\d+-\d{8}T\d{6}Z$")
        self.assertEqual(d.name.split("-")[1], "1")

    def test_numbering_is_max_plus_one(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1-"))
        lane_root = lod.lane_root(ROOT, "R1", "L", tmp)
        (lane_root / "attempt-1-20260101T000000Z").mkdir(parents=True)
        (lane_root / "attempt-3-20260101T000001Z").mkdir()
        self.assertEqual(lod.next_attempt_number(lane_root), 4)
        self.assertEqual(lod.derive_output_dir(ROOT, "R1", "L", output_root=tmp).name.split("-")[1], "4")

    def test_explicit_attempt_number_is_honoured(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1-"))
        d = lod.derive_output_dir(ROOT, "R1", "L", attempt=7, output_root=tmp)
        self.assertEqual(d.name.split("-")[1], "7")
        with self.assertRaises(ValueError):
            lod.derive_output_dir(ROOT, "R1", "L", attempt=0, output_root=tmp)

    def test_creating_an_existing_dir_fails_loudly(self):
        """exist_ok=False: the SECOND creator of the same path raises LaneOutputCollision."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1-"))
        d = lod.derive_output_dir(ROOT, "R1", "L", attempt=1, ts="20260101T000000Z", output_root=tmp)
        self.assertEqual(lod.create_output_dir(d), d)
        with self.assertRaises(lod.LaneOutputCollision) as ctx:
            lod.create_output_dir(d)
        self.assertIn("ERR_LANE_OUTPUT_DIR_EXISTS", str(ctx.exception))


class C3RepairPrecondition(unittest.TestCase):
    """The premature-judgement overrun: a repair must not spawn before the prior attempt ended."""

    def test_terminal_marker_is_the_last_exit_line(self):
        self.assertIsNone(disp.find_terminal_marker("no marker here\n"))
        self.assertEqual(disp.find_terminal_marker("x\nEXIT=0\ny\n"), "EXIT=0")
        self.assertEqual(disp.find_terminal_marker("EXIT=0\njunk\nEXIT=2\n"), "EXIT=2")
        self.assertEqual(disp.parse_exit_code("EXIT=2"), 2)
        self.assertIsNone(disp.parse_exit_code("nope"))
        self.assertIsNone(disp.parse_exit_code(None))

    def test_process_liveness_self_is_alive_dead_pid_is_gone(self):
        alive = lod.process_liveness(os.getpid())
        self.assertTrue(alive["checked"])
        self.assertTrue(alive["alive"])
        gone = lod.process_liveness(999999)
        self.assertTrue(gone["checked"])
        self.assertFalse(gone["alive"])
        self.assertIsNone(lod.process_liveness(None)["alive"])

    def test_live_attempt_in_reads_the_marker(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        d = tmp / "attempt-1-x"
        d.mkdir()
        lod.write_attempt_marker(d, round_name="R1", lane="L", attempt=1, pid=os.getpid())
        info = lod.live_attempt_in(d)
        self.assertTrue(info["exists"])
        self.assertEqual(info["marker"]["pid"], os.getpid())
        self.assertTrue(info["liveness"]["alive"])

    def test_dispatch_refuses_when_prior_log_has_no_terminal_marker(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("still running...\n", encoding="utf-8")
        prior = tmp / "attempt-1-20260101T000000Z"
        prior.mkdir()
        lod.write_attempt_marker(prior, round_name="R1", lane="L", attempt=1,
                                 pid=999999, log_path=str(log))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--prior-attempt-dir", str(prior)]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_REPAIR_PRIOR_ATTEMPT_NO_TERMINAL_MARKER")
        self.assertFalse(rec["ok"])

    def test_dispatch_refuses_when_prior_process_is_alive(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("EXIT=0\n", encoding="utf-8")  # log would pass, but the process is alive
        prior = tmp / "attempt-1-20260101T000000Z"
        prior.mkdir()
        lod.write_attempt_marker(prior, round_name="R1", lane="L", attempt=1,
                                 pid=os.getpid(), log_path=str(log))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--prior-attempt-dir", str(prior)]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_REPAIR_PRIOR_ATTEMPT_ALIVE")

    def test_dispatch_proceeds_when_prior_is_gone_with_exit_marker(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("...\nEXIT=0\n", encoding="utf-8")
        prior = tmp / "attempt-1-20260101T000000Z"
        prior.mkdir()
        lod.write_attempt_marker(prior, round_name="R1", lane="L", attempt=1,
                                 pid=999999, log_path=str(log))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--prior-attempt-dir", str(prior)]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(rec["repair_precondition"]["prior_process_gone"], True, p.stdout + p.stderr)
        self.assertEqual(rec["repair_precondition"]["terminal_marker"], "EXIT=0")
        self.assertEqual(rec["repair_precondition"]["prior_exit_code"], 0)
        self.assertTrue(rec["ok"], p.stdout + p.stderr)

    # ---- D5 (round HGK-GCM-REPAIR2-20261013): the three INSUFFICIENT proofs must now REFUSE ----
    # Round 1 accepted all three and spawned a stub attempt anyway. None of them proves the prior
    # PROCESS is gone, which is the only thing that licenses a repair. All three must now fail closed
    # with the typed `ERR_REPAIR_PRIOR_ATTEMPT_LIVENESS_UNPROVEN` code (no pid, no liveness, no spawn).

    def _liveness_unproven(self, cmd, env):
        p, rec, _ = _run_dispatch(cmd, env=env)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_REPAIR_PRIOR_ATTEMPT_LIVENESS_UNPROVEN", p.stdout + p.stderr)
        self.assertFalse(rec["ok"])
        # No attempt served: the precondition refused BEFORE any spawn (no attempts recorded).
        self.assertFalse(rec.get("attempts"), p.stdout + p.stderr)
        return rec

    def test_d5_variant_a_log_only_exit_marker_refuses(self):
        """(a) a prior log carrying EXIT= ALONE (no dir, no pid) must refuse, not spawn."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("...\nEXIT=0\n", encoding="utf-8")
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--prior-attempt-log", str(log)]
        rec = self._liveness_unproven(cmd, _stub_env(tmp))
        self.assertIsNone(rec["repair_precondition"]["prior_process_gone"])

    def test_d5_variant_b_absent_dir_plus_log_refuses(self):
        """(b) an ABSENT prior dir plus a log must refuse: the absent dir carries no pid/marker."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("...\nEXIT=0\n", encoding="utf-8")
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--prior-attempt-dir", str(tmp / "no-such-prior-dir"),
               "--prior-attempt-log", str(log)]
        rec = self._liveness_unproven(cmd, _stub_env(tmp))
        self.assertIsNone(rec["repair_precondition"]["prior_process_gone"])
        self.assertFalse(rec["repair_precondition"]["prior_exists"])

    def test_d5_variant_c_existing_dir_no_marker_plus_log_refuses(self):
        """(c) an EXISTING dir with NO marker plus a log must refuse: no pid -> liveness unproven."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("...\nEXIT=0\n", encoding="utf-8")
        prior = tmp / "attempt-1-20260101T000000Z"
        prior.mkdir()  # exists, but NO attempt.marker.json
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--prior-attempt-dir", str(prior), "--prior-attempt-log", str(log)]
        rec = self._liveness_unproven(cmd, _stub_env(tmp))
        self.assertIsNone(rec["repair_precondition"]["prior_process_gone"])

    def test_d5_positive_prior_gone_with_pid_proceeds(self):
        """The positive control: a DEAD prior pid + EXIT marker lets the repair proceed."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c3-"))
        log = tmp / "prior.log"
        log.write_text("...\nEXIT=0\n", encoding="utf-8")
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--prior-attempt-pid", "999999",
               "--prior-attempt-log", str(log)]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(rec["repair_precondition"]["prior_process_gone"], True, p.stdout + p.stderr)
        self.assertTrue(rec["ok"], p.stdout + p.stderr)


class D4DispatcherConsumesAuthorization(unittest.TestCase):
    """D4 (round HGK-GCM-REPAIR2-20261013): the dispatcher must ACQUIRE and CONSUME the single-use
    authorization resource through the EXISTING Spine leases table, so the overrun is structural.

    Round-1 defect: the dispatcher imported `authorization_claim` but never acquired or checked it, so
    both sequential distinct holders won and the SAME holder won twice. These tests drive the REAL
    dispatcher CLI with the deterministic stub child and an isolated Spine DB.
    """

    def _dispatch(self, tmp, env, resource, extra=None):
        extra = extra or []
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--authorization-resource", resource] + extra
        return _run_dispatch(cmd, env=env)

    def test_first_spawn_consumes_the_resource_second_refused(self):
        """Sequential distinct holders sharing one resource: the 2nd dispatch must be refused."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-d4-"))
        env, spine, db = _authorized_env(tmp)
        resource = "gcm-live-measurement-D4-sequential"
        p1, rec1, _ = self._dispatch(tmp, env, resource)
        self.assertTrue(rec1["ok"], p1.stdout + p1.stderr)
        self.assertEqual(rec1["authorization"]["consumed"], True, p1.stdout + p1.stderr)
        self.assertEqual(rec1["authorization"]["consumed_before"], False)
        # a second, distinct invocation is a DIFFERENT holder (new pid) and must be refused
        p2, rec2, _ = self._dispatch(tmp, env, resource)
        self.assertEqual(p2.returncode, 4, p2.stdout + p2.stderr)
        self.assertEqual(rec2["code"], "ERR_AUTHORIZATION_ALREADY_CONSUMED", p2.stdout + p2.stderr)
        self.assertFalse(rec2["ok"])
        self.assertFalse(rec2.get("attempts"), p2.stdout + p2.stderr)  # refused BEFORE any spawn
        self.assertTrue(authz.is_consumed(spine, resource))

    def test_same_holder_twice_is_refused(self):
        """The round-1 hole: `acquire_lease` silently renews for the SAME holder. The CONSUMED
        tombstone must make a same-holder second use fail too."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-d4-"))
        env, spine, db = _authorized_env(tmp)
        resource = "gcm-live-measurement-D4-same-holder"
        p1, rec1, _ = self._dispatch(tmp, env, resource)
        self.assertTrue(rec1["ok"], p1.stdout + p1.stderr)
        self.assertTrue(authz.is_consumed(spine, resource))
        # A module-level re-claim by ANY holder (including the prior holder identity) is refused.
        holder = "same-holder-identity"
        with self.assertRaises(authz.ClaimAlreadyConsumed):
            authz.claim(spine, resource, holder, "tok-again", ttl_seconds=60)
        p2, rec2, _ = self._dispatch(tmp, env, resource)
        self.assertEqual(rec2["code"], "ERR_AUTHORIZATION_ALREADY_CONSUMED", p2.stdout + p2.stderr)

    def test_concurrent_dispatches_exactly_one_winner_or_refusal(self):
        """Two dispatches race ONE resource from two threads -> exactly one spawns and consumes the
        resource; the other is refused (conflict or already-consumed). Never both."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-d4-"))
        env, spine, db = _authorized_env(tmp)
        resource = "gcm-live-measurement-D4-concurrent"
        barrier = threading.Barrier(2)
        results: dict[str, tuple] = {}

        def racer(name):
            out = tmp / f"rec-{name}.json"
            renv = dict(env)
            renv["HGK_STUB_USAGE"] = str(tmp / f"usage-{name}.jsonl")
            cmd = [sys.executable, str(SCRIPTS / "hgk-lane-dispatch.py"),
                   "--json-out", str(out), "--relay-home", str(tmp / "no-such-relay-home"),
                   "--lane", "VERIFY_SECURITY", "--force-rank", "1",
                   "--codex-executable", str(STUB), "--usage", str(tmp / f"usage-{name}.jsonl"),
                   "--timeout", "30", "--prompt", "x",
                   "--authorization-resource", resource]
            barrier.wait()
            p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", stdin=subprocess.DEVNULL, timeout=120,
                               cwd=str(ROOT), env=renv)
            rec = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else None
            results[name] = (p, rec)

        threads = [threading.Thread(target=racer, args=(n,)) for n in ("a", "b")]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)

        wins = [n for n, (p, rec) in results.items() if rec and rec.get("ok")]
        refusals = [n for n, (p, rec) in results.items()
                    if rec and not rec.get("ok") and p.returncode == 4]
        self.assertEqual(len(wins), 1, results)
        self.assertEqual(len(refusals), 1, results)
        loser = refusals[0]
        self.assertIn(results[loser][1]["code"],
                      ("ERR_AUTHORIZATION_ALREADY_CONSUMED", "ERR_AUTHORIZATION_CLAIM_REFUSED"), results)
        self.assertTrue(authz.is_consumed(spine, resource))

    def test_unexercised_window_is_reclaimable(self):
        """A dispatch whose spawn never served does NOT burn the resource: the window is released and
        the resource is reclaimable (it was never consumed)."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-d4-"))
        env, spine, db = _authorized_env(tmp)
        resource = "gcm-live-measurement-D4-unexercised"
        # Drop the usage line so the stub emits no matching usage receipt -> the attempt does not
        # serve -> nothing is consumed (the turn fails rather than serving).
        env = dict(env)
        env.pop("HGK_STUB_USAGE_LINE", None)
        p1, rec1, _ = self._dispatch(tmp, env, resource)
        self.assertFalse(rec1["ok"], p1.stdout + p1.stderr)
        self.assertFalse(rec1["authorization"]["consumed"])
        self.assertTrue(rec1["authorization"]["window_released"])
        self.assertFalse(authz.is_consumed(spine, resource))
        # a clean retry can now take the (still-unconsumed) window and consume it
        env["HGK_STUB_USAGE_LINE"] = json.dumps({"provider": "opencode-go",
                                                 "model": "deepseek-v4.1-flash", "status": 200})
        p2, rec2, _ = self._dispatch(tmp, env, resource)
        self.assertTrue(rec2["ok"], p2.stdout + p2.stderr)
        self.assertTrue(rec2["authorization"]["consumed"])

    def test_no_authorization_resource_reports_unchecked(self):
        """Backwards-compatible: when no resource is named the boundary is explicitly NOT checked."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-d4-"))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertFalse(rec["authorization"]["checked"])


class D4ModuleConsumeTombstone(unittest.TestCase):
    """Unit-level locks on the CONSUMED tombstone: durable, holder-independent, resettable."""

    def test_consume_blocks_every_holder_until_reset(self):
        spine, db, tmp = _scratch_spine()
        resource = "r-consumed"
        c = authz.claim(spine, resource, "h1", "t1", ttl_seconds=60)
        self.assertFalse(authz.is_consumed(spine, resource))
        self.assertTrue(c.consume())
        self.assertTrue(authz.is_consumed(spine, resource))
        # release of the WINDOW must NOT clear the tombstone
        self.assertTrue(c.release())
        self.assertTrue(authz.is_consumed(spine, resource))
        # every holder is refused while the tombstone is live
        for holder in ("h1", "h2", authz.CONSUMED_HOLDER):
            with self.assertRaises(authz.ClaimAlreadyConsumed):
                authz.claim(spine, resource, holder, "tok", ttl_seconds=60)
        # the documented rollback frees it
        self.assertTrue(authz.reset(spine, resource))
        self.assertFalse(authz.is_consumed(spine, resource))
        again = authz.claim(spine, resource, "h3", "t3", ttl_seconds=60)
        self.assertTrue(again.acquired)

    def test_acquire_does_not_consume(self):
        """Acquiring the WINDOW alone must not mark it consumed (only a successful spawn does)."""
        spine, db, tmp = _scratch_spine()
        resource = "r-window-only"
        c = authz.claim(spine, resource, "h", "t", ttl_seconds=60)
        self.assertFalse(authz.is_consumed(spine, resource))
        c.release()
        # a released-but-unconsumed window is reclaimable
        self.assertTrue(authz.claim(spine, resource, "h2", "t2", ttl_seconds=60).acquired)


class C4RemoteWritePrecheck(unittest.TestCase):
    """DETECTION_ONLY: a non-publication brief carrying remote-write markers must refuse to dispatch."""

    def test_marker_detection(self):
        self.assertEqual(disp.detect_remote_write_markers("no markers"), [])
        got = disp.detect_remote_write_markers("run `git push origin main` and --force it")
        self.assertIn("git push", got)
        self.assertIn("--force", got)
        self.assertIn("refs/heads", disp.detect_remote_write_markers("write refs/heads/main"))
        self.assertIn("publish", disp.detect_remote_write_markers("PUBLISH the artifact"))

    def test_workorder_token_authorizes(self):
        pre = disp.remote_write_precheck(brief_text="git push origin main", publication_wo=None)
        self.assertTrue(pre["would_refuse"])
        pre2 = disp.remote_write_precheck(brief_text="git push", publication_wo="WO-PUBLISH-1")
        self.assertFalse(pre2["would_refuse"])
        # a WorkOrder-looking token inside the brief also authorizes
        pre3 = disp.remote_write_precheck(brief_text="git push\nWorkOrder: WO-PUB-9", publication_wo=None)
        self.assertFalse(pre3["would_refuse"])
        # D6 (round HGK-GCM-REPAIR2-20261013): the extraction must return the BARE id, not the
        # label-prefixed "WorkOrder: WO-PUB-9". Round 1 relaxed this to assertIn; that relaxation is
        # reverted here and the function is fixed instead.
        self.assertEqual(pre3["publication_wo"], "WO-PUB-9")
        self.assertEqual(disp.detect_publication_workorder("WorkOrder: WO-PUB-9"), "WO-PUB-9")
        self.assertEqual(disp.detect_publication_workorder("PUBLICATION WO: X-1"), "X-1")
        self.assertEqual(disp.detect_publication_workorder("bare WO-PUB-9 token"), "WO-PUB-9")
        self.assertIsNone(disp.detect_publication_workorder("no workorder here"))

    def test_dispatch_refuses_brief_with_markers(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c4-"))
        brief = tmp / "BRIEF.md"
        brief.write_text("Please run git push --force to refs/heads/main.\n", encoding="utf-8")
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--brief", str(brief)]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED")
        self.assertTrue(rec["detection_only"])

    def test_dispatch_proceeds_with_publication_workorder(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c4-"))
        brief = tmp / "BRIEF.md"
        brief.write_text("git push origin main\n", encoding="utf-8")
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x", "--brief", str(brief),
               "--publication-workorder", "WO-PUBLISH-42"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertFalse(rec["remote_write_precheck"]["would_refuse"], p.stdout + p.stderr)
        self.assertTrue(rec["ok"], p.stdout + p.stderr)


class C1NonceNumberOfDispatchDerivedDir(unittest.TestCase):
    """The dispatcher must DERIVE the output dir (--round) and record the policy in the receipt."""

    def test_round_derives_output_dir_and_records_marker(self):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1d-"))
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--round", "R-DERIVE", "--output-root", str(tmp), "--attempt", "1"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertTrue(rec["ok"], p.stdout + p.stderr)
        self.assertEqual(rec["output_dir_policy"]["mode"], "derived")
        derived = pathlib.Path(rec["output_dir_policy"]["derived"])
        self.assertTrue(derived.is_dir())
        self.assertEqual(derived.parent, tmp / "R-DERIVE" / "VERIFY_SECURITY")
        self.assertTrue((derived / "attempt.marker.json").is_file())

    def test_round_derived_dir_that_already_exists_collides_loudly(self):
        """Pre-create the exact path the dispatcher will derive -> the dispatcher must refuse."""
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-c1d-"))
        lane_root = lod.lane_root(ROOT, "R-DERIVE2", "VERIFY_SECURITY", tmp)
        # The dispatcher stamps the derived dir with the CURRENT UTC second (a subprocess we cannot
        # freeze). Seed the current second AND its neighbours so the second-boundary crossing cannot
        # make the test flaky: whichever instant the subprocess derives, the path already exists.
        now = datetime.now(UTC)
        for delta in (-1, 0, 1, 2):
            stamp = lod.utc_stamp(now + timedelta(seconds=delta))
            (lane_root / f"attempt-1-{stamp}").mkdir(parents=True, exist_ok=True)
        cmd = ["--lane", "VERIFY_SECURITY", "--force-rank", "1",
               "--codex-executable", str(STUB), "--usage", str(tmp / "usage.jsonl"),
               "--timeout", "30", "--prompt", "x",
               "--round", "R-DERIVE2", "--output-root", str(tmp), "--attempt", "1"]
        p, rec, _ = _run_dispatch(cmd, env=_stub_env(tmp))
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        self.assertEqual(rec["code"], "ERR_LANE_OUTPUT_DIR_EXISTS")


if __name__ == "__main__":
    unittest.main()
