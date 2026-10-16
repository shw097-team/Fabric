# WS-C WRITER BRIEF — checker write-root isolation: evidence of absence + a proven mechanism

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`. Authority: EIA-R6-03 (`EVIDENCE_GAP` / HIGH,
owner "HGK Checker Harness Owner"). Claim ceiling: **LOCAL / candidate-only**.

## The finding you are answering
The external acceptance report found that in R6 the checker lane **actually wrote** into the guarded
subject's neighbourhood (`WRITER_ROOT`), which both voids independence (SoD) and is a real side effect
on a frozen artifact. R7 responded by relocating the verifier's write root outside the subject — a
**procedural** control. No OS-enforced control exists. Never claim one does.

## Deliverable
Produce the honest, reproducible evidence pack that says exactly what is and is not enforced today,
plus a proven mechanism the owner could adopt. **You must not change any ACL on any real path.**

## Inputs
- Guarded subject (read-only for you): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`
- Local digest reference: `…/CNV-PIPD-LS-SP-20261015-R8/WS_D/GUARDED_SUBJECT_BYTE_EXACTNESS.json`
  (300 files, 1,102,562 bytes, digest `3588d5d51a4941cf1c9425beee9dcf3f4162fe23bcdd276bc1dd3939af86f16c`,
  computed as sha256 over sorted `relpath:sha256` lines) — there is **no outbound network** in this lane,
  so compare against this recorded value, not against GitHub.
- Your work root: `…/CNV-PIPD-LS-SP-20261015-R8/WS_C/`

## Steps
1. **Effective ACL of the guarded subject** (read-only):
   `icacls "C:\Projects\Agent_Workspace\_handover\CNV-PIPD-LS-SP-20261015\R6_DELIVERY"` — capture the raw
   output verbatim. Also capture `whoami` and `icacls` for the parent `_handover` directory. State plainly
   whether any `(DENY)` ACE restricts writes for the current identity.
2. **Absence evidence (positive control).** In `WS_C/acl_probe/` (a scratch directory **you** create,
   outside the guarded subject), create `probe_before.txt` and write bytes into it. Record the command,
   exit code and result. This demonstrates what the current ACE set permits — nothing more.
3. **Mechanism proof.** In the same scratch directory:
   a. `icacls "WS_C\acl_probe" /deny "%USERNAME%":(W)` and record the raw output.
   b. Attempt to create `probe_denied.txt` and write bytes — expect failure. Capture stdout/stderr and the
      exact exit code; if the write **succeeds**, that is the finding (the mechanism does not work as
      expected here) — record it and stop step 3.
   c. `icacls "WS_C\acl_probe" /remove:d "%USERNAME%"` and record the raw output.
   d. Attempt the write again — expect success. Record it.
   e. Delete the scratch directory and verify it is gone.
4. **Proposed change for the owner (do not execute).** Write the exact command that would apply the same
   deny ACE to the guarded subject, its exact rollback command, the blast radius (which identities would
   lose write access), and the reason it is *not* applied in this round.
5. **Guarded-subject re-measurement.** Recompute the 300-file digest with the documented method and
   compare to the recorded value. Record `files`, `bytes`, `digest`, `match: true|false`.
6. Write `WS_C/CHECKER_WRITE_ROOT_ISOLATION_EVIDENCE.json` (all raw outputs as strings) and
   `WS_C/WS_C_RECEIPT.md`. Print the JSON at the end.

## Hard constraints (a violation voids your turn)
- Write only under `WS_C/`. The `icacls` calls in steps 2–3 may only target `WS_C/acl_probe`.
  **Never** run `icacls` with a mutating verb (`/grant`, `/deny`, `/remove:d`, `/reset`, `/setowner`)
  against any path outside `WS_C/acl_probe`.
- Never write, delete or rename anything under the guarded subject or anywhere in `_handover/` outside `WS_C/`.
- No outbound network access; no git commands that modify state; no credential reads.
- Do not claim the isolation exists, and do not claim it is fixed. Report exactly what you observed.
- If a step cannot be run on this host, say so with the raw error. An honest "not enforceable here" is a
  valid and valuable outcome.
