# Session closure and handover — CNV-HYGIENE-README-CLOSURE-20261016

Claim ceiling for everything in this document: LOCAL / candidate only. Nothing here is an acceptance.

## What this round delivered

1. A measurement of the repository surface and the local surfaces, read-only, into `A00_HYGIENE_AUDIT.json`.
2. A FAR deviation study with one ruling per finding: executed `R1 R5 R7 R8 R9`, rejected `R2 R11`, owner-gated
   `R3 R4 R6 R10`. See `FAR_STUDY_AND_RULING.md` and the machine form in `FAR_RULING.json`.
3. Typed admission for the round, then the four orchestration surfaces: change record (strict-valid), named-method
   route (`hygiene_readme_closure` -> NATIVE), board with the round's cards, and a SWARM graph of three workers.
4. A bounded writer lane and a read-only verifier lane, both served through the Codex CLI relay on the owner's
   mandated arm, with usage receipts. The verifier's own finding set: V1-V7 CLEAN, `VERDICT: PASS`.
5. The homepage upgrade: a status refresh plus an external-reader appendix, additive, every other section intact.
6. Branch hygiene: 14 remote branches whose pull request is merged were removed, each with its tip commit and its
   rollback ref recorded first; the open, the orphan and the default branch were kept.
7. This pack, published through PR #16 and read back blob by blob.

## What is explicitly NOT claimed

- No independent acceptance, no acceptance-officer acceptance, no effect admission.
- No production or runtime release. The status words on the homepage remain true after this round.
- No continuous-integration status: this repository has no workflow file, so any green light would be invented.
- Model-axis independence is ABSENT for this round's lanes: the writer and the checker ran the same mandated
  model, so only the process and the evidence paths were separate. This is the same declared condition as the
  previous round, not a new finding and not a repair.
- The homepage change is NOT on the default branch. It is a candidate in PR #16, and the owner decides.

## Open items and their owners

| id | item | owner |
|---|---|---|
| PR-16 | merge or return this round's homepage and pack | Owner / Maintainer |
| PR-15 | the previous round's pack is still open, unmerged | Owner / Maintainer |
| R2 | a root LICENSE: a licence choice is an owner/legal decision, not a round's | Owner |
| R3/R4 | continuous integration and repository metadata: considered and rejected for this round | Owner |
| R6 | destructive local cleanup (control-plane database pre-images, worktrees, sandbox binaries) | Owner (human) |
| R10 | publishing the homepage to the default branch | Owner |
| TS-VAL-01 / TS-CHECKER-01 / TS-G1-01 | the three routed-out task specifications from the previous round | their owners |

## Resume pointer for the next session

- Canonical control plane: HG-KSEOS. Fabric is the policy contract surface; the current canonical Hermes is its
  governed runtime/orchestration plane. Do not build a second control plane.
- Read this first: `EVIDENCE/CNV-HYGIENE-README-CLOSURE-20261016/` in the repository, starting with
  `APPLY_RECEIPT.json`, then `FAR_RULING.json`, then `SELF_CHECK_RECEIPT.json`.
- Round ids: admission project `CNV-HYGIENE-FAR-RULING`, work orders `WO-TS-RULING-01..06`; board
  `cnv-hygiene-readme-closure`; SWARM root `t_02df625d`; branch `homepage/cnv-hygiene-readme-closure-20261016`;
  PR #16; default-branch commit at publish `bcd91043`.
- Never redo: the 14 branch removals already happened (rollback refs are in `BRANCH_HYGIENE_RECEIPT.json`); the
  merged pull requests #12, #13 and #14 must not be merged again; published `EVIDENCE/**` blobs are never
  rewritten; the lane registry and route slots are never edited to make a dispatch succeed.
- Restore path for the removed branches: create `refs/heads/<name>` at the tip commit recorded for that branch in
  `BRANCH_HYGIENE_RECEIPT.json`.

## Owner-gated local hygiene candidates (recommendation: leave to the owner)

| candidate | size | why it is destructive | recommendation |
|---|---|---|---|
| the control-plane spine database and its three pre-images | ~823 MB each plus ~794 MB | the live state and the only rollback basis | never delete the live one; leave the pre-images |
| archived evidence shards holding a nested runtime binary | ~334 MB | deleting makes an archived run unreplayable | leave |
| checker sandbox binaries bound to evidence | ~298 MB each | deleting breaks the replay of the evidence that binds them | leave |
| roughly 120 `*.bak-*` pre-images under config, scripts, src, tests | KB each | each is a pre-image in a chain | leave |
| 20 worktrees, some detached or holding an unmerged tip | unmeasured | some hold the only reference to a commit | leave |
| untracked trees and eight worktrees in the repository clone | up to ~9.8 MB per file | untracked content may be its only copy | leave |
