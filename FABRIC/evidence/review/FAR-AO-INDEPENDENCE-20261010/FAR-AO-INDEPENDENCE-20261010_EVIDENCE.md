# FAR-AO-INDEPENDENCE-20261010 — 獨立 AO lane 與 required-arm / 非變異守衛

> Round: `FAR-AO-INDEPENDENCE-20261010`
> 日期: 2026-10-10（台北 UTC+8）
> Authority: owner 直接工作令 ＋ 該輪四項裁決（見 §5）
> Status: **ROUND CLOSED；本輪自身的 requirement 與 acceptance 已由獨立 checker lane 判 PASS 並經 typed API 落帳**
> Claim ceiling: **local verification ＋ owner-approved promotion ＋ process-only independence**（詳見 §6）

---

## 1. 本輪核心目標與結論

**Owner 原話**：「必須堅持無人窗口也要 `gpt-6.1-sol`，此為本輪任務的核心目標。」

**結論：已達成，且以真實回合實測（E12）。**

| 欄位 | 值 |
|---|---|
| dispatch exit / `ok` | `0` / `true` |
| `required_arm` → `served_arm` | `openai-codex/gpt-6.1-sol` → **`openai-codex/gpt-6.1-sol`** |
| `identity_gate` | `state=enforced`、`degraded=false`、rank 4 `requirement=relay_pool`、`ok=true` |
| attempt | rank 4、`exit 0`、**5.97s**、`nonce_present=true`（`item.completed/agent_message`） |
| 用量收據 | **`usage_status 200`**、`openai-p6a1fe3` / `gpt-6.1-sol` |
| 持久化 | `stdout_byte_exact=true`、590 bytes |
| 模型原文 | `OAUTH_ARM_SERVED_UNATTENDED` ⏎ `HGK_LANE_NONCE_OK` |

「無人窗口」的實質證明：lane home（`…\HG-KSEOS\codex-hermes`）**沒有 `auth.json`**（`Not logged in`），回合以 `--ask-for-approval never` 經 relay URL（`127.0.0.1:10101`）取得 arm；**沒有開啟任何互動視窗，也不需要**。

**Owner 更正（同日，已納入紀錄）**：`(ii)` 專用 relay-pool 帳號**撤銷為 NOT APPLICABLE**——owner 只有一個 ChatGPT 帳號，因此「第二個身分」在此環境**不存在可執行版本**；此非 blocked、非 deferred，而是目標本身不成立。詳見 §5.3。

---

## 2. 本輪改了什麼（canonical subject 綁定）

| 檔案 | sha256 | bytes |
|---|---|---|
| `scripts/hgk-lane-dispatch.py` | `5ee625a11fe5aa25e4c127a2fd606a0907004e2f1cd3f2e5c0c545aa864d6f14` | 42584 |
| `config/lane-route-slots.candidate.json` | `c6e6c21fdf7bc04f5d534be88909cab8a0fe6a00881cc41613b3276e91bec386` | 23651 |
| `tests/test_lane_dispatch_ao_guard.py` | `4d214dc5f0f911d400ba2f2ed296e644ac3a2a71f2fe93421b576cad1bf26d8f` | 24514 |
| `tests/fixtures/stub_lane_child.py`（新） | `8dc7e9d08235dc782d12220684434afcf8057f0468ed06b37f5d56e21d331493` | 2959 |
| `openspec/specs/ao-lane-independent-verify/spec.md` | `c211866296ca3b400c8444be5f014c965d5ef8ef10299dc573943197d81c8691` | 13250 |

變更要點（全部為 `CANDIDATE` 起點，經 owner 核准後 promotion）：

1. **Pre-spawn 身分／健康閘門（fail-closed）**：在 spawn 子行程**之前**驗證 OAuth arm 是否具備可 refresh 的憑證；**不健康即拒絕**（`ERR_RELAY_OAUTH_NEEDS_REAUTH`，exit 4），**不得靜默改跑別的 arm**。gate 不排除 OAuth arm，而是「**驗證後放行**」（owner 裁決）。
2. **`--require-arm` 語意＝該 arm 必須實際服務本回合**：檢查**移出** gate 分支之外，且以 **pre-gate 候選集**判定「是否在 pool 中」；若閘門放行但由別的 arm 服務 → **`ERR_REQUIRED_ARM_NOT_SERVED`（exit 3）**。
3. **非變異守衛（non-mutation guard）改為條件必備**：升權 lane 必須帶 `--guard-subject`；守衛根**無法解析時拒絕**（`ERR_GUARD_ROOT_MISSING`，0 attempts），並新增 `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`（禁止把 harness 自己的輸出目錄當受檢主體）。
4. **回合原始 bytes 持久化**：子行程 stdout/stderr 以 **bytes 捕獲並原樣落檔**（先前以 `text=True` 解碼會破壞位元組）；receipt 保留完整 stdout 而非僅尾端 400 字元，可獨立重算（E6c/E6d 已重算 MATCH_ALL）。
5. **確定性（無模型）負測接縫**：新增 `--codex-executable`，可把 checked child 換成 stub，讓守衛的作廢路徑能在**沒有模型**的情況下端到端驅動。
6. **pool 宣告帶入受評 arm**：`identity_requirement` 不再於 `main()` 被丟棄。
7. **OpenSpec**：新增 change 並 archive，delta 已套入 **main specs**（`+16 requirements`）。

---

## 3. 驗證證據（E1–E12，全部為真實執行）

### 3.1 角色／lane 實測

| 代號 | 內容 | 結果 |
|---|---|---|
| E1 | EXECUTE writer 回合 | `usage 200`（opencode-go）13.9s |
| E2 | VERIFY/SECURITY checker 回合 | `usage 200`（opencode-go）50.4s |
| E3 | AO checker 回合 | `usage 200`；verdict `ADVISORY_INCONCLUSIVE_FROM_RECORD` |
| E4 | checker 執行 `certutil` 獨立算檔 | sha256 `6794afc5…02bd8`，與 manifest 一致，11.5s |
| E6c / E6d | checker **自行重算**最終修訂的兩個 digest | `MATCH_ALL=True`、`mutated=false`、`stdout_byte_exact=true`（6389 bytes vs receipt 舊版尾端 400 chars） |
| E7 | 閘門 `enforced` 且 required arm 被服務 | `required_arm=openai-codex/gpt-6.1-sol`、`exit 0`、`usage 200` |
| E8 | relay home 不存在 → **fail-closed** | `exit 4`、`ERR_RELAY_OAUTH_NEEDS_REAUTH`、**未 spawn** |
| E9b | 釘 rank ＋ `--require-arm` | `required_arm == served_arm == openai-codex/gpt-6.1-sol`、8.73s |
| E10c | 只 `--require-arm` 不釘 rank | 閘門 4/4 放行但由 rank 1 服務 → **`exit 3` / `ERR_REQUIRED_ARM_NOT_SERVED`** |
| **E12** | **本輪核心目標：無人窗口 `gpt-6.1-sol`** | **通過**（見 §1） |
| A1–A4 | 專用帳號切換前量測（現已撤銷，見 §5.3） | `A1 FAIL`（同一帳號）、`A3 PASS`、`A4 PASS`（`exit 4` fail-closed）、`A2` 未跑 |

### 3.2 確定性負測矩陣（**無模型**，E11a–E11e，全數 PASS）

以 `--codex-executable tests/fixtures/stub_lane_child.py` 驅動；stub 同時提供**兩個受理條件**（`nonce` 於 `item.completed/agent_message` 內、以及**寫入 scratch 帳本**的匹配用量列），因此下列「作廢」案例是**本應通過**的回合被守衛作廢，而非回合本身失敗：

| 案例 | stub 行為 | 期望 | 實測 |
|---|---|---|---|
| E11a | 不動 | 控制組應成立 | `ok=true`、`mutated=false` |
| **E11b** | 改寫受檢檔 | 作廢 | **`exit 3` / `ERR_CHECKER_MUTATED_SUBJECT`**，而 `nonce=True`、用量列匹配 |
| **E11c** | 刪除受檢檔 | 作廢 | **`exit 3` / `ERR_CHECKER_MUTATED_SUBJECT`**，同上 |
| E11d | 在受檢目錄新增檔 | 記錄但不致命 | `ok=true`、`added` 已記錄 |
| E11e | 守衛根不存在 | spawn 前拒絕 | **`exit 4` / `ERR_GUARD_ROOT_MISSING`、`attempts=0`** |

其中 4 例已固化為回歸測試；scratch 帳本確保探針**不會污染真實 relay 帳本**。

### 3.3 回歸與測試

- Guard suite：`tests/test_lane_dispatch_ao_guard.py` → **34/34 OK**（exit 0）。
- 全量 holdout（canonical 制，`PYTHONPATH=src`）：**366 tests / 7 FAIL**；**失敗 ID 集合與變更前基線完全相同（BEFORE 332/7）→ 0 引入**。
- OpenSpec：`validate --strict` → valid（exit 0）。

### 3.4 對抗式審查（子代理執行，8 項繞道被證實，逐項先複驗再修）

樣本：F1 `--require-arm` 被巢狀於 gate 內（可繞）；F2 pool `identity_requirement` 在 `main()` 被丟棄；F3 登入探測以字串包含判定（偽陽性）；F7 `text=True` 在落檔前已破壞位元組；F8 attempt log 無 `run_id`（跨回合覆寫）。每一項修補均附**以該發現命名的回歸測試**。

---

## 4. 獨立驗收（acceptance，已落帳）

**這一步不是 maker 自判**：先立 oracle → 再派獨立 checker lane → verdict 由 checker 產生 → maker 僅**機械化轉錄**。

| 項目 | 值 |
|---|---|
| requirement | `REQ-AO-INDEP-012`（project `FAR-LANE-ROUTE-SLOTS-012`）→ **`ACCEPTED`**（version 4） |
| acceptance | `ACC-AO-INDEP-012` → **`PASS`** |
| checker lane | `VERIFY_SECURITY`，rank 1，**獨立 CODEX CLI 行程**，338.72s，`usage 200` |
| 該 lane 的逐字判決 | `VERDICT: PASS` / `UNVERIFIED: NONE` |
| verdict 映射規則 | **fail-closed**：非「乾淨 PASS 且 `UNVERIFIED: NONE`」一律記 `FAIL` |
| 證據 | `EVD-AO-INDEP-012-CHECKER`（checker 自身落檔 bytes）、`EVD-AO-INDEP-012-ARTIFACT`（凍結 manifest） |
| canonical events | **5 筆**：acceptance `NOT_RUN→PASS`（`EVT-8ed0663f03a5d7bb`）＋ requirement `CANDIDATE→FROZEN→IMPLEMENTED→VERIFIED→ACCEPTED`（`EVT-c2d2b247…`、`EVT-6c8c6c7e…`、`EVT-c3917124…`、`EVT-e1bcd23b…`） |
| `actor` 欄位 | `MAKER_LANE_TRANSCRIBING_CHECKER_VERDICT:VERIFY_SECURITY_LANE`（判決屬 checker，動列屬 maker，兩者不混同） |

**checker 自陳的驗證範圍**：C1 正向（**它自己另跑了一次巢狀 `--force-rank 4 --require-arm` 實測**，並比對 maker 落檔的原始 bytes）；C2 未釘 rank → `exit 3` 且別的 arm 那回合被作廢；C3 不健康 arm → `exit 4`、**沒有 attempts、沒有 log dir = 沒有 spawn**；C4 確定性守衛（突變作廢 ＋ 守衛根缺失零 attempt）；C5 `34 tests OK`。它同時自陳兩項天花板：**arm 健康探針是憑證檔檢查而非活體 relay 連線**，且它**未改動任何受控檔**。

---

## 5. Owner 裁決的執行結果

| # | 裁決 | 處置 |
|---|---|---|
| 1 | 核准 promotion | 已執行：`IC-48A73CF4`（CodePatchCandidate／risk MEDIUM／COV-11-06 `human_gate=required`）→ `state=PROMOTED`、`gate=HUMAN_APPROVED`；OpenSpec change 已 archive，delta 入 main specs（+16 requirements） |
| 2 | D-3 不必換模型 | **未做任何模型變更**。三條 lane 仍同模型 → maker==checker 在構造上可達；本輪提供的是 **process-only 獨立性**（獨立行程、獨立 receipt、digest 可自行重算），**不是**模型多樣性 |
| 3 | (ii) 切專用帳號 | **由 owner 更正撤銷 = NOT APPLICABLE**（見 §5.3）；agent **全程未取得／輪替／複製／讀取任何憑證、未執行登入、未發起任何登入視窗** |
| 4 | 用非模型確定性方式補齊 live negative | 已關閉（E11a–E11e，見 §3.2） |

### 5.3 (ii) 的撤銷與取代它的誠實敘述

Owner 原話：「這根本不是本次核心任務目的阿，而且我只有一個GPT帳號呀」。

- pool 與桌面**共用同一帳號 id**（digest `18d61772731a`），但 **token 值不同**（pool `f14ff738d342` vs human `8f2a50cac70d`）。
- 單一帳號下此耦合無可避免，其後果是**共用失效域（shared failure domain）**——帳號憑證被撤銷或方案到期時，無人 arm 與互動桌面**一起失效**——**不是**身分洩漏。
- 真正在位的緩解不是身分分離，而是：**閘門 fail-closed**（`ERR_RELAY_OAUTH_NEEDS_REAUTH`，E8/A4 實測）**而非靜默改跑別的 arm**；lane home 自有 `CODEX_HOME` 並經 relay URL 取用 arm，**從未讀取 human `auth.json`**。
- 要達到真正的身分分離**必須有第二個帳號**——屬**採購決策**，不由 agent 越權建議。

---

## 6. Claim ceiling 與未關閉的殘餘（隨本文件帶入，不因結案而關閉）

**Ceiling：**

1. 本輪為 **local verification ＋ owner-approved promotion ＋ process-only independence**；**promotion ≠ acceptance**（各自獨立落帳）。
2. AO / checker 的 verdict 一律 **ADVISORY**，不構成任何主體（subject）的驗收。
3. 守衛是**偵測（DETECTION）**，**不是阻止（prevention）**。

**Open residuals（已揭露、未關閉）：**

- **瞬時改寫／還原偵測不到**：兩點 digest 比較無法發現「改完又改回」的 TOCTOU 型改寫。
- **守衛根以外未量測**：宣告根之外的寫入不在本輪量測範圍。
- **F10**：既無 `--attempt-log-dir` 亦無 `--json-out` 時不落任何 log，而 `ok` 仍可能為真。
- **F13**：閘門探 relay **HOME** 憑證檔，而回合走 relay **URL**，兩者未交叉驗證。
- **D-3**：三條 lane 同模型（owner 刻意取捨：速度／CP 值／低風險）。
- **共用失效域**（§5.3）。

---

## 7. 自我揭露（本輪我自己造成的缺陷，全部已修並附測試）

1. **D-4 空泛通過**：守衛根無法解析 → 0 檔快照被報「乾淨」→ 修為 `ERR_GUARD_ROOT_MISSING` 拒絕。
2. **A3 假陽性**：A1–A4 驗收器首版把「找不到材質」的佔位字串判為 disjoint `PASS`（**與 D-4 同類：輸入缺失的比較器回報成功**）→ 改為三值判定 `PASS / FAIL / INCONCLUSIVE`，缺失一律視為**未驗收**。修正後 `A1` 才是誠實的 `FAIL`。
3. **自我指涉（3 次）**：manifest 把自己列進清單（記錄到上一版 size/digest）；freeze 執行中的 run log 被列入 manifest（寫入中 digest 不穩）→ 一律改為**由構造排除**，不事後修補 digest。
4. **測試設計缺陷**：首版 F6 測試因守衛根指向別處而**誤 spawn 一回合**（~121s，未列 receipts）→ 已修正測試，整組重跑 1.3s。
5. **成本低估（更正）**：我提出 acceptance lane 時說「一回合」；**實測該步驟在 relay 帳本留下 27 筆 `usage 200`**（25 × `deepseek-v4.1-flash` ＋ 2 × `gpt-6.1-sol`），視窗約 8 分鐘——原因是 checker 自行跑了多次 dispatcher 子探針，而每個 attempt 都會落列。
6. **獨立重算子代理推翻我的宣稱**：「10 個全失敗」僅在未設 `PYTHONPATH=src` 時字面成立；canonical 下為 7/10 fail（3 個實為 `ModuleNotFoundError`）→ 已重測 A/B 並改以集合比較。

---

## 8. 副作用揭露（本輪全部）

| 類別 | 事實 |
|---|---|
| `src/**` | **未改動** |
| 服務重啟 | **無** |
| 憑證操作 | **無**（未取得／輪替／複製／讀取任何憑證，未執行登入） |
| **canonical store 寫入** | **有**：`var/shared-spine/hg-kseos.db` 的 `improvement_candidates` 得 `IC-48A73CF4` promotion 列；acceptance act 另寫 **5 筆 canonical_events ＋ 2 筆 evidence_refs ＋ 2 筆 leases**（全走**型別化 API**，未下 raw SQL）。**注意**：evolution promotion 路徑**不寫** `canonical_event` 亦**不寫** `release_decision`，故 promotion 本身**沒有事件日誌**。 |
| OpenSpec main specs | **已寫**（`openspec/specs/ao-lane-independent-verify/spec.md`，+16 requirements），owner 核准 |
| route promotion | `false` |
| relay 用量 | 見 §7.5（acceptance 步驟 27 列為實測值） |
| 受控檔以外 | 本輪產物全部落在 `var/far-ao-independence-20261010/` 與 `evidence/review/` |

---

## 9. 重現指令（隨附期望輸出）

```bash
# 1) 核心目標：無人窗口 gpt-6.1-sol（需 relay 10101 健康）
PYTHONPATH=src .venv/Scripts/python.exe scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY --force-rank 4 \
  --require-arm openai-codex/gpt-6.1-sol --attempt-log-dir var/<round>/logs/e12 --timeout 240 \
  --json-out var/<round>/receipts/E12.json \
  --prompt 'Reply with exactly one line: OAUTH_ARM_SERVED_UNATTENDED . Then end with a final line containing only HGK_LANE_NONCE_OK'
# 期望：dispatch exit 0；receipt ok=true；required_arm == served_arm == openai-codex/gpt-6.1-sol；usage 200 gpt-6.1-sol

# 2) 不健康 arm 必須 fail-closed（不 spawn）
... --relay-home <不存在的路徑> ...
# 期望：exit 4 / ERR_RELAY_OAUTH_NEEDS_REAUTH

# 3) 確定性負測（無模型、不耗 relay 額度）
bash var/<round>/run_negative_deterministic.sh
# 期望：E11a/…/E11e 全 PASS；E11b/E11c 為 exit 3 / ERR_CHECKER_MUTATED_SUBJECT

# 4) 守衛回歸套件
.venv/Scripts/python.exe -m unittest tests.test_lane_dispatch_ao_guard
# 期望：Ran 34 tests ... OK
```

---

## 10. 產物處置（manifest，含未發布項與理由）

本輪凍結收據：`FREEZE_MANIFEST.json`，**165 round artifacts ＋ 15 repo files = 180/180 digest 通過、0 檔案晚於凍結時間**，sha256 `27a255646ee618a8d60b76049873b21489a7376f6737c96c5e9a7a788c456f92`，`frozen_at_utc 2026-10-10T15:46:53Z`。

| 類別 | 處置 |
|---|---|
| 本文件與 `IMPLEMENTATION_SUMMARY.md` | **DELIVERED**（發布至本 repo 的 `evidence/FAR-AO-INDEPENDENCE-20261010/`） |
| `RESEARCH_REPORT_AO_INDEPENDENCE.md`（30058 B，sha256 `adcbdc1309efc258…`） | **DELIVERED（mirror）**，作為 FABRIC 側 evidence |
| receipts / logs / probes（`var/far-ao-independence-20261010/**`） | **EXCLUDED from publication**：這些是機器產生的原始證據，路徑慣例為本機 `var/`（本 repo 既有發布從不含 `var/`）。**保留於本機**，以 §2 與 §3 的 digest 綁定引用 |
| `var/shared-spine/hg-kseos.db`（spine 本體） | **EXCLUDED**：二進位資料庫，非文件發布物；其狀態以 §4 的 event id 引用 |
| `config/*.bak-*` | **EXCLUDED_SCRATCH**：修改前備份，僅供 rollback |

---

## 11. 對應本 repo 的文件更新

本輪同步更新（同一發布）：`HG-KSEOS/README.md`（§2c 新增 ＋ claim 標頭）、`HG-KSEOS/AGENTS.md`（version ＋ 新作業規則）、`HG-KSEOS/docs/HG-KSEOS使用說明文檔.md`（lane dispatch 一節），以及 FABRIC 側 `FABRIC/README.md`、`FABRIC/AGENTS.md`、`FABRIC/docs/Fabric使用說明文檔.md` 與其 `evidence/review/` mirror。
