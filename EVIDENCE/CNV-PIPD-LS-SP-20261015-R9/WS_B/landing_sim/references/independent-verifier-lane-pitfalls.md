# Independent-verifier lane pitfalls (learned in the field)

## 1. A verifier that honours a read-only rule will run the suite in the WRONG environment

A checker told "do not mutate the subject" often refuses to run the test suite inside the checkout and
instead exports the tree (`git archive`) or clones it. Suites that depend on git history or build
outputs then fail there — and the receipt says the candidate is broken.

Rule: before accepting a "suite fails" finding, reproduce it on the BASE commit under the SAME
transport (`git archive <base> | tar -x`, then run identical argv). Identical failure counts
(failures/errors/skipped) prove an environment effect, not a regression. Only then argue about it —
and put the reproduction in the evidence, because the checker's own run cannot be edited.

Corollary: an independent checker has its own session and its own host side effects. Two seen in
practice: it pip-installed the subject into the GLOBAL site-packages, and it left the checkout dirty
from test side effects. Sweep for both and report them; they are findings about the harness.

## 2. Every "N tracked files get rewritten" claim needs to be measured, not assumed

Test suites and CLI checks that rewrite tracked artifacts (regenerating JSON projections, crosswalk
files) have a side-effect set the operator usually under-counts. Enumerate it empirically — run the
suite, diff `git status --porcelain`, count — before publishing a non-mutation guard that names a
specific number. A wrong count is a finding the checker will (rightly) raise.

## 3. Give the verifier a second round on the same frozen subject identity

A repair changes the subject commit. Re-freeze, re-run the checker, and expect fresh findings: the
second round both validates your repairs and independently confirms your disclosures (a checker
writing "TT disclosure correct" is worth more than any self-claim). Two rounds of "no new runtime
or schema defect" is the honest ceiling — never round it up to a pass the checker did not grant.

## 4. Correct a false claim by disclosure, not by rewriting the signed artifact

If the checker finds an inaccurate claim in your commit message or brief while the commit is already
hash-bound to its receipt, do NOT amend the commit — that invalidates the evidence that caught the
error. Write a correction record next to the receipt and restate the accurate claim there. State
in the commit that the product subject is unchanged and the tree is identical.
