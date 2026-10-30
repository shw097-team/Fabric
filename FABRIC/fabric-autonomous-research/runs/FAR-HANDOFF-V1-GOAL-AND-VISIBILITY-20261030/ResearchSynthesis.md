# ResearchSynthesis — the todo/goal that keeps closing, and the status nobody can see

> Run `FAR-HANDOFF-V1-GOAL-AND-VISIBILITY-20261030` ｜ `RESEARCH_GENERAL` ｜ route `native + selected ARIS`
> Reason code `FAR_ROUTE_NATIVE_DEFAULT`
> Two owner questions: (1) why do `todo_list` + `/goal` keep being closed, and how is opening them *forced*;
> (2) why did I report a running task the owner could not see, and how does a running task become visible
> without asking anyone.

---

## 1. Question 1 — the todo list and the goal keep closing

### What actually happened, mechanically

| event | mechanism |
|---|---|
| the list vanished between turns | `todo_list` state is a **session object**; a compaction or a new session erases it |
| items disappeared while the session lived | I called `todo_list` with `merge: false`, which **replaces the whole list**; twice this dropped items I had not finished |
| the goal could not be re-asserted by me | `hermes goal` is not a CLI command; `/goal` is a desktop slash command, so the assistant cannot invoke it — I substituted `hermes kanban create --goal`, which creates an anchor card but is **not** the same object the interface shows |
| nothing noticed the loss | no gate, cron or hook checks whether a goal or todo exists |

So the answer to *"is it a missing locked route, or is your self-assessment unclear?"* is **neither**:

> The todo list and the goal were **session objects being asked to do a control-plane job.** Anything that must
> survive a turn boundary cannot live in a turn. I kept re-creating them from memory, and memory is exactly what
> a compaction truncates.

That is the third instance tonight of one root cause: *state that must persist was stored in the layer that is
guaranteed to be discarded* (the round's remaining work → the queue; the review's subject → a snapshot; the
goal/todo → now a projection).

### The cure, and why it is forced rather than promised

`scripts/ops_status.py`, run by the cron wrapper **before** anything else every 15 minutes, writes from
`hg-kseos.db`:

- `C:/wg/queue/GOAL.json` — objective, `locked: true`, `derived_from: work_queue + acceptances`, current running set
- `C:/wg/queue/TODO.md` — the 22 WPs with `[x]` / `[!]` / `[ ]`, generated from the queue
- `C:/wg/queue/STATUS.json` / `STATUS.md` — what is running right now

Because these are **derived from the control plane**, they cannot drift from it, cannot be forgotten, and exist
even when no model is running. The interface's todo and the assistant's todo are no longer two copies of a
memory; one is a view of the other's source.

## 2. Question 2 — a task was reported running that the owner could not see

### What was true, and what I got wrong

- 23:04:07 — a VERIFY dispatch for WP-FHS-11 started. I reported it. **That was true.**
- 23:07:25 — it ended. The receipt says `ok: false`, `ERR_CHECKER_MUTATED_SUBJECT`, `changed=2`: **my own edits
  to `scripts/` while the officer was reading voided the verdict.** `review_lock` blocks commits, not file writes.
- The officer had written `officer/verdict.json` = **FAIL / NOT_RUN / `HOST_SP_MATRIX_INCOMPLETE`** ("all three
  archives and all nine native lifecycle cells absent"). The driver only looked for `<queue>/verdict.json`, so it
  believed no verdict existed and would have re-dispatched the same unit **every 15 minutes, forever**.
- Between 23:07 and 23:10 nothing ran at all — so the owner's "I see nothing running" was correct, and my earlier
  "a VERIFY is in flight" was stale rather than false.

### Three defects, all measured, all now fixed

| # | defect | symptom | fix |
|---|---|---|---|
| V-1 | status derived from a `text=True` subprocess on a **cp950 console** | `UnicodeDecodeError` killed the reader thread → the snapshot reported `running: 0` **while a dispatch was live** | decode bytes with `errors="replace"`; a query failure now reports `STATUS_QUERY_FAILED`, never "idle" |
| V-2 | driver's phase keyed on `<queue>/verdict.json` only | officer wrote `officer/verdict.json` → phase never advanced → re-dispatch loop | search the tree (`rglob`), never assume the path |
| V-3 | no way to move past a FAIL | WP-FHS-11 failed and stayed "next" forever | `work_queue.py settle` records the FAIL with its evidence and `next` skips settled units, listing them as `settled_failures` |

### The cure for visibility

- `STATUS.md` — ten readable lines: **RUNNING: n** or **IDLE**, per-WP brief/verdict/artefact/last-receipt table.
- `STATUS.json` — the same for machines.
- **A Kanban card per live dispatch** on board `fhs-msc-allpass-20261030`, so the desktop board shows the round
  without running a command. Measured: `running: 1` → `Created t_d132f357`.
- The cron rewrites all three every 15 minutes, and immediately before dispatching.

## 3. The pattern behind all four rounds of tonight

| round | the state that was stored in the wrong layer | the layer it belonged in |
|---|---|---|
| continuation | remaining work → session context | `work_queue` in the control plane |
| review integrity | guarded subject → the live working tree | a frozen snapshot |
| goal / todo | the objective → a session object | a projection of the queue |
| visibility | "is it running" → a sentence in a transcript | `STATUS.json` + board cards |

**One sentence:** every failure tonight was a durable fact kept in a disposable place. The fixes are all the
same move — write the fact where a compaction cannot reach it, and derive the disposable views from it.

## 4. What would falsify this

- A turn where `GOAL.json`/`TODO.md` are stale while the queue moved → the projection is not being regenerated.
- A live dispatch that `STATUS.json` calls idle after the encoding fix → the visibility cure is not real.
- A FAIL that `next` returns again after `settle` → the repeat-block prevention is not working.

## 5. Non-claims

- `GOAL.json` is a projection, not an authority: it cannot authorize anything, and `/goal` in the desktop remains
  the owner's own control which I cannot set.
- The board card is visibility, not admission. It never implies a WP passed.
- WP-FHS-11 is **FAIL**, settled with the officer's own reason. It is not "pending" and it is not "in progress".
