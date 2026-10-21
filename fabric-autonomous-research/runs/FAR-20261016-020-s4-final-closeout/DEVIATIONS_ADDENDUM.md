# FAR-20261016-020 — Deviations addendum (complete list)

This addendum exists because the run's `VERDICT.json` was written before the round closed; it carries the
complete deviation list so a reader does not have to reconcile two files.

| ID | What deviated | Found by | Fix | Class lesson |
|---|---|---|---|---|
| `DEV-S4F-01` | My own comparison compared a sorted API list against an **unsorted** expectation list, producing a false `FAIL` on `pr18_paths_exact`. | My own re-read of the JSON (the frozen values were the contract's, mine were derived). | Sort both sides; re-ran the readback → 13/13 matched. | A false FAIL from your own tooling looks exactly like a product defect. Sort both sides before asserting set equality. |
| `DEV-S4F-02` | `check_write_set.py` reads the workflow **from the current checkout**, so running it on main's tree mis-failed PR #18 for `docs/USER_GUIDE.md` — the candidate itself amends that allowlist. | Reading the classifier's own body source. | `git worktree add --detach` at the subject's head → `PASS (changed=27 excluded=0, 0 frozen, 0 outside)`. | When a candidate modifies the gate that judges it, the gate must be read from the candidate's own tree. |
| `DEV-S4F-03` | SWARM lane 2 died with `HTTP 429` (provider usage limit) after 121 s. | Async failure notice. | Immediate declared fallback to a deterministic script (no model in the loop); identical result, recorded in the artifacts. | Every extractable readback needs a model-free route, and a 429 converts to it at once instead of being retried. |
| `DEV-S4F-04` | I assumed a branch push would run CI; the workflow triggers on `pull_request` and `workflow_dispatch` only. | Reading the workflow `on:` block. | No CI is claimed for the evidence branch; the write-set classifier is run locally instead. | Attribute CI to run id + head sha, never to "our push". |
| `DEV-S4F-05` | The first manifest was computed from round-root copies, so 2 of 12 rows mismatched the committed blobs after git normalised CRLF→LF (`* text=auto eol=lf`). | The fresh-extract self-check: 10 matched / **2 DIGEST_MISMATCH**. | Recompute the manifest from the `git archive` extraction, record both digests under `byte_normalization`, new commit, re-verified **12/12**. | Manifests must describe the shipped bytes; receipts are the likeliest CRLF carriers. |
| `DEV-S4F-06` | Completed the board with three wrong task-id literals. | KANBAN's own refusal. | Re-ran with the board's real ids → 8/8 done. | Read ids from the board, not from memory. |
| `DEV-S4F-07` | All three SWARM lanes died on `HTTP 429` — they were running `gpt-6.1-sol` because `delegation.provider/model` still pinned `openai-codex`/`gpt-6.1-sol`. The owner's 2026-10-16 lane order (GPT → DeepSeek) had been applied to the PLAN, EXECUTE and VERIFY lanes but **not** to delegation, so subagents kept burning the quota the owner was trying to leave. | The batch failure notice, which names the model and says "rate-limited every one of 3 attempts ... resets in ~52 min". | `delegation.provider=opencode-go`, `delegation.model=deepseek-v4.1-flash` via `main.py config set`; **proved** by a one-command smoke lane that completed on `deepseek-v4.1-flash` in 5.2 s (the GPT lanes had died at 121 s and 153 s) and independently reported the same tip this round recorded. | A lane switch is not finished until it covers every spawn path; delegation inherits its own provider/model and will silently stay on the old model. |

## Standing self-iteration points

1. Sort both sides of every comparison before asserting equality.
2. Keep a deterministic, model-free route for anything extractable; convert on the first 429.
3. Run the subject's own gate in a worktree at the subject's head, never in an ambient checkout.
4. Recompute the manifest from the shipped commit and re-run extract-and-verify after **every** added file.
5. Claim CI only with a run id and a head sha; check the workflow's triggers before assuming a push ran it.
6. A model/lane switch must cover **every spawn path** — session model, governed profile, and `delegation.provider/model` — or subagents keep consuming the quota you switched away from.
7. Before freezing an artifact, confirm no background writer is still alive, and judge consistency tri-way (working copy vs committed blob vs manifest), never from the working copy alone.
