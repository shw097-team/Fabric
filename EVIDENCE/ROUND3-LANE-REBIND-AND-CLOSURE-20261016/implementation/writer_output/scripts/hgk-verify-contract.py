#!/usr/bin/env python3
"""hgk-verify-contract.py - read-only verify-lane contract tooling (P1).

Round FAR-LANE-SOD-007. CANDIDATE_ONLY. Three read-only subcommands:

  brief          --matrix M --round R --out O [--contract C]
  check-skeleton V [--contract C] [--matrix M] [--round R] [--expected-contract-sha256 H]
  validate       V [--contract C] [--matrix M] [--round R] [--expected-contract-sha256 H]

Exit codes (uniform across all three):
  0  operation valid / contract-compliant
  2  typed contract / schema / usage violation
  3  missing or unreadable input
  4  stale or identity mismatch (round, matrix digest, contract digest)

Every failure prints a typed JSON object {ok,error_code,reason,details} so an
argparse usage exit can never be mistaken for a typed refusal: the process exit
code always carries the same code that appears in error_code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

EXIT_OK = 0
EXIT_VIOLATION = 2
EXIT_MISSING = 3
EXIT_STALE = 4
EXIT_USAGE = 64

DEFAULT_CONTRACT = os.path.join("config", "verify-lane-contract.json")

REQUIRED_KEYS_FALLBACK = [
    "round",
    "verifier_model_and_provider",
    "verdict",
    "checks",
    "caveats",
    "unfinished",
]
CHECK_ITEM_KEYS_FALLBACK = ["id", "claim", "evidence", "holds"]
VERDICT_ENUM_FALLBACK = ["PASS", "PARTIAL", "FAIL"]
MAX_STRING_CHARS_FALLBACK = 250


class ContractError(Exception):
    """Typed failure carrying a uniform exit code and reason."""

    def __init__(self, code: int, reason: str, **details):
        super().__init__(reason)
        self.code = code
        self.reason = reason
        self.details = details


class TypedArgumentParser(argparse.ArgumentParser):
    """D08: argparse usage errors emit the typed JSON body with a distinct code."""

    def error(self, message):
        payload = {
            "ok": False,
            "error_code": "usage_error",
            "reason": "usage_error",
            "details": {"prog": self.prog, "message": message},
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        raise SystemExit(EXIT_USAGE)


def _fail(code: int, reason: str, **details):
    raise ContractError(code, reason, **details)


def emit_ok(payload: dict) -> int:
    payload = {"ok": True, "error_code": "OK", **payload}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return EXIT_OK


def emit_error(exc: ContractError) -> int:
    payload = {
        "ok": False,
        "error_code": exc.reason,
        "reason": exc.reason,
        "details": exc.details,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return exc.code


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        _fail(EXIT_MISSING, "file_missing", path=path)
    except OSError as exc:
        _fail(EXIT_MISSING, "file_unreadable", path=path, error=str(exc))


def read_json_strict(path: str) -> dict:
    """Parse JSON, rejecting duplicate object keys and non-object roots."""
    text = read_text(path)
    try:
        obj = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except ContractError:
        raise
    except ValueError as exc:
        _fail(EXIT_VIOLATION, "not_json", path=path, error=str(exc))
    if not isinstance(obj, dict):
        _fail(EXIT_VIOLATION, "not_object", path=path, kind=type(obj).__name__)
    return obj


def _reject_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            _fail(EXIT_VIOLATION, "duplicate_key", key=key)
        seen[key] = value
    return seen


def sha256_file(path: str) -> str:
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except FileNotFoundError:
        _fail(EXIT_MISSING, "file_missing", path=path)
    except OSError as exc:
        _fail(EXIT_MISSING, "file_unreadable", path=path, error=str(exc))


def load_contract(path: str):  # noqa: C901 - explicit schema reading
    data = read_json_strict(path)
    required_keys = data.get("required_keys", REQUIRED_KEYS_FALLBACK)
    if not isinstance(required_keys, list) or not all(
        isinstance(k, str) for k in required_keys
    ):
        _fail(EXIT_VIOLATION, "contract_bad_required_keys", path=path)
    max_chars = data.get("max_string_chars", MAX_STRING_CHARS_FALLBACK)
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 1:
        _fail(EXIT_VIOLATION, "contract_bad_max_string_chars", path=path)
    verdict_enum = data.get("verdict_enum", VERDICT_ENUM_FALLBACK)
    if not isinstance(verdict_enum, list) or not verdict_enum:
        _fail(EXIT_VIOLATION, "contract_bad_verdict_enum", path=path)
    check_keys = data.get("check_item_keys", CHECK_ITEM_KEYS_FALLBACK)
    if not isinstance(check_keys, list) or not all(
        isinstance(k, str) for k in check_keys
    ):
        _fail(EXIT_VIOLATION, "contract_bad_check_item_keys", path=path)
    status_enum = data.get("check_status_enum") or []
    if not isinstance(status_enum, list):
        _fail(EXIT_VIOLATION, "contract_bad_check_status_enum", path=path)
    return {
        "required_keys": required_keys,
        "max_string_chars": max_chars,
        "verdict_enum": verdict_enum,
        "check_item_keys": check_keys,
        "status_enum": status_enum,
    }


def ensure_expected_digest(path: str, expected: str | None, label: str) -> None:
    if not expected:
        return
    actual = sha256_file(path)
    if actual.lower() != expected.lower():
        _fail(
            EXIT_STALE,
            "digest_mismatch",
            subject=label,
            expected=expected.lower(),
            actual=actual,
        )


def canonical_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)


# --------------------------------------------------------------------------
# Subcommand: brief
# --------------------------------------------------------------------------
def cmd_brief(args) -> int:
    contract = load_contract(args.contract)
    ensure_expected_digest(args.contract, args.expected_contract_sha256, "contract")
    matrix = read_json_strict(args.matrix)
    ensure_expected_digest(args.matrix, args.expected_matrix_sha256, "matrix")

    items = matrix.get("ordered_items")
    if not isinstance(items, list) or not items:
        _fail(EXIT_VIOLATION, "matrix_has_no_ordered_items", matrix=args.matrix)
    rows = []
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            _fail(EXIT_VIOLATION, "matrix_item_not_object", matrix=args.matrix)
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            _fail(EXIT_VIOLATION, "matrix_item_missing_id", matrix=args.matrix)
        if item_id in seen:
            _fail(EXIT_VIOLATION, "matrix_item_duplicate_id", id=item_id)
        seen.add(item_id)
        claim = item.get("claim", "")
        control = item.get("control", "ordinary")
        rows.append((item_id, item.get("required", True), control, claim))

    matrix_sha = sha256_file(args.matrix)
    contract_sha = sha256_file(args.contract)

    lines = []
    lines.append(f"# VERIFY brief - round {args.round}")
    lines.append("")
    lines.append(f"contract: {args.contract}  sha256={contract_sha}")
    lines.append(f"matrix:   {args.matrix}  sha256={matrix_sha}")
    lines.append("")
    lines.append("## Bounded checklist (frozen denominator - do NOT rediscover scope)")
    lines.append("")
    lines.append("| # | id | required | control | claim |")
    lines.append("|---|----|----------|---------|-------|")
    for idx, (item_id, required, control, claim) in enumerate(rows, 1):
        lines.append(
            f"| {idx} | {item_id} | {'yes' if required else 'no'} | {control} | {claim} |"
        )
    lines.append("")
    lines.append("## Lane discipline (contract rules)")
    lines.append("")
    lines.append(
        "- skeleton_first = true: write the durable verdict skeleton at the target "
        "path BEFORE any discovery."
    )
    lines.append(
        "- forbid_heredoc_writes: never author artifacts with a heredoc or shell redirection."
    )
    lines.append(
        f"- max_string_chars = {contract['max_string_chars']} (Unicode code points, recursive)."
    )
    lines.append(
        "- default_tool_call_budget = 28 calls, counting nested and parallel calls; "
        "stop and checkpoint PARTIAL at the bound."
    )
    lines.append(
        "- typed_refusal: on refusal stop and emit BLOCKED; zero authorization retries; "
        "at most one transient-read retry."
    )
    lines.append("")
    lines.append("## Behavior required before discovery")
    lines.append("")
    lines.append("1. Emit `verdict.json` with one ordered NOT_RUN row per id above. Never initialize PASS.")
    lines.append("2. If the controller enforcement hook is not authorized, mark that rule BLOCKED.")
    lines.append("")

    out_path = os.path.abspath(args.out)
    out_root = os.path.abspath(args.round_root)
    if os.path.commonpath([out_path, out_root]) != out_root:
        _fail(EXIT_VIOLATION, "out_outside_round_root", out=out_path, round_root=out_root)
    for alias in (args.matrix, args.contract):
        if os.path.exists(out_path) and os.path.exists(alias):
            if os.path.samefile(out_path, alias):
                _fail(EXIT_VIOLATION, "out_aliases_input", out=out_path, input=alias)

    tmp_path = out_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines) + "\n")
    os.replace(tmp_path, out_path)
    return emit_ok(
        {
            "command": "brief",
            "round": args.round,
            "items": len(rows),
            "out": out_path,
            "matrix_sha256": matrix_sha,
            "contract_sha256": contract_sha,
        }
    )


# --------------------------------------------------------------------------
# Shared verdict-read helpers
# --------------------------------------------------------------------------
def load_verdict(path: str, contract: dict, args) -> dict:
    verdict = read_json_strict(path)
    for key in contract["required_keys"]:
        if key not in verdict:
            _fail(EXIT_VIOLATION, "missing_required_key", key=key, path=path)
    round_id = args.round or verdict.get("round")
    if args.round and verdict.get("round") != args.round:
        _fail(
            EXIT_STALE,
            "round_mismatch",
            expected=args.round,
            actual=verdict.get("round"),
        )
    return verdict


def check_skeleton_shape(verdict: dict, contract: dict, path: str) -> None:
    v = verdict.get("verdict")
    if v is not None and v not in contract["verdict_enum"]:
        _fail(EXIT_VIOLATION, "bad_verdict_enum", value=v, allowed=contract["verdict_enum"])
    checks = verdict.get("checks")
    if not isinstance(checks, list):
        _fail(EXIT_VIOLATION, "checks_not_list", path=path)


def iter_strings(obj, prefix=""):
    if isinstance(obj, str):
        yield prefix, obj
    elif isinstance(obj, dict):
        for k, val in obj.items():
            yield from iter_strings(val, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            yield from iter_strings(val, f"{prefix}[{i}]")


def cmd_check_skeleton(args) -> int:
    contract = load_contract(args.contract)
    ensure_expected_digest(args.contract, args.expected_contract_sha256, "contract")
    if args.matrix:
        read_json_strict(args.matrix)
        ensure_expected_digest(args.matrix, args.expected_matrix_sha256, "matrix")
    verdict = load_verdict(args.verdict, contract, args)
    check_skeleton_shape(verdict, contract, args.verdict)
    return emit_ok(
        {
            "command": "check-skeleton",
            "round": verdict.get("round"),
            "verdict": verdict.get("verdict"),
            "checks": len(verdict.get("checks", [])),
        }
    )


def cmd_validate(args) -> int:
    contract = load_contract(args.contract)
    ensure_expected_digest(args.contract, args.expected_contract_sha256, "contract")
    matrix = None
    if args.matrix:
        matrix = read_json_strict(args.matrix)
        ensure_expected_digest(args.matrix, args.expected_matrix_sha256, "matrix")
    manifest = None
    if args.manifest:
        manifest = read_json_strict(args.manifest)
        ensure_expected_digest(args.manifest, args.expected_manifest_sha256, "manifest")
    verdict = load_verdict(args.verdict, contract, args)
    check_skeleton_shape(verdict, contract, args.verdict)

    # D07: the verdict's declared input pins must match the supplied frozen
    # artifacts (re-verified, not merely declared). Only checked when supplied.
    if matrix is not None:
        declared = verdict.get("matrix_sha256")
        actual = sha256_file(args.matrix)
        if declared is not None and str(declared).lower() != actual.lower():
            _fail(EXIT_STALE, "verdict_matrix_pin_mismatch",
                  declared=declared, actual=actual)
    if manifest is not None:
        declared = verdict.get("manifest_sha256")
        actual = sha256_file(args.manifest)
        if declared is not None and str(declared).lower() != actual.lower():
            _fail(EXIT_STALE, "verdict_manifest_pin_mismatch",
                  declared=declared, actual=actual)

    # 1. Recursive string cap.
    cap = contract["max_string_chars"]
    for pointer, value in iter_strings(verdict):
        if len(value) > cap:
            _fail(
                EXIT_VIOLATION,
                "string_too_long",
                pointer=pointer,
                length=len(value),
                max=cap,
            )

    # 2. Verdict must be a concrete enum value for validate.
    if verdict.get("verdict") not in contract["verdict_enum"]:
        _fail(
            EXIT_VIOLATION,
            "bad_verdict_enum",
            value=verdict.get("verdict"),
            allowed=contract["verdict_enum"],
        )

    # 3. Check items shape + uniqueness + holds consistency.
    checks = verdict.get("checks")
    status_enum = contract["status_enum"] or []
    item_keys = contract["check_item_keys"]
    seen_ids = set()
    for pos, item in enumerate(checks):
        if not isinstance(item, dict):
            _fail(EXIT_VIOLATION, "check_item_not_object", index=pos)
        for key in item_keys:
            if key not in item:
                _fail(EXIT_VIOLATION, "check_item_missing_key", index=pos, key=key)
        if not isinstance(item.get("id"), str) or not item["id"]:
            _fail(EXIT_VIOLATION, "check_item_bad_id", index=pos)
        if item["id"] in seen_ids:
            _fail(EXIT_VIOLATION, "check_item_duplicate_id", id=item["id"])
        seen_ids.add(item["id"])
        if not isinstance(item.get("claim"), str):
            _fail(EXIT_VIOLATION, "check_item_bad_claim", id=item["id"])
        if not isinstance(item.get("evidence"), list):
            _fail(EXIT_VIOLATION, "check_item_evidence_not_list", id=item["id"])
        holds = item.get("holds")
        if not isinstance(holds, bool):
            _fail(EXIT_VIOLATION, "check_item_holds_not_bool", id=item["id"])
        status = item.get("status")
        if status_enum:
            if status not in status_enum:
                _fail(
                    EXIT_VIOLATION,
                    "check_item_bad_status",
                    id=item["id"],
                    value=status,
                    allowed=status_enum,
                )
            expected_holds = {"PASS": True, "FAIL": False}.get(status)
            if expected_holds is not None and holds is not expected_holds:
                _fail(
                    EXIT_VIOLATION,
                    "check_item_holds_status_inconsistent",
                    id=item["id"],
                    status=status,
                    holds=holds,
                )

    # 4. Frozen-denominator binding when a matrix is supplied.
    if matrix is not None:
        item_ids = []
        for item in matrix.get("ordered_items", []):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                item_ids.append(item["id"])
        unknown = sorted(set(seen_ids) - set(item_ids))
        if unknown:
            _fail(EXIT_VIOLATION, "checks_unknown_ids", ids=unknown)

    # 5. unfinished lists exactly the ids not PASS/FAIL.
    if matrix is not None and status_enum:
        non_final = {
            item["id"]
            for item in checks
            if item.get("status") in {"NOT_RUN", "BLOCKED"}
        }
        unfinished = verdict.get("unfinished")
        if not isinstance(unfinished, list):
            _fail(EXIT_VIOLATION, "unfinished_not_list")
        if set(unfinished) != non_final:
            _fail(
                EXIT_VIOLATION,
                "unfinished_inconsistent",
                expected=sorted(non_final),
                actual=sorted(str(x) for x in unfinished),
            )

    # 6. Aggregate verdict consistency.
    _check_aggregate(verdict, checks, contract, matrix)

    return emit_ok(
        {
            "command": "validate",
            "round": verdict.get("round"),
            "verdict": verdict.get("verdict"),
            "checks": len(checks),
        }
    )


def _check_aggregate(verdict: dict, checks: list, contract: dict, matrix) -> None:
    status_enum = contract["status_enum"]
    if not status_enum:
        return
    statuses = [c.get("status") for c in checks if isinstance(c, dict)]
    v = verdict.get("verdict")
    if v == "PASS":
        if matrix is None:
            _fail(
                EXIT_VIOLATION,
                "pass_requires_matrix_denominator",
                note="cannot prove complete coverage without the frozen matrix",
            )
        # D06: zero checks can never be a PASS.
        if not checks:
            _fail(EXIT_VIOLATION, "pass_with_zero_checks")
        required_ids = [
            item["id"]
            for item in matrix.get("ordered_items", [])
            if isinstance(item, dict) and item.get("required", True)
        ]
        by_id = {c.get("id"): c for c in checks if isinstance(c, dict)}
        if not required_ids:
            _fail(EXIT_VIOLATION, "pass_with_empty_denominator")
        # D06 (a): exact canonical order - the check sequence must equal the
        # frozen matrix denominator in order.
        matrix_ids = [
            item["id"]
            for item in matrix.get("ordered_items", [])
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        seq = [c.get("id") for c in checks if isinstance(c, dict)]
        if seq != matrix_ids:
            _fail(
                EXIT_VIOLATION,
                "pass_checks_not_in_canonical_order",
                expected=matrix_ids,
                actual=seq,
            )
        # D06 (b): every declared check must carry non-empty evidence.
        for c in checks:
            if not isinstance(c, dict):
                continue
            ev = c.get("evidence")
            if not isinstance(ev, list) or not ev:
                _fail(EXIT_VIOLATION, "pass_check_without_evidence", id=c.get("id"))
        # D06 (c): only frozen matrix runner/probe ids may appear (unknown => exit).
        unknown = sorted(set(seq) - set(matrix_ids))
        if unknown:
            _fail(EXIT_VIOLATION, "checks_unknown_ids", ids=unknown)
        # D06 (d): a mandatory negative control must be present AND observed with
        # its expected outcome (status PASS).
        negative_ids = [
            item["id"]
            for item in matrix.get("ordered_items", [])
            if isinstance(item, dict) and item.get("control") == "negative"
        ]
        if not negative_ids:
            _fail(EXIT_VIOLATION, "pass_without_negative_control")
        for nid in negative_ids:
            if by_id.get(nid, {}).get("status") != "PASS":
                _fail(
                    EXIT_VIOLATION,
                    "pass_negative_control_not_observed",
                    id=nid,
                    status=by_id.get(nid, {}).get("status"),
                )
        # D06 (e): complete proven coverage of every required id.
        for rid in required_ids:
            if by_id.get(rid, {}).get("status") != "PASS":
                _fail(
                    EXIT_VIOLATION,
                    "pass_with_incomplete_coverage",
                    id=rid,
                    status=by_id.get(rid, {}).get("status"),
                )
    elif v == "FAIL":
        if "FAIL" not in statuses:
            _fail(EXIT_VIOLATION, "fail_without_failed_check")
    elif v == "PARTIAL":
        if "FAIL" in statuses:
            _fail(EXIT_VIOLATION, "partial_with_failed_check_should_be_fail")
        if not any(s in {"NOT_RUN", "BLOCKED"} for s in statuses):
            _fail(EXIT_VIOLATION, "partial_without_incomplete_coverage")


def build_parser() -> argparse.ArgumentParser:
    parser = TypedArgumentParser(prog="hgk-verify-contract.py")
    sub = parser.add_subparsers(dest="command", required=True)

    brief = sub.add_parser("brief", help="emit a matrix-consuming verifier brief")
    brief.add_argument("--matrix", required=True)
    brief.add_argument("--round", required=True)
    brief.add_argument("--out", required=True)
    brief.add_argument("--contract", default=DEFAULT_CONTRACT)
    brief.add_argument("--round-root", default="var/far-lane-sod-007")
    brief.add_argument("--expected-contract-sha256", default=None)
    brief.add_argument("--expected-matrix-sha256", default=None)

    skel = sub.add_parser("check-skeleton", help="shape check for the durable skeleton")
    skel.add_argument("verdict")
    skel.add_argument("--contract", default=DEFAULT_CONTRACT)
    skel.add_argument("--matrix", default=None)
    skel.add_argument("--round", default=None)
    skel.add_argument("--expected-contract-sha256", default=None)
    skel.add_argument("--expected-matrix-sha256", default=None)

    val = sub.add_parser("validate", help="full conformance validation")
    val.add_argument("verdict")
    val.add_argument("--contract", default=DEFAULT_CONTRACT)
    val.add_argument("--matrix", default=None)
    val.add_argument("--manifest", default=None)
    val.add_argument("--round", default=None)
    val.add_argument("--expected-contract-sha256", default=None)
    val.add_argument("--expected-matrix-sha256", default=None)
    val.add_argument("--expected-manifest-sha256", default=None)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "brief": cmd_brief,
        "check-skeleton": cmd_check_skeleton,
        "validate": cmd_validate,
    }
    try:
        return handlers[args.command](args)
    except ContractError as exc:
        return emit_error(exc)
    except (BrokenPipeError, KeyboardInterrupt):
        return 130
    except Exception as exc:  # noqa: BLE001 - typed fail-closed
        return emit_error(ContractError(EXIT_VIOLATION, "internal_error", error=str(exc)))


if __name__ == "__main__":
    sys.exit(main())
