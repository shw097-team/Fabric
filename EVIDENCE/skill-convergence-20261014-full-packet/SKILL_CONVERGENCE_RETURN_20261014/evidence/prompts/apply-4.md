# Bounded EXECUTE lane — candidate patch for the lane-dispatch timeout capture loss

Your writable directory is this lane's cwd (`candidates/apply`). You may READ outside it; you must not modify
anything outside it.

The defect, already reproduced by the round harness and by reading the source: in
`C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py` the branch that handles a lane timeout lets
`subprocess.TimeoutExpired` escape, so whatever the child had already written to stdout/stderr is discarded and
the attempt record is written with 0 bytes and an empty tail. Eleven lanes of this round died that way and their
diagnostics were lost, so the failure class stayed opaque until it was counted by class.

TASK, in this order, and nothing else:
1. READ the canonical script; record its sha256, its byte size, and the exact line range of the timeout branch.
2. Make a COPY of the canonical script inside your cwd (`patch/hgk-lane-dispatch.py`). Never edit the canonical file.
3. Write `patch/repro_timeout_capture.py`: it must (a) build a tiny child command that prints a few lines and then
   sleeps longer than the timeout, (b) run it twice through the copied dispatcher's timeout path — once as the
   canonical code behaves, once with the proposed behaviour — and (c) print the number of stdout/stderr bytes each
   run preserved. Honour the child's timeout with a short value so the reproduction stays quick. Use the interpreter
   `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.
4. Produce `patch/lane-dispatch-timeout-capture.patch`: a unified diff against the canonical path that, on timeout,
   captures the bytes already read from the child and writes them into the attempt record together with an explicit
   timed_out marker. The patch must NOT change: the non-zero exit status, the absence of a nonce, `ok=false`, or
   `usage_receipt_ok=false`. A timeout must stay a timeout; it just stops being silent.
5. Write `patch/APPLY_NOTES.md`: the defect, the minimal change, why the change is safe, what it explicitly does not
   change, how to revert, and the statement that this is a candidate patch that has NOT been applied to the
   canonical control plane and must go through that plane's own admission and landing.
6. Verify the canonical file is untouched: recompute its sha256 and compare with step 1.

OUTPUT: `remediation_result.json` in the cwd with: schema, lane, observed_at, canonical {path, sha256_before,
sha256_after, bytes, timeout_branch_line_range}, reproduction {before_bytes_preserved, after_bytes_preserved,
command}, patch {path, bytes, sha256}, notes_path, canonical_untouched (bool), exact_commands[], coverage,
claim_ceiling. The claim ceiling must say this is a candidate patch plus a reproduction, that it grants no landing
authority, and that editing the control plane's lane mechanism is a canonical change requiring its own admission.

Facts you must not overstate: a patch that applies cleanly is not a fix; only a landed, re-verified dispatcher is.

Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`. Write scripts to files and run
them by path; do not build long inline PowerShell commands.

Final literal transport token (not an acceptance): SKCV_APPLY_4_OK
