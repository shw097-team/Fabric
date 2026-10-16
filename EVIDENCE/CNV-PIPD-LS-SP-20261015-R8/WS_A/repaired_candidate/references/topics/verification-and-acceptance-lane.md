===== SKCV-TOPIC-BATCH BEGIN theme=verification-and-acceptance-lane =====
topic: verification-and-acceptance-lane
note: complete verbatim bytes of absorbed files; envelope only, no byte edits; byte offset = offset of the absorbed file's first byte within this topic file
segment_count: 4

===== SKCV-TOPIC-SEGMENT 1 BEGIN path=references/verdict-artifact-and-budget.md offset=475 bytes=5032 sha256=79efb0c631348071900d7a2ad599bfd4f5792f79c564a455bb2b22936313f5ab =====
# The verdict artifact contract, and sizing an audit against a context ceiling

Two shapes waste a verification round, and neither is fixed by a stronger model:

- the checker's verdict is a **terminal** output, so any budget/attention exhaustion destroys the whole
  check; and
- an **unbounded** multi-item audit is dispatched against a **fixed** context ceiling, so the checker
  spends its budget on fixtures and reaches the ceiling before it reaches the findings.

Fix both by ORDER and SIZE.

## The artifact contract

- **Pre-create the verdict artifact BEFORE the expensive work, and make the skeleton explicitly NOT a
  verdict.** The runner writes `<workdir>/VERDICT.json` with every item `INCONCLUSIVE` plus a flag such
  as `updated_by_checker: false`; the brief's first instruction is to take that file over (set the flag
  true, save back) and then update it IN PLACE after each item. Consequence: exhaustion can only
  DOWNGRADE items to `INCONCLUSIVE`, never delete the artifact.
- **The post-condition must refuse an untouched skeleton.** If exit-0 is accepted whenever the file
  merely exists, pre-creation manufactures exactly the false green the control exists to remove. Fail
  under a distinct code (e.g. `ERR_VERIFY_NO_VERDICT`) when the artifact is missing, unparsable, or
  still carries `updated_by_checker: false`.
- **A missing artifact is not a zero exit.** Give it its own exit code, distinct from the lane's own
  failure codes, so a report can tell "the check ran and failed" from "the check never produced a
  verdict".
- **The receipt should carry the flag, not just the verdict string** (`verdict`,
  `verdict_updated_by_checker`, `verdict_is_skeleton_only`), so a downstream reader cannot mistake a
  skeleton for an acceptance.
- **Ordering has to be written into the brief.** A deliverable list with no order clause is silent about
  order, and a checker will naturally write the verdict last. State the ordering as part of the
  requirement, with the reason.
- **Add a scope-discipline clause.** Forbid expanding beyond the listed items; require the smallest
  discriminating fixture and `INCONCLUSIVE` + reason for anything unresolved. An honest partial verdict
  in the file beats a complete analysis that never gets written.

## Sizing an audit against the ceiling

- Resolve the checker model's `context_window` / `auto_compact_token_limit` from the catalogue entry
  selected **by slug** — a first-match regex in a multi-model catalogue returns another model's numbers.
- Measure the peak `usage.inputTokens` of a single request from the provider's per-request ledger. A lane
  whose peak sits at ~99% of its declared compaction limit is working against history that has already
  been compacted away: the symptom is degraded judgement (a comparator that reports PASS on its own
  broken comparison) or an unterminated lane — not a clean error.
- **Shard**: N items per lane, sized so each lane's peak stays well under the ceiling (tens of thousands
  of tokens, not hundreds of thousands). Cheaper and more reliable than one deep lane under a bigger
  timeout, because the ceiling, not the timeout, is what binds.
- **Pre-bake fixtures** (a read-only pack with expected outputs) so the checker's budget goes into
  judging rather than into building test material.
- Sizing is part of the harness, so it is verifiable without a model call: assert the shard list covers
  every item exactly once and that each shard's item count is under the cap.

## Acceptance test for any such control

- **Positive**: force the budget to be cut mid-run and require the artifact to exist with at least one
  resolved item — exhaustion must leave a downgraded artifact behind.
- **Negative**: remove the control and require the artifact to be ABSENT. A control that cannot be shown
  to change the outcome is not yet a mechanism.
- **Boundary**: kill the lane mid-write and require the on-disk artifact to be the last incremental
  state — never absent, never a stale `PASS`.

## False-green shapes to look for in a checker lane

- Exit 0 with no artifact, because the verdict was optional or terminal.
- A verdict produced from a comparison the lane itself observed failing (e.g. a path comparator that
  reports every frozen file as "extra" because of a separator mismatch). A broken comparator must yield
  `INCONCLUSIVE`, never `PASS`.
- Facts attributed to a previous run without timestamps proving it. Require before/after counts and
  hashes, and check the artifact's own mtime against the lane's execution window — an artifact whose own
  timestamp contradicts its "legacy, unchanged" claim refutes itself.
- A lane reporting success while its log shows every command rejected by policy (sandbox/policy
  refusal): read the log, not the exit code.
- A verdict authored by the same agent that produced the deliverable. Independent acceptance is a
  separate, independently owned state; the maker cannot close it.
===== SKCV-TOPIC-SEGMENT 1 END =====
===== SKCV-TOPIC-SEGMENT 2 BEGIN path=references/sealed-evidence-corpus.md offset=5722 bytes=4816 sha256=276955b67c30961e7d6cf0bc22b56e2968da719d4e0d86719440c2e096e82b81 =====
# Adding a NEW artefact to a SEALED evidence corpus

The class: a corpus has already been externally accepted (a sealed subject binding, a frozen manifest,
a reviewer's sign-off) and this round must add its own evidence to the same folder without disturbing
what was sealed. The trap is that a corpus checker rarely scans all files equally.

## The prefix-series hijack

A checker can **select the LAST sorting member of a filename prefix** and assert against that one file.
Common selections are "the latest must carry no self-hash" and "the latest's declared subject must equal
the manifest's `subject_root` and the checker's own subject". Add a new file into that series and it
becomes "the latest", so **it silently becomes the subject of checks it was never written for** - and a
binding an external reviewer already accepted moves.

Rules:

- **Read the checker before naming anything.** Find which files it selects by name, by prefix, by sort
  order, or by "latest". Those are the files you must not join.
- **Name round evidence OUTSIDE the sealed series**, with a distinct family name, and let the round
  directory be how a reader finds it.
- **Prove the binding did not move rather than asserting it.** Run the checker **before** and **after**
  the addition, record both verdict lines and the printed binding value, and corroborate with
  byte-identity of the sealed file at the commit's parent and at the commit. A single PASS after the fact
  is not evidence that nothing moved; the before/after pair is.
- **Never regenerate the manifest so it includes your new file.** That rewrites the exact-set counters
  and the sealed subject root to include material nobody reviewed - manufacturing acceptance one layer up
  from `EXISTS != TRUE`. Declining this is usually the most important judgement in the whole task.
- **Two manifests can declare the same schema version with different content** (different entry counts,
  different subject roots). Establish which instance the checker actually reads, state which one you
  chose, and do not average them or quietly prefer one.

## Put AFTER-the-run records OUTSIDE the run root

A run that produces its own manifest — a file listing every artefact with its digest, plus a run digest
over the sorted (path, sha) pairs — is **self-sealing**: the moment a file is added, renamed or rewritten
inside it, the manifest's file list and digest are stale, and the run stops verifying for exactly the
reason it exists.

So records produced **after** the run go **as a sibling beside the run root** — e.g.
`<run_id>.EXECUTION_RECORD.md` next to `<run_root>/<run_id>/` — never inside it. This covers an execution
record for a decision the owner later authorised, a hand-off note, and a post-hoc correction.

- Reference the sibling **by path** from the run's own decision/hand-off record.
- Do **not** regenerate the manifest to absorb it — the same rule as the sealed corpus above.
- Do **not** rewrite the run's candidate file to say `executed: true`. The run's job was the decision; its
  frozen bytes are the evidence the decision was reached *before* the action, and that ordering is the
  point.

Generate the artefact set **programmatically** from the declared contract rather than hand-writing N files —
hand-writing a large fixed set invites schema drift, and a missing member then looks exactly like a member
that never existed.

## Publish the digest out-of-band

If the contract forbids a self-hash in the body, publish the artefact's own digest in a **sibling
sidecar committed in the same change** as the file it digests, so a reader re-hashes and compares. Assert
mechanically that the body contains no self-hash literal, rather than assuming the generator honoured it.

## Use the owner's contract, and run the owner's checker

Reuse the corpus owner's own written contract (`AGENTS.md` or equivalent) rather than inventing a format
that reads well to you - a locally invented shape will not survive the owner's own gate. Then actually
run that gate. If the team's contract and your format disagree, the contract wins.

## Commit ONLY the paths this round authored

A corpus folder is frequently dirty with other sessions' uncommitted entries. `git add` the exact paths
and say so; a commit that "adds everything to be safe" destroys the ability to attribute anyone else's
work. Report the pre-existing dirty count before and after as the proof that nothing else was swept in.

## A sealed corpus is not the place to land a claim

State in the artefact itself that it extends nothing already sealed and closes no finding. Submission-
ready as **evidence** is not an acceptance verdict, and writing it as though it were is the over-claim a
checker will find next.
===== SKCV-TOPIC-SEGMENT 2 END =====
===== SKCV-TOPIC-SEGMENT 3 BEGIN path=references/independent-verification-hygiene.md offset=10764 bytes=3385 sha256=9da3a1278235d4373e38a4ddf83c4f07b8cb2287d563e5cd3da4f43d7d40b339 =====
# Independent-verification hygiene (governed acceptance rounds)

Rules for the lane that CHECKS a frozen subject, and for the artifacts that lane produces.
Each one cost a round to learn.

## Stage the checker's copy OUTSIDE the subject tree

An independent checker that needs a working copy must place it outside the repository /
worktree under verification — a `verify/<lane>/` path that is not inside the subject, or a
scratch dir outside the repo entirely.

Copying the candidate INTO its own tree pollutes the subject: tree-wide tests (scanners, smoke
tests, anything that walks the project) pick up the copy, and suites unrelated to the change
fail on it. The symptom is a cluster of failures in tests that have nothing to do with the
subject, appearing only in the round that copied inward — which then reads as product defects
and sends the next iteration chasing a phantom. Move the copy out, then re-run the full suite
from the pristine subject and compare counts before accepting any failure as real.

## Discovery is not effective load

The host chain is discover → effective load → invoke → POS/NEG → rollback. A gate satisfied at
one link does not satisfy the next, and these links are routinely conflated.

When a probe can LIST the installed skill/plugin names, that is DISCOVERY. A session answering
"8 skills, directory visible, contents not loaded" has proven nothing about load. Effective load
requires a transcript in which the skill body was applied to a bounded task.

Record the tier explicitly and never let a listing become a Host PASS:

    discovery            : VERIFIED
    effective load       : NOT VERIFIED
    POS / REFUSE / ADV   : NOT RUN

The same discipline covers the other surfaces: files present != registered,
registered != loaded, built != host-loaded.

## Verify the bytes of every artifact the round writes, including your own evidence

Read back and byte-count any substantial file before relying on it. A long tool-call argument
can be truncated in transit, and a placeholder marker can land INSIDE the file — leaving a
plausible-looking path that a reviewer later reads as your evidence, which is the worst possible
artifact to ship in a governance round. If a read-back shows the file short or carrying a marker,
rewrite it in smaller appended sections and re-verify. Check the OTHER new files from the same
batch too: one truncated write says nothing about whether its siblings landed.

## Keep the failure evidence of a lane deviation

When a declared model/provider/lane fails and execution continues on the declared backup, keep
the FAILING run's log and exit codes alongside the successful re-run, and carry the deviation as
an open item in the claim ceiling. Reporting only the successful re-run launders a backup-model
result into a declared-model claim.

## A superseded branch is a trap for the verifier — mark it

When a candidate cannot fast-forward (its base moved), do not force: publish a NEW dedicated
branch and record the rejected ref plus the reason. Then prove no history was rewritten
(`git merge-base --is-ancestor <old-tip> <new-tip>`) and state explicitly in the round record
that the OLD branch is stale and is not an acceptance subject. Leave a stale candidate branch
unmarked and the next verifier happily accepts bytes nobody tested.
===== SKCV-TOPIC-SEGMENT 3 END =====
===== SKCV-TOPIC-SEGMENT 4 BEGIN path=references/finding-classification.md offset=14365 bytes=3707 sha256=6055fcd360b24dfab3c7bfd642df25a99575b69ccc2dcfa96c8822930dce9226 =====
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
===== SKCV-TOPIC-SEGMENT 4 END =====
===== SKCV-TOPIC-BATCH END =====
