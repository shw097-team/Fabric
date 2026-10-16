# Pre-implementation design discussion under HGK governance (GENIE vNext case, verified 2026-08-14)

Trigger: user opens a 實作前設計開發討論 / design-intent clarification round before
implementation ("與用戶進行實作前設計開發討論，主動釐清開發設計原意和需求，就緒後說一聲").
This is the design-phase counterpart of the governed execution pipeline.

## Mode + surfaces
- Run inside the 實作前開發文檔工廠 (Spec-Driven Document Factory) contract: 7 Specs
  (CORPUS/DOCUMENT/IA/SOURCE_POLICY/COVERAGE/PUBLISH/EVALUATION) + constitution
  (raw sources immutable, writer ≠ approver, 缺規格即 Fail Closed). Evidence contract
  lives in 知識庫 Hermes & AIKD 討論-4 + SSOT 實作前開發文檔包.
- Standard six surfaces still default-on: HGK WO admission (typed SharedSpine), Kanban DAG
  (G1 modes → G2 corpus → G3 discussion → G4 user decisions → G5 readiness),
  gstack route check (`route("plan-design")` → GSTACK plan-eng-review), dual-lane swarm
  readback of admission + corpus inventory, Codex only when tracked doc writes begin.

## Discussion method (mattpocock `grilling` skill — enabled, use it)
- Map a design tree; ask the WHOLE frontier per round; each question:
  `❓Q# - title: body with options` + `➡️ recommended answer`.
- Decisions are the user's; FACTS are yours — dispatch parallel read-only lanes
  (`delegate_task`, max 3 concurrent → split batches) for anything look-up-able.
- Recompute the frontier after each answer. STOP between rounds.
- User pattern (this user): replies by option letters, frequently "照建議" = wholesale
  adoption of all recommendations — treat as frozen decisions, record them.

## Fact-gathering lanes that worked
- Old-design stack inventory: grep keyword counts (Chinese + ASCII, `grep -E` quoted) over
  the KB corpus; verdict dated-vs-current.
- Hot-OSS scan: GitHub REST API via curl (stars/pushed_at/created_at — REAL values only,
  never fabricated); theme tags (SPEC_DRIVEN/AGENT_SKILLS/MCP/A2A/EVAL/ORCHESTRATION/...).
- Capability matrix of the existing stack (CLI surfaces, control tree, spine tables,
  profiles, Fabric contracts) → reuse-first mapping of old product lanes onto existing
  capabilities. Expect the user's own insight that "現成系統 ≈ 舊設計的產品化" — verify
  it, then the remaining work = gap-filling + productization, not rebuilding.

## Gap matrix methodology
- Extract the old design's infrastructure component/service list from its own docs
  (numbered lists WITH file citations per item).
- Map each onto the capability matrix: ✅ landed (rename/productize) / ⚠️ partial
  (thin-layer add) / ❌ gap (needs build or OSS integration).
- **Today-lens re-research (user directive, 2026-08-14):** every ⚠️/❌ item must be
  re-checked for (1) outdated-as-of-today, (2) replaceable by existing OSS, (3) higher-heat
  community direction — run as FAR research (WO admission → parallel research lanes →
  challenge lane → HITL gate) BEFORE committing the build list. New corpora added to the KB
  mid-task (e.g. TCA-10X/ASCE-WebX) must be scanned for supersede/extend/orthogonal vs the gaps.

## Close-out
- User decisions frozen as `USER_DECISION_<topic>_<date>.md` (SHA-bound into REQ locator).
- Every governed round still closes per invariant #9: fresh-context AO lane + single evidence
  MD mirrored byte-identical to the 3 roots.
- Non-claims during design: no runtime/repo/PASS claims; P4+ selections stay
  "評估中" until evidence lands.

## Pitfalls observed
- Kanban board gets switched away by parallel sessions (`boards list` first, switch back,
  re-claim, then heartbeat).
- `HERMES_DELEGATED_CHILD_CONTEXT` blocks kanban mutations after every delegate_task batch —
  remove the var before kanban ops.
- Delegation fan-out cap is 3 concurrent children — plan batches of ≤3; queue the rest.
