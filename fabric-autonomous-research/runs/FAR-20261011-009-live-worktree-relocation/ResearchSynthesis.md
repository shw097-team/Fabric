# FAR synthesis — FAR-20261011-009-live-worktree-relocation

**Decision question.** Once the lock clears, should `PIPD-postrelease-wt` be relocated into
`PIPD/worktrees/`?

**Verdict. `DEFER_TO_ROUND_CLOSE`. Do not relocate now.**

The previous record described this as *blocked*. That was the wrong frame. The lock is a **symptom**;
the reason not to act is that the three stated criteria — low resistance, upstream conformity, high
engineering necessity — **are not met**.

## What the lock actually is (reproduced, not assumed)

Renaming each immediate subdirectory (`.hgk`, `src`, `tests`) **succeeds**; renaming the **directory
node itself** fails with `Device or resource busy`. That is the signature of a live process holding the
directory as its **current working directory** — nothing inside is exclusively open. `git worktree move`,
a plain `mv`, and `pwsh Move-Item` all fail identically, so it is not a tool quirk.

The correlation is exact: of the six sibling worktrees, the **five that relocated cleanly were never a
lane `--cd` target**; this one was, because the R2 EXECUTE lanes ran
`codex exec --cd <this worktree>`. The prime suspect is therefore the
`codex-windows-sandbox-service.exe` process that was already long-lived before the lanes started. Stated
as a **suspect class, not proven attribution** — and deliberately **not** terminated to find out.

## Why the move is not justified

1. **Necessity is low.** The worktree's value is its **branch** (the open round's tip) and its
   **untracked evidence** (four lane logs + a verify log). Neither depends on where the directory sits.
   The move would buy exactly one fewer directory name at the workspace root — and the substantive
   hygiene was already achieved: the stray shadow tree under the drive root was removed, six
   out-of-workspace temporary worktrees were pruned, and five sibling worktrees were consolidated.
2. **Resistance is not cheap.** Getting past the lock means **killing a live service the owner may still
   be using**, or waiting without bound. Neither is a low-resistance operation, and neither is
   proportionate to the gain.
3. **It goes against upstream practice.** The move only became possible by threading worktrees **into**
   the repository tree and then adding a `worktrees/` ignore rule. No PIPD or Fabric rule requires
   worktrees to live inside the repo; siblings are the ordinary arrangement.
4. **It churns governance-bound paths during an open acceptance window.** This worktree is the home of
   the round whose acceptance is still pending, and its absolute path is referenced by taskspec rows and
   by the acceptance master. Relocating it mid-window trades a cosmetic improvement for edits to records
   that a reviewer has already read.

## The executed decision

Deferral is recorded as an **intentional** state with a named trigger and the exact command, so it cannot
be mistaken later for an abandoned attempt:

- **Trigger:** round close-out, or any time the holder exits (`git worktree move` succeeds).
- **Command:**
  `git -C C:/Projects/Agent_Workspace/PIPD worktree move "C:/Projects/Agent_Workspace/PIPD-postrelease-wt" "C:/Projects/Agent_Workspace/PIPD/worktrees/postrelease-wt"`
- **After moving:** add the old-to-new mapping to the migration record and update the acceptance master's
  path reference, exactly as was done for the other relocated subject.

## Non-claims

This run does **not** claim: that the lock holder was identified (it was narrowed to a suspect class);
that the move is undesirable in principle (only that it is unjustified now); that anything was moved,
deleted or killed. Independent challenge lane `NOT_RUN`.
