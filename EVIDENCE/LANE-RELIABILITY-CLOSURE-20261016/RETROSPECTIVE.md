# RETROSPECTIVE — LANE-RELIABILITY-CLOSURE-20261016

Self-research, self-learning, self-iteration, self-evolution over this round's own conduct, under the
Fabric / HG-KSEOS contract. **Everything here is candidate-only: these are PROPOSALS, not adoptions.**
No agent may authorise a change to the round contract; the gates below exist so the owner can accept or
reject each one cheaply.

## 1. 自研究 — what the measurements actually revealed

1. **The lane turn has two budgets, and only one of them is bounded.** Editing is bounded by the brief;
   command execution is unbounded (a test runner, a process enumeration, anything that can open stdin).
   Evidence: two EXECUTE turns wedged at 900 s *after* writing their first file; the identical change set
   with test-running removed completed in **74 s**. The failure mode is therefore attributable to turn
   *shape*, and the receipts prove it is not attributable to the arm — both wedged turns show
   `required_arm == served_arm` with a matching usage receipt.
2. **The strongest evidence a candidate-only round can produce is a contrast, not a pass.** The same
   three fixtures returned `exit 3` on the canonical root and `exit 0 /
   no-session-id-unattributable` on the candidate root. A candidate-only detection list would have
   reported a pass with nothing to compare against.
3. **Independent verification has a measurable ceiling and it is not "agreement".** The V2 checker
   confirmed both change sets — *and* volunteered the limit: *"these are declaration checks, not proof
   of actual backend effort."* The round's model selection is proven at the *declaration and transport*
   layer (arm served, usage receipt matched, role identity gate passed) and **not** at the layer of what
   the backend actually did with the tokens.
4. **A contradictory brief produces UNCERTAIN, and that is information about the brief.** The V1 checker
   refused to fabricate a result it was forbidden to produce. The round's own authoring defect was found
   by the lane's refusal, not by any self-review.

## 2. 自學習 — the rules extracted, and where they now live

| rule | recorded in |
|---|---|
| Take the oracle out of the writer turn: edit-only turns, orchestrator owns RED/GREEN | `hgk-kanban-and-lane-routing/references/bounded-writer-turn-shaping.md` |
| Scope a verification brief's writes to the checker's own work dir; never ban what you require; UNCERTAIN means fix the brief | `…/references/checker-brief-write-scope.md` |
| Run one detection list at both roots, annotate root-dependent expectations, never rewrite a raw status | `…/references/detection-list-across-two-roots.md` |
| Gate a packet before publishing; verify the remote by blob sha, not by push output | `remote-repo-publication/references/packet-publication-gate.md` |
| Terminate a wedged attempt only on measurement, and leave a `TERMINATION.json` | `…/references/lane-stall-triage.md`, `…/bounded-writer-turn-shaping.md` |

These are placements into existing topic files where the topic already existed; nothing was duplicated
into a new file for its own sake.

## 3. 自迭代 — numbered proposals for the next round

1. **Adopt edit-only as the default shape for EXECUTE turns, with the oracle orchestrator-side.**
   Trigger: any brief whose change set needs verification. Cost: the lane's receipt will not contain a
   GREEN; the orchestrator's detection list must therefore be treated as the primary oracle — which is
   the separation-of-duties direction anyway.
2. **Add a brief-lint step to the round's own admission chain.** Trigger: before any lane dispatch.
   Test: does the brief forbid a capability it also requires? Would a correct reader be forced into
   UNCERTAIN? Cost: minutes; it would have saved a 413 s checker turn.
3. **Make the two-root detection list mandatory for candidate-only rounds.** Trigger: any round with a
   candidate/canonical split. Cost: one extra suite run; buys the before/after contrast.
4. **Add a `TERMINATION.json` requirement to the runner itself**, so an orchestrator-stopped attempt
   always leaves a machine-readable reason instead of relying on the operator to write one.
5. **Price F1 (the PLAN route outlier) as a bounded rebind task** with its own WorkOrder, so it stops
   being carried as an open residual into every round.
6. **Record, per round, which lane shape was used and how many attempts it took** — this round's
   `3 EXECUTE attempts, 1 success` is a datum worth tracking as a trend rather than a one-off note.

## 4. 自進化 — what should become standing, and what must not

- **Should become standing (owner authorisation required):** proposals 1, 2 and 4 are shape-and-record
  changes to the round contract itself. They make future rounds cheaper and more honest without changing
  what is accepted by whom.
- **Must NOT be inferred from this round:** that the lanes are *reliable* in general. The claim this
  round can support is: **each of the three arms was served and identity-matched, in the attempts that
  completed**, on this host, in this session. One successful EXECUTE turn and two completed VERIFY
  attempts is a small sample, and the sample is stated as a count rather than smoothed.
- **Must not change:** the promotion gate. This round deliberately did not promote its own candidate,
  even though its own door (proposal 1) made promotion cheap. An agent that can widen its own authority
  because its work looked good has no separation of duties left.

## 5. Claim ceiling for this retrospective

A self-assessment by the same party that did the work. It is evidence *about the process*, subject to
the same rule as everything else in this packet: **CANDIDATE_ONLY, not accepted, not promoted.**
