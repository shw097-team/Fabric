# VERIFY lane brief — review of FAR run FAR-W0-R27-UNBLOCK-20261111 (read-only)

You are the independent checker for a FAR research product. Read-only: no writes, no repair, no push.
Your job is to falsify the product, not to praise it.

## Subject

Run directory:
`C:/Projects/Agent_Workspace/FHS_R26_WT/fabric-far/FABRIC/fabric-autonomous-research/runs/FAR-W0-R27-UNBLOCK-20261111/`
Read: `ResearchRequest.yaml`, `ResearchPlan.yaml` (if present), `ResearchSourceDenominator.tsv`,
`ClaimLedger.tsv`, `ContradictionLedger.tsv`, `RejectedAlternativeLedger.tsv`,
`OpenQuestionLedger.tsv`, `ResearchSynthesis.md`, `RetrievalLedger.json`, `CrossReferenceLedger.tsv`.

## Four attacks, in this order

1. **Unsupported claims.** For every row of `ClaimLedger.tsv` whose status is MEASURED, check that the cited
   source actually says what the claim says. A claim whose evidence does not contain the number is
   `UNSUPPORTED`, not "approximately right". Report the claim ids.
2. **Category errors.** The synthesis distinguishes "a mechanism exists" from "an effect is authorised", and
   "a pool admits a slot" from "an assignment makes it dispatchable". Find any place where it collapses two
   of those into one and calls it closed. Name the paragraph.
3. **The over-read test.** The synthesis claims the full-22-gate hold was a misread (`B4`). Try to refute that:
   is `GATE_R26.json` really a full-profile run of the same gate, and does its 21/22 actually discharge the
   challenge's demand? Quote the challenge text and the gate record side by side.
4. **The unblock test.** For `U1`, `U2`, `U5`, `U8` in `ResearchSynthesis.md` section 2: is the stated success
   criterion checkable by a command, or is it a description of an outcome? A step whose "success" cannot be
   falsified is not a plan.

## Also

- Confirm whether `RetrievalLedger.json` shows web as `WEB_RETRIEVAL_SKIPPED_NO_ROOTS` and whether the product
  declares that honestly rather than silently.
- State what this run does NOT establish (e.g. it cannot authorise a merge, sign an acceptance, or prove a host effect).

## Output

A table `attack | finding | evidence (file:line or command) | severity (BLOCKER/HIGH/MODERATE/NOTE)`, then
`verdict ∈ {RESEARCH_PASS_CANDIDATE, REVISE, REJECT}` with one sentence of justification, then
`claim_ceiling_recommendation` naming exactly which tokens this research product may and may not carry.
If you cannot run a check because the environment denies it, write `UNPROVEN <reason>` — never guess.
