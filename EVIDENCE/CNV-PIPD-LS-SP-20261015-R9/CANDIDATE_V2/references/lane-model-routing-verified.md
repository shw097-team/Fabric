# Verified lane model routing on this stack (Windows / Hermes + sealed Codex lane)

Lessons measured in a governed FAR round that had to prove which model served each lane.
Apply them when a contract mandates a per-lane model split (PLAN / EXECUTE / VERIFY-SECURITY).

## Routing a lane to a model, verifiably

- Route a lane by setting the delegation provider/model immediately before the dispatch, then
  restore and read both values back. Children keep the model they were spawned with, so this is
  safe even while other lanes run.
- The authoritative evidence is the runtime log line naming the session's own model and provider
  (e.g. `agent.log`, `conversation turn: session=... model=... provider=... platform=subagent`).
  The delegation banner can contradict the log; never report a route from the banner alone.
- A per-task override surface exists on the kanban dispatcher (`create --model/--provider`,
  `set-model`, and the dispatch mapping of the task's model/provider fields). Prefer it when a
  board drives the dispatch; it scopes the override to one card instead of the whole runtime.
- On failover keep the MANDATED MODEL and change only the provider; that preserves the axis the
  maker/checker rule needs.

## A probe that reports an arm live is not evidence the arm can serve as a lane

- Exercise the arm in the lane's own request shape (a real subagent turn), not only a raw
  completion. A measured case: the same model/provider answered a direct completion in ~5 s and
  never completed a subagent turn in two attempts (one stalled after 599 s at its 6th call, one
  never finished its first call in 1800 s). The same task on another provider finished in 159 s.
- A listed model is not necessarily a model that answers, and an answering model is not
  necessarily a usable lane. Report the three states separately.

## Reasoning-mode and budget artifacts

- A short-probe "empty answer" can be `finish_reason=length` with the budget consumed by
  reasoning, not a model fault. Probe with thinking disabled or a budget large enough for the
  reasoning tokens before concluding an arm is unreachable.
- State a plain/non-Flash sibling's timeout as an open contradiction (transport timeout versus a
  thinking-mode/budget interaction) with the evidence on both sides, not as a single verdict.

## Stalled lanes

- Bound a lane's context and prefer a write-first ordering; a stalled child can consume 10-30 min
  and never write its output file.
- A steer may not land if the child is mid-model-call; if a lane is silent, preserve its live
  transcript into the round as evidence before stopping it, and record the timed-out duration.

## Declaration surfaces self-contradict

- The same routing fact is often encoded at several sites in one policy file (a summary field, an
  assignment array, per-lane chain entries, and historical keys). Sweep EVERY active site or the
  file contradicts itself; that drift is the usual origin of stale model names.
- An independent checker should be pointed at the declaration file, not only at the conclusions;
  that is how the unswept sites are found.

## Final freeze order (do not reorder)

1. Enumerate and hash every artifact.
2. Write the evidence manifest.
3. Generate the single evidence file LAST so it binds every digest.
4. Mirror it to the further roots and assert the digests are equal (re-verify by hand with a hash
   tool, not only in-script).
5. Pin the configuration hash the round depends on and abort the generator on drift.
- A checker that scans citations may also scan its own previous output and report self-referential
  violations; classify those as tool defects rather than laundering the historical record.

## Host pitfalls confirmed here

- Pass NATIVE paths (`C:/...`) to native tools (python, git, node). MSYS-looking paths like
  `/c/...` reach native programs as `C:\c\...` and fail; a bash builtin `cd` is unaffected.
- A relay/proxy process that the sealed lane depends on has no supervisor: it can be killed mid
  round, and the lane then fails loudly (connection refused). Preserve the failed attempt as
  evidence, restart, verify readiness with a health probe before re-running.
