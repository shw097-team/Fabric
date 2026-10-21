# Decision question

Round `FAR-20261016-017-s4r6-residual-closure`, continuation of `PIPD-S4-R6-CLOSEOUT-20261016`.

The owner asked FAR to rule on **every** residual / gap / blocked item, **every** owner-decision item,
**every** candidate that has not been landed into usable form (including skills), and the matters of
**closing and handing over this session** — and then to execute the ruling, because the owner has
pre-authorized the ruling's execution.

The governing references are the two attachments of the S4 R6 round (the command厚
`S4 R6｜階段結案＋私人 Plugin 指揮薄.md` and the independent review
`PIPD-LS-SP｜S4 R6 修補後外部獨立複驗與階段結案裁決.md`) and the upper blueprint control package under
`C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\PIPD`.

## The question, stated so that it can be answered by measurement

For the set of residuals produced by the S4 R6 closeout round — the `F-R6-01..07` findings, the round's
`TT-R6-*` tickets and `O-1..O-5` owner decisions, the defects this round itself discovered
(`F-R6-08` served-document provenance drift; the `VERIFY_SECURITY` pool ordering defect), the
checker-side qualification limits, and the unlanded round assets — which action set is

1. **low-friction** (reuses what already exists; needs no new framework, no new release, no new
   governance plane),
2. **high-feasibility** (executable by this round with the authority it actually holds),
3. **high engineering necessity** (closes a defect that is real, or is explicitly ordered by the
   governing documents),
4. **not over-engineered** (does not build a second system to guard a line of prose),
5. **aligned with this session's objective and with the upper blueprint and the acceptance report**,

and which items must instead stay with the owner because executing them would exceed this round's
authority?

## Sub-questions that must be answered by measurement, not by opinion

- Q1 Which residuals are *already* closed by work that exists on `main`, so that re-doing them would be
  waste? (The R6 report says explicitly: stop re-asking for the D1/D2/ClaimCeiling repairs.)
- Q2 `F-R6-01` asks for "a single doc-link / release-identity check". Does such a check exist today? If
  part of it exists, exactly which part is missing, with locators?
- Q3 Can an agent-held round give its checker the ability to fetch served bytes and to run the test
  suite, inside the lane contract, or is that capability out of reach? (The previous checker recorded
  both as its own NOT_RUN.)
- Q4 What is the minimal, non-destructive form in which the `VERIFY_SECURITY` pool ordering defect can
  be handed to the owner without this round editing the control plane?
- Q5 Which of the remaining items are *structurally* the owner's (merge, tag, release, human account
  UI) and therefore must NOT be executed by an agent even under a pre-authorisation?
- Q6 What must a handover of this session contain so that a successor round can resume without
  re-deriving anything?

## Out of scope by the governing ruling (not re-litigated)

`S5`–`S8`, production promotion, public plugin directory / KYC / review, the `.hgk/` migration, the
`PR #14`/`#15` CNV lanes, and any change to the published `v0.1.1-preview.4` tag or its seven assets.
