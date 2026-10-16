# ROUND 3 — Lane rebind to the new owner mandate, residual closure, repo cleanup and session handover

Round id: `ROUND3-LANE-REBIND-AND-CLOSURE-20261016` · Session `20261016_104922_d455e7` · Round dir
`var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/`. Control plane: HG-KSEOS. Governed runtime/orchestration plane:
the canonical Hermes bound to it. Claim ceiling: **CANDIDATE_ONLY**, no self-acceptance.

## 1. The owner mandate (verbatim intent, three lanes)

| lane | who runs it | mandated provider / model |
|---|---|---|
| PLAN & Orchestrator | inside Hermes | **opencode-go / glm-5.3-flash** |
| EXECUTE — bounded writer | handed to CODEX CLI | **opencode-go / deepseek-v4.1-flash** |
| VERIFY / SECURITY — independent acceptance officer | handed to CODEX CLI | **opencode-go / deepseek-v4.1-flash** |

Plus: FAR over every residual / gap / blocker, owner-decision item, candidate-not-landed item and skill, the
repository's merge / branch-cleanup / publication surface, and this session's closure & handover; then EXECUTE
the ruling directly (owner-authorised); publish implementation + evidence to `shw097-team/Fabric` with the PAT at
`C:\Projects\Agent_Workspace\API KEY\GITHUB-REPO_SHW097-4.txt` for external acceptance; enable
KANBAN + SWARM + GSTACK + OPENSPEC; run CODEX CLI + parallel sub-agents; self-check / self-repair /
self-verify to completion; finish with a governed self-study / self-learning / self-iteration / self-evolution pass.

## 2. Ground truth measured BEFORE any ruling (not from config or memory)

- **Registry (canonical, epoch 21)** — `config/lane-routing-registry.yaml`: PLAN = `openai-codex/gpt-6.1-sol`
  (medium, openai_oauth, ADMITTED), fallbacks `[glm-5.3-flash, deepseek-v4.1-flash]`;
  EXECUTE = `opencode-go/deepseek-v4.1-flash`, fallbacks `[gpt-6-luna, nvidia/deepseek-ai/deepseek-v4.1-flash]`;
  VERIFY_SECURITY = `openai-codex/gpt-6.1-sol` (medium), fallbacks `[glm-5.3-flash, deepseek-v4.1-flash]`.
  So the mandate reverses PLAN's rank order (GLM is currently fallback1, not default) and moves VERIFY off
  `gpt-6.1-sol` onto the arm that EXECUTE already holds.
- **`sod_invariants.pairs[]`**: `{EXECUTE, VERIFY_SECURITY, distinct_required: true}` and
  `{PLAN, VERIFY_SECURITY, distinct_required: false}`. The mandate therefore **flips the collision axis**: the
  pair that must stay distinct (writer vs checker) becomes SAME-model, while the pair that carried the recorded
  owner-ordered conflict (`SOD006-C2`, PLAN vs VERIFY, both `gpt-6.1-sol`) stops colliding — PLAN moves to GLM.
  A registry edit that does not also re-declare the conflict set is not conformant.
- **Model availability, MEASURED**: the exec frontdoor `127.0.0.1:10100/healthz` = **200**; the relay
  `127.0.0.1:10101/v1/chat/completions` answers `glm-5.3-flash` and `deepseek-v4.1-flash` with **http 200 and
  `PROBE_OK`** each. Both mandated models are therefore *reachable* — reachability is not yet lane service, which
  is what the EXECUTE/VERIFY dispatches below must prove with `required_arm == served_arm`.
- **Hermes bindings**: root `model.default = glm-5.3-flash`, `model.provider = opencode-go`, and
  `delegation.provider = opencode-go`, `delegation.model = glm-5.3-flash` — so the orchestration plane and the
  sub-agent fan-out are ALREADY bound to the mandated PLAN model. The governed profile
  `profiles/hgk-governed/config.yaml` still binds `gpt-6.1-sol` / `openai-codex` — a STALE binding under the new
  mandate, and one of this round's repair items. This interactive session's own serving model is
  `deepseek-v4.1-flash` (runtime header): disclosed as an observed-vs-bound split, not as compliance.
- **Fabric repository**: `origin/main` = `b8ff810`; PRs #1/#2/#3 MERGED, #4/#5/#6/#7/#8 OPEN; 10 remote
  branches, of which the two `pub/*` branches carry this workstream's rounds and four `evidence/*` / `docs/*`
  branches belong to another workstream (three of their PRs are merged).

## 3. What FAR must rule on (the研究 axes of this round)

1. **R-lane**: the registry rebind to the mandate — exact fields, coupled declarations (`source_of_routes`,
   `registry_epoch`, every affected `projections[].bindings[]`), the SoD re-declaration for the flipped axis,
   and the `/sod/*` prose that F-IND-2 already recorded as contradicting the structured fields.
2. **R-residual**: the 15 residuals + F-IND-2 / F-IND-3, each re-derived against the live tree, and separated
   into do / decide / drop — including which the new mandate makes moot and which it makes newly active.
3. **R-candidate**: OpenSpec changes never applied or archived, candidate artifacts never landed, and skills
   written but never validated — land / drop / defer.
4. **R-repo**: merge, branch cleanup and publication — what an agent may do under a contract that reserves
   merges to the owner, and what a merge-readiness packet must contain.
5. **R-close**: this session's closure and handover, plus the self-study / self-learning / self-iteration /
   self-evolution pass.

## 4. Sequence (each step with its receipt; nothing is claimed before it is measured)

1. Recon (this file §2) → 2. parallel sub-agent research (4 axes, read-only) → 3. FAR ruling with priced options
and rejected alternatives → 4. HGK typed admission (WorkOrders + TaskSpecs) → 5. KANBAN + SWARM graph,
OPENSPEC change (`--strict`) → 6. GSTACK named-method readback → 7. execution of the ruling (registry rebind,
governed-profile rebind, residual repairs that are in scope) → 8. independent VERIFY lane on the mandated
checker arm → 9. self-check / self-repair harness + publication gate → 10. publish to Fabric (branch + PR,
never force-push, never merge) → 11. session closure + handover checkpoint → 12. self-evolution note.

## 5. Standing constraints carried into this round

Candidate-only; no agent self-acceptance or self-promotion; merges are the owner's; every round side effect
disclosed; absolute test counts are environment-dependent while paired deltas are the reproducible claim;
a receipt that a re-runnable script overwrites is not a receipt; freeze only bytes that no tool of the round
rewrites after the freeze; a published digest must name its stage; every published file is verified by reading
the remote's own objects, never by the push's exit code.
