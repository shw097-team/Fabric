---
name: hgk-governed-execution
description: "Use for governed cross-stack acceptance under HG-KSEOS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [hgk, sqs, governance, kanban, swarm, codex, shared-spine, evidence, acceptance]
---

# HGK Governed Execution (cross-stack acceptance / canary tasks)

The user's recurring class of work: run a governed acceptance/canary task across the
HG-KSEOS stack — HGK as the sole governance control plane, Hermes as the orchestration
plane, Codex CLI as the primary implementation/execution worker, SQS-THC as the domain
stack — and freeze byte-identical evidence into three review roots. Task A / Task A-2 /
RP-001 / RP-002 all follow this pattern; future tasks will too.

## When to use
- The user asks whether an upgrade / patch / self-evolution change **survived another
  session's work, or was overwritten / regressed** ("是否被整合保留? 還是被覆蓋造成升級倒退?")
  → run `references/cross-session-integrity.md` (per-item survival verdicts +
  status-marker discipline) BEFORE claiming any status.
- The user asks **"is this order 100% complete / `是否已解決` all the problems and recommendations in
  those reports?"** → run `references/order-completion-audit.md` and answer from a per-deliverable audit
  of the ORDER TEXT against the filesystem. Verified blockers are NOT order completion: an order that
  names required artifacts per gate (reconciliation record, TT/CR delta, scan receipts, typed-lineage
  receipt, compiler-receipt predicates, a fixed final-report shape with a hash register) is satisfied
  only when EACH named artifact exists and is internally coherent. Answer in the standing three-state
  discipline — implemented / locally+independently verified / externally accepted — and list explicitly
  what is NOT done. Never infer completion from green verdicts, and never self-issue the external one.
- A prompt is tagged `FAIL_CLOSED` / `EVIDENCE_FIRST` / `KANBAN_SWARM_REQUIRED` /
  `CODEX_PRIMARY` and references HG-KSEOS, SQS-THC, or Fabric evidence roots.
- You must admit a WorkOrder through the HGK Shared Spine, or freeze mirrored evidence
  into `HGK|SQS|Fabric\evidence\review\`.
- You must prove Kanban + genuine parallel Swarm lanes + a real Codex process spawn.
- Operability ChangeSets (A-3 class): README/User Guide/Skill upgrades, GPT steering
  layers, auto-route proofs, governed self-evolution canaries, cold-start canaries —
  same admission → auto-route → Kanban/Swarm → Codex → evidence freeze pipeline, plus
  the evolution chain (§Step 8) and CAPC Gate-A3-0 contract exercise
  (`references/capc-contract-building.md`).
- Thin FINAL-CLOSURE / resume rounds after an accepted ChangeSet (doctor repair,
  WorkOrder state, docs currentness, worktree requalification, evolution HITL gate,
  evidence reseal) — see `references/final-closure-resume.md`.
- Read-only SQS-THC data-plane cross-confirmation (台股歷史資料庫 vs Shioaji-first
  blueprint, 知識庫 legacy disambiguation) — see `references/sqs-data-plane-verification.md`.
- 當日沖銷(T0) 主軸/當沖方法制定 research across the FOUR authority families
  (RBWI + FSDT DOC + TW-ICT v3.0 + SQS-THC 工程) — T0 axis, Session Phase Tree 時間窗,
  SessionCandidatePool-S1, SetupQualification, 盤中 JobCards, DOC-05 權威鏈, MTH/CMP 當沖技
  — see `references/daytrading-t0-axis-authoritative-chain.md`.


## Entry routing map (SKCV-20261014 extraction - refusal-first)

This main entry keeps the inlined core: frontmatter/identity/triggers, architecture +
execution invariants 1-11, and the mandatory local pre-action/authorization hard gates
(Step 9-0 / Step 9-0a). Every other original byte was moved verbatim, without decode.

| Need | Read (verbatim original text) |
|---|---|
| Skill routing map, RP-002 v2.0 status | `references/topics/construction-wave-and-remaining-procedures.md` (slice 1) |
| External-challenge closure, independent acceptance lane, Steps 0-8, watchdog, evidence home/closure pipelines (6B/6C/6D), Step 10A, pitfalls | same file (slice 3) |
| Step 9 operations detail, Step 9A, Step 10, Support files | same file (slice 5) |
| Exact byte provenance / reconstruction | `entry_map.json` (per-slice source+destination offsets and sha256) |

Construction-wave and remaining procedures route to their original moved bytes in the
reference above. Refusal-first: do NOT reconstruct or paraphrase those procedures from
memory. If the reference is missing, a slice is missing/reordered/corrupt, or a digest
disagrees with `entry_map.json`, STOP and report the `ERR_ENTRY_MAP_*` code - never return
a green result for an incomplete entry. Moved text carries the same authority; this
pointer adds none.
## Architecture invariants (never violate)

```text
HG-KSEOS  = sole Governance / Normative / WorkOrder / Evidence / Release control plane
Hermes    = governed Runtime / Orchestration Plane (Kanban, dispatch, heartbeat, swarm)
Codex CLI = primary bounded implementation/execution worker
SQS-THC   = Financial Product / Domain Stack under HGK governance
src/kernel/fsdt = financial truth owner (TW-ICT Financial Contract Kernel)
```

Never create a second orchestrator, task DB, Kanban engine, reducer, or evidence
authority. No live broker write, no production claim. RP-002 v2.0: Stage-1
(FABRIC-FOUNDATION) was executed 2026-08-12 per explicit user direction —
project state ACTIVE, REQ-RP2-STAGE1-001 FROZEN, terminal
PENDING_EXTERNAL_META_ACCEPTANCE (external GPT-5.6 Sol receipt required before
STAGE-1-SEAL; Stage-2 = RP002-STAGE-HGK, next gate K1). Do NOT issue the seal,
self-approve the external receipt, or start Stage-2 without the user.

## Execution-method invariants (HARD — default-on for large governed tasks)

**Trigger: ANY task that is NOT pure Q&A chat** — every HGK control-plane task
(user-uploaded PROMPT.md, implementation, acceptance, stage execution,
continuation, upgrade, WorkOrder-bearing work, evidence closure, even a
single-file artifact generation inside a governed stage) MUST default-enable
ALL SIX execution surfaces. Do not wait to be asked; do not treat "already
enabled once this session" as "enabled for this artifact".

The six surfaces: **HGK** (every durable mutation rides a Shared Spine
WorkOrder/ExecutionBinding lineage — maker-direct writes without a WorkOrder
binding are NOT governed execution), **KANBAN**, **SWARM**, **GSTACK**,
**OPENSPEC**, **CODEX** (writer=codex WorkOrders get a real spawn per
deliverable batch, not once per stage).

Applies to RP-00x Stage executions, A2/A3-class canaries, continuations,
upgrades, and any WorkOrder-bearing task. These surfaces are DEFAULT-ON;
do not wait to be asked.

1. **HGK control-plane binding is default-on.** Every durable mutation must be
   traceable to the admitted WorkOrder (REQ→TS→WO lineage in Shared Spine) and,
   where the gate requires, an ExecutionBinding. Maker-direct writes inside a
   governed stage are execution-method gaps unless they are explicitly
   WorkOrder-scoped evidence generation.
2. **Kanban tracking is default-on, not optional.** Create the canonical board
   + a gate task DAG and assign/claim/heartbeat/complete every card. Do NOT run
   a governed task maker-direct without a Kanban trace.
3. **Swarm independent verification is default-on.** Use `hermes kanban swarm`
   or `delegate_task` dual-lane leaves for independent readback of gate evidence
   (denominator counts, receipts, classification). Record overlap interval.
4. **Codex tracked writes are default-on for WorkOrders with writer=codex.** Real
   spawn on the sealed lane + provider receipt + independent readback hash.
5. **gstack/OpenSpec route check is default-on.** Confirm `named_methods` registry
   ACTIVE_SELECTED state and run `route(flow)` for the task flow; record
   selected_route + reason_code as evidence even when the result is NATIVE.
6. **`router → NATIVE/DIRECT` decides the orchestration lane only.** It NEVER
   licenses skipping Kanban/Swarm/Codex/gstack/OpenSpec. Lane ≠ execution method.
   (This exact misreading was the R1 root cause of the Stage-1 gap; the user's
   correction caught it.)
7. **Registry stale state is a repairable defect, not an excuse.** If a registry
   field (e.g. `config/hermes.json kanban_state: NOT_RESTORED_REBUILD_REQUIRED`)
   contradicts live evidence (kanban.db exists, CLI surface works), treat it as a
   smallest-repair candidate: backup → minimal edit → readback/hash → focused
   regression (doctor) → rerun. Never read "not ready" as "therefore don't use".
8. **Stage switch = rebuild execution surfaces (learned Stage-2, 2026-08-12).**
   Moving from one Stage to the next (e.g. RP002-STAGE-FABRIC → RP002-STAGE-HGK)
   does NOT inherit the previous Stage's board/lanes as current. You must:
   - create the NEW canonical board (Stage-2 r2 mandates `RP002-FABRIC-BOOTSTRAP`;
     a prior Stage-1 board is not a substitute — B1 rejects inherited boards);
   - create the new gate DAG (K1→D1→…→SEAL) with claim/heartbeat/complete;
   - run NEW Swarm independent lanes for the new Stage's gates (a Stage-1
     delegation batch does not verify Stage-2 K1/D1 artifacts);
   - make Codex actually execute the new WorkOrder (writer=codex means a real
     spawn + provider receipt + independent readback for THAT Stage's deliverables —
     previous Stage Codex writes are not this Stage's tracked implementation).
   This is the same R1 defect (lane ≠ execution method) re-appearing at Stage
   granularity; the fix is to treat each Stage as a fresh execution-surface
   closure.
9. **Every governed round closes with acceptance + single evidence MD
   (audit-proof close-out, verified 2026-08-13 FAR first-use).** The close-out
   contract applies to EVERY WorkOrder-bearing round — including follow-up,
   continuation, first-use/dogfood, and "small" patch rounds. Never treat a small
   round as exempt: (a) run a fresh-context independent acceptance lane
   (`delegate_task` VERIFY_ONLY leaf; record `ACCEPTANCE_OFFICER_VERDICT=PASS`);
 (b) generate a single evidence MD (claim ceiling / binding / artifacts raw
   index / gates / nonclaims / STOP) LAST per freeze order and mirror
   byte-identical to HGK|Fabric|SQS `evidence\review\` with SHA-256 equality;
 (c) keep the claim ceiling honest. Observed gap: the FAR first-use round had a
   challenge lane but no AO lane + no evidence MD; the user's audit questions
   ("內部驗收? 單一MD? 結果?") exposed it — preempt by always closing the loop.

10. **MVLT round lessons (verified 2026-08-24, WO-MVLT-AB experiment):**
   (a) **Admission ≠ execution.** Creating the Kanban board/DAG + admitting
   WorkOrders does NOT constitute governed execution — an earlier round claimed
   governance while silently skipping assign/claim/heartbeat/complete, Swarm
   delegation, and the freeze-order pipeline; only the independent AO lane caught
   it (the drift itself is the strongest argument FOR governance). Every card
   needs real CLI receipts; every Swarm lane needs a real delegate_task log.
   (b) **Spine DELIVERED fail-closes** (`ERR_PENDING_WORK_CANNOT_DELIVER`) while
   any project WorkOrder lacks a result — call
   `spine.record_workorder_result(wo_id, writer='codex', checker=<different>,
   verdict='PASS', evidence_refs=[...])` first (writer==checker raises
   ERR_WORKORDER_SELF_REVIEW). This fail-closed gate is correct behavior; do not
   bypass it.
   (c) **Dual-state semantics:** `projects.state` is the registry/product-root
   layer (created once as 'ACTIVE', never updated by the lifecycle controller);
   delivery truth lives ONLY in `project_lifecycles.state` (=DELIVERED).
   Existing precedent: RP-001 shows DELIVERED+ACTIVE too. An independent fresh AO
   WILL flag ACTIVE-vs-DELIVERED as PARTIAL unless the evidence MD states this
   invariant preemptively — write the VALID_DELIVERED_ACTIVE_REGISTRY combination
   into the MD before freezing.

11. **Maker-side measurement integrity: a gate's own probes must be able to fail.** Before
   handing gate evidence to any checker: (a) no hardcoded expected result — invoke the real
   production surface and ship a control case the mechanism ACCEPTS plus a case it must
   REJECT; (b) an aggregate PASS field must never be satisfiable by not-applicable /
   zero-denominator results; (c) assert a registry lookup HIT with both key forms rather than
   a silent `.get(key, default)` fall-through, which turns a probe into a no-op while the
   receipt still reads PASS; (d) match whole tokens with a boundary, never a short suffix
   substring; (e) drive the token set from the authoritative register, not a hand-written
   regex — when a probe finds zero of N declared items, suspect the extractor before the
   corpus; (f) while a fix is unverified the stated result is `PARTIAL` (pending), not PASS,
   and the run-level verdict lives in exactly ONE artifact.
   (g) **Prove the checker's FAILURE path actually fires — by injection — and never claim its stated rule is an
   EXACT description of the code.** An error list that is initialised and never appended to makes
   `assert not errors` always true — the checker is VACUOUS and a receipt claiming it "fails on a
   contradiction" is simply untrue. Read the error path, not just the pass path; then inject each
   contradiction SHAPE the checker claims to catch (wrong value for a named target; the same kind of
   value under a differently-named key; a `commit:path` reference carrying a DIFFERENT blob's hash; a
   named target that resolves to nothing; a case-variant digest; a value that is a bare array element)
   and require ALL of them to be caught, asserting non-vacuity inside the run so a regression aborts the
   build. Three rules that each returned a finding before being learned: (1) **pair every declared hash
   with ITS OWN reference** — an object holding several refs gets each hash compared against whichever
   ref the walker reaches first, so your validator errors against a CORRECT artifact; derive the target
   from the hash key's stem (`X_sha256` -> `X_ref`/`X_path`/`X_file`) and give that name-affine tier
   PRECEDENCE over a generic path-key list. (2) **"every declared value" must include bare list
   elements**, or a hash sitting as an array element is never inspected. (3) **Do not write the sentence
   "exact description of the implementation"** — it is falsifiable and a reviewer will falsify it; any
   wording broader than the code (a restated key order, "the first present" where the code collects all
   present, "always an error" where it errors only when nothing else resolved) IS the finding. State the
   rule as a behavioural description, say the code is authoritative, enumerate what it does not cover in
   `known_limitations` (including any counterexample already found), and point at the constant the code
   reads instead of restating an order. Prefer CUTTING the claim over growing the validator, and put
   every count you quote (items, hashes checked, shapes caught, exempted references) INSIDE the artifact
   — a number that lives only in your message is unverifiable. Full rules, the readback pattern for
   artifacts that cannot contain their own hash, and the invalidation cascade:
   `references/self-verifying-probe-authoring.md`.

## Step 9 — FDA / Windows desktop automation with Cua (verified 2026-08-13)

> **FDA 操作路由（2026-08-14 r11 驗收通過後）**: 任何 XQ/XS 桌面操作請載入專屬 skill
> **`fda-desktop-automation`**（完整流程路由 §0 QUICKSTART、SSC-V2 異常查螢幕含 hidden/小視窗、
> 零滑鼠硬路由、control IDs、陷阱）。三鐵律：① 異常→先查螢幕實況（screen_state_check.py），
> XQ 很少真卡死，通常是沒看見的小視窗需確認（BM_CLICK 無效→WM_CLOSE）；② 不和用戶搶鍵盤滑鼠
> （禁 click_input/set_focus/foreground/SendInput）；③ REUSE-FIRST 查 FDA_ASSET_REGISTRY.json。

### Step 9-0 — FDA 執行前強制序列 (HARD GATE 0, user-mandated 2026-08-14 UD-FDA-UPGRADE-HITL-2026-08-14-001)

**ANY FDA-class desktop automation (XQ/XS/PAPER/radar/cua/ufo2 work) MUST start here.
Step 9-0 is the EXECUTION of Step 10A rule 3 — it turns the prose "verify-and-call
qualified assets" rule into a mechanical gate.**

1. **Run the preflight gate FIRST, before ANY automation:**
   `python "C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\fda_preflight.py" --action-class <CLASS>`
   (assets are hardcoded in the script; the venv python is
   `C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe`). No FDA operation
   may begin before preflight has run and its output has been read.
2. **NEW/EDITED automation scripts must pass the script guard BEFORE first
   execution:** any new or modified automation script (`.py` used to drive FDA
   operations) is scanned for mouse-stealing / focus-stealing APIs by
   `fda_script_guard.py` — `python "C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\fda_script_guard.py" <script.py>`
   (exit 0 = CLEAN, exit 1 = BLOCKED; quarantines violating scripts). Dual copy:
   `HG-KSEOS\var\fda\fda_script_guard.py` (identical; keep in sync). The guard is a
   STATIC source scan (click_input/set_focus/send_keystrokes/SetCursorPos/SendInput/
   SetForegroundWindow/mouse_event/keybd_event/bring_to_front/foreground) — it does
   NOT replace the environment preflight in rule 1; both run: rule 1 gates the
   environment/route, rule 2 gates the script content. Full details:
   `fda-desktop-automation-cua.md` §15.3.
3. **PASS (exit 0) → proceed using ONLY the reported `allowed_channels`**
   (CUA = `CUA_BACKGROUND_ONLY` + `WIN32_MESSAGES_ONLY`). Anything else — foreground,
   pixel-first, click_input/set_focus/send_keystrokes/SendInput/SetCursorPos — is
   PROHIBITED regardless of what the UI suggests (§13/§14/§15).
4. **BLOCKED (exit 2) → STOP.** Report to the user with the `blocked_reasons` list,
   record a defect, and attempt NO install / downgrade / provider-swap / retry. The
   assets are already qualified — a missing asset is a defect to surface, not a
   license to re-install.
5. **Mid-run anomaly (any op fails) → run `screen_state_check.py` FIRST** (read-only
   diagnostic, same references dir; fixed route per `fda-desktop-automation-cua.md`
   §15.1/§15.2), then pause and present the user 2-4 options (incl. HITL manual
   assist) per §16/§17 — never blind-retry.
6. If preflight itself errors (yaml/schema/route exception), treat as BLOCKED with
   the error text as the reason.

### Step 9-0a — FDA 授權閘 (HARD GATE 0a, user-mandated 2026-08-15 UD-FDA-GUARDRAIL-2026-08-15-001, WO-HGK-FDA-GUARD-IMPL-001)

**Hermes 嚴格禁止自動調用 FDA，除非滿足以下三條件之一：**

1. **用戶指令明確提及使用 FDA** — `pre_llm_call` mint hook（`references/fda_guard_mint.py`）掃描用戶原文（意圖動詞 ∧ FDA 目標詞雙條件）→ 寫入 session 授權 token（`~/.hermes/var/fda-auth/<session_id>.json`，TTL 1h）。
2. **執行既有的已登記受治理路由** — `references/FDA_ROUTE_REGISTRY.json` 中 status=ACTIVE 的 route（WO-only mutation + digest 驗證；route 不得引用非 QUALIFIED matrix row）。
3. **任務執行必須使用 FDA** — 先主動暫停任務、詢問用戶、取得明確授權（用戶授權回覆 → 下一 turn mint → 放行）。

**機械強制（多層，不可只靠記憶）：**
- **A 層**：`pre_tool_call` guard hook（`references/fda_guard_hook.py`，fail_closed: true）——FDA 相關 tool call（terminal/computer_use/execute_code/delegate_task/write_file/patch）無 token、無 route → `{"action":"block"}` + exit 2 → 模型被迫「暫停+詢問」。
- **B 層**：`fda_preflight.py` 新增 `--route-id <ID>` / `--auth-token <FILE>`——`--action-class`（操作意圖）無授權 → exit 2 `no_authorization:<reason>`；`--check-assets`/`--list` 診斷模式免授權。
- **C 層**：`approvals.deny`（config.yaml）——`*quarantined_violations*`、`*cua-driver*foreground*`、`*cua-driver*bring_to_front*` 無條件硬擋（**先於 --yolo**；勿加 `*python*var/fda/*`——會誤擋合法 fda_run 路由執行）。
- **allowlist**：`references/FDA_ROUTE_REGISTRY.json`（schema FDA-ROUTE-REGISTRY/1；新增/撤銷 route 一律經 HGK WorkOrder + 用戶確認）。

**三條件皆無 → STOP + 主動詢問用戶**（BLOCK message 內建條件 3 指令）。任何 FDA 操作前先自問：本次授權來源是 1/2/3 哪一個？答不出來就是條件 3 路徑。

