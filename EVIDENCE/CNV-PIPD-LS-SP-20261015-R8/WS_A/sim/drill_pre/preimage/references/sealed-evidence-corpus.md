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
