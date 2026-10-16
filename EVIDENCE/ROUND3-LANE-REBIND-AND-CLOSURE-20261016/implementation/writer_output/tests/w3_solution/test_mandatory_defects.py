"""Deterministic regressions for the four defects that rejected the previous
round. Each test names the defect it prevents and the code that prevents it."""

import os
import shutil
from pathlib import Path

import pytest

from conftest import preflight
from lane_harness import (
    GIT_BASH,
    copy_deliverable,
    run_launcher,
    run_preflight_script,
    tree_sha256_map,
    write_declaration,
    write_stub,
)


DECLARED_MODEL = "gpt-6.1-sol"


# ---- Defect 2: containment rejects BOTH directions (ancestor case) ----------

def test_containment_guard_rejects_target_inside_subject(tmp_path):
    subject = (tmp_path / "deliverable").resolve()
    base = (tmp_path / "scratch_base").resolve()
    target = subject / "inner"
    ok, code, detail = preflight.check_containment(base, target, subject)
    assert ok is False
    assert code == preflight.ERR_TARGET_INSIDE_SUBJECT


def test_containment_guard_rejects_subject_inside_target(tmp_path):
    """The ancestor case the previous round's weaker guard missed: if the subject
    lives UNDER the target, deleting the target would delete the subject."""
    base = (tmp_path / "root").resolve()
    target = (base / "lane").resolve()
    subject = (target / "deliverable").resolve()   # subject lives UNDER target
    ok, code, detail = preflight.check_containment(base, target, subject)
    assert ok is False
    assert code == preflight.ERR_SUBJECT_INSIDE_TARGET
    assert "delete" in detail


def test_containment_guard_rejects_target_equal_to_base(tmp_path):
    subject = (tmp_path / "deliverable").resolve()
    base = (tmp_path / "scratch_base").resolve()
    ok, code, _ = preflight.check_containment(base, base, subject)
    assert ok is False
    assert code == preflight.ERR_TARGET_OUTSIDE_BASE


def test_containment_guard_accepts_a_clean_sibling(tmp_path):
    subject = (tmp_path / "deliverable").resolve()
    base = (tmp_path / "scratch_base").resolve()
    target = base / "lane"
    ok, code, _ = preflight.check_containment(base, target, subject)
    assert ok is True and code == ""


# ---- Defect 1: NO filesystem mutation before containment is PROVEN ---------

def test_preflight_creates_nothing_when_scratch_is_inside_subject(tmp_path):
    """A caller-supplied scratch inside the subject is refused BEFORE any mkdir;
    the scratch, its parent and the log dir are never created."""
    # The subject is a BOUNDED copy of the deliverable, not the repository. The
    # copy's OWN preflight script derives its subject root from its location, so
    # "inside the subject" is proven without walking the repository.
    subject = copy_deliverable(tmp_path / "deliverable")
    scratch_inside = subject / "would-be-inside"
    log = tmp_path / "out" / "preflight.log"
    receipt = tmp_path / "out" / "receipt.json"
    proc = run_preflight_script(
        subject,
        "--model", DECLARED_MODEL, "--scratch", scratch_inside,
        "--log", log, "--receipt", receipt,
    )
    assert proc.returncode == preflight.EXIT_CONTAINMENT, proc.stderr
    assert not scratch_inside.exists()
    # The receipt is written OUTSIDE the subject and records 0 attempts.
    doc = json_load(receipt)
    assert doc["scratch_created"] is False
    assert doc["attempts"] == 0


def test_preflight_refuses_log_dir_inside_subject_before_creating_it(tmp_path):
    """Defect 1: a caller log path under the subject must be checked BEFORE it is
    created. Nothing (not even the log dir) may be created."""
    subject = copy_deliverable(tmp_path / "deliverable")
    # The SAME whole-subject freeze as before, just on a bounded copy: the tree
    # hash still catches a leaked log dir, scratch dir or receipt.
    before = tree_sha256_map(subject, exclude=())
    scratch_outside = tmp_path / "scratch_outside"
    log = subject / "would-be-log-dir" / "preflight.log"
    receipt = tmp_path / "out" / "receipt.json"
    proc = run_preflight_script(
        subject,
        "--model", DECLARED_MODEL, "--scratch", scratch_outside,
        "--log", log, "--receipt", receipt,
    )
    assert proc.returncode == preflight.EXIT_OUTPUT_INSIDE_SUBJECT, proc.stderr
    assert not log.parent.exists(), "the log dir must not be created"
    assert not scratch_outside.exists(), "refusal must precede scratch creation"
    assert tree_sha256_map(subject) == before


def test_launcher_log_dir_inside_subject_refused_before_any_mkdir(tmp_path):
    """Defect 1 (launcher half): the caller LOG_DIR must be proven outside the
    subject BEFORE it is created. Exit non-zero, create nothing."""
    if not GIT_BASH:
        pytest.skip("needs a POSIX shell")
    deliverable = copy_deliverable(tmp_path / "deliverable")
    stub, sha = write_stub(tmp_path / "deliverable", version="9.9.9",
                           body="OpenAI Codex v9.9.9\nmodel: gpt-6.1-sol\nprovider: x\nOK\n",
                           exit_code=0)
    decl = write_declaration(tmp_path / "deliverable", stub, "9.9.9", sha)
    brief = tmp_path / "brief.md"
    brief.write_text("hi\n", encoding="utf-8")
    log = deliverable / "inside-log" / "lane.log"
    scratch_base = tmp_path / "scratch_base"
    proc = run_launcher(deliverable=deliverable, lane="inside-log-lane",
                        model=DECLARED_MODEL, effort="medium", brief=brief, log=log,
                        declaration=decl, scratch_base=scratch_base)
    assert proc.returncode == 94, proc.stderr
    assert "ERR_LANE_LOG_PATH_INSIDE_SUBJECT" in proc.stderr
    assert not log.parent.exists(), "refusal must precede the log-dir mkdir"
    assert not scratch_base.exists(), "refusal must precede scratch creation"


# ---- Defect 3: a cleanup failure changes the return code + is recorded ------

def test_preflight_cleanup_failure_changes_return_code_and_is_recorded(tmp_path, monkeypatch):
    """If rmtree of the throwaway home fails, the run's exit status must change
    and the receipt must record the failure (never claim a deletion that did not
    happen)."""
    record, code = preflight._toolchain.resolve(preflight._toolchain.default_declaration_path())
    assert code == 0
    scratch = tmp_path / "scratch_outside"
    log = tmp_path / "out" / "preflight.log"
    receipt = tmp_path / "out" / "preflight.receipt.json"

    real_run = preflight.subprocess.run

    def fake_run(cmd, **kwargs):
        class P:
            returncode = 0
            stdout = f"OpenAI Codex v{record['version']}\nmodel: {DECLARED_MODEL}\nprovider: f\nOK\n"
            stderr = ""
        return P() if "exec" in cmd else real_run(cmd, **kwargs)

    monkeypatch.setattr(preflight.subprocess, "run", fake_run)
    real_rmtree = preflight.shutil.rmtree

    def failing_rmtree(path, *a, **k):
        raise OSError("simulated rmtree failure")

    monkeypatch.setattr(preflight.shutil, "rmtree", failing_rmtree)
    rc = preflight.main([
        "--model", DECLARED_MODEL, "--scratch", str(scratch),
        "--log", str(log), "--receipt", str(receipt),
    ])
    assert rc == preflight.EXIT_CLEANUP_FAILED, rc
    doc = json_load(receipt)
    assert doc["cleanup_outcome"]["home_removed"] is False
    assert doc["cleanup_outcome"]["errors"], "the cleanup failure must be recorded"
    assert "rmtree" in " ".join(doc["cleanup_outcome"]["errors"])


@pytest.mark.skipif(not GIT_BASH, reason="needs a POSIX shell")
def test_launcher_cleanup_failure_changes_exit_status(tmp_path):
    """Defect 3 (launcher half): a failed rm -rf must change the exit code and
    must not be swallowed with `|| true`."""
    deliverable = copy_deliverable(tmp_path / "deliverable")
    stub, sha = write_stub(tmp_path / "deliverable", version="9.9.9",
                           body="OpenAI Codex v9.9.9\nmodel: gpt-6.1-sol\nprovider: x\nOK\n",
                           exit_code=0)
    decl = write_declaration(tmp_path / "deliverable", stub, "9.9.9", sha)
    brief = tmp_path / "brief.md"
    brief.write_text("hi\n", encoding="utf-8")
    log = tmp_path / "out" / "lane.log"
    scratch_base = tmp_path / "scratch_base"

    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    fake_rm = fakebin / "rm"
    real_rm = shutil.which("rm")
    fake_rm.write_text(
        "#!/usr/bin/env sh\n"
        "case \"$1\" in\n"
        f"  -f) exec \"{real_rm}\" \"$@\" ;;\n"
        "  -rf) exit 1 ;;\n"
        "esac\n"
        f"exec \"{real_rm}\" \"$@\"\n",
        encoding="ascii",
    )
    fake_rm.chmod(0o755)
    proc = run_launcher(deliverable=deliverable, lane="rmfail", model=DECLARED_MODEL,
                        effort="medium", brief=brief, log=log, declaration=decl,
                        scratch_base=scratch_base,
                        extra_env={"PATH": str(fakebin) + os.pathsep + os.environ.get("PATH", "")})
    assert proc.returncode == 99, proc.stderr
    assert "CLEANUP_FAILED" in proc.stderr


def json_load(path):
    import json
    return json.loads(Path(path).read_text(encoding="utf-8"))
