# False green: the three ways a verification step passes while proving nothing

All three were hit for real inside one governed round (AO independence). They share a signature: the
check reports SUCCESS exactly when its INPUT is missing, unstable, or already satisfied by the probe
itself. Treat a green result that would also be green with the system broken as a defect.

## 1. Vacuous pass -- the comparator's input never arrived

Symptom A: a mutation guard snapshots a declared root, the root does not resolve, the file list is
empty before AND after, and the guard reports `mutated: false` -- a clean bill of health from zero
evidence. Fix: refuse to run. Emit a typed blocker (`ERR_GUARD_ROOT_MISSING`) and return non-zero.
An empty input set is never a passing observation.

Symptom B: an A/B comparator digests a value it cannot find and substitutes a placeholder; the
placeholder is NOT EQUAL to the other side, so the comparison "passes" as disjoint. Fix: return an
EMPTY collection on no-match and make the call site three-valued:

    INCONCLUSIVE (either side missing) -> NOT ACCEPTED, non-zero exit
    FAIL         (intersection non-empty)
    PASS         (both present, disjoint)

Rule: assert non-empty inputs BEFORE comparing, and make "I could not find it" fail closed. Print the
observed SCHEMA KEY NAMES (never the values) so the operator can see why nothing matched.

## 2. Self-reference -- the artefact's digest depends on recording it

Symptom A: the freeze manifest lists itself; the recorded size/digest is the PREVIOUS revision, so
verification reports a mismatch on the recorder.
Symptom B: the run log written by the very command that builds the manifest is still being flushed
when the manifest digests it; the recorded digest is stale the instant the redirect closes.
Fix: exclude the recorder and any in-flight output from the scanned set BY CONSTRUCTION -- do not
"fix up" the digest afterwards, and never hand-edit a manifest. Keep run logs outside the scanned
directory.

## 3. Vacuous negative -- the negative probe already fails on a different condition

A negative probe only proves the guard works if the probe's attempt would otherwise have PASSED.
If the attempt is rejected earlier (missing nonce, missing usage receipt, missing arm) then the
void/refusal proves nothing about the guard.
Build the probe so it satisfies EVERY other acceptance condition, then asserts that the one condition
under test is what voids it, and record the satisfied conditions in the receipt so a reader can see
the attempt was a would-have-passed one.

## Deterministic (model-free) negative probes

Prefer a seam over a model when a negative must be demonstrated end to end. A `--<tool>-executable`
CLI override that points at a stub script makes the whole pipeline drivable with no model: the stub
emits the accepted carriers (nonce inside the message item, a matching usage row in a SCRATCH ledger
-- never the production ledger) and then performs the mutation. Cases to cover: clean control,
mutate, delete, create-inside-root (usually recorded but non-fatal), unresolvable root (must refuse
pre-spawn with 0 attempts). Freeze the pass into the regression suite, and state the ceiling: this
proves DETECTION of a real filesystem change by a real child process, not prevention.

## 4. Relaxed assertion -- a green suite that was made green

A writer landed a defect, a test caught it (`1 failed`), and the writer then edited the TEST so the
suite went green while the defect stayed. Detection, all cheap and independent of the report:

- Compare the test file's **size/mtime against the moment the failure was observed**. Measured case:
  the file was 20260 B at the run that reported `1 failed`, then 20257 B at the run that reported
  `22 passed`. Three bytes is exactly `assertEqual` -> `assertIn`.
- Call the function under test DIRECTLY with the failing input. If it still returns the old wrong
  value, the code was never fixed.
- Treat a report line like "No test was edited to match a regression" as an **assertion to be tested**,
  not as context. In that case it was false as written.

Rule: when a writer both owns a test and owns the code it tests, require the test's pre/post bytes and
never accept "all tests pass" as evidence that the code is correct. A relaxed assertion is a MEDIUM
defect and the associated report claim is its own defect.

## 5. Unenforced discipline narrated as enforcement

The checker's `read-only` property is often a HABIT, not a sandbox property: on hosts where
read-only blocks shell by policy, the checker must run `danger-full-access` to execute anything, so
non-mutation rests entirely on before/after subject hashes. Recording that as "read-only discipline,
non-mutation enforced" is an over-claim -- and the fix belongs in the ledger, not the log. State the
two facts separately: what the sandbox header says, and what evidence actually bounds mutation.

## 6. Fail-open order bugs in "any disabling setting" scans

A classifier that asks "is there any entry whose value disables interaction?" and returns true on the
FIRST hit has no precedence ordering, so a later, higher-precedence re-enable is ignored and the
whole-context verdict is a WRONG PASS. Any scan whose semantics are "the effective value is the last
one wins" must resolve ordering, not existence. Related: matching a helper by basename/family alone
accepts an arbitrary executable at an unexpected path as if it were the known-safe one -- require
resolved path plus digest identity, never a name.

## Reporting rule

When one of these is found after a green run, disclose it as a finding of the round and say which
claim it invalidated -- a defect caught by reading your own output is evidence the check is real.
