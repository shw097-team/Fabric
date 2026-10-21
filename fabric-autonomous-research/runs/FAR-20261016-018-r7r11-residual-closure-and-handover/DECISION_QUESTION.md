# Decision question

Round `FAR-20261016-018-r7r11-residual-closure-and-handover`, continuation of `CNV-EVIDENCE-ARCHIVE-R7R11-20261016`.

The owner asked FAR to rule on **every** residual / gap / blocked item, **every** owner-decision item,
**every** candidate that has not been landed into usable form (including skills), and the matters of
**closing and handing over this session** — and then to execute the ruling, because the owner has
pre-authorized the ruling's execution.

Governing references: the R7～R11 command厚 (`Fabric × Hermes × HG-KSEOS｜R7～R11 外部驗收後續作「指揮薄
PROMPT」.md`), the independent acceptance report `Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md`,
and the upper blueprint control package `Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md`.

## The question, stated so that it can be answered by measurement

For the set of residuals the R7～R11 evidence-archive round left behind — the ten `EIA-20261016-01..10`
findings and their dispositions, the round's own discovered lane-binding defects, the seven errata the
three independent swarm lanes earned, the unlanded candidate assets (the two slimmed skills and the
round-local lane declaration), the owner-scoped-but-unexecuted peer chain, and the session's own
closeout/handover obligations — which action set is

1. **low-friction** (reuses what already exists; no new framework, no new release, no new governance plane),
2. **high-feasibility** (executable by this round with the authority it actually holds),
3. **high engineering necessity** (closes a defect that is real, or is explicitly ordered by the governing documents),
4. **not over-engineered** (does not build a second system to guard a line of prose),
5. **aligned with this session's objective and with the upper blueprint and the acceptance report**,

and which items must instead stay with the owner because executing them would exceed this round's authority?

## Sub-questions that must be answered by measurement, not by opinion

- Q1 Which residuals are *already* closed by work that exists, so that re-doing them is waste?
  (EIA-20261016-06 was closed in the previous round as metadata errata — verify, do not re-do.)
- Q2 `EIA-20261016-02` (R7-03) demands checker isolation that is *enforced by the OS*, not by end-of-turn
  hash equality. Is that achievable **on this host, today, inside the lane contract** — measured, not
  assumed? What exactly does the checker's sandbox currently permit and block, quoted from the dispatcher source?
- Q3 `EIA-20261016-07` reports the HGK skill's `entry_map.json` as dangling. Does the file exist, do the
  moved-payload pointers still verify, and is a non-destructive repair possible from verified data alone?
- Q4 Which residuals are *structurally* the owner's (merge, release, cross-repo code promotion, canonical
  control-plane edits, OS ACL on the product host) and therefore must NOT be executed by an agent even
  under a pre-authorisation?
- Q5 What must a handover of this session contain so that a successor round resumes without re-deriving anything?

## Out of scope by the governing ruling (not re-litigated)

The full 221-case / G-A～H convergence, production promotion, the `.hgk/` migration, the `R7-02` validator
code promotion into the PIPD repository, the peer chain `#6/#8/#10` merge, `PR #12` promotion out of draft,
and any edit to the published R6～R11 evidence — each of these is named, routed to its owner, and prepared
in one-action form, not executed here.
