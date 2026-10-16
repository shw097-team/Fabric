#!/usr/bin/env python3
"""hgk-verify-evidence-runner.py - deterministic read-only evidence runner (P2).

Round FAR-LANE-SOD-007. CANDIDATE_ONLY.

  python hgk-verify-evidence-runner.py --matrix M --manifest F [--contract C]
      --expected-matrix-sha256 H [--expected-manifest-sha256 H] --out O [--twice]

Safety boundary (MF01):
  * Command probes are NEVER arbitrary argv. Only fixed, audited probe IDs from a
    built-in allowlist may execute, with a typed argument schema and shell=False.
  * Interpreter inline/encoded execution (-c/-e/-EncodedCommand) is rejected
    outright. The interpreter binary is selected from the round venv and the
    fallback (sys.executable) WITHOUT a manifest digest check; the executed lint
    tool (var/far-lane-sod-007/tools/hgk_lint.py) IS pinned by full sha256 against
    the subject manifest. (The prior "interpreter pinned by full sha256" claim was
    inaccurate and is downgraded here to the truth.)
  * A token denylist is applied as a supplementary refusal layer; it is never the
    safety proof. An unknown command or unknown probe ID fails closed.

Output-collision boundary (D01):
  * Every input path and --out are resolved with canonical realpath (case-
    insensitive on Windows). The run is refused (typed exit) when --out equals,
    or lives inside, any input (the matrix, the manifest, the contract, or any
    manifest artifact already consumed as evidence). There is no default output
    path.

Canonical body (D07):
  * The canonical body pins more than observations: each record also carries the
    declared control, expected_observation, expect (predicate + value) and probe
    declaration, so a change to an expectation changes body_sha256. Input pins
    (matrix + manifest) are re-verified AFTER the run as well as before it.

Exit codes:
  0  every executed predicate/control held and, with --twice, determinism held
  2  a predicate/control failed, a refusal fired, or the matrix is invalid
  3  missing / unreadable input
  4  stale identity or a prohibited ordinary probe/path (incl. --out collision)
  64 typed argparse usage error (JSON body, distinct from any substantive exit)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

EXIT_OK = 0
EXIT_FAIL = 2
EXIT_MISSING = 3
EXIT_STALE = 4
EXIT_USAGE = 64

TAIL = 400
DEFAULT_TIMEOUT = 20
MAX_INPUT_BYTES = 2_000_000

ROUND_ROOT = os.path.abspath(os.path.join("var", "far-lane-sod-007"))
PY_EXE = os.path.join(ROUND_ROOT, ".venv", "Scripts", "python.exe")
FALLBACK_PY = sys.executable
LINT_TOOL_ID = "ART-LINT-TOOL"

VALID_CONTROLS = {"ordinary", "negative"}
VALID_OBSERVATIONS = {"match", "mismatch", "refused"}

# Supplementary denylist tokens (MF01 layer 2 - never the sole proof).
DENY_TOKENS = [
    "write", "rm", "del", "mv", "cp", "mkdir", "touch", "set-content", "out-file",
    "tee", ">", "shutdown", "stop", "kill", "install", "pip", "npm", "git commit",
    "git push",
]
# Inline/encoded interpreter execution is always rejected.
INLINE_FLAGS = ["-c", "-e", "--eval", "-encodedcommand", "-command", "/c", "-exec"]

# Fixed audited probe allowlist: probe_id -> {argv_schema, lint_argv}
APPROVED_PROBES = {
    "py_lint_check_syntax": {
        "argv_schema": ["--check-syntax", "<artifact-id:py>"],
        "lint_argv": lambda art: ["--check-syntax", art],
    },
    "py_lint_deprecation_report": {
        "argv_schema": ["--deprecation-report", "-", "<artifact-id:py>"],
        "lint_argv": lambda art: ["--deprecation-report", "-", art],
    },
}

VALID_KINDS = {"command", "hash", "grep", "exists"}
KIND_PREDICATES = {
    "command": {"rc_zero", "equals"},
    "hash": {"sha256_prefix"},
    "grep": {"regex_match"},
    "exists": {"file_exists"},
}


class RunnerError(Exception):
    def __init__(self, code, reason, **details):
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.details = details


class TypedArgumentParser(argparse.ArgumentParser):
    """argparse usage errors emit the typed JSON body (D08), never plain usage."""

    def error(self, message):
        payload = {
            "ok": False,
            "error_code": "usage_error",
            "reason": "usage_error",
            "details": {"prog": self.prog, "message": message},
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        raise SystemExit(EXIT_USAGE)


def _fail(code, reason, **details):
    raise RunnerError(code, reason, **details)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def real_norm(path: str) -> str:
    return os.path.normcase(os.path.realpath(os.path.abspath(path)))


def read_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
    except FileNotFoundError:
        _fail(EXIT_MISSING, "file_missing", path=path)
    except OSError as exc:
        _fail(EXIT_MISSING, "file_unreadable", path=path, error=str(exc))
    except ValueError as exc:
        _fail(EXIT_FAIL, "not_json", path=path, error=str(exc))
    if not isinstance(obj, dict):
        _fail(EXIT_FAIL, "not_object", path=path)
    return obj


def canonical_bytes(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def is_below(child: str, parent: str) -> bool:
    child, parent = os.path.abspath(child), os.path.abspath(parent)
    try:
        return os.path.commonpath([child, parent]) == parent
    except ValueError:
        return False


def has_reparse_or_link(path: str) -> bool:
    if os.path.islink(path):
        return True
    try:
        if os.name == "nt":
            import stat as _stat

            attrs = os.lstat(path).st_file_attributes
            if attrs & _stat.FILE_ATTRIBUTE_REPARSE_POINT:
                return True
    except OSError:
        pass
    return False


def _python_exe() -> str:
    return PY_EXE if os.path.exists(PY_EXE) else FALLBACK_PY


def assert_out_not_input(out_path: str, inputs) -> None:
    """D01: refuse when --out equals or lives inside any consumed input tree."""
    out_r = real_norm(out_path)
    for label, path in inputs:
        if not path:
            continue
        in_r = real_norm(path)
        if out_r == in_r:
            _fail(EXIT_STALE, "out_aliases_input", out=out_path, input=path, label=label)
        if os.path.isdir(path):
            base = in_r.rstrip("\\/")
            if out_r == base or out_r.startswith(base + os.sep):
                _fail(
                    EXIT_STALE, "out_inside_input_tree", out=out_path, input=path, label=label
                )


def load_manifest(path: str) -> dict:
    manifest = read_json(path)
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        _fail(EXIT_FAIL, "manifest_no_artifacts", path=path)
    by_id = {}
    for art in artifacts:
        if not isinstance(art, dict) or not isinstance(art.get("artifact_id"), str):
            _fail(EXIT_FAIL, "manifest_bad_artifact", path=path)
        by_id[art["artifact_id"]] = art
    manifest["_by_id"] = by_id
    return manifest


def resolve_subject(manifest: dict, artifact_id: str):
    art = manifest["_by_id"].get(artifact_id)
    if art is None:
        _fail(EXIT_FAIL, "unknown_artifact_id", artifact_id=artifact_id)
    path = os.path.abspath(art["path"])
    if not is_below(path, ROUND_ROOT) and not is_below(path, os.path.abspath(".")):
        _fail(EXIT_STALE, "subject_outside_roots", path=path)
    return path, art


def refusal_check(argv: list, subject_path=None):
    """Return a refusal reason string, or None if the probe passes the boundary."""
    for raw in (str(a).strip().lower() for a in argv):
        if raw in INLINE_FLAGS or raw.startswith("--eval"):
            return "inline_or_encoded_execution"
        for bad in DENY_TOKENS:
            if bad in raw:
                return "non_read_only_probe"
    if subject_path is not None and not subject_path.lower().endswith(".py"):
        return "probe_subject_not_python"
    return None


def _declared_probe(item: dict) -> dict:
    """The declared probe identity minus executable argv (pinned in the body)."""
    probe = item.get("probe") or {}
    decl = {"kind": probe.get("kind")}
    for key in ("path", "pattern", "approved_probe_id", "timeout_s", "max_input_bytes"):
        if key in probe:
            decl[key] = probe.get(key)
    return decl


def run_probe(item: dict, manifest: dict, contract: dict) -> dict:
    probe = item.get("probe") or {}
    kind = probe.get("kind")
    expect = item.get("expect") or {}
    predicate = expect.get("predicate")
    control = item.get("control", "ordinary")
    expected_observation = item.get("expected_observation", "match")

    if control not in VALID_CONTROLS:
        _fail(EXIT_FAIL, "unknown_control", id=item.get("id"), control=control)
    if expected_observation not in VALID_OBSERVATIONS:
        _fail(
            EXIT_FAIL,
            "unknown_expected_observation",
            id=item.get("id"),
            expected_observation=expected_observation,
        )
    if kind not in VALID_KINDS:
        _fail(EXIT_FAIL, "unknown_probe_kind", id=item.get("id"), kind=kind)
    if predicate not in KIND_PREDICATES[kind]:
        _fail(
            EXIT_FAIL,
            "unknown_predicate_for_kind",
            id=item.get("id"),
            kind=kind,
            predicate=predicate,
        )

    rec = {
        "id": item.get("id"),
        "probe_kind": kind,
        "control": control,
        "expected_observation": expected_observation,
        "probe_declared": _declared_probe(item),
        "expect": {"predicate": predicate, "value": expect.get("value")},
        "subject_artifact_id": None,
        "subject_sha256": None,
        "argv": None,
        "executed": False,
        "rc": None,
        "status": None,
        "error_code": None,
        "refused": False,
        "reason": None,
        "stdout_tail": "",
        "stderr_tail": "",
        "sha256_of_stdout": None,
        "sha256_of_stderr": None,
        "predicate_holds": None,
        "holds": None,
    }

    if kind == "command":
        probe_id = probe.get("approved_probe_id")
        spec = APPROVED_PROBES.get(probe_id)
        argv = probe.get("argv")
        if spec is None:
            _fail(EXIT_STALE, "unknown_approved_probe_id", id=item.get("id"), probe_id=probe_id)
        if not isinstance(argv, list) or not argv or not isinstance(argv[0], str):
            _fail(EXIT_FAIL, "command_probe_bad_argv", id=item.get("id"))
        # Token-level refusal fires before any subject resolution.
        reason = refusal_check(argv)
        if reason:
            rec["argv"] = [str(a) for a in argv]
            rec["refused"] = True
            rec["reason"] = reason
            rec["status"] = "refused"
            rec["executed"] = False
            return _finish(item, rec, expect)
        artifact_id = argv[-1]
        subject_path, art = resolve_subject(manifest, artifact_id)
        subject_sha = art.get("sha256")
        if subject_sha and os.path.exists(subject_path):
            if sha256_file(subject_path) != subject_sha:
                _fail(
                    EXIT_STALE,
                    "subject_digest_mismatch",
                    id=item.get("id"),
                    artifact_id=artifact_id,
                )
        rec["subject_artifact_id"] = artifact_id
        rec["subject_sha256"] = subject_sha
        reason = refusal_check(argv, subject_path)
        if reason:
            rec["refused"] = True
            rec["reason"] = reason
            rec["status"] = "refused"
            rec["executed"] = False
            return _finish(item, rec, expect)
        lint_art = manifest["_by_id"].get(LINT_TOOL_ID)
        lint_path = (
            os.path.abspath(lint_art["path"])
            if lint_art
            else os.path.join(ROUND_ROOT, "tools", "hgk_lint.py")
        )
        if lint_art and sha256_file(lint_path) != lint_art.get("sha256"):
            _fail(EXIT_STALE, "lint_tool_digest_mismatch")
        lint_args = spec["lint_argv"](artifact_id)
        rec["argv"] = [
            os.path.basename(_python_exe()),
            "-B",
            os.path.relpath(lint_path, os.getcwd()).replace("\\", "/"),
            *lint_args,
        ]
        run_argv = [_python_exe(), "-B", lint_path] + spec["lint_argv"](subject_path)
        timeout = int(probe.get("timeout_s", DEFAULT_TIMEOUT))
        try:
            proc = subprocess.run(
                run_argv, shell=False, capture_output=True, timeout=timeout, cwd=ROUND_ROOT
            )
        except subprocess.TimeoutExpired:
            rec["executed"] = True
            rec["status"] = "timeout"
            rec["error_code"] = "command_timeout"
            return _finish(item, rec, expect)
        except OSError as exc:
            rec["executed"] = True
            rec["status"] = "spawn_failed"
            rec["error_code"] = str(exc)
            return _finish(item, rec, expect)
        rec["executed"] = True
        rec["rc"] = proc.returncode
        rec["status"] = "executed"
        out = proc.stdout or b""
        err = proc.stderr or b""
        rec["stdout_tail"] = out[:TAIL].decode("utf-8", "replace")
        rec["stderr_tail"] = err[:TAIL].decode("utf-8", "replace")
        rec["sha256_of_stdout"] = sha256_bytes(out)
        rec["sha256_of_stderr"] = sha256_bytes(err)
        rec["predicate_holds"] = _command_predicate(predicate, expect, rec["rc"], out)
        return _finish(item, rec, expect)

    artifact_id = probe.get("path")
    subject_path, art = resolve_subject(manifest, artifact_id)
    rec["subject_artifact_id"] = artifact_id
    rec["subject_sha256"] = art.get("sha256")
    rec["executed"] = True
    rec["status"] = "executed"
    value = expect.get("value")

    if kind == "exists":
        observed = os.path.isfile(subject_path)
        rec["predicate_holds"] = observed is bool(value)
    elif kind == "hash":
        prefix = value if isinstance(value, str) else ""
        if len(prefix) != 64 or not re.fullmatch(r"[0-9a-fA-F]{64}", prefix):
            _fail(EXIT_FAIL, "hash_prefix_must_be_full_64_hex", id=item.get("id"))
        observed = sha256_file(subject_path) if os.path.exists(subject_path) else ""
        rec["predicate_holds"] = observed.lower() == prefix.lower()
        rec["sha256_of_stdout"] = observed or None
    else:  # grep
        pattern = probe.get("pattern") if isinstance(probe.get("pattern"), str) else ""
        if not pattern:
            _fail(EXIT_FAIL, "grep_empty_pattern", id=item.get("id"))
        if os.path.getsize(subject_path) > int(probe.get("max_input_bytes", MAX_INPUT_BYTES)):
            _fail(EXIT_FAIL, "grep_input_too_large", id=item.get("id"))
        with open(subject_path, "r", encoding="utf-8") as fh:
            text = fh.read()
        rec["sha256_of_stdout"] = sha256_bytes(text.encode("utf-8"))
        try:
            compiled = re.compile(pattern)
        except re.error as exc:
            _fail(EXIT_FAIL, "grep_bad_regex", id=item.get("id"), error=str(exc))
        rec["predicate_holds"] = (compiled.search(text) is not None) is bool(value)

    return _finish(item, rec, expect)


def _finish(item, rec, expect) -> dict:
    control = item.get("control", "ordinary")
    expected_observation = item.get("expected_observation", "match")
    if rec["refused"]:
        rec["holds"] = expected_observation == "refused"
    else:
        held = rec["predicate_holds"]
        if held is None:
            rec["holds"] = False
        elif expected_observation == "refused":
            rec["holds"] = False
        elif control == "negative" and expected_observation == "mismatch":
            rec["holds"] = held is False
        else:
            rec["holds"] = held is True
    return rec


def _command_predicate(predicate, expect, rc, out_bytes) -> bool:
    value = expect.get("value")
    if predicate == "rc_zero":
        return rc == 0 and value is True
    if predicate == "equals":
        if not isinstance(value, dict):
            return False
        if value.get("rc") != rc:
            return False
        if "stdout_utf8" in value:
            return value["stdout_utf8"] == out_bytes.decode("utf-8", "replace")
        return True
    return False


def run_matrix(matrix: dict, manifest: dict, contract: dict) -> dict:
    items = matrix.get("ordered_items")
    if not isinstance(items, list) or not items:
        _fail(EXIT_FAIL, "matrix_has_no_ordered_items")
    seen = set()
    records = []
    for item in items:
        if not isinstance(item, dict):
            _fail(EXIT_FAIL, "matrix_item_not_object")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            _fail(EXIT_FAIL, "matrix_item_missing_id")
        if item_id in seen:
            _fail(EXIT_FAIL, "matrix_item_duplicate_id", id=item_id)
        seen.add(item_id)
        records.append(run_probe(item, manifest, contract))

    ordinary = [r for r in records if _control_of(items, r["id"]) == "ordinary"]
    executed_ordinary = [r for r in ordinary if r.get("executed") and not r.get("refused")]
    coverage = {
        "total": len(records),
        "ordinary": len(ordinary),
        "executed_ordinary": len(executed_ordinary),
        "refused": len([r for r in records if r.get("refused")]),
    }
    aggregate = {
        "all_hold": all(r.get("holds") is True for r in records),
        "records": len(records),
    }
    return {"ordered_records": records, "coverage": coverage, "aggregate": aggregate}


def _control_of(items, item_id):
    for item in items:
        if isinstance(item, dict) and item.get("id") == item_id:
            return item.get("control", "ordinary")
    return "ordinary"


def top_envelope(matrix_sha, manifest_sha, contract_sha, runner_sha, body):
    body_sha = sha256_bytes(canonical_bytes(body))
    return {
        "schema_version": 1,
        "round": "FAR-LANE-SOD-007",
        "matrix_sha256": matrix_sha,
        "manifest_sha256": manifest_sha,
        "contract_sha256": contract_sha,
        "runner_sha256": runner_sha,
        "body": body,
        "body_sha256": body_sha,
    }


def _check_expected(path, expected, label):
    if not expected:
        return
    actual = sha256_file(path)
    if actual.lower() != expected.lower():
        _fail(EXIT_STALE, "digest_mismatch", subject=label, expected=expected, actual=actual)


def _run(args) -> int:
    start = time.monotonic()
    out_path = os.path.abspath(args.out)
    if not is_below(out_path, ROUND_ROOT):
        _fail(EXIT_STALE, "out_outside_round_root", out=out_path)

    matrix = read_json(args.matrix)
    manifest = load_manifest(args.manifest)
    contract = read_json(args.contract)
    _check_expected(args.matrix, args.expected_matrix_sha256, "matrix")
    _check_expected(args.manifest, args.expected_manifest_sha256, "manifest")
    if has_reparse_or_link(args.matrix) or has_reparse_or_link(args.manifest):
        _fail(EXIT_STALE, "input_reparse_point_rejected")

    # D01: refuse an --out that aliases or lives inside any consumed input tree.
    inputs = [("matrix", args.matrix), ("manifest", args.manifest), ("contract", args.contract)]
    for art in manifest.get("artifacts", []):
        if isinstance(art, dict) and art.get("path"):
            inputs.append(("artifact:" + str(art.get("artifact_id")), art["path"]))
    assert_out_not_input(out_path, inputs)

    matrix_sha = sha256_file(args.matrix)
    manifest_sha = sha256_file(args.manifest)
    contract_sha = sha256_file(args.contract)
    runner_sha = sha256_file(os.path.abspath(__file__))

    if matrix.get("contract_sha256") and matrix["contract_sha256"] != contract_sha:
        _fail(EXIT_STALE, "matrix_contract_digest_mismatch")
    if manifest.get("contract_sha256") and manifest["contract_sha256"] != contract_sha:
        _fail(EXIT_STALE, "manifest_contract_digest_mismatch")

    body1 = run_matrix(matrix, manifest, contract)
    envelope = top_envelope(matrix_sha, manifest_sha, contract_sha, runner_sha, body1)

    determinism = None
    exit_code = EXIT_OK
    if args.twice:
        body2 = run_matrix(matrix, manifest, contract)
        run2_sha = sha256_bytes(canonical_bytes(body2))
        identical = canonical_bytes(body1) == canonical_bytes(body2)
        determinism = {
            "run1": envelope["body_sha256"],
            "run2": run2_sha,
            "identical": identical,
            "body_recomputable": True,
        }
        if not identical:
            exit_code = EXIT_FAIL

    # D07: re-verify the frozen input pins AFTER the run as well as before it.
    if sha256_file(args.matrix) != matrix_sha:
        _fail(EXIT_STALE, "matrix_changed_during_run")
    if sha256_file(args.manifest) != manifest_sha:
        _fail(EXIT_STALE, "manifest_changed_during_run")
    for pid, art in manifest["_by_id"].items():
        expected = art.get("sha256")
        if expected is None:
            continue
        now = sha256_file(art["path"]) if os.path.exists(art["path"]) else None
        if now != expected:
            _fail(EXIT_STALE, "subject_moved_during_run", artifact_id=pid)

    if not envelope["body"]["aggregate"]["all_hold"]:
        exit_code = EXIT_FAIL
    if envelope["body"]["coverage"]["executed_ordinary"] == 0:
        _fail(EXIT_FAIL, "no_executed_ordinary_coverage")

    envelope["generated_at"] = "1970-01-01T00:00:00Z"
    envelope["duration_ms"] = round((time.monotonic() - start) * 1000.0, 3)
    envelope["out"] = os.path.relpath(out_path, os.getcwd()).replace("\\", "/")
    if determinism is not None:
        envelope["determinism"] = determinism
    envelope["ok"] = exit_code == EXIT_OK
    envelope["error_code"] = "OK" if exit_code == EXIT_OK else "PREDICATE_OR_DETERMINISM_FAILED"

    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    os.replace(tmp, out_path)
    return exit_code


def main(argv=None) -> int:
    parser = TypedArgumentParser(prog="hgk-verify-evidence-runner.py")
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--contract", default=os.path.join("config", "verify-lane-contract.json"))
    parser.add_argument("--expected-matrix-sha256", default=None)
    parser.add_argument("--expected-manifest-sha256", default=None)
    parser.add_argument("--out", required=True)
    parser.add_argument("--twice", action="store_true")
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except RunnerError as exc:
        sys.stdout.write(
            json.dumps(
                {"ok": False, "error_code": exc.reason, "reason": exc.reason, "details": exc.details},
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
