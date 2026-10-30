# FAR synthesis — the loop had two actuators and the mandate named three

Run `FAR-HANDOFF-V1-THREE-LANE-GAP-20261030` · 2026-10-31 · Fabric contract / SBL entry / HG-KSEOS control plane

## 1. The question, answered before the reasoning

**I stop because the machine I built can write briefs and verdicts but cannot write implementations, and the only
actor that can was me, in-session — and a session ends when I stop calling tools.**

That is not a discipline failure and it is not fixable by resolving to try harder. It is a missing actuator, and
this is the measurement that proves it:

| Evidence | Value |
|---|---|
| `continuation_driver.py` prompt builders before this run | `plan_prompt`, `verify_prompt` — **no `execute_prompt`** |
| `--lane EXECUTE` occurrences in the driver | 0 |
| `--lane EXECUTE` occurrences in the whole queue (`C:/wg/queue`) | 0 |
| Lanes the mandate names | 3 |
| Lanes the loop could dispatch | 2 |

So the loop's repertoire was: *plan the card*, *judge the card*. The one thing that changes the world — writing the
artefact the officer says is missing — had no lane. Every FAIL therefore became terminal in the loop, the queue
drained to "6 remaining FAIL", and the only way forward was a new assistant turn. Each turn boundary reads to the
owner as "it stopped again", and it did.

## 2. Why six FAR runs missed it

All six studied **the artefacts or the rules**, never **the actuator set**. Their units of analysis:

| Run | Concluded | Missing |
|---|---|---|
| CONTINUATION | "the stop is a runtime property; add a queue and a cron" | added the loop but never asked what the loop can *do* |
| GOAL-AND-VISIBILITY | "todo/goal are session objects; project them" | projections of a two-actuator loop |
| VISIBILITY-CAPABILITY | freshness, windows, false dilemma | still the loop's *outputs*, not its *verbs* |
| LANE-USAGE-AUDIT | "PLAN was never dispatched" | counted PLAN, never noticed EXECUTE was also never dispatched |
| REFUSAL-AUDIT | refusals were claims | about what I said, not what the machine can do |
| ALLPASS-GAP | listed the six remaining cards | treated them as work, not as evidence of a missing verb |

The recurring blind spot has a name: **I kept auditing the product of the process and never the process's
capability set.** A process that cannot produce a category of work looks identical, from the outside, to a process
whose operator keeps forgetting.

## 3. Is it Hermes routing or HGK routing?

Neither, and the distinction matters because both were suspected:

* **Hermes routing is not defective.** All three lanes dispatch and return receipts whose asked model equals the
  served model: `--lane PLAN` → `gpt-6.1-sol` rank 1 (323.72 s, `NONCE-ECHO` present); `--lane VERIFY_SECURITY` →
  `gpt-6.1-sol` (163.65 s, `LANE_SERVED_AS_CLAIMED`); `--lane EXECUTE` → accepted just now with the EXECUTE chain's
  arm. The session plane (deepseek) versus lane plane separation held: PLAN work went out, not in.
* **HG-KSEOS routing is not defective either** — `config/lane-routing-registry.yaml` epoch 34 declares all three
  chains correctly, and `lane_evidence_gate` refuses a mismatch.
* **The defect is in the continuation graph I wrote on top of them**, which is HG-KSEOS's own layer but not its
  routing: two of three lanes wired, and `FAIL → settle → skip` logic that was correct against blind retry and
  fatal in the absence of EXECUTE.

Naming it precisely: *a routing plane with three lanes, driven by a graph with two edges.*

## 4. Second-order defect found while fixing the first

A FAIL was settled and skipped to stop the repeat-block. Correct — but combined with the missing EXECUTE edge it
made every FAIL permanent. And the repeat guard counted *receipts in the queue directory*, so archiving old receipts
(the honest thing to do) reset the count, and my own `--auto-record` change made the gate read a `PRE_ATTEMPT`
receipt that carries no attempts, producing `NO_ATTEMPT` → the driver parked at `AWAITING_RECORD` forever. Measured
at 00:48: `{"verdict": "NO_ATTEMPT", "problems": ["receipt carries no attempt"]}`.

**A phase that cannot advance must retry or refuse loudly; it may never park.** That is now enforced.

## 5. Rulings

| ID | Ruling | Implemented as |
|---|---|---|
| OD-AA1 | The loop must carry the mandate's three actuators, not two | `execute_prompt()` + `EXECUTE_READY` / `REVERIFY` phases |
| OD-AA2 | A FAIL is a specification, not a terminal state; settle only after EXECUTE rounds are exhausted | `MAX_EXECUTE_ROUNDS = 3`, then `HALTED_EXECUTE` |
| OD-AA3 | A phase that cannot advance retries with a reason or refuses loudly; never parks silently | `NO_ATTEMPT` + no verdict → re-dispatch `BRIEF_READY` |
| OD-AA4 | A paused goal is a silent criterion failure; the tick asserts it | `ops_status` prints `GOAL: <status>`; wrapper resumes and logs |
| OD-AA5 | Key material never enters git; the seed is DPAPI-bound | `.gitignore` + `config/issuer/issuer.key` ignored |
| OD-AA6 | Only `relay_daemon.py` may start the relay; a console window is a spawn-time property | `relay_daemon.py start|status|hide`; existing window hidden via `ShowWindow` |

## 6. Audit: are this session's fixes in active places?

| Fix | Where it was put | Active? | Correction |
|---|---|---|---|
| `winproc.install()` | 7 headless entry points | yes | — |
| cron wrapper: pythonw re-exec, `--auto-record`, goal resume | **profile** `scripts/hgk_continuation.py` (the file the job runs) | yes | the duplicate under `hermes/scripts/` is inert; noted, not relied on |
| driver EXECUTE phase | `HG-KSEOS/scripts/continuation_driver.py`, called by the wrapper by absolute path | yes | verified by an actual `EXECUTE` dispatch, not by reading |
| acceptance rows for re-judging | `acceptances` table (`-V3`, `-V2`) | yes | history preserved; no FAIL deleted |
| `/goal` | `state_meta goal:<session>` | **was PAUSED** | `set_goal.py resume` + tick assertion |
| issuer key | `config/issuer/issuer.key` | **untracked in a repo, no ignore** | `.gitignore` added; DPAPI at rest |
| receipts archived for a fresh phase count | `attempts/` | **broke the gate's newest-receipt input** | `NO_ATTEMPT` handling; archive no longer strands the phase |
| relay | running from `cmd /K` | **visible window, duplicate bun** | window hidden (`IsWindowVisible → False`), `relay_daemon` is now the only start path |

The pattern in the three failures: each fix was correct **in content** and wrong **about which copy is live**. That
is the same class as the six FAR runs missing the actuator — a derivative standing in for the source.

## 7. What is still not done

WP-17's officer has refused three times for three different reasons; the fourth is a capability gap, not an
authority gap: a capability probe is not a native host occupant. The EXECUTE dispatch now running is the first
attempt in this session where the loop, not the assistant, is the one answering an officer's objection. Whether it
succeeds is a fact about the model's work, not about the loop's wiring — and the loop will now carry the result
forward without me.
