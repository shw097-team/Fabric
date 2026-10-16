# EXECUTE brief — FAR-20261019 bounded writer batch

Round: `FAR-20261019-owner-authorized-closure`. Lane: EXECUTE (`opencode-go/deepseek-v4.1-flash`).
Nonce: `CNVEA-FAR019-EXECUTE-NONCE-7b2e94`
Echo the nonce line verbatim in your final receipt, on its own line, prefixed `NONCE-ECHO:` — the lane
receipt is only accepted when the arm itself emits the nonce.

## Standing rules

- You are a **bounded writer**. Write ONLY inside the round directory
  `C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure/writer/`.
- Do **not** edit anything under `HG-KSEOS/`, `Fabric/`, or the previous round's directory. Where a fix
  belongs in canonical tooling, deliver a **candidate copy plus a unified diff**, never an in-place edit.
- Every deliverable must have a **self test you can run**, and the self test must be able to FAIL
  (invariant 11). A test that cannot fail is worse than no test: report `VACUOUS` if you cannot make one fail.
- No hardcoded expected results. Invoke the real code path; assert on what it actually returns.
- Report honestly: a partial result is `PARTIAL`, never `PASS`. If a task cannot be done, say so and why.
- Write `writer/WRITER_MANIFEST.json` listing each file, its purpose and the raw command you ran to test it.

## T1 — receipt loss on retry (FAR018-ER1)

`HG-KSEOS/scripts/hgk-lane-dispatch.py` writes its receipt to a fixed path, so a retry overwrites the
record of the first attempt's refusal. The previous round lost exactly such a receipt and only recovered it
by hand.

Deliver: `writer/receipt_attempt_numbering.patch` (unified diff against the canonical file) plus
`writer/receipt_attempt_numbering_test.py`. The test must **create the failure the fix prevents**: write an
attempt-1 receipt, then let a second attempt run against the same path, and assert that attempt-1's bytes
are still readable afterwards. Also assert the fix does not rename or alter an existing receipt's content.
Read the canonical file first and quote in the manifest the exact lines the patch changes.

## T2 — non-vacuity regression proofs (A7)

For each probe below, a previous round shipped a probe that could not fail. Build
`writer/nonvacuity_regression.py`, which for each case runs the *repaired* artifact against the *original*
defect and requires a FAILURE verdict:

1. `writer/METADATA_SEMANTICS_V2.json` — the original defect: a mutable live source recorded with a
   point-in-time digest and treated as byte-exact.
2. `writer/CROSS_INDEX_V2.json` — the original defect: a hardcoded presence flag (`source_linked = true`)
   instead of a computed ledger-ID lookup.
3. The previous round's `self_check.py` S8b — the original defect: the success value written as the
   literal `True` with the declared predicate never consulted.

For each: state in the manifest what you corrupted, the command, the raw verdict, and the return code.
A case that passes when corrupted is a **finding**, not a success — record it as such.

## T3 — publisher argument safety (FAR018-BROKER-ARGUMENT-SAFETY)

In the previous round a `--help` probe **actually published**, because the publisher parses no arguments.
Deliver `writer/publisher_arg_guard.patch` + `writer/publisher_arg_guard_test.py`. The guard must make an
unknown argument exit non-zero **without performing any network call** (assert there is no network call by
monkeypatching the transport to raise), and must keep the documented invocations working.

## T4 — guard predicate candidate (B7, do NOT install)

The guard refuses evidence that merely *enumerates* skill reference filenames. Locate the guard
implementation under the `hgk-governed-execution` skill's `references/` directory (glob for filenames
containing `guard`), quote the predicate that decides refusal, and deliver
`writer/guard_predicate_candidate.md` + `.patch`: what the documented two-condition design is, what the
code actually does, the minimal change that restores it, and precisely what would break if the predicate is
loosened. **Deliver as a candidate for owner review — do not install it, and do not test it by weakening a
live guard.** A test that writes a temporary copy of the guard and exercises that copy is acceptable.

## Out of scope

Anything outside the round directory; any canonical in-place edit; any network write; any change to the
spine DB, the Kanban board, or the OpenSpec records.
