# WRITER BRIEF — EXECUTE lane (CODEX CLI, opencode-go/minimax-m3.1-flash-free)

## FIRST LINE OF YOUR OUTPUT
Print exactly this line first, before anything else:

    ARM-NONCE: SBL-RCA-027-EXEC

Then do the work.

## What this round is
A governed FAR research round under HG-KSEOS admission:
`REQ-HGK-PRJ-SBL-HGK-RCA-20261022` (FROZEN) / `TS-req-hgk-prj-sbl-hgk-rca-20261022` (ADMITTED) /
`WO-TS-REQ-HGK-PRJ-SBL-HGK-RCA-20261022-EXEC` (CREATED, writer = you).
Your cwd IS the admitted writable root. Do not write outside it. Do not touch C:/Projects/Agent_Workspace/HG-KSEOS,
/SBL, /Fabric/FABRIC or any other repository path — read-only access to them is not needed and not granted.

## Read these (all in your cwd) — in this order
1. `OWNER_MANDATE.txt` — the owner's frozen words, the required model plan and the execution requirements.
2. `ResearchRequest.yaml` — the admitted question, sub-questions Q1..Q4, claim ceiling.
3. `ResearchPlan.yaml` — route, swarm split, gates G1..G4.
4. `evidence/W1_fabric_integration.md` — is SBL integrated into the Fabric governance contract?
5. `evidence/W2_base_drift.md` — is SBL on the current HG-KSEOS base? (numbers re-derived by the orchestrator)
6. `evidence/W3_capability_probe.md` — seven capability surfaces, measured.
7. `evidence/W4_performance_delta.md` — measured SBL+HGK vs HGK-only comparison.
8. `ROUTE_DECISION.json`, `GSTACK_ROUTE_DECISION.json` — real route receipts.

## Produce exactly these six files (overwrite nothing else)

### 1. `ResearchSynthesis.md` — the report the owner asked for (Traditional Chinese, zh-TW)
Structure it EXACTLY like this, and keep every claim traceable to a locator you took from the evidence files
(format: `path:line` or `path` + the quoted command/exit code):

```
# SBL × HG-KSEOS 降級根因研究報告（FAR-20261022-027）
## 0. 一句話結論
## 1. 量測基準與方法（admission、車道、模型實測、證據來源）
## 2. 問題一：SBL 是否完整且正確接入 Fabric 治理契約
## 3. 問題二：SBL 是否以「現版 HG-KSEOS」為工程基座升級
## 4. 問題三：為何「SBL & HG-KSEOS」比只用「HG-KSEOS」更差（把每個成因分類為 已量測 / 推論 / 證據不支持）
## 5. 問題四：七大能力面實測狀態（KANBAN / SWARM / GSTACK / OPENSPEC / CODEX CLI / SUB-AGENT / 自檢測-自修補-自驗收-自進化）
## 6. 根因清單（依「結構性 / 流程性 / 宣告性」分組，每條附證據 locator 與可修復槓桿）
## 7. 低摩擦修復選項（每項：動作、成本、風險、是否需 owner 決策）
## 8. 未量測與不在範圍（NOT_MEASURABLE / OUT_OF_SCOPE，逐項寫原因）
## 9. 宣稱上限（claim ceiling）
```

Rules for the synthesis:
- Q4's own headline answer must be stated plainly: the owner asked whether SBL&HG-KSEOS **really can**
  enable all seven surfaces with automated self-detect / self-repair / self-accept. Answer per surface from
  W3's measured states; do not upgrade a PARTIAL to PASS, and do not soften a FAIL.
- Highlight the SoD collision as the load-bearing conflict: SBL's own label is "self-accept", HG-KSEOS
  refuses `writer == checker` (`ERR_WORKORDER_SELF_REVIEW`), and W3 measured SBL raising
  `SBL_E_SELF_CHECK_FORBIDDEN`. The reconcilable reading is "self-detect + self-repair are legitimate;
  self-ACCEPT must be an independent lane" — say that explicitly and cite both locators.
- The performance question must be answered honestly: W4 measured recurring SBL non-acceptance and a
  large open backlog, but a material time/money premium is NOT supported by the artefacts. Do not invent a
  duration, a percentage, or a cost figure.
- Do not write "exact description", do not claim acceptance, do not claim installation or native integration.
- Language: zh-TW prose, English identifiers.

### 2. `FINDINGS.tsv`
Header exactly: `id\tclass\tstatement\tevidence`
`class` ∈ {structural, process, declarative, defect, method, claim}. One row per finding, ids F1..Fn, no gaps.
Take the findings from W1..W4 and the orchestrator's measured facts; compress duplicates (W4 reports "44 SBL
finding rows — not 44 unique defects"), and say nothing that a locator does not support.

### 3. `VERDICT.json`
Schema `FAR-VERDICT/1`. Required keys (mirror run 026's shape):
`schema, run_id ("FAR-20261022-027-sbl-hgk-degradation-rca"), captured_at_utc, ruling, mandate, answers{Q1..Q4},
capability_states{KANBAN,SWARM,GSTACK,OPENSPEC,CODEX_CLI,SUB_AGENTS,SELF_*}, root_cause_groups, claim_ceiling,
next_best_action, open_items[]`.
`mandate` must carry the model plan as MANDATE vs OBSERVED: PLAN deepseek-v4.1-flash (session plane),
EXECUTE opencode-go/minimax-m3.1-flash-free@rank1 (served, 3.78 s, usage ok), VERIFY
opencode-go/deepseek-v4.1-flash@rank4 (served, 2.50 s, usage ok), and must state that the pool's DECLARED
rank-1 for PLAN/VERIFY is openai-codex/gpt-6.1-sol and this round pinned the owner's arms instead
(pool `selection_semantics` permits it) — a disclosed deviation, not a silent substitution.

### 4. `DEVIATIONS.tsv`
Header exactly: `id\tclass\twhat\twhy\tceiling_effect`. Record at minimum: the declared-vs-pinned lane arms;
worker W2's write being refused by this session's pre-write guard and the orchestrator re-deriving its
numbers (so W2 carries no child self-report); W3's two surfaces that could not be fully exercised; the
adversarial-challenge FAR class routing to NATIVE_NO_CHALLENGE.

### 5. `ProposedEvolution.yaml`
Candidate-only evolution proposals (self-research → self-learning → self-iteration → self-evolution), each
with: `id, target (repo/path), change, why, evidence, cost, risk, owner_decision_required (true|false),
claim_ceiling: CANDIDATE_ONLY`. At least one item must address the vacuous version pin, one the missing
`hg_kseos` dependency/install wiring, one the self-accept vs SoD collision, one the un-drained SBL backlog.

### 6. `ResearchHandoff.yaml`
`run_id, verdict_ref, candidate_refs, residuals[] (each: id, owner, one_action, blocked_by), resume_command,
claim_ceiling`. Every residual must be OWNER-READY: one action, no open-ended question.

## Hard constraints
- Only the six files above. Do not edit `evidence/*`, do not create extra reports, no temp files left behind.
- No git commands that write (no commit/add/push/checkout).
- If a fact you need is absent from the evidence files, write `NOT_MEASURABLE` with the reason — never
  manufacture a number, a duration, a percentage or a passing test.
- Your output is CANDIDATE research, not an acceptance. Say so in the files themselves.
