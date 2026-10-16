# Handover hygiene for lane-based verification

An officer can only judge a delivery that was actually handed to it cleanly. These are the failure modes
that cost three rounds on a real governed round, and the mechanisms that fixed them.

## Hand the checker a clean worktree, and make that structural

- **The lane runner dirties the delivery by construction**: it writes the brief, its own runner script
  and the lane log into the same worktree that is then handed to the officer. `git status --porcelain`
  is therefore non-empty, and the officer correctly refuses to call the handover clean. Cleaning up
  afterwards fixes the instance, not the cause.
- **Fix it in the launcher, fail-closed**, with all four in place: commit the round's harness artifacts
  before launching anyone; require `git status --porcelain` to be empty and **exit non-zero without
  launching the model** if it is not; write the lane log to a directory **outside** the worktree; copy
  the log in and commit the lane's output only after the run finishes.
- Parameterise the worktree (`LANE_WT=<path>`) so a checker can exercise the refusal path against its
  own throwaway clone without ever dirtying the real delivery.

## Do not touch the subject while a checker is running

Even a tidy-up is worse than the dirt: a mid-run commit moves HEAD while the officer is verifying it.
Let the verdict land, then repair under control and re-hand. Say plainly that a passing subclaim is not
acceptance of a dirty handover, and that dirt created by the orchestration window is not evidence of a
defect in the committed candidate.

## Keep the officer's output inside the allow-list

A repository-root `verify/` is typically **outside** a round's write-set allowlist, so an officer writing
there produces an acceptance-set violation even though it only followed the brief. Name the
**round-relative** output directory explicitly in the brief, and take a copy of the subject **outside**
the tree (temp clone / worktree) so suites never run inside the delivery.

## Writer exit codes lie; read the bytes back

- Verify every produced artifact by re-reading it, printing its byte size and computing its hash.
- On Windows a lane agent must not build a patch in PowerShell and pipe it into `apply_patch`: the
  handoff mangles the encoding and it fails with `Error: --codex-run-as-apply-patch requires a UTF-8
  PATCH argument`. Write with the interpreter instead, with an explicit `encoding="utf-8"`.
- A lane agent that hits `Selected model is at capacity. Please try a different model.` should record the
  line verbatim, wait and retry — never silently substitute a model for a verification or research task.
  Two lanes sharing one checker model make this more likely: **serialise** them rather than running both.

## Adjudicating a lane that deviated from its declared model

- Record the deviation and the requested configuration; never relabel artifacts as the originally
  declared model's output, and never treat a lane label or a self-reported model id as provenance.
- A model's own `MODEL_SEEN`-style self-report, a catalog entry, a header echo or a transport warning
  are **not** identity evidence or health signals. A websocket upgrade warning that also precedes
  successful runs proves nothing about which upstream served the request.
- Do not infer "the model is unavailable" from a provider 4xx. Read the error text for what it actually
  names, and separate request/history/protocol failures from availability and from transport faults —
  the three have different remedies.
- Let an independent officer decide acceptance of deviant artifacts, and study the deviation with a
  dedicated research lane that itself must not be judged by the maker. The cheapest durable prevention
  is admission control in the launcher: pin the immutable assigned model **and** effort, refuse a
  changed model before any writer starts, qualify the exact configuration with a no-write multi-tool
  round-trip that must exit zero, and aggregate real child exit codes so failed children can never
  yield a green parent.
