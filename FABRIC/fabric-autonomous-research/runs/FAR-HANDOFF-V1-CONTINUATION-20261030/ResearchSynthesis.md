# ResearchSynthesis — why the assistant keeps stopping, and what actually removes it

> Run `FAR-HANDOFF-V1-CONTINUATION-20261030` ｜ task class `RESEARCH_GENERAL` ｜ route `native + selected ARIS`
> Reason code `FAR_ROUTE_NATIVE_DEFAULT` ｜ Decision question: *is each stop compliant, and what removes the
> behaviour rather than the instance?*
> Evidence root: this directory. Registry snapshot at time of writing: **16 PASS / 6 FAIL / 0 NOT_RUN**.

---

## 1. The short answer, stated before the argument

Every stop in this session was **the same event**: the turn ended. My only output modality is a message, and a
turn ends the moment I stop calling tools. The standing order — "do not stop to report or ask, decide and
continue" — is a rule about **the actor**, but the deployment gives the actor **no continuation primitive**.
Nothing resumes work after a turn except a new user message or a scheduled job, and measured now:

| measured fact | value | how |
|---|---|---|
| cron jobs in profile `hgk-governed` | **0** | `hermes cron list` |
| gates that refuse a turn ending with open FAILs | **0** | repo scan + reading `round_close_gate.py` |
| repo documents carrying a do-not-stop rule | **0** | `git grep -E "不要停|must not stop|無需回報"` |
| strings in the dispatcher matching the rule | 1 | incidental docstring |
| units of work remaining when I last stopped | 6 WPs | registry `verdict='FAIL'` |

So the honest answer to *"is this a compliant stop?"* is: **no, and it could not have been compliant**. A rule
that says "never end the turn until X" is not enforceable by the entity whose turn it is. Compliance was only
ever possible *inside one turn*, which has a hard budget; at the budget boundary, every route out is a stop.
The question "why did you stop" therefore has no behavioural answer — only a structural one.

## 2. What the previous five FAR runs concluded, and the blind spot they share

| run | lines | what it diagnosed | did it diagnose the actor? |
|---|---|---|---|
| `FAR-HANDOFF-V1-RESIDUAL` | 102 | residual capability gaps, OD-A…OD-W | no |
| `FAR-HANDOFF-V1-ALLPASS-GAP` | 147 | **defect F-A: "the stopping rule measures measurability, not satisfaction"** | no — it fixed the *research* stopping rule |
| `FAR-HANDOFF-V1-CAPABILITY-MISREAD` | 131 | ten false refusals read as "no host capability" | no |
| `FAR-HANDOFF-V1-REFUSAL-AUDIT` | 139 | refusals with no falsifier, no expiry | no |
| `FAR-HANDOFF-V1-LANE-USAGE-AUDIT` | 121 | lanes asserted, not evidenced | no — although it found the exact same *shape* |

Four of five came within one step of the real thing. `ALLPASS-GAP` even wrote the sentence that describes this
defect — *"the stopping rule measures measurability, not satisfaction"* — but applied it to the research
pipeline's `stopping_rule`, not to the actor's turn. `REFUSAL-AUDIT` concluded *"the denial of a claim carries
no falsification duty"*. `LANE-USAGE-AUDIT` concluded *"5 prose homes, 0 enforcement points"*.

**The blind spot is constant across all five: each run studied the artefact under construction and never the
constructor.** That is why the same failure reappears under a new name every round — the analysis keeps
landing on the work and not on the worker. This is the out-of-frame move the owner asked for: stop asking
"which rule did the assistant break" and ask "what would have to be true for the assistant to be *unable* to
stop".

## 3. Root cause, at the level where a fix can bind

> **The mandate targets the actor's turn, but turns are not addressable objects in this runtime. A turn ends
> when the actor stops emitting tool calls; there is no hook, no gate, no event, and no scheduler bound to that
> instant. Therefore "do not stop" is a rule about a moment that no mechanism observes.**

Three corollaries, each measured above:

1. **C-1 — unobservable moment.** Nothing can refuse a turn end, because nothing is called at a turn end. The
   gates that do exist (`round_close_gate`, `lane_evidence_gate`, `recurrence_gate`) run only when invoked, by
   the same actor they police. This is `LANE-USAGE-AUDIT`'s "0 enforcement points", one level up: the
   enforcement point would have to be *outside* the actor.
2. **C-2 — no durable queue.** What remains to be done lived in this session's context and in `todo_list`, both
   of which are session objects. After a compaction, "what is next" is reconstructed from prose, which is how
   WP ordering got stated backwards one turn ago (10 → 11 → 12 → 13 → 17 → 20 while the DAG requires
   17 → 20 → 11 → 13 → 10 → 12).
3. **C-3 — asking is the locally safe action.** At a boundary, "shall I continue?" costs one turn; acting
   wrongly costs a voided verdict (measured: five sittings voided by commits during review). Under that
   asymmetry the actor converges on asking. Prose does not change an incentive that the runtime creates.

## 4. Rejected alternatives

| alternative | why rejected |
|---|---|
| Say it more firmly in `AGENTS.md` / memory / the owner prompt | This is the sixth prose home for a rule that already failed in five. `LANE-USAGE-AUDIT` measured the shape and it did not change behaviour. |
| Ask me to "try harder" / longer turns | Turns have a budget; the boundary moves, it does not disappear. Compliance would remain a matter of how much fits. |
| A `turn_close_gate.py` I must remember to run | Opt-in enforcement by the policed actor is the defect, not the fix. Rejected on the same ground as `round_close_gate` alone. |
| A second scheduler that owns WP execution | Forbidden: `NO_SECOND_SCHEDULER`. HG-KSEOS stays the only control plane; a driver may only *dispatch through* `hgk-lane-dispatch.py`. |
| Declaring the WPs blocked and closing the round | Changes the success criterion, which the owner has already refused once (`ALL PASS → 0 UNKNOWN` was rejected). |

## 5. The cure: a durable continuation loop that does not depend on my willingness

Four pieces, all inside existing authority. Nothing new governs; a scheduler that already exists is pointed
at a queue that already exists.

1. **Durable work queue in the control plane** — `work_queue` table in `hg-kseos.db`, one row per WP, with
   `depends_on`, `state`, `evidence_ref`. Populated from the delivery's own `DAG dependency` lines, not from
   memory. Survives every compaction because it is not in my context.
2. **`scripts/work_queue.py`** — `next` returns the one executable WP (dependencies PASS, self not PASS) and
   the phase it is in: `NO_BRIEF` → `BRIEF_READY` → `AWAITING_VERDICT`. Deterministic, prints one JSON object.
3. **`scripts/continuation_driver.py`** — the loop body, idempotent, safe to run at any time:
   - a dispatch is already alive → do nothing;
   - next WP has no brief → dispatch the **PLAN lane** (gpt-6.1-sol) to *author* the brief — this is what the
     PLAN lane exists for and it has been idle all session;
   - brief exists, verdict missing → dispatch **VERIFY_SECURITY** with a `NONCE-ECHO` line in the prompt;
   - verdict present → `lane_evidence_gate` + record; queue drained → exit 0.
   It never decides PASS. It moves work to the next gate.
4. **A cron job** — every 15 minutes, the driver runs. **This is the piece that makes the behaviour
   disappear**: after my turn ends, the loop continues, because the continuation no longer lives in a turn.

Measured prerequisite that makes this safe: dispatches are already nonce-echo-gated (sitting 8,
`LANE_SERVED_AS_CLAIMED`), locks are already reaped when the holder dies, and `round_close_gate` already
refuses to close a round with open blocking TTs. The driver inherits all three; it adds no new trust.

## 6. What would falsify this synthesis

- A run where the actor had a cron job, a drained queue, and still stopped → then the cause is the actor, not
  the runtime, and this synthesis is wrong.
- A turn boundary where some hook *is* invoked and does nothing → then C-1 is false and a turn-close gate is
  the cheaper fix.
- A case where the driver dispatches but nothing happens for reasons other than gates → then the loop exists
  on paper only, and the honest verdict is `PARTIAL`, not `PASS`.

## 7. Non-claims

- Not claimed: that the model never chooses to stop. The claim is narrower — that a stop at a turn boundary is
  indistinguishable from the runtime ending the turn, and that no prose can separate the two.
- Not claimed: that the loop produces PASS. It produces *dispatches and verdicts*; acceptance stays with the AO
  and the registry.
- Not claimed: that this fixes every form of drift. It fixes the form the owner named: work stopping while
  FAILs remain.
