#!/usr/bin/env python3
"""Guarded apply VALIDATION / DRY-RUN + real guarded APPLY / ROLLBACK
(PARTIAL_APPLY_TOOLING).

WorkOrder: WO-SKCV-20261014-APPLY (successor, decomposed).

This module carries two capability tiers:

  * ``--validate`` / ``--dry-run`` / ``--check-plan`` — the phase-1 read-only
    validator, preserved unchanged in behaviour.
  * ``--apply`` / ``--rollback`` — the phase-2 real, guarded, atomic writer and
    its compensating rollback. In the delivered tests these run ONLY against
    the tool's own fixtures under ``tests/_work_p2``.

Phase-2 apply / rollback contract:

  * Every write is atomic: bytes are written to a temp file IN THE TARGET
    directory, flushed + fsynced, then ``os.replace``d into place. A target is
    never truncated in place.
  * Before any write, each target's exact current bytes are copied into an
    IMMUTABLE pre-image store INSIDE this candidate root, keyed by target path
    plus digest, and recorded in a per-round ledger.
  * The whole plan is refused before touching anything if any pre-image is
    missing or stale; each target's digest is re-checked immediately before its
    write, and movement since validation is a typed stale-preimage refusal.
  * After each write the bytes are read back and re-hashed; a mismatch is a
    typed post-write error that compensates every touched file.
  * Rollback restores each touched target from the pre-image store atomically,
    then re-hashes to prove the exact original bytes are back. It refuses when
    unrelated post-apply drift is detected on a target it would overwrite.

What it does (stdlib only):

  * Load an immutable per-round plan whose rows each name ONE concrete absolute
    target path, its frozen *before* sha256 (or explicit ``null`` for a new
    target), the candidate file path, and the candidate *after* sha256.
  * Refuse empty or duplicate rows.
  * Refuse a target whose absolute path is not inside an exact allowed root, or
    that escapes via traversal, symlink or junction redirection.
  * Read the *current* bytes / digest of each source target and each candidate
    file and compare them to the plan. It never recomputes an "expected" digest
    to hide drift: a source digest mismatch or stale pre-image is a refusal.
  * Require a subject-bound review receipt (bound to the round, the allowed
    roots and the exact manifest digest) AND an owner scope declaration. A
    missing / stale / foreign / FAIL / INCONCLUSIVE / advisory-only review is a
    refusal before anything else runs.
  * Emit a labelled result (non-live for validation; fixture-scoped live
    effects for apply/rollback).

Honesty / authority ceiling:

  * This is a tooling candidate. It is NOT canonical authority. It never
    generates an acceptance token, an OracleReceipt or a canonical status, and
    nothing here may be used to derive one.
  * An advisory review may gate this explicitly scoped, owner-authorized LOCAL
    engineering operation, but it is never canonical authority. No self-grant
    and no implicit grant widening: a fixture review only ever authorizes a
    fixture root.
  * Fixture grants / reviews must carry ``test_fixture: true`` and
    ``live_effects_claimed: 0``. Such a grant is labelled ``FIXTURE_ONLY`` and
    is not portable to a real target; use with ``--allow-fixture`` confines
    every target to the plan's allowed roots marked as fixture roots. A live
    apply/rollback result claims effects ONLY inside those fixture roots.

Accepted modes / flags (enumerated):

  Modes (exactly one; default ``--validate``):
    --validate     validate the plan and emit a non-live validation result
    --dry-run      alias of --validate that labels the result a dry run
    --check-plan   alias of --validate for independent review
    --apply        atomically apply every target with pre-image capture and
                   post-write read-back (only against fixture roots here)
    --rollback     restore every touched target from the pre-image store

  Inputs:
    --plan PATH          immutable per-round plan JSON            (required)
    --allow-fixture      permit a TEST_FIXTURE grant; confines every target to
                         the plan's allowed roots marked as fixture roots

  Test-only seam (fixture grants only):
    --fault-inject-after N   deterministically fail after N successful writes
                             to drive mid-failure compensation. Refused unless
                             the grant is a fixture grant.

Exit codes: 0 = VALIDATE_OK / DRY_RUN_OK / APPLY_OK / ROLLBACK_OK,
            2 = REFUSED (fail-closed).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------- #
# constants / exit codes
# --------------------------------------------------------------------------- #

EXIT_OK = 0
EXIT_REFUSE = 2

PLAN_SCHEMA = "HGK-SKCV-APPLY-PLAN/2"
BINDING_SCHEMA = "HGK-SKCV-ADMITTED-BINDING/1"
SCOPE_SCHEMA = "HGK-SKCV-OWNER-SCOPE-DECLARATION/1"
REVIEW_SCHEMA = "HGK-SKCV-INDEPENDENT-REVIEW-RECEIPT/1"
RESULT_SCHEMA = "HGK-SKCV-VALIDATE-RESULT/1"

CLAIM_CEILING = "PARTIAL_VALIDATE_ONLY"
LIVE_EFFECTS_CLAIMED = 0

# Phase-2 (real guarded apply / rollback).
CLAIM_CEILING_APPLY = "PARTIAL_APPLY_TOOLING"
PREIMAGE_STORE_DIRNAME = ".guarded_preimage_store"
LEDGER_SCHEMA = "HGK-SKCV-PREIMAGE-LEDGER/1"
APPLY_RESULT_SCHEMA = "HGK-SKCV-APPLY-RESULT/1"
ROLLBACK_RESULT_SCHEMA = "HGK-SKCV-ROLLBACK-RESULT/1"

ACCEPTED_BINDING_AUTHORITIES = ("OWNER", "HGK")
ACCEPTED_REVIEW_VERDICTS = ("PASS", "FAIL", "INCONCLUSIVE")
FIXTURE_LABEL = "FIXTURE_ONLY"


class Refuse(Exception):
    """Fail-closed refusal. ``code`` is a stable machine error class."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail

    def as_dict(self) -> dict:
        return {"code": self.code, "detail": self.detail}


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: str | os.PathLike) -> str | None:
    p = Path(path)
    try:
        if not p.is_file():
            return None
        return sha256_bytes(p.read_bytes())
    except OSError:
        return None


def _require(obj: object, key: str, code: str, where: str) -> object:
    """Strict required-field fetch. Missing / null / empty is a refusal — never
    a permissive default."""
    if not isinstance(obj, dict) or key not in obj:
        raise Refuse(code, f"{where}: required field '{key}' is missing")
    value = obj[key]
    if value is None:
        raise Refuse(code, f"{where}: required field '{key}' is null")
    if isinstance(value, str) and not value.strip():
        raise Refuse(code, f"{where}: required field '{key}' is empty")
    return value


def _require_hex(obj: object, key: str, code: str, where: str) -> str:
    value = _require(obj, key, code, where)
    if not isinstance(value, str) or len(value) != 64:
        raise Refuse(code, f"{where}: field '{key}' is not a sha256 hex digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise Refuse(code, f"{where}: field '{key}' is not hex ({exc})") from exc
    return value.lower()


def _load_json_strict(path: str | os.PathLike, code: str, where: str) -> dict:
    p = Path(path)
    if not p.is_file():
        raise Refuse(code, f"{where}: file not found: {p}")
    raw = p.read_bytes()
    if not raw.strip():
        raise Refuse(code, f"{where}: file is empty (nonempty input required): {p}")
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise Refuse(code, f"{where}: not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(doc, dict):
        raise Refuse(code, f"{where}: top-level JSON must be an object")
    return doc


def _norm_abs(path: str) -> str:
    return os.path.normcase(os.path.abspath(path))


def _is_within(child: str, parent: str) -> bool:
    child_n = _norm_abs(child)
    parent_n = _norm_abs(parent)
    if child_n == parent_n:
        return True
    return child_n.startswith(parent_n.rstrip("\\/") + os.sep)


def _real(path: str) -> str:
    return os.path.realpath(path)


def _assert_no_link_components(target_abs: str, label: str) -> None:
    """Walk every existing component of an absolute target path and refuse if
    any component is a symlink / junction. Defeats symlink or junction escape
    and TOCTOU redirection through a linked directory."""
    parts = Path(target_abs).parts
    if not parts:
        return
    current = parts[0]
    for part in parts[1:]:
        current = os.path.join(current, part)
        if not os.path.exists(current) and not os.path.islink(current):
            # Remaining components do not exist yet; nothing left to traverse.
            break
        try:
            if os.path.islink(current):
                raise Refuse("ERR_SYMLINK_ESCAPE",
                             f"{label}: symlink/junction component: {current}")
        except OSError as exc:  # pragma: no cover - defensive
            raise Refuse("ERR_SYMLINK_ESCAPE",
                         f"{label}: could not stat component {current}: {exc}") from exc


def _validate_target_path(target_abs: str, allowed_roots: list[str], label: str) -> str:
    """Validate ONE concrete absolute target path against the exact allowed
    roots. Refuses relative paths, traversal, symlink/junction escape, and any
    path outside every allowed root. Returns the resolved real path."""
    if not isinstance(target_abs, str) or not target_abs.strip():
        raise Refuse("ERR_TARGET_PATH", f"{label}: target path is empty")
    if not os.path.isabs(target_abs):
        raise Refuse("ERR_TARGET_PATH", f"{label}: target path must be absolute: {target_abs!r}")
    norm = os.path.normpath(target_abs)
    if any(part == ".." for part in Path(norm).parts):
        raise Refuse("ERR_TRAVERSAL", f"{label}: traversal component in {target_abs!r}")
    if not any(_is_within(norm, r) for r in allowed_roots):
        raise Refuse("ERR_ROOT_ESCAPE",
                     f"{label}: target {norm!r} is outside every allowed root")
    _assert_no_link_components(norm, label)
    resolved = _real(norm)
    if not any(_is_within(resolved, _real(r)) for r in allowed_roots):
        raise Refuse("ERR_SYMLINK_ESCAPE",
                     f"{label}: target resolves outside every allowed root ({resolved})")
    if os.path.isdir(resolved):
        raise Refuse("ERR_TARGET_PATH", f"{label}: target is a directory, not a file")
    return resolved


# --------------------------------------------------------------------------- #
# plan normalization
# --------------------------------------------------------------------------- #

def _normalize_allowed_roots(plan: dict) -> list[str]:
    raw = _require(plan, "allowed_roots", "ERR_PLAN", "plan")
    if not isinstance(raw, list) or not raw:
        raise Refuse("ERR_PLAN_EMPTY", "plan.allowed_roots must be a nonempty list")
    roots: list[str] = []
    seen: set[str] = set()
    for i, r in enumerate(raw):
        where = f"plan.allowed_roots[{i}]"
        if not isinstance(r, str) or not r.strip():
            raise Refuse("ERR_PLAN", f"{where}: allowed root must be a nonempty string")
        if not os.path.isabs(r):
            raise Refuse("ERR_PLAN", f"{where}: allowed root must be absolute: {r!r}")
        key = _norm_abs(r)
        if key in seen:
            raise Refuse("ERR_PLAN", f"{where}: duplicate allowed root {r!r}")
        seen.add(key)
        roots.append(r)
    return roots


def normalize_targets(plan: dict) -> list[dict]:
    raw_targets = _require(plan, "targets", "ERR_PLAN", "plan")
    if not isinstance(raw_targets, list) or not raw_targets:
        raise Refuse("ERR_PLAN_EMPTY", "plan.targets must be a nonempty list")
    seen: set[str] = set()
    normalized: list[dict] = []
    for i, t in enumerate(raw_targets):
        where = f"plan.targets[{i}]"
        if not isinstance(t, dict):
            raise Refuse("ERR_PLAN", f"{where}: must be an object")
        target = str(_require(t, "target", "ERR_PLAN", where))
        if not os.path.isabs(target):
            raise Refuse("ERR_TARGET_PATH", f"{where}: target must be absolute: {target!r}")
        key = _norm_abs(target)
        if key in seen:
            raise Refuse("ERR_PLAN_DUPLICATE", f"{where}: duplicate target {target!r}")
        seen.add(key)
        if "before_sha256" not in t:
            raise Refuse("ERR_PLAN", f"{where}: required field 'before_sha256' is missing")
        pre = t["before_sha256"]
        if pre is not None:
            if not isinstance(pre, str) or len(pre) != 64:
                raise Refuse("ERR_PLAN", f"{where}: before_sha256 must be null or sha256 hex")
            try:
                int(pre, 16)
            except ValueError as exc:
                raise Refuse("ERR_PLAN", f"{where}: before_sha256 not hex") from exc
            pre = pre.lower()
        cand_path = str(_require(t, "candidate_path", "ERR_PLAN", where))
        cand_sha = _require_hex(t, "after_sha256", "ERR_PLAN", where)
        normalized.append({
            "target": target,
            "before_sha256": pre,
            "candidate_path": cand_path,
            "after_sha256": cand_sha,
        })
    normalized.sort(key=lambda x: _norm_abs(x["target"]))
    return normalized


def canonical_manifest(targets: list[dict]) -> bytes:
    """Deterministic, order-independent serialization of the manifest rows."""
    lines = []
    for t in sorted(targets, key=lambda x: _norm_abs(x["target"])):
        pre = t["before_sha256"] if t["before_sha256"] else "ABSENT"
        lines.append(f"{_norm_abs(t['target'])}\t{pre}\t{t['after_sha256']}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def manifest_digest(targets: list[dict]) -> str:
    return sha256_bytes(canonical_manifest(targets))


def load_plan(path: str) -> dict:
    plan = _load_json_strict(path, "ERR_PLAN", "plan")
    schema = str(_require(plan, "schema", "ERR_PLAN", "plan"))
    if schema != PLAN_SCHEMA:
        raise Refuse("ERR_PLAN_SCHEMA", f"plan.schema must be {PLAN_SCHEMA!r}, got {schema!r}")
    for key in ("plan_id", "round"):
        _require(plan, key, "ERR_PLAN", "plan")
    roots = _normalize_allowed_roots(plan)
    targets = normalize_targets(plan)
    plan["_allowed_roots"] = roots
    plan["_targets"] = targets
    plan["_manifest_sha256"] = manifest_digest(targets)
    plan["_plan_sha256"] = sha256_bytes(Path(path).read_bytes())
    return plan


# --------------------------------------------------------------------------- #
# binding / scope / review
# --------------------------------------------------------------------------- #

def _check_ref_digest(ref_obj: object, code: str, where: str) -> dict:
    if not isinstance(ref_obj, dict):
        raise Refuse(code, f"{where}: must be an object with path+sha256")
    path = str(_require(ref_obj, "path", code, where))
    declared = _require_hex(ref_obj, "sha256", code, where)
    actual = sha256_path(path)
    if actual is None:
        raise Refuse(code, f"{where}: referenced file not found: {path}")
    if actual != declared:
        raise Refuse("ERR_STALE_REF",
                     f"{where}: referenced file digest mismatch "
                     f"(declared {declared}, actual {actual})")
    return {"path": path, "sha256": actual}


def validate_binding(plan: dict, binding: dict) -> dict:
    where = "binding"
    if _require(binding, "schema", "ERR_BINDING", where) != BINDING_SCHEMA:
        raise Refuse("ERR_BINDING_SCHEMA", f"binding.schema must be {BINDING_SCHEMA!r}")
    binding_id = str(_require(binding, "id", "ERR_BINDING", where))
    authority = str(_require(binding, "authority", "ERR_BINDING", where)).upper()
    if authority not in ACCEPTED_BINDING_AUTHORITIES:
        raise Refuse("ERR_BINDING_AUTHORITY",
                     f"binding.authority must be one of {ACCEPTED_BINDING_AUTHORITIES}, got {authority!r}")
    status = str(_require(binding, "status", "ERR_BINDING", where)).upper()
    if status != "ADMITTED":
        raise Refuse("ERR_BINDING_STATUS", f"binding.status must be ADMITTED, got {status!r}")
    round_ = str(_require(binding, "round", "ERR_BINDING", where))
    if round_ != plan["round"]:
        raise Refuse("ERR_BINDING_FOREIGN",
                     f"binding.round {round_!r} != plan.round {plan['round']!r}")
    b_manifest = _require_hex(binding, "manifest_sha256", "ERR_BINDING", where)
    if b_manifest != plan["_manifest_sha256"]:
        raise Refuse("ERR_BINDING_STALE",
                     f"binding.manifest_sha256 {b_manifest} != manifest {plan['_manifest_sha256']}")
    test_fixture = _require(binding, "test_fixture", "ERR_BINDING", where)
    if not isinstance(test_fixture, bool):
        raise Refuse("ERR_BINDING", f"{where}: test_fixture must be a boolean")
    return {"id": binding_id, "authority": authority, "status": status,
            "manifest_sha256": b_manifest, "test_fixture": test_fixture}


def validate_scope(plan: dict, scope: dict) -> dict:
    """Owner scope declaration: the owner authorizes THIS exact scope. It is not
    a canonical grant and cannot be widened implicitly."""
    where = "owner_scope"
    if _require(scope, "schema", "ERR_SCOPE", where) != SCOPE_SCHEMA:
        raise Refuse("ERR_SCOPE_SCHEMA", f"scope.schema must be {SCOPE_SCHEMA!r}")
    owner = str(_require(scope, "owner", "ERR_SCOPE", where))
    round_ = str(_require(scope, "round", "ERR_SCOPE", where))
    if round_ != plan["round"]:
        raise Refuse("ERR_SCOPE_FOREIGN",
                     f"scope.round {round_!r} != plan.round {plan['round']!r}")
    s_manifest = _require_hex(scope, "manifest_sha256", "ERR_SCOPE", where)
    if s_manifest != plan["_manifest_sha256"]:
        raise Refuse("ERR_SCOPE_STALE",
                     f"scope.manifest_sha256 {s_manifest} != manifest {plan['_manifest_sha256']}")
    raw_roots = _require(scope, "allowed_roots", "ERR_SCOPE", where)
    if not isinstance(raw_roots, list) or not raw_roots:
        raise Refuse("ERR_SCOPE", f"{where}: allowed_roots must be a nonempty list")
    declared = {_norm_abs(str(r)) for r in raw_roots}
    plan_roots = {_norm_abs(r) for r in plan["_allowed_roots"]}
    if declared != plan_roots:
        raise Refuse("ERR_SCOPE_WIDEN",
                     "scope.allowed_roots must exactly equal plan.allowed_roots "
                     "(no implicit grant widening)")
    operation = str(_require(scope, "operation", "ERR_SCOPE", where))
    if operation not in ("LOCAL_ENGINEERING", "DRY_RUN_VALIDATE"):
        raise Refuse("ERR_SCOPE",
                     f"{where}: operation must be LOCAL_ENGINEERING or DRY_RUN_VALIDATE")
    live_effects = _require(scope, "live_effects_claimed", "ERR_SCOPE", where)
    if live_effects != 0:
        raise Refuse("ERR_SCOPE",
                     f"{where}: live_effects_claimed must be 0 for a non-live validation")
    test_fixture = _require(scope, "test_fixture", "ERR_SCOPE", where)
    if not isinstance(test_fixture, bool):
        raise Refuse("ERR_SCOPE", f"{where}: test_fixture must be a boolean")
    return {"owner": owner, "round": round_, "operation": operation,
            "manifest_sha256": s_manifest, "test_fixture": test_fixture}


def validate_review(plan: dict, receipt: dict) -> dict:
    where = "review_receipt"
    if _require(receipt, "schema", "ERR_REVIEW", where) != REVIEW_SCHEMA:
        raise Refuse("ERR_REVIEW_SCHEMA", f"review.schema must be {REVIEW_SCHEMA!r}")
    reviewer = str(_require(receipt, "reviewer", "ERR_REVIEW", where))
    verdict = str(_require(receipt, "verdict", "ERR_REVIEW", where)).upper()
    if verdict not in ACCEPTED_REVIEW_VERDICTS:
        raise Refuse("ERR_REVIEW_FOREIGN_VERDICT",
                     f"review.verdict {verdict!r} is not a recognized verdict")
    if verdict != "PASS":
        raise Refuse("ERR_REVIEW_NOT_PASS",
                     f"review.verdict must be PASS, got {verdict!r} (INCONCLUSIVE/FAIL are not acceptance)")
    round_ = str(_require(receipt, "round", "ERR_REVIEW", where))
    if round_ != plan["round"]:
        raise Refuse("ERR_REVIEW_FOREIGN",
                     f"review.round {round_!r} != plan.round {plan['round']!r}")
    r_manifest = _require_hex(receipt, "manifest_sha256", "ERR_REVIEW", where)
    if r_manifest != plan["_manifest_sha256"]:
        raise Refuse("ERR_REVIEW_STALE",
                     f"review.manifest_sha256 {r_manifest} != manifest {plan['_manifest_sha256']}")
    raw_roots = _require(receipt, "allowed_roots", "ERR_REVIEW", where)
    if not isinstance(raw_roots, list) or not raw_roots:
        raise Refuse("ERR_REVIEW", f"{where}: allowed_roots must be a nonempty list")
    declared = {_norm_abs(str(r)) for r in raw_roots}
    plan_roots = {_norm_abs(r) for r in plan["_allowed_roots"]}
    if declared != plan_roots:
        raise Refuse("ERR_REVIEW_FOREIGN",
                     f"{where}: allowed_roots do not match the plan's exact subject roots")
    advisory = _require(receipt, "advisory", "ERR_REVIEW", where)
    if not isinstance(advisory, bool):
        raise Refuse("ERR_REVIEW", f"{where}: advisory must be a boolean")
    test_fixture = _require(receipt, "test_fixture", "ERR_REVIEW", where)
    if not isinstance(test_fixture, bool):
        raise Refuse("ERR_REVIEW", f"{where}: test_fixture must be a boolean")
    live_effects = _require(receipt, "live_effects_claimed", "ERR_REVIEW", where)
    if not isinstance(live_effects, int) or live_effects != 0:
        raise Refuse("ERR_REVIEW", f"{where}: live_effects_claimed must be 0")
    if advisory and not test_fixture:
        raise Refuse("ERR_REVIEW_ADVISORY",
                     f"{where}: an advisory-only review may not gate a real target")
    return {"reviewer": reviewer, "verdict": verdict, "advisory": advisory,
            "test_fixture": test_fixture, "manifest_sha256": r_manifest}


# --------------------------------------------------------------------------- #
# validation pass (no mutation)
# --------------------------------------------------------------------------- #

def validate(plan: dict, allow_fixture: bool) -> dict:
    """Run the full read-only validation. Returns a context dict of verified
    target records, or raises Refuse."""

    binding_ref = _check_ref_digest(_require(plan, "binding_ref", "ERR_PLAN", "plan"),
                                    "ERR_BINDING", "plan.binding_ref")
    scope_ref = _check_ref_digest(_require(plan, "owner_scope_ref", "ERR_PLAN", "plan"),
                                  "ERR_SCOPE", "plan.owner_scope_ref")
    review_ref = _check_ref_digest(_require(plan, "review_receipt_ref", "ERR_PLAN", "plan"),
                                   "ERR_REVIEW", "plan.review_receipt_ref")

    binding = validate_binding(plan, _load_json_strict(binding_ref["path"], "ERR_BINDING", "binding"))
    scope = validate_scope(plan, _load_json_strict(scope_ref["path"], "ERR_SCOPE", "owner_scope"))
    review = validate_review(plan, _load_json_strict(review_ref["path"], "ERR_REVIEW", "review_receipt"))

    fixture_flags = (binding["test_fixture"], scope["test_fixture"], review["test_fixture"])
    is_fixture = any(fixture_flags)
    if is_fixture:
        if not all(fixture_flags):
            raise Refuse("ERR_FIXTURE_SCOPE",
                         "a fixture grant requires binding + scope + review to all be test_fixture=true")
        if not allow_fixture:
            raise Refuse("ERR_FIXTURE_SCOPE",
                         "TEST_FIXTURE grant present but --allow-fixture was not passed")

    records: list[dict] = []
    for t in plan["_targets"]:
        label = t["target"]
        resolved = _validate_target_path(t["target"], plan["_allowed_roots"], label)

        exists = os.path.isfile(resolved)
        if t["before_sha256"] is None:
            if exists and sha256_path(resolved) != t["after_sha256"]:
                raise Refuse("ERR_NEW_TARGET_PRESENT",
                             f"{label}: new target must be absent but a file exists "
                             f"that does not match the candidate")
        else:
            if not exists:
                raise Refuse("ERR_PREIMAGE_MISSING",
                             f"{label}: frozen pre-image expected but target is absent")
            actual_pre = sha256_path(resolved)
            if actual_pre != t["before_sha256"]:
                raise Refuse("ERR_STALE_PREIMAGE",
                             f"{label}: target differs from frozen before-image "
                             f"(expected {t['before_sha256']}, actual {actual_pre})")

        cand_path = t["candidate_path"]
        if not os.path.isfile(cand_path):
            raise Refuse("ERR_CANDIDATE_MISSING", f"{label}: candidate not found: {cand_path}")
        cand = Path(cand_path).read_bytes()
        if not cand:
            raise Refuse("ERR_CANDIDATE_EMPTY",
                         f"{label}: candidate is empty (nonempty input required)")
        if sha256_bytes(cand) != t["after_sha256"]:
            raise Refuse("ERR_CANDIDATE_MISMATCH",
                         f"{label}: candidate differs from frozen after-image "
                         f"(expected {t['after_sha256']}, actual {sha256_bytes(cand)})")

        records.append({
            "target": resolved,
            "target_identity": f"{plan['round']}:{_norm_abs(t['target'])}",
            "before_sha256": t["before_sha256"],
            "new_target": t["before_sha256"] is None,
            "new_target_absent": not exists,
            "candidate_path": cand_path,
            "after_sha256": t["after_sha256"],
        })

    return {
        "manifest_sha256": plan["_manifest_sha256"],
        "plan_sha256": plan["_plan_sha256"],
        "allowed_roots": plan["_allowed_roots"],
        "binding": binding,
        "scope": scope,
        "review": review,
        "binding_ref": binding_ref,
        "scope_ref": scope_ref,
        "review_ref": review_ref,
        "fixture_only": is_fixture,
        "records": records,
    }


# --------------------------------------------------------------------------- #
# phase 2: atomic writer + immutable pre-image store + rollback
# --------------------------------------------------------------------------- #

def _candidate_root() -> str:
    """The candidate root = the directory holding this tool. Every store write
    must stay inside it."""
    return os.path.dirname(os.path.abspath(__file__))


def _resolve_store_root(store_arg: str | None) -> str:
    root = os.path.abspath(store_arg) if store_arg else os.path.join(
        _candidate_root(), PREIMAGE_STORE_DIRNAME)
    if not _is_within(root, _candidate_root()):
        raise Refuse("ERR_STORE_ESCAPE",
                     f"pre-image store {root!r} is outside the candidate root "
                     f"{_candidate_root()!r}")
    return root


def _round_dir(store_root: str, plan: dict) -> str:
    """Per-round ledger directory. The manifest binding is enforced by the
    ledger's own ``manifest_sha256`` field (verified on load), NOT duplicated in
    the path, so the pre-image store stays well under the Windows MAX_PATH
    limit even under a deep candidate root."""
    round_key = "".join(c if c.isalnum() or c in "-_." else "_"
                        for c in str(plan["round"]))
    return os.path.join(store_root, round_key)


def _preimage_key(target_abs: str, digest: str) -> str:
    """Key a pre-image by target path PLUS digest (immutable, content-addressed).
    The key is the sha256 of both, so it stays a bounded 64-hex name; the exact
    target path and digest are recorded in full in the per-round ledger, and the
    blob's bytes are always re-hashed before use."""
    keyed = (f"{_norm_abs(target_abs)}\x00{digest}").encode("utf-8")
    return f"{sha256_bytes(keyed)}.bin"


def _store_immutable_blob(path: str, data: bytes) -> None:
    """Write a pre-image blob once, then seal it read-only. If the blob already
    exists its bytes MUST match: a mismatch is store corruption, never a silent
    overwrite (the store is immutable)."""
    if os.path.exists(path):
        try:
            existing = Path(path).read_bytes()
        except OSError as exc:
            raise Refuse("ERR_PREIMAGE_STORE",
                         f"pre-image blob unreadable: {path}: {exc}") from exc
        if existing != data:
            raise Refuse("ERR_PREIMAGE_STORE",
                         f"pre-image blob already exists with different bytes: {path}")
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".pre_tmp_", dir=os.path.dirname(path))
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        except BaseException:
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except OSError:
                pass
            raise
    try:
        os.chmod(path, stat.S_IREAD)
    except OSError:
        pass  # best effort; the digest check below is the real guard
    if sha256_path(path) != sha256_bytes(data):
        raise Refuse("ERR_PREIMAGE_STORE", f"pre-image blob read-back mismatch: {path}")


def _atomic_write(target_abs: str, data: bytes) -> None:
    """Write bytes atomically into place: temp file IN THE TARGET DIRECTORY,
    flush + fsync, then os.replace. The target is never truncated in place."""
    directory = os.path.dirname(target_abs) or "."
    fd, tmp = tempfile.mkstemp(prefix=".guarded_tmp_", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target_abs)
    except BaseException:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass
        raise
    try:  # best-effort directory durability
        dfd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    except OSError:
        pass


def _atomic_remove(target_abs: str) -> None:
    """Remove a file created by a new-target write (compensation / rollback)."""
    if os.path.exists(target_abs):
        os.remove(target_abs)


def capture_preimages(plan: dict, ctx: dict, store_root: str) -> dict:
    """Copy every target's exact current bytes into the immutable store and
    return a per-round ledger. Refuses the WHOLE plan (before any write) if any
    pre-image is missing or stale."""
    if not ctx["records"]:
        raise Refuse("ERR_PREIMAGE_MISSING", "plan has no targets; refusing a vacuous capture")
    rdir = _round_dir(store_root, plan)
    blob_dir = os.path.join(rdir, "preimages")
    entries: list[dict] = []
    for rec in ctx["records"]:
        target = rec["target"]
        if rec["new_target"]:
            if os.path.exists(target):
                raise Refuse("ERR_STALE_PREIMAGE",
                             f"{target}: new target must be absent at capture time")
            entries.append({
                "target": target,
                "target_identity": rec["target_identity"],
                "new_target": True,
                "before_sha256": None,
                "after_sha256": rec["after_sha256"],
                "preimage_path": None,
                "preimage_size": 0,
            })
            continue
        if not os.path.isfile(target):
            raise Refuse("ERR_PREIMAGE_MISSING",
                         f"{target}: frozen pre-image expected but target is absent")
        data = Path(target).read_bytes()
        digest = sha256_bytes(data)
        if digest != rec["before_sha256"]:
            raise Refuse("ERR_STALE_PREIMAGE",
                         f"{target}: target moved since validation "
                         f"(expected {rec['before_sha256']}, actual {digest})")
        blob = os.path.join(blob_dir, _preimage_key(target, digest))
        _store_immutable_blob(blob, data)
        entries.append({
            "target": target,
            "target_identity": rec["target_identity"],
            "new_target": False,
            "before_sha256": digest,
            "after_sha256": rec["after_sha256"],
            "preimage_path": os.path.relpath(blob, rdir),
            "preimage_size": len(data),
        })

    ledger = {
        "schema": LEDGER_SCHEMA,
        "round": plan["round"],
        "manifest_sha256": plan["_manifest_sha256"],
        "plan_sha256": plan["_plan_sha256"],
        "fixture_only": ctx["fixture_only"],
        "candidate_root": _candidate_root(),
        "allowed_roots": plan["_allowed_roots"],
        "entries": entries,
    }
    ledger_path = os.path.join(rdir, "ledger.json")
    payload = json.dumps(ledger, indent=2, ensure_ascii=False).encode("utf-8")
    if os.path.exists(ledger_path):
        existing = Path(ledger_path).read_bytes()
        if existing != payload:
            raise Refuse("ERR_LEDGER_CONFLICT",
                         f"an immutable ledger already exists for this round/subject: "
                         f"{ledger_path}")
    else:
        _atomic_write(ledger_path, payload)
    ledger["_ledger_path"] = ledger_path
    ledger["_round_dir"] = rdir
    return ledger


def _write_one(rec: dict) -> str:
    """Write ONE target atomically, with a pre-write digest re-check and a
    post-write read-back re-hash. Returns the re-read digest."""
    target = rec["target"]
    # Re-check the target's digest IMMEDIATELY before its write.
    if rec["new_target"]:
        if os.path.exists(target):
            raise Refuse("ERR_STALE_PREIMAGE",
                         f"{target}: new target appeared after validation")
    else:
        current = sha256_path(target)
        if current is None:
            raise Refuse("ERR_STALE_PREIMAGE", f"{target}: target vanished after validation")
        if current != rec["before_sha256"]:
            raise Refuse("ERR_STALE_PREIMAGE",
                         f"{target}: target moved since validation "
                         f"(expected {rec['before_sha256']}, actual {current})")

    cand_path = rec["candidate_path"]
    if not os.path.isfile(cand_path):
        raise Refuse("ERR_CANDIDATE_MISSING", f"{target}: candidate not found: {cand_path}")
    cand = Path(cand_path).read_bytes()
    if sha256_bytes(cand) != rec["after_sha256"]:
        raise Refuse("ERR_CANDIDATE_MISMATCH", f"{target}: candidate moved since validation")

    _atomic_write(target, cand)

    actual = sha256_path(target)
    if actual != rec["after_sha256"]:
        raise Refuse("ERR_POSTWRITE_MISMATCH",
                     f"{target}: post-write read-back mismatch "
                     f"(expected {rec['after_sha256']}, actual {actual})")
    return actual


def _restore_entry(entry: dict, round_dir: str) -> None:
    """Atomically restore ONE target from the pre-image store (or remove it for
    a new target) and verify the exact original bytes are back."""
    target = entry["target"]
    if entry["new_target"]:
        _atomic_remove(target)
        if os.path.exists(target):
            raise Refuse("ERR_ROLLBACK_VERIFY",
                         f"{target}: new target still present after rollback")
        return
    preimage = os.path.join(round_dir, entry["preimage_path"])
    if not os.path.isfile(preimage):
        raise Refuse("ERR_PREIMAGE_MISSING",
                     f"{target}: pre-image blob missing for rollback: {preimage}")
    data = Path(preimage).read_bytes()
    if sha256_bytes(data) != entry["before_sha256"]:
        raise Refuse("ERR_PREIMAGE_STORE",
                     f"{target}: pre-image blob digest mismatch: {preimage}")
    _atomic_write(target, data)
    actual = sha256_path(target)
    if actual != entry["before_sha256"]:
        raise Refuse("ERR_ROLLBACK_VERIFY",
                     f"{target}: rollback read-back mismatch "
                     f"(expected {entry['before_sha256']}, actual {actual})")


def _compensate(entries: list[dict], written: list[str], round_dir: str) -> list[dict]:
    """Restore every already-written target from the pre-image store. Best
    effort across all entries; returns per-target restore results."""
    results: list[dict] = []
    for entry in entries:
        if entry["target"] not in written:
            continue
        try:
            _restore_entry(entry, round_dir)
            results.append({"target": entry["target"], "restored": True})
        except Refuse as exc:  # keep compensating the rest
            results.append({"target": entry["target"], "restored": False,
                            "error": exc.as_dict()})
    return results


def apply_plan(plan: dict, ctx: dict, store_root: str,
               fault_inject_after: int | None = None) -> dict:
    """Real guarded apply: capture immutable pre-images, then atomically write
    every target with pre-write re-check and post-write read-back. A mid-plan
    failure compensates every touched file."""
    ledger = capture_preimages(plan, ctx, store_root)
    entries = ledger["entries"]
    round_dir = ledger["_round_dir"]

    written: list[str] = []
    applied: list[dict] = []
    try:
        for rec in ctx["records"]:
            digest = _write_one(rec)
            written.append(rec["target"])
            applied.append({
                "target": rec["target"],
                "target_identity": rec["target_identity"],
                "new_target": rec["new_target"],
                "before_sha256": rec["before_sha256"],
                "after_sha256": digest,
            })
            if fault_inject_after is not None and len(written) > fault_inject_after:
                raise Refuse(
                    "ERR_FAULT_INJECTED",
                    f"test seam: failing after {fault_inject_after} successful write(s)")
    except BaseException as exc:
        compensation = _compensate(entries, written, round_dir)
        failed = [c for c in compensation if not c["restored"]]
        detail = {
            "error": exc.as_dict() if isinstance(exc, Refuse) else
                     {"code": "ERR_INTERNAL", "detail": f"{type(exc).__name__}: {exc}"},
            "touched_before_failure": list(written),
            "compensation": compensation,
            "compensation_complete": not failed,
        }
        raise Refuse("ERR_APPLY_COMPENSATED",
                     json.dumps(detail, ensure_ascii=False)) from exc
    return {
        "ledger": ledger,
        "applied": applied,
        "touched": [e["target"] for e in applied],
    }


def load_ledger(plan: dict, store_root: str) -> dict:
    """Load the immutable per-round ledger for this exact subject (fail-closed:
    a missing or foreign ledger is a refusal, never an empty-pass)."""
    rdir = _round_dir(store_root, plan)
    ledger_path = os.path.join(rdir, "ledger.json")
    if not os.path.isfile(ledger_path):
        raise Refuse("ERR_LEDGER_MISSING",
                     f"no pre-image ledger for round {plan['round']!r} / "
                     f"manifest {plan['_manifest_sha256']}: {ledger_path}")
    ledger = json.loads(Path(ledger_path).read_bytes().decode("utf-8"))
    if ledger.get("schema") != LEDGER_SCHEMA:
        raise Refuse("ERR_LEDGER_MISSING", f"ledger schema mismatch: {ledger_path}")
    if ledger.get("manifest_sha256") != plan["_manifest_sha256"]:
        raise Refuse("ERR_LEDGER_FOREIGN",
                     "ledger manifest does not match this plan's manifest")
    if not ledger.get("entries"):
        raise Refuse("ERR_LEDGER_MISSING", "ledger has no entries; refusing a vacuous rollback")
    ledger["_ledger_path"] = ledger_path
    ledger["_round_dir"] = rdir
    return ledger


def rollback_plan(plan: dict, ctx: dict, store_root: str) -> dict:
    """Restore every touched target from the pre-image store. Refuses when an
    unrelated post-apply drift is detected on a target it would overwrite."""
    ledger = load_ledger(plan, store_root)
    entries = ledger["entries"]
    round_dir = ledger["_round_dir"]

    # Drift gate FIRST: check every target before overwriting anything.
    for entry in entries:
        target = entry["target"]
        if entry["new_target"]:
            if not os.path.exists(target):
                continue  # already absent: idempotent (a prior rollback finished)
            actual = sha256_path(target)
            if actual != entry["after_sha256"]:
                raise Refuse("ERR_ROLLBACK_DRIFT",
                             f"{target}: post-apply drift on a new target "
                             f"(expected applied {entry['after_sha256']}, actual {actual})")
        else:
            if not os.path.isfile(target):
                raise Refuse("ERR_ROLLBACK_DRIFT",
                             f"{target}: target is absent; cannot prove post-apply state")
            actual = sha256_path(target)
            if actual not in (entry["after_sha256"], entry["before_sha256"]):
                raise Refuse("ERR_ROLLBACK_DRIFT",
                             f"{target}: unrelated post-apply drift "
                             f"(expected applied {entry['after_sha256']} or original "
                             f"{entry['before_sha256']}, actual {actual})")

    restored: list[dict] = []
    for entry in entries:
        _restore_entry(entry, round_dir)
        restored.append({
            "target": entry["target"],
            "target_identity": entry["target_identity"],
            "restored_sha256": entry["before_sha256"],
            "new_target_removed": entry["new_target"],
        })
    # Final proof pass: every target is exactly back to its original bytes.
    for entry in entries:
        if entry["new_target"]:
            if os.path.exists(entry["target"]):
                raise Refuse("ERR_ROLLBACK_VERIFY",
                             f"{entry['target']}: still present after rollback")
        elif sha256_path(entry["target"]) != entry["before_sha256"]:
            raise Refuse("ERR_ROLLBACK_VERIFY",
                         f"{entry['target']}: not restored to original bytes")
    return {"ledger": ledger, "restored": restored,
            "touched": [e["target"] for e in entries]}


# --------------------------------------------------------------------------- #
# result envelope
# --------------------------------------------------------------------------- #

def _base_result(mode: str) -> dict:
    return {
        "schema": RESULT_SCHEMA,
        "mode": mode,
        "live": False,
        "live_effects_claimed": LIVE_EFFECTS_CLAIMED,
        "claim_ceiling": CLAIM_CEILING,
        "canonical_acceptance": "NOT_PERFORMED",
        "oracle_receipt": "NOT_CREATED",
        "advisory_review_is_authority": False,
        "generated_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }


def emit(doc: dict) -> None:
    json.dump(doc, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

MODES = ("validate", "dry-run", "check-plan")
APPLY_MODES = ("apply", "rollback")
ALL_MODES = MODES + APPLY_MODES


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Guarded apply VALIDATION + DRY-RUN + guarded APPLY/ROLLBACK "
                    "(tooling candidate; PARTIAL_APPLY_TOOLING)")
    ap.add_argument("--validate", action="store_true",
                    help="validate the plan and emit a non-live validation result (default)")
    ap.add_argument("--dry-run", action="store_true", dest="dry_run",
                    help="alias of --validate labelled as a dry run")
    ap.add_argument("--check-plan", action="store_true", dest="check_plan",
                    help="alias of --validate for independent review")
    ap.add_argument("--apply", action="store_true",
                    help="atomically apply every target with pre-image capture and read-back")
    ap.add_argument("--rollback", action="store_true",
                    help="restore every touched target from the immutable pre-image store")
    ap.add_argument("--plan", default=None, help="immutable per-round plan JSON (required)")
    ap.add_argument("--allow-fixture", action="store_true", dest="allow_fixture",
                    help="permit a TEST_FIXTURE grant (confined to the plan's allowed roots)")
    ap.add_argument("--store-root", default=None, dest="store_root",
                    help="pre-image store root inside this candidate (default: "
                         "candidate_root/.guarded_preimage_store)")
    ap.add_argument("--fault-inject-after", type=int, default=None, dest="fault_inject_after",
                    help="TEST seam (fixture grants only): fail after N successful writes "
                         "to drive mid-failure compensation")
    return ap


def _selected_mode(args: argparse.Namespace) -> str:
    chosen = [m for m in ALL_MODES if getattr(args, m.replace("-", "_"))]
    if len(chosen) > 1:
        raise Refuse("ERR_MODE", f"at most one mode flag may be set, got {chosen}")
    return chosen[0] if chosen else "validate"


def run(argv: list[str] | None = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)

    try:
        mode = _selected_mode(args)
    except Refuse as exc:
        emit({**_base_result("refused"), "verdict": "REFUSED", "refused": True,
              "error": exc.as_dict()})
        return EXIT_REFUSE

    if mode in APPLY_MODES:
        return _run_apply_or_rollback(args, mode)

    if not args.plan:
        emit({**_base_result(mode), "verdict": "REFUSED", "refused": True,
              "error": {"code": "ERR_PLAN", "detail": "--plan is required"}})
        return EXIT_REFUSE

    try:
        plan = load_plan(args.plan)
        ctx = validate(plan, allow_fixture=args.allow_fixture)
    except Refuse as exc:
        emit({**_base_result(mode), "verdict": "REFUSED", "refused": True,
              "error": exc.as_dict(), "plan": args.plan})
        return EXIT_REFUSE

    doc = {
        **_base_result(mode),
        "verdict": "DRY_RUN_OK" if mode == "dry-run" else "VALIDATE_OK",
        "dry_run": mode == "dry-run",
        "plan": args.plan,
        "plan_id": plan["plan_id"],
        "round": plan["round"],
        "allowed_roots": ctx["allowed_roots"],
        "manifest_sha256": ctx["manifest_sha256"],
        "plan_sha256": ctx["plan_sha256"],
        "binding": ctx["binding"],
        "owner_scope": ctx["scope"],
        "review": ctx["review"],
        "fixture_only": ctx["fixture_only"],
        "fixture_label": FIXTURE_LABEL if ctx["fixture_only"] else None,
        "target_count": len(ctx["records"]),
        "targets": [{
            "target": r["target"],
            "target_identity": r["target_identity"],
            "before_sha256": r["before_sha256"],
            "new_target": r["new_target"],
            "after_sha256": r["after_sha256"],
        } for r in ctx["records"]],
        "note": ("non-live validation only; no file was written; the real apply/rollback "
                 "and canonical admission-reader wiring are later WorkOrder scope"),
    }
    emit(doc)
    return EXIT_OK


def _apply_base_result(mode: str) -> dict:
    """Live-for-fixtures envelope. ``live`` is True only because a file inside
    the fixture roots really moved; ``live_effects_claimed`` still counts only
    fixture-root effects, and canonical authority is never minted here."""
    return {
        "schema": APPLY_RESULT_SCHEMA if mode == "apply" else ROLLBACK_RESULT_SCHEMA,
        "mode": mode,
        "live": True,
        "live_effects_scope": "fixture_roots_only",
        "claim_ceiling": CLAIM_CEILING_APPLY,
        "canonical_acceptance": "NOT_PERFORMED",
        "oracle_receipt": "NOT_CREATED",
        "advisory_review_is_authority": False,
        "acceptance_token_minted": False,
        "grant_widened": False,
        "generated_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }


def _run_apply_or_rollback(args: argparse.Namespace, mode: str) -> int:
    if not args.plan:
        emit({**_apply_base_result(mode), "verdict": "REFUSED", "refused": True,
              "error": {"code": "ERR_PLAN", "detail": "--plan is required"}})
        return EXIT_REFUSE
    try:
        store_root = _resolve_store_root(args.store_root)
    except Refuse as exc:
        emit({**_apply_base_result(mode), "verdict": "REFUSED", "refused": True,
              "error": exc.as_dict(), "plan": args.plan})
        return EXIT_REFUSE

    try:
        plan = load_plan(args.plan)
        ctx = validate(plan, allow_fixture=args.allow_fixture)
        if not ctx["fixture_only"]:
            raise Refuse("ERR_APPLY_NOT_AUTHORIZED",
                         "live apply/rollback here is confined to TEST_FIXTURE grants; "
                         "there is no real-target authorization in this candidate")
        if args.fault_inject_after is not None and args.fault_inject_after < 0:
            raise Refuse("ERR_FAULT_INJECTED", "--fault-inject-after must be >= 0")
        if mode == "apply":
            outcome = apply_plan(plan, ctx, store_root,
                                 fault_inject_after=args.fault_inject_after)
        else:
            if args.fault_inject_after is not None:
                raise Refuse("ERR_FAULT_INJECTED",
                             "--fault-inject-after applies only to --apply")
            outcome = rollback_plan(plan, ctx, store_root)
    except Refuse as exc:
        emit({**_apply_base_result(mode), "verdict": "REFUSED", "refused": True,
              "error": exc.as_dict(), "plan": args.plan,
              "fixture_only": True,
              "fixture_label": FIXTURE_LABEL,
              "portable_to_real_targets": False})
        return EXIT_REFUSE

    ledger = outcome["ledger"]
    doc = {
        **_apply_base_result(mode),
        "verdict": "APPLY_OK" if mode == "apply" else "ROLLBACK_OK",
        "plan": args.plan,
        "plan_id": plan["plan_id"],
        "round": plan["round"],
        "allowed_roots": ctx["allowed_roots"],
        "manifest_sha256": ctx["manifest_sha256"],
        "plan_sha256": ctx["plan_sha256"],
        "binding": ctx["binding"],
        "owner_scope": ctx["scope"],
        "review": ctx["review"],
        "fixture_only": ctx["fixture_only"],
        "fixture_label": FIXTURE_LABEL,
        "portable_to_real_targets": False,
        "preimage_store": ledger["_round_dir"],
        "preimage_ledger": ledger["_ledger_path"],
        "preimage_entries": [{
            "target": e["target"],
            "target_identity": e["target_identity"],
            "new_target": e["new_target"],
            "before_sha256": e["before_sha256"],
            "after_sha256": e["after_sha256"],
            "preimage_path": e["preimage_path"],
            "preimage_size": e["preimage_size"],
        } for e in ledger["entries"]],
    }
    if mode == "apply":
        doc["touched"] = outcome["touched"]
        doc["applied"] = outcome["applied"]
        doc["note"] = ("fixture-scoped live apply; each target written atomically and "
                       "read back; no acceptance token was minted")
    else:
        doc["touched"] = outcome["touched"]
        doc["restored"] = outcome["restored"]
        doc["note"] = ("fixture-scoped rollback; each target restored from the immutable "
                       "pre-image store and re-hashed; no acceptance token was minted")
    emit(doc)
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
