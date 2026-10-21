# FAR-20261016-020 — Learning record (self-learning / self-iteration / self-evolution)

Governed by Fabric + HG-KSEOS. Only lessons that survive the round are admitted here; round narration
is deliberately excluded.

## Promoted lessons (durable, reusable)

| # | Lesson | Why it is durable | Where it now lives |
|---|---|---|---|
| L1 | **Judge a candidate's self-modifying gate in a tree at the candidate's own head.** A classifier that reads a declaration out of the ambient checkout will flag the candidate's own legitimate widening as a violation. | It converts a forbidden repair round into a one-command check, and the failure mode is silent: it looks exactly like a real product violation. | skill `adversarial-verification-rounds` → `references/closeout-round-verification.md` |
| L2 | **Attribute CI to a run id plus head SHA, never to "our push".** Check the workflow's `on:` block before asserting any CI for a branch. | Claim attribution is the failure that survives an audit; a push that triggers nothing is not a red or green anything. | same reference |
| L3 | **Every extractable readback keeps a model-free route.** When a lane dies (429, timeout), switch to the deterministic script immediately, keep going, and record the substitution inside the artefact. | Provider quota is an availability property of the orchestrator, not a property of the subject; the subject must not inherit it. | same reference |
| L4 | **Freeze the STOP RULE first.** On a closeout round, search the counterexamples before writing any plan that contains a repair step. | Prevents the highest-cost error available to an over-eager round: repairing a surface the governing review already closed. | same reference |
| L5 | **A closeout's denominator set is evidence, so it is published raw and unreconciled** — and a denominator that was *not* re-executed this round is labelled as history, not presented as current. | Keeps the round from manufacturing a measurement it did not take. | same reference |

## Not promoted (kept as round history only)

- The four specific hashes and the branch tip belong in the packet, not in memory or a skill.
- The 429 incident itself is an availability event; only its *handling* became L3.
- `DEV-S4F-01` (unsorted comparison in my own script) is an instance of a class already covered by the
  existing "repair the class, not the instance" reference; it is recorded in the packet rather than
  promoted separately.

## Iteration, concretely

This round iterated **twice on its own tooling** before producing evidence: the readback script was
fixed and re-run after it produced a false negative-equivalent (a false FAIL on its own comparison), and
the write-set classifier was re-run in a different tree after its first result was shown to be a
method artefact rather than a product defect. Both iterations were disclosed in the published packet
rather than only in the session transcript.

## Evolution delta proposed to the governance stack

| Proposal | Scope | Why |
|---|---|---|
| Make the write-set classifier take the subject tree as an explicit argument (or default to reading the workflow from `<head>:path` instead of the working tree) | one tool, one parameter | removes L1's whole failure class instead of relying on the operator to remember |
| Have round templates carry an explicit `ci_attribution` field (run id + head SHA, or `NO_RUN_TRIGGERED`) | template + packet schema | makes L2 structural rather than a discipline |
| Require oracle/deterministic fallbacks to be *named in the plan* before dispatch | planning template | makes L3 a designed property, not an improvisation |

These are proposals to the owning stack; nothing in the governance stack was modified by this round.
