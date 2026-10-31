# ORCHESTRATOR ADDENDUM — deviations and concurrency observed after the writer's files were frozen

Author: orchestrator lane (Hermes session plane). This file is ADDITIVE. It does not alter
`DEVIATIONS.tsv`, `FINDINGS.tsv`, `VERDICT.json` or any other writer artifact; those stay byte-frozen as the
writer produced them. Claim ceiling: CANDIDATE_ONLY.

## D6 — the control plane moved while the round ran (concurrent actor, disclosed)

- The round's measurements were pinned at HG-KSEOS `3dfaebc5c1d2ffe7d1782f3027bd25b54a557f2b` (clean tree,
  verified at 10:10 and again at 11:38 by the VERIFY lane).
- At 11:32:22 +0800 another session committed `5ae4190 feat(oracle): a typed semantic oracle that refuses what
  the PIPD schemas accept`. Measured properly: `git rev-list --count 3dfaebc..5ae4190` = **9 commits**, not 3 —
  an earlier draft of this addendum read only the last three entries of `git log --oneline -3` and understated
  the advance. The nine, oldest first, are `8e602eb` (10:36), `ab0773e` (10:52), `726ccc8` (10:53), `eec2f17`
  (11:01), `d09dda0` (11:06), `a32f675` (11:14), `5973688` (11:17), `ac9f35f` (11:27), `5ae4190` (11:32) — all
  after this round's 10:10 base check. Two of them touch the lane plane directly
  (`a32f675 feat(lane): derive the assignment from the registry…`, `ac9f35f feat(lanes): separate lane, round,
  session and served scope…`), which is precisely the plane this round's probe receipts were measured on.
- Effect on this round's claims: none of the numeric claims is retracted — the VERIFY lane re-derived every
  one of them **against `3dfaebc`**, so they are base-pinned and reproducible. What changes is the freshness
  ceiling: this report says nothing about `5ae4190`, and any reader must re-measure the conformance residual
  (RS4) on the newer head.

## D7 — the audited SBL board also moved during the round (concurrent actor, disclosed)

- W3 captured `sbl-r14-full-product` at 23 ready / 8 done (10:19:31). By 11:58 the same board reads
  **20 ready / 11 done**: three cards completed at ~10:51 by another session.
- Effect: the capability finding "the backlog does not drain inside the round's window" is snapshot-scoped and
  stays true as stated (`evidence/W3_capability_probe.md:97` says exactly that); the stronger temporal claim
  ("this backlog never drains") is **not** made by this round and must not be inferred from it. Three of 23
  cards did drain while this round ran, which is the honest counter-evidence.

## D8 — this round's own lane accounting (stall census)

| Attempt | Lane | Budget | Outcome |
|---|---|---|---|
| probe | EXECUTE rank1 | 180 s | ok, 3.78 s, nonce present, usage ok |
| probe | VERIFY rank4 | 180 s | ok, 2.50 s, nonce present, usage ok |
| slice 1 | EXECUTE rank1 | 1200 s | `ERR_LANE_ALL_ROUTES_EXHAUSTED` after landing 3 of 6 files |
| slice 2 | EXECUTE rank1 | 700 s | same code, 0 files |
| slice 3 (dispatch 1) | EXECUTE rank1 | — | refused before spawn: `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` (brief carried a `--force` marker inside a resume command) |
| slice 3 (dispatch 2) | EXECUTE rank1 | 1500 s | ok, 282.67 s, 3 files, usage ok |
| verify | VERIFY rank4 | 1100 s | nonzero `ERR_NO_ARM_EMITTED_NONCE`, full verdict in persisted stdout |

Same-shape repeat count for the writer timeout class: **2** (under the owner's >4 threshold). The action taken
was budget/decomposition and a mechanical templated brief — never a loosened oracle. The measured lesson is
that the same arm finished the same three files in **282.67 s** once the brief became fill-in-the-blanks,
against 1900 s of failed budgets before it.

## D9 — one correction to the writer's framing, made by the orchestrator

`VERDICT.json.capability_states.SELF_DETECT` = **PASS** while `evidence/W3_capability_probe.md:19` headlines
`SELF-DETECT / REPAIR / ACCEPT / EVOLVE | FAIL` as a *grouped* row. The VERIFY lane examined this and held the
PASS to be a fidelity improvement (W3's own detail row at `:1010` records detection as working and non-mandatory),
not a softening. This addendum records the discrepancy so a reader does not have to discover the grouped-vs-split
row difference alone. No state was changed by this note.
