# FAR-LANE-VERSION-MIX-20261021 — 最終報告

受測主體：`C:\Projects\Agent_Workspace\HG-KSEOS` @ HEAD `903e47c`｜量測日 2026-10-21（local, UTC+8）｜回合 `FAR-LANE-VERSION-MIX-20261021`｜WorkOrder `WO-FAR-LANE-MIX-001`（writer=codex，REQ FROZEN v1）

**一句話結論**：lane 模型版本混雜是結構性問題——八個 surface 各自宣告 lane 模型且至少四組互相牴觸、四個 routing 檔全部沒有 commit lineage、toolchain 三個版本中有一個 pin 指向不存在的檔案；owner 要求的 mandated scheme（PLAN `gpt-6.1-sol` / EXECUTE `deepseek-v4.1-flash` / VERIFY `gpt-6.1-sol`）只在**明確 pin** 的情況下成立，並不是現行預設。

**本回合未實施任何修復。** 這是量測與診斷回合，權限為 READ-ONLY 加限定證據寫入（`var/FAR-LANE-VERSION-MIX-20261021/`）；下文所有 P0–P4 都是待授權的方案，不是已執行的工作。

---

## 1. 執行摘要

- 五個以上 surface 各自宣告 lane 模型，實測收斂出 4 組牴觸（C1–C4）；其中 C2（rank 與 role 標籤互斥）與 C4（同一份 `model-lane-assignment.json` 內同時宣告 gpt 已降級與 gpt 仍為現行 binding）是**單一檔案內部**的自相矛盾。
- `lane_policy.check_drift(registry=reg)` 今天**不是 clean**：恰好 2 筆 `severity: error`，`/codex_version` 期望 `0.162.0-alpha.17.2` 實得 `0.163.0-alpha.10.2`，`/codex_sha256` 期望 `e98c516f…b99e` 實得 `9ecb9df2…a46d`。
- toolchain 同時存在三個 Codex 版本——實際安裝 `0.163.0-alpha.10.2`、registry projection `0.162.0-alpha.17.2`、`<HERMES_HOME>/config.yaml` 的 `codex_bin` `codex-0.147.0-alpha.6.5`——而 `config/hermes-codex-lane.json::codex_executable` 指向的路徑**不存在**，信任該 pin 的 dispatch 會在呼叫任何模型之前 fail-closed（`ERR_LANE_TOOLCHAIN_BINARY_MISSING`）。
- 四個 routing 檔（registry、assignment、pool、lane binding）在 Git 中全部未追蹤：`git status --short` 皆為 `??`，`git log -- <file>` 各 **0 commits**；同期在同一批檔案上累積 8／13／8／6 份 `.bak`，至少 **6 個 rebind 世代 in 13 days**。
- `gpt-6.1-sol` 跨 session「時有時無」是入口與選擇方式的差異，不是單純供應問題：`--require-arm` 是**驗證器**、`--force-rank` 才是**選擇器**，unpinned dispatch 依 rank 前進因此拿到 PLAN 的 `glm-5.3-flash` 與 VERIFY 的 `deepseek-v4.1-flash`。
- mandated scheme 經 pin 實測可用：VERIFY 以 `used_rank=2` 服務 `openai-codex/gpt-6.1-sol`，`required_arm == served_arm`、nonce 與 usage receipt 皆到位（4.38 s）；EXECUTE 以 `used_rank=1` 服務 `opencode-go/deepseek-v4.1-flash`（3.23 s）。
- 治理債未清：spine workorders 為 CREATED 444 對 VERIFIED 112、RESULT_RECORDED 20、COMPLETED 11；requirements 為 CANDIDATE 496 對 ACCEPTED 2；`var/` 下 FAR/lane 相關回合目錄 **44** 個。
- 因此本報告能支持的最強主張只有一句：**用明確 pin 可以跑到 owner 要求的 lane／模型組合**；不能主張「預設值已修好」、「所有 session 都會如此」或「drift 已清零」。

---

## 2. 量測方法與受測主體

| 項目 | 值 |
|---|---|
| 受測主體 | `C:\Projects\Agent_Workspace\HG-KSEOS` |
| HEAD | `903e47c` |
| 量測時間 | 2026-10-21（local, UTC+8）；probe 的 `generated_utc` 落在 `2026-10-21T03:47Z`–`03:48Z` |
| 回合權限 | READ-ONLY ＋ 限定證據寫入 `var/FAR-LANE-VERSION-MIX-20261021/` |
| WorkOrder / REQ | `WO-FAR-LANE-MIX-001`（writer=codex）／REQ FROZEN v1 |
| 量測性質 | 每一列都是 LIVE readback，不是憑記憶的宣稱 |

探針清單（四支）：

1. **EXECUTE attempt1** — 未要求 nonce（brief 缺陷），`ok=false, code=ERR_NO_ARM_EMITTED_NONCE`。
2. **EXECUTE attempt2** — 要求 nonce，`ok=true`，`used_rank=1`。
3. **VERIFY_SECURITY pinned** — `--force-rank 2 --require-arm openai-codex/gpt-6.1-sol`，`ok=true`。
4. **PLAN in-Hermes plane** — 以 `-m gpt-6.1-sol --provider openai-codex` 的一次性（one-shot）呼叫；輸出 `PLAN_GPT_SOL_PROBE_OK`（exit 0）。

共同條件：pool 取自 `config/lane-route-slots.candidate.json`；transport 為 per-invocation `-c openai_base_url` 指向 relay `http://127.0.0.1:10101/v1`（不改 config）；`mode=forced_rank`；EXECUTE sandbox 為 `danger-full-access`、VERIFY 為 `read-only`。

靜態量測面：`config/lane-routing-registry.yaml`、`config/model-lane-assignment.json`、`config/lane-route-slots.candidate.json`、`config/hermes-codex-lane.json`、`AGENTS.md`、`profiles/hgk-governed/config.yaml`、`<HERMES_HOME>/config.yaml`、`tests/test_lane_policy.py`、`lane_policy.check_drift` / `check_sod`、`git status --short` / `git ls-files` / `git log`、`<HERMES_HOME>/state.db::sessions`、`var/shared-spine/hg-kseos.db`。

證據位置：`var/FAR-LANE-VERSION-MIX-20261021/EVIDENCE_DIGEST.md`（S1–S9）、`probes/`（raw receipts 與逐次 stdout／stderr）。

---

## 3. 結構診斷

**結論：這是結構性問題，不是單次升級遺漏。** 根因不是「版本太多」本身，而是多份可獨立變動的宣告、實際執行入口與治理紀錄，沒有被綁進同一條可驗證的權威鏈——任何一個表面被單獨重綁，其他表面都不會被強制跟上，於是每一次「修復」都能局部成功、整體繼續分裂。

根因機制（編號）：

1. **多重權威且語意不一致。** `config/lane-routing-registry.yaml`、`config/model-lane-assignment.json`、`config/lane-route-slots.candidate.json`、`AGENTS.md`、`profiles/hgk-governed/config.yaml` 與 `tests/test_lane_policy.py` 各自承載政策。PLAN 在這些表面分別指向 `glm-5.3-flash`、`gpt-6.1-sol`、`deepseek-v4.1-flash`；同一份 assignment 內同時存在「gpt 已於 2026-10-16 降級」與「gpt 仍是現行 binding」兩個宣告（C1、C4）。
2. **排序、role 標籤與 engine 分裂。** pool 把 rank-2 的 gpt 標成 `DEFAULT/首選`，rank-1 卻標 `FALLBACK1/備援1`（PLAN）與 `FALLBACK2/備援2`（VERIFY）（C2）；registry 給 VERIFY_SECURITY `engine: hermes`，而其他宣告與 dispatcher 的 `gate_scope` 都按 Codex CLI 處理（C3）。不同入口即使「各自遵照設定」，仍會得到不同結果。
3. **session plane 與 lane plane 被混用為證據。** session picker、profile default、lane dispatch、delegation 不是同一個 binding。某個聊天 session 用 gpt（sessions 表 127 筆），不能證明 PLAN／VERIFY lane 已按治理要求綁到 gpt；assignment 本身也把 per-session picker 與 `delegation.provider/model` 列為 `not_the_binding`。
4. **toolchain 沒有一致且可用的固定版本。** registry projection、lane config、`<HERMES_HOME>::model.codex_bin` 是三個不同版本，而 lane config 指定的 executable 已不存在。版本欄位正確不代表 executable 能啟動——`0.163.0-alpha.10.2` 寫在 lane config 裡，但同一份檔案的 `codex_executable` 是死路徑。
5. **drift gate 只覆蓋部分一致性。** `check_drift` 已有 2 筆 error；但它抓不到 assignment 內部矛盾、文件與 profile 分裂、rank/role 互斥與 engine 不符。`check_sod(PLAN, VERIFY_SECURITY)` 反而回報 `SOD_OK glm-5.3-flash != deepseek-v4.1-flash`，因為 registry 已被重綁離開 `AGENTS.md` 的宣告——SoD 通過的理由，正是治理文件被違反後的產物。
6. **變更與結案缺少可靠歷程。** 四個核心 routing 檔均未納 Git，多代 `.bak` 不能替代 commit lineage；大量停在 CREATED 的 WorkOrder 與 44 個 FAR/lane 回合目錄，顯示修復容易停在局部重綁，未完成跨面一致性與結果驗收。（狀態分布能證明紀錄閉環不足，不能單憑它斷言所有工作都未執行。）

---

## 4. 為何 `gpt-6.1-sol` 跨 session 時有時無

不是單一「模型供應不穩」，而是入口、選擇方式、設定世代與 upstream 條件共同造成。判讀時必須先把失敗分類成：**未選中 / 政策排除 / toolchain 阻擋 / epoch 或 cache 問題 / upstream 限流**，再談 availability。

| 可選中路徑（任一即可） | 不可選中路徑（任一即可） |
|---|---|
| 釘選 dispatch：`--force-rank 2 --require-arm openai-codex/gpt-6.1-sol`（pool rank 2 = gpt）。本回合 VERIFY receipt 已證明 `required_arm == served_arm`、`used_rank=2`。 | 未釘選 dispatch：dispatcher 沿 rank 前進，PLAN rank-1 `glm-5.3-flash`、VERIFY rank-1 `deepseek-v4.1-flash` 先被服務。`--require-arm` 只驗證，不選擇。 |
| In-Hermes PLAN plane 以 `HERMES_HOME=<profiles/hgk-governed>` 啟動，**且該 profile 當時持有 gpt binding**（2026-10-16 的實測狀態）。本回合以顯式 `-m gpt-6.1-sol --provider openai-codex` one-shot 在同一 profile 上成功（`PLAN_GPT_SOL_PROBE_OK`）；此結果**不覆蓋** profile 現行 bytes 為 deepseek 的事實。 | 以 registry 預設路徑 dispatch（`route_for_lane` top level）→ glm / deepseek，永遠不是 gpt。 |
| per-session picker 選 gpt-6.1-sol（sessions 表 127 筆）——這是 session-plane 事實，對 lane binding 不授權任何事。 | 後續 rebind 之後重新啟動 profile → `deepseek-v4.1-flash`（S1e），而宣告檔仍宣稱 gpt（S1f）；歷史設定文字不會覆寫現行 bytes。 |
| GPT 配額可用期間（owner note 2026-10-20；relay ledger 近 3 日有 393 筆 `gpt-6.1-sol` 呼叫）。 | 回合級排除：`round_model_exclusions`（`HGK-ROUND-MODEL-EXCLUSION-1`，2026-10-12 回合）以 `ERR_MODEL_FAMILY_EXCLUDED_ROUND` 對 `gpt-*` 恢復 fail-closed。 |
| — | 過期 toolchain pin：`ERR_LANE_TOOLCHAIN_BINARY_MISSING`，在**任何模型被呼叫之前**就失敗，表象看起來像「模型不可用」。 |
| — | pool epoch 依賴：同一 lane 在某一 registry epoch 拒絕的 arm，在下一個 epoch 可以服務；沒有 cache invalidation 讓舊判定失效。 |
| — | 服務商 429：`fallback_providers` 接手，served model 可能在 session 中途改變（2026-10-21 10:26→11:20 有 `deepseek-v4.1-flash → mimo-v2.6-pro` 的 fallback 紀錄，`session_model_usage` 同時留下兩個模型而 `model_config` 仍寫 deepseek）。 |

---

## 5. 版本混雜現況

### 5.1 各 surface 分歧表

| # | Surface | PLAN | EXECUTE | VERIFY_SECURITY | engine |
|---|---|---|---|---|---|
| S1a | `config/lane-routing-registry.yaml` `routes[]`（epoch **22**） | **glm-5.3-flash** / opencode-go, medium | deepseek-v4.1-flash / opencode-go | **deepseek-v4.1-flash** / opencode-go, medium | PLAN=hermes, EXECUTE=codex-cli, **VERIFY=hermes** |
| S1b | `config/model-lane-assignment.json` `lane_chains` | rank1 glm-5.3-flash；gpt-6.1-sol = `fallback1_operator_selectable`（註記「Rank-1 default of epochs 19-21」） | rank1 deepseek-v4.1-flash | rank1 deepseek-v4.1-flash；gpt-6.1-sol = operator-selectable alternate | — |
| S1c | `config/lane-route-slots.candidate.json` `ordered_pool` | rank1 glm（role **FALLBACK1/備援1**）／rank2 gpt-6.1-sol（**DEFAULT/首選**, medium, openai_oauth）／rank3 deepseek（FALLBACK2）／rank4 mimo（OPTIONAL）／rank5-6 nvidia | rank1 deepseek（DEFAULT）／rank2 gpt-6-luna／rank3 nvidia deepseek | rank1 deepseek（**FALLBACK2**）／rank2 gpt-6.1-sol（**DEFAULT/首選**）／rank3 glm（FALLBACK1）／rank4 nvidia deepseek | — |
| S1d | `AGENTS.md` L53–55（治理文件） | default **openai-codex/gpt-6.1-sol**（medium, OAuth）→ glm → deepseek | default deepseek-v4.1-flash → gpt-6-luna → nvidia | default **gpt-6.1-sol**（medium）→ glm → deepseek | 「Hermes-internal」vs「Codex CLI」 |
| S1e | `profiles/hgk-governed/config.yaml`（`_plane` 鍵自稱 PLAN plane） | **model.default = deepseek-v4.1-flash / provider opencode-go** | — | — | hermes |
| S1f | `config/model-lane-assignment.json::in_hermes_plan_orchestrator_plane.binding_surface` | 要求同一 profile 檔應為 `model.default=gpt-6.1-sol`、`provider=openai-codex`，引用 2026-10-16 probe（`PLAN_LANE_PROBE_OK`，state.db 列為 gpt-6.1-sol） | — | — | — |
| S1g | `tests/test_lane_policy.py` L100–113（conformance gate） | 斷言 rank-1 = `("opencode-go","glm-5.3-flash")` | deepseek rank-1 | 斷言 rank-1 = `("opencode-go","deepseek-v4.1-flash")`（註解「same model as the EXECUTE writer BY OWNER ORDER」） | — |
| S1h | `<HERMES_HOME>/config.yaml`（session 預設 plane） | `model.default=deepseek-v4.1-flash`, `provider=opencode-go` | — | — | hermes |

### 5.2 牴觸集（實測，非推論）

| 代號 | 內容 | 涉及 surface |
|---|---|---|
| C1 | registry／assignment／test 把 PLAN rank-1 放在 **glm-5.3-flash**；`AGENTS.md` 與 binding_surface 把 PLAN plane 放在 **gpt-6.1-sol**；live profile bytes 卻是 **deepseek-v4.1-flash** | S1a, S1b, S1g vs S1d, S1f vs S1e |
| C2 | rank-2 標 `DEFAULT/首選`，rank-1 卻標 `FALLBACK1`（PLAN）與 `FALLBACK2`（VERIFY）——同一檔案內 rank 與 role 互斥 | S1c |
| C3 | registry 給 VERIFY_SECURITY `engine: hermes`；`AGENTS.md`、pool 與 dispatcher `gate_scope`（`--lane VERIFY_SECURITY`）按 Codex CLI 處理 | S1a vs S1c, S1d |
| C4 | 同一份 assignment 的 `prior_revision_note` 記錄 gpt 曾是 epochs 19–21 的 rank-1 default 並於 2026-10-16 被降級，`binding_surface` 卻仍宣告 gpt 為現行；`check_drift` 對此**不報任何事** | S1b 內部 |

### 5.3 toolchain 三版本（其中一個 pin 已死）

| 來源 | 宣告值 | 實測 |
|---|---|---|
| `config/hermes-codex-lane.json::codex_executable` | `…/OpenAI/Codex/bin/**e78bad9887fa50cf**/codex.exe` | **路徑不存在**（`ls` 驗證） |
| `config/hermes-codex-lane.json::codex_version` | `0.163.0-alpha.10.2`，sha `9ecb9df2…` | 與實際安裝同版，但同檔的 executable 路徑是死的 |
| `<HERMES_HOME>/config.yaml::model.codex_bin` | `…/HG-KSEOS/runtime/**codex-0.147.0-alpha.6.5**/codex.exe` | 存在（Aug 7 build）——第三個、較舊的 pin |
| 實際安裝 | `…/OpenAI/Codex/bin/**896a0166b774037a**/codex.exe` | `codex-cli 0.163.0-alpha.10.2` |
| registry projection | `0.162.0-alpha.17.2` ／ `e98c516f…` | 與實際不符 → `check_drift` 2 筆 error |

### 5.4 版控狀態與 `.bak` 世代

- `git status --short`：`?? config/lane-routing-registry.yaml`、`?? config/model-lane-assignment.json`、`?? config/lane-route-slots.candidate.json`、`?? config/hermes-codex-lane.json`。
- `git ls-files config/` 只有 `config/hermes.json`、`config/project.json`；`git log -- <routing file>` 對四個檔各為 **0 commits**。
- `.gitignore` 另忽略 `var/` 與 `var/shared-spine/*.db`，因此 spine DB 與每一個證據根目錄也都沒有 commit lineage。
- `.bak` 普查：`lane-routing-registry.yaml` 8 份、`model-lane-assignment.json` **13** 份、`hermes-codex-lane.json` 8 份、`lane-route-slots.candidate.json` 6 份（四檔合計 35 份，本報告僅就上述列舉加總）。
- 最新三份都掛 `…-round3-lane-rebind-20261016`；其餘跨 `chainrebind-20261015`、`far-remediation-20261016`、`lane-reliability-20261016`、`planrebind-20261015`、`pre-rebind-20261013`、`pre-rebind-20261012`、`final-route-20261008` → 同一批檔案上至少 **6 個 rebind 世代 in 13 days**。

### 5.5 session plane 的模型分佈（僅作對照，不是 lane binding 證據）

`<HERMES_HOME>/state.db::sessions` 全量模型計數：`deepseek-v4.1-flash` 203、`gpt-6.1-sol` 127、`glm-5.3-flash` 84、`mimo-v2.6-pro` 18。近期順序顯示聊天 plane 在 deepseek / gpt / glm / mimo 之間跨日翻轉；2026-10-21 10:26→11:20（local）出現 `Rate-limit backoff level 0` 之後的 `Fallback activated: deepseek-v4.1-flash → mimo-v2.6-pro (opencode-go)`。`session_model_usage` 在同一 session 內記錄兩個模型，而 `model_config` 仍寫 deepseek——即 **served model 在 session 中途改變**。

`<HERMES_HOME>/config.yaml::fallback_providers` 的 HEAD 原為 `opencode-go/mimo-v2.6-pro`，今天 2026-10-21 由 owner 指示換成 `opencode-go/glm-5.3-flash`（receipt：`var/config-change-mimo2glm-20261021/RECEIPT.md`）。

### 5.6 治理債數字

| 表 | 狀態分佈 |
|---|---|
| workorders | CREATED **444**、VERIFIED 112、RESULT_RECORDED 20、COMPLETED 11、ADMITTED 2、FAILED 1、ROLLED_BACK 1、COMPLETED_WITH_BINDING_DEFECT 1 |
| requirements | CANDIDATE **496**、FROZEN 413、ACCEPTED 2、ADMITTED 1、OPEN 2 |

`var/` 下符合 FAR/lane 主題的回合目錄 **44** 個，包含 `far-lane-health-repair-20261011`、`FAR-LANE-REPAIR-20261014`、`FAR-LANE-REUSE-RCA-20261015`、`FAR-LANE-ENFORCEMENT-RCA-20261015`、`FAR-LANE-ROUTE-REBIND-20261015`、`far-lane-sod-003/004/005`、`FAR-REMEDIATION-AND-CLOSURE-20261016`、`far-018`、`far-019`。

### 5.7 跨來源不一致（照實並列，不選邊）

1. **epoch 編號**：`AGENTS.md` 標題寫「current, epoch 18」、source pin 為 revision 18；而本回合實測的 `config/lane-routing-registry.yaml` 為 epoch **22**，assignment 又記載 gpt 是 epochs **19–21** 的 rank-1 default。三者對「現在是哪個 epoch」的敘述不一致，本報告不判定何者為準。
2. **SoD 紀錄 vs 實測**：`AGENTS.md` L57 記載 SOD006-C2（PLAN 與 VERIFY 共用同一個默認 arm）為 `OPEN_OWNER_ORDERED`；但實測 registry（epoch 22）中 PLAN 是 `glm-5.3-flash`、VERIFY 是 `deepseek-v4.1-flash`，`check_sod` 回 `SOD_OK`。也就是說，被記錄為「仍然存在」的模型同質碰撞，在現行 registry 上已被重綁消除；而 owner 要求的方案會讓它重新出現。兩者並列，不自行裁決。

---

## 6. 修復方案（P0–P4，依優先順序）

以下每一項都需先取得具明確 write-set、writer、驗收與 rollback 條件的 remediation WorkOrder；現有 `WO-FAR-LANE-MIX-001` 的 READ-ONLY 授權**不因本報告完成而擴大**。

### P0 — 先定政策與授權，停止再一次局部重綁

- **檔案**：`AGENTS.md`、`config/model-lane-assignment.json`、`config/lane-routing-registry.yaml`。
- **動作**：明定目標為 PLAN=`gpt-6.1-sol`／OAuth／Hermes、EXECUTE=`deepseek-v4.1-flash`／Codex CLI、VERIFY_SECURITY=`gpt-6.1-sol`／Codex CLI；同時核定 fallback、required-arm 模式與 `round_model_exclusions` 的適用範圍。不得為了恢復 gpt 而直接繞過既有 exclusion。
- **治理步驟**：由 owner 重新確認目標與 SoD 例外（PLAN 與 VERIFY 共用模型屬 `OPEN_OWNER_ORDERED` 類決策），依既有流程修訂並重新 FROZEN REQ，再據以開立 remediation WorkOrder；若現行規則不允許擴充本回合，另立實施回合。
- **驗收條件**：三個檔對三條 lane 的 default／fallback／engine 敘述完全一致，且與 owner 核定的 REQ 逐字對得上；SoD 例外有具名紀錄而非隱含通過。
- **風險**：再一次只有部分表面被改，其餘表面（profile、pool、test）落後，等於新增第 5 個「權威」；以及以「恢復 gpt 可用」為名繞過 `round_model_exclusions`，把政策排除誤判為供應故障。

### P1 — 先修 toolchain，排除「模型根本沒被呼叫」

- **檔案**：`config/hermes-codex-lane.json`、`config/lane-routing-registry.yaml` 的 projection、經確認作用中的 `<HERMES_HOME>/config.yaml`。
- **動作**：以實際存在、通過 `--version` 且完成完整 SHA-256 驗證的 binary，統一 executable／version／hash 三欄；縮寫 hash 不足以作為寫入值。清理舊 `codex_bin` 的有效引用；若不同 plane 確有不同版本需求，必須明文列為受控例外。
- **治理步驟**：核准 toolchain 變更與 rollback；先確認受影響 `HERMES_HOME` 的所有權，不跨 profile 修改；變更後重跑 preflight 與 `check_drift`。
- **驗收條件**：已知 2 筆 `DRIFT_VALUE`（`/codex_version`、`/codex_sha256`）歸零，且 pin 的 executable 在磁碟上存在並可執行；之後才進行模型 probes（順序不可顛倒，否則 probe 失敗無法歸因）。
- **風險**：把 pin 改成「某台機器現在剛好有的路徑」而沒有納入可重現的版本宣告；或同時改動多個 plane 的 `codex_bin`，讓原本分離的 plane 互相污染。

### P2 — 建立單一權威與單向產生的 projections

- **檔案**：`config/lane-routing-registry.yaml`、`config/model-lane-assignment.json`、`config/lane-route-slots.candidate.json`、`profiles/hgk-governed/config.yaml`、`AGENTS.md`。
- **動作**：以 registry 承載核准後的 lane policy，其餘 routing 表面改為可檢查或可產生的 projections；明定 profile 是 runtime binding 而非另一份政策。對齊 rank、`DEFAULT/FALLBACK` role、provider、engine、effort 與 `in_hermes_plan_orchestrator_plane.binding_surface`；把 epochs 19–21 與舊 probe 移入歷史語意，不再冒充 current binding；明定 candidate 檔是否可被 runtime 消費，禁止候選與生效設定混用。
- **治理步驟**：核准權威來源與新 epoch，把跨檔更新視為**同一個變更集**（single change set）送審。
- **驗收條件**：全部 projections 在同一 epoch 下一致才可驗收；不接受「逐檔成功」即結案；rank 順序與 role 標籤在每個 lane 內互不矛盾；engine 欄位與 dispatcher 實際使用的 engine 相同。
- **風險**：把 registry 升格為權威但没有淘汰舊宣告，造成兩套並存的「權威」；以及用 epoch 遞增掩蓋內容未對齊（epoch 換了、bytes 沒對齊）。

### P3 — 讓 dispatch 與 gates 驗證實際執行語意

- **檔案**：`scripts/hgk-lane-dispatch.py`、`tests/test_lane_policy.py`、`lane_policy.check_drift` / `check_sod` 的實作檔案（實際路徑須先定位，不臆造檔名）。
- **動作**：把 selection 與 assertion 清楚分離——過渡期保留顯式 `--force-rank` 與 `--require-arm`，長期改用穩定的 arm selector，避免 gpt 因 rank 變動而被選錯；對要求固定 arm 的呼叫 fail-closed，不得靜默 fallback 後仍宣稱符合要求；pool verdict 綁 epoch／內容版本並驗證 invalidation；擴充 gates 覆蓋內部宣告一致性、rank/role、engine、profile binding、binary 存在與 hash，以及真實 SoD 關係。
- **治理步驟**：以核准 REQ 作為測試 oracle，另做 code review；更新舊 rank-1 測試時，必須是「因政策變更而更新 oracle」，不是改 assertion 讓新設定過關。
- **驗收條件**：測試涵蓋 pinned／unpinned、錯 arm、排除、缺 binary、舊 epoch、429、nonce 缺失等成功與失敗路徑，且每個 fail-closed 路徑都有具名錯誤碼與非零 exit。
- **風險**：只改 assertion 使新設定通過，形成 false-green；以及把「pool 在某 epoch 拒絕過某 arm」的舊判定當成現況（缺 invalidation）。

### P4 — 補齊版本管理、fresh-session 驗證與結案鏈

- **檔案與紀錄**：把四個未追蹤 config 檔納入 Git；檢視 `.gitignore` 的 evidence 保存政策；依既有介面更新 `var/shared-spine/hg-kseos.db` 的治理紀錄（不直接改 DB 偽造狀態）。
- **動作**：提交前檢查 secrets；runtime DB 不必直接進 Git，但設定 commit、REQ／WO、epoch、receipt 必須可互相追溯；被忽略的 `var` 證據應有受控保存或索引與完整性校驗。從 fresh session 驗證 PLAN 的**預設** binding，再驗證 EXECUTE 與 VERIFY dispatch；另測 relaunch、fallback、epoch 更新與較長工作負載。
- **治理步驟**：先記錄結果與殘餘，再按既有狀態機完成 VERIFIED／COMPLETED 所需步驟；maker 不自判 verdict。
- **驗收條件**：四檔有 commit lineage 且能對回同一 epoch 與同一 REQ；fresh session 的 PLAN default 為 gpt-6.1-sol（而非靠 `-m` 覆寫）；既有 2 筆 drift error 維持為零；既有 CREATED 堆積有明確處置（結案或具名 deferral）。
- **風險**：把 secrets 一併 commit；以新增 repair WO 或短 probe 成功取代實際結案；以及把 `var` 證據「進 Git」誤做成把 runtime DB 一起提交。

---

## 7. 主張上限與殘餘

1. 本回合證據支持 mandated scheme「**經明確 pin 可使用**」，不支持「現行 defaults 已修好」或「所有 session 都會如此執行」。
2. PLAN one-shot 的 exit 0／成功字串，與 VERIFY 的 `required_arm`、`served_arm`、nonce、usage receipt 不是同等強度的證據；正式驗收須分別列出，不能混稱為同等 binding attestation。
3. probe 的 `used_seconds` 為 2.78 s（EXECUTE attempt1）、3.23 s（EXECUTE attempt2）、4.38 s（VERIFY）；digest 以「3–4 s」概括，本報告改以 receipt 實測值並列。無論取何值，都只證明短時 transport 與 arm binding，不證明長期穩定性、quota 容量、重啟後一致性或高負載可用性。
4. 目標方案讓 PLAN 與 VERIFY 使用同一個 `gpt-6.1-sol`，兩者的 **model-axis SoD 不存在**；maker（EXECUTE=`deepseek-v4.1-flash`）≠ checker（`gpt-6.1-sol`）的模型分離仍成立。程序分離不能包裝成模型獨立。
5. session 的 model 標籤是 Hermes 紀錄，不是獨立 provider attestation；`.bak` mtime 是檔案系統 metadata，不是作者或授權證據；歷史成功也不是當前設定的驗證。
6. 修復本地 routing 與 toolchain，仍不能保證 upstream quota、429 或服務容量；嚴格 required-arm 的代價可能是**更明確地拒絕服務**，而不是提高表面成功率。
7. 本報告的 claim ceiling：可依 digest 判定結構性根因、解釋間歇性來源、定義修復與驗收順序；**尚不能**宣稱 remediation 已獲授權、已實施、drift 已清零或治理已結案。`hgk_canonical_acceptance: NOT_PERFORMED`。
8. 附錄觀察（digest 未列，僅轉錄 receipt 原文，不改變任何 verdict）：VERIFY 的 stdout 在 turn 前出現 `Model metadata for gpt-6.1-sol not found. Defaulting to fallback metadata`。此訊息說明該 arm 是以 fallback metadata 服務，是否影響長期行為**本回合未量測**。

---

## 8. 附錄：本回合探針與 receipt 對照表

| 探針 | Receipt | ok | required_arm | served_arm | used_rank | nonce | usage_receipt_ok | 秒數 | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| EXECUTE attempt1（未要求 nonce） | `probes/probe_EXECUTE_attempt1_nononce.json` | **false**（`ERR_NO_ARM_EMITTED_NONCE`） | `opencode-go/deepseek-v4.1-flash`（`identity_gate.required_arm`） | 未綁定（top-level `used_rank: null`；`attempts[0].rank=1`） | null | **false** | true | 2.78 | 該 turn **確實完成**：`stdout_tail` 有 `EXECUTE_DS_LANE_PROBE_OK`，usage `status=200`、`provider=opencode-go`、`model=deepseek-v4.1-flash`。失敗成因是 brief 沒有要求 nonce，nonce gate 屬 transport attestation，不代表沒有工作發生。 |
| EXECUTE attempt2（要求 nonce） | `probes/probe_EXECUTE.json` | true | `opencode-go/deepseek-v4.1-flash` | `opencode-go/deepseek-v4.1-flash` | 1 | true | true | 3.23 | `mode=forced_rank`，`pool=config/lane-route-slots.candidate.json`；skip 紀錄：rank 3 `nvidia/deepseek-ai/deepseek-v4.1-flash`（`UNREACHABLE_MEASURED_20261011`）。 |
| VERIFY_SECURITY pinned gpt-6.1-sol | `probes/probe_VERIFY.json` | true | `openai-codex/gpt-6.1-sol` | `openai-codex/gpt-6.1-sol` | 2 | true | true | 4.38 | `reasoning_effort=medium`、sandbox `read-only`；usage `status=200`、`provider=openai-p6a1fe3`、`model=gpt-6.1-sol`；skip 紀錄：rank 4 `nvidia/deepseek-ai/deepseek-v4.1-flash`（同上）。 |
| PLAN in-Hermes plane gpt-6.1-sol medium | 無 JSON receipt（one-shot） | 以 stdout 判定 | 以 `-m gpt-6.1-sol --provider openai-codex` 指定 | stdout `PLAN_GPT_SOL_PROBE_OK`（exit 0） | n/a | n/a | 未產生 | 未量測 | 證據強度低於前兩者：沒有 `required_arm`／`served_arm`／nonce／usage receipt 的結構化綁定，不能與 Codex-CLI lane 的 receipt 混稱同等。 |

逐次 attempt 明細另存於 `probes/probe_EXECUTE.json.attempts.ndjson` 與 `probes/*.json.logs/`（每次 stdout／stderr 皆有 byte 長度與 SHA-256）。三次 Codex-CLI attempt 的 stderr 都出現同一筆 `426 Upgrade Required` websocket 連線訊息（`ws://127.0.0.1:10101/v1/responses`），其後由 HTTP 路徑完成；本回合僅記錄，不推論其影響。

EXECUTE 與 VERIFY 的 receipt 皆標明 claim ceiling：通過只證明「該 Codex-CLI lane 經 relay 服務了這一回合且有相符的 usage receipt」，**不是**對任何受測主體的 acceptance。
