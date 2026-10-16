# Git-tree integrity signals, and restoring repository metadata from a frozen copy

Depth for the boundary/attribution rules (a modification attributed by mtime window, a superseded pin,
a checker's own footprint). Use it when you must claim "this tree was not touched", when a boundary count
MOVES between two of your own measurements, or when you must restore a repository a concurrent writer
damaged.

## 1. A `dirty`-count boundary signal is fragile — know what pollutes it

Observed on one shared governed repository inside twenty minutes, with no product edit:
`git status --porcelain` reported 33, then 44, then 37, then 33 lines. Three different mechanisms, none of
them a source change:

| Mechanism | Symptom | Evidence to read |
|---|---|---|
| `.git/config` lost `[diff] ignoreSubmodules = dirty` | nested-repo gitlink entries appear as ` M <path>` with **0 insertions / 0 deletions** (`git diff` shows no text change; index mode `160000`) | `grep -A1 '^\[diff\]' .git/config`; compare a pre-incident copy's config bytes |
| index `assume-unchanged` bits set or cleared | the same gitlink paths appear or vanish from `status` | `git ls-files -v -- <path>` — a LOWERCASE status letter (`h`) means assume-unchanged, `H` means normal. Count them: `git ls-files -v | grep -cE '^[a-z]'` |
| a tool that manages its own directory | a managed skills/config directory appears as `D` then reappears | the directory's own target file and mtime; re-run the tool and re-read `status` |

Consequences for a boundary check:
- **Never compare a `dirty` COUNT across two runs without comparing the SETS.** `diff <(sort) <(sort)` two
  porcelain dumps: an equal count can hide a swap, and a moved count can be one added directory line —
  git collapses untracked directories, so new files inside an already-untracked directory do not move the
  count at all.
- Report `dirty_entries` plus the explicit set, and state which entries are product paths.
- A delta consisting only of gitlink `-dirty` markers or managed-directory churn is a metadata artifact:
  say so and name the mechanism. Do not report it as a source change, and do not "fix" it by restoring
  bytes a legitimate later state produced (superseded, not reverted).

## 2. Restoring a repository after a destructive incident

A deletion can remove `.git/HEAD`, `.git/config`, `.git/index` and `.git/logs` while leaving `objects/`
intact. Restore from a byte-copy taken BEFORE the incident (a frozen acceptance copy is ideal), then prove
the restore by counts and sets:

1. `git rev-parse HEAD` and `git rev-parse --abbrev-ref HEAD` — expected commit and branch.
2. Tracked-file count versus the tree: `git ls-files | wc -l` must equal
   `git ls-tree -r --name-only HEAD | wc -l`.
3. `git fsck --full` — expect no missing/corrupt objects; dangling commits are benign.
4. `.git/config` — restore the frozen bytes verbatim rather than hand-editing the missing sections.
5. index flags — read the FROZEN index for truth: `git ls-files -v -- <path>` shows `H` when nothing was
   marked. Clear wrong marks with `git update-index --no-assume-unchanged <path>`. An agent that
   "reproduced the baseline" by marking paths assume-unchanged changed state; it did not restore it.
6. `.git/logs` — copy the frozen logs tree back; a missing reflog is metadata loss, not content loss.
7. `git remote -v` — if it is empty in the live tree, check the FROZEN copy before calling it lost: a
   repository legitimately pushed via an explicit URL has no remote configured.
8. Close with set equality: `git status --porcelain | sort` versus the frozen copy's, byte-identical.

Report what could NOT be restored (e.g. a scratch file like `.git/COMMIT_EDITMSG`) instead of rounding the
restore up to complete.

## 3. Attribution order for an unexplained anomaly

Before blaming an external tool or a concurrent workstream, exclude the writers you dispatched:

1. **Your own lanes.** Check whether any child you spawned was running in that window and whether its
   restore/cleanup step would produce exactly the observed state. A subagent that self-reports a
   destructive mistake and a repair is the FIRST hypothesis for churn you did not cause yourself.
2. Per-file mtime against the lane's own start/end window, derived from the launcher's create time —
   never from a hand-typed epoch literal.
3. The control-plane store's own event log; sibling run directories with fresh mtimes; other live
   sessions in the runtime log.
4. Only then a third-party tool, with its own mechanism named and measured.

Two disciplines that each cost a correction: **localise a difference to ONE mechanism before writing the
conclusion** (two plausible-but-wrong explanations were published and had to be retracted — "a CLI manages
its own directory" and "a file copy cannot reproduce nested-repo dirtiness" — when the real causes were a
dispatched writer's deletion plus a lost config setting), and **state which observation supports which
mechanism**, so a later reader can re-derive it.

## 4. A recursive manifest beats a single mtime

To claim "this tree was not touched", take `relpath -> (size, mtime_ns, is_dir)` for every entry below the
root before and after, and diff the three sets (added / removed / changed). A root-directory mtime alone
cannot establish that descendants were untouched, and a reviewer will reject it. Bound the walk (entry
cap) and report whether it truncated. The same manifest pattern is the right proof for a probe that is
supposed to delete nothing (see the `destructive-path-guards` skill).
