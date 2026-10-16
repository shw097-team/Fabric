# Tasks — hgk-far-remediation-20261016

## Admission and orchestration

- [ ] 1. Typed HGK admission for this round (requirement FROZEN, TaskSpec ADMITTED, WorkOrder per role)
- [ ] 2. WorkOrder created for each canonical change: R1, R2, R5
- [ ] 3. KANBAN board + SWARM graph recorded with the root, workers, verifier and synthesizer ids
- [ ] 4. This change validated `--strict` by the project CLI before execution

## R1 / R3 — registry ruling

- [ ] 5. Back up `config/lane-routing-registry.yaml`; record its sha256 before the change
- [ ] 6. Rebind `routes[].PLAN` to `openai-codex/gpt-6.1-sol` medium OAuth with the in-force order as its
      `selection_authority`
- [ ] 7. Replace the stale `usable_now: QUOTA_429_2026-10-15` marker with this session's measurement,
      keeping the 429 as a dated prior-revision note rather than deleting the history
- [ ] 8. Set `admission_status` from this session's measurement rather than leaving `UNPROVEN`
- [ ] 9. Reclassify `declared_conflicts[SOD006-C2]` to `OWNER_ORDERED_IN_FORCE` and record the remaining
      independence (process / lane / evidence path)
- [ ] 10. Advance registry `epoch` 20 -> 21 and record the reason in the provenance block
- [ ] 11. Record sha256 after the change; prove `check_drift` reports no fatal item

## R2 — promotion

- [ ] 12. Take the PROMOTE set from the measured candidate-vs-canonical diff, not from memory
- [ ] 13. Apply each file with a backup and a before/after digest
- [ ] 14. Prove each promoted file equals the frozen candidate's digest byte for byte
- [ ] 15. Prove nothing round-local was promoted into the canonical tree

## R5 — turn shape

- [ ] 16. EXECUTE lane, EDIT-ONLY turn: implement `--turn-shape {normal,edit_only}` additively
- [ ] 17. Require a typed RED-first test module for the new flag
- [ ] 18. Prove the default path is behaviourally unchanged (an existing invocation's receipt compares)
- [ ] 19. Apply the lane's product to canonical only after the orchestrator re-derives it

## Verification, closure and publication

- [ ] 20. Re-derive the full detection list D01..D16 orchestrator-side
- [ ] 21. Freeze the subject and have the independent VERIFY/SECURITY lane challenge it
- [ ] 22. Record the checker's verdict verbatim, agreeing or not
- [ ] 23. Write the closure JSON, README and the handover checkpoint, with the surviving residuals
- [ ] 24. Gate the packet, publish it, and read the remote back by digest
- [ ] 25. Record the self-research / self-learning / self-iteration / self-evolution note

## Claim ceiling

A checked box is a claim until the detection list re-derives it. Items marked done without a re-derived
observation are to be reported as unverified rather than as complete.
