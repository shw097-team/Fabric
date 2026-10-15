# R7-0 acceleration round — KANBAN · SWARM · GSTACK · OPENSPEC

Mission `CNV-PIPD-LS-SP-20261015`. This document records the acceleration pass run after the R7-0 packet was first
published. Claim ceiling throughout: **LOCAL / candidate-only** — nothing here is an acceptance, an approval, a
Gate PASS or a production effect.

## KANBAN + SWARM (real board, ids on disk)
- Board: `cnv-r7-0-accel-20261015`
  (`…/hermes/kanban/boards/cnv-r7-0-accel-20261015/kanban.db`).
- One `kanban swarm` call built the whole DAG: root `t_cb349415`; workers `t_6b486801` (WS1), `t_309d743f` (WS2),
  `t_487b3659` (WS3), `t_d11b97eb` (WS4), `t_9bb5924a` (WS5); verifier `t_18395e4b`; synthesizer `t_c7f0b89b`.
  Ids and titles are also written to `KANBAN_SWARM_GRAPH_R7.json` so a later round can re-verify the graph
  instead of trusting prose.
- All five worker cards were closed with an evidence string (the evidence lives in this packet, not in the card).
  The verifier card was promoted by the DAG and is being run as a **sealed Codex VERIFY/SECURITY lane**, not by the
  orchestrator.

## GSTACK (named-method route check)
`WS4_GSTACK_ROLEMAP_READBACK.json` + `WS4_GSTACK_RECEIPT.md` (read-only pass, reproducing the R6 probe and driving
the repo's own gates). Headlines:
- The ACTIVE_SELECTED evidence for GSTACK roles lives in `HG-KSEOS/src/hg_kseos/named_methods.py`, **not** in
  `config/`: **7 of 19** role-map entries have a role-keyed method.
- Gaps named: `DECLARED_NOT_SELECTED` = autoplan, qa-only; `MAP_ROLE_ABSENT` = investigate, benchmark, document-*,
  canary, design-consultation, codex (no `route(flow)` branch — they route NATIVE); `SELECTED_NOT_IN_MAP` = 0.
- Live routes at readback time: VERIFY_SECURITY → `openai-codex/gpt-6.1-sol` (medium) with GLM→DS fallbacks and
  `admission_status: UNPROVEN`; PLAN → `opencode-go/glm-5.3-flash`; EXECUTE → `opencode-go/deepseek-v4.1-flash`.
- **SoD residual, stated plainly:** this session's delegation plane is `opencode-go/glm-5.3-flash`, which is also
  the VERIFY arm-B identity, so **model-axis and provider-axis independence do not exist**; what remains is process
  separation plus EXECUTE-vs-VERIFY-A distinctness. The registry carries owner-recorded deviations `SOD006-C2` /
  `SOD006-C3` (`OPEN_OWNER_ORDERED`).
- Extra findings surfaced by the same pass: one `DRIFT_VALUE` (`/codex_sha256`, the known stale pointer); the
  assignment file internally contradicts itself on VERIFY arm A (prose vs supply selector — invisible to
  `check_drift`); `runtime_role_binding_assert.py` is untracked and unwired (its only wired caller is a prior
  round's E2E harness).

## OPENSPEC
`WS3_OPENSPEC_PROPOSAL_RECEIPT.md` — new change `hgk-lane-brief-and-guard-hardening-20261015`
(`HG-KSEOS/openspec/changes/…`, 5 files) proposing the remediation of all nine tooling findings TF-01..TF-09, each
task naming the finding id, the exact file/surface, the acceptance evidence, and its applicability (`NOW`, or
`BLOCKED-owner` for the spine/relay/AO-adjacent work). Validated with the repo's own CLI:
`npx openspec validate <id> --type change --strict` → *is valid*, exit 0 (CLI 1.8.0), `deltaCount: 7`.
It is a **proposal**: zero implementation, every task unchecked.

## WS1 — product-side publication, and the blocker it exposed
The R7-0 change was authored in a workspace copy of the product that is **not** current `main`:
- the writer's pre-change snapshots are byte-identical to the blobs of commit **`a503efe`**
  (`ce840caadca8` / `7f21aa84c4ae` / `69095baeb68a`); `main` is `dba4b19456777d3b597fdf71480f6423dd974243`
  (`7c3145cd002b` / `75799b744e8a` / `4a2e13fbbdd7`);
- so the patch is a delta **against `a503efe`**, and copying the candidate files onto `main` would **revert**
  intervening work (net `main`→candidate is +164/−158 lines in `validate.py` alone, including the CE-2 refinement);
- a mechanical rebase does not apply cleanly: `pipeline.py` applies (`rc=0`); `validate.py` and `cli.py` conflict
  (`git apply --check rc=1`). Measurement: `REBASE_MEASUREMENT.json`; deltas: `REBASE/*.delta.patch`.

Handling (option A, chosen for zero regression risk): nothing was applied to `src/`. The candidate files (evidence
copies), the delta patches, the measurement and the blocker record were published on PIPD-LS-SP branch
`evidence/cnv-r7-0-validator-hardening-20261015` (head `eae636d8668027887977a797b20e63899465ad8d`, 16 blobs under
`evidence/cnv-r7-0/`, `src/` untouched, blob-ids verified) with Draft PR #15. Option B — rebuild against `main`
and **re-measure the 18 mutations there** — is the recommended next change set (R8-0), because the round's M04/M06/
M16 result is measured only on the `a503efe`-derived tree.

## WS5 — the self-check / self-repair harness
`selfcheck/round_selfcheck.py` re-verifies the round's invariants from live evidence (branch head vs remote vs
recorded readback; 212 packet blobs re-hashed as `sha1("blob N\0"+bytes)`; manifest reconciliation; `main` and the
R6 archive frozen by digest; the M2 verdict; the authoritative checker verdict's schema and ceiling), refuses to
write outside the handover root, refuses git write verbs, and prints the claim ceiling on every run. Result:
**6/6 PASS, overall PASS, exit 0**, re-run by the orchestrator with the same outcome (`SELFCHECK_OUTPUT.txt`).
Repair mode is armed but touched nothing (no repair was needed). Its own limits are stated in
`selfcheck/WS5_SELFCHECK_RECEIPT.md`: it is a **machine gate**, not a governance acceptance, and it explicitly
keeps four claims unverifiable (provider/model attestation, upstream CI, the 221 acceptance cases, the voided
attempt-1 evidence).

## Verifier
`VERIFIER_BRIEF_SWARM_R7.md` was dispatched to a sealed Codex VERIFY/SECURITY lane with its own write root
(`R7_VERIFIER_SWARM/`), tasked to **falsify** the five claims above — including an adversarial read of the
self-check harness itself (can any check pass vacuously; do its guards really refuse). Its verdict, if it lands,
is published as `R7_VERIFIER_SWARM/` and remains a candidate verdict for the Owner.
