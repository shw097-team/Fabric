#!/usr/bin/env python3
"""Deterministic tests for guarded_apply.py (PARTIAL_VALIDATE_ONLY primitive).

Every test drives the tool ONLY through its CLI against fixtures under this
candidate's own cwd (tests/_work). No live skill tree is read or written. The
simulated binding / owner-scope / independent review are explicitly
TEST_FIXTURE (``test_fixture: true``, ``live_effects_claimed: 0``) and the tool
refuses a fixture grant unless ``--allow-fixture`` is passed.

Run:  <qualified python> tests/run_guarded_apply_tests.py
Exit: 0 when every case passes, 1 otherwise. Emits a JSON summary naming each
ran / skipped case and its result. An unavailable host capability is reported as
SKIPPED, and a skip is NOT counted as a pass.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOOL = ROOT / "guarded_apply.py"
WORK = HERE / "_work"

BINDING_SCHEMA = "HGK-SKCV-ADMITTED-BINDING/1"
SCOPE_SCHEMA = "HGK-SKCV-OWNER-SCOPE-DECLARATION/1"
REVIEW_SCHEMA = "HGK-SKCV-INDEPENDENT-REVIEW-RECEIPT/1"
PLAN_SCHEMA = "HGK-SKCV-APPLY-PLAN/2"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256(Path(p).read_bytes())


class Case:
    def __init__(self, name: str):
        self.name = name
        self.status = "pending"
        self.detail = ""


RESULTS: list[Case] = []


def _record(case: Case, ok: bool, detail: str = "") -> None:
    case.status = "PASS" if ok else "FAIL"
    case.detail = detail
    RESULTS.append(case)


def _skip(case: Case, detail: str) -> None:
    case.status = "SKIPPED"
    case.detail = detail
    RESULTS.append(case)


def run_tool(args, cwd=None):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, str(TOOL)] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True,
                          cwd=str(cwd or ROOT), env=env, timeout=120)


def parse(receipt: str) -> dict:
    return json.loads(receipt)


def _manifest_lines(plan_targets: list[dict]) -> list[str]:
    lines = []
    for t in sorted(plan_targets, key=lambda x: os.path.normcase(os.path.abspath(x["target"]))):
        pre = t["before_sha256"] or "ABSENT"
        lines.append("%s\t%s\t%s" % (os.path.normcase(os.path.abspath(t["target"])),
                                     pre, t["after_sha256"]))
    return lines


def manifest_sha(plan_targets: list[dict]) -> str:
    return sha256(("\n".join(_manifest_lines(plan_targets)) + "\n").encode("utf-8"))


def build_fixture(base: Path, targets=None, binding_status="ADMITTED", review_verdict="PASS",
                  review_advisory=False, review_test_fixture=True, binding_authority="OWNER",
                  round_="SKCV-TEST-ROUND", binding_manifest_override=None,
                  review_manifest_override=None, allow_fixture_expected=True,
                  binding_test_fixture=True, scope_test_fixture=True):
    """Build a self-consistent fixture plan tree. Returns a dict of paths."""
    root = base / "target"
    root.mkdir(parents=True, exist_ok=True)

    if targets is None:
        targets = []
        (root / "existing.txt").write_bytes(b"original-A\n")
        targets.append({"relpath": "existing.txt", "candidate_bytes": b"candidate-A\n",
                        "preimage": True})
        targets.append({"relpath": "newfile.txt", "candidate_bytes": b"brand-new\n",
                        "preimage": False})
        (root / "pkg").mkdir(exist_ok=True)
        (root / "pkg" / "mod.py").write_bytes(b"VALUE = 1\n")
        targets.append({"relpath": "pkg/mod.py", "candidate_bytes": b"VALUE = 2\n",
                        "preimage": True})

    cand_dir = base / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    plan_targets = []
    for i, t in enumerate(targets):
        rel = t["relpath"]
        cand_bytes = t["candidate_bytes"]
        cand_path = cand_dir / ("cand_%d_%s" % (i, rel.replace("/", "_")))
        if "cand_path" in t:
            cand_path = Path(t["cand_path"])
            cand_bytes = cand_path.read_bytes()
        else:
            cand_path.write_bytes(cand_bytes)
        tgt = root / rel
        pre = sha256_file(tgt) if t.get("preimage") else None
        plan_targets.append({
            "target": str(tgt),
            "before_sha256": pre,
            "candidate_path": str(cand_path),
            "after_sha256": sha256(cand_bytes),
        })

    manifest_digest = manifest_sha(plan_targets)

    binding_path = base / "binding.json"
    scope_path = base / "owner_scope.json"
    review_path = base / "review.json"
    binding_path.write_text(json.dumps({
        "schema": BINDING_SCHEMA, "id": "BIND-TEST-1", "authority": binding_authority,
        "status": binding_status, "round": round_,
        "manifest_sha256": binding_manifest_override or manifest_digest,
        "test_fixture": binding_test_fixture,
    }, indent=2), encoding="utf-8")
    scope_path.write_text(json.dumps({
        "schema": SCOPE_SCHEMA, "owner": "OWNER-TEST (simulated)", "round": round_,
        "manifest_sha256": manifest_digest, "allowed_roots": [str(root)],
        "operation": "LOCAL_ENGINEERING", "live_effects_claimed": 0,
        "test_fixture": scope_test_fixture,
    }, indent=2), encoding="utf-8")
    review_path.write_text(json.dumps({
        "schema": REVIEW_SCHEMA, "reviewer": "GLM-5.3-Flash (simulated)",
        "verdict": review_verdict, "round": round_,
        "manifest_sha256": review_manifest_override or manifest_digest,
        "allowed_roots": [str(root)], "advisory": review_advisory,
        "test_fixture": review_test_fixture, "live_effects_claimed": 0,
    }, indent=2), encoding="utf-8")

    plan = {
        "schema": PLAN_SCHEMA, "plan_id": "PLAN-TEST-1", "round": round_,
        "allowed_roots": [str(root)], "targets": plan_targets,
        "binding_ref": {"path": str(binding_path), "sha256": sha256_file(binding_path)},
        "owner_scope_ref": {"path": str(scope_path), "sha256": sha256_file(scope_path)},
        "review_receipt_ref": {"path": str(review_path), "sha256": sha256_file(review_path)},
    }
    plan_path = base / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    return {"root": root, "plan": plan_path, "binding": binding_path, "scope": scope_path,
            "review": review_path, "manifest_sha256": manifest_digest, "plan_doc": plan,
            "fixture_root": base}


def resync_refs(fx: dict) -> dict:
    """TEST plumbing: refresh plan ref digests after a test mutates a ref file.
    Does not loosen any guard."""
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["binding_ref"]["sha256"] = sha256_file(fx["binding"])
    plan["owner_scope_ref"]["sha256"] = sha256_file(fx["scope"])
    plan["review_receipt_ref"]["sha256"] = sha256_file(fx["review"])
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    fx["plan_doc"] = plan
    return fx


def resync_all(fx: dict) -> dict:
    """TEST plumbing: recompute the manifest digest from the current plan rows
    and rebind binding/scope/review to it, then refresh ref digests. This keeps
    the plan self-consistent after a test adds a row; it does not disable any
    guard."""
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    digest = manifest_sha(plan["targets"])
    for key, path in (("binding", fx["binding"]), ("scope", fx["scope"]),
                      ("review", fx["review"])):
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["manifest_sha256"] = digest
        path.write_text(json.dumps(doc), encoding="utf-8")
    fx["manifest_sha256"] = digest
    return resync_refs(fx)


def fresh(name: str) -> Path:
    base = WORK / name
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    return base


# --------------------------------------------------------------------------- #
# cases
# --------------------------------------------------------------------------- #

def case_positive_dry_run():
    c = Case("positive_dry_run")
    base = fresh("positive_dry_run")
    fx = build_fixture(base)
    before = {p: sha256_file(p) for p in fx["root"].rglob("*") if p.is_file()}
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    after = {p: sha256_file(p) for p in fx["root"].rglob("*") if p.is_file()}
    ok = (proc.returncode == 0 and doc["verdict"] == "DRY_RUN_OK"
          and doc["live"] is False and doc["live_effects_claimed"] == 0
          and doc["claim_ceiling"] == "PARTIAL_VALIDATE_ONLY"
          and doc["canonical_acceptance"] == "NOT_PERFORMED"
          and doc["fixture_label"] == "FIXTURE_ONLY"
          and doc["target_count"] == 3 and before == after)
    _record(c, ok, "rc=%s verdict=%s live=%s label=%s unchanged=%s"
            % (proc.returncode, doc.get("verdict"), doc.get("live"),
               doc.get("fixture_label"), before == after))


def case_live_apply_refused():
    c = Case("live_apply_without_fixture_grant_refused")
    # Phase 2 implements real apply/rollback. This case now asserts the phase-2
    # authorization boundary: a REAL (non-fixture) grant has no authorization in
    # this candidate, so --apply/--rollback fail closed (ERR_APPLY_NOT_AUTHORIZED)
    # with NO write and NO canonical token. The full fixture-scoped apply and
    # rollback lives in tests/run_guarded_apply_phase2_tests.py.
    base = fresh("live_refused")
    fx = build_fixture(base)
    for path in (fx["binding"], fx["scope"], fx["review"]):
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["test_fixture"] = False
        path.write_text(json.dumps(doc), encoding="utf-8")
    resync_refs(fx)
    p_apply = run_tool(["--plan", str(fx["plan"]), "--apply"])
    d_apply = parse(p_apply.stdout)
    p_rb = run_tool(["--plan", str(fx["plan"]), "--rollback"])
    d_rb = parse(p_rb.stdout)
    ok = (p_apply.returncode == 2 and d_apply["error"]["code"] == "ERR_APPLY_NOT_AUTHORIZED"
          and d_apply["acceptance_token_minted"] is False
          and p_rb.returncode == 2 and d_rb["error"]["code"] == "ERR_APPLY_NOT_AUTHORIZED"
          and not (fx["root"] / "newfile.txt").exists()
          and sha256_file(fx["root"] / "existing.txt") == sha256(b"original-A\n"))
    _record(c, ok, "apply_rc=%s apply_code=%s rb_rc=%s rb_code=%s"
            % (p_apply.returncode, d_apply.get("error", {}).get("code"),
               p_rb.returncode, d_rb.get("error", {}).get("code")))


def case_empty_manifest_refused():
    c = Case("empty_manifest_refused")
    details = []
    ok_all = True
    base = fresh("empty_plan")
    empty_plan = base / "plan.json"
    empty_plan.write_bytes(b"")
    p = run_tool(["--plan", str(empty_plan), "--dry-run"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_PLAN"
    details.append("empty_plan:code=%s" % d.get("error", {}).get("code"))

    base = fresh("empty_targets")
    plan = base / "plan.json"
    plan.write_text(json.dumps({"schema": PLAN_SCHEMA, "plan_id": "P", "round": "R",
                                "allowed_roots": [str(base)], "targets": []}), encoding="utf-8")
    p = run_tool(["--plan", str(plan), "--dry-run"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_PLAN_EMPTY"
    details.append("empty_targets:code=%s" % d.get("error", {}).get("code"))

    base = fresh("empty_allowed_roots")
    plan = base / "plan.json"
    plan.write_text(json.dumps({"schema": PLAN_SCHEMA, "plan_id": "P", "round": "R",
                                "allowed_roots": [], "targets": [
                                    {"target": str(base / "x"), "before_sha256": None,
                                     "candidate_path": str(base / "c"), "after_sha256": "0" * 64}]}),
                    encoding="utf-8")
    p = run_tool(["--plan", str(plan), "--dry-run"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_PLAN_EMPTY"
    details.append("empty_roots:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_duplicate_rows_refused():
    c = Case("duplicate_rows_refused")
    base = fresh("duplicates")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    dup = dict(plan["targets"][0])
    plan["targets"].append(dup)
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    ok = proc.returncode == 2 and doc["error"]["code"] == "ERR_PLAN_DUPLICATE"
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


def case_stale_preimage_refused():
    c = Case("stale_preimage_refused")
    base = fresh("stale")
    fx = build_fixture(base)
    (fx["root"] / "existing.txt").write_bytes(b"DRIFTED\n")
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    other = sha256_file(fx["root"] / "pkg" / "mod.py") == sha256(b"VALUE = 1\n")
    ok = (proc.returncode == 2 and doc["error"]["code"] == "ERR_STALE_PREIMAGE" and other)
    _record(c, ok, "rc=%s code=%s other_untouched=%s"
            % (proc.returncode, doc.get("error", {}).get("code"), other))


def case_missing_or_corrupt_candidate_refused():
    c = Case("missing_and_corrupt_candidate_refused")
    details = []
    ok_all = True

    base = fresh("candidate_missing")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    missing = Path(plan["targets"][0]["candidate_path"])
    missing.unlink()
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_CANDIDATE_MISSING"
    details.append("missing:code=%s" % d.get("error", {}).get("code"))

    base = fresh("candidate_corrupt")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    Path(plan["targets"][0]["candidate_path"]).write_bytes(b"TAMPERED\n")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_CANDIDATE_MISMATCH"
    details.append("corrupt:code=%s" % d.get("error", {}).get("code"))

    base = fresh("candidate_empty")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"][0]["after_sha256"] = sha256(b"")
    Path(plan["targets"][0]["candidate_path"]).write_bytes(b"")
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    resync_all(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_CANDIDATE_EMPTY"
    details.append("empty:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_traversal_and_outside_roots_refused():
    c = Case("traversal_and_outside_roots_refused")
    details = []
    ok_all = True

    base = fresh("traversal")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(fx["root"]) + os.sep + ".." + os.sep + "escape.txt",
        "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    resync_all(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] in (
        "ERR_TRAVERSAL", "ERR_ROOT_ESCAPE")
    details.append("traversal:code=%s" % d.get("error", {}).get("code"))

    # absolute target outside every allowed root
    base = fresh("outside_root")
    fx = build_fixture(base)
    outside = base / "outside.txt"
    outside.write_bytes(b"OUTSIDE\n")
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": str(outside), "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    resync_all(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_ROOT_ESCAPE"
    details.append("outside_root:code=%s" % d.get("error", {}).get("code"))

    # relative target path must be refused outright
    base = fresh("relative_target")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan["targets"].append({
        "target": "relative/escape.txt", "before_sha256": None,
        "candidate_path": str(base / "candidates" / "cand_0_existing.txt"),
        "after_sha256": sha256(b"candidate-A\n"),
    })
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    resync_all(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_TARGET_PATH"
    details.append("relative:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_symlink_escape_refused():
    c = Case("symlink_escape_refused")
    base = fresh("symlink")
    fx = build_fixture(base)
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
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    ok = (proc.returncode == 2 and doc["error"]["code"] == "ERR_SYMLINK_ESCAPE"
          and (outside / "secret.txt").read_bytes() == b"OUTSIDE\n")
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


def case_missing_or_stale_review_refused():
    c = Case("missing_and_stale_review_refused")
    details = []
    ok_all = True

    base = fresh("review_fail")
    fx = build_fixture(base, review_verdict="FAIL")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_REVIEW_NOT_PASS"
    details.append("fail:code=%s" % d.get("error", {}).get("code"))

    base = fresh("review_inconclusive")
    fx = build_fixture(base, review_verdict="INCONCLUSIVE")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_REVIEW_NOT_PASS"
    details.append("inconclusive:code=%s" % d.get("error", {}).get("code"))

    base = fresh("review_missing_verdict")
    fx = build_fixture(base)
    r = json.loads(fx["review"].read_text(encoding="utf-8"))
    r.pop("verdict", None)
    fx["review"].write_text(json.dumps(r), encoding="utf-8")
    resync_refs(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_REVIEW"
    details.append("missing:code=%s" % d.get("error", {}).get("code"))

    base = fresh("review_stale_manifest")
    fx = build_fixture(base, review_manifest_override="f" * 64)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_REVIEW_STALE"
    details.append("stale:code=%s" % d.get("error", {}).get("code"))

    base = fresh("review_stale_ref")
    fx = build_fixture(base)
    r = json.loads(fx["review"].read_text(encoding="utf-8"))
    r["note"] = "post-freeze edit"
    fx["review"].write_text(json.dumps(r), encoding="utf-8")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_STALE_REF"
    details.append("stale_ref:code=%s" % d.get("error", {}).get("code"))

    base = fresh("review_advisory_real")
    fx = build_fixture(base, review_advisory=True, review_test_fixture=False)
    # scope/binding stay real (non-fixture) -> advisory-only review must refuse.
    for path in (fx["binding"], fx["scope"]):
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc["test_fixture"] = False
        path.write_text(json.dumps(doc), encoding="utf-8")
    resync_refs(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_REVIEW_ADVISORY"
    details.append("advisory_real:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_missing_scope_and_widening_refused():
    c = Case("missing_scope_and_widening_refused")
    details = []
    ok_all = True

    base = fresh("scope_missing")
    fx = build_fixture(base)
    plan = json.loads(fx["plan"].read_text(encoding="utf-8"))
    plan.pop("owner_scope_ref", None)
    fx["plan"].write_text(json.dumps(plan), encoding="utf-8")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_PLAN"
    details.append("missing_scope_ref:code=%s" % d.get("error", {}).get("code"))

    base = fresh("scope_widen")
    fx = build_fixture(base)
    s = json.loads(fx["scope"].read_text(encoding="utf-8"))
    s["allowed_roots"] = [str(fx["root"]), str(base / "extra-root")]
    fx["scope"].write_text(json.dumps(s), encoding="utf-8")
    resync_refs(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_SCOPE_WIDEN"
    details.append("scope_widen:code=%s" % d.get("error", {}).get("code"))

    base = fresh("scope_stale")
    fx = build_fixture(base)
    s = json.loads(fx["scope"].read_text(encoding="utf-8"))
    s["manifest_sha256"] = "f" * 64
    fx["scope"].write_text(json.dumps(s), encoding="utf-8")
    resync_refs(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_SCOPE_STALE"
    details.append("scope_stale:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_binding_guards_refuse():
    c = Case("binding_guards_refuse")
    details = []
    ok_all = True

    base = fresh("binding_rogue_authority")
    fx = build_fixture(base, binding_authority="ROGUE")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_BINDING_AUTHORITY"
    details.append("rogue_authority:code=%s" % d.get("error", {}).get("code"))

    base = fresh("binding_draft")
    fx = build_fixture(base, binding_status="DRAFT")
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_BINDING_STATUS"
    details.append("draft:code=%s" % d.get("error", {}).get("code"))

    base = fresh("binding_stale_manifest")
    fx = build_fixture(base, binding_manifest_override="f" * 64)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_BINDING_STALE"
    details.append("stale_manifest:code=%s" % d.get("error", {}).get("code"))

    base = fresh("binding_foreign_round")
    fx = build_fixture(base)
    b = json.loads(fx["binding"].read_text(encoding="utf-8"))
    b["round"] = "OTHER-ROUND"
    fx["binding"].write_text(json.dumps(b), encoding="utf-8")
    resync_refs(fx)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    d = parse(p.stdout)
    ok_all = ok_all and p.returncode == 2 and d["error"]["code"] == "ERR_BINDING_FOREIGN"
    details.append("foreign_round:code=%s" % d.get("error", {}).get("code"))
    _record(c, ok_all, "; ".join(details))


def case_fixture_scope_and_flag():
    c = Case("fixture_scope_requires_flag")
    base = fresh("fixture_flag")
    fx = build_fixture(base)
    p = run_tool(["--plan", str(fx["plan"]), "--dry-run"])  # no --allow-fixture
    d = parse(p.stdout)
    ok = p.returncode == 2 and d["error"]["code"] == "ERR_FIXTURE_SCOPE"
    _record(c, ok, "rc=%s code=%s" % (p.returncode, d.get("error", {}).get("code")))


def case_check_plan_read_only():
    c = Case("check_plan_read_only_alias")
    base = fresh("checkplan")
    fx = build_fixture(base)
    snapshot = {p: sha256_file(p) for p in fx["root"].rglob("*") if p.is_file()}
    proc = run_tool(["--plan", str(fx["plan"]), "--check-plan", "--allow-fixture"])
    doc = parse(proc.stdout)
    after = {p: sha256_file(p) for p in fx["root"].rglob("*") if p.is_file()}
    ok = (proc.returncode == 0 and doc["verdict"] == "VALIDATE_OK"
          and snapshot == after and doc["live"] is False)
    _record(c, ok, "rc=%s verdict=%s unchanged=%s"
            % (proc.returncode, doc.get("verdict"), snapshot == after))


def case_new_target_present_refuses():
    c = Case("present_new_target_refuses")
    base = fresh("new_target_present")
    fx = build_fixture(base)
    (fx["root"] / "newfile.txt").write_bytes(b"SOMETHING-ELSE\n")
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    ok = proc.returncode == 2 and doc["error"]["code"] == "ERR_NEW_TARGET_PRESENT"
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


def case_junction_escape_refused():
    """Windows-native link escape via a directory junction (no elevation)."""
    c = Case("junction_escape_refused")
    if os.name != "nt":
        _skip(c, "junctions are a Windows-only host capability (os.name=%s)" % os.name)
        return
    base = fresh("junction")
    fx = build_fixture(base)
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
    resync_all(fx)
    proc = run_tool(["--plan", str(fx["plan"]), "--dry-run", "--allow-fixture"])
    doc = parse(proc.stdout)
    ok = (proc.returncode == 2 and doc["error"]["code"] == "ERR_SYMLINK_ESCAPE"
          and (outside / "secret.txt").read_bytes() == b"OUTSIDE\n")
    _record(c, ok, "rc=%s code=%s" % (proc.returncode, doc.get("error", {}).get("code")))


CASES = [
    case_positive_dry_run,
    case_live_apply_refused,
    case_empty_manifest_refused,
    case_duplicate_rows_refused,
    case_stale_preimage_refused,
    case_missing_or_corrupt_candidate_refused,
    case_traversal_and_outside_roots_refused,
    case_symlink_escape_refused,
    case_junction_escape_refused,
    case_missing_or_stale_review_refused,
    case_missing_scope_and_widening_refused,
    case_binding_guards_refuse,
    case_fixture_scope_and_flag,
    case_check_plan_read_only,
    case_new_target_present_refuses,
]


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    for fn in CASES:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - a harness crash is a FAIL, not a pass
            _record(Case(fn.__name__), False,
                    "harness exception: %s: %s" % (type(exc).__name__, exc))

    passed = [x for x in RESULTS if x.status == "PASS"]
    failed = [x for x in RESULTS if x.status == "FAIL"]
    skipped = [x for x in RESULTS if x.status == "SKIPPED"]
    summary = {
        "schema": "HGK-SKCV-GUARDED-APPLY-TEST-SUMMARY/2",
        "tool": "guarded_apply.py",
        "command": "%s tests/run_guarded_apply_tests.py" % sys.executable,
        "interpreter": sys.executable,
        "ran": [x.name for x in passed] + [x.name for x in failed],
        "skipped": [x.name for x in skipped],
        "passed": [x.name for x in passed],
        "failed": ["%s: %s" % (x.name, x.detail) for x in failed],
        "count": {"total": len(RESULTS), "pass": len(passed), "fail": len(failed),
                  "skip": len(skipped)},
        "test_fixture_only": True,
        "claim_ceiling": "PARTIAL_VALIDATE_ONLY",
        "skip_is_not_pass": True,
        "detail": {x.name: {"status": x.status, "detail": x.detail} for x in RESULTS},
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
