# Gate Calibration Contract

Run every applicable row. A missing required calibration edge blocks only the affected claim and must remain visible.

| Calibration edge | Challenge question | Required evidence |
|---|---|---|
| Objective alignment | Does the gate test the frozen acceptance objective rather than an implementation proxy? | acceptance ID to oracle mapping |
| Risk proportionality | Is strictness commensurate with impact and reversibility? | risk class and rationale |
| Positive coverage | Can a valid subject pass for the intended reason? | normal fixture/result |
| Negative coverage | Does a known invalid subject fail? | negative fixture/result |
| Adversarial coverage | Does a bypass, injection, poison, or stale-binding mutation fail? | adversarial fixture/result |
| False positive | Can a proxy, summary, file presence, or hidden failure incorrectly pass? | destructive mutation |
| False negative | Can a conforming candidate be rejected by brittle or irrelevant criteria? | conforming counterfixture |
| Regression | Are previously accepted neighboring behaviors rechecked? | baseline and affected regression result |
| Judge disagreement | Do deterministic and semantic judges diverge? | per-judge result and disputed predicate |
| Anti-overfitting | Was the evaluator changed to fit the candidate or exposed to the candidate solution? | evaluator diff and isolation evidence |
| Domain/HITL | Does frozen acceptance require a domain owner or Human decision? | authorized identity and scoped decision |

Do not repair the gate inside the candidate review. A suspected gate defect is `ORACLE_DISAGREEMENT` or `EVIDENCE_GAP` and routes through governed adjudication.
