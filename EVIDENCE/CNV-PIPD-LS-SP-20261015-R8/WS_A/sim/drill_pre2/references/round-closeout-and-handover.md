# Closing a round, and pausing one

The round is not over when the verdict lands. Close it so a future session can verify the ending
without re-deriving it, and so a pause costs nothing.

## Close-out checklist

1. **Stop the tree before hashing anything.** Confirm no lane is still running (process count for the
   writer binary plus each lane log no longer growing) and only then hash subjects. A hash taken
   while a writer is live is evidence about nothing.
2. **Write the round closure doc** at `var/<round>/closure/<ROUND>_EVIDENCE.md`, carrying in this
   order: a header table (round, admission id + FROZEN state, checker nonce, **verdict**,
   `is_acceptance`, `sod_axis_model`, claim ceiling, **what it supersedes**); the defect table with
   the **how I re-derived it myself** column; what the checker could NOT check; residual
   limitations; security events; side effects; open items; the claim ceiling restated last. Never
   write acceptance or completion into it.
3. **Mirror byte-identically to the review roots — discover them, never remember them.** Search the
   workspace for an already-mirrored doc from a previous round and reuse the exact directories it
   lives in; a remembered list will be incomplete. For HG-KSEOS the three are
   `HG-KSEOS/evidence/review/`, `Fabric/evidence/review/`, `HGK/evidence/review/` — the third is the
   one that gets missed. After copying, `sha256sum` every copy plus the origin and require **one
   identical hash across all of them**.
4. **Additive-only rule.** Once a doc is mirrored, never edit it in place — editing one copy diverges
   the others and silently invalidates the freeze. Facts that arrive later (typically a verdict that
   landed after the close-out was written) go in a **new addendum file** beside it whose first line
   states it does not modify the close-out. Re-hash the mirrored originals and confirm they still
   match their recorded value before declaring the round closed.
5. **Record the checkpoint through the typed API, never by SQL:**
   `PYTHONPATH=src python -m hg_kseos project checkpoint <project_id>`. It prints a `checkpoint_id`
   of the form `CK-<project-suffix>-<HEX8>` and writes a `checkpoints` row plus `last_checkpoint_id`
   and an `intent_json` sidecar; it does **not** advance state. Read it back: newest `checkpoints`
   row, `project_lifecycles.last_checkpoint_id`, project state (unchanged), table count (unchanged).
   A checkpoint row you did not create can appear when other sessions are live — attribute yours by
   id and **disclose the foreign one** rather than claiming it.
6. **Superseded kanban cards.** For work that was superseded rather than satisfied, `comment` the
   reason then `complete` with an explicit `--summary`: `SUPERSEDED, NOT SATISFIED — <what replaced
   it>`. The CLI refuses a completion with no summary, so use it. A card closed silently reads to the
   next session as satisfied verification. (The Hermes kanban CLI needs `HERMES_HOME` exported and is
   run as `python hermes_cli/main.py kanban --board <board> ...` from the source dir.)

## Pause / handover (owner asks to stop or shut down)

Write **one self-sufficient checkpoint file**, mirror it byte-identically, and add a one-line memory
pointer to its path: `var/<round>/_CHECKPOINT_RESUME.md` + `_handover/CHECKPOINT_<round>.md`. Order its
sections so the next session can act with no re-derivation:

1. state line — nothing running, no pending capture;
2. the verdict / claim-ceiling table **re-read from disk**, not from memory;
3. what is NOT done, as an executable numbered list with the actual commands;
4. security events and what was already done about them;
5. open items that are deliberate rather than unfinished;
6. the evidence index (verdict JSON, checker narrative, receipts, index files);
7. the round's full side effects (host settings, repo paths, git actions, credential requests,
   windows opened, DB changes).

Stop the tree first, then verify: no lane processes, both copies hash equal. On resume, read the
checkpoint **and** the repo's `AGENTS.md` before writing anything, re-read the verdict from disk, then
mark the file `RESUME COMPLETED`, re-mirror, and confirm the re-mirrored hash.

## Secret handling in round artifacts

- A lane that dumps its own environment writes the provider key into its log. If the launcher passes
  the **real** provider key to children as `OPENAI_API_KEY`, every lane is a leak site — report the
  structural fix (a scoped/ephemeral relay key) to the owner rather than only cleaning up.
- Redaction sweep: read the env value into a variable, scan every file you own for that literal,
  replace with `[REDACTED]`, then **re-scan and report 0 occurrences**. Never print the value or even
  a prefix of it. Scope the walk to your own round directories with `os.walk(..., onerror=...)` — a
  whole-tree walk of a shared `var/` trips over other sessions' locked files and vanished directories
  and aborts before it verifies anything.
- Disclose the redaction as a side effect of the round: you changed the bytes of a frozen artifact.
