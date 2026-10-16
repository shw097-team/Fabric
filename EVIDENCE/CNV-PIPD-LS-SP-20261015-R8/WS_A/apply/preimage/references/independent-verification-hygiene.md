# Independent-verification hygiene (governed acceptance rounds)

Rules for the lane that CHECKS a frozen subject, and for the artifacts that lane produces.
Each one cost a round to learn.

## Stage the checker's copy OUTSIDE the subject tree

An independent checker that needs a working copy must place it outside the repository /
worktree under verification — a `verify/<lane>/` path that is not inside the subject, or a
scratch dir outside the repo entirely.

Copying the candidate INTO its own tree pollutes the subject: tree-wide tests (scanners, smoke
tests, anything that walks the project) pick up the copy, and suites unrelated to the change
fail on it. The symptom is a cluster of failures in tests that have nothing to do with the
subject, appearing only in the round that copied inward — which then reads as product defects
and sends the next iteration chasing a phantom. Move the copy out, then re-run the full suite
from the pristine subject and compare counts before accepting any failure as real.

## Discovery is not effective load

The host chain is discover → effective load → invoke → POS/NEG → rollback. A gate satisfied at
one link does not satisfy the next, and these links are routinely conflated.

When a probe can LIST the installed skill/plugin names, that is DISCOVERY. A session answering
"8 skills, directory visible, contents not loaded" has proven nothing about load. Effective load
requires a transcript in which the skill body was applied to a bounded task.

Record the tier explicitly and never let a listing become a Host PASS:

    discovery            : VERIFIED
    effective load       : NOT VERIFIED
    POS / REFUSE / ADV   : NOT RUN

The same discipline covers the other surfaces: files present != registered,
registered != loaded, built != host-loaded.

## Verify the bytes of every artifact the round writes, including your own evidence

Read back and byte-count any substantial file before relying on it. A long tool-call argument
can be truncated in transit, and a placeholder marker can land INSIDE the file — leaving a
plausible-looking path that a reviewer later reads as your evidence, which is the worst possible
artifact to ship in a governance round. If a read-back shows the file short or carrying a marker,
rewrite it in smaller appended sections and re-verify. Check the OTHER new files from the same
batch too: one truncated write says nothing about whether its siblings landed.

## Keep the failure evidence of a lane deviation

When a declared model/provider/lane fails and execution continues on the declared backup, keep
the FAILING run's log and exit codes alongside the successful re-run, and carry the deviation as
an open item in the claim ceiling. Reporting only the successful re-run launders a backup-model
result into a declared-model claim.

## A superseded branch is a trap for the verifier — mark it

When a candidate cannot fast-forward (its base moved), do not force: publish a NEW dedicated
branch and record the rejected ref plus the reason. Then prove no history was rewritten
(`git merge-base --is-ancestor <old-tip> <new-tip>`) and state explicitly in the round record
that the OLD branch is stale and is not an acceptance subject. Leave a stale candidate branch
unmarked and the next verifier happily accepts bytes nobody tested.
