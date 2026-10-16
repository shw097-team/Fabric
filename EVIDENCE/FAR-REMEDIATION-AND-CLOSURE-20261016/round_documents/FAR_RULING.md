# FAR 研究報告與最佳工程裁決 — FAR-REMEDIATION-AND-CLOSURE-20261016

Round `FAR-REMEDIATION-AND-CLOSURE-20261016`（session `20261016_104922_d455e7`，第二回合）
格式沿用 `var/LANE-ENFORCEMENT-APPLY-20261015/FAR-GAP-RULING-20261015/FAR_PLAN_ORCHESTRATOR_MODEL_RULING.md`。
研究對象：`RESIDUAL_INVENTORY.json` 全部 22 項（9 residual／3 gap／3 owner_decision／6 closure／1 publication）。

## 一、研究問題

本 session 的殘留帳（`LANE-RELIABILITY-CLOSURE-20261016/ROUND_CLOSURE.json`）是同一個地方把「系統還剩
什麼偏離」寫下來的唯一位置，而這些項性質不同：一個 config 列、一個已驗證但未推廣的變更、一個
owner 已下令的模型重疊、一個環境受限的測試、一個回合形狀的可靠性修補、以及結案與發布義務。

所以一個問題同時決定全部處置：**哪些項需要工程（do）、哪些項需要一個決策（decide）、哪些項應該被
重新分類到不存在（drop）？** 判斷準則固定為四條，全部由 owner 的目標導出：**低阻力、高可行性、高工程
必要性、不過度工程化**，且必須對齊本 session 目標（三車道模型選擇可用且可靠）。

## 二、事實（全部來自實地讀取，非推論）

### 2.1 F1 的前提已在本 session 內失效（關鍵新事實）

`config/lane-routing-registry.yaml` §`routes[].PLAN` 目前逐字為：

| field | value |
|---|---|
| `provider` / `model` | `opencode-go` / `glm-5.3-flash` |
| `selection_authority` | `owner-order-20261015-plan-model-rebind-glm` |
| `arms[openai-codex/gpt-6.1-sol].usable_now` | `QUOTA_429_2026-10-15` |
| `admission_status` | `UNPROVEN` |

該列之所以指向 `glm-5.3-flash`，理由寫在同一列裡：`openai-codex/gpt-6.1-sol` 於 **2026-10-15** 因
`status=429` 不可用。**本 session 實測該理由已不成立**：

- PLAN 平面：`PLAN_LANE_PROBE_OK`、`PLAN_TOOL_PROBE_OK`（可執行工具，非只回話）；
- governed profile 自身 `state.db::sessions` 出現新服務列
  `gpt-6.1-sol / openai-codex / https://chatgpt.com/backend-api/codex / subscription_included`；
- VERIFY/SECURITY 車道兩次（v1、v2）皆 `required_arm == served_arm == openai-codex/gpt-6.1-sol`
  且 `usage_receipt_ok: true`。

### 2.2 五個 PLAN 宣告面中四個一致，第五個是唯一離群

`FINDINGS_F1_PLAN_ROUTE_OUTLIER.md` 的五面比較仍然成立，且本回合複測未變：pool rank-1、registry
`sod_invariants`、`tests/test_lane_policy.py` owner chain、本 session `role_mandate.json` 皆為
`openai-codex/gpt-6.1-sol`；只有 `routes[].PLAN` 為 `opencode-go/glm-5.3-flash`。後果是 repo **自己的**
conformance gate 在 canonical 上為紅。

### 2.3 owner 在本回合下的令與 2.1 的舊令衝突，且目標與 pool 一致

本回合 owner 明令：PLAN & Orchestrator = `GPT 6.1 SOL-MEDIUM (OPEN AI OAuth)`。這與
`owner-order-20261015-plan-model-rebind-glm` 直接衝突，而與其餘四個宣告面一致。**衝突的解法不需要新
工程，只需要把舊令的前提已失效一事記錄下來，並換上在效的令。**

### 2.4 已驗證但未推廣的變更（GAP-PROMOTION）

前一回合的 frozen candidate（200 檔，aggregate `c2527970…`）被獨立驗收官判為 `claim_B AGREE` /
`claim_C AGREE`（V2；V1 因我自己的 brief 矛盾回 UNCERTAIN，原文保留）。同一組 fixture 在 canonical 為
`exit 3`、在 candidate 為 `exit 0 / allow / no-session-id-unattributable`——**canonical 目前仍帶著那個
outage**。

### 2.5 可靠性缺陷的形狀已由量測定位（非猜測）

本 session 三次 EXECUTE：(BC1) 900.07s 逾時、(BC2) 量測後由 orchestrator 終止、(BC3) **74.25s 完成**。
BC3 與前兩者唯一的差別是**被要求只編輯、不執行**。故失敗面在「命令執行」，不在模型或車道；BC1 的
attempt 層歸屬仍指名同一 arm，但其聚合判定是失敗（`served_arm: null`）。

### 2.6 環境受限項（E11）

前 session 記載 E11／C2 五案「需要 relay `auth.json` metadata，在本沙箱失敗」。本回合派 sub-agent
獨立複查並要求逐案給出 file:line 與實際錯誤文字，結論見第四節 R4（該節在證據落地後定稿）。

## 三、最佳工程裁決

準則：**低阻力、高可行、高工程必要性、不過度工程化、對齊本 session 目標。** 每項先列裁決，再列被
否決的選項與否決理由——被否決的選項必須留下，否則無法區分「想過」與「沒想到」。

---

### R1 — GAP-F1 ＋ GAP-OWNER-ORDER-STALE → **REBIND（do）**

**裁決**：把 `routes[].PLAN` 重綁為 `openai-codex` / `gpt-6.1-sol` / `reasoning_effort: medium` /
`auth: openai_oauth` / `oauth: true`，並：

1. `selection_authority` 改為本回合在效的令（`owner-order-20261016-plan-model-rebind-gpt61-sol`）；
2. 移除／改寫 `arms[openai-codex].usable_now` 的 429 標記，改記本 session 的實測（並保留該 429 的歷史
   為 `prior_revision_note`，不刪史）；
3. `admission_status` 由 `UNPROVEN` 改為本 session 的實測值；
4. registry `epoch` 20 → 21，並在 provenance 段記明「本次重綁的前提是 2026-10-16 實測，取代
   2026-10-15 的 429 前提」。

**為何是最高必要性**：owner 指定的車道模型，與 registry 實際選擇的模型不一致；不修，則 repo 自己的
conformance gate 永遠為紅，且下一回合的 PLAN 車道選型會再次以此列為準。

**被否決的選項**

| 選項 | 否決理由 |
|---|---|
| 不動（僅保留 finding） | repo 自己的 gate 持續為紅；且舊令前提已實測失效，留著等於讓已知過期的宣告繼續當權威 |
| 反向對齊：把 pool／測試／mandate 改成 `glm-5.3-flash` | 直接違反本回合 owner 令，且要改四個一致的面去遷就一個離群面 |
| 一次同時清除所有歷史 arm 與 fallback | 過度工程化：fallback 鏈本身是刻意設計，破壞它會讓 429 再次發生時無路可退 |

---

### R2 — GAP-PROMOTION → **PROMOTE（do；owner 已於本回合授權執行）**

**裁決**：把 frozen candidate 的 **PROMOTE 集**（精確清單取自 sub-agent 的
`EVIDENCE_PROMOTION_SCOPE.json`，不憑記憶）套用到 canonical，逐檔備份、記前後 sha256，每項一個
WorkOrder。**此為「受 owner 前授權的 apply」，不是驗收**：套用後對外驗收仍為待辦。

**為何有必要**：`hgk-governed-runtime-controller.py` 的空白 session id outage 目前在 **canonical 產品
線仍是活的**；B 的努力軸在 canonical 仍不存在。留作 candidate-only 的唯一理由是「無推廣授權」，而該
理由在本回合已由 owner 解除。

**被否決的選項**

| 選項 | 否決理由 |
|---|---|
| 繼續只留 candidate | canonical 帶著已修好的 outage；且本回合 owner 明確要求執行裁決 |
| 只推 C（outage）不推 B（effort 軸） | B 已同強度驗證；少推一半會讓 effort 軸回退成「無人攔阻」 |
| 連 `var/` 回合產物一起推 | 把回合暫存物汙染產品線，且 sub-agent 的分類就是為此而做 |

---

### R3 — SOD006-C2 → **RECLASSIFY（decide 的結果：由 owner 令結案，非新決策）**

**裁決**：把 `sod_invariants.declared_conflicts[SOD006-C2]` 由 `OPEN_OWNER_ORDERED` 改為
`OWNER_ORDERED_IN_FORCE`，引用本回合的令（PLAN 與 VERIFY 同為 `openai-codex/gpt-6.1-sol`），並在該
衝突條目內明寫**剩餘的獨立性**：模型獨立性**刻意不存在**，仍保留的是流程／車道／證據路徑獨立，以及
「驗收官不評自家產物」的角色分離。

**為何不是「drop」也不是「do」**：owner 已下令兩道同模型，所以它不是待決策，也不是需要工程的偏離；
它是一個**已被下令接受的偏離**，正確處置是把狀態寫對，否則未來的稽核會把它當成未結項重複提起。

**被否決的選項**：把 VERIFY 換成第三個模型以恢復模型獨立性——直接違反 owner 令，且 owner 未授權。

---

### R4 — E11／C2 五案 → **RECLASSIFY 為環境受限（pending 證據定稿；principle 先定）**

**裁決原則**：若五案的失敗原因確實是缺一項**沙箱外**前置條件（relay `auth.json` metadata），則：

1. 分類為 `ENVIRONMENT_LIMITED_PRECONDITION`，並把前置條件寫成**可檢查的斷言**（例如：案件的失敗
   必須以「前置條件缺失」的具名理由呈現）；
2. 不得為了讓它變綠而刪除或整批 skip——那會把閘門變弱，是本裁決明確拒絕的方向；
3. 若證據顯示其實是產品缺陷，則改判為 `do`，並依 sub-agent 報告中最小可行修法執行。

**為何**：一個永遠掛著的「未結缺口」會讓殘留帳失真——讀者無法區分「產品壞了」與「這裡沒有那項設施」。

---

### R5 — 回合形狀 → **IMPLEMENT（do，加性）**

**裁決**：把本 session 量測到的修法**寫進工具**，而不是只寫進散文：在 `scripts/hgk-lane-dispatch.py`
新增一個**可選**的 `--turn-shape {normal,edit_only}`，`edit_only` 時在 prompt 前插入固定的 HARD RULES
區塊（禁止程序枚舉、禁止互動程式、只做寫入、不跑測試套件），並把所用的 shape 記入 `dispatch.json`。

**為何有必要**：同一形狀在本 session 造成 2 次各 900 秒的無效回合，修法已由量測確立；把修法留在
散文裡，下一個回合的人（或 agent）仍會重犯。

**被否決的選項**

| 選項 | 否決理由 |
|---|---|
| 只寫文件 | 已寫入技能，但工具不會因此改變行為；量測到的修法應固化在執行路徑上 |
| 預設改成 edit_only | 過度工程化且會移除「車道自證」的能力；使用者應能選擇 |
| 另建一個 wedge 偵測服務 | 明顯過度工程化：本 session 的偵測只需在既有 runner 內幾行 |
| 改寫 dispatcher 的既有旗標語意 | 加性原則是為了可回滾與可並存；改語意會讓既有回合的證據不可比 |

---

### R6 — CLOSE-01／CLOSE-02 ＋ 其餘 RES-* → **DO（結案與發布）**

**裁決**：寫 `ROUND_CLOSURE.json`（含逐項處置與批判上限）、`README.md`、`_handover/CHECKPOINT_*`，
經封包閘門與遠端回讀後開 PR。RES-* 中屬「已在本回合被 R1–R5 涵蓋或結案」的項，在其項內標明由哪一條
裁決結案；仍存續的（如 EXECUTE 樣本數、外部驗收未做）明確保留，不併入結案語句。

**被否決的選項**：把殘留帳清空以呈現「全數完成」——本 session 的批判上限要求相反的做法。

## 四、執行方案

依序執行；每一步都有回滾路徑與回執。

| 步 | 動作 | WorkOrder | 回滾 |
|---|---|---|---|
| E1 | 建 `admission.json`／`role_mandate.json`（三車道模型沿用 owner 令）並經 typed admission | `WO-FAR-20261016-ADMISSION` | 刪除本回合 admission |
| E2 | 建 KANBAN tasks＋`KANBAN_SWARM_GRAPH.json`；OPENSPEC change `hgk-far-remediation-20261016`（`--strict`） | — | 目錄自身 |
| E3 | **R1**：registry 重綁＋epoch 20→21（備份＋前後 sha256） | `WO-FAR-20261016-R1` | 從 `.bak` 還原 |
| E4 | **R3**：SOD006-C2 改判（同一次 registry 變更內完成） | `WO-FAR-20261016-R1` | 同上 |
| E5 | **R2**：依 `EVIDENCE_PROMOTION_SCOPE.json` 推廣 PROMOTE 集（逐檔備份） | `WO-FAR-20261016-R2` | 逐檔還原 |
| E6 | **R5**：EXECUTE 車道（edit-only）實作 `--turn-shape`；本回合即為其首次使用驗證 | `WO-FAR-20261016-R5` | `git checkout` 該檔 |
| E7 | 檢測清單 D01–D16 由 orchestrator 重導（不採信車道自述） | — | — |
| E8 | **VERIFY 車道**獨立複核 frozen subject（含 `subject_mutation` 判定） | — | — |
| E9 | 結案／移交／發布（封包閘門＋遠端回讀） | — | 分支可棄 |

## 五、claim ceiling

本檔是**研究與裁決**，不是執行結果；裁決的效力來自 owner 在本回合的前授權（「用戶授權你必須直接執行
FAR 提出的最佳工程裁決+執行方案」）。**任何實作是否成立，一律由檢測清單重導的結果決定，且對外驗收
仍為 `NOT_PERFORMED`。** 本檔不宣告任何項已完成。
