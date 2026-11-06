# Session closure — round CNV-OWNER-DECISION-MAIN-LANDING-20261016

Claim ceiling: candidate only. Nothing here is an acceptance, a release or a production effect.

## What this round actually did

1. Measured the decision surface: 100 open items (kind histogram 28 gaps, 15 residuals, 14 blocked, 14 owner
   decisions, 13 unlanded candidates, 10 new, 6 closed), two open candidate pull requests, the default branch.
2. Ruled on nine options with one disposition each: executed R-B1..R-B6, prepared for the owner R-B7 and R-B9,
   rejected R-B8 (licence, continuous integration, metadata).
3. Found and repaired a real defect in the previous round's delivery: the homepage candidate was published with
   CRLF endings in an LF-only repository, so its diff rewrote all 72 lines. It is now `+77/-0`.
4. Admitted the round (`CNV-OWNER-DECISION-LANDING`, checkpoint `CK-LANDING-86F7DD4F`) and drove all four
   orchestration surfaces, including a named-method route with a negative control.
5. Ran three lanes on the owner's models: PLAN and VERIFY on `openai-codex/gpt-6.1-sol`, EXECUTE on
   `opencode-go/deepseek-v4.1-flash`. Both GPT lanes failed once under an unpinned required arm and succeeded
   when the rank was pinned.
6. Produced the owner bulletin for the 14 owner-decision and 14 blocked items, and had it checked.
7. Did NOT merge the two candidates: the independent checker cleared V1-V5 and held on V6, and the round's own
   gate made that verdict decisive.

## What is held and why

- PR #15: held. Additivity, mergeability and head binding all cleared; the hold is the V6 finding about the
  synthetic credential-shaped positive controls inside the scanner it publishes.
- PR #16: held under the same gate, although its own checks cleared, including the repaired additive diff.
- The owner's minimal action: settle whether the scanner's synthetic fixtures are acceptable in a published
  pack, then merge after a fresh live read. Neither merge needs more engineering.

## Model separation, stated plainly

This round's writer and checker ran different models on different providers, so the model axis is genuinely
separate for the first time in this sequence. The checker is still not an acceptance officer and its verdict is
advisory; the round claims nothing beyond candidate status.

## Resume pointer

- Read `EVIDENCE/CNV-OWNER-DECISION-MAIN-LANDING-20261016/` starting with `MERGE_DECISION.json`, then
  `FAR_RULING_2.json`, then `VERDICT3_RECHECK.md`, then `SELF_CHECK_RECEIPT_2.json`.
- Admission project `CNV-OWNER-DECISION-LANDING`; checkpoint `CK-LANDING-86F7DD4F`; board
  `cnv-owner-decision-main-landing`; SWARM root `t_71075154`; branch `evidence/cnv-owner-decision-main-landing-20261016`.
- Never redo: the homepage repair is published in PR #16; the two candidate packs must not be merged without the
  owner's answer on the V6 finding; published `EVIDENCE/**` blobs are never rewritten.
