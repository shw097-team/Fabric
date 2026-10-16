"""Matrix-D case M06: argv ``--require-arm`` conflicting with the persisted mandate.

This is a BEHAVIORAL test. It exercises the REAL pre-spawn rejection of the dispatcher (a typed
refusal + NO spawn, asserted end-to-end) by mirroring the passing ``DispatcherPreSpawn`` shape in
``test_role_binding_enforcement.py``: a temp dir, a projected ``--role-binding-file``, and a
persisted mandate that is the AUTHORITY. The supplied projection must match the persisted binding.
It never calls a live model and never asserts on source text.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import tempfile
import unittest

# Reuse the canonical fixture/helpers so we do NOT invent a new one.
# `tests/` is a package (has __init__.py), so the sibling module is imported under the package name.
from tests.test_role_binding_enforcement import (  # noqa: E402
    BASE,
    HGK_PY,
    ROOT,
    WO,
    _binding,
    disp,
)

from hg_kseos.spine import SharedSpine  # noqa: E402
from hg_kseos import role_binding  # noqa: E402


class M06(unittest.TestCase):
    """M06: ``--require-arm`` that conflicts with the persisted mandated arm must refuse, no spawn."""

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

    def test_argv_require_arm_conflicting_with_mandate_refused_no_spawn(self):
        # The mandated EXECUTE arm is (opencode-go, deepseek-v4.1-flash). We assert a DIFFERENT arm.
        mandate_arm = _binding()["roles"]["EXECUTE"]
        self.assertEqual((mandate_arm["provider"], mandate_arm["model"]),
                         ("opencode-go", "deepseek-v4.1-flash"))
        conflicting = "openai-codex/gpt-6.1-sol"
        self.assertNotEqual(conflicting, f'{mandate_arm["provider"]}/{mandate_arm["model"]}')

        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m06-e2e-", dir=str(ROOT.parent / "TEST_RESULTS")))
        bf = self._write_binding(tmp)
        db = self._persist_spine(tmp)
        p = self._run(["--role-binding-file", str(bf), "--workorder", WO,
                       "--require-arm", conflicting], tmp, spine_db=db)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertIs(r["ok"], False)
        self.assertEqual(r["code"], disp.ERR_ROLE_BINDING_ARM_MISMATCH)
        self.assertEqual(list(tmp.glob("*.logs")), [])


class M07(unittest.TestCase):
    """M07: an OMITTED ``--require-arm`` cannot escape the mandate; a wrong ``--force-rank`` is refused.

    M07a is the mirror of M06 from the other direction: with NO ``--require-arm`` on the argv the
    persisted binding is still the AUTHORITY, so the run must be bound to the MANDATED arm -- an argv
    default can never pick a different arm. M07b re-checks the rank half of the same discipline:
    a ``--force-rank`` that contradicts the binding is refused pre-spawn with a typed code and no logs.
    These reuse the SAME fixture shape as M06/``DispatcherPreSpawn`` (temp dir, persisted spine
    authority, projection file), and M07a drives the deterministic stub lane-child fixture so the run
    reaches a no-nonce refusal WITHOUT a live model -- the binding is derived pre-spawn either way.
    """

    def _run(self, extra, tmpdir, spine_db):
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
               "--json-out", str(tmpdir / "receipt.json"),
               "--relay-home", str(tmpdir / "no-such-relay-home")] + extra
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(spine_db)
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                              cwd=str(ROOT), env=env)

    def _write_binding(self, tmpdir, **over):
        p = tmpdir / "binding.json"
        p.write_text(json.dumps(_binding(**over)), encoding="utf-8")
        return p

    def _persist_spine(self, tmpdir, **over):
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

    def test_omitted_require_arm_cannot_escape_mandate(self):
        # The persisted mandate binds EXECUTE to (opencode-go, deepseek-v4.1-flash) at rank 1.
        mandate_arm = _binding()["roles"]["EXECUTE"]
        mandated = f'{mandate_arm["provider"]}/{mandate_arm["model"]}'
        self.assertEqual(mandated, "opencode-go/deepseek-v4.1-flash")
        # An argv DEFAULT would be some OTHER arm; the binding must overrule it, not vice-versa.
        self.assertNotEqual(mandated, f'{_binding()["roles"]["PLAN"]["provider"]}/'
                                      f'{_binding()["roles"]["PLAN"]["model"]}')

        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m07a-",
                                            dir=str(ROOT.parent / "TEST_RESULTS")))
        bf = self._write_binding(tmp)          # a projection of the persisted binding
        db = self._persist_spine(tmp)          # the AUTHORITY
        scratch = tmp / "usage.jsonl"
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(db)
        env["HGK_STUB_MODE"] = "clean"
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": mandate_arm["provider"], "model": mandate_arm["model"], "status": 200,
             "nonce": "M07A-STUB-NONCE"})
        # NO --require-arm on the argv. The stub child emits no nonce, so the run stops with a
        # no-nonce refusal -- but only AFTER the mandated arm/rank were DERIVED pre-spawn.
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "deterministic omitted-require-arm case",
               "--role-binding-file", str(bf), "--workorder", WO,
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(scratch), "--nonce", "M07A-STUB-NONCE",
               "--json-out", str(tmp / "receipt.json"),
               "--cwd", str(tmp), "--relay-home", str(tmp / "no-such-relay-home")]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                           cwd=str(ROOT), env=env)
        # CASE SHAPE (recorded): the dispatcher did NOT refuse at the binding stage -- it PROCEEDED
        # to the stub-child refusal for the absent nonce (exit 3, ERR_NO_ARM_EMITTED_NONCE). So the
        # mandate-branch assertion is the one used below: the receipt still reflects the mandated arm.
        self.assertEqual(p.returncode, 3, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertIs(r["ok"], False)
        self.assertEqual(r["code"], "ERR_NO_ARM_EMITTED_NONCE")
        # The BINDING drove selection: digest/arm/rank all come from the persisted mandate, and the
        # identity gate + candidate set are pinned to the mandated rank (never an argv default).
        self.assertEqual(r["identity_gate"]["required_arm"], mandated)
        self.assertEqual(r["role_binding"]["role_binding_arm"], mandated)
        self.assertEqual(r["role_binding"]["role_binding_rank"], mandate_arm["rank"])
        self.assertEqual(r["binding_forced_rank"], mandate_arm["rank"])
        self.assertEqual(r["candidates_considered"], [mandate_arm["rank"]])
        self.assertEqual(r["mode"], "forced_rank")
        self.assertTrue(r["role_binding"]["role_binding_digest"])

    def test_wrong_force_rank_refused(self):
        mandate_rank = _binding()["roles"]["EXECUTE"]["rank"]
        wrong_rank = int(mandate_rank) + 1          # contradicts the binding
        self.assertNotEqual(wrong_rank, int(mandate_rank))

        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m07b-",
                                            dir=str(ROOT.parent / "TEST_RESULTS")))
        bf = self._write_binding(tmp)
        db = self._persist_spine(tmp)
        p = self._run(["--role-binding-file", str(bf), "--workorder", WO,
                       "--force-rank", str(wrong_rank)], tmp, db)
        self.assertEqual(p.returncode, 4, p.stdout + p.stderr)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertIs(r["ok"], False)
        self.assertEqual(r["code"], disp.ERR_ROLE_BINDING_RANK_MISMATCH)
        self.assertEqual(list(tmp.glob("*.logs")), [])


class M08(unittest.TestCase):
    """M08 (P3c-2, MINIMAL / test-only): a FOREIGN-surface usage receipt cannot complete.

    The completion path treats a usage receipt whose provider/model is NOT the MANDATED arm as
    "not answered", so a generic delegate can never substitute the Codex CLI surface. This is the
    M07a harness EXACTLY (stub child + scratch ``--usage`` ledger + ``--nonce`` + projection
    ``--role-binding-file`` + persisted spine authority) with ONE change: the stub's usage row
    reports a FOREIGN surface (``openrouter`` / ``anthropic/claude-opus-4.8``) whose nonce matches
    the argv ``--nonce``. That isolates the SURFACE as the only intended defect, and the turn must
    still be REFUSED rather than completed.

    Rationale (recorded): the mandated EXECUTE arm is (opencode-go, deepseek-v4.1-flash); a usage
    receipt naming a different provider/model is not this turn's receipt, so it is never counted as
    an ``answered`` arm. If this run instead COMPLETES (``ok`` true) that is a REAL finding: STOP and
    report it as NOT_RUN with the exact receipt -- the code change would be a SEPARATE successor.
    """

    def _run(self, extra, tmpdir, spine_db):
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "PLACEHOLDER-NOT-USED-BY-A-REFUSAL",
               "--json-out", str(tmpdir / "receipt.json"),
               "--relay-home", str(tmpdir / "no-such-relay-home")] + extra
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(spine_db)
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                              cwd=str(ROOT), env=env)

    def _write_binding(self, tmpdir, **over):
        p = tmpdir / "binding.json"
        p.write_text(json.dumps(_binding(**over)), encoding="utf-8")
        return p

    def _persist_spine(self, tmpdir, **over):
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

    def test_foreign_surface_usage_receipt_cannot_complete(self):
        # The mandated EXECUTE arm is (opencode-go, deepseek-v4.1-flash) at rank 1.
        mandate_arm = _binding()["roles"]["EXECUTE"]
        mandated = f'{mandate_arm["provider"]}/{mandate_arm["model"]}'
        self.assertEqual(mandated, "opencode-go/deepseek-v4.1-flash")
        foreign = "openrouter/anthropic/claude-opus-4.8"
        self.assertNotEqual(mandated, foreign)

        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m08-",
                                            dir=str(ROOT.parent / "TEST_RESULTS")))
        # A real deliverable ON DISK so the turn genuinely reaches the settlement/completion path;
        # the ONLY intended defect is the FOREIGN surface of the usage receipt.
        deliverable = b"bound round deliverable that really landed\n"
        (tmp / "deliverable.py").write_bytes(deliverable)
        ov = {"deliverable": {"path": "deliverable.py",
                              "sha256": hashlib.sha256(deliverable).hexdigest()}}
        bf = self._write_binding(tmp, **ov)    # a projection of the persisted binding
        db = self._persist_spine(tmp, **ov)    # the AUTHORITY
        scratch = tmp / "usage.jsonl"
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(db)
        env["HGK_STUB_MODE"] = "clean"
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_EMIT_NONCE"] = "M08-FOREIGN"  # make the emitted nonce match --nonce: SURFACE is the only defect
        # The stub reports a FOREIGN surface in its usage row; the nonce matches the argv --nonce so
        # the SURFACE is the only intended defect (isolating provider/model substitution).
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": "openrouter", "model": "anthropic/claude-opus-4.8", "status": 200,
             "nonce": "M08-FOREIGN"})
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "foreign-surface usage receipt cannot complete",
               "--role-binding-file", str(bf), "--workorder", WO,
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(scratch), "--nonce", "M08-FOREIGN",
               "--json-out", str(tmp / "receipt.json"),
               "--cwd", str(tmp), "--relay-home", str(tmp / "no-such-relay-home")]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                           cwd=str(ROOT), env=env)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        # The turn MUST NOT complete. The observed production refusal code for this config is
        # ERR_LANE_ALL_ROUTES_EXHAUSTED: the FOREIGN usage row never matches the mandated arm's
        # model, so `usage_receipt_ok` is false and NO attempt counts as `answered` -- the frozen
        # requirement's table then yields the generic exhausted code rather than the no-nonce code.
        # (The only other permitted code is ERR_NO_ARM_EMITTED_NONCE; if the observed code changes to
        # that, update this assertion and the comment -- never a fake green.)
        self.assertIs(r["ok"], False, f"FOREIGN surface COMPLETED -- REAL finding, NOT_RUN: {r}")
        self.assertEqual(r["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED", r)
        self.assertIn(r["code"], ("ERR_NO_ARM_EMITTED_NONCE", "ERR_LANE_ALL_ROUTES_EXHAUSTED"))
        # The binding still drove selection to the MANDATED arm; the foreign surface was rejected.
        self.assertEqual((r.get("role_binding") or {}).get("role_binding_arm"), mandated)
        attempts = r.get("attempts") or []
        self.assertTrue(attempts)
        self.assertEqual(attempts[0]["provider"], mandate_arm["provider"])
        self.assertEqual(attempts[0]["model"], mandate_arm["model"])
        self.assertIs(attempts[0]["usage_receipt_ok"], False)


    def test_mandated_surface_usage_receipt_completes_control(self):
        """CONTROL for the case above: with the MANDATED surface (same fixture, same nonce echo) the
        turn MUST complete. Without this control the foreign-surface negative is confounded -- a
        fixture that fails for an unrelated reason (e.g. a nonce mismatch) would satisfy the refusal
        assertion for the wrong reason, proving nothing about surface substitution.
        """
        mandate_arm = _binding()["roles"]["EXECUTE"]
        mandated = f'{mandate_arm["provider"]}/{mandate_arm["model"]}'
        self.assertEqual(mandated, "opencode-go/deepseek-v4.1-flash")
        nonce = "M08-CONTROL"

        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-m08ctl-",
                                            dir=str(ROOT.parent / "TEST_RESULTS")))
        deliverable = b"bound round deliverable that really landed\n"
        (tmp / "deliverable.py").write_bytes(deliverable)
        ov = {"deliverable": {"path": "deliverable.py",
                              "sha256": hashlib.sha256(deliverable).hexdigest()}}
        bf = self._write_binding(tmp, **ov)
        db = self._persist_spine(tmp, **ov)
        scratch = tmp / "usage.jsonl"
        env = dict(os.environ)
        env["HGK_SPINE_DB"] = str(db)
        env["HGK_STUB_MODE"] = "clean"
        env["HGK_STUB_USAGE"] = str(scratch)
        env["HGK_STUB_EMIT_NONCE"] = nonce   # the same value passed to --nonce below
        env["HGK_STUB_USAGE_LINE"] = json.dumps(
            {"provider": mandate_arm["provider"], "model": mandate_arm["model"], "status": 200,
             "nonce": nonce})
        cmd = [str(HGK_PY), str(ROOT / "scripts" / "hgk-lane-dispatch.py"),
               "--lane", "EXECUTE", "--prompt", "mandated-surface control: must complete",
               "--role-binding-file", str(bf), "--workorder", WO,
               "--codex-executable", str(ROOT / "tests/fixtures/stub_lane_child.py"),
               "--usage", str(scratch), "--nonce", nonce,
               "--json-out", str(tmp / "receipt.json"),
               "--cwd", str(tmp), "--relay-home", str(tmp / "no-such-relay-home")]
        subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", stdin=subprocess.DEVNULL, timeout=180,
                       cwd=str(ROOT), env=env)
        r = json.loads((tmp / "receipt.json").read_text(encoding="utf-8"))
        self.assertIs(r["ok"], True,
                      f"mandated-surface control did NOT complete -- M08 stays confounded: {r}")


if __name__ == "__main__":
    unittest.main()
