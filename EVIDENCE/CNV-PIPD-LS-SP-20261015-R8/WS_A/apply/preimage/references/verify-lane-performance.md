# Verify-lane performance: measuring why a delegated checker runs long

A recurring shape: delegated verification lanes take many times longer than maker lanes, stall more
often, and occasionally die with no artifact at all — and the instinct is to blame the verify model.
The measurement below is what settles it. Nothing here replaces the dispatch budget (SKILL.md rule 21)
or the stall-triage order; it supplies the diagnosis those steps act on.

## 1. Where the evidence lives

- **Per-child transcript**: `<hermes home>/cache/delegation/live/<deleg id>/task-<n>.log` — append-only,
  one line per tool call and per result, each result line carrying its wall duration (`ok 12.3s`,
  `ERROR 0.4s`). Plus `manifest.json` beside it with the delegation id, model, provider, start/end.
- **Runtime log**: `logs/agent.log` — per-call lines `API call #N: model=... provider=... in=... out=...
  latency=...`, plus spawn lines for delegations, turn-end reasons, and hard-stop events.
- Two independent parsers over these two sources is the point: they must agree where they overlap.
  Parsing the transcript gives tool-call counts and durations; parsing the runtime log gives API-call
  counts, token sizes and per-call latency. Treat a disagreement as "different counters" only after
  checking that it is not a real inconsistency.

## 2. Metrics to compute (aggregate; never print raw lines)

Per lane: wall clock, API-call count, tool-call count, result count, duration max/sum, count of result
lines carrying an error/refusal token, heredoc-mediated writes versus direct file writes, input and
output token growth (first vs last call), and whether an output file exists.

Then correlate, over the full call series of the worst lane, **per-call latency against input size and
against output size separately**. That single correlation is what decides the causal story.

## 3. What the measured shapes mean

- Latency tracked **output** size strongly and input size not at all — so the lane is slow because of
  what it generates and the tool work it drives, not because it re-reads a large context.
- Single-call maxima on a verify lane sat at 80–180 s against 1–4 s on maker lanes, and the cost
  concentrated in **broad filesystem discovery** (two scans timed out at ~180 s and ~197 s).
  Conclusion form: "no evidence supports intrinsic model slowness"; the difference is the work, not
  the model.
- A refusal/error tally taken by a fast text grep **undercounts** against the structured per-call lines,
  by a factor of three or more in practice. Re-derive any earlier hand-made count before publishing it,
  and correct the number openly when a checker contradicts it.
- A "lanes with an output file" count can be **null by design**: verdicts are often written outside the
  delegation cache, so a zero there measures where the lane writes, not whether it succeeded. Check the
  lane's own declared output path before reading 0 as failure.
- The first call of a lane can take an order of magnitude longer than its later calls; a long opening
  silence is a generation-length effect, not yet a stall.

## 4. Classify the interruption before it enters a statistic

An old lane is not automatically stalled, and a lane that died young is not automatically a lane defect.
Read the cause out of the runtime log first:

- An explicit hard stop, a parent-session end (`user_stop`, `parent delegation ended`), and a
  mid-stream drop all leave an interrupted child with no artifact — and they occur in the same second as
  the orchestrator's own turn ending. Those are **casualties of the parent turn**, not lane behaviour.
  Folding them into lane-quality numbers inflates the "verify lanes stall" story, and re-dispatching is
  the whole remedy.
- Distinguish that from a lane that is genuinely long: a fresh transcript mtime and a growing tool-call
  counter mean it is working, whatever its wall-clock age.

## 5. Failure modes that produce the long runs

Unbounded filesystem discovery (recursive walks over an install tree, greps across a whole runtime);
writing the verdict once at the very end, so an interruption loses everything; writing JSON or a long
file through a shell heredoc (mangled or invalid, unparseable on read-back); re-printing receipts and
transcripts into context instead of aggregating; retrying a refusal blindly; and an open-ended mandate
("verify all of it") that forces the lane to rediscover its own scope by scanning.

## 6. Remediation set, in the order to apply it

1. **Minimum viable, near-zero risk — write the verdict skeleton FIRST**, to its final target path,
   before any discovery, and refine it in place. Demonstrated live: a skeleton written on the first tool
   call survived a twelve-minute generation phase and left a usable verdict, where the same lane
   previously wrote nothing until the end and lost the run to an interruption.
2. **Biggest structural win — a frozen, numbered acceptance matrix plus a deterministic read-only
   evidence runner**, keeping bounded adversarial checks. The verifier then checks a list and runs a
   runner instead of rediscovering the scope.
3. Bound and index discovery: authoritative roots plus explicit exclusions.
4. Serialize-and-validate before replacing a safe artifact, with a checkpoint per item.
5. Typed refusal handling: stop retrying, emit BLOCKED/HITL.
6. Summarize receipts once; cap per-command output and context.
7. Per-item budget plus a no-progress watchdog.
8. Controlled telemetry / A-B qualification before ever swapping the model.

## 7. Steer rather than kill — and re-read before steering

A running lane can be steered: reorder its remaining priorities, cap the remaining tool calls, and tell
it to prefer a PARTIAL verdict with named unfinished items over running long. That is cheaper than
killing and re-dispatching, which also loses its accumulated evidence.

One trap: **re-read the artifact before steering about it.** A steer written from an observation a few
minutes old can order a lane to delete a file it has since written correctly; if the steer lands after
it finished, it is reported as undelivered — but the ordering is what decides whether a valid
article is destroyed. Read the file, then steer.

## 8. A verify lane that inherits the parent's model is not the lane the plan named

When a round's model plan assigns VERIFY to a specific model and the dispatch takes no model argument,
the child silently inherits the **parent's** model. A checker can look properly independent — separate
context, separate session, read-only mandate — and still be the wrong lane. Check the child session's
`model` in `state.db` rather than inferring it from the plan; a receipt that names the plan's model
while the session ran another is a fabricated SoD claim even when nobody intended one. Fix it by
pinning `delegation.provider`/`delegation.model` before dispatch, then restore (see the hermes-agent
skill's `configuration.md`).

Expect the correctly-pinned lane to be **stricter**, not merely different. A green run on the wrong
model is weak evidence of agreement, and re-running on the specified lane is how you find out: a
12-claim pass that also returns valid counter-examples means the earlier clean pass was a weaker
instrument, not a truer one. Neither verdict cancels the other — record both, and stop resting the
claim on the green one.

## 9. Receipts go stale against mutable surfaces — scope them, do not chase them

A receipt binds the artefact it read. If the published surface is later edited (README, release body,
notes asset), the receipt still holds for the **immutable** parts — tag, commit, tree, artifact bytes —
and no longer describes the edited ones. Re-running the whole verification after every wording change
is a treadmill, and "my old receipt predates my edit" is a category error rather than a defect.

Cut it by scoping explicitly: the immutables are covered by the receipt (permanently); the mutable
surfaces are covered by a **timestamped readback** that asserts the live copy is byte-identical to the
repository. Then disclose on the mutable surfaces and let one final readback close the cycle. Two
operational notes: an anonymous-API readback must treat quota exhaustion as INCONCLUSIVE rather than
FAIL, or it manufactures failures; and a "the branch points at the release commit" invariant is wrong
the moment post-release evidence commits land on that branch — assert reachability instead.
