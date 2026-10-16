# The verdict artifact contract, and sizing an audit against a context ceiling

Two shapes waste a verification round, and neither is fixed by a stronger model:

- the checker's verdict is a **terminal** output, so any budget/attention exhaustion destroys the whole
  check; and
- an **unbounded** multi-item audit is dispatched against a **fixed** context ceiling, so the checker
  spends its budget on fixtures and reaches the ceiling before it reaches the findings.

Fix both by ORDER and SIZE.

## The artifact contract

- **Pre-create the verdict artifact BEFORE the expensive work, and make the skeleton explicitly NOT a
  verdict.** The runner writes `<workdir>/VERDICT.json` with every item `INCONCLUSIVE` plus a flag such
  as `updated_by_checker: false`; the brief's first instruction is to take that file over (set the flag
  true, save back) and then update it IN PLACE after each item. Consequence: exhaustion can only
  DOWNGRADE items to `INCONCLUSIVE`, never delete the artifact.
- **The post-condition must refuse an untouched skeleton.** If exit-0 is accepted whenever the file
  merely exists, pre-creation manufactures exactly the false green the control exists to remove. Fail
  under a distinct code (e.g. `ERR_VERIFY_NO_VERDICT`) when the artifact is missing, unparsable, or
  still carries `updated_by_checker: false`.
- **A missing artifact is not a zero exit.** Give it its own exit code, distinct from the lane's own
  failure codes, so a report can tell "the check ran and failed" from "the check never produced a
  verdict".
- **The receipt should carry the flag, not just the verdict string** (`verdict`,
  `verdict_updated_by_checker`, `verdict_is_skeleton_only`), so a downstream reader cannot mistake a
  skeleton for an acceptance.
- **Ordering has to be written into the brief.** A deliverable list with no order clause is silent about
  order, and a checker will naturally write the verdict last. State the ordering as part of the
  requirement, with the reason.
- **Add a scope-discipline clause.** Forbid expanding beyond the listed items; require the smallest
  discriminating fixture and `INCONCLUSIVE` + reason for anything unresolved. An honest partial verdict
  in the file beats a complete analysis that never gets written.

## Sizing an audit against the ceiling

- Resolve the checker model's `context_window` / `auto_compact_token_limit` from the catalogue entry
  selected **by slug** — a first-match regex in a multi-model catalogue returns another model's numbers.
- Measure the peak `usage.inputTokens` of a single request from the provider's per-request ledger. A lane
  whose peak sits at ~99% of its declared compaction limit is working against history that has already
  been compacted away: the symptom is degraded judgement (a comparator that reports PASS on its own
  broken comparison) or an unterminated lane — not a clean error.
- **Shard**: N items per lane, sized so each lane's peak stays well under the ceiling (tens of thousands
  of tokens, not hundreds of thousands). Cheaper and more reliable than one deep lane under a bigger
  timeout, because the ceiling, not the timeout, is what binds.
- **Pre-bake fixtures** (a read-only pack with expected outputs) so the checker's budget goes into
  judging rather than into building test material.
- Sizing is part of the harness, so it is verifiable without a model call: assert the shard list covers
  every item exactly once and that each shard's item count is under the cap.

## Acceptance test for any such control

- **Positive**: force the budget to be cut mid-run and require the artifact to exist with at least one
  resolved item — exhaustion must leave a downgraded artifact behind.
- **Negative**: remove the control and require the artifact to be ABSENT. A control that cannot be shown
  to change the outcome is not yet a mechanism.
- **Boundary**: kill the lane mid-write and require the on-disk artifact to be the last incremental
  state — never absent, never a stale `PASS`.

## False-green shapes to look for in a checker lane

- Exit 0 with no artifact, because the verdict was optional or terminal.
- A verdict produced from a comparison the lane itself observed failing (e.g. a path comparator that
  reports every frozen file as "extra" because of a separator mismatch). A broken comparator must yield
  `INCONCLUSIVE`, never `PASS`.
- Facts attributed to a previous run without timestamps proving it. Require before/after counts and
  hashes, and check the artifact's own mtime against the lane's execution window — an artifact whose own
  timestamp contradicts its "legacy, unchanged" claim refutes itself.
- A lane reporting success while its log shows every command rejected by policy (sandbox/policy
  refusal): read the log, not the exit code.
- A verdict authored by the same agent that produced the deliverable. Independent acceptance is a
  separate, independently owned state; the maker cannot close it.
