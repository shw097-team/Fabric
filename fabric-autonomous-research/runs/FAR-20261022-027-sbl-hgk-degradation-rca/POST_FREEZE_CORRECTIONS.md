# POST-FREEZE CORRECTIONS — disclosed, with before/after and reason

The acceptance officer returned **FAIL** on the product as captured, naming two overclaims. Both were in this
round's own artefacts. Editing them is the honest repair; leaving them would let a defect sit under a claim that
still reads as true. Every correction is recorded here with what the text said, what it says now, who was wrong
and why.

Claim ceiling: CANDIDATE_ONLY. These corrections do not lift anything; they narrow two sentences.

## C-1 — `ResearchSynthesis.md` §4.3 item 2 (causal attribution withdrawn)

- **Before:** "…SBL 自己的標籤是 self-accept、HGK 又禁止同一 maker/checker，導致驗收必須外求獨立車道；記錄中
  3/3 回合因此沒有取得驗收（…W4:88）" — i.e. it asserted that the SoD/self-accept conflict *caused* the three
  sampled rounds to miss acceptance.
- **Now:** the structural half is kept ("acceptance can only be sourced from an independent lane") and the causal
  half is explicitly withdrawn, with the three rounds' own recorded reasons named instead (R7 checker
  `INCONCLUSIVE`; R9 no independent acceptance ever run; R10 a fresh-session handover criterion this session
  cannot satisfy itself — `evidence/W4_performance_delta.md:36-38`).
- **Who was wrong:** the writer lane. The officer's point is that a structural conflict plus a correlation is not
  a mechanism, and W4's own per-round rows contradict a single cause.
- **Evidence that the correction is not cosmetic:** the sentence now cites the three distinct per-round reasons,
  which the original citation list did not carry.

## C-2 — `ORCHESTRATOR_ADDENDUM.md` D6 (concurrency count corrected)

- **Before:** "`5ae4190` … i.e. **3 commits past the round's base**".
- **Now:** "`git rev-list --count 3dfaebc..5ae4190` = **9 commits**, not 3 — an earlier draft read only the last
  three entries of `git log --oneline -3`", followed by the nine SHAs with their timestamps and the note that two
  of them (`a32f675`, `ac9f35f`) change the lane plane this round measured on.
- **Who was wrong:** this orchestrator seat. The error class is the one the round's own W3 warns about: reading a
  display of N items as the count of the population.
- **Measured value:** `9` (`git -C HG-KSEOS rev-list --count 3dfaebc..5ae4190`), reproduced by the officer and by
  the VERIFY lane independently.

## Digest bookkeeping (deliberate, not silent)

`EVIDENCE_INDEX.json` and `ResearchRunReceipt.json` are generated **after** these corrections, so every digest in
them is post-correction. The two corrected files are named here so a reader can see that the frozen set moved by
exactly two files:

| File | Corrected? | Who found it |
|---|---|---|
| `ResearchSynthesis.md` | yes (C-1) | acceptance officer (AO-1) |
| `ORCHESTRATOR_ADDENDUM.md` | yes (C-2) | acceptance officer (AO-2) |
| `FINDINGS.tsv`, `VERDICT.json`, `DEVIATIONS.tsv`, `ProposedEvolution.yaml`, `ResearchHandoff.yaml` | no | — |
| `evidence/W1..W4` | no | — |
| `VERIFY_REPORT.md`, `ACCEPTANCE_OFFICER_VERDICT.md`, this file | authored after the officer's read | — |

Superseded pre-correction bytes were **not** preserved in this directory: both edits are small, the failing text
is quoted verbatim above, and keeping a stale copy of a withdrawn sentence invites it to be cited later. That
choice is itself disclosed here rather than left implicit.

## What the officer's FAIL does to the round's status

The round is reported as **`AO_FAIL_THEN_CORRECTED`** with the HGK acceptance left `NOT_RUN` and the workorder
result recorded as FAIL by a checker that is not the writer. A correction after the officer's read does not turn
its FAIL into a PASS: no second officer was dispatched, and this file does not assert one.

## C-3 — `ResearchHandoff.yaml` `resume_command` (placeholder → copy-ready)

- **Before:** `… --lane VERIFY_SECURITY <RANK_PIN_FLAG> 4 …` — the officer's word: "not copy-ready".
- **Now:** the literal flag, plus a new `resume_command_guard_note` field recording why the placeholder existed:
  the dispatcher refuses a `--brief` file whose text carries a remote-write marker
  (`ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED`, measured at 11:16 when a brief quoting `--force…` was rejected
  pre-dispatch). The token belongs on the command line, never inside a brief.
- **Who was wrong:** this orchestrator seat — the placeholder respected the guard but shipped a command nobody
  could paste.

## C-4 — `ResearchHandoff.yaml` RS4 target (superseded base → live head)

- **Before:** "Re-measure HG-KSEOS conformance on 3dfaebc".
- **Now:** re-measure at the live head, naming `5ae4190` and the fact that two of the nine intervening commits
  change the lane plane. The officer's objection was that RS4 pointed at a base the control plane had already left.
- **Who was wrong:** writer lane, faithfully copying this round's measurement base into a forward-looking action.

## C-5 — the checker's PASS is recorded, not endorsed

The officer held that the VERIFY lane's unconditional PASS "is not fully earned" on A4, because A4 asked whether
each root-cause claim carries a verifiable locator and the checker accepted the causal sentence that A4 was
supposed to test. Both statements now appear in the evidence MD §5: the lane returned PASS (verbatim, unchanged),
and this round does not claim the root-cause answer was completely verified. No re-run was attempted to make the
PASS look earned.

## Seal bookkeeping

Seal 1 = the set the officer read (`EVIDENCE_INDEX.json` digest `7a16700d…`, 26 entries). Seal 2 = the set after
C-1..C-4, regenerated by `freeze.py`; the workorder result already recorded in the spine references **seal 1**
digests, so seal-2 digests are registered as additional evidence rows rather than rewritten — a digest chain, not
a silent replacement. The spine's workorder row is `FAILED` and cannot be re-recorded by design
(`record_workorder_result` requires state `CREATED`).
