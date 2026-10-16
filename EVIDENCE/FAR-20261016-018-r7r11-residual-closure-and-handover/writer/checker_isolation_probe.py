#!/usr/bin/env python
"""
A1 - checker_isolation_probe.py

Reusable, FAIL-ABLE OS isolation harness for FAR-20261016-018 (EXECUTE lane).

What it proves (and what it does NOT):
    It creates a probe directory, confirms a baseline write SUCCEEDS, denies
    Write to the *current* identity with an inherited deny ACE
    (`icacls <dir> /deny <identity>:(OI)(CI)(W)`), confirms the write is DENIED,
    removes the ACE, confirms the write SUCCEEDS again, then removes the dir.
    The receipt carries an explicit `limit`: the denying identity can lift its
    own ACE, so this is ORDINARY DENIAL, not an immutable boundary.

Safety: everything happens under `--root`. The default root is a fresh temp dir
the script itself creates. It never touches anything outside that root, it
aborts if a caller-supplied root already holds foreign content, and it always
removes the deny ACE and the probe dir in a `finally` block, verifying removal.

Modes:
    (default)        run the full probe and emit ONE JSON receipt to stdout.
    --self-test      run the probe with the deny step SKIPPED (mutation) and
                     assert the harness REPORTS FAILURE; prints `SELF_TEST=PASS`
                     only when that mutation is detected.

Exit codes: 0 = verdict PASS (default) / mutation detected (--self-test);
            1 = verdict FAIL / mutation NOT detected; 2 = usage/IO error.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

SCHEMA = "FAR018/CHECKER-ISOLATION-PROBE/1"
PY = sys.executable


def current_identity():
    """The identity icacls is asked to deny. Measured form: `desktop-57eo414\\user`."""
    dom = os.environ.get("USERDOMAIN", "")
    usr = os.environ.get("USERNAME", "")
    return (dom + "\\" + usr).lower()


def run(argv, timeout=120):
    """Run a command and capture returncode + RAW stdout/stderr."""
    try:
        p = subprocess.run(
            argv, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout,
        )
        return {
            "argv": list(argv),
            "returncode": p.returncode,
            "stdout": p.stdout,
            "stderr": p.stderr,
        }
    except Exception as exc:  # noqa: BLE001 - recorded, never raised
        return {
            "argv": list(argv),
            "returncode": None,
            "stdout": "",
            "stderr": "harness-exec-error: {0}: {1}".format(type(exc).__name__, exc),
        }


def pycode(code):
    return [PY, "-B", "-c", code]


def _denied(step):
    """True when a write step failed for a permission-shaped reason."""
    if step.get("returncode") in (0, None):
        return False
    blob = (step.get("stderr") or "") + (step.get("stdout") or "")
    markers = ("PermissionError", "[Errno 13]", "Access is denied", "denied")
    return any(m in blob for m in markers)


def run_probe(root, identity, skip_deny=False):
    """Execute the probe. Returns the receipt dict. Never raises on step failure."""
    base_file = os.path.join(root, "baseline_write.txt")
    deny_file = os.path.join(root, "denied_write.txt")
    restore_file = os.path.join(root, "restored_write.txt")
    steps = {}
    cleanup = {}

    write_code = lambda path: pycode(
        "import io,sys\n"
        "with io.open({0!r}, 'w', encoding='utf-8') as fh:\n"
        "    fh.write('probe-write-ok')\n"
        "sys.stdout.write('write-ok\\n')".format(path)
    )

    try:
        steps["create_dir"] = run(pycode(
            "import os, sys\n"
            "os.makedirs({0!r}, exist_ok=True)\n"
            "sys.stdout.write('created\\n')".format(root)))

        steps["baseline_write"] = run(write_code(base_file))
        baseline_ok = steps["baseline_write"]["returncode"] == 0

        if not skip_deny:
            steps["apply_deny_ace"] = run(
                ["icacls", root, "/deny", "{0}:(OI)(CI)(W)".format(identity)])

        steps["denied_write"] = run(write_code(deny_file))
        denied_ok = _denied(steps["denied_write"])

        if not skip_deny:
            steps["remove_deny_ace"] = run(
                ["icacls", root, "/remove:d", identity])

        steps["restored_write"] = run(write_code(restore_file))
        restored_ok = steps["restored_write"]["returncode"] == 0

        booleans = {
            "baseline_write_succeeded": bool(baseline_ok),
            "denied_write_failed": bool(denied_ok),
            "restored_write_succeeded": bool(restored_ok),
        }
    finally:
        # ALWAYS lift the ACE (idempotent) and remove the dir, then verify.
        if not skip_deny:
            cleanup["remove_deny_ace_final"] = run(
                ["icacls", root, "/remove:d", identity])
        cleanup["acl_readback"] = run(["icacls", root])
        acl_txt = ((cleanup["acl_readback"].get("stdout") or "")
                   + (cleanup["acl_readback"].get("stderr") or "")).lower()
        cleanup["deny_ace_removed"] = (identity.lower() not in acl_txt) or not os.path.exists(root)
        cleanup["remove_dir"] = run(pycode(
            "import shutil, sys\n"
            "shutil.rmtree({0!r}, ignore_errors=True)\n"
            "sys.stdout.write('removed\\n')".format(root)))
        cleanup["probe_dir_removed"] = not os.path.exists(root)

    cleanup_verified = bool(cleanup.get("deny_ace_removed")) and bool(
        cleanup.get("probe_dir_removed"))
    verdict_pass = (
        booleans["baseline_write_succeeded"]
        and booleans["denied_write_failed"]
        and booleans["restored_write_succeeded"]
        and cleanup_verified
    )

    receipt = {
        "schema": SCHEMA,
        "identity": identity,
        "identity_source": "USERDOMAIN\\USERNAME (lowercased); owner SID "
                           "S-1-5-21-2687334950-3868438633-1592137926-1000",
        "probe_path": root,
        "deny_step_skipped_mutation": bool(skip_deny),
        "steps": steps,
        "booleans": booleans,
        "cleanup": cleanup,
        "cleanup_verified": cleanup_verified,
        "limit": (
            "ORDINARY DENIAL, NOT AN IMMUTABLE BOUNDARY: the same identity that "
            "applies the deny ACE (`{0}`) can lift it again with "
            "`icacls <dir> /remove:d {0}`, which this harness itself does. The "
            "barrier is an owner-settable ACL, not an OS-enforced impossibility; "
            "a principal able to author the ACE can also remove it.".format(identity)
        ),
        "verdict": "PASS" if verdict_pass else "FAIL",
    }
    return receipt


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Fail-able OS write-denial isolation harness (FAR-20261016-018 A1).")
    ap.add_argument("--root", default=None,
                    help="probe directory; default is a fresh temp dir the script creates")
    ap.add_argument("--identity", default=None,
                    help="identity to deny (default: USERDOMAIN\\USERNAME lowercased)")
    ap.add_argument("--self-test", action="store_true",
                    help="run the deny-skip mutation and assert the harness reports FAILURE")
    args = ap.parse_args(argv)

    identity = (args.identity or current_identity())

    if args.root is None:
        root = tempfile.mkdtemp(prefix="far018_probe_")
    else:
        root = os.path.abspath(args.root)
        if os.path.isdir(root) and os.listdir(root):
            sys.stderr.write("refusing: --root exists and is non-empty (safety)\n")
            return 2
        os.makedirs(root, exist_ok=True)

    if args.self_test:
        # Mutation: skip the deny step. A correct harness must notice the write
        # that should have been denied instead SUCCEEDED and report FAILURE.
        mutated = run_probe(root, identity, skip_deny=True)
        detected = (
            mutated["verdict"] == "FAIL"
            and mutated["booleans"]["denied_write_failed"] is False
        )
        sys.stdout.write(json.dumps(mutated, indent=2, ensure_ascii=False) + "\n")
        if detected:
            sys.stdout.write("SELF_TEST=PASS\n")
            return 0
        sys.stdout.write("SELF_TEST=FAIL\n")
        return 1

    receipt = run_probe(root, identity, skip_deny=False)
    sys.stdout.write(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
