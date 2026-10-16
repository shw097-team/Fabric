# Product-branch write-set gates: where a round's own artifacts may live

Pointer note: this file could not be linked from SKILL.md — that SKILL.md is already over the 100,000-char
limit, so no patch that grows it is accepted. Read this file directly.

A product repo can carry its own **positive** write-set gate: a CI step that measures
`git diff --name-only <DECLARED_BASE>...HEAD` and REFUSES any path outside a per-stage allowlist regex
(`ALLOWED` / `DENIED` / `ALLOWED_PLANTS` / `REFUSED_PLANTS`), with each stage's base and set declared in the
workflow itself. Treat that gate as an acceptance edge of the round, because it is one.

## The rule

- **Never commit the round's evidence tree or its `openspec/` change to the product branch.** A positive
  allowlist admits only enumerated product paths, so a round artifact directory fails the gate on the first
  push — correctly. The convention that already exists for this: publish the evidence on a **separate
  evidence-return branch** (keep the name shape the repo's earlier rounds used), and keep the product branch
  carrying product-shaped changes only.
- **Put a record where the docs ALREADY say it lives.** When documentation names the file a reader must
  consult ("its identities live in the `<tag>` entry of `docs/RELEASE_TUPLE.json`"), that path IS the target —
  not a new file invented beside it. Read the doc string before choosing the landing path; inventing a
  parallel file leaves the documented route broken while looking like progress.
- **Pre-simulate the gate locally, after committing.** The range is `BASE...HEAD` from the commit graph, so
  working-tree deletions that are not yet committed still appear in the diff. Commit first, then run the same
  regexes over `git diff --name-only BASE...HEAD` and report a single boolean. This catches the red run for the
  cost of one local command instead of a CI round-trip plus a repair commit.
- **Amend an allowlist only as a NAMED amendment, mirrored in the self-test.** One file, not a prefix; say in
  the workflow comment why (name the measured defect); add the same path to `ALLOWED_PLANTS` so the classifier
  still proves it refuses the frozen paths; and state in the PR that the arm was amended in this same PR
  rather than presenting it as pre-existing. Widening a guard to admit your own output is the antipattern the
  arm's own comments warn about.
- **Keep the red run.** The gate's first failure, the offending paths, the repair and the green run after it
  are all evidence; a reader who finds the failure first has found a concealment.

## The adjacent trap: repo conventions your new test file must satisfy

Adding a test file to a repo you did not write is two changes: the test, and the house style its own tooling
enforces. Measured: a new `tests/test_*.py` omitted the `sys.path` bootstrap every sibling file carries, and
that repo's tooling test turned the full suite red on an otherwise correct file. Read the header of an existing
sibling test first, and run the repo's FULL suite (not only the new file) before pushing — a gate that only
ever sees your new tests cannot tell you this.

## Ordering that avoids the whole class

1. Freeze the subject and read what the docs claim a reader can find.
2. Locate the repo's own write-set gate, its declared base and its stage; decide landing paths from it.
3. Keep the product branch to allowlisted paths; publish round evidence on its own branch.
4. Commit, then simulate the gate locally; only then push.
5. Record the hosted run ids for both the red and the green state of every gate that binds the round.

## Lane receipts: attribute by JOB, never by attempt number

The dispatcher names its receipt `<lane>_dispatch_receipt_attempt<N>.json` — **no job key**. Two different jobs
on one lane (a probe, then a writer) therefore produce attempt1 and attempt2 belonging to *different* jobs, and
`attempt2` also reports the deadline in seconds as its predecessor's id. The round read them as one job 'retried'.

Never publish a `failed attempt 1 / retried attempt 2` alert without checking the contract:

- Name the job in every row: `job`, `receipt path`, and the marker the job actually logged (`PROBE_DONE=…`,
  `LANE_ECHO=…`); pick the marker out of the payload, not from the file name.
- Cross-check against the per-attempt subdirectory `<lane>/attempt-<N>-<UTC>Z/`, which IS unique; nothing is
  separately overwritten when present, and its timestamp identifies the run.
- A lane that returned the payload but no nonce is `TRANSPORT_PROBE_ONLY / NOT_BOUND`: the dispatcher's
  `ERR_NO_ARM_EMITTED_NONCE` forbids a served-arm claim even though the row names the right provider/model.
- When the round reads a receipt, cite it by *attempt row*, not by request count, and correct the record on the
  PR when a later job overwrites the name — a reader who finds the correction first has found the defect.
