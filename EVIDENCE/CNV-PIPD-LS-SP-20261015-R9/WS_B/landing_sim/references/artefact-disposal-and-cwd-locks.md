# Disposing of redundant clones / checkouts, and the cwd-pinned lock

Use before deleting a clone, stale checkout or worktree as "workspace hygiene". A disposal is a
destructive act; what makes it defensible is the probe set and the recorded output, not the tidiness.

## The three-probe uniqueness test (run all three, keep the raw output)

```bash
# P1. is every ref target present in the parent repo's object DB?
for o in $(git -C "$CLONE" for-each-ref --format="%(objectname)" refs/heads refs/remotes | sort -u); do
  git -C "$PARENT" cat-file -e "$o" 2>/dev/null || echo "MISSING_IN_PARENT $o"
done

# P2. clean tree, no stashes, no untracked files?
git -C "$CLONE" status --porcelain | wc -l
git -C "$CLONE" stash list | wc -l

# P3. is a clone-only BRANCH NAME backed by a commit reachable in the parent?
git -C "$PARENT" branch -a --contains <sha-of-the-clone-only-branch-tip>
```

**The trap P3 catches.** A missing *branch name* in the parent proves nothing — the parent may lack a ref
called `foo-successor` while still containing and reaching the commit it points at. Test the **commit's
reachability**, not the label's presence. A commit that is an ancestor of live work is **not** orphaned by
deleting the clone.

Also record, before removal: the clone's `remote -v` (a *local* origin means the clone is not a publication
boundary), its size, and an independent preservation site (e.g. the upstream still serving the branch).
"Zero unique content, two preservation sites, clean tree" is a decision. "It looks redundant" is a guess.

**Reversibility sentence worth writing down:** a clone of a *local* repo is reconstructible with
`git clone <local-path>` — no network and no credential required.

## The cwd-pinned lock: symptom vs reason

If a directory **cannot be renamed** but its **immediate subdirectories can**, the lock is on the
**directory node**, not on any file inside it — some process holds it as its **current working directory**.
`git worktree move`, plain `mv` and `Move-Item` then fail identically, which rules out a tool quirk. The
correlation to check first is **which of your own lanes was given that directory** (`--cd`, or a
shell cwd): a long-lived sandbox/service process started for a lane will pin it until it exits.

Two rules follow:

1. **Diagnose the symptom, but decide on necessity.** Clearing such a lock means killing a live process or
   waiting without bound. Before paying that, ask what the artefact's value depends on. It is usually the
   **branch** and the **uncommitted evidence**, neither of which depends on the directory's location — so
   relocation buys only cosmetics. Defer to a natural boundary (round close-out) and record the deferral
   as a **decision with a trigger and the exact command**. Never record it as "blocked": that reads as an
   abandoned attempt at a wanted outcome and hides that a choice was made.
2. **Never kill a process to find out whose it is.** Narrow it to a suspect class, state it as a suspicion
   rather than a fact, and leave it running.

## Order of operations that held up

probes → record raw output → record remotes/size/preservation sites → re-run the probes immediately before
removal (a second, fresh pass) → remove → verify the parent's object DB still resolves the branch tip →
record reclaimed size → update the old→new map and any artefact that named the removed path.
