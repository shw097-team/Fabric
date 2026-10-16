# Dispatching an independent checker against a subject that must not move

A checker that measures "the subject did not change" is only meaningful if the orchestrator stops
changing it. Three failures cost a full re-run each time; avoid them by construction.

## 1. Freeze and clean the subject BEFORE the lane starts

The checker snapshots the worktree at start and re-snapshots at the end. Any tracked file edited in
between is reported as a non-mutation FAIL — correctly, because from the checker's point of view the
subject really did move. Commit everything you intend to be part of the subject first, and assert
`git status --porcelain` is empty immediately before dispatch.

This includes artefacts **you** think are harmless: a task list, a brief, a note. If it is tracked
and you edit it, you fail your own check.

## 2. Put every run artefact OUTSIDE the subject

The brief, the lane log, the guard file and the receipt must live in scratch, not in the tree under
check. If they are inside, either the runner dirties the subject mid-run or you cannot record the
run at all.

Pattern that works: runner reads the brief from scratch, writes logs and the guard to scratch, and
the orchestrator copies the artefacts back into the subject **only after the lane has fully exited**,
then commits them as a separate, path-disjoint evidence commit. Verify with
`git diff <product-commit>..<evidence-commit> -- <product paths>` being empty.

## 3. Never tick your own acceptance box before the verdict exists

A checker will find it and refuse it, e.g. "the working task list marked independent-officer task
complete before this verdict was issued; this state is absent from frozen HEAD and cannot be accepted
as evidence of independent acceptance." Marking your own completion is the one thing the whole
separation-of-duties apparatus exists to prevent; doing it in passing destroys the receipt's value.
Tick it in a commit **after** the verdict, quoting the verdict.

## 4. Keep the invalidated run

When a run is invalidated by your own action, do not delete it and do not let it be mistaken for a
verdict. Rename it (`*_RUN1_INVALIDATED.json`), commit it, and say in the round report what it caught
and what you changed. A checker that caught your mistake is the strongest evidence the check was real.

## 5. Expect the checker to catch your prose

Cross-check your own numbers against the frozen subject before dispatch: file counts, commit SHAs,
tree SHAs, test totals. A stale figure in a summary (a count measured on an earlier commit, quoted
against a later one) is a legitimate disagreement and reads as carelessness. When it happens, fix the
statement and preserve the checker's wording verbatim.

## 6. Assert the served model, not the requested one

Confirm from the lane's own startup header that the checker ran as the intended model and provider,
and if the runtime does not expose an exact model id, record that as an independence limitation rather
than claiming the pin held. `required_arm == served_arm` is the check; the request is not evidence.
