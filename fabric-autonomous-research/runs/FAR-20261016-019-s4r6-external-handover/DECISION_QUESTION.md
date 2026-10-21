# FAR-018 — Decision question

run_id: `FAR-20261016-019-s4r6-external-handover`
round: `PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016`
extends: `FAR-20261016-016-pipd-s4r6-closeout-learning`, `FAR-20261016-017-s4r6-residual-closure`

## The question

R17 delivered and pushed a **green** product candidate (`127ec1c`: install-doc release-identity pin,
same-`plugin_id` update route, a doc-identity guard, and a named `stage-c` write-set amendment) with its
packet on the evidence branch `0b50d3e`, verified by an independent checker (`PASS`, with an honest
ceiling) and by hosted CI (`verify` success). The residual universe it measured has 37 rows, 33 of them
not yet addressed, 12 of which are owner decisions rather than engineering work.

Given that, what remains that **this round can legally execute**, and that has the highest necessity for
the two readers the mandate names — an **external acceptance officer** who must verify, and an
**external engineering team** who must continue development?

Three candidate answers were on the table before the study:

- **(a) Nothing.** The candidate is green, the evidence is published, the rest is owner-gated. Declare
  closure and stop. (Safest; ignores the round's own reported defect.)
- **(b) Everything not yet done.** Attack the residual universe: `.hgk/` migration, PR #14/#15
  disposition, four-host UAT, the control-plane dispatcher repairs, a new preview release. (Highest
  apparent completeness; re-litigates owner rulings and exceeds the round's write authority.)
- **(c) Close only the defects that block the two named readers, and prove it.** The round reported one
  defect of its own making: its plan documents were never back-filled, so a verifier reading them first
  concludes the round never ran. And no artifact yet answers "how does an outside team continue?".
  Neither is owner-gated; both are cheap; both are exactly about the reader.

## Sub-questions

- **Q1.** Is the un-back-filled checklist pair actually a defect against the governing documents, or
  only an internal inconsistency? (If the thin-prompt or the acceptance report requires a plan document
  whose status matches reality, it is a requirement, not a nicety.)
- **Q2.** Which residual rows are **owner gates** (an agent must not do them) versus **nobody did them**?
  The two must not be merged, or the round either over-claims or under-delivers.
- **Q3.** What does an external engineering team need that no existing artifact provides, and can each
  item be proved by a command rather than asserted?
- **Q4.** Does the round's own write authority permit those artifacts, and where must they land so the
  hosted write-set gate does not go red again?

## What would change the answer

- A finding that the checklists are *not* required by the governing documents (then (a) gains weight).
- A real safety or regression failure on the product branch (then the priority is the failure, not the
  documentation).
- Evidence that an owner-gated item is in fact within the round's authority (then it moves to the
  execute set).
