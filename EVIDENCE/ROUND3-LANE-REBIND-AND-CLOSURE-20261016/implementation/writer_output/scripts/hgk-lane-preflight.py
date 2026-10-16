#!/usr/bin/env python3
"""T2 - bounded pre-lane identity preflight + typed failure classification.

Runs ONE trivial prompt (a one-line echo, budget <= 120 s) through the DECLARED
Codex CLI - resolved and verified by hgk-lane-toolchain.py (T1) - BEFORE any long
lane. It classifies the outcome and writes a receipt.

Typed failure codes (exactly two):
  LANE_TOOLCHAIN_MISMATCH  HARNESS fault: a models-cache schema error
                           (``failed to load models cache: missing field ...``),
                           ``Model metadata for <model> not found``, an unknown
                           subcommand/flag, or the unsupported stdin form
                           (``error: unexpected argument '-' found``). The
                           offending build (path + version) is named. Substitution
                           is REFUSED.
  LANE_MODEL_REFUSED       a genuine provider refusal on the declared model while
                           the build identity matches. Only this class may open a
                           declared model deviation.

Internal non-failure states (never open a deviation):
  LANE_OK                  exit 0 and the CLI header named the declared model.
  LANE_INCONCLUSIVE        timeout / empty / unparsable. Not a verdict.

Receipt fields (additive): ``codex_cli`` (path), ``codex_cli_version``,
``declared_model``, ``served_model`` (``null`` when no turn was served),
``error_class``, ``preflight_raw``.

Safety (the four mandatory defects, all prevented here):
  1. NOTHING is created until containment is PROVEN: the single canonical guard
     ``check_containment`` runs first and, if it fails, the process refuses with a
     typed code and creates no scratch/log/receipt inside the subject.
  2. The guard rejects the ancestor case in BOTH directions (subject inside target
     as well as target inside subject) and is the ONLY containment predicate used.
  3. Cleanup reports failures and never claims a deletion before it happened; a
     deletion failure is reflected in the receipt and in the exit status.
  4. (suite-level) the tests force every scratch/basetemp path outside the tree.

Read-only with respect to the subject: log/receipt/scratch live outside it.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Do not drop a __pycache__ next to the module we load from the tree under test.
sys.dont_write_bytecode = True


def _load_toolchain_module():
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "hgk_lane_toolchain", here / "hgk-lane-toolchain.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_toolchain = _load_toolchain_module()

# ---- typed codes -----------------------------------------------------------

LANE_OK = "LANE_OK"
LANE_TOOLCHAIN_MISMATCH = "LANE_TOOLCHAIN_MISMATCH"
LANE_MODEL_REFUSED = "LANE_MODEL_REFUSED"
LANE_INCONCLUSIVE = "LANE_INCONCLUSIVE"

# typed refusals of the preflight itself
ERR_SUBJECT_INSIDE_TARGET = "ERR_LANE_PREFLIGHT_SUBJECT_INSIDE_TARGET"
ERR_TARGET_INSIDE_SUBJECT = "ERR_LANE_PREFLIGHT_TARGET_INSIDE_SUBJECT"
ERR_TARGET_OUTSIDE_BASE = "ERR_LANE_PREFLIGHT_TARGET_OUTSIDE_BASE"
ERR_BASE_INSIDE_SUBJECT = "ERR_LANE_PREFLIGHT_BASE_INSIDE_SUBJECT"
ERR_OUTPUT_INSIDE_SUBJECT = "ERR_LANE_PREFLIGHT_OUTPUT_INSIDE_SUBJECT"
ERR_SEED_AUTH_MISSING = "ERR_LANE_PREFLIGHT_SEED_AUTH_MISSING"
ERR_UNEXPECTED = "ERR_LANE_PREFLIGHT_UNEXPECTED"

# exit codes
EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_CONTAINMENT = 96
EXIT_OUTPUT_INSIDE_SUBJECT = 97
EXIT_SEED_AUTH_MISSING = 95
EXIT_TOOLCHAIN_UNRESOLVED = 90
EXIT_CLEANUP_FAILED = 99


# ---- subject root ----------------------------------------------------------

def default_subject_root() -> Path:
    """The deliverable root: the parent of this script's own directory.

    The scripts live in ``<deliverable>/scripts/``; the deliverable root is the
    directory that contains them. This is location-derived, never the cwd.
    """
    return Path(__file__).resolve().parent.parent


# ---- ONE canonical containment guard (mandatory defect 2) ------------------

def _inside(child: Path, parent: Path) -> bool:
    """True when resolved ``child`` is ``parent`` or a descendant of it."""
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def check_containment(base, target, subject):
    """The ONE containment predicate used on every path.

    Deleting / writing ``target`` under ``base`` is permitted only when ALL hold
    (all on resolved absolute paths):

      * ``target`` is strictly inside ``base`` (``target != base``);
      * ``base`` is not inside ``subject``;
      * ``target`` is not inside ``subject``;
      * ``subject`` is not inside ``target``   <-- the ancestor case that the
        previous round's weaker guard missed: if the subject lives UNDER the
        target, deleting the target would delete the subject.

    Returns ``(ok: bool, code: str, detail: str)``. ``code`` is ``""`` when ok.
    """
    base = Path(base).resolve()
    target = Path(target).resolve()
    subject = Path(subject).resolve()

    # Subject-safety checks run FIRST so the most dangerous cases carry the most
    # specific typed code even when the target also happens to be outside base.
    if _inside(target, subject):
        return (
            False,
            ERR_TARGET_INSIDE_SUBJECT,
            f"target {target} is inside subject root {subject}",
        )
    if _inside(subject, target):
        return (
            False,
            ERR_SUBJECT_INSIDE_TARGET,
            f"subject root {subject} is inside target {target} "
            f"(deleting target would delete the subject)",
        )
    if _inside(base, subject):
        return (
            False,
            ERR_BASE_INSIDE_SUBJECT,
            f"base {base} is inside subject root {subject}",
        )
    if target == base or not _inside(target, base):
        return (
            False,
            ERR_TARGET_OUTSIDE_BASE,
            f"target {target} is not strictly inside base {base}",
        )
    return True, "", "containment proven"


def scratch_is_inside_subject(path, subject_root) -> bool:
    """Pure prefix test used by tests: is ``path`` inside ``subject_root``?"""
    return _inside(Path(path).resolve(), Path(subject_root).resolve())


def subject_root_is_safe_override(overridden, derived) -> bool:
    """An explicit --subject-root is only honored when it CONTAINS the derived
    root, so it can never narrow the containment window and hide a path that
    lives inside the deliverable."""
    return _inside(Path(derived).resolve(), Path(overridden).resolve())


# ---- classifier ------------------------------------------------------------

# Literal harness-symptom signatures (present => harness fault).
HARNESS_SYMPTOMS = (
    "failed to load models cache",   # models-cache schema error
    "model metadata for",            # "Model metadata for `X` not found."
    "unexpected argument",           # "error: unexpected argument '-' found"
    "unrecognized subcommand",
    "unknown subcommand",
    "unknown flag",
    "unrecognized flag",
)

_REFUSAL_STATUS_RE = re.compile(r'(?:status"?\s*[:=]\s*|HTTP\s+)(400|401|403)')
_ACCOUNT_LANGUAGE_RE = re.compile(
    r"not supported when using|account|entitlement|not available|no access|"
    r"missing bearer|unauthorized",
    re.IGNORECASE,
)
_HEADER_MODEL_RE = re.compile(r"^model:\s*(.+?)\s*$")
_HEADER_VERSION_RE = re.compile(r"^OpenAI Codex v(.+?)\s*$")
_BANNER_LINE_RE = re.compile(
    r"^(?:--------|workdir:|model:|provider:|approval:|sandbox:|"
    r"reasoning effort:|reasoning summaries:|session id:)"
)


def _startup_banner_lines(lines) -> list[str]:
    """The first CLI-owned startup banner block, or ``[]`` when absent.

    The block starts at the first ``OpenAI Codex v...`` line that appears before
    the interactive/body marker and stops at the first non-banner line. This is
    deliberately narrower than a log-wide search: a ``model:`` line written by
    the agent later in its own output must not be able to satisfy or break the
    served-vs-declared identity assertion.
    """
    stripped_lines = [line.rstrip("\r\n") for line in lines]
    start = None
    for idx, stripped in enumerate(stripped_lines):
        if stripped in ("user", "codex"):
            break
        if _HEADER_VERSION_RE.match(stripped):
            start = idx
            break
    if start is None:
        return []

    out = [stripped_lines[start]]
    for stripped in stripped_lines[start + 1:]:
        if stripped in ("user", "codex") or not stripped:
            break
        if _HEADER_VERSION_RE.match(stripped):
            break
        if _BANNER_LINE_RE.match(stripped):
            out.append(stripped)
            continue
        break
    return out


def extract_banner_model(lines) -> str | None:
    """Return the model id from the CLI startup banner only.

    Delegates to ``_headline_lines``, the existing anchored-header projection, so
    there is one notion of what the startup header is.
    """
    for line in _headline_lines(lines):
        m = _HEADER_MODEL_RE.match(line)
        if m:
            return m.group(1)
    return None


def served_from_header(lines) -> tuple[str | None, str | None]:
    """Read the served model + version from the CLI's OWN startup header."""
    model = extract_banner_model(lines)
    version = None
    for line in _headline_lines(lines):
        v = _HEADER_VERSION_RE.match(line)
        if v and version is None:
            version = v.group(1)
    return model, version


def classify(lines, exit_code: int, declared_model: str) -> str:
    """Map a captured run to one typed class. Pure function (unit-testable)."""
    joined = "\n".join(lines)
    lowered = joined.lower()

    # 1) Harness faults dominate: they manufacture provider-looking errors.
    for symptom in HARNESS_SYMPTOMS:
        if symptom in lowered:
            return LANE_TOOLCHAIN_MISMATCH

    # 2) Genuine provider refusal: HTTP 400/401/403 naming the declared model,
    #    with account/entitlement language, and NO toolchain symptom above.
    names_model = declared_model.lower() in lowered
    status = _REFUSAL_STATUS_RE.search(joined)
    if status and names_model and _ACCOUNT_LANGUAGE_RE.search(joined):
        return LANE_MODEL_REFUSED

    # 3) Success: clean exit AND the header named the declared model.
    served_model, _ = served_from_header(lines)
    if exit_code == 0 and served_model == declared_model:
        return LANE_OK

    return LANE_INCONCLUSIVE


def build_command(exe: str, workdir: str, model: str, effort: str) -> list[str]:
    """The one-line echo command. The model pin is on argv, not only in config."""
    return [
        exe,
        "exec",
        "--cd",
        workdir,
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "-",
    ]


# ---- receipt helpers -------------------------------------------------------

def _receipt_path_outside_subject(receipt_path, subject_root) -> bool:
    """The receipt may not be written inside the subject root."""
    return not scratch_is_inside_subject(receipt_path, subject_root)


def _write_receipt(receipt_path: Path, doc: dict, subject_root) -> bool:
    """Write the receipt ONLY when it resolves outside the subject root.

    Returns True when a file was written, False when suppressed to honour
    containment. ``mkdir`` happens here, so it happens only AFTER every
    containment decision above has passed.
    """
    if not _receipt_path_outside_subject(receipt_path, subject_root):
        print(
            f"{ERR_OUTPUT_INSIDE_SUBJECT}: receipt {receipt_path} is inside subject "
            f"root {subject_root}; receipt write suppressed.",
            file=sys.stderr,
        )
        return False
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return True


def _base_doc(args, subject_root, *, error_class=None, detail=None):
    return {
        "codex_cli": None,
        "codex_cli_version": None,
        "declared_model": args.model,
        "declared_effort": args.effort,
        "served_model": None,
        "served_provider": None,
        "error_class": error_class,
        "preflight_raw": "",
        "exit_code": None,
        "raw_log_path": str(args.log),
        "headline_lines": [],
        "substitution_permitted": False,
        "scratch_created": False,
        "attempts": 0,
        "subject_root": str(subject_root),
        "detail": detail,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=None, help="declared model to pin on argv")
    parser.add_argument("--effort", default="medium", help="declared reasoning effort")
    parser.add_argument("--scratch", default=None, help="dir for the throwaway CODEX_HOME")
    parser.add_argument("--log", default=None, help="raw preflight output path")
    parser.add_argument("--receipt", default=None, help="JSON receipt path")
    parser.add_argument("--timeout", type=int, default=120, help="hard timeout seconds (<=120)")
    parser.add_argument("--prompt", default="Reply with exactly OK", help="trivial prompt")
    parser.add_argument(
        "--subject-root",
        default=None,
        help="deliverable root; scratch/log/receipt MUST live outside it "
             "(default: this script's parent directory)",
    )
    parser.add_argument("--keep-scratch", action="store_true", help="keep the throwaway home")
    parser.add_argument(
        "--seed-auth",
        default=None,
        help="optional auth.json to seed the throwaway home from",
    )
    parser.add_argument(
        "--declaration",
        default=None,
        help="path to hermes-codex-lane.json (default: T1 default)",
    )
    parser.add_argument(
        "--check-containment",
        nargs=3,
        metavar=("BASE", "TARGET", "SUBJECT"),
        default=None,
        help="probe mode: print the typed containment verdict for BASE/TARGET/SUBJECT "
             "using the one canonical guard, then exit (creates nothing)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    # ---- containment probe mode (used by lane_launcher.sh) ----------------
    # Shares the ONE canonical guard; prints the typed code and exits non-zero
    # when containment is not proven. Nothing is created.
    if args.check_containment is not None:
        base, target, subject = args.check_containment
        ok_probe, code_probe, detail_probe = check_containment(base, target, subject)
        if ok_probe:
            print("containment proven")
            return 0
        print(f"{code_probe}: {detail_probe}", file=sys.stderr)
        return EXIT_CONTAINMENT

    if args.timeout > 120:
        print(
            f"ERR_LANE_PREFLIGHT_TIMEOUT_TOO_LARGE: {args.timeout} > 120",
            file=sys.stderr,
        )
        return EXIT_CONTAINMENT

    # Required in normal mode (relaxed above so the containment probe can run
    # standalone without a model/scratch/log).
    missing = [n for n, v in (("--model", args.model), ("--scratch", args.scratch),
                              ("--log", args.log)) if not v]
    if missing:
        print(
            "error: the following arguments are required in normal mode: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    log_path = Path(args.log)
    receipt_path = (
        Path(args.receipt) if args.receipt else log_path.with_name(log_path.name + ".receipt.json")
    )

    # ---- subject root: derived, with a fail-closed override ---------------
    derived_subject_root = default_subject_root()
    if args.subject_root:
        overridden = Path(args.subject_root)
        if not subject_root_is_safe_override(overridden, derived_subject_root):
            doc = _base_doc(
                args,
                derived_subject_root,
                error_class=ERR_TARGET_OUTSIDE_BASE,
                detail=(
                    f"--subject-root {overridden} does not contain the derived "
                    f"subject root {derived_subject_root}"
                ),
            )
            _write_receipt(receipt_path, doc, subject_root=derived_subject_root)
            print(
                f"ERR_LANE_PREFLIGHT_SUBJECT_ROOT_NOT_ANCESTOR: {overridden} does not "
                f"contain {derived_subject_root}; refused (0 attempts).",
                file=sys.stderr,
            )
            return EXIT_CONTAINMENT
        subject_root = overridden
    else:
        subject_root = derived_subject_root

    scratch = Path(args.scratch)

    # ---- 1. Containment FIRST, before ANY mutation ------------------------
    #    scratch lives under its own parent; both must be outside the subject
    #    and the subject must not live under the scratch (ancestor case).
    ok, code, detail = check_containment(scratch.parent, scratch, subject_root)
    if not ok:
        doc = _base_doc(args, subject_root, error_class=code, detail=detail)
        _write_receipt(receipt_path, doc, subject_root=subject_root)
        print(
            f"{code}: scratch {scratch} refused before any spawn "
            f"(containment not proven: {detail}); 0 attempts.",
            file=sys.stderr,
        )
        return EXIT_CONTAINMENT

    #    the log and receipt must live outside the subject too (defect 1).
    for out in (log_path, receipt_path):
        ok_o, code_o, detail_o = check_containment(out.parent, out, subject_root)
        if not ok_o:
            doc = _base_doc(args, subject_root, error_class=ERR_OUTPUT_INSIDE_SUBJECT,
                            detail=f"{out}: {detail_o}")
            _write_receipt(receipt_path, doc, subject_root=subject_root)
            print(
                f"{ERR_OUTPUT_INSIDE_SUBJECT}: output path {out} refused before any "
                f"write ({detail_o}); 0 attempts.",
                file=sys.stderr,
            )
            return EXIT_OUTPUT_INSIDE_SUBJECT

    codex_home = scratch / "binaryhome"

    # ---- cleanup bookkeeping (defect 3) -----------------------------------
    cleanup_outcome = {
        "credential_removed": None,
        "home_removed": False,
        "errors": [],
        "keep_scratch": bool(args.keep_scratch),
    }

    def cleanup() -> dict:
        auth = codex_home / "auth.json"
        if auth.exists():
            try:
                auth.unlink()
                cleanup_outcome["credential_removed"] = True
            except OSError as exc:
                cleanup_outcome["credential_removed"] = False
                cleanup_outcome["errors"].append(f"credential unlink failed: {exc}")
        if args.keep_scratch:
            return cleanup_outcome
        try:
            shutil.rmtree(codex_home)
            cleanup_outcome["home_removed"] = True
        except FileNotFoundError:
            cleanup_outcome["home_removed"] = True
        except OSError as exc:
            cleanup_outcome["home_removed"] = False
            cleanup_outcome["errors"].append(f"home rmtree failed: {exc}")
        return cleanup_outcome

    credential_temp_copy = False
    credential_cleanup_action = None
    result_doc: dict | None = None
    result_rc = EXIT_REFUSED

    def finalize(fn_doc: dict, rc: int) -> tuple[dict, int]:
        """Attach the cleanup outcome, then run cleanup and record the truth."""
        outer = dict(fn_doc)
        outer["credential_temp_copy"] = credential_temp_copy
        outer["credential_cleanup_action"] = credential_cleanup_action
        cleanup()
        outer["cleanup_outcome"] = dict(cleanup_outcome)
        outer["cleanup_reported"] = True
        if cleanup_outcome["errors"]:
            # A cleanup failure must change the return code and be reported.
            if rc == EXIT_OK:
                rc = EXIT_CLEANUP_FAILED
            outer["detail"] = (outer.get("detail") or "") + (
                " | cleanup errors: " + "; ".join(cleanup_outcome["errors"])
            )
        return outer, rc

    try:
        # ---- 2. Create the throwaway home (only now, containment proven) --
        codex_home.mkdir(parents=True, exist_ok=True)

        if args.seed_auth:
            src_auth = Path(args.seed_auth)
            if not src_auth.is_file():
                result_doc, result_rc = finalize(
                    {**_base_doc(args, subject_root, error_class=ERR_SEED_AUTH_MISSING,
                                 detail=f"seed auth not found: {src_auth}"),
                     "scratch_created": True},
                    EXIT_SEED_AUTH_MISSING,
                )
                print(f"{ERR_SEED_AUTH_MISSING}: {src_auth}", file=sys.stderr)
                return result_rc
            shutil.copyfile(src_auth, codex_home / "auth.json")
            credential_temp_copy = True
            credential_cleanup_action = "remove binaryhome (with copied auth.json) on exit"

            if os.environ.get("HGK_LANE_PREFLIGHT_FAULT_AFTER_SEED"):
                raise RuntimeError("injected fault after credential seeding")

        # ---- 3. Resolve + verify the toolchain via T1 ---------------------
        declaration = Path(args.declaration) if args.declaration else _toolchain.default_declaration_path()
        record, tcode = _toolchain.resolve(declaration)
        if tcode != 0:
            result_doc, result_rc = finalize(
                {**_base_doc(args, subject_root,
                             error_class=record.get("error") or LANE_INCONCLUSIVE,
                             detail=record.get("detail")),
                 "codex_cli": record.get("path"),
                 "codex_cli_version": record.get("version"),
                 "scratch_created": True},
                EXIT_TOOLCHAIN_UNRESOLVED,
            )
            print(f"{result_doc['error_class']}: {record.get('detail')}", file=sys.stderr)
            return result_rc

        exe = str(Path(record["path"]).resolve())
        workdir = str(scratch)
        cmd = build_command(exe, workdir, args.model, args.effort)

        env = dict(os.environ)
        env["CODEX_HOME"] = str(codex_home)
        for key in ("OPENAI_BASE_URL", "OPENAI_API_KEY", "OPENCODE_GO_API_KEY"):
            env.pop(key, None)

        timed_out = False
        raw_text = ""
        exit_code: int | None = None
        try:
            proc = subprocess.run(
                cmd,
                input=args.prompt + "\n",
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=args.timeout,
                env=env,
                cwd=workdir,
            )
            exit_code = proc.returncode
            raw_text = (proc.stdout or "") + (proc.stderr or "")
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            if isinstance(exc.stdout, bytes):
                raw_text = exc.stdout.decode("utf-8", errors="replace")
            elif isinstance(exc.stdout, str):
                raw_text = exc.stdout
            else:
                raw_text = ""
        except OSError as exc:
            raw_text = f"ERROR: {exc}"

        lines = raw_text.splitlines()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(raw_text, encoding="utf-8")

        if timed_out:
            error_class = LANE_INCONCLUSIVE
        else:
            error_class = classify(lines, exit_code if exit_code is not None else -1, args.model)

        served_model, served_version = served_from_header(lines)
        result_doc = {
            "codex_cli": exe,
            "codex_cli_version": record.get("version") or served_version,
            "declared_model": args.model,
            "declared_effort": args.effort,
            "served_model": served_model,
            "served_provider": None,
            "error_class": error_class,
            "preflight_raw": raw_text,
            "exit_code": exit_code,
            "raw_log_path": str(log_path),
            "headline_lines": _headline_lines(lines),
            "substitution_permitted": error_class == LANE_MODEL_REFUSED,
            "timeout_seconds": args.timeout,
            "scratch_created": True,
            "attempts": 1,
            "subject_root": str(Path(subject_root).resolve()),
            "codex_cli_sha256": record.get("sha256"),
            "detail": None,
        }
        rc = EXIT_OK if error_class == LANE_OK else EXIT_REFUSED
        result_doc, result_rc = finalize(result_doc, rc)
        return result_rc

    except BaseException as exc:  # noqa: BLE001 - record, cleanup, re-raise
        result_doc, result_rc = finalize(
            _base_doc(args, subject_root, error_class=ERR_UNEXPECTED,
                      detail=f"{type(exc).__name__}: {exc}"),
            EXIT_REFUSED,
        )
        raise
    finally:
        if result_doc is not None:
            _write_receipt(receipt_path, result_doc, subject_root=subject_root)
            print(
                f"error_class={result_doc.get('error_class')} "
                f"substitution_permitted={result_doc.get('substitution_permitted')}",
                file=sys.stderr,
            )
            if result_doc.get("error_class") == LANE_MODEL_REFUSED:
                print(
                    "genuine provider refusal on the declared model: a declared "
                    "model deviation may be recorded (owner decision).",
                    file=sys.stderr,
                )
            elif result_doc.get("error_class") == LANE_TOOLCHAIN_MISMATCH:
                print(
                    "HARNESS FAULT: toolchain mismatch, NOT a provider refusal. "
                    "Model substitution is REFUSED.",
                    file=sys.stderr,
                )


def _headline_lines(lines) -> list[str]:
    out = []
    for stripped in _startup_banner_lines(lines):
        if _HEADER_VERSION_RE.match(stripped):
            out.append(stripped)
        elif re.match(r"^(model|provider|reasoning effort):", stripped):
            out.append(stripped)
    for line in lines:
        stripped = line.rstrip("\r\n")
        if stripped.startswith("ERROR:") or stripped.startswith("error:"):
            out.append(stripped[:400])
    return out


if __name__ == "__main__":
    raise SystemExit(main())
