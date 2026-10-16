# HGK-KSEOS SSOT — proposal grounding & upstream-vs-HGK authority determination

Condensed knowledge bank (2026-08-21 read-only grounding lane). Use when a proposal / defect /
remediation must be **grounded in the HGK-KSEOS governance SSOT** and you must decide WHO owns the
fix: HGK's governed code/contracts, or an **upstream provider** (Hermes / Codex / DocETL / OpenCode).
This root is `知識庫/HG-KSEOS_SSOT/` — DIFFERENT from the Fabric/technical-DOC corpus covered in
`governance-knowledge-map.md`. Never use for executing acceptance/canary tasks (parent skill's job).

## Root layout (verified paths)

```
C:\Projects\Agent_Workspace\知識庫\HG-KSEOS_SSOT\
├── HG-KSEOS_P0-CIP-PACK_v2026.08.05-r2.md        (6.7 MB / 69,376 lines — the governance contract)
├── HG-KSEOS_實作RBWI_WP_控制工件_PACK_FINAL_r2\   (Group-01..07 control-artifact pack)
│     *Group-04_ControlPlane_Providers_ToolTranslation.md
│     *Group-05_Coding_Security_Verification_SRE.md
│     *Group-07_CrossPack_Registries_Executable_Control_Contracts.md
├── RBWI_WP_CONTROL_PACK\                         (older G01..G07 — often superseded by FINAL_r2)
└── 藍圖\
      HG-KSEOS_多智能體協作系統_本地部屬藍圖_r2.md  (multi-agent orchestration blueprint, 2,190 lines)
      HG-KSEOS_藍圖_r2.md
```

## CRITICAL navigation pitfall — H2-xx boilerplate vs substantive body

The P0-CIP-PACK's `## H2-00..H2-09` "r2 Domain Contract" sections are ~98% **generated
boilerplate** (identical schema/state/oracle/security text repeated for every section). Do NOT read
them for substance. The REAL normative content lives in:
- The **chapter bodies**: CH-01 `Operative Authority Stack` (L926-939) and `Normative Claim Card`
  (L943-960) schema; CH-01 conflict-resolution table (L962-971); Version-Alias ledger (L1080-1098);
  Source-to-Clause precision rules (L997-1002).
- **PUB-00 / Package Constitution** body (L47-51, L79-131): sole-Root declaration, authority order,
  claim ceiling, PURPOSE/BOUNDARY (PUB-00 explicitly does NOT own runtime/install/production).

Navigation recipe: `search_files` header pattern `^#{1,3} ` to get the chapter map, then
`read_file offset=` straight into the substantive chapter/sub-section — skip the H2-xx boilerplate
ranges. The decisive clauses are usually in the RBWI Groups and the 藍圖, not the giant PACK body.

## THE core determination — is X a governed SSOT of HGK, or upstream?

**Result: Hermes (and DocETL / Codex / OpenCode / HLPE / SDLC_PRW / SRU) are UPSTREAM PROVIDERS,
pinned external artifacts — NOT governed SSOTs of HGK. HGK owns design intent + contracts + evidence,
NOT their source code.** Decisive, verifiable sources:

- **Package Constitution**: "HG-KSEOS remains the sole Product Root… Hermes, DocETL, Codex, OpenCode,
  HLPE, SDLC_PRW, SRU_OROCHI and every external tool are providers, methods, branches, projections,
  receivers or legacy assets—not parallel Roots." — PACK **L49**; authority order A0→A7→Web, lower
  tier cannot override higher — **L51 / CH-01 L928-939**.
- **RBWI Group-04 REQ-122 / REQ-124 / REQ-128** (the single strongest set of anchors):
  - REQ-122: "Hermes 是 cognitive coordination plane 與受治理 workspace host，不能成為產品 Root、
    Shared Spine 或 release authority" — Group-04 **L1164**
  - REQ-124: "直接整本移植 Hermes 導致名稱/權威/狀態漂移…Hermes local state 變 canonical" — **L1166**
  - REQ-128: "Hermes 是 Primary/Preferred Provider 之一，不是不可替換 kernel；HG-KSEOS contract
    永遠先於 Hermes implementation" — **L1264**
- **藍圖 §20.3** pins the Hermes installer from `NousResearch/hermes-agent/<commit>/install.ps1` with
  SHA-256 + HUMAN_APPROVAL_REQUIRED — proving Hermes is a pinned upstream artifact, not an HGK fork.
  Blueprint §19 tool ledger lists `hermes` as CORE/global_orchestration with
  `No auto-promotion; CR + independent regression required` (**L1596**).

## Blueprint §/anchors for orchestration & isolation (quote these)

- **§6.4 Hard vs soft enforcement** (L524-535): Hermes Profile = "runtime persona, NOT OS sandbox";
  hard boundaries only from Windows identity/ACL/Codex sandbox/bare remote/Publisher identity; P0 does
  NOT claim profile ACL. **⇒ HGK-side guards are config-level, never OS-sandbox claims.**
- **§7.1** (L556): "Profile隔離 Hermes config/session/memory/skills；Kanban board是同一 Hermes home 的
  shared coordination primitive."
- **§8.1** (L624): Kanban per-board SQLite = P0 global task lifecycle; delegate_task/Hermes Subagent /
  Codex Subagent must NOT create a second durable truth.
- **§8.5** (L707-708): one bounded task → one Kanban worker (parent Card = durable owner);
  `delegate_task`/Sub-Agent = short read-only exploration inside default runtime, durable owner =
  parent Card, writer = none.
- **§9.3** (L849): "Worker只收 frozen ContextPack，不傳未治理 chat history" — context isolation contract.
- **§8.2** (L644-646): `required_worker_env: HERMES_KANBAN_BOARD / HERMES_KANBAN_TASK` — worker env contract.

## RBWI WP contracts for process / env / tool isolation (Group-07)

- **WP-06 Hermes Workspace/Runtime**: integrate Hermes "以 adapter 方式…而不讓 Hermes 成為 authoritative
  control plane"; map Hermes to planning/routing/proposal ports, no canonical write / release rights
  (**L2125/2157/2193**); rollback = disable adapter/gateway, revoke token, export+isolate Hermes state.
- **WP-09 Bounded Multi-Agent/A2A**: "A2A message 只傳 typed artifacts/refs，不傳隱藏推理或未過濾
  secrets"; detect double writer / stale lease / duplicate effect / out-of-order (**L2497/2564**);
  non_scope: no two agents writing same authoritative body (**L2526**).
- **WP-10 Harness & Side-effect**: capture process/file/network/tool call/exit code, kill/quarantine;
  "不以 Prompt 警告取代 sandbox、ACL、approval 或 tool-level control" (**L2623/2652**).
- **Tool adoption gate (Group-04 L206, SRC-069)**: `P0_EXTERNAL_TOOL_AND_OSS_ADOPTION_GATE_REQUIRED=YES /
  RAW_TOOL_ADOPTION_FROM_CHAT=NO / TOOL_CANDIDATE_AUTO_ADOPT=NO`.
- All FINAL_r2 WPs: `runtime_status: NOT_EXECUTED / NOT_RUN` — never infer runtime/production pass.

## Claim-ceiling vocabulary (must be carried verbatim in any proposal)

- Current ceiling for the whole PACK: `BODY_SUBSTANTIVE_PASS_LOCAL_WITH_TT / RUNTIME_NOT_EXECUTED /
  INDEPENDENT_ACCEPTANCE_NOT_EXECUTED / PRODUCTION_PASS_NOT_CLAIMED` — PACK **L98**.
- Edge clause shared by every H2-xx: "claim_ceiling=BODY_SUBSTANTIVE_PASS_LOCAL_WITH_TT; do not infer
  provider activation or production admission" (**L587** representative).
- Source-to-Clause precision: high-risk clauses need an exact `SRC-nnnnn#heading` / KP ID / DOC anchor /
  Human Decision ID — never a filename/TOC label (**L997-1002**).

## Apply to a runtime-defect remediation (the pattern that works)

For a defect in an UPSTREAM tool's runtime behavior (e.g. the `HERMES_DELEGATED_CHILD_CONTEXT=1`
session-env leak — see `delegation-marker-env-leak.md` for the mechanism), the compliant split is
THREE layers, all required:

1. **Root fix = upstream patch** in the tool's codebase (HGK does NOT own/fork it). Ship as a
   pinned/vendored patch tracked in `versions.lock.yaml` + Version-Alias ledger (PACK L1084-1098);
   old body = REGRESSION_ONLY, no inherited runtime claim (**L979**).
2. **HGK records evidence/acceptance**: open CR + named TT; write a Normative Claim Card (schema
   L943-960) with status starting `TEMP_CLOSED_WITH_TT`; add negative/upgrade-regression fixture
   (readback before Kanban admission). Authority to AUTHORIZE the patch = A0 Current Human PATCH
   Authority (conflict table L962-971).
3. **HGK-side wrapper**: ALLOWED as config-level guardrail / defense-in-depth (scrub/deny the env
   marker + readback), but per §6.4 it must NOT be claimed as an OS process sandbox, and it is NOT a
   substitute for the upstream fix (REQ-128: contract precedes implementation).

**Do NOT** claim "patched ⇒ production-ready": that violates the claim ceiling (REQ-124 risk:
NOT_EXECUTED misread as available capability).

## Pitfalls
- The giant PACK body is mostly boilerplate — read chapter bodies + RBWI Groups + 藍圖 for substance.
- Directory names have the `HG-KSEOS_` prefix (e.g. `HG-KSEOS_實作RBWI_WP_控制工件_PACK_FINAL_r2`),
  which trips naive `ls` — use `ls -d */` to discover exact names before path-building.
- FINAL_r2 RBWI pack supersedes the older `RBWI_WP_CONTROL_PACK` — cite Group-04/05/07 of FINAL_r2.
- All quotes must be re-verified against the file at read time (r2 is a body-replacement; r1 claims
  like `PASS_BODY_WITH_TT` are not inherited).
