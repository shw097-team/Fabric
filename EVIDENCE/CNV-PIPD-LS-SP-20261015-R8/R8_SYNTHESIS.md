# R8-0 ROUND SYNTHESIS — CNV-PIPD-LS-SP-20261015

ChangeSet `R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE` · HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE` (4 WorkOrders, WORKORDERS_ADMITTED)
Authority: `Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` v2.0.0 (SHA `96d9d564…`), `HG-KSEOS/AGENTS.md`
Claim ceiling: **LOCAL / candidate-only**. Not an acceptance, not a Gate PASS, nothing merged.

## 1. What this round set out to do, and what actually happened

| # | Objective | Outcome |
|---|---|---|
| ① | Reuse the existing lanes; bind Hermes as the governed runtime plane under HG-KSEOS as the control plane | Done — no new lane was invented; the delegation plane was bound to the plan model, and the WS-A/WS-B/WS-V turns ran through the existing Codex-CLI lanes. Two lanes were served under the declared plan's arms (see §5 deviation). |
| ② | Skill-slim regression detection + guarded apply, per the PKG | Done — AVR candidate repaired and applied with a pre-image and a rehearsed byte-exact rollback; the HGK candidate was **not** applied because the detector found real content loss. |
| ③ | Close `BLK-R7-WS1-STALE-BASELINE` (rebuild the R7-0 hardening on `main`, re-measure the 18 mutations) | Substantively closed — M04/M06/M16 REJECT on `main`; the previously-detected ids stay detected. A genuinely new, honest cost surfaced: the port introduces 2 test failures (§4). |
| ④ | Resolve every EIA advisory, question, requirement and recommendation | Reconciled claim by claim (§3), with the parts that need owner authority or identity separation left gated rather than declared done. |
| ⑤ | Publish the R8 evidence packet to Fabric for an external acceptor | Done — branch `evidence/cnv-pipd-ls-sp-20261015-r8`, Draft PR #5, byte-level readback with 0 mismatches. |
| ⑥ | KANBAN + SWARM + GSTACK + OPENSPEC + multi-subagent execution with self-check/self-repair/self-verification | Done — 5 worker cards, 3 subagents, one independent verifier lane; OpenSpec proposal strictly valid; GSTACK role map read back. |
| ⑦ | Governed self-research / self-learning / self-iteration / self-evolution | `SELF_EVOLUTION_R8.md` + `.json` (7 research, 7 learning, 6 iteration, 7 evolution items, each with owner and gate). |

## 2. Round deliverables (all under `EVIDENCE/CNV-PIPD-LS-SP-20261015-R8/`)

- `WS_A/` — regression harness (C1–C6), per-candidate verdicts, repaired candidate, guarded apply record with pre-image and rollback, live post-apply re-check, receipt recomputation, `loader_parity_raw.txt` (annotated).
- `WS_B/` — the R8-0 semantic rebuild of the R7-0 hardening on `main`, the 18-mutation re-measurement, pytest outputs, per-mutation raw receipts, receipt with the honest partial.
- `WS_C/` — checker write-root isolation: the absence finding, the OS-level probe, the reversible mechanism proof, proposal only.
- `WS_D/` — guarded-subject byte-exactness against the merged packet (300 files, 0 mismatches).
- `WS_F/` — OpenSpec proposal (5 artifacts, strict validation exit 0) + receipt.
- `WS_G/` — GSTACK role-map readback, registry drift receipt, verification.
- `WS_H/` — repaired self-check harness (expectations derived at run time) + 7 regression tests + receipt.
- `R8_VERIFY/` — the independent verifier's own root: verdict, receipt, real mutation re-runs, re-derived harnesses, the diff, and **the orchestrator's attribution errata**.
- `R8_LEDGER.json`, `SELF_EVOLUTION_R8.*`, `PKG_ALIGNMENT_R8.json`, `R8_PUBLICATION_VERIFICATION.json`, `R8_MISSION_PLAN.md`, this synthesis, `PACKET_MANIFEST.json`.

## 3. EIA-R6-01…09 disposition

| id | disposition | basis |
|---|---|---|
| 01 | Errata text drafted and carried in the packet; publication of the correction is the archive owner's act | the R6 merge is a fact (`b8ff8104`); the advisory was about a metadata sentence, not the archive |
| 02 | Same class as 01 — one-line errata, not a re-cut | the 2-item manifest gap is explained by the recursion (manifest + `.gitattributes`), now closed |
| 03 | Open, owner-gated: procedural isolation stands; no OS-level denial exists; the mechanism is proven but unmounted | `WS_C/`, single-identity maker/checker separation is structural, not a bug to patch |
| 04 | Counterexamples closed on `main`; the port's own cost recorded | `WS_B/` + independent re-runs of M04/M06/M16 |
| 05 | Blocked on authority — not satisfiable locally | `WS_D/`, unchanged this round |
| 06 | Closed locally by the owner-authorised merge `b8ff8104` | readback of the merged prefix (581 blobs) |
| 07 | Owner-gated, unchanged | `WS_D/` |
| 08 | Quarantined, unchanged | `WS_D/` |
| 09 | Measured, and the >60 references condition was kept a soft warning — no invented gate | `PKG_ALIGNMENT_R8.json` (RQ08), live counts 118 candidate / 90 / 26 |

## 4. The honest partial (do not read this round as clean)

The R8-0 rebuild of the hardening is **not drop-in on `main`**: it introduces **2 test failures** —
`tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints` and
`tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs` (the latter with `AttributeError: 'str' object has no attribute 'get'` at `validate.py:434` in `derive_frozen_context`).
Measured 2×2: clean `main` (`dba4b19`) passes both (2 passed, 629 deselected, 27.89 s — orchestrator; 2 passed, 23.07 s — maker's stash run); the hardening tree fails both (2 failed, 18.69 s — orchestrator; 2 failed / 609 passed — checker's full suite).
Filed as `BLK-R8-WS2-MAIN-DIVERGENCE`, severity high, **not fixed in this round by design**: adaptation belongs to R9-0 with the hardening owner.

## 5. Deviations, incidents and errata disclosed

1. **Lane arm attribution could not be proven** (`TF-06`, now 10 occurrences across the round): both lanes returned `ERR_NO_ARM_EMITTED_NONCE` — the WS-A/WS-B turns report `opencode-go/deepseek-v4.1-flash` and the VERIFY turn reports `opencode-go/glm-5.3-flash` as nonce-absent arms, while each turn's usage receipt is `ok`. **Which arm actually served those turns cannot be proven from the receipt**, so the declared plan (EXECUTE DeepSeek V4.1 Flash; VERIFY gpt-6.1-sol) is a *dispatch declaration*, not an attested fact. Outputs stood on their own evidence instead.
2. **Control plane vs mandate disagreement** (`R8-F6`): the lane routing registry declares `opencode-go` where the mandate declares `openai-codex`, and the assignment file contradicts its own structured arm selector. Recorded, not silently edited.
3. **The pre-tool guard refused 2 receipt writes**; resolved through the sanctioned authorisation path with the user's explicit approval, filename and path references preserved, and the authorisation recorded in the receipts themselves.
4. **Checker errata** (`R8-F8`): the verifier's verdict is sound in its measurements but its WS-B-3 causal clause is false; corrected by third-party re-measurement (`R8_VERIFY/WS_B_3_ATTRIBUTION_ERRATA.json`). This is a lesson, not a reason to discard the verdict: the counts were honest, the cause was inverted.
5. **PKG alignment gap** (`R8-F7`): the PKG's RQ06 close predicate names a "10/6" slice partition; the artifacts in hand reconstruct 5 (AVR) and 6 (HGK, 6/6 slice byte-ranges verified) slices. Byte-exactness is therefore claimed against the artifacts' own maps, **not** against the PKG's named partition.
6. **Side effects**: the live skill tree was modified (AVR only, with a pre-image and rollback); the delegation plane was rebound; a Kanban board was created; two worktrees were added (`wt-r8-cleanmain`, and the maker's `r8-wt`); the Fabric branch and Draft PR #5 were created; a `HG-KSEOS/var/LANE-RELIABILITY-CLOSURE-20261016/` directory appeared during the round and is disclosed as not authored by this orchestrator.
7. **Not done**: 221 acceptance cases (0 run), gates G-A…G-H (0 PASS), AUD-24 (0/24), fresh G1 (not certified), R7-01…09 residual items, the `runtime_role_binding_assert.py` wiring, the `PLAN_READY` residue, the Hermes version-declaration mismatch, the PKG source #6 `FAIL_CLOSED`, and the 20 `*-R04` polarity defects (still isolated).

## 6. What would falsify this round's claims

- Recompute any `WS_A/WS_B/WS_C/WS_D` arithmetic from the published bytes: a mismatch means the packet is wrong, not the claim.
- Re-run the 18 mutations on the published `WS_B` tree: if M04/M06/M16 do not REJECT, §3 row 04 is refuted.
- Re-run the two disputed tests on clean `main` and on the hardening tree: if clean `main` fails, §4's attribution is refuted (it was the checker's version that failed this test, not the maker's).
- Re-resolve every declared path of `PACKET_MANIFEST.json` against the published tree: 358 == 358 with no exceptions.

## 7. Next round's entry conditions (R9-0)

1. Adapt the hardening to `main`'s newer test expectations and fix the `derive_frozen_context` crash path — this is the round's single blocking deliverable.
2. Rebind or repair the lane/registry declarations so the served arm is attested (`TF-06`) and the registry matches the owner's mandate (`R8-F6`).
3. Reconcile the RQ06 "10/6" partition with the artifacts (`R8-F7`), then let the Skill Owner run the trusted observation under an owner pin.
4. Owner decision on the checker identity/write-root separation (EIA-R6-03/05/07).
