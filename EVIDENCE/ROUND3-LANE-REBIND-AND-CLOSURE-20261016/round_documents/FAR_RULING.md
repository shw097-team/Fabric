# FAR 研究報告與最佳工程裁決 — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

Round `ROUND3-LANE-REBIND-AND-CLOSURE-20261016`（session `20261016_104922_d455e7`，第三回合）。
格式沿用 `var/FAR-REMEDIATION-AND-CLOSURE-20261016/FAR_RULING.md`。
研究對象：① 新 owner 模型令的三車道重綁 ② 前回合 15 項殘留＋F-IND-2/F-IND-3 的重新判定
③ 候選未落地項目／SKILLS ④ REPO 的 MERGE／分支清理／發布 ⑤ 本 session 結案移交。

## 一、研究問題

新令把三車道改為 PLAN=`opencode-go/glm-5.3-flash`、EXECUTE=`opencode-go/deepseek-v4.1-flash`、
VERIFY=`opencode-go/deepseek-v4.1-flash`。它不是單純的模型替換：**它使唯一被要求互斥的那一對
（maker EXECUTE / checker VERIFY，`distinct_required: true`）變成同模型**，而原本載有 owner 令碰撞的
`{PLAN, VERIFY}`（`SOD006-C2`）不再碰撞。所以一個問題同時決定全部處置：**哪些項要工程（do）、哪些要一個
決策（decide）、哪些應被重新分類（drop）**，準則固定為低阻力、高可行、高工程必要性、不過度工程化、
對齊本 session 目標（三車道模型選擇可用且可靠地符合 owner 令）。

## 二、事實（全部來自本回合實地量測，非推論）

**2.1 兩個受令模型可服務**：relay `127.0.0.1:10101/v1/chat/completions` 對 `glm-5.3-flash` 與
`deepseek-v4.1-flash` 皆回 **http 200 ＋ `PROBE_OK`**；exec frontdoor `10100/healthz` = 200。
Hermes 根綁定已是 `model.default=glm-5.3-flash`／`delegation.model=glm-5.3-flash`（= 新令的 PLAN 模型）；
本回合四個研究子代理**實測由 `glm-5.3-flash` 服務**。

**2.2 受令車道目前只在 pool 的中段，不是預設**：PLAN 的 GLM 是 `rotation_alternate`／
`automatic_selection: false`（pool rank 2）；VERIFY 的 DeepSeek 是 arm C／fallback2（pool rank 3），
`selected_arm: A`／`selected_arm_identity: gpt-6.1-sol`。**不重綁，令就沒有生效**。

**2.3 選型權威有兩處，且必須同批改**：registry `routes[]` 與 `config/lane-route-slots.candidate.json`
的 slots pool。只改其一＝兩個權威互相矛盾（正是 F-IND-2 缺陷類）。

**2.4 guard 已對新令 fail-closed（實測）**：`hgk-lane-guard.py --lane VERIFY_SECURITY
--maker-model opencode-go/deepseek-v4.1-flash --target-model opencode-go/deepseek-v4.1-flash`
→ `REFUSE`／`ERR_LANE_SOD_VIOLATION`／exit 2。故 **SoD 重宣告必須與 registry 編輯落在同一批**，否則
該車道根本無法派工。

**2.5 宣告面比 registry 更寬**：`config/model-lane-assignment.json` 有 **12 個 `sod` 散文欄位**，
其中至少 9 個的前提是「VERIFY default arm A = gpt-6.1-sol」（含
`verify_vs_execute_model_separation: PASS on BOTH arms`、`verify_vs_plan_model_separation: NONE`、
`maker_self_acceptance`、`provider_separation`…），且 `/sod/plan_lane` 的**整段文字被 registry
`projections[].bindings[]` 釘為 expected（registry:475）**。新令使這些散文**變成假的**，而
`check_drift` 讀不到（它只比對被釘的指標自身）。

**2.6 前回合 15 項殘留的重新判定（實測）**：2 項**被本令取代**（R-05 epoch-19 候選 config、
R-07 `SOD006-C2`）／1 項部分關閉（R-14 校準）／1 項不可驗（R-09 量測注意事項）／**11 項 OPEN**；
本令使 R-08 **更糟**（governed profile 仍綁 gpt-6.1-sol），並新增 2 條 fail-closed 軸
（**NF-02** EXECUTE==VERIFY 同模型、**NF-03** `sod.plan_lane` 散文在第二軸上同樣為假）。

**2.7 更正我前回合已發布的一項描述**：所謂「757 個 access-denied 目錄」**實為長路徑
（`OSError WinError 3`）而非權限**——本回合重新走訪得 641,986 個檔案項、4,093 個不可列目錄、
59,434 個 stat 失敗，同一類。這是對已發布文字的實質更正，非新增缺陷。

**2.8 REPO 面（實測）**：`origin/main` = `b8ff810`；5 個 open PR（#4/#5/#6/#7/#8）皆
`mergeable: true`／`mergeable_state: clean`，head 皆非 main 的祖先（即尚未合併）；3 條分支
（`docs/skill-convergence-20261014`、`-followup`、`evidence/cnv-pipd-ls-sp-20261015-r6`）的 tip
**正是各自已合併 PR 的 head 且為 main 的祖先** → 合併後分支，可刪但屬 ref 變更。

**2.9 OpenSpec 的「未落地」是**慣例**而非缺陷**：`OPENSPEC/changes/` 有約 24 個 change，
`OPENSPEC/changes/archive/` 僅 1 個（2026-10-10），`OPENSPEC/specs/` 僅 2 個。
即本 repo 的慣例是**不套用/不歸檔**；把它報成本回合漏做會是假發現。

## 三、最佳工程裁決

準則：**低阻力、高可行、高工程必要性、不過度工程化、對齊本 session 目標。** 每項先列裁決，再列被否決
的選項與否決理由——被否決的選項必須留下，否則無法區分「想過」與「沒想到」。

### R1 — 三車道重綁至新令 → **REBIND（do，最高必要性，單批完成）**

**裁決**：PLAN 與 VERIFY 的**預設**改為令指定臂（EXECUTE 已是令指定臂，**不動**），且**同一批**改完
所有耦合面：

| 面 | 檔案／欄位 |
|---|---|
| 路由列 | `config/lane-routing-registry.yaml` `routes[].PLAN`（provider/model/canonical_identity/auth/oauth/selection_authority）、`routes[].VERIFY_SECURITY`（同上 ＋ `selected_arm`/`selected_arm_identity`）、兩者的 `arms[]` 預設旗標與 `fallbacks[]` 順序 |
| 選型權威 | `config/lane-route-slots.candidate.json` 的 slots pool rank（PLAN GLM 提升至 rank 1；VERIFY DeepSeek 提升至 rank 1） |
| 指派面 | `config/model-lane-assignment.json`：`lane_chains.PLAN[0]`、`lane_chains.VERIFY_SECURITY[0]`、`registry_epoch` |
| 版本耦合 | registry `epoch` 21→22；`source_of_routes.{revision,sha256}` 以**改後**網站摘要重釘（否則 `ERR_LANE_SOURCE_STALE`） |
| 投影 | 每一條受影響的 `projections[].bindings[]`（指標 ＋ expected 字串），含 registry:475 的 `/sod/plan_lane` 與 registry:474 的 `/lane_chains/VERIFY_SECURITY/1/automatic_selection` |
| 入口狀態 | 兩臂 `admission_status` **維持 UNPROVEN** 直到有實測 dispatch 回執（不得先寫 ADMITTED） |

**為何是最高必要性**：owner 指定誰服務哪一車道；不重綁，令就沒生效，且下一回合仍會依舊預設選型。

**被否決的選項**

| 選項 | 否決理由 |
|---|---|
| 只改 slots pool | registry 仍宣告舊預設 → 兩個權威矛盾（F-IND-2 缺陷類） |
| 只改路由列、不改 arms 旗標 | arms 內 `default: true` 仍指舊臂 → 宣告自相矛盾而 `check_drift` 為 0 |
| 只重綁 PLAN，VERIFY 留待下回合 | 直接漏做令的第三車道 |
| 連 EXECUTE 一起「重綁」 | 空操作；只增加風險與 diff，無對應收益 |
| 先把 `admission_status` 寫成 ADMITTED | 無實測回執即宣告＝本 session 明確禁止的自我宣稱 |

### R2 — SoD 重宣告（do，**與 R1 同批**，由 guard 實測強制）

**裁決**：`sod_invariants.pairs[]` 兩對**旗標互換**：
`{PLAN, VERIFY}` → `distinct_required: true`（兩者現已不同模型）；
`{EXECUTE, VERIFY}` → `distinct_required: false` **並新增** `declared_conflicts[]` 條目
（新 id、axis `canonical_identity`、`status: OWNER_ORDERED_IN_FORCE`、`ruled_by` 指向本令），其文字必須
**明寫殘留**：maker 與 checker **刻意同模型**，仍保留的是流程／車道／證據路徑分離與「驗收官不評自家產物」。
`SOD006-C2` 改為 `SUPERSEDED` 並註明由本令取代——**取代而非刪除**。

**為何不是別的**：guard 已實測對同模型對 fail-closed（2.4），故不重宣告則 VERIFY 車道無法派工；而
`distinct_required: true` 與「已宣告接受碰撞」同時存在即自我矛盾。

**被否決的選項**

| 選項 | 否決理由 |
|---|---|
| 只加 declared_conflicts、不動 pairs | guard 立即拒絕派工（已實測） |
| 保留 EXECUTE/VERIFY `distinct_required: true` | 要求互斥卻又宣告接受碰撞＝自我矛盾 |
| 把 checker 換成第三個模型以恢復獨立性 | 直接違反本令，owner 已明選 DeepSeek |
| 沿用 `SOD006-C2` 的 id | 破壞歷史可追溯性；id 不可重用，舊條目以 SUPERSEDED 表達 |

### R3 — 散文 vs 旗標（F-IND-2 ＋ NF-03）→ **PROSE REPAIR（do，併入 R1/R2 同一批）＋偵測器軸 DEFER**

**裁決**：以**結構化旗標為權威**，在同一批編輯內把 9 個 `sod` 散文欄位改寫為**改後的實際階層**；
把「偵測器新增 automatic_selection 軸」列為**下一回合的具價 WorkOrder**（需 RED-first 測試）。

**為何**：散文在同一批內修復**零邊際成本**，而它現在**同時**與結構化鏈及 owner 令矛盾（雙重為假）；
偵測器擴軸是獨立工程，塞進本回合即為過度工程化。

**被否決的選項**：只改散文不改旗標（矛盾照舊）／只改旗標不改散文（registry:475 的 expected 立即 drift）
／本回合就擴偵測器（無測試即無 RED，違反本 session 的 TDD 紀律）。

### R4 — governed profile 重綁 ＋ PLAN 平面服務證明（do）

**裁決**：`profiles/hgk-governed/config.yaml` 由 `gpt-6.1-sol` 改綁 `glm-5.3-flash` ＋ `opencode-go`，
以 `HERMES_HOME=<profile>` 跑一次 `PROBE_OK` one-shot，並**以該 profile 自己的 `state.db::sessions` 列**
作為服務證據。**同時揭露**：本互動 session 自身由 `deepseek-v4.1-flash` 服務（observed≠bound），
不得當成 PLAN 平面證據。

**被否決的選項**：只改根預設（已正確，但 profile 是 PLAN 平面的宣告綁定，留舊＝重造宣告 vs 服務落差）／
把互動 session 當證明（正是本 workstream 存在的目的要消除的那種替代）。

### R5 — 殘留分流（do／decide／defer，逐項）

| 項 | 分流 | 理由 |
|---|---|---|
| **R-03** 兩處未捕捉 metadata `OSError`（`scripts/hgk-lane-dispatch.py:864-866`、`:1134-1136`） | **DO（本回合 EXECUTE 車道）** | 邊界明確、seam 已知、真產品缺陷；且正好以令指定的 writer 臂落地，使 EXECUTE 的 `admission_status` 由 UNPROVEN 轉為有實測回執 |
| **NF-01** 列舉障礙更正 | **DO** | 更正已發布描述（長路徑，非權限）；零工程 |
| **R-15** 判決不一致 | **DO（本回合 VERIFY 車道）** | 以**新 checker 臂**重跑 C1–C7；同意則關閉、同項反向分歧則強化、新項分歧則擴大——不得軟性「關閉」 |
| **R-05** epoch-19 候選 config 是否可刪 | **DECIDE（owner）** | 屬刪除授權，非工程 |
| **R-06** 348 個 canonical-only 檔 | **DECIDE（owner）** | 保留不需決策，刪除才需要 |
| **R-13** R2 事前 admission 缺漏 | **DECIDE（owner）** | 事前 admission **不可回溯補做**；只能由 owner 裁定為有界接受的偏離 |
| **R-01** `--turn-shape` | **DEFER ＋ 分解** | 前回合兩次嘗試皆未落地；再跑同一形狀＝設計訊號被忽略。改為交付 seam 規格（錨點／hunk／測試名）給後續回合 |
| **R-02** R7 規則進產品 | **DEFER ＋ 定價** | 需 WorkOrder ＋ RED-first 測試；本回合以 R3 的散文修復先除矛盾 |
| **R-04** 全樹列舉不可證明 | **DEFER ＋ 定價** | 需長路徑感知列舉器，或把宣稱縮到 200 檔覆蓋層 |
| **R-09 / R-10 / R-11 / R-14** | **CARRY** | 無可關閉物：量測注意事項、自我演化僅為提案集、外部審查尚未發生（本回合的發布即是邀請）、校準說明 |

### R6 — REPO 的 MERGE／分支清理／發布 → **PUBLISH-READINESS（do）＋ MERGE/CLEANUP 交還 OWNER（decide）**

**裁決**：**不合併任何 PR**（5 個 open PR 機制上皆 clean，但合併＝接受/推廣，屬 owner）；**不刪任何分支**
（3 條已合併分支的 tip 可經 merge commit 永遠取得，安全論證成立，但「安全」不等於「有權」）。
代理可做的低阻力動作：發布 **merge-readiness 包**（逐 PR 的 head/base/ancestor/clean/changed-files）
＋ 本回合自己的證據分支與 PR，並把**一行指令**的合併與清理處方交給 owner。

**被否決的選項**：合併 #8（自我推廣）／刪 3 條已合併分支（非本回合任何宣稱所需）／force-push 或 rebase
任何分支（本 session 恆禁）。

### R7 — 候選落地（do／decide／defer）

**裁決**：本回合建立並 `--strict` 驗證**自己的** OpenSpec change；舊 change 未套用至 `OPENSPEC/specs`
一事，依 2.9 判定為**本 repo 慣例**，記為 convention note 而**不列為那些回合的缺陷**；子代理關於
`skills/hgk-r8-eia-closure` 的條目**無法在磁碟上定位** → 標記 **UNVERIFIED 且不據以行動**。
本回合學到的教訓回寫技能庫；第三方驗證仍為缺（沿用 R-10）。

### R8 — 結案／移交／發布（do）

逐項檢測清單、殘留表、凍結主體、閘門報告、發布回執、含「下一回合前 N 個動作」的移交 checkpoint、
以及自我演化註記；發布到 `pub/round3-lane-rebind-and-closure-20261016` ＋ PR（**never force-push、never merge**）。

### R9 — 自研究／自學習／自迭代／自進化（do）

本回合**實測學到**的教訓回寫技能（兩權威重綁、guard 對令指定對 fail-closed、長路徑列舉、
`HERMES_HOME` 原生路徑、回執被覆寫類），並以 `SELF_EVOLUTION.md` 明列「改了什麼、什麼仍未驗證」。

## 四、執行方案

| 步 | 動作 | WorkOrder | 回滾 |
|---|---|---|---|
| E1 | typed admission（Requirement／TaskSpec／WorkOrder） | `WO-R3-ADMISSION` | 刪本回合 admission |
| E2 | R1＋R2＋R3 單批 registry／site／pool 重綁（逐檔 `.bak` ＋前後 sha256） | `WO-R3-R1R2R3` | 逐檔自 `.bak` 還原 |
| E3 | 自我檢查：`check_drift` 0、conformance test、**guard 對新配對必須 ALLOW**、`check_sod` 兩對 | — | — |
| E4 | R4 governed profile 重綁 ＋ `PROBE_OK` one-shot ＋ profile state.db 列 | `WO-R3-R4` | 還原 profile config `.bak` |
| E5 | **EXECUTE 車道**（令指定臂）落地 R-03 兩處修補（edit-only） | `WO-R3-R03` | `git checkout` 該檔 |
| E6 | **VERIFY 車道**（令指定檢查臂）獨立複核本回合主體（含 R-15 的 C1–C7 重導） | — | — |
| E7 | 發布前閘門 ＋ 封包 ＋ 遠端回讀 | — | 分支可棄 |
| E8 | 結案、移交、發布、自演化 | — | — |

## 五、claim ceiling

本檔是**研究與裁決**，不是執行結果；裁決效力來自 owner 在本回合的前授權（「用戶授權你必須直接執行
FAR 提出的最佳工程裁決+執行方案」）。**任何實作是否成立，一律由檢測清單重導的結果決定**；
套用裁決不等於接受裁決；合併仍屬 owner；對外驗收仍為 `NOT_PERFORMED`。本檔不宣告任何項已完成。
