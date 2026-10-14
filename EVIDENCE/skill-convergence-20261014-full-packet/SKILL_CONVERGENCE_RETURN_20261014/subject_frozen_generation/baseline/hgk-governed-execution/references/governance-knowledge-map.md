# HGK/FABRIC Governance Knowledge Map (read-only analysis lanes)

Condensed knowledge bank from a governance-analysis lane (2026-08-14): where the governance
machine truth lives, the SHARED_INFRASTRUCTURE_PROFILE_TEAM pattern, and the efficient
workflow for extracting principles from the large Chinese DOC corpus. Use for read-only
feasibility assessments ("拆出成 FABRIC 共享基礎設施" style proposals) — never for
executing acceptance/canary tasks (that is the parent skill's job).

## Corpus locations

- Hermes_Agent_OS 專業技術文檔 (20 files, 4–7k lines each, 繁體中文):
  `C:\Projects\Agent_Workspace\知識庫\專業技術文檔\Hermes_Agent_OS_專業技術文檔\DOC-*_r2.md`
- FABRIC governance surface:
  `C:\Projects\Agent_Workspace\Fabric\` — `control\*.yaml` (policy),
  `contracts\*.schema.yaml`, `assurance\*.yaml` + `assurance\acceptance-packs\<pack>\`,
  `rp002\RP002_*.yaml`, `fabric-desktop-automation\` (FDA), `fabric-autonomous-research\` (FAR),
  `stage\RP002-STAGE-HGK\KG1\` (KG1 runtime truth)
- The master blueprint (RP-002_v2.0_Master_Blueprint_2026-08-12_r2.md) is NOT stored locally —
  referenced by locator only; the frozen `control\*`/`contracts\*` YAMLs ARE the machine truth.

## Efficient search workflow for the DOC corpus

DOC files are too large to read fully; ToC anchor lines pollute keyword searches badly.

1. Per-file `search_files` with `context: 3`, pattern on distinctive terms (e.g.
   `四道門|canonical|TruthBoundary|taint|admission|health`) — search ONE file at a time.
2. Find body anchors with `output_mode: "content"` on header patterns
   (`^#{2,4} .*(CH-20|Asset|Curation)`), since ToC entries don't match `^#` headers.
3. `read_file` the precise line range around each anchor (e.g. SPEC/ART/WF blocks are
   contiguous ~30-80 line ranges).
4. For status/owner facts, the first ~60 lines of each DOC carry the verdict card
   (Accountable owner F0x, checker F11, security F12, release reducer F13, approver F01).

## Governance principles by DOC (condensed, verified quotes in report)

- **DOC-01 Product Constitution**: hard invariants — one Canonical Owner per decision domain;
  constitutional change = two-key human approval; five-way split: Canonical knowledge =
  source-backed approved artifact, Memory = candidate/temporal state, RAG = retrieval, KG =
  rebuildable derived view; all source/tool/MCP/legacy text = DATA until admitted.
- **DOC-02**: KB = approved source-backed only; Memory = scoped/temporal/retention/promotion
  candidate; RAG = retrieval/grounding; KG = derived view; Skill/MCP = capability interface.
  None own truth; on conflict return to AuthorityRule.
- **DOC-08 (SC-DOC08-06)**: taint-as-DATA — source text/memory/RAG hits/provider output/tool
  descriptions are DATA until sanitized+adopted; can inform reasoning, cannot create
  permission or alter policy; TaintLabel/ContextTaintMap/RouteOutRecord/SanitizedToolProfile/
  ProvenanceRef; redaction required.
- **DOC-11**: Memory is NOT truth (candidate state with source/scope/time/permission/
  freshness/retention/conflict/evidence). Four gates: capture → object → recall → promotion
  (F06 proposes, target owner accepts, F11/F12/F13 verify, NO self-promotion). Cross-tenant
  fleet-memory injection = poisoning incident. Owner F06; CH-11 must not be swallowed by
  DOC-10/12.
- **DOC-12**: "Grounded Retrieval is a governed derived-view layer, not canonical truth."
  KB admission 7 gates: identity→sanitation→rights/tenant→canonical state→segmentation/dedup→
  projection plan→checker admission (F11/F12 check, F06 accepts). KG: Schema before edges;
  each edge needs direct evidence locator + checker + effective interval; inferred vs source
  edges layered; state PROPOSED→VALIDATED→ADMITTED→DISPUTED→WITHDRAWN/SUPERSEDED; high-risk
  edge = 2 independent sources or human approval. Grounded requires tenant namespace + rights
  filter + source withdrawal graph + citation gate + rollback.
- **DOC-13**: capability may consume retrieval; truth promotion belongs to knowledge owner;
  MCP descriptors untrusted until tool admission + negative tests + least-privilege;
  published trust is time-bounded → re-certification on drift.
- **DOC-20 (CH-20)**: candidate-first invariant — none may approve itself/become canonical
  truth/release directly. AssetHealthRecord (multi-dim, never one collapsed score;
  ERR_HEALTH_DIMENSION_COLLAPSED) for asset classes memory/KB/skill/repo/index/KG. WF-17:
  classify→health→candidate (never direct write)→dependency→disposition→rebuild→reduce.
  ConflictDecision (authority+temporal+checker), SupersessionRecord (no successor without
  acceptance+consumer impact).

## FABRIC machine truth (verified file contents)

- `control/KNOWLEDGE_POLICY.yaml` (FABRIC-KNOWLEDGE-POLICY/1): principle
  CENTRAL_GOVERNANCE_SHARED_SUBSTRATE_DISTRIBUTED_DOMAIN_PRODUCTION; namespaces hgk/sqs/
  fabric/assurance/shared; `cross_namespace_write_default: DENY`; `candidate_is_truth: false`;
  `domain_owner_retains_truth_authority: true`; provider runtime validation gate = KG1.
- `stage/RP002-STAGE-HGK/KG1/KG1_NAMESPACE_MODEL.json` (machine truth): hgk.candidate.*
  (write=agents, promote=HGK_AUTHORIZED_ROUTE_ONLY), hgk.approved.* (write=promotion-gate,
  read=all-governed), hgk.revoked.* (revocation-gate, auditors), fabric.* (fabric-authorized,
  promote=FABRIC_GATE), assurance.*, sqs.* (stage2 read-only), shared.approved.*; rules:
  agent write=candidate only, promotion=owner/gate only, forget=tombstone+audit receipt,
  cross-stack export=explicit promotion.
- `control/AUTHORITY_MATRIX.yaml`: HGK_ENGINEERING_TRUTH owner HGK, fabric_can_govern_access
  =true, fabric_can_mutate_truth=false (same for SQS_FINANCIAL_TRUTH); PROMOTION_DECISION
  owner=DETERMINISTIC_FABRIC_REDUCER requires_acceptance; human_only = constitutional_change /
  unresolved_same_rank_authority_conflict / live_financial_side_effect_authorization.
- `control/PROMOTION_POLICY.yaml`: requires frozen_subject, exact_candidate_digest,
  required_acceptance_receipt, domain_receipt_if_applicable, rollback_target,
  projection_consistency; auto_promotion_from_agent_output=false.
- `control/CAPABILITY_QUALIFICATION_POLICY.yaml`: DOC-29 lifecycle (consumer_need →
  identity_pin_license → local_evidence → official_probe → capability_nfr →
  security_rights_sbom_permission → fixture_benchmark → portable_baseline → selection →
  adapter_pilot → consumer_ack → drift → requalification → migration_rollback_exit);
  MISSING_TOOL_ROW=FAIL_CLOSED; popularity can't override hard gate.
- `control/MEMBER_POLICY.yaml`: admission requires stable_identity/source_digest/
  authority_ceiling/permission_scope/lifecycle_state/rollback_or_disable_path.
- `control/PROFILE_STACK_REGISTRATION_POLICY.yaml`: registration != authorization.
- `assurance/acceptance-packs/knowledge/acceptance-pack.yaml`: checks = candidate write
  only / promotion by gate / revoke+tombstone.
- Provider ledger (KG1_PROVIDER_LEDGER): SQLite/FTS5 P0 REUSE active; HGK Memory P0 REUSE
  (candidate ≠ truth); Qdrant/Neo4j default-off (not installed); pgvector conditional;
  Cognee P1 shadow.

## SHARED_INFRASTRUCTURE_PROFILE_TEAM pattern (FDA + FAR precedent)

- Registry: `rp002/RP002_PROFILE_TEAM_MANIFEST.yaml` (schema RP002-PROFILE-TEAM-MANIFEST/1,
  r3 §20.4) — additive instance rows + team_artifacts; NO schema fork; parent rows preserved.
- Team artifact: `<team>/TEAM.md` with `team_class: SHARED_INFRASTRUCTURE_PROFILE_TEAM`,
  `heavy_stack: false` (heavy stack count stays 2: HGK_ENGINEERING + SQS_FINANCIAL),
  `task_truth: HGK WORKORDER`, `normative_control_plane: HG-KSEOS`,
  `independent_checker: ACCEPTANCE_OFFICER (VERIFY_ONLY)`,
  `knowledge_policy_ref: CURRENT_FABRIC_KNOWLEDGE_POLICY (fabric.* namespace; candidate-only)`.
- Hard invariants to copy: MAY NOT CREATE_WORKORDER / SELF_ACCEPT / SELF_PROMOTE /
  CREATE_SECOND_KNOWLEDGE_PLATFORM / change domain truth; one active writer; provider switch
  requires readback+checkpoint+known state+lease; SQS live = NOT_AUTHORIZED.
- Materialization recipe (FAR_FIRST_USE_EVIDENCE, "未來同類 Shared Infrastructure Team 落地"):
  WO admission → CAPC (capability/qualification) → canary → dual-lane acceptance (internal AO
  VERIFY_ONLY fresh context + external reviewer) → freeze. Gates: G0,G1,K1,D1,C1,H1,O1,B1,
  F0,CF1,F1,KG1,SQP1,S1,E1,E2,R1 (historical names KBN1/FG1 do not execute).

## Feasibility assessment framing (for "split X into FABRIC shared infra" proposals)

- Feasible ONLY as "shared capability substrate / contract surface", never as truth transfer.
- Three non-negotiable bottom lines: domain_owner_retains_truth_authority=true,
  cross_namespace_write_default=DENY, fabric_can_mutate_truth=false.
- Owner change of a decision domain = constitutional change → human two-key approval
  (F01 + Human Policy Owner) per DOC-01 #1/#2 and AUTHORITY_MATRIX human_only list.
- DOC-12 source-backed admission and DOC-20 asset health are ENFORCERS for shared infra,
  not relaxers — they must be built into the shared service contract and fail closed.
- SoD trap: the shared team must not be both maker and gate for its own namespace;
  promotion stays with FABRIC_GATE / DETERMINISTIC_FABRIC_REDUCER + independent checker.
- Output format used: Chinese structured JSON
  `{"governance_principles":[{principle,source,quote}], "profile_team_blueprint":{...},
  "upgrade_governance_assessment":{feasible,conditions,risks}}` with verbatim quotes —
  parent lane expects quotes bound to exact DOC sources.

## Pitfalls

- ToC anchor lines flood content searches in these DOC files → prefer header-anchored
  `output_mode:"content"` patterns and per-file searches.
- Master blueprint MD not on disk; don't claim blueprint text you can't read — use the
  frozen control/contracts YAMLs as the authoritative local source.
- Verify quotes against the file at read time (r2 files are body-replacements; r1 claims
  like PASS_BODY_WITH_TT are not inherited).
- `.git` object noise dominates naive `find`/`ls` in `Fabric\` — use `find . -path ./.git
  -prune -o -name '*.md' -print` style filtering.
