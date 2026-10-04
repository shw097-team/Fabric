# RP-002 External Challenge Profile

Use only when reviewing RP-002.

## Canonical gate graph

```text
G0 → G1 → K1 → D1 → C1 → H1 → O1 → B1 → F0 → CF1 → F1 → KG1 → SQP1 → S1 → E1 → E2 → [E3_IF_APPLICABLE] → R1
```

Do not invent alternate machine gate IDs.

## High-value external challenge checkpoints

### O1 — Internal Oracle

Challenge:
- candidate Oracle did not exist before its allowed bootstrap point;
- Oracle Core/Acceptance Pack/receipt identity is exact;
- checker isolation is fresh/read-only/no maker-memory/no candidate-write;
- candidate cannot self-promote;
- unknown subject and missing raw evidence fail closed.

### F1 — Self-hosting cutover

Challenge:
- post-cutover normal work actually uses qualified Profile+Kanban path;
- no silent fallback to bootstrap path except documented rollback/incident;
- WorkOrder remains the normative executor contract; Kanban is not a second task truth.

### E1 — Cross-stack engineering evolution

Challenge:
- defect is real or explicitly labeled fault-injection;
- old state reproduces the failure;
- smallest owner/repair is identified;
- old + new regression exists;
- promotion is atomic and evidence-bound;
- the exact original SQS task replays successfully;
- live write remains zero.

### E2 — Behavioral artifact evolution

Challenge:
- old Distribution reproduces the behavior defect;
- new SOUL/Skill/Profile/Pipeline loads in a fresh session;
- positive + negative + regression run;
- original behavior replay passes;
- rollback to prior Distribution works.

### E3 — Oracle evolution

If Oracle changed:
- old/external Meta-Oracle, not candidate Oracle, must check the new Oracle;
- evaluator changes are separately governed;
- candidate Oracle cannot approve itself.

If Oracle did not change: require `N/A_WITH_SOURCE_LOCATOR`.

### R1 — Final local acceptance

Challenge exact-subject consistency across:
- mandatory gates;
- blocking TT = 0;
- canonical Evidence Manifest;
- independent aggregate acceptance;
- package exact-set/checksums/readback;
- final report subject digest;
- no unauthorized external side effect/live broker write.

RP-002 local acceptance does not imply production autonomy, remote deployment authorization, or SQS live trading authorization.
