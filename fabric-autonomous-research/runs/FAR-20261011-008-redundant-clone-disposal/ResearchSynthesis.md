# FAR synthesis — FAR-20261011-008-redundant-clone-disposal

**Decision question.** Should `C:/Projects/Agent_Workspace/PIPD-r7-release` be deleted?

**Verdict. `DELETE`.** High engineering necessity, low resistance, reversible.

## Why

The clone is **85 MB of data that two other sites already hold**.

1. **Nothing unique is committed there.** All 14 ref targets resolve to objects PIPD already has
   (`PIPD_HAS=14 PIPD_MISSING=0`). The working tree is clean, there are no stashes and no untracked files.
2. **The one plausible "unique" — its branch `r7-del018-successor` — is not unique.** PIPD has no ref by
   that *name*, but the commit it points at (`024d358cc972…`) is reachable in PIPD from two live branches,
   `postrelease-narrow-repair-20261011` and the current round branch `s4-r2-affected-only-20261011`.
   So it is an **ancestor of the work in flight**, not an orphan only this clone preserves.
3. **It is independently preserved upstream.** An anonymous read of the public repo returns
   `refs/heads/r7-del018-successor = 024d358cc972…`. Deleting the local copy leaves the commit in two
   independent places.
4. **It is not a boundary of anything.** Its `origin` is a *local filesystem path*, not a network remote,
   so it is not a publication mirror and holds no release-authority role.
5. **No governance record binds it.** A read-only pass over the shared spine found no requirement,
   taskspec or work order referring to it.

## Cost of each branch

- **Keep:** 85 MB (12.3% of PIPD's own 691 MB) and one more path a reader must reason about, in exchange
  for zero unique capability.
- **Delete:** one local `rm -rf` of a clean directory; reversible in minutes by
  `git clone C:/Projects/Agent_Workspace/PIPD` (no network, no credential) or by fetching the branch from
  upstream.

## Non-claims

This run does **not** claim: that the push credential works; that anything was deleted (it was not — this
is a proposal); that deleting the clone deletes anything upstream; that any other clone in the workspace
is also redundant.
