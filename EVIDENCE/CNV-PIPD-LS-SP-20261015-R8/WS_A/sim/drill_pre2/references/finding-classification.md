# Classifying findings: measured capability, preferences, and the register

Every line in a finding register, evidence appendix or open-items list is a **claim that something is
required**. This file is the rule set for earning that claim, so the register stays a signal instead of
becoming a list the reader learns to skip.

## Classify by MEASURED CAPABILITY, not by the fact that something happened

The trigger for a finding is never "an exposure occurred" or "a bad thing is technically present". It is
**what the thing can actually do**, and you usually already have the measurement:

| Observation | Capability | Classification |
|---|---|---|
| Value does not authenticate at all (401 at every endpoint, no scope header) | none | **preference**, one line, NOT an open item |
| Value authenticates but is narrowly scoped | real but bounded | finding — name the granted capability |
| Value authenticates broadly | full | finding — requires action |

Concretely: a credential that the server does not recognise confers **no capability**, so its disclosure
creates **no exposure that rotation would remove**. Rotation is then a hygiene *preference* — record it as
one line and explicitly not as a finding. A credential that returns 200 is live, exposure is real, and
rotation is required.

## A rejected finding is worse than no finding

An item that stays in the open register after the owner has ruled it unwarranted does more damage than
never having raised it: it inflates the open count, dilutes the items that matter, and forces the same
ruling twice. When the owner rules an item not warranted:

- **remove it from the open register**, and
- **record it as a stated non-requirement with its basis** — e.g.
  `rotation: NOT_REQUIRED — value is not recognised by the server (401, no scope header), therefore
  confers no capability`.

Do not simply delete it: a stated non-requirement is a decision a reader can audit; a silent omission
looks like something was dropped.

## Wording carries obligation — say which you mean

"The credential should also be rotated" reads as a requirement. If it is not required by a measurement,
write **"preference, not required"** in the same sentence, or a reviewer scores it as an unmet
requirement and the register shows a gap that does not exist.

The same trap applies to an action you *chose* not to take. Recording it as **"blocked"** reads as an
abandoned attempt at a wanted outcome. Record instead the **decision**, its trigger, and the exact command
that would execute it later — a deferral is a result.

## Correcting a claim means correcting it EVERYWHERE

A corrected claim that survives in one artefact keeps being read and re-raised. The correction is not
finished until a grep for the old wording comes back empty across everything you own that carried it:
acceptance master, hand-off note, the references you appended, memory, and the summary already given to
the operator.

When you fix the wording, say that you did and why — the artefact that previously asserted the stronger
claim should show the softer one **with the basis attached**, not merely the softer one alone, or the next
reader cannot tell whether it was measured or quietly downgraded.

## Non-claims are part of the finding

A finding stated without its boundary gets read as a broader claim than it is. Pair each one with what it
does **not** establish — "no remote deletion was performed", "the holder was narrowed to a suspect class,
not identified", "nothing was moved". A ceiling stated in the same breath as the claim is what keeps a
reviewer from inferring more than the evidence supports.
