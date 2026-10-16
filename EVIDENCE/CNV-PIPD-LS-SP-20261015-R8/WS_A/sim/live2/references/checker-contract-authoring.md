# Authoring a verification contract that yields a DECIDABLE verdict

Load this before writing or revising an independent-checker contract (see rule 53 and rule 40). The
contract is an instrument: when a round returns DISAGREED or UNCERTAIN, the first question is whether the
product failed or the instrument asked an unanswerable question. Measured in one round: a nine-property
contract returned 6 RE_DERIVED / 2 DISAGREED / 1 UNCERTAIN, both disagreements and the uncertainty
resolved to the CONTRACT's wording, and the next revision returned ALL_PASS 9/9 with no product change.

## The property set that converges

Write 5-10 numbered properties, each with a verdict vocabulary of `RE_DERIVED` / `DISAGREED` /
`UNCERTAIN`, and define the top-level verdict as `ALL_PASS` only when `DISAGREED == 0 AND UNCERTAIN == 0`.
Make each property a DISCRIMINATOR, never a topic: "the recorded value does not move with the checkout"
not "the fix looks right". Pin the subject by digest inside the contract, require the verdict to name the
revision it read, and require `evidence.raw_commands` (command, cwd, exit_code) plus a raw output excerpt
per property so you can adjudicate from captured output instead of the checker's prose. Require a
`falsification_attempts` array and a `not_verified` + `claim_ceiling` pair that grants nothing.

## Form 1 — the candidate is UNCOMMITTED

A pristine clone of the commit beneath an uncommitted candidate contains the PRE-fix bytes. Any property
of the form "a pristine checkout shows the new value" is then unsatisfiable, and the clone's disagreement
is the control, not a defect. Write it as two steps and label the intent:

1. Clone at the base commit, run the tool there: expect the OLD shape (no new keys). Call this the CONTROL.
2. Copy the working-tree subject files INTO that same clone, re-run, assert the property there, and state
   that `measured_now` may legitimately differ between the two trees while `value` must not.

Where the round is free to commit before verifying, commit and keep form 1 as the literal-clone assertion
instead — that is the stronger claim, and it needs no overlay. Either way say which form you used and why.

## Form 2 — never quote a from-memory baseline

Do not put a suite count, a failure count or a named failure cause in the contract. You will be wrong
(measured: a remembered "1 failure, cause X" was actually 2 errors + 1 failure with a different cause) and
the checker reports the divergence against the PRODUCT. Instead require the checker to establish its own
control and report the delta:

- run the suite on a copy carrying the PARENT revisions of the changed files (a matched parent-subject
  control), and
- compare the failing/erroring test NAME sets between candidate and control, and
- compare test name sets in the changed test module between parent commit and candidate, so "purely
  additive, N added, 0 removed" is a measured statement.

An identical name set means no candidate regression whatever the raw counts are. Also ask explicitly for
pre-existing failures to be attributed as pre-existing with their cause.

## Form 3 — the suite runs in a COPY, and the copy excludes the evidence tree

The product's own suite frequently writes into the tree it runs in (projection writes, scratch fixtures),
so an in-place run breaks the read-only posture you just promised. Mandate the copy, then handle the two
ways the copy itself fails:

- **Windows MAX_PATH.** Long-path support is commonly DISABLED on a Windows host, so the limit is 260
  characters including the destination prefix. A deep evidence directory (a nested candidate copy left by
  an earlier round is the usual source) plus a deep scratch prefix exceeds it and the copy dies with
  `FileNotFoundError [WinError 3]` — which surfaces through the suite as an ERROR and reads as a product
  defect. Measure before you blame the candidate:

  ```bash
  python -c "import ctypes; print(ctypes.windll.ntdll.RtlAreLongPathsEnabled())"
  python -c "import os;r=r'<repo>';m=max(((len(os.path.join(d,f)),os.path.join(d,f)) for d,_,fs in os.walk(r) for f in fs));print(m)"
  ```

  Then compare `len(destination_prefix) + len(longest_relative_path)` against 260. Exclude the evidence
  directory (`.hgk/`, `openspec/`, any round tree) from the copy and say why in the contract; those paths
  are untracked round artifacts, not product.
- **Recursion through your own scratch.** Confirmed by rule 48: scratch left inside the tested tree makes
  the subject's own `copytree` recurse. Put scratch OUTSIDE the tree and say so in the contract.

## Form 4 — grading a RED suite

A red suite observed in the AUTHORING tree is not the candidate's result. Measured in one round: the suite
reported 13 failures + 1 error when run in the dirty authoring tree or a copy of it, and `283 tests OK` in
a clean anonymous clone of the same branch — the failures were an artifact of the tree's own untracked
evidence and deep paths. Therefore state the tree a red was observed in, and grade the candidate from a
clean checkout plus a matched control. Never publish a dirty-tree failure count as the candidate's.

## Revision discipline

- Freeze the contract and pin ITS digest in the same operation as the subject digests (rule 40). A contract
extended after the freeze is lower-authority; if you must extend it, re-freeze and record a dual pin.
- When a revision revokes a property, keep the revocation IN the new contract as a labelled correction
  naming the earlier wording as the author's defect. Do not silently drop the row — a dropped row is
  indistinguishable from a property that passed.
- Make the verdict name the contract revision it read, so "which instrument produced this" is answerable
  from the artifact.
- Carry the adjudication into the deliverable: per disagreement, the product-vs-instrument call, the raw
  output that decided it, and whether any product change followed (usually none).

## Checklist before dispatch

1. Every property is decidable and mapped to a message the checker can measure.
2. No property requires a pristine checkout to exhibit an uncommitted change (form 1), or it is labelled a
   control.
3. No baseline number or failure cause is quoted from memory (form 2).
4. The suite is contracted to run in a copy, the copy excludes the evidence tree, and the path arithmetic has
   been checked (form 3).
5. The tree a red may be observed in is stated, and grading is from a clean checkout (form 4).
6. Subject digests pinned; contract digest pinned; read-only scope and the single permitted write path named;
   `ALL_PASS` defined as `DISAGREED == 0 AND UNCERTAIN == 0`.
7. The prompt POINTS AT the contract file rather than inlining it, and names the interpreter path plus the
   ban on the shell's alternatives (rule 45).

## Adjacent lesson: verify the verdict, then verify the PRODUCT from outside

After the checker returns, spot-check its decisive properties from its own captured raw output before
reporting the verdict — and once the candidate is committed and published, re-run the decisive property
from an ANONYMOUS clone. That external run is what turns "locally verified" into "publicly consumable" and
it is the one check a maker cannot self-sign.
