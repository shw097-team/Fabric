"""Deterministic reproduction of the lane-dispatch timeout capture loss.

The canonical dispatcher's timeout branch, inside ``run_candidate``, forces the
captured streams to empty bytes::

    except subprocess.TimeoutExpired:
        rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""

Whatever the child had already written to stdout/stderr before the kill is discarded,
so the attempt record is written with 0 bytes and an empty tail.

This repro drives the ACTUAL ``run_candidate`` timeout path -- not a hand-simulation --
against a tiny child that prints a few lines and then sleeps far longer than a short
timeout, twice:

  * ``canonical`` -- ``patch/hgk-lane-dispatch.py`` (the byte-for-byte copy of the
    canonical control-plane script), loaded as a module and run.
  * ``proposed``  -- the SAME module with the candidate patch applied in memory, so the
    two runs differ only by the timeout branch under test.

It prints how many stdout/stderr bytes each path preserved. The short timeout keeps the
reproduction quick. The interpreter is the one named in the brief when present; this
lane exposes it only through a denied path, so the running interpreter is used and the
choice is recorded rather than hidden.
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BRIEFED_PY = r"C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
HERE = Path(__file__).resolve().parent
COPIED = HERE / "hgk-lane-dispatch.py"
CANONICAL = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py")
PATCHED_VARIANT = HERE / "hgk-lane-dispatch.timeout-capture.py"

# Short enough to stay quick, long enough that the flushed lines land before the kill.
TIMEOUT = 2.0
SLEEP = 30


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def resolve_interpreter():
    """The brief names ``BRIEFED_PY``. On this lane that path exists but is DENIED to
    this process, so fall back to the running interpreter and report which was used."""
    try:
        if Path(BRIEFED_PY).is_file():
            return BRIEFED_PY, "briefed"
        reason = "absent"
    except OSError as exc:
        reason = "unreadable ({})".format(type(exc).__name__)
    return sys.executable, "fallback: briefed interpreter {}, using sys.executable".format(reason)


def child_source():
    lines = ["import sys, time"]
    for i in range(4):
        lines.append("print('stdout line %d payload' % {0}, flush=True)".format(i))
    for i in range(3):
        lines.append("print('stderr line %d payload' % {0}, file=sys.stderr, flush=True)".format(i))
    lines.append("time.sleep({0})".format(SLEEP))
    return "\n".join(lines) + "\n"


def canonical_branch_line_range(path):
    """(start, end) 1-based byte-line range of the canonical timeout branch, or None."""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read().split("\n")
    start = None
    for idx, line in enumerate(text):
        if line.strip().startswith("except subprocess.TimeoutExpired"):
            start = idx + 1
            break
    if start is None:
        return None
    end = start
    for idx in range(start, len(text)):
        if text[idx].strip() == 'rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""':
            end = idx + 1
            break
    return [start, end]


def load_module(path, name):
    # The copied script computes ROOT from its OWN location (patch/), so its relative
    # `ROOT/src` and `ROOT/scripts/gcm-containment` inserts point at the wrong tree. Put the
    # canonical repo's real roots on sys.path first so `hg_kseos` and the GCM helpers import.
    repo = CANONICAL.parent.parent
    for extra in (repo / "src", repo / "scripts" / "gcm-containment"):
        if str(extra) not in sys.path:
            sys.path.insert(0, str(extra))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def apply_candidate_patch(source_text):
    """Apply exactly the two candidate edits (the timeout branch + the timed_out marker)
    to the copied source in memory, so the 'proposed' run differs only by that change."""
    nl = "\r\n" if "\r\n" in source_text else "\n"

    def to_nl(t):
        return t.replace("\n", nl)

    old_branch = to_nl(
        "    except subprocess.TimeoutExpired:\n"
        '        rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""\n')
    new_branch = to_nl(
        "    except subprocess.TimeoutExpired as exc:\n"
        "        timed_out = True\n"
        '        rc = "TIMEOUT"\n'
        '        out_b = exc.stdout if isinstance(exc.stdout, bytes) else (exc.stdout or "").encode("utf-8", errors="replace")\n'
        '        err_b = exc.stderr if isinstance(exc.stderr, bytes) else (exc.stderr or "").encode("utf-8", errors="replace")\n'
        '        out = out_b.decode("utf-8", errors="replace")\n'
        '        err = err_b.decode("utf-8", errors="replace")\n')
    old_try = to_nl("    t0 = time.time()\n    try:\n")
    new_try = to_nl("    t0 = time.time()\n    timed_out = False\n    try:\n")
    old_exit = to_nl('            "reasoning_effort": entry.get("reasoning_effort"), "exit": rc,\n')
    new_exit = to_nl('            "reasoning_effort": entry.get("reasoning_effort"), "exit": rc,\n'
                     '            "timed_out": timed_out,\n')
    out = source_text
    for old, new in ((old_try, new_try), (old_branch, new_branch), (old_exit, new_exit)):
        assert out.count(old) == 1, ("anchor missing/not unique", out.count(old))
        out = out.replace(old, new)
    return out


def run_timeout_path(module, py, child, workdir):
    """Run the module's REAL ``run_candidate`` against the tiny child and return the
    attempt record (plus the persisted log sizes).

    ``run_candidate`` treats its ``codex`` argument as the child executable and builds the
    argv from it; a value ending in ``.py`` is launched under ``sys.executable``. So the
    tiny child script IS that executable, and the dispatcher's own argv tokens are ignored
    by the child (it just prints and sleeps).
    """
    entry = {"rank": 7, "provider": "stub", "model": "stub-model", "transport_model": "stub-model",
             "reasoning_effort": None}
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    class Args:
        lane = "EXECUTE"
        sandbox = "read-only"
        cwd = str(workdir)
        relay_base = "http://127.0.0.1:10101/v1"
        nonce = "HGK_LANE_NONCE_OK"
        prompt = "repro"
        usage = str(Path(workdir) / "usage.jsonl")
        timeout = TIMEOUT
        codex_arg = None
        codex_home_config = {}
        credential_posture_gate = str(Path(workdir) / "no_such_gate.py")  # -> INCONCLUSIVE/WARN_CONTINUE
        credential_posture_gate_git = None
        credential_posture_gate_test_global = None

    Path(Args.usage).parent.mkdir(parents=True, exist_ok=True)
    Path(Args.usage).write_text("", encoding="utf-8")
    log_dir = Path(workdir) / "attempt-logs"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        attempt = module.run_candidate(entry, Args(), str(child), Path(workdir),
                                       attempt_log_dir=log_dir, run_id="repro")
    return attempt, log_dir


def main():
    py, py_source = resolve_interpreter()
    branch = canonical_branch_line_range(COPIED)
    copied_bytes = COPIED.read_bytes()
    copied_text = copied_bytes.decode("utf-8")
    canonical_branch_present = 'rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""' in copied_text

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        child = work / "child_print_then_sleep.py"
        child.write_text(child_source(), encoding="utf-8")

        canonical_mod = load_module(COPIED, "hgk_lane_dispatch_canonical")
        before_attempt, before_dir = run_timeout_path(canonical_mod, py, child, work / "canonical")

        patched_src = apply_candidate_patch(copied_text)
        patched_path = work / "hgk-lane-dispatch.patched.py"
        # newline="" keeps the CRLF that apply_candidate_patch produced; the default would
        # translate every \n again and yield \r\r\n (a stray blank line / SyntaxError).
        with open(patched_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(patched_src)
        proposed_mod = load_module(patched_path, "hgk_lane_dispatch_proposed")
        after_attempt, after_dir = run_timeout_path(proposed_mod, py, child, work / "proposed")

    def summarize(attempt, log_dir):
        so = attempt.get("stdout_bytes") or 0
        se = attempt.get("stderr_bytes") or 0
        return {
            "exit": attempt.get("exit"),
            "timed_out": attempt.get("timed_out", "<absent>"),
            "nonce_present": attempt.get("nonce_present"),
            "usage_receipt_ok": attempt.get("usage_receipt_ok"),
            "stdout_bytes": so,
            "stderr_bytes": se,
            "total_bytes": so + se,
            "stdout_tail": attempt.get("stdout_tail", ""),
            "stderr_tail": attempt.get("stderr_tail", ""),
            "log_dir": str(log_dir),
        }

    before = summarize(before_attempt, before_dir)
    after = summarize(after_attempt, after_dir)
    summary = {
        "schema": "hgk-lane-timeout-capture-repro/1",
        "interpreter": py,
        "interpreter_source": py_source,
        "copied_dispatcher": str(COPIED),
        "copied_dispatcher_sha256": sha256_bytes(copied_bytes),
        "canonical_dispatcher": str(CANONICAL),
        "canonical_dispatcher_sha256": sha256_file(CANONICAL),
        "timeout_branch_line_range": branch,
        "canonical_branch_present_in_copy": canonical_branch_present,
        "timeout_seconds": TIMEOUT,
        "child_sleep_seconds": SLEEP,
        "before_bytes_preserved": before["total_bytes"],
        "after_bytes_preserved": after["total_bytes"],
        "command": "{} {} (child: {} + print/sleep)".format(py, COPIED.name, child.name),
        "runs": [dict(policy="canonical", **before), dict(policy="proposed", **after)],
        "verdict": ("REPRODUCED: the canonical timeout branch preserved {} bytes; the proposed "
                    "branch preserved {} bytes").format(before["total_bytes"], after["total_bytes"]),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
