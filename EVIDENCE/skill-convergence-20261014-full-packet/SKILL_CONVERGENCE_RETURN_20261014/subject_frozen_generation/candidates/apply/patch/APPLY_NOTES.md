# Candidate patch: lane-dispatch timeout capture loss

This is a **candidate patch**. It has **NOT** been applied to the canonical control plane
(`C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py`) and it grants **no
landing authority**. Editing the control plane's lane mechanism is a canonical change and
must go through that plane's own admission and landing (Shared Spine event + evidence +
rollback reference + an independent checker result). A patch that applies cleanly is not a
fix; only a landed, re-verified dispatcher is.

## The defect

In `run_candidate`, the branch that handles a lane timeout lets the captured output go
nowhere:

```python
    except subprocess.TimeoutExpired:
        rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""
```

`subprocess.run(..., capture_output=True, timeout=...)` raises `subprocess.TimeoutExpired`
and stores whatever the child had already written to stdout/stderr on the exception
(`exc.stdout` / `exc.stderr`). The canonical branch ignores `exc` and forces the streams to
`b""` / `""`, so every timed-out attempt is persisted with **0 bytes and an empty tail** and
the child's diagnostics are lost. In this round eleven lanes died that way and their
diagnostics were unrecoverable, so the failure class stayed opaque until it was counted by
class.

The branch under test is the canonical file's lines **1143-1144** (1-based, CRLF file),
reported as `timeout_branch_line_range` in `remediation_result.json`.

## The minimal change

Bind the exception and preserve the bytes already read, plus an explicit `timed_out` marker
on the attempt record. Two edits, no restructuring:

* `except subprocess.TimeoutExpired:` becomes `except subprocess.TimeoutExpired as exc:`. The
  branch keeps `rc = "TIMEOUT"` and instead of discarding, sets
  `out_b`/`err_b` from `exc.stdout`/`exc.stderr` (byte-exact when they are bytes, otherwise a
  lossless-by-replacement UTF-8 encode) and re-derives `out`/`err` from them.
* `timed_out = False` is initialised before the `try`, set to `True` in the timeout branch,
  and added to the attempt dict as `"timed_out": timed_out`.

## Why the change is safe

The change only affects what is **recorded**; it does not touch control flow. On a timeout the
child has already been killed, so there is no live stream to keep consistent. A non-timeout
run leaves `timed_out = False` and the existing variable assignments untouched. The preserved
bytes flow through exactly the same downstream code that already consumes
`out_b`/`err_b`/`out`/`err` (the nonce verdict, the carrier extraction, `persist_attempt_logs`,
and the tails), so no new parsing surface is introduced. The reproduction
(`patch/repro_timeout_capture.py`) drives the real `run_candidate` path and shows the change is
confined to the timeout case: the canonical path preserves 0 bytes, the proposed path
preserves the 161 bytes the child had flushed, while every classification field stays
identical.

## What it explicitly does NOT change

* The **non-zero exit status**: a timeout still records `exit = "TIMEOUT"`.
* The **absence of a nonce**: `nonce_present` stays `false` (the preserved bytes generally do
  not carry the nonce; the verdict is computed downstream and is not forced by this patch).
* `ok = false`: the receipt's `ok` is decided by whether an attempt served the turn, which a
  timeout never does.
* `usage_receipt_ok = false`: no fresh usage row is bound to a timed-out attempt.

A timeout must stay a timeout; this patch only stops it from being silent.

## How to revert

The change is a candidate file, not a landing. Reverting is deleting the candidate; nothing
in the canonical tree was touched. If the patch is ever landed and must be undone, revert the
single commit that applies `patch/lane-dispatch-timeout-capture.patch`: restore
`except subprocess.TimeoutExpired:` with the body
`rc, out, err, out_b, err_b = "TIMEOUT", "", "", b"", b""`, drop the `timed_out = False`
initialiser, the `timed_out = True` line, and the `"timed_out": timed_out` attempt field.
Because the edit is additive and local to one branch and one dict, the rollback is exact.

## Files in this candidate

* `patch/hgk-lane-dispatch.py` -- byte-for-byte copy of the canonical script (sha256
  `17e667d136f1463609a44e2de6a8f7ba9aab07653f6ea4490178fc4ff93a6c56`, 128634 bytes).
* `patch/lane-dispatch-timeout-capture.patch` -- the unified diff against the canonical path.
* `patch/repro_timeout_capture.py` -- the deterministic reproduction.
