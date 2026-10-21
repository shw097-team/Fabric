# Tasks — FAR lane/model declaration remediation (epoch 23)

- [ ] 1.1 Apply P0/P1/P2 declaration alignment via `var/FAR-REMEDIATION-20261021/apply_far_remediation.py --apply`
- [ ] 1.2 Verify `check_drift` returns `[]` and the owner-chain test is green
- [ ] 1.3 Declare `SOD006-C4 OPEN_OWNER_ORDERED` and supersede `SOD006-C3`
- [ ] 2.1 Toolchain pin names the installed 0.163.0-alpha.10.2 build with measured sha256
- [ ] 2.2 Hermes `model.codex_bin` unified to the same binary
- [ ] 3.1 Pool rank/role labels agree with rank order for all three lanes
- [ ] 3.2 In-Hermes PLAN-plane profile binds `openai-codex/gpt-6.1-sol`
- [ ] 4.1 Run the self-check harness and the bounded repair loop to green
- [ ] 4.2 Independent AO lane (gpt-6.1-sol, read-only) re-derives every gate claim
- [ ] 5.1 Bring the four routing files under git (local commit, no remote)
- [ ] 5.2 Fresh-session PLAN default verified from the profile's own state.db row
