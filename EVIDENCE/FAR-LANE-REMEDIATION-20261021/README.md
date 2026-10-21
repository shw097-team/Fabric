# FAR-LANE-REMEDIATION-20261021 — publication summary for external acceptance

**Repository:** `shw097-team/Fabric` (branch `pub/far-lane-remediation-20261021`)
**Subject:** HG-KSEOS lane/model declaration remediation — registry epoch 22 → 24
**Control plane:** HG-KSEOS (sole control plane); canonical Hermes = governed Runtime/Orchestration Plane
**Claim ceiling:** `CANDIDATE_ONLY` — mirrored governed artefacts for external acceptance. Local
verification is not independent acceptance; publication is not release.

## What an external engineer can verify from this repository alone

1. **The route contract itself** — `implementation/lane-routing-registry.yaml`,
   `implementation/model-lane-assignment.json`, `implementation/lane-route-slots.candidate.json`,
   `implementation/hermes-codex-lane.json` are the exact bytes that the governance registry
   projects. Their digests are in `PACKET_MANIFEST.json`.
2. **The change that produced them** — `implementation/IMPLEMENTATION_DIFF.patch` (the
   `AGENTS.md` + owner-chain-oracle diff of the epoch-23 alignment), `IMPLEMENTATION_DIFFSTAT.txt`,
   and the two apply scripts (`apply_far_remediation.py`, `apply_closure.py`) with their receipts
   (`evidence/apply_receipt.json`, `evidence/apply_receipt.json` for the closure round).
3. **The lane receipts that prove which arm actually served** — `lane_receipts/` holds the raw
   dispatcher receipts: the EXECUTE turn served by `opencode-go/minimax-m3.1-flash-free`
   (`required_arm == served_arm`), the earlier `opencode-go/deepseek-v4.1-flash` turn, the
   `openai-codex/gpt-6.1-sol` VERIFY turn, and the AO attempt that did **not** complete.
4. **The self-check gate** — `implementation/selfcheck_epoch24.py` and
   `evidence/selfcheck_receipt.json` (GATE_PASS 20/20, re-runnable; prints its own claim ceiling).
5. **The research that drove the closure** — `research/RESEARCH_GAPS.md` (11 gaps classified A/B/C),
   `research/RESEARCH_CANDIDATES.md` (candidate-merge adjudication), `research/RESEARCH_DOCUPGRADE.md`
   (file-level upgrade list with line numbers).
6. **The diagnosis that started it** — `round_documents/FAR_LANE_VERSION_MIX_REPORT.md` and
   `evidence/EVIDENCE_DIGEST.md` (the cross-surface contradiction table and the mechanism analysis).

## Current declared route (epoch 24)

| Lane | Rank-1 provider/model | Engine | Fallbacks |
|---|---|---|---|
| PLAN | `openai-codex/gpt-6.1-sol` (medium, OAuth) | hermes | `opencode-go/glm-5.3-flash`, `opencode-go/deepseek-v4.1-flash` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | codex-cli | `openai-codex/gpt-6-luna`, `nvidia/deepseek-ai/deepseek-v4.1-flash` |
| VERIFY_SECURITY | `openai-codex/gpt-6.1-sol` (medium, OAuth) | codex-cli | `opencode-go/glm-5.3-flash`, `opencode-go/deepseek-v4.1-flash` |

`opencode-go/minimax-m3.1-flash-free` is carried as a **PROBE** arm on EXECUTE (rank 4,
`automatic_selection: false`): the Codex-CLI lane was measured serving it
(`required_arm == served_arm`, nonce present, usage receipt OK), but it is **not** a policy default.

**Independence:** PLAN and VERIFY_SECURITY share `gpt-6.1-sol` **by owner order** — declared as
`SOD006-C4 OPEN_OWNER_ORDERED`. Model-axis independence is **absent** for that pair; only process
separation is claimed. EXECUTE (`deepseek-v4.1-flash`) vs VERIFY (`gpt-6.1-sol`) remain model-distinct.

## What is NOT claimed

- No independent acceptance was obtained for this change-set. The AO lane
  (`openai-codex/gpt-6.1-sol` over the Codex-CLI transport) returned
  `Provider error 400: Upstream request failed: Model is unavailable` on every attempt; the
  provider's own quota shows 31% weekly used with a valid (unexpired) credential, so the
  unavailability is an upstream model-availability condition, not a quota wall and not a local
  configuration defect. `lane_receipts/AO_verdict2.json` records the failing attempt verbatim.
- No canonical acceptance, no release, no production authorisation.
- The mirrored `var/` trees, the spine database, the credential stores and every machine-local
  runtime path are **not** published here.
