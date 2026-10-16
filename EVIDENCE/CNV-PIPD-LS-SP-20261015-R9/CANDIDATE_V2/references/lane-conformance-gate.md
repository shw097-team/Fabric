# Lane conformance gate (run this at admission, and again before any pack is delivered)

A declared lane/model arrangement is not satisfied by the lanes merely existing. It is satisfied only
when each role's receipt names rank, provider and model, and the arm produced real output. Verify it,
and disclose the result in the round's own files - a rule that lives only in the chat does not survive
context compaction.

## At admission

1. **Compare the serving model against the declared PLAN model.** Read this session's own model/provider
   and state it explicitly against the order. If they differ, do not proceed silently: either the
   operator switches the session model, or the deviation is recorded before work starts. A planner
   running on the writer's model means PLAN and EXECUTE are one model, which voids model-level SoD for
   everything downstream - including any "the checker is a different model" sentence written later.
2. **Persist the arrangement into the round's checkpoint/contract file**, verbatim, with the role ->
   provider/model mapping and the substitution rule. Compaction summarises chat, not the round's files.
3. **Smoke the lanes before depending on them.** Dispatch one trivial job per lane and require non-empty
   output. A lane whose configured executable path is stale (check it exists) or whose child returns
   nothing is a dead lane; discover that before the round, not at the report.

## During the round

4. **A lane that returns zero bytes stops the role - it does not silently reassign it.** If the writer
   lane produces nothing, the correct move is to say so and ask, not to write the artefact yourself and
   keep the original role labels. Self-substitution is what turns a declared three-model setup into one
   model wearing three names.
5. **Every substitute checker is labelled as a substitute.** On the declared arm's failure, dispatch the
   declared backup and record the switch, the failure code and the fact that the verdict now comes from a
   different checker. An unlabelled substitute verdict is a false independence claim.

## Before delivery

6. **Audit every independence sentence in the pack against a receipt.** Words like "distinct",
   "different process", "different model" are claims; each needs a receipt naming the model. If the
   receipt is missing, withdraw the clause and say so in the pack rather than shipping the adjective.
7. **Name the model, not the adjective.** "A distinct read-only lane" is unfalsifiable; "rank 4,
   openai-codex/gpt-6.1-sol, 0 bytes, ERR_LANE_ALL_ROUTES_EXHAUSTED" is checkable.

## Environment faults are real, and they are not the excuse

Two faults recurred in one round on this host and are worth checking every time: the lane config's
pinned Codex executable path was stale (the declared lane could not start at all), and a wired
`pre_llm_call` authorization-mint hook did not fire for the operator's authorization message, so the
token had to be minted by hand. Both are genuine, both cost time, and neither forced the role collapse:
that came from skipping steps 1, 2 and 4 above. Report environment faults as findings with evidence, and
keep them separate from the discipline failures - mixing them is how a genuine bug becomes an alibi.
