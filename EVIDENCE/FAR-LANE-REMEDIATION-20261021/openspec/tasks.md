# Tasks — FAR lane/model declaration remediation (epoch 23 -> 24)

- [x] 1.1 Apply P0/P1/P2 declaration alignment via `var/FAR-REMEDIATION-20261021/apply_far_remediation.py --apply` (receipt: `var/FAR-REMEDIATION-20261021/apply_receipt.json`; local commit `c442f07`)
- [x] 1.2 Verify `check_drift` returns `[]` and the owner-chain test is green (receipt: `var/FAR-REMEDIATION-20261021/selfcheck_receipt.json`, GATE_PASS 18/18; pytest 3 passed / 90 subtests)
- [x] 1.3 Declare `SOD006-C4 OPEN_OWNER_ORDERED` and supersede `SOD006-C3` (registry `sod_invariants.declared_conflicts`; assignment `sod_conflicts`)
- [x] 2.1 Toolchain pin names the installed 0.163.0-alpha.10.2 build with measured sha256 (sha256 f6dbf48c…, verified by `codex --version` and by digest recomputation)
- [x] 2.2 Hermes `model.codex_bin` unified to the same binary
- [x] 3.1 Pool rank/role labels agree with rank order for all three lanes
- [x] 3.2 In-Hermes PLAN-plane profile binds `openai-codex/gpt-6.1-sol` (fresh-session one-shot served gpt-6.1-sol via openai-codex)
- [x] 4.1 Run the self-check harness and the bounded repair loop to green (GATE_PASS 18/18)
- [x] 4.2 Independent AO lane (gpt-6.1-sol, Codex CLI) re-derives every gate claim — OBTAINED in round `FAR-CLOSURE-20261021-R2` after the transport-vocabulary repair (G8): VERDICT PASS, 10/10 claims, receipt `var/FAR-CLOSURE-20261021-R2/probes/VERIFY_acceptance.json`; the non-mutation guard recorded 520/520 governed files unchanged (verdict CLEAN). Ceiling: the AO receipt itself states a pass is not an acceptance of any subject; local green is not release.
- [x] 5.1 Bring the four routing files under git (local commit `c442f07`, no remote action)
- [x] 5.2 Fresh-session PLAN default verified from the profile's own state.db row (row: model=gpt-6.1-sol, billing_provider=openai-codex, source=oneshot)

## Round `FAR-CLOSURE-20261021-R2` — closure of the measured residual gaps (epoch 24)

- [x] 6.1 F1: align `sod.verify_security_arm_A` to `lane_chains.VERIFY_SECURITY[0]` (a cross-field
  contradiction `check_drift()` cannot see) and add the named gate `C15_crossfield_arm_A`
  (receipt `var/FAR-CLOSURE-20261021/apply_receipt.json`; local commit `5d63e00`)
- [x] 6.2 F2/F3/F4: stop the registry's internal residue — `authorization_basis` (revision 17),
  `selected_arm_identity` (deepseek-v4.1-flash), and the projection note (revision 22 / PLAN=glm)
- [x] 6.3 F5: label the measured PROBE arm as `PROBE/探測` with `automatic_selection: false` and add the
  named gate `C16_probe_not_auto` — a measurement arm must never read as a policy default
- [x] 6.4 F6/F7: reconcile the checklist against receipts; point `AGENTS.md` at the live SoD conflict
  (SOD006-C4, not the superseded C2) and at source revision 24
- [x] 6.5 G8 (ROOT CAUSE of "gpt-6.1-sol sometimes works"): the pool carries a governance identity
  (`provider`/`model`) AND a transport vocabulary (`transport_model`), and the vocabulary is per-provider —
  the openai arm REQUIRES the BARE id. The pool carried the qualified `openai-codex/gpt-6.1-sol`, which the
  relay routes to the default provider and answers HTTP 400 `Model is unavailable`. Measured on the live
  relay: bare -> 200, qualified -> 400. Repaired for PLAN#1, VERIFY_SECURITY#1 and EXECUTE#2, and a
  conformance test now fails if any openai-codex entry carries a qualified transport id
  (receipt `var/FAR-CLOSURE-20261021-R2/apply_receipt.json`; `check_drift` `[]`; pytest 5 passed / 90 subtests)
- [x] 6.6 G9: a checker lane could not re-derive a test-suite result because the host shell exports
  `TMPDIR=/tmp` (an MSYS virtual path a native Windows child cannot use), so `tempfile.mkdtemp` failed and
  pytest aborted with "No usable temporary directory found". The dispatcher now hands the child a
  Windows-usable scratch root as `TMPDIR`/`TEMP`/`TMP`, plus `PYTHONDONTWRITEBYTECODE=1` and
  `-p no:cacheprovider`
- [x] 6.7 Independent re-derivation: the AO lane (openai-codex/gpt-6.1-sol, Codex CLI, escalated to
  `workspace-write` under an explicit authorisation with a digest guard over the governed tree) re-derived
  all 10 claims -> VERDICT PASS, 520/520 governed files unchanged
  (receipt `var/FAR-CLOSURE-20261021-R2/probes/VERIFY_acceptance.json`)
- [x] 6.8 Publish the epoch-24 contract + receipts + research to Fabric as a candidate-only packet with a
  per-file SHA-256 manifest (branch `pub/far-lane-remediation-20261021`)

### Still open (not closed by this round)

- Model-axis independence between PLAN and VERIFY_SECURITY is ABSENT: both are `openai-codex/gpt-6.1-sol`
  **by owner order**, declared as `SOD006-C4 OPEN_OWNER_ORDERED`. Only process separation is claimed.
  Closing it needs an owner decision, not engineering.
- The `openai-codex` arm's upstream availability is not under local control. The ChatGPT OAuth backend
  listed 9 models including `gpt-6.1-sol` and `gpt-6-sol`; the relay's own catalogue is a stale snapshot
  (92 entries, no 6.x) and its `models_cache.json` records `fetched_at = 2000-01-01`. The lane works
  today because the bare id is forwarded verbatim, not because the catalogue is current.
