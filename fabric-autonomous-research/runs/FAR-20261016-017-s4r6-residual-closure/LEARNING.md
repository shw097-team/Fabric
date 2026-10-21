# Learning

## 1. Run the gate that judges you BEFORE you push, not after

PR #18 went red on `verify` while `ci` stayed green. The cause was not the code: the product repository's
own governed write-set classifier judges `git diff --name-only <declared base>...HEAD` against a positive
allowlist, and the round's evidence directory is deliberately outside it. The exact refused path set was
reproducible locally in one script, because the allowlist is a literal regex in a checked-in workflow.
**Rule: for any repository that gates on a declared write set, extract the classifier and run it against
your own `BASE...HEAD` before the first push. A red check that you could have computed locally is a
self-inflicted delay, and it also means the reviewer learns your scope from a failure instead of from you.**

## 2. Fix the artefact, not the gate — and if the gate must move, name the amendment

Two ways existed to make the red gate green: permit the round's evidence tree inside the product write
set, or move the evidence out. The workflow itself rejects the first ("an exclusion a reviewer can read
beats a permission a reviewer has to notice"), so the ruled action was to move the evidence to a
dedicated branch — the repo's own precedent. The one genuine allowance change was `docs/USER_GUIDE.md`,
which the round's work order names and the stage's allowlist omitted; that was done as a **named,
one-line amendment**, disclosed in the PR body and in the packet, exactly as the workflow's own
convention requires. **Rule: prefer moving your artefact over widening the gate; when widening is
required by the work order, make it one named line a reviewer can see, never a prefix that swallows a
class of paths.**

## 3. A control-plane collision may be an owner order, not a defect

The `VERIFY_SECURITY` pool ranks the writer's own model first, which silently destroys separation of
duties if a round just "dispatches the VERIFY lane". It is tempting to file that as a defect and fix it.
It is not a defect: the registry records the collision as `SOD006-C3`, status `OWNER_ORDERED_IN_FORCE`,
under an owner order dated the same day. Reordering it would reverse an owner decision. **Rule: before
proposing a control-plane "fix", read the declaration that produced the state (`declared_by`, registry
status). The round's correct action is to obtain the arm it needs by identity, and to record the
divergence — not to edit the plane that measured it.**

## 4. A checker's NOT_RUN can be a property of the harness, not of the subject

The previous checker recorded two NOT_RUNs. Both were sandbox limits: network sockets refused, no usable
temporary directory. Neither said anything about the deliverable. The lane contract already had the
remedy — an escalated sandbox plus a guard root that must not change — so the limit was removable.
**Rule: when a checker reports NOT_RUN, classify it (subject property vs harness capability) before
accepting it as a permanent bound. Bounds the round can remove should be removed; bounds it cannot must
stay visible.**

## 5. Aim falsifiability at the historical defect, not only at synthetic mutations

The new guard's own mutation cases run against the current document. That proves the checks can fail, but
it does not prove they would have caught the defect that motivated them. Running the guard against a
worktree of the pre-repair commit (`d3bd545`) produced `FAILED (failures=6)`: four real-document checks
caught the historical defect, and two mutation cases refused because their fixture base differed — which
is the healthy behaviour the repository's own comment describes. **Rule: for a guard written after a
defect, re-run it against the tree before the repair. That is the only run that answers "would this have
caught it?"**

## 6. An evidence packet's home is a branch, not the product diff

The product repository has a convention: a round's evidence lives on its own branch, and the product
branch carries only the product change. Following it is not bureaucracy; it keeps the governed write set
equal to the product change, which is exactly what makes the write-set gate meaningful.

## 7. Reconnaissance sub-agents pay for themselves when they are pointed at artifacts, not opinions

The 37-row residual universe and the red-gate find (`RS-01`) came from two read-only children that were
told to read named files and report locators, and to put anything they could not locate in a separate
section. **Rule: give a reconnaissance child a file to write, an exact source list, and an explicit place
to admit failure; then de-duplicate in code.**

## 8. The inverse of the first lesson: a green `ci` is not a green PR

`offline-gate` was green on the same head whose `verify` was red. Two gates, two different subjects —
the suite and the write set. Reading only one of them produces a false all-clear, which is the same class
of error as the `tee` false-green the repository already documents.
