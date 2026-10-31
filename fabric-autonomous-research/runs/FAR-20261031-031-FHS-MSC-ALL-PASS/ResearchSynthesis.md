# FAR-20261031-031｜FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1
## 未完成項目盤點、ALL-PASS 路徑、工程裁決與授權建議

| | |
|---|---|
| Run | `FAR-20261031-031-FHS-MSC-ALL-PASS` |
| 日期 | 2026-10-31（UTC+8），實測窗口 20:23–20:40 |
| 研究對象 | `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`（含其 22 個 WP 的實際完成度） |
| 治理契約 | Fabric（policy / contract 消費端，不產生 PASS） |
| 產品工程入口 | SBL / FHS-MSC（DOC-00～13 語義權威） |
| 控制平面 | HG-KSEOS（唯一 normative：WorkOrder、SharedSpine、acceptance、release） |
| 車道 | PLAN `openai-codex/gpt-6.1-sol` ／ EXECUTE `opencode-go/deepseek-v4.1-flash` ／ VERIFY `opencode-go/mimo-v2.6-flash`（實測見 §4） |
| Claim ceiling | `MEASURED_RESEARCH_AND_ENGINEERING_VERDICT`；本報告**不宣稱**任何 WP 已由本輪升為 PASS、不宣稱 native/release |

> **方法聲明（FAR §7 source-as-data）**：本報告每一條「已完成／未完成」都綁到一個檔案、一次指令輸出或一次 API 讀回；凡無法重算者標 `NOT_MEASURED`。對話紀錄、上一輪的摘要文件一律不當證據——本輪已實測推翻三份先前文件的三項主張（§5）。

---

## 0. 三句話結論

1. **封包本身是完整的**：我在 `C:\wg\pkg` 獨立重算 **909/909 逐檔 SHA 相符、0 缺、0 不符**，17 主冊 + 14 SBL 升級冊全在。你手上那個資料夾副本是**有損副本**（415 列缺失：398 列超過 Win32 260 字元上限、17 列是目錄改名），不是封包壞了。
2. **22 個 WP 現在是 16 PASS / 3 FAIL / 3 NOT_RUN**（控制平面 `work_queue`，2026-10-31T11:17Z）。6 個非 PASS **全部是 `HOST_OP` 效應類**，全部以 `REFUSAL-20261030-NO-HOST-CAPABILITY` 拒絕。授權那一關已經過了（`R21-CANON-c0542636` 已簽，允許 7 包 `HOST_INSTALL` 至 2026-11-14）；**缺的是每包的 writeset → permit → install → fresh-load → 獨立 VERIFY**，而這條鏈目前**一步都還沒開始**（`var/permits/`、`var/R21-NATIVE-EXEC/` 不存在）。
3. **「VERIFY 車道壞了、無法獨立驗收」這個結論是錯的**。本輪實測：三條車道**全部可服務**——PLAN `gpt-6.1-sol` 6.19 s 回 nonce、EXECUTE `deepseek-v4.1-flash` 1.85 s 回 nonce、VERIFY `mimo-v2.6-flash` 成功且 `required_arm == served_arm`。過去失敗的真正原因是**身分來源走錯**（`identity_source=relay-usage` 在本機拿不到 usage 列）＋**prompt 沒要求回 nonce**；改用 `--identity-source codex-rollout` 後同一臂一次通過。這是一行程式參數，不是能力缺口。

---

## 1. 研究請求（R0）與來源分母（R2）

**Decision question**：`HANDOFF-PATCH-v1` 還有哪些項目尚未實際完成／PASS？如何全部實際完成並達成 ALL PASS？殘留／缺口／阻斷／未關閉項目如何關閉？哪些需要 owner／issuer 決策授權？哪些候選可升格？哪些未併入 main 的分支可併入？

**來源分母**（本輪實際讀取，全部可定位）：

| 類別 | 來源 | 用途 |
|---|---|---|
| 交付本體 | `C:\wg\pkg`（canonical 解包）＋ `SHA256_PAYLOAD_MANIFEST.json`（909 列） | 完整性重算 |
| 你的副本 | `知識庫\…\FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`（917 檔／228 MB） | 副本有損量測 |
| 控制平面 | `HG-KSEOS\var\shared-spine\hg-kseos.db`（`work_queue` 22 列、`acceptances` 955 列） | WP 狀態權威 |
| 上一輪收據 | `var\FHS-HANDOFF-EXEC-20261030\receipts\`（28 份，P1–P17） | 已宣稱事實的再核 |
| 上一輪移交 | `HG-KSEOS\ops\session-20261031\HANDOFF.md`、`IMPLEMENTATION_INDEX.md` | 2026-10-31 現況 |
| 治理 | `config/lane-routing-registry.yaml`（epoch 39）、`config/model-lane-assignment.json`（rev 39） | 車道綁定 |
| 遠端 | GitHub API：4 repo × PR（`state=all`）、`git merge-tree` / `git merge-base` | 合併判定 |
| 車道實測 | `scripts/hgk-lane-dispatch.py` 5 次派送 + `hgk-lane-preflight.py` 1 次 | 可服務性 |

**不採用為證據**：`FINAL_HANDOFF.md` 的「PR #7 open / no merge」（實測已 merged）、`FHS-B1_使用說明文檔` §7 的「四個 PR 待簽收後合併」（實測四支全部已併）、`P10` 的「無獨立臂可用」（作者自己已在 `P11` 撤回，本輪再以實測確認撤回正確）。

---

## 2. 實測現況（Measured）

### 2.1 封包完整性 — PASS

| 檢查 | 結果 | 命令 |
|---|---|---|
| 909 列逐檔 SHA-256 | **909 matched / 0 missing / 0 mismatch** | 對 `C:\wg\pkg` 重算 `SHA256_PAYLOAD_MANIFEST.json` |
| 17 主冊 + 14 SBL 升級冊 | 17 / 14 全在 | `01_SUBSTANTIVE_BODY\` 與 `…\SBL_DOC00_13_INTEGRATED_READER_UPGRADES\` |
| BODY 封存 | 114 entries / 4,007,065 B / `5e722cfb…` byte-exact（P15 O2） | `P15_AO_ACCEPTANCE.json` |
| EVIDENCE 封存 | 801 entries / 25,914,281 B / `0e7763b8…` byte-exact（P15 O3，作者原「短少 4,801 B」主張已撤回） | 同上 |

### 2.2 你的資料夾副本 — 有損（415/909 缺）

| 缺失成因 | 列數 | 說明 |
|---|---:|---|
| 路徑 ≥ 260 字元（Win32 MAX_PATH） | **398** | 解壓時靜默截斷；含 14 冊 SBL 升級冊與 384 個證據子樹檔 |
| 目錄改名 `01_SUBSTANTIVE_BODY` → `01_FHS-MSC_PIPD-LS-PKG_BODY` | **17** | manifest 與 `INDEX.md` 仍寫舊名；17 主冊本體存在，改名後 17/17 SHA 相符 |
| 合計 | **415** | 副本最大可見路徑長度 = 259，≥260 者 0 檔——這就是截斷線 |

**這是可修復的展示層缺陷，不是交付缺陷**。修法：用支援長路徑的解壓（`7z x -spe` / `\\?\` 前綴 / `tar -xf`），再把目錄名與 manifest 對齊（見裁決 V6）。

### 2.3 22 個 WP — 四份互相矛盾的記分板

| 記分板 | 位置 | DONE/PASS | PARTIAL | PARKED/FAIL | HOLD/NOT_RUN |
|---|---|---:|---:|---:|---:|
| **控制平面（權威）** | `hg-kseos.db:work_queue` | **16 PASS** | — | **3 FAIL**（10,12,13） | **3 NOT_RUN**（11,17,20） |
| 佇列投影 | `/c/wg/queue/TODO.md`、`GOAL.json` | 16 | — | 3 | 3 |
| 終態宣告 | `R18…/receipts/TERMINAL_STATE.json` | 2 DONE | 12 | 7 PARKED | 1 HOLD（05） |
| 驅動器 | `R18…/DRIVER_STATE.json` | 6 | 13 | 7 | — |

同一批 22 包，四份檔案給出四種答案；`HANDOFF.md` 又說「defensible 22/22, stop_condition_met: true」。**在記分權威統一之前，任何「ALL PASS」宣告都不成立**（見根因 RC-1、裁決 V1）。

**6 個非 PASS 的具名理由**（`acceptances` 表，`REFUSAL-20261030-NO-HOST-CAPABILITY`）：

| WP | 標題 | 效應類 | 狀態 | 缺什麼 | 授權是否已備 |
|---|---|---|---|---|---|
| WP-FHS-10 | B1 3 GWO & G-A/G-B | HOST_OP | FAIL | 被當成「無 host 能力」拒絕；**實際證據已存在**（B1 `GATES.json`：G-A 6/6、G-B 3/3、GWO ALL_THREE_PASS、checker `gpt-6.1-sol` PASS、`mission_complete true`） | 不需新授權，只需**重綁** |
| WP-FHS-12 | W18 Normal Mode | HOST_OP | FAIL | 新 PID 普通 Goal 的正式 Profile／ToolAutoSelect／真 served／test-only 移除 | R21 已含 |
| WP-FHS-13 | CAP On-Demand + HotSwap | HOST_OP | FAIL | 替代 Parity 與原功能同 | R21 已含 |
| WP-FHS-11 | Portable Host Dogfood | HOST_OP | NOT_RUN | 每 Portable SP 的 install/load/invoke/nontrigger/remove | R21 已含；**缺 writeset**（無 `candidate/`，須由 `pkg-src/`+`build/` 推導） |
| WP-FHS-17 | CAP-BOOT Native Occupants | HOST_OP | NOT_RUN | needed occupant 先建、再驗 LoadedSHA；18/18 artefact 已備、`reproduce.ps1` REPRODUCED | **不在 R21 allowlist**；走 `issue_grant.py`（Ed25519，`key_id 135455ca00280c39`） |
| WP-FHS-20 | CLI/Agent/Host Kind Matrix | HOST_OP | NOT_RUN | 192 組合每 Host/Mode/Provider 具本 cell Raw 或明確 NoFit；`candidate_digest 5b448c2a6d62e6f3` 已存在 | R21 已含 |

> WP-10 這一列是本輪最重要的發現：它被計為 FAIL，但它的 oracle 證據**已經在 B1 輪產出並簽章**，`checker_receipt_codex_r7.json` 的 SHA-256 我重算 = `97496bbb…`，與 `GATES.json` 宣稱值相符。這是**綁定缺口，不是能力缺口**。

### 2.4 車道 — 三條全部可服務（實測）

relay：`ocx 2.11.0`，`127.0.0.1:10101/healthz` ok，PID 8432，`providers.openai.disabled=false`。

| 車道 | 臂 | 派送參數 | 結果 | 秒 | nonce | 收據 |
|---|---|---|---|---:|---|---|
| PLAN | `openai-codex/gpt-6.1-sol` | `--force-rank 1 --require-arm … --codex-home C:/Users/user/.codex --allow-human-home-transport --identity-source codex-rollout` | **ok, required==served** | — | ✓ | `evidence/lane_dispatch_plan.json` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | 同上但無 home 覆寫 | **ok, usage_receipt_ok** | 1.85 | ✓（prompt 要求回 nonce） | `evidence/lane_dispatch_exec2.json` |
| VERIFY | `opencode-go/mimo-v2.6-flash` | `--force-rank 1 --require-arm …` | **ok, required==served** | — | ✓ | `evidence/lane_dispatch_verify2.json` |
| VERIFY | `openai-codex/gpt-6.1-sol` | `--force-rank 2`（**不加** `--require-arm`） | **ok，served `gpt-6.1-sol`** | 6.75 | ✓ | `evidence/lane_dispatch_verify_sol.json` |
| VERIFY | `openai-codex/gpt-6.1-sol` | 加 `--require-arm` | **拒絕，未 spawn**：`ERR_ARM_NOT_IN_ASSIGNMENT`（rev 39 只列 mimo，`alternates_are_operator_selectable: false`） | — | — | `evidence/lane_dispatch_verify.json` |
| EXECUTE | `deepseek` | 不加 `--identity-source`（預設 `relay-usage`） | **ERR_LANE_ALL_ROUTES_EXHAUSTED**——模型其實答了，是 predicate 失敗（`usage_rows_after_offset: 0`、`nonce_present: false`） | 1.85 | ✗ | `evidence/lane_dispatch_exec.json` |
| PLAN | `gpt-6.1-sol`（T2 preflight，直連 openai 平面） | `hgk-lane-preflight.py` | `LANE_INCONCLUSIVE`：`responses_websocket` 連不上 | — | ✗ | `evidence/lane_preflight_gpt61.json` |

**兩個結論**：
- (a) 失敗類別是 **predicate／transport**，不是臂不可用。`relay-usage` 這條身分來源在本機永遠拿不到 usage 列，因此任何車道都會「耗盡」；`codex-rollout` 一次通過。
- (b) 你指定的 VERIFY = `gpt-6.1-sol` **技術上可服務**（6.75 s 成功），但**治理上目前不可選**：rev 39 的 assignment 只列 mimo 且明示 alternates 不可由 operator 選。要用 gpt-6.1-sol 做 VERIFY 並留下 `required==served` 的證據級收據，必須由 owner 發 **revision 40**（§6 D-3）。

### 2.5 治理／政策 — 已由髒工作區回到乾淨

| 事實 | 值 |
|---|---|
| `config/lane-routing-registry.yaml` | `epoch 39` / `contract_epoch 34` / `revision 39`，**已 commit，工作樹 0 變更** |
| `config/model-lane-assignment.json` | `revision 39` |
| 綁定 | PLAN `gpt-6.1-sol`、EXECUTE `deepseek-v4.1-flash`、VERIFY_SECURITY `mimo-v2.6-flash`（owner order 2026-10-31） |
| P16 當時 | `POLICY_DIRTY`：HEAD rev 33 vs 磁碟 rev 38、4 檔未 commit、落後 7 天 → **現已修** |

### 2.6 GitHub — 合併狀態（實測 API）

- **已併入 main**：HG-KSEOS #3/#4/#6/**#7**、Fabric #19、SBL #14、PIPD #21/#18/#17。
  → **HANDOFF-PATCH-v1 的執行輪 PR #7 已經在 main 上**（merge sha `1e98abf71b`，2026-10-30T11:39Z）；`FINAL_HANDOFF.md` 的「open, no merge」是過期敘述。
- **未併、可併（12 支 clean）**：HG-KSEOS #1/#2、Fabric #18/#17/#15、SBL #9/#10/#11/#12/#13、PIPD #15/#14。
- **未併、不可直接併**：Fabric #16（`dirty`，衝突）；PIPD #19/#20（`unstable`，commit status 未綠）；HG-KSEOS #5（`unknown`，base 是 r18）。
- **血緣問題（結構性）**：`candidate/r18-fhs-skeleton-spine-20261029` 與 `candidate/r19-fhs-implementation` 對 `origin/main` **`merge-base = NONE`（unrelated histories）**，r18 相對 main 為 **264 ahead / 83 behind**。2026-10-31 整輪工作（`287c8df`、`7e093ef`、R21 簽章、owner_window、queue-patches）**只存在於 r18**，用正常 merge 永遠進不了 main。

---

## 3. 「尚未實際完成 / PASS」完整清單

分類沿用交付包自己的四類（`GAPS_CLASSIFICATION_AND_RESUME.json`）＋本輪新增兩類。

### A. SOURCE_RESOLVABLE／可自解（不需外部決策）

| ID | 項目 | 現況 | 關閉動作 |
|---|---|---|---|
| A-1 | **WP-FHS-10** 被誤判 FAIL | 證據已在 B1（GATES + checker 收據，SHA 相符） | 以 typed spine 重綁 `ACC-WP-FHS-10` → 重跑該 WP 的 Reader 讀回，狀態改 PASS；不重跑 native |
| A-2 | 副本 415 列缺失 | 398 MAX_PATH + 17 改名 | 長路徑解壓 ＋ 目錄/manifest 對齊 ＋ 重驗 909/909 |
| A-3 | `PACKAGE_READBACK.json` 缺席（F-01） | 交付根無此檔；`C:\wg\seal2\PACKAGE_READBACK.json`（1,710 B）存在 | 以 seal2 版本補入交付根並在 `SHA256_DELIVERY_MANIFEST.md` 標明來源，或重封一次 |
| A-4 | 記分板不一致（4 份） | §2.3 | 指定 `work_queue` 為唯一權威，另三份降為投影並加一致性 gate |
| A-5 | 車道 predicate（`relay-usage` 永不出 usage 列） | 實測 | 把 `identity_source` 預設改 `codex-rollout`；prompt 模板強制回 nonce；把 `ERR_LANE_ALL_ROUTES_EXHAUSTED` 細分為 `ERR_LANE_PREDICATE_*` |
| A-6 | 你指定的 VERIFY 臂不可選 | rev 39 只列 mimo | owner revision 40（D-3）或改用 mimo（零治理變更） |
| A-7 | 封包 35/35 依賴 `READERS` 快照、`prepare.py` 無法重建（F-13） | 已記錄 | 把 `READERS` 快照納入 manifest 並讓 `prepare.py` 可重建；否則 35/35 不可異機重現 |
| A-8 | `elapsed_seconds` 十六位數相同（F-14） | 34/1 與 35/0 兩份記錄共用耗時 | 重跑一次並記錄真實耗時；保留兩份為異常證據 |

### B. REPO_BINDABLE／可綁定（本輪已完成或可即刻完成）

| ID | 項目 | 現況 |
|---|---|---|
| B-1 | 24 功能句 → 24 Atom、PI/PD/TaskSpecSeed/三 SPEC | 已綁，`validate_pi` PASS、strict handoff PASS、`KnownAnswer_reasked 0` |
| B-2 | HGK 純 request constructor（taskspec/workorder） | 已靜態綁，POS + foreign-root NEG；canonical `create_*` 未呼叫 |
| B-3 | WP-FHS-17 18/18 artefact ＋ `reproduce.ps1` | 已 REPRODUCED（218 artefacts），只差 permit |
| B-4 | 22 WP 契約 harness | 22/22 `contract_ok`；11 需 native authority、11 無需 |

### C. OWNER_DECISION_REQUIRED／需 owner 裁決（詳見 §6）

`H-HOST-MAP`（Host matrix 版本未批准）、`H-PROVIDER`（token→boolean 未綁）、`H-CLI14`（CLI 13 vs 14 的正式契約）、`CR_ORACLE_001`（DOC-07 與 legacy DOC-03 的 native ratification）、`SOURCEFREEZE_DECLARED_HOLD`（9/9 冊未正式凍結）、per-principal keys（3 SID / 1 key）、以及本輪新發現的車道 revision、血緣合併、封存採用、layout/manifest 修復、identity scoping、WP-15 closure edge。

### D. NATIVE_EVIDENCE_REQUIRED／需原生收據

`canonical admission`、`actual loaded/served`、`bounded worker / world effect / reconcile`、`independent acceptance`、`release`。目前：**NATIVE_NOT_RUN、INDEPENDENT 已可跑（§2.4）、RELEASE NOT_RUN**。

### E. 產品語義差額（保留在原 WP，不阻斷首工作）

- **7649 筆量詞子項**：`SBL-D00-L00070-C01` 為第一作者端失敗（`AUTHOR_COMPOUND_SUBITEM_CONTRACT_INCOMPLETE`）。這是**作者可由來源修補**的缺陷，不可改標 HOLD。
- **282 Runner/W18 case**：全部 `NOT_RUN`，需逐 case registry request。
- **949 R15** owner 差額、**96 Oracle**、**192 Cell** host/provider 對照、**485 技術資格**。

### F. 基礎設施／營運（非產品，但阻塞無人值守）

| ID | 項目 | 現況 |
|---|---|---|
| F-1 | `/c/wg/queue` 無 git remote | 只有本地 commit `3fca7b9` ＋ bundle `a3f2c03bf413…`；一次磁碟故障即全失 |
| F-2 | 第二個 Hermes 實例 `D:\Hermes-Recovery\live22` | `TT-HOST-SECOND-HERMES-001`，未關 |
| F-3 | 排程 `\Root\HGK-OpenCodex-Sealed-10101` 每 5 分鐘 | FAR-028 F7，未關 |
| F-4 | 228 MB 凍結 subject 與 1 GB `var/` 輪次 | 無備份（`IMPLEMENTATION_INDEX.md` §2 自承） |

---

## 4. 為什麼到現在還沒 ALL PASS（根因，R4）

| ID | 根因 | 證據 | 若不修的後果 |
|---|---|---|---|
| **RC-1** | **記分權威分裂**：四份記分板並存，沒有 gate 檢查它們一致 | §2.3 | 任何「ALL PASS」都可被另一份檔案否定；驗收無法收斂 |
| **RC-2** | **能力缺口與授權缺口被混為一談**：6 個 `HOST_OP` 一律以 `NO-HOST-CAPABILITY` 拒絕，但 R21 已授權 7 包、WP-10 證據早已存在 | `acceptances`、`R21_signing_receipt.json`、B1 `GATES.json` | 授權做完了卻還在等授權；真正缺的 writeset 沒人做 |
| **RC-3** | **車道 predicate 缺陷被讀成能力缺口**：`relay-usage` 身分來源在本機永不出 usage 列，於是「所有路由耗盡」 | §2.4 兩次對照 | 每輪都重複「VERIFY 不可用 → 無法獨立驗收 → 停在 HANDOFF_READY」 |
| **RC-4** | **主幹血緣斷裂**：r18/r19 與 main 無共同祖先 | `merge-base = NONE` | 最新治理工作永遠進不了 main；`main` 與工作線持續分叉 |
| **RC-5** | **交付封裝對 Win32 不友善**：`01_SUBSTANTIVE_BODY` 改名 ＋ 深路徑 | §2.2 | 每個拿到封包的人都會得到「415 列缺失」的假故障，重複調查 |
| **RC-6** | **政策曾長期是髒工作區**（rev 33 HEAD / rev 38 磁碟，7 天） | P16（現已修，rev 39 clean） | 收據無法異機重現；舊 schema 讀者解析不到 |

RC-3 與 RC-6 有共同形狀：**宣告層（assignment/config）與服務層（實際 served）之間沒有 fail-closed 的一致性檢查**。建議的機器級閘門：`served_arm == required_arm` 且 `identity_source` 必須能產出 usage 或 rollout 證據，否則拒絕啟動而非「耗盡」。

---

## 5. 本輪推翻／修正的先前主張（誠實記錄）

| 先前主張 | 出處 | 本輪實測 | 判定 |
|---|---|---|---|
| 「PR #7 open，未合併」 | `FINAL_HANDOFF.md` §1 | PR #7 `merged=True`，merge sha `1e98abf71b` | **過期** |
| 「四個 B1 PR 待 owner 簽收後合併」 | `FHS-B1_使用說明文檔` §7 | #3/#19/#21/#14 全部已 merged | **過期** |
| 「沒有任何獨立臂可用，INDEPENDENT_ACCEPTED 今日不可達」 | `P10`（已被 `P11` 撤回） | VERIFY `mimo` 成功且 `required==served`；`gpt-6.1-sol` 以 rank 派送亦成功 | **撤回正確，且可再加強** |
| 「EVIDENCE 封存短少 4,801 B」 | `FINAL_HANDOFF.md` §1 | `P15` O3 已 byte-exact 重現；`P12` 亦已推翻 | 已撤回 |
| 「12/30 是缺口」 | 早期 FAR | 分母＝registry 列數；書面要求僅 `INSTALLED`（30/30 已滿足） | 維持「inventory，不是 gap」 |

---

## 6. 待 OWNER / ISSUER 決策授權項目（15 項，含建議）

| ID | 決策 | 誰 | 建議裁決 | 成本 | 可否延後 |
|---|---|---|---|---|---|
| **D-1** | r18/r19 與 main 的血緣（unrelated histories） | owner ＋ repo admin | 以 `--allow-unrelated-histories` 做一次**具名 graft merge**，在 merge commit message 寫明兩條根的來源與時間；之後 `main` 單線 | 1 次合併、1 次簽章 | **不可**（不解決則 2026-10-31 全部工作永遠不在 main） |
| **D-2** | 12 支 clean PR 是否併入 | owner | 分批併：先「證據類」（SBL #9–#13、PIPD #14/#15、Fabric #15/#17/#18），再「程式類」（HG-KSEOS #1/#2） | 12 次 merge | 可延後，但每延一天分叉多一天 |
| **D-3** | VERIFY 車道臂：`mimo-v2.6-flash`（現行 rev 39）或回到 `gpt-6.1-sol`（你的指定） | owner | **建議維持 mimo**（已在 registry 內、模型軸與 EXECUTE 相異、零治理變更）；若必須用 `gpt-6.1-sol`，發 **revision 40**：VERIFY rank1=`gpt-6.1-sol`、rank2=`mimo`，並記錄「human-home transport 破壞 sealed-home 不變式」的代價 | rev 40 = 1 次 config 變更 ＋ 1 次 resync | 不可（決定本輪 VERIFY 證據的合法性） |
| **D-4** | WP-FHS-05 HOLD | PIPD Writer | 以 PIPD Writer 身分對 `61 candidates / ack 0` 給出 writer ACK 或明確 NoFit | 1 次裁決 | 可（僅 1 包） |
| **D-5** | `HOST_PROVIDER_LEGACY_MAP`（DeepSeek48→ChatGPT 遷移） | Product/Host/Provider Owner | 先給「同版本映射決議」；未決前保持 `bool=null` + runtime disabled（現況即 fail-closed，正確） | 1 次裁決 | 可 |
| **D-6** | `CR_ORACLE_001`（DOC-07 與 legacy DOC-03） | PIPD DOC07 / legacy Schema Owner | 採 PIPD PR #20（oracle compat API）為候選，補 native ratification readback | 1 次裁決 ＋ CI 綠 | 可 |
| **D-7** | CLI 13 vs 14 的正式契約 | PIPD CLI/Schema Owner | 定 14 為正式並更新 exact-set 與 `test_oracle_compat` | 1 次裁決 | 可 |
| **D-8** | SourceFreeze 9/9 `HOLD` 是否正式凍結 | SBL owner | 採「凍結不改正本」：逐檔 sha256 manifest ＋ 1 次解鎖 1 個簽章 ＋ `SOURCEFREEZE.json`，0 位元組變更 | 1 次解鎖 | 可，但 native admission 會一直帶著 `SOURCEFREEZE_DECLARED_HOLD` |
| **D-9** | per-principal keys（3 個 SID、1 把 key） | owner | B1 已裁 `ACCEPTED_AS_SUFFICIENT`；若要走真分離，需 3 把 key 與 3 次簽章 | 3 次簽章 | 可 |
| **D-10** | `/c/wg/queue` 的 remote | owner | 指定一個 repo（建議 `shw097-team/HG-KSEOS` 的 `queue/` 子樹，或新 repo `FHS-QUEUE`）並 push | 1 次建立 | **不可**（無人值守的執行證據只存在一顆磁碟） |
| **D-11** | 第二 Hermes 實例與 5 分鐘排程 | owner | 關閉 `D:\Hermes-Recovery\live22`、停用 `\Root\HGK-OpenCodex-Sealed-10101`（或改為 on-demand） | 2 個動作 | 可（但屬共用失效域） |
| **D-12** | 新封存（seal2）是否採用為 canonical | owner | 採用 `C:\wg\seal2` 兩檔 ＋ `PACKAGE_READBACK.json`；舊封存標 superseded | 1 次宣告 | 可 |
| **D-13** | layout/manifest 修復（F-02） | owner | 採「manifest 與目錄同名」方向：把交付目錄改回 `01_SUBSTANTIVE_BODY`，重算 909 列 | 1 次重封 | 可（但每個收件人都會被 415 列嚇一次） |
| **D-14** | identity scoping（F-04：`PI-d0974c55…` 綁絕對 root） | owner | 採 root-relative identity，兩種 root 下同 digest | 1 次程式修補 ＋ 重跑 | 可 |
| **D-15** | WP-FHS-15 closure edge（`{00,15}` vs 宣告 `{00,01,15}`） | owner | 以 typed edge 為準修正宣告文字（宣告錯，不是圖錯） | 1 次文字修補 | 可 |

---

## 7. 候選升格（已檢測、可升為實用）

| # | 候選 | 證據 | 升格動作 | 風險 |
|---|---|---|---|---|
| P-1 | **`--identity-source codex-rollout`** 為車道預設 | 3/3 車道實測通過（§2.4） | 改 `config/verify-lane-contract.json` 預設 ＋ dispatcher 對 `relay-usage` 無 usage 列時 fail-closed 並具名 | 低；需一次 lane 政策 revision |
| P-2 | **`durable_import.py` 的三道防空洞閘**（`WALK_INCOMPLETE` / `FILE_COUNT_MISMATCH` / `EMPTY`） | P17：正測 911=911、負測 9110→exit 6 | 升為交付匯入的**唯一**工具（禁止裸 `os.scandir`） | 低 |
| P-3 | **`R21-CANON-c0542636`**（HOST_INSTALL、7 包、至 2026-11-14） | `signature_verifies: true`、`ops_used_after: 2` | 直接投入使用（§8 Phase 2） | 已生效 |
| P-4 | **WP-FHS-17 的 `reproduce.ps1`**（218 artefacts、REPRODUCED） | `queue-patches/`、queue commit `3fca7b9` | 交 officer 重坐一次即可 | 低 |
| P-5 | **B1 `GATES.json` ＋ checker 收據** 作為 WP-10 證據 | SHA `97496bbb…` 相符 | 重綁 ACC，不重跑 | 低 |
| P-6 | **F3 console-window gate** | HG-KSEOS `440cb34`、`ROUND_MAY_CLOSE` | 已在 main 線，維持 blocking | — |
| P-7 | **FAR-028/029/030 根因報告** | Fabric `2527b81`/`31a97ed`/`325e4fe` | 已 push，作為 recurrence ledger 輸入 | — |
| P-8 | PIPD PR #20 oracle compat API | `mergeable=True, unstable` | 先讓 CI 綠，再由 D-6 決定 | 中（語義權威） |

**不可升格**（維持候選／拒絕）：`P10` 的「無獨立臂」結論（已撤回）、`12/30 effect runner`（8 條輸入不存在，實作即造假）、任何把 `claim_ceiling` 當已簽內容的用法。

---

## 8. 分支／候選併入 MAIN 判定

| Repo | 分支／PR | 判定 | 依據 |
|---|---|---|---|
| HG-KSEOS | #1 `codex/b1-r5-native-admission` | **可併**（clean） | merge-tree clean；10 檔 +1153/−19 |
| HG-KSEOS | #2 `codex/b1-r6-artifact-scope` | **可併**（clean） | 2 檔 +65/−5 |
| HG-KSEOS | #5 `candidate/r19-fhs-implementation` | **不可直接併** | base 是 r18；r18 與 main `merge-base NONE` → 併 #5 前必須先做 D-1 |
| HG-KSEOS | `candidate/r18-fhs-skeleton-spine-20261029` | **不可直接併（血緣）** | unrelated histories；264 ahead / 83 behind；承載 2026-10-31 全部工作 |
| Fabric | #18 / #17 / #15 | **可併**（clean） | API `mergeable_state=clean` |
| Fabric | #16 `homepage/cnv-hygiene…` | **不可併（衝突）** | `mergeable_state=dirty` |
| SBL | #9 / #10 / #11 / #12 / #13 | **可併**（clean） | 全部 clean |
| SBL | `candidate/r14-ts15-kinds`（本地） | **不可併（衝突）** | merge-tree 在 `evidence/security/SECRET_SCAN.json` 衝突 |
| PIPD | #14 / #15 | **可併**（clean） | clean |
| PIPD | #19 / #20 | **暫緩** | `mergeable_state=unstable`（commit status 未綠） |
| PIPD | `b1/closure-20261029`（本地） | **可併**（clean） | tree `ead090e3` |

---

## 9. 最佳工程裁決（V1–V9）

上位裁決順位：①對齊 HANDOFF-v1 ②Native E2E 自主執行閉環 ③無人值守 ④必要性 ⑤適度治理 ⑥適度工程化。衝突時前者勝。

| # | 裁決 | 為什麼（對齊上位順位） |
|---|---|---|
| **V1** | **指定 `hg-kseos.db:work_queue` 為 22 包狀態的唯一權威**；`TERMINAL_STATE.json`、`TODO.md`、`GOAL.json`、`HANDOFF.md` 降為投影，並在 round start/close 各跑一次一致性 gate（不一致即 `ERR_SCOREBOARD_DIVERGENCE`，不得 close） | ①⑤：沒有單一真相就沒有 ALL PASS 可言 |
| **V2** | **WP-10 以重綁收案，不重跑**：把 B1 `GATES.json` ＋ checker 收據綁進 `ACC-WP-FHS-10`，Reader 讀回後改 PASS | ①④⑥：證據已存在，重跑是浪費與新風險 |
| **V3** | **6 個 `HOST_OP` 走同一條量產鏈**：`writeset 推導 → issue_grant(HOST_INSTALL) → install → fresh-load → 獨立 VERIFY(delta=0)`；先 WP-11（最完整、已有 pkg-src/build），再 17（換 issue_grant 憑證）、20、12、13 | ②③：一次建立可重複的閉環，而不是六次特例 |
| **V4** | **車道預設改 `identity_source=codex-rollout`**，並把「無 usage 列」改成具名 fail-closed 錯誤；prompt 模板強制回 nonce | ②③⑥：把「耗盡」這種不可診斷的錯誤換成可診斷的錯誤 |
| **V5** | **VERIFY 維持 mimo**（rev 39），不為模型偏好改治理；若 owner 要 `gpt-6.1-sol`，走 rev 40 並在收據寫明 transport 代價 | ①⑤：治理變更要有紀錄，不能靠 operator 選臂繞過 |
| **V6** | **交付層修復三件事**：長路徑解壓（398 列）、目錄與 manifest 同名（17 列）、補 `PACKAGE_READBACK.json`（1 列）；修完重驗 909/909 | ①④：讓每個收件人五分鐘內得到 909/909，而不是 415 列假故障 |
| **V7** | **血緣一次講清楚**：r18→main 做具名 graft merge（D-1），之後禁止再出現第二條根 | ①⑤：不合，最新工作永遠不在 main |
| **V8** | **`ir1_policy_gate` 前移到 round start 為阻擋條件**（P16 建議），並把 `config/` 的 4 檔納入必要 commit 清單 | ⑤⑥：政策髒工作區是 RC-6，會讓所有收據不可重現 |
| **V9** | **queue 必須有 remote**（D-10）；`/c/wg/queue` 的 81 MB 是 22 包唯一的執行證據 | ③：無人值守的前提是證據不會隨磁碟消失 |

---

## 10. 完整可執行方案（Phase 0–5）

> 每個 Phase 都有「退出條件」與「claim ceiling」。任何 Phase 不得越級宣告。

### Phase 0｜一致性與可重現（0.5 h，PLAN lane）
```bash
# 0.1 副本修復並重驗
7z x -spe FHS-MSC_BODY_2026-10-30_HANDOFF-PATCH-v1.zip -o"<dest>"
python tools/verify_package.py "<dest>"          # 期望 909/909/0
# 0.2 記分板一致性 gate（V1）
python -m hg_kseos project status FHS-MSC-PIPD-LS-PKG   # 與 work_queue 對比
# 0.3 政策乾淨 gate（V8）
python fhs_msc_handoff_20261030/tools/ir1_policy_gate.py --repo C:/Projects/Agent_Workspace/HG-KSEOS
```
**退出**：909/909、記分板一致、`ir1` 非 `POLICY_DIRTY`。

### Phase 1｜把「已完成但沒綁」的收掉（1 h，PLAN + EXECUTE）
1. WP-10 重綁（V2）：`ACC-WP-FHS-10` ← B1 `GATES.json` + `checker_receipt_codex_r7.json`（SHA `97496bbb…`）。
2. 補 `PACKAGE_READBACK.json`、manifest 目錄對齊（V6）。
3. 修正 WP-15 closure 宣告（D-15）。
**退出**：`work_queue` 出現 17 PASS；交付根 909/909 + 3 份封存行可驗。

### Phase 2｜HOST_OP 量產鏈（單包 20–40 min，EXECUTE，無人值守）
以 WP-11 為樣板：
```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS
# 1) writeset 由 pkg-src/ + build/ 推導（issue_grant 要 JSON 檔，不吃 glob）
python tools/derive_writeset.py --wp WP-FHS-11 --out var/permits/WP-FHS-11.writeset.json
# 2) 發 permit（R21 已授 HOST_INSTALL）
python scripts/issue_grant.py issue --principal HERMES-R21-EXECUTE-LANE \
  --operation HOST_INSTALL --writeset var/permits/WP-FHS-11.writeset.json \
  --ttl 60 --epoch 39 --scope WP-FHS-11 --nonce R21-WP11-PERMIT-01 \
  --subject FHS-MSC/WP-FHS-11 --out var/permits/WP-FHS-11.permit.json
# 3) 安裝 → fresh-load
python tools/install_occupant.py --permit var/permits/WP-FHS-11.permit.json \
  --dest var/R21-NATIVE-EXEC/occupants/WP-FHS-11
# 4) 獨立 VERIFY（read-only，delta 必須 0）
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY \
  --prompt-file C:/wg/verify/WP-FHS-11.md --nonce NONCE-WP11-VERIFY-01 \
  --force-rank 1 --require-arm opencode-go/mimo-v2.6-flash \
  --identity-source codex-rollout --sandbox read-only \
  --guard-subject var/R21-NATIVE-EXEC/occupants/WP-FHS-11 \
  --json-out var/receipts/WP-FHS-11.verify.json
```
依序 WP-11 → 17（改用 `issue_grant` 憑證）→ 20 → 12 → 13。
**退出**：每包 `permit.json` ＋ `install receipt` ＋ `fresh-load` ＋ `VERIFY delta=0` 四件齊，`work_queue` 22 PASS。

### Phase 3｜Native admission 閉環（1 個 owner 窗口，load-once）
```bash
# 一次解鎖簽完整批（TTL 3600 硬限制，不要放寬）
powershell -File scripts/native-trust-maintenance.ps1 -Batch var/wave/native-batch.json
python wave2/run_corpus_native.py --journal var/wave/journal.jsonl   # 可斷點續跑
python gates.py                                                      # G-A/GWO/G-B 合取
```
**退出**：`native_admission` 事件 ＋ lease ＋ nonce 逐案落帳，`case_fail 0`，`gates_conjunction PASS`。

### Phase 4｜獨立驗收與發佈邊界（VERIFY lane）
```bash
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY \
  --brief C:/wg/brief_verify.md --nonce NONCE-FINAL-VERIFY-01 \
  --force-rank 1 --require-arm opencode-go/mimo-v2.6-flash \
  --identity-source codex-rollout --sandbox read-only \
  --guard-subject C:/wg/pkg --require-durable-gates \
  --json-out var/receipts/FINAL_VERIFY.json
```
**退出**：`VERDICT.json` 零 FAIL 零 INCONCLUSIVE；`RELEASE` 仍為 `NOT_RUN`（發佈是另一個 owner 決策）。

### Phase 5｜收尾與移交（無人值守的最後一段）
1. 四 repo commit + push；r18→main graft merge（D-1）；12 支 clean PR 分批併（D-2）。
2. queue push 到 remote（D-10）。
3. 產出 `EVIDENCE_INDEX.md`（問題 → 檔案#line → 重現指令）＋ `MANIFEST.json`（逐檔 bytes+sha256）。
4. 寫 `HANDOFF.md`：現況、證據、下一個 session 的開場指令。

---

## 11. 簽章與授權建議

| 需要什麼 | 現在有沒有 | 建議 |
|---|---|---|
| 7 包 `HOST_INSTALL` 授權 | **有**（`R21-CANON-c0542636`，至 2026-11-14，`RELEASE` 仍 deny） | 直接用；到期前完成 Phase 2 |
| WP-17 的 native occupant 授權 | 部分（owner ruling 指向 `issue_grant.py`，`key_id 135455ca00280c39`） | Phase 2 時逐包發 permit，不要用 R21 冒充 |
| 車道 assignment 變更（若採 gpt-6.1-sol VERIFY） | 無（rev 39 只列 mimo） | 發 **revision 40**，同時更新 `lane-routing-registry.yaml` 與 `model-lane-assignment.json`，跑 `lane_policy_reconcile.py` |
| SourceFreeze 正式凍結 | 無（9/9 HOLD） | 1 次解鎖 1 個簽章、0 位元組變更 |
| 合併簽章／repo 端收據 | 無 | graft merge 的 merge commit message 即收據；另附 `PROMOTION_RECEIPT` 級紀錄 |
| 本報告 | — | **不需簽章**：FAR 產出是 candidate，不是 acceptance |

**不要做的事**（每條都有理由）：
1. 不要為了讓 WP-10 變綠而重跑 native——證據已在，重跑只增加新變異。
2. 不要用 `--force-rank` 繞過 assignment 去取得「看起來獨立」的 VERIFY 收據；那會讓 `required==served` 失效。
3. 不要把 415 列缺失寫成「封包損壞」——那是 MAX_PATH 與改名。
4. 不要放寬 reference TTL 換長跑（`native-trust-maintenance.ps1:151` 硬限制 3600）。
5. 不要把 `HANDOFF.md` 的「defensible 22/22」當 PASS；`defensible ≠ passing`。
6. 不要在血緣未決前合併 #5 或 r18——會製造第二條主幹。

---

## 12. Claim ceiling 與非宣稱

```
本報告 = MEASURED_RESEARCH_AND_ENGINEERING_VERDICT（candidate）
封包完整性 = 909/909（本輪實測，C:\wg\pkg）
22 WP = 16 PASS / 3 FAIL / 3 NOT_RUN（控制平面，2026-10-31T11:17Z）
車道可服務性 = PLAN/EXECUTE/VERIFY 皆實測通過（收據見 evidence/）
NATIVE_ADMITTED / NATIVE_VERIFIED / RELEASE = NOT_RUN
本輪未修改任何 WP 狀態、未簽任何 permit、未合併任何 PR
PRODUCTION / LIVE / REMOTE = NOT_CLAIMED
```

**非宣稱**：本報告不宣稱 22 包已 ALL PASS；不宣稱獨立驗收已完成（只宣稱車道可服務）；不宣稱 7649 量詞子項已補；不宣稱 native admission 已跑；不宣稱任何分支已合併。

---

## 13. 殘餘風險

| 風險 | 影響 | 緩解 |
|---|---|---|
| r18 血緣未決 | 2026-10-31 全部工作不在 main；一次磁碟故障即失去 | D-1 ＋ `var/` 關鍵收據鏡射到 `ops/`（已部分完成） |
| queue 無 remote | 22 包唯一執行證據只在一顆磁碟 | D-10 ＋ bundle `a3f2c03bf413…` |
| `relay-usage` 仍為部分腳本預設 | 任何人跑舊命令都會得到「所有路由耗盡」 | V4（改預設 ＋ 具名錯誤） |
| 5 分鐘排程與第二 Hermes 實例 | 共用失效域，會污染 lane 身分 | D-11 |
| 228 MB subject 無備份 | 語義權威來源遺失 | 交由 owner 決定是否入版控或冷備 |

---

## 14. 下一個 session 的開場指令

```
接續 FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1 的 ALL-PASS 推進。
先讀 Fabric/fabric-autonomous-research/runs/FAR-20261031-031-FHS-MSC-ALL-PASS/ResearchSynthesis.md
（§3 清單、§6 D-1..D-15、§10 Phase 0–5）。
起手三件事，依序：
(1) Phase 0：長路徑解壓重驗 909/909 ＋ 記分板一致性 gate（work_queue 為唯一權威）；
(2) Phase 1：WP-10 以 B1 GATES.json + checker_receipt_codex_r7.json（97496bbb…）重綁；
(3) Phase 2：WP-FHS-11 writeset → issue_grant(HOST_INSTALL, R21-CANON-c0542636) → install →
    fresh-load → VERIFY（mimo-v2.6-flash，--identity-source codex-rollout，guard-subject，delta=0）。
車道一律加 --identity-source codex-rollout；VERIFY 用 --require-arm opencode-go/mimo-v2.6-flash。
owner 待決：D-1（r18→main 血緣）、D-3（VERIFY 臂是否改 gpt-6.1-sol）、D-10（queue remote）。
```

---

## 附錄 A — 本輪新增的可重現指令

```bash
# 封包完整性（本輪實測 909/909）
python - <<'PY'
import json,os,hashlib
pkg=r"C:\wg\pkg"; man=json.load(open(os.path.join(pkg,"SHA256_PAYLOAD_MANIFEST.json"),encoding="utf-8"))
ok=miss=bad=0
for e in man["files"]:
    p=os.path.join(pkg,e["path"].replace("/",os.sep))
    if not os.path.isfile(p): miss+=1; continue
    h=hashlib.sha256(open(p,"rb").read()).hexdigest(); ok+=h==e["sha256"]; bad+=h!=e["sha256"]
print(len(man["files"]),ok,miss,bad)
PY

# 車道三連測（本輪實測全部 ok）
python scripts/hgk-lane-dispatch.py --lane EXECUTE --prompt "Reply with exactly: NONCE-X" --nonce NONCE-X \
  --identity-source codex-rollout --sandbox read-only --json-out /tmp/x.json
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY --prompt "Reply with exactly: NONCE-Y" --nonce NONCE-Y \
  --force-rank 1 --require-arm opencode-go/mimo-v2.6-flash --identity-source codex-rollout \
  --sandbox read-only --json-out /tmp/y.json
python scripts/hgk-lane-dispatch.py --lane PLAN --prompt "Reply with exactly: NONCE-Z" --nonce NONCE-Z \
  --force-rank 1 --require-arm openai-codex/gpt-6.1-sol --codex-home C:/Users/user/.codex \
  --allow-human-home-transport --identity-source codex-rollout --sandbox read-only --json-out /tmp/z.json

# 合併判定
git merge-tree --write-tree --name-only origin/main <branch>
git merge-base origin/main <branch>     # NONE 即 unrelated histories
```

## 附錄 B — 證據檔對照

| 檔案 | 內容 |
|---|---|
| `evidence/package_integrity.json` | 909/909 重算結果 |
| `evidence/instance_loss_measurement.json` | 副本 415 列缺失（398 長路徑 / 17 改名） |
| `evidence/wp_scoreboard_control_plane.json` | 22 列 `work_queue` 快照 |
| `evidence/lane_*.json`、`evidence/lane_*.ndjson` | 5 次派送 + 1 次 preflight 的原始收據與 attempt 記錄 |
| `evidence/lane_policy_state.json` | epoch 39 / rev 39 / 三車道綁定 |
| `evidence/github_pr_state.json` | 16 支 open PR 的 mergeable 狀態 |
| `evidence/merge_matrix.json` | merge-tree 與 merge-base 判定 |
