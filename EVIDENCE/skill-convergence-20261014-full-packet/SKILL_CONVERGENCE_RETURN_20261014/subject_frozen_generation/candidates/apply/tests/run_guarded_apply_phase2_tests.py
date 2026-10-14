#!/usr/bin/env python3
"""Deterministic phase-2 tests for guarded_apply.py (PARTIAL_APPLY_TOOLING).

Every case drives the tool ONLY against fixtures under this candidate's own
``tests/_work_p2`` directory, and the immutable pre-image store is confined to
``tests/_work_p2/_store`` (inside the candidate root). No real skill tree is
read or written, and no acceptance token is ever minted.

Cases:
  * apply_success_with_readback
  * rollback_roundtrip_exact_bytes
  * stale_preimage_refused_before_write
  * mid_failure_compensation_restores_all
  * path_escape_refused_apply
  * junction_escape_refused_apply
  * symlink_escape_refused_apply   (SKIPPED if the host cannot create symlinks)
  * rollback_refuses_on_post_apply_drift

Run:  <qualified python> tests/run_guarded_apply_phase2_tests.py
Exit: 0 when every non-skipped case passes, 1 otherwise. Emits a JSON summary;
a skip is NOT counted as a pass.
"""
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOOL = ROOT / "guarded_apply.py"
P1_WORK = HERE / "_work"
WORK = HERE / "_work_p2"
STORE = WORK / "_store"

sys.path.insert(0, str(HERE))
import run_guarded_apply_tests as p1  # noqa: E402  (reuse fixture plumbing)
sys.path.insert(0, str(ROOT))
import guarded_apply as ga  # noqa: E402

sha256 = p1.sha256
sha256_file = p1.sha256_file


class Case:
    def __init__(self, name: str):
        self.name = name
        self.status = "pending"
        self.detail = ""
        self.requests: list[dict] = []
        self.responses: list[dict] = []


RESULTS: list[Case] = []
CURRENT: Case | None = None


def store_for(case_name: str) -> Path:
    """A store root unique per case, so one case's immutable ledger can never
    collide with another's. Still inside this candidate root."""
    s = STORE / case_name
    s.mkdir(parents=True, exist_ok=True)
    return s


def _record(case: Case, ok: bool, detail: str = "") -> None:
    case.status = "PASS" if ok else "FAIL"
    case.detail = detail
    RESULTS.append(case)


def _skip(case: Case, detail: str) -> None:
    case.status = "SKIPPED"
    case.detail = detail
    RESULTS.append(case)


def run_tool(args, store=True):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    full = [sys.executable, str(TOOL)] + list(args)
    if store:
        full += ["--store-root", str(store_for(CURRENT.name if CURRENT else "misc"))]
    req = {"argv": full, "cwd": str(ROOT)}
    proc = subprocess.run(full, capture_output=True, text=True,
                          cwd=str(ROOT), env=env, timeout=120)
    try:
        doc = json.loads(proc.stdout)
    except ValueError:
        doc = {"_unparsed_stdout": proc.stdout, "_stderr": proc.stderr}
    if CURRENT is not None:
        CURRENT.requests.append(req)
        CURRENT.responses.append({"returncode": proc.returncode,
                                  "stdout": doc, "stderr": proc.stderr.strip()})
    return proc, doc


def fresh(name: str) -> Path:
    base = WORK / name
    if base.exists():
        rmtree_force(base)
    base.mkdir(parents=True)
    return base


def rmtree_force(path: Path) -> None:
    """Remove a tree even when the immutable pre-image blobs are read-only:
    clear the read-only bit on failure and retry, using one shell throughout."""
    def onerror(func, target, exc_info):
        try:
            os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
            func(target)
        except OSError:
            pass
    shutil.rmtree(path, onerror=onerror)


def _tree(root: Path) -> dict:
    return {str(p): sha256_file(p) for p in root.rglob("*") if p.is_file()}


def build(case_name: str, base: Path):
    """Build a fixture whose round name is unique to the case, so its immutable
    ledger lives under a case-specific round directory and store root."""
    return p1.build_fixture(base, round_="SKCV-P2-%s" % case_name.upper())


# --------------------------------------------------------------------------- #
# cases
# --------------------------------------------------------------------------- #

def case_apply_success_with_readback():
    c = Case("apply_success_with_readback")
    base = fresh("apply_ok")
    fx = build(c.name, base)
    before = _tree(fx["root"])
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    cand = {k: sha256_file(Path(k)) for k in
            [t["candidate_path"] for t in fx["plan_doc"]["targets"]]}
    existing_ok = sha256_file(fx["root"] / "existing.txt") == sha256(b"candidate-A\n")
    new_ok = (fx["root"] / "newfile.txt").read_bytes() == b"brand-new\n"
    mod_ok = sha256_file(fx["root"] / "pkg" / "mod.py") == sha256(b"VALUE = 2\n")
    ledger = Path(doc.get("preimage_ledger", ""))
    blob_ok = bool(doc.get("preimage_entries")) and all(
        (Path(ledger).parent / e["preimage_path"]).is_file()
        for e in doc.get("preimage_entries", []) if e["preimage_path"])
    ok = (proc.returncode == 0 and doc.get("verdict") == "APPLY_OK"
          and doc.get("live") is True
          and doc.get("live_effects_scope") == "fixture_roots_only"
          and doc.get("claim_ceiling") == "PARTIAL_APPLY_TOOLING"
          and doc.get("canonical_acceptance") == "NOT_PERFORMED"
          and doc.get("acceptance_token_minted") is False
          and doc.get("fixture_label") == "FIXTURE_ONLY"
          and existing_ok and new_ok and mod_ok and blob_ok)
    _record(c, ok, "rc=%s verdict=%s existing=%s new=%s mod=%s blobs=%s"
            % (proc.returncode, doc.get("verdict"), existing_ok, new_ok, mod_ok, blob_ok))


def case_rollback_roundtrip_exact_bytes():
    c = Case("rollback_roundtrip_exact_bytes")
    base = fresh("rollback_ok")
    fx = build(c.name, base)
    before = _tree(fx["root"])
    run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    after_apply = _tree(fx["root"])
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--rollback", "--allow-fixture"])
    after_rb = _tree(fx["root"])
    ok = (proc.returncode == 0 and doc.get("verdict") == "ROLLBACK_OK"
          and before == after_rb and after_apply != before
          and not (fx["root"] / "newfile.txt").exists()
          and doc.get("canonical_acceptance") == "NOT_PERFORMED"
          and doc.get("acceptance_token_minted") is False)
    _record(c, ok, "rc=%s verdict=%s roundtrip_exact=%s"
            % (proc.returncode, doc.get("verdict"), before == after_rb))


def case_stale_preimage_refused_before_write():
    c = Case("stale_preimage_refused_before_write")
    details = []
    ok_all = True

    # (a) CLI: mutate a target after the plan was frozen; --apply must refuse at
    # validation, before any write.
    base = fresh("stale_apply_cli")
    fx = build(c.name, base)
    snapshot = _tree(fx["root"])
    (fx["root"] / "existing.txt").write_bytes(b"DRIFTED-BEFORE-APPLY\n")
    drifted = _tree(fx["root"])
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    after = _tree(fx["root"])
    ok_a = (proc.returncode == 2 and doc.get("error", {}).get("code") == "ERR_STALE_PREIMAGE"
            and after == drifted and not (fx["root"] / "newfile.txt").exists()
            and sha256_file(fx["root"] / "pkg" / "mod.py") == sha256(b"VALUE = 1\n"))
    ok_all = ok_all and ok_a
    details.append("cli:rc=%s code=%s nothing_written=%s"
                   % (proc.returncode, doc.get("error", {}).get("code"),
                      not (fx["root"] / "newfile.txt").exists()))

    # (b) module seam: drift a target AFTER validate() but BEFORE capture, so the
    # pre-write digest re-check / capture refuses and no write happens.
    base = fresh("stale_apply_seam")
    fx = build(c.name, base)
    plan = ga.load_plan(str(fx["plan"]))
    ctx = ga.validate(plan, allow_fixture=True)
    (fx["root"] / "pkg" / "mod.py").write_bytes(b"DRIFTED-AT-CAPTURE\n")
    seam_code = None
    try:
        ga.apply_plan(plan, ctx, str(store_for("stale_seam")), fault_inject_after=None)
    except ga.Refuse as exc:
        seam_code = exc.code
    ok_b = (seam_code == "ERR_STALE_PREIMAGE"
            and sha256_file(fx["root"] / "existing.txt") == sha256(b"original-A\n")
            and sha256_file(fx["root"] / "pkg" / "mod.py") == sha256(b"DRIFTED-AT-CAPTURE\n")
            and not (fx["root"] / "newfile.txt").exists())
    ok_all = ok_all and ok_b
    details.append("seam:code=%s nothing_written=%s"
                   % (seam_code, not (fx["root"] / "newfile.txt").exists()))
    _record(c, ok_all, "; ".join(details))


def case_mid_failure_compensation_restores_all():
    c = Case("mid_failure_compensation_restores_all")
    base = fresh("mid_failure")
    fx = build(c.name, base)
    before = _tree(fx["root"])
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture",
                          "--fault-inject-after", "1"])
    after = _tree(fx["root"])
    err = doc.get("error", {})
    detail_blob = {}
    if err.get("code") == "ERR_APPLY_COMPENSATED":
        detail_blob = json.loads(err["detail"])
    ok = (proc.returncode == 2 and err.get("code") == "ERR_APPLY_COMPENSATED"
          and detail_blob.get("error", {}).get("code") == "ERR_FAULT_INJECTED"
          and detail_blob.get("compensation_complete") is True
          and len(detail_blob.get("touched_before_failure", [])) == 2
          and before == after and not (fx["root"] / "newfile.txt").exists())
    _record(c, ok, "rc=%s code=%s touched=%s complete=%s restored_all=%s"
            % (proc.returncode, err.get("code"),
               len(detail_blob.get("touched_before_failure", [])),
               detail_blob.get("compensation_complete"), before == after))


def case_path_escape_refused_apply():
    c = Case("path_escape_refused_apply")
    details = []
    ok_all = True

    # traversal component
    base = fresh("p2_traversal")
    fx = build(c.name, base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(fx["root"]) + os.sep + ".." + os.sep + "escape.txt",
        "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p1.resync_all(fx)
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    ok_all = ok_all and proc.returncode == 2 and doc.get("error", {}).get("code") in (
        "ERR_TRAVERSAL", "ERR_ROOT_ESCAPE")
    details.append("traversal:code=%s" % doc.get("error", {}).get("code"))

    # absolute target outside every allowed root
    base = fresh("p2_outside")
    fx = build(c.name, base)
    outside = base / "outside.txt"
    outside.write_bytes(b"OUTSIDE\n")
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(outside), "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p1.resync_all(fx)
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    ok_all = ok_all and proc.returncode == 2 and doc.get("error", {}).get("code") == "ERR_ROOT_ESCAPE"
    ok_all = ok_all and outside.read_bytes() == b"OUTSIDE\n"
    details.append("outside:code=%s untouched=%s"
                   % (doc.get("error", {}).get("code"), outside.read_bytes() == b"OUTSIDE\n"))

    # relative target path
    base = fresh("p2_relative")
    fx = build(c.name, base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": "relative/escape.txt", "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p1.resync_all(fx)
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    ok_all = ok_all and proc.returncode == 2 and doc.get("error", {}).get("code") == "ERR_TARGET_PATH"
    details.append("relative:code=%s" % doc.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_junction_escape_refused_apply():
    c = Case("junction_escape_refused_apply")
    if os.name != "nt":
        _skip(c, "junctions are a Windows-only host capability (os.name=%s)" % os.name)
        return
    base = fresh("p2_junction")
    fx = build(c.name, base)
    outside = base / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_bytes(b"OUTSIDE\n")
    link = fx["root"] / "linkdir"
    made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                          capture_output=True, text=True)
    if made.returncode != 0 or not link.exists():
        _skip(c, "junction creation unavailable on this host: %s"
              % ((made.stdout or "") + (made.stderr or "")).strip())
        return
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(link / "secret.txt"), "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p1.resync_all(fx)
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    ok = (proc.returncode == 2 and doc.get("error", {}).get("code") == "ERR_SYMLINK_ESCAPE"
          and (outside / "secret.txt").read_bytes() == b"OUTSIDE\n")
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


def case_symlink_escape_refused_apply():
    c = Case("symlink_escape_refused_apply")
    base = fresh("p2_symlink")
    fx = build(c.name, base)
    outside = base / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_bytes(b"OUTSIDE\n")
    link = fx["root"] / "linkdir"
    try:
        os.symlink(str(outside), str(link), target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        _skip(c, "symlink creation unavailable on this host: %s" % exc)
        return
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(link / "secret.txt"), "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p1.resync_all(fx)
    proc, doc = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    ok = (proc.returncode == 2 and doc.get("error", {}).get("code") == "ERR_SYMLINK_ESCAPE"
          and (outside / "secret.txt").read_bytes() == b"OUTSIDE\n")
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


def case_rollback_refuses_on_post_apply_drift():
    c = Case("rollback_refuses_on_post_apply_drift")
    base = fresh("rollback_drift")
    fx = build(c.name, base)
    p_apply, d_apply = run_tool(["--plan", str(fx["plan"]), "--apply", "--allow-fixture"])
    # apply succeeded; now an unrelated edit lands on one applied target
    (fx["root"] / "existing.txt").write_bytes(b"UNAUTHORIZED-LATER-EDIT\n")
    drifted = sha256_file(fx["root"] / "existing.txt")
    p_rb, d_rb = run_tool(["--plan", str(fx["plan"]), "--rollback", "--allow-fixture"])
    still_drifted = sha256_file(fx["root"] / "existing.txt")
    ok = (p_apply.returncode == 0 and d_apply.get("verdict") == "APPLY_OK"
          and p_rb.returncode == 2 and d_rb.get("error", {}).get("code") == "ERR_ROLLBACK_DRIFT"
          and still_drifted == drifted
          and sha256_file(fx["root"] / "pkg" / "mod.py") == sha256(b"VALUE = 2\n"))
    _record(c, ok, "apply_rc=%s rb_rc=%s rb_code=%s drift_preserved=%s"
            % (p_apply.returncode, p_rb.returncode,
               d_rb.get("error", {}).get("code"), still_drifted == drifted))


CASES = [
    case_apply_success_with_readback,
    case_rollback_roundtrip_exact_bytes,
    case_stale_preimage_refused_before_write,
    case_mid_failure_compensation_restores_all,
    case_path_escape_refused_apply,
    case_junction_escape_refused_apply,
    case_symlink_escape_refused_apply,
    case_rollback_refuses_on_post_apply_drift,
]


def main() -> int:
    global CURRENT
    if WORK.exists():
        rmtree_force(WORK)
    WORK.mkdir(parents=True)
    STORE.mkdir(parents=True)

    for fn in CASES:
        case = Case(fn.__name__.replace("case_", ""))
        CURRENT = case
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - a harness crash is a FAIL, not a pass
            _record(case, False, "harness exception: %s: %s" % (type(exc).__name__, exc))
        CURRENT = None

    passed = [x for x in RESULTS if x.status == "PASS"]
    failed = [x for x in RESULTS if x.status == "FAIL"]
    skipped = [x for x in RESULTS if x.status == "SKIPPED"]
    summary = {
        "schema": "HGK-SKCV-GUARDED-APPLY-PHASE2-TEST-SUMMARY/1",
        "tool": "guarded_apply.py",
        "command": "%s tests/run_guarded_apply_phase2_tests.py" % sys.executable,
        "interpreter": sys.executable,
        "ran": [x.name for x in passed] + [x.name for x in failed],
        "skipped": [x.name for x in skipped],
        "passed": [x.name for x in passed],
        "failed": ["%s: %s" % (x.name, x.detail) for x in failed],
        "count": {"total": len(RESULTS), "pass": len(passed), "fail": len(failed),
                  "skip": len(skipped)},
        "test_fixture_only": True,
        "fixture_roots": str(WORK),
        "preimage_store": str(STORE),
        "claim_ceiling": "PARTIAL_APPLY_TOOLING",
        "live_effects_claimed": "fixture_roots_only",
        "canonical_acceptance": "NOT_PERFORMED",
        "skip_is_not_pass": True,
        "detail": {
            x.name: {"status": x.status, "detail": x.detail,
                     "requests": x.requests, "responses": x.responses}
            for x in RESULTS
        },
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
