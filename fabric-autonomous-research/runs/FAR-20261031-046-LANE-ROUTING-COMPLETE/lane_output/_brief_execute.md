NONCE-ECHO: FAR-EXECUTE-85D6690B

# EXECUTE brief

Question:
How can FAR research actually be executed through the three mandated lanes rather than written as prose by the session model? Nine FAR runs 036-044 carry no lane receipts. Identify the structural cause and the mechanism that makes the routed path the default.

PLAN output:
I’ll read the brief and check its requested scope against the repository’s execution rules.
NONCE-ECHO: FAR-PLAN-F289CF9C

The structural cause is a bypassable workflow: session-written prose can look like completed research, while dispatching the three lanes requires extra commands. Instructions name the lanes, but only an enforced entry point and publication boundary can make their execution mandatory.

The brief reports missing receipts for runs 036–044; I have not independently audited those nine runs.

The current implementation already attempts the right mechanism: [`scripts/far_round.py`](C:/Projects/Agent_Workspace/HG-KSEOS/scripts/far_round.py) provides one command for PLAN → EXECUTE → VERIFY_SECURITY. However, inspection shows gaps that prevent treating this as a complete routed path:

- The runner creates flattened receipts without `attempts`; `far_lane_gate.py` passes those receipts to `lane_evidence_gate.py`, which requires nonempty `attempts`.
- `served_arm` is initialized from the requested arm rather than derived from successful dispatch evidence.
- Routing and transport are hardcoded instead of resolved from the canonical registry.
- Arbitrary `--lanes` selections can reach `LANES_SERVED`; that status does not prove all three mandated lanes ran.
- VERIFY receives the EXECUTE prose under a “PLAN output” heading. The checker should instead receive the frozen question, preregistered criteria, candidate artifacts, and raw evidence, without the writer’s summary.
- The runner does not itself enforce publication admission. Making dispatch convenient does not prevent a separate path from publishing prose.

For the routed path to become the default, these conditions must hold:

1. **One normal research entry point.** FAR creation and continuation invoke the runner automatically.
2. **Evidence-bound handoffs.** Each lane consumes identified inputs and produces an output bound to its run, nonce, subject, and complete dispatch receipt.
3. **Mandatory validation before advancement.** Check the actual served attempt, canonical provider/model identity, permitted rank, agent-message nonce, usage evidence, and successful completion. Missing evidence stops the round.
4. **Enforced publication admission.** Every publishing or downstream consumption path requires validated evidence for all three lanes. A directory or synthesis file alone remains unpublished candidate material.
5. **Independent checking.** VERIFY runs in a separate process against frozen artifacts. Successful dispatch proves lane service; it does not prove research correctness or canonical acceptance.

EXECUTE should build **one work package: complete the runner-to-admission contract**. Retain full dispatcher receipts, resolve routing through the existing canonical machinery, validate each handoff, supply artifact-based checker inputs, and connect the resulting gate to the actual publication boundary. Avoid creating another routing registry or acceptance authority.

Deterministic tests should cover a complete successful chain and otherwise-valid cases with a missing lane, wrong provider/model, nonce found only in prompt text, absent usage, stale receipt, changed subject, provisional completion, subset lane selection, and direct publication bypass. An independent checker must rederive the results. Rollback must preserve failed-run evidence and leave publication closed.

This response is planning content. Its PLAN-lane provenance must be established by the enclosing dispatcher’s completed receipt; the response cannot certify itself.

Build exactly one work package from the plan. Keep it small enough to finish. Report what you changed and why.

Begin your reply with the nonce line exactly as given above, verbatim.
