# Answering "is the mandate complete / can a third party accept this now"

The recurring question arrives in three parts at once (*are the reported findings resolved? is the
mandate's task list done? can an external officer accept the artifact?*) and the three have DIFFERENT
answers. Answer them separately; a single verdict conflates them and always rounds up.

**Scope rule when the order says "run it through to external acceptance" / "do not leave gaps":** the
deliverable then INCLUDES the acceptance packaging (the gaps in section 7). Reporting a verified LOCAL
result and asking whether to also package the evidence is not diligence — the packaging was already
ordered, and asking converts finished work into a return trip. Ask only where a real decision is missing
(a scope change, a destructive or canonical side effect, a credential), never for permission to complete
what was ordered.

## 1. Take the mandate's own enumeration as the denominator

A governed prompt usually enumerates its items itself: a findings ledger (N rows, listed by id), a
work-order table, a UAT case list, and a numbered final-output list. Build one row per enumerated item
and disposition it. Never answer from impression, and never re-derive the item set from memory — the
mandate's list is the checklist the reviewer will use.

## 2. The disposition vocabulary is closed and its members must not be summed

`closed` / `closed_pending_<gate>` / `conditional` / `deferred` / `blocked` / `owner_pending` /
`out_of_scope`.

- "N/N dispositions recorded" is NOT "N/N PASS". A mandate that demands "every item dispositioned" is
  satisfied by having all of them — a different claim from all of them being closed. Print both numbers.
- A row closed by an OWNER RULING rather than by a code change is closed as a decision, and its
  before/after artefact bytes are identical. Say which of the two it is in the same sentence.
- A row that is `blocked` on source availability is not "in progress"; it is a named blocker with an
  owner.

## 3. Read the mandate's own termination section before writing your verdict

Governed mandates state what a PASS REQUIRES (often: an authorized independent verdict over the same
frozen subject, plus every safety authorization closed). If that condition is unmet, the GLOBAL verdict
is the mandate's own partial state regardless of how many local cells are green. A clause reading "if X
remains unresolved, keep the global verdict FAIL/PARTIAL" is a standing instruction, not advice — and a
local "the small cases work" must never be written as a whole-mandate PASS.

## 4. Run, do not assert, the remote-acceptance blockers

For "can an external officer accept this from the repository" the blockers are checkable in seconds:

```bash
git remote -v                                   # none configured => there is nothing to read
git rev-parse HEAD                              # a local-only commit is not a candidate
git status --porcelain | wc -l                  # uncommitted work is not a candidate
git cat-file -t <observed-baseline-sha>         # absent => candidate cannot be bound to the reviewed subject
<artifact> publication --check --current        # the artifact's own publication gate
```

Plus the authorization state (a non-granting license means there is no publishable content).
Report each as a NAMED blocker, then state the honest split: a third party can review the LOCAL frozen
tree and the evidence master; a REMOTE acceptance is not possible today. The absent baseline commit is
the one no local evidence can repair — the reviewer's subject is simply not present.

**No `origin` configured is NOT itself a blocker — check before you report it as one.** A repository that
was built locally has no remote while the remote nonetheless exists (a public repo needing no credential):
add the plain URL (`git remote add origin https://<host>/<owner>/<repo>.git`) and re-run the check. Report
an absent remote only when the target genuinely does not exist, and say which of the two you measured.

**Classify every red gate as PRE-EXISTING or round-introduced.** Run the same gate against the pristine
baseline and record the difference: the same class of violation is often old for one path and new for
another, and a pre-existing gap reported as this round's defect sends the repair queue after the wrong
target. Quote the violation's own reason string — it names the checker's input, which is usually not the
file you would guess.

**Deliver the readiness answer as a table of OBSERVED exit codes, then a two-sided verdict.** Run the
officer's own commands inside the anonymous clone and report, per check, the raw result (suite ran N tests
/ OK / skipped K, verifier exit 0, installer exit 0, doctor on a fresh root exit 0, the packaging gate's
exit 1 with its violation list). Then split the answer in two sentences: what the officer CAN now do
(clone, read the evidence, execute each acceptance command) and which gate WILL fail if their checklist
includes it — with the named fix or the owner's disclosure option. A single "ready / not ready" word hides
one of the two halves and always overstates the whole.

## 5. Disclose what you fixed while answering

The act of answering this question is itself a read of the deliverable, and it commonly turns up the
document's own self-contradictions (see rule 52). Those belong in the reply as a disclosure, not as a
silent cleanup: the reviewer reads the same file you just corrected, and a contradiction they find
later looks like concealment.

## 6. Close with the ceiling and the open items

State the claim ceiling verbatim, list every unclosed item with its owner and its earliest next step,
and say plainly which claims are NOT made (`INDEPENDENT_PASS`, `PUBLICATION_APPROVED`, `RELEASED`,
`PRODUCTION_VERIFIED` are separate claims that do not inherit from each other or from a green suite).

## 7. Publishing the code is NOT publishing the evidence — the four packaging gaps

A pushed branch with a green suite can still be unacceptable to an external officer, because acceptance
needs the round's EVIDENCE in the clone, not just its code. Four gaps, all measured on one round that had
already been pushed and independently verified:

1. **The evidence was never committed.** The round's evidence directory was untracked, so the clone held
   none of it — the independent verdict, the verify contract, the re-run results, the adjudications. Any
   item a reviewer must read has to be tracked in the delivered branch, or it does not exist for them.
2. **No binding for the TIP.** An earlier subject attestation pinned an older commit, so the branch tip
   was bound by nobody; recompute the subject digests and write a branch-scoped attestation for the
   current tip, additively (never rewrite the existing sidecar).
3. **No acceptance entry point.** Grep the repo for the deliverable name, the tip sha and the round id:
   zero hits means the reviewer has no stated starting place. An entry document carries branch + subject
   commit/tree, the defect and the change, the digests, ONE runnable command per acceptance item, what was
   deliberately NOT done, and the claim ceiling.
4. **The canonical specs surface was not updated.** Check the repo's own convention FIRST — in one repo an
   empty specs directory is the norm for every change and not a gap; calling it a gap is a false finding.

**Verify the packaging from a FRESH ANONYMOUS clone with credentials removed.** Clone the public branch
with no credential helper, then run the entry document's commands verbatim and require each one's raw
output — the digests match, the suite's pass/skip counts, the projection gate's `violations []`, the
attestation's `PASS`, and the strict validation's `N passed, 0 failed`. A reviewer's first two minutes are
exactly these commands; if they are not reproducible anonymously the deliverable is not published, whatever
the local tree says. Rebuild the evidence manifest (derived counts, not typed) after any such re-run so the
delivered set matches what the commands actually consume.

**The clone is the control for your own local result, in BOTH directions.** A red you saw in your working
tree and cannot reproduce in the clone is a local-ref artifact — name the ref it depends on (a sibling
branch, a pinned commit constant, an uncommitted file) and report it as such, never as a delivered defect.
Symmetrically, a green that has only ever existed in your own working tree is not evidence about the clone:
the same ref dependence runs the other way, and a test asserting on repository STATE or on a local ref can
pass for you and SKIP or FAIL for the reviewer. Run the acceptance set in the clone before quoting any
number from it.

**Then finish the packaging by publishing the evidence SET, not the whole round directory.** A round
directory is mostly working state (live agent homes carrying `auth.json`, container venvs, superseded runs),
and a repository-side digest builder that walks the whole tree will list every one of those paths — including
credential files — into a manifest that then gets committed. Relocate that scratch out of the product tree
BEFORE any reseal, secret-scan the curated set, ship an index with per-file sha256 and an
`excluded_on_purpose` list carrying reasons, and check the sibling rounds to learn whether tracking evidence
in-tree is this repository's convention (if it is, an untracked evidence directory is an EVIDENCE_GAP, not a
stylistic choice). Recipe: the `remote-repo-publication` skill's `references/evidence-curation.md`.
