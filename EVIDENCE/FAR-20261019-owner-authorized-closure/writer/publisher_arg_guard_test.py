#!/usr/bin/env python
"""T3 self-test: publisher argument safety (FAR018-BROKER-ARGUMENT-SAFETY).

The archived `publish_broker.py` parsed no arguments, so a `--help` probe took the
publishing main path and actually published. The candidate adds `parse_args()`
before any credential read or API call.

This test NEVER touches the network. It loads the CANDIDATE module, replaces the
transport `_req` with a stub that records the call and raises immediately, and
asserts:

  A  canonical module has no argument parser AND a `--help`-shaped run reaches
     the transport (the defect). If the canonical file already refused, the test
     FAILS: it cannot certify a guard that already exists.
  B  candidate `--help` exits via SystemExit with code 0 and makes ZERO transport
     calls.
  C  candidate unknown flag `--bogus` exits via SystemExit non-zero and makes
     ZERO transport calls.
  D  candidate `--dry-run` returns 0 after the manifest/prefix check and makes
     ZERO transport calls.
  E  the DOCUMENTED invocation (no arguments) still ENGAGES the transport path,
     proving the guard did not silently disable publishing.

Every result is read from the real modules on this run; nothing expected is
hardcoded. Exit 0 only when A-E all hold; 3 otherwise.
"""

import argparse
import importlib.util
import io
import contextlib
import json
import sys
from pathlib import Path

CANONICAL = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/publish_broker.py")
CANDIDATE = Path(__file__).resolve().parent / "publish_broker.candidate.py"


class NetworkCalled(Exception):
    """Raised by the transport stub; if it is never raised, no network path ran."""


def load(path, alias):
    spec = importlib.util.spec_from_file_location(alias, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


def install_stub(mod):
    calls = []

    def stub(method, path, body=None, raw=False):
        calls.append((method, path))
        raise NetworkCalled("transport stubbed: no network is permitted in this test")

    mod._req = stub
    return calls


def run_capture(mod, argv, dry_run=False):
    """Run the candidate entry point; return (system_exit_code, transport_calls)."""
    calls = install_stub(mod)
    code = None
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            mod.parse_args(argv)
    except SystemExit as e:  # argparse: --help (0) or unknown flag (2)
        code = e.code
        return code, calls
    # arguments parsed cleanly -> drive main() as __main__ would.
    mod.main._dry_run = dry_run
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            rc = mod.main()
    except NetworkCalled:
        rc = "NetworkCalled"
    return rc, calls


def phase_a_canonical_defect():
    mod = load(CANONICAL, "canonical_broker")
    has_parser = hasattr(mod, "parse_args")
    calls = install_stub(mod)
    # emulate the archived `--help` probe: run main() exactly as __main__ did.
    try:
        mod.main()
        rc = 0
    except NetworkCalled:
        rc = "NetworkCalled"
    except SystemExit as e:
        rc = e.code
    reached_transport = len(calls) > 0
    defect_reproduced = (not has_parser) and reached_transport
    return {
        "phase": "A_canonical_defect",
        "source_contains_argparse": has_parser,
        "transport_calls": len(calls),
        "help_probe_reached_transport": reached_transport,
        "rc": rc,
        "defect_reproduced": defect_reproduced,
        "verdict": "PASS" if defect_reproduced else "FAIL",
    }


def phase_b_help():
    mod = load(CANDIDATE, "candidate_broker_b")
    code, calls = run_capture(mod, ["--help"])
    ok = code == 0 and len(calls) == 0
    return {"phase": "B_candidate_help", "system_exit_code": code,
            "transport_calls": len(calls), "verdict": "PASS" if ok else "FAIL"}


def phase_c_unknown_flag():
    mod = load(CANDIDATE, "candidate_broker_c")
    code, calls = run_capture(mod, ["--bogus"])
    ok = code not in (0, None) and len(calls) == 0
    return {"phase": "C_candidate_unknown_flag", "system_exit_code": code,
            "transport_calls": len(calls), "verdict": "PASS" if ok else "FAIL"}


def phase_d_dry_run():
    mod = load(CANDIDATE, "candidate_broker_d")
    rc, calls = run_capture(mod, ["--dry-run"], dry_run=True)
    ok = rc == 0 and len(calls) == 0
    return {"phase": "D_candidate_dry_run", "rc": rc,
            "transport_calls": len(calls), "verdict": "PASS" if ok else "FAIL"}


def phase_e_documented_invocation():
    mod = load(CANDIDATE, "candidate_broker_e")
    rc, calls = run_capture(mod, [])
    engaged = len(calls) > 0
    return {"phase": "E_documented_no_arg_invocation", "rc": rc,
            "transport_calls": len(calls), "transport_engaged": engaged,
            "verdict": "PASS" if engaged else "FAIL"}


def main(argv=None):
    argparse.ArgumentParser(description="T3 publisher argument-safety self-test.").parse_args(argv)
    results = [phase_a_canonical_defect(), phase_b_help(), phase_c_unknown_flag(),
               phase_d_dry_run(), phase_e_documented_invocation()]
    failed = [r["phase"] for r in results if r["verdict"] != "PASS"]
    for r in results:
        print(json.dumps(r, indent=2))
    print("T3_RESULT=" + ("PASS" if not failed else "FAIL:" + ",".join(failed)))
    return 0 if not failed else 3


if __name__ == "__main__":
    raise SystemExit(main())
