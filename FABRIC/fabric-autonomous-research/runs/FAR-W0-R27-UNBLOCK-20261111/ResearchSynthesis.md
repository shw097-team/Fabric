# FAR 研究合成：W0 殘餘項目的阻斷判定與解鎖方案

run_id `FAR-W0-R27-UNBLOCK-20261111`｜subject `FHS PIPD-LS-PKG W0`｜R6 synthesis
裁決等級：`ADVISORY_RESEARCH_PASS_CANDIDATE`（研究建議，不是驗收，不是簽章，不改任何 HGK 資料列）

---

## 0. 一句話結論

九個「未完成」項目裡，**只有 3 個是真阻斷**（B5 控制平面不一致、B6 測試未遷移、B7 只有 strict 生效），
**1 個是我把報告當成設計原意而誤判的**（B4 全 profile），**1 個機制早就在、缺的只是採用**（B2），
**1 個的能力已經開在你桌上**（B3 簽署視窗 OPEN），其餘 3 個（B1 分支未合併、B8 歷史票、B9 checker 環境）各有明確的關閉動作。
**沒有任何一項需要新權威、第二個 router、或改寫已簽 bytes。**

---

## 1. 逐項判定（GQ-1 / GQ-2）

| 項目 | 判定 | 關鍵證據 | 為什麼不是「真阻斷」 |
|---|---|---|---|
| **B1** epoch-41 不在 main | `REAL_STATE`（狀態，不是阻斷） | `pulls/16` → `mergeable=true`、`draft=true`、`check-runs=[]`；H0 `merge-base` exit 1、roots `a2389c13` vs `ec58a0be` | 分支存在且可合；缺的是「把一個被移植作廢的測試遷移掉」＋你的合併決定 |
| **B2** 跨 Session 硬入口 | `ALREADY_BUILT` + `ADOPTION_GAP` | guard 在 `hgk-lane-dispatch.py` spawn 前攔截：`FHS_ENTRY_ASSERT_REQUIRED` exit 20、`attempts=[]`（0 spawn） | 機制已存在且預設開啟；122 個測試失敗就是它在工作。缺的是其他宿主採用同一 ABI |
| **B3** NATIVE_SIGNED / PASS_CHALLENGE / RELEASE | `REAL_HOLD`，但**專用簽章機制存在**（見 §6 更正） | `owner_window.py` `ALLOWED_KINDS={merkle_root,row,owner_semantic_accept,original_reader_ack}`；`FORBIDDEN_KINDS={release,sourcefreeze,policy_authority,trust_anchor,owner_enrollment,…}` | 我原先寫「需要 owner」是對的，但**沒寫清楚哪一半現在就能簽**。能簽的是語意接受與 reader ACK；不能簽的是 release/policy authority——那是**設計上就沒有工具**，不是沒排程 |
| **B4** full 22-gate 跑不了 | `MISREAD`（層級錯）+ `REAL`（對象錯） | ① `out/GATE_R26.json`：`profile=full, checks=22, pass=21, blocking=0, G16b OPEN`——**這台機器跑過**。② 我拿修好的 gate 對**已封存的 round tree** 重跑：`VERDICT FAIL pass=16/22`，4 個 blocking 全是可達性（`G13 UNQUALIFIED_NO_SOURCES`：31 冊不可達；`G19 ROOT_ABSENT`：25 個 root 有 24 個已消失） | 真正的句子應該是「**修好的 gate 從未對修好的 payload 跑過 full**」。而 full 需要的 31 冊與 25 個 root 已在 2026-11-10 的 workspace 清理中處置掉了（bounded find 0 hits） |
| **B5** 5 個槽被拒 | `REAL_DEFECT`（控制平面） | `ERR_ARM_NOT_IN_ASSIGNMENT`：assignment 解析 PLAN 為 `primary-only`（`fallbacks_declared=false`），而 pool 與 `lane_chains` 投影都列 6 個 PLAN 臂 | 這不是模型不可用，是 **assignment 與 pool 兩個物件不一致**；dispatcher 的 `lane_assigned_arms()` 已支援 `fallbacks`/`non_default_alternates`，所以是「對齊既有能力」而非新增能力 |
| **B6** 122 測試 fail-closed | `SOLVABLE_BY_ALTERNATIVE`（不需第二個 issuer，見 §6） | 122 failed / 127 passed，**所有失敗同一個碼** `FHS_ENTRY_ASSERT_REQUIRED` | 它們派送未綁定行程——正是 finding 要求拒絕的行為。可透過受制裁 reader 在 tmp run_id 造 binding 來遷移 |
| **B7** session/process 只在 strict | `REAL_PARTIAL` | 4/4 真票都沒有 `session_id`/`process_id`；硬性要求會拒掉回合自己已簽的票 | 契約條文與已簽事實衝突。解法是**生效時點**（r28 起），不是回頭改票 |
| **B8** 126 張 legacy 票無 candidate binding | `REAL_BLOCK`（不是純 by-design；見 §6） | `verify_quorum.py`：`source = votes_r25 or votes`；收據不可改寫 | 那是歷史紀錄，不是待修缺陷。若也要綁，只能重簽——那是改寫已簽 artefact |
| **B9** checker 起不了 Python / dubious ownership | `ENV_DEFECT` | `spawn ...Python311\python.exe ENOENT`；`fatal: detected dubious ownership`；同一 lane 用 node 驗到 7/7 簽章 | lane 的**可達範圍**被環境限制，不是它的獨立性有問題。給 shim 或改用 node-only brief 即可 |

### 1.1 有沒有「其實已經有實作，而你沒找到」？

有，三處，且都是這次才挖出來的：

1. **全 profile 跑得動**——證據是我自己過去輪的 `GATE_R26.json`（22 checks / 21 pass），不是推論。
2. **簽署儀式存在且現在開著**——`~/.hgk-owner/window.json` `state=OPEN`、`task=R27-POSTREPAIR`、`max_ops=40`、`ops_used` 從 0 起算、`effect_class_ceiling=REPOSITORY_WRITE`。我上一輪把它寫成「需要你按」，但沒說**視窗現在就能簽 r27 的語意接受**。
3. **dispatcher 本來就吃得下 fallback**（`lane_assigned_arms()` 讀 `assignment[]`，且有 `fallbacks` 欄位），所以 B5 不是缺功能，是資料沒填。
4. **issuer grant 可以做機械入口的補強**——`issue_grant.py` 產的是綁 principal／operation／writeset 的 Ed25519 grant，非密碼簽章不可自證。若把 `binding_id` 加成 grant payload 的必填欄，**沒有綁定就拿不到 permit**——這比「叫每個 Session 記得先跑 CLI」硬得多，而且不需要新 router。

### 1.2 有沒有「過度解讀藍圖」？

有一處，就是 B4。round 自己的 `EVIDENCE_SCOPE.json` 早就把 **payload profile（CI 跑的那個）** 與 **full profile（作者 round 跑的那個）** 分開，
r25 交接也明寫「CI 只跑 payload profile」。我把外審的一句話（「原 31 冊 full Gate 未重跑」）當成 W0 的結案條件，
這比設計原意嚴。**設計原意要求的是「證據分層誠實」，不是「31 冊必須在本機」。**

### 1.3 有沒有「替代方案可行」？

| 替代 | 能不能解 | 界線 |
|---|---|---|
| 獨立車道 | 解 B9 的**一部分**（換一個可執行的 checker 環境），不解 B4 | 車道證明的是路由與拒絕，不是 31 份文件存在 |
| 本地 Docker 沙盒 | **尚未實測**（列 `OQ-04`） | 容器看不到 `C:/` 路徑除非掛載；而該 lane 已能透過 node 讀到工件 |
| owner 口令信封 | **能**：`owner_semantic_accept` / `original_reader_ack`；**不能**：release / policy authority（`FORBIDDEN_KINDS`） | 能力 ≠ 權限；視窗的 `claim_ceiling` 自己就這樣寫 |
| issuer grant 綁 writeset | **能**，作為 B2 的機械補強 | 需要 owner 指令把 `binding_id` 列為 grant 必填 |

---

## 2. 完整可執行的解鎖方案（GQ-1 的「怎麼全部實際完成」）

順序即依賴順序；每一步都標「誰做、命令、成功判準、回滾」。

**U1（現在，owner 授權即可）修 assignment 不一致 → 解 B5**
- 誰：HGK owner 下指令，maker 執行。
- 做什麼：在 `config/model-lane-assignment.json` 的 PLAN／EXECUTE／VERIFY 三條 chain 宣告 fallback（值取 epoch-41 pool 已列的臂），用 repo 自己的 `scripts/lane_policy_reconcile.py` 重生成投影，不手改。
- 成功判準：`fhs_3lm.py --menu` 九格 admitted **且** dispatcher 對 5 個先前被拒的槽不再回 `ERR_ARM_NOT_IN_ASSIGNMENT`（實際 probe 一次）。
- 回滾：`git revert` 該 commit；binding 全部 epoch-scoped，registry sha 一動就 `EPOCH_DRIFT`，不會殘留錯誤綁定。

**U2（現在）讓 SBL #66 變綠 → 解「候選不可合併」**
- 已做：三個 `.sh` 改成 `.sh.txt`（commit `6243062`），因為 `tests/test_reproducible_build.py` 的不變量是「repo 不運 Windows-only 腳本」。
- 還要做：等 CI 重跑；若 `test (windows/ubuntu)` 仍紅，逐條讀 job log 再修（不得改測試）。
- 成功判準：五個 check 全綠。
- 回滾：branch 可丟，main 未動。

**U3（現在）合併 Fabric #54 → 解「mirror 未准入」**
- `mergeable_state=clean`、`fhs-nav-static=success`、additive 25 insertions 0 deletions。
- 建議：**先合這個**，因為它是純加法、可回滾、且不受其他 PR 影響。

**U4（需要一次 owner 簽章）r27 語意接受**
- 視窗已 OPEN；把最終 r27 文件（689,974 B / `9f2af277…`）與收據集凍結後，用 `owner_window.py` 的 `owner_semantic_accept` 簽一次。
- 這會把 `FINDING_R26-06_TZ_UNQUALIFIED` 一併解決（新簽章帶 `+08:00` 偏移）。
- 不簽就不能宣稱 `FHS_ORIGINAL_ACK`；這不是我可以代簽的。

**U5（需要治理裁決）122 測試遷移 → 解 B6**
- 做法：測試 fixture 呼叫受制裁 reader `fhs_3lm.py --bind`（tmp run_id），再 mint 一次性 capability；不得在測試裡自造 issuer。
- 對 synthetic arm：需要裁決新增一個**記錄用、不可派送**的 `SYNTHETIC_ARM` binding 類別（`OQ-03`）。沒有這個裁決，那幾條測試只能維持 fail-closed 並標 `EXPECTED_REFUSAL`。

**U6（需要 owner 裁決）B7 生效時點**
- 建議：`session_id`/`process_id` 自 **r28 起**為硬性；r26/r27 已簽票記為 `LEGACY_VOTE_NO_PROCESS_IDENTITY`，不重簽。

**U7（設計裁決，可選）W0 的驗收 profile**
- 建議裁決句：「W0 的結案證據 = `payload profile` 的 `gate_r20.py` 全綠 + 一次 `full profile` 歷史紀錄（`GATE_R26.json` 21/22，`G16b REPORTING OPEN`）＋本輪 G24 反證。」這樣 B4 就不再是阻斷，而是一個**已被記錄的範圍聲明**。
- 若不接受，替代是重建 31 冊與 25 個 root——本機已無，需從原始來源重取，成本高於 W0 的價值。

**U8（時間序最後）HGK #16 undraft + 合併**
- 前置：U1（assignment 一致）、`PoolSelectionTests.MANDATE` 遷移（epoch-33 硬編碼 → 由 registry 讀）、3 個殘餘 fatal drift 由 owner 決定是否同批。
- 建議合併順序：**Fabric #54 → SBL #66 → HGK #16**；前三者可獨立回滾，HGK 最後且單獨 PR。

---

## 3. 決策與授權（GQ-4 / GQ-5）

| ID | 決策 | 種類 | 可用的授權工具 | 今天能不能做 |
|---|---|---|---|---|
| `OD-1` | 修 assignment fallback（U1） | `DECIDE_OWNER` | owner 書面指令 + repo PR | **能**（指令即可） |
| `OD-2` | 合併 Fabric #54 | `AUTHORISE` | 你的 preauth（推 branch+PR）→ 合併仍需你點 | **能**（按 merge） |
| `OD-3` | 合併 SBL #66（CI 綠後） | `AUTHORISE` | 同上 | **能**（等 CI） |
| `OD-4` | 簽 r27 語意接受（U4） | `SIGN` | **owner 簽署視窗（已 OPEN）** | **能**（需你在視窗按一次） |
| `OD-5` | 122 測試遷移政策、synthetic arm 類別（U5） | `DECIDE_OWNER` | 治理裁決 + 受制裁 issuer 實作 | 需裁決 |
| `OD-6` | r28 起 session/process 硬性（U6） | `DECIDE_OWNER` | 契約修訂 | 需裁決 |
| `OD-7` | W0 驗收 profile = payload（U7） | `DECIDE_OWNER` | 裁決句 + 報告附註 | 需裁決 |
| `OD-8` | 合併 HGK #16 | `AUTHORISE` | 需先 OD-1 與 test 遷移 | **不能**（前置未完） |
| `OD-9` | `NATIVE_SIGNED` / `PASS_CHALLENGE` / `RELEASE` | `DECIDE_OWNER` | **無工具**（`FORBIDDEN_KINDS`）；要給就得先做治理修訂 | **不能**（設計如此） |

### 3.1 升格／合併建議（高信心）

- **可合併**：Fabric #54（clean、additive、有負例）。
- **立即可合併（條件式）**：SBL #66 —— 條件是 CI 五項全綠；這是我造成的紅燈，已修。
- **不可合併**：HGK #16（draft、0 checks、3 fatal、1 個被移植作廢的測試）。
- **可升格實用**：`fhs_entry_guard.py` 的守衛（已在本 repo 生效，且在真實 fresh process 上 0 spawn 拒絕）、`verify_public_bundle.py`（7/7 真驗）、r27 append-only 文件（prefix 逐位元相同）。
- **不可升格**：任何以 pool 命中代替 ActualServed 的宣稱；任何以 GitHub 綠燈代替 Host 生效的宣稱。

---

## 4. 最高信心建議（給 owner 的裁決句）

1. **今天的三個動作**：合 #54；等 #66 CI 綠後合；在已開的視窗簽一次 r27 `owner_semantic_accept`。
2. **這週的一個指令**：修 assignment fallback（U1），讓 9 個槽真的可派送——這是唯一一個「宣稱與事實不符」的技術缺陷。
3. **一週後的治理決定**：122 測試遷移 + synthetic arm 類別；沒有它，#16 永遠只能在 draft。
4. **不要做的三件事**：不要合 #16 來「讓 main 前進」；不要為 B7 重簽歷史票；不要把 release 塞進 owner 視窗（那是改治理，不是用工具）。

---

## 5. 不確定性與反證條件

- `OQ-01`（W0 驗收 profile）若你裁定「必須 full」，則本方案的 U7 失效，B4 變真阻斷，需先重建 31 冊。
- `OQ-03` 若裁定「測試不得 mint binding」，則 B6 只能以 `EXPECTED_REFUSAL` 收尾，#16 永久 draft。
- 我**沒有**實測 Docker 沙盒路徑（`OQ-04`），所以「容器可解 B9」是**未驗證的替代**，不是結論。
- 本輪 PLAN 車道的獨立判讀若與上表衝突，以車道收據為準並在 handoff 記錄分歧（見 `ResearchHandoff.yaml`）。

---

## 6. PLAN 車道的獨立判讀，以及它對我的三處更正

PLAN 車道（`openai-codex/gpt-6.1-sol`，read-only，收據 ok=true）對同一份紀錄做了獨立判讀，全文在 `PLAN_LANE_VERDICT.md`。
它同意 B1/B2/B4/B5/B9 的性質，但**在三處推翻或修正了我的合成**，以下是更正後立場：

| # | 我原本寫 | PLAN 的證據 | 更正 |
|---|---|---|---|
| M-1 | B3「release 在 `FORBIDDEN_KINDS`，設計上沒有工具」 | `owner_window.py` 另有 `DEDICATED_KINDS = {"sourcefreeze","release"}`，且有限制（需 `--allow-dedicated <kind>`、TTL ≤ 1h、max_ops ≤ 4） | **我漏讀了 dedicated 分支。** 正確說法：release 有**受嚴格限界的專用視窗機制**，但它只證明「能產生簽章」，**不證明 Publisher admission**。B3 仍是 HOLD，但理由要改成「缺原 consumer/Publisher 的受理」，不是「沒有工具」 |
| M-2 | B4「修好的 gate 從未對修好的 payload 跑過 full」 | `gate_r20.py` 的 `--profile` choices 是 `round,payload`；`full` 屬於 `--scope`。正確呼叫是 `--profile round --scope full --sources <corpus>` | **我的 B4 實驗用預設 `--round .` 才跑得動；`--profile full` 根本不是合法值。** 我先前那句「full 跑不了」是把**語法錯誤**當成能力缺失。更正：能跑，缺的是 corpus 與 root 可達性 |
| M-3 | B6「需要治理裁決 synthetic arm 的 binding 誰能簽」 | guard 檢查 binding/capability，**不要求 issuer 對 binding 簽章**；因此測試 fixture 可經受制裁 reader 造 binding，不必造第二個 issuer | **我把它說得比實際更死。** B6 降級為 `SOLVABLE_BY_ALTERNATIVE`：先做一個 admitted 的 fixture pilot，再遷移 |
| M-4 | B8「by design，歷史紀錄不可改寫」 | 126 是 **properties** 而非 126 張票；L0:298 要求 same Subject/Candidate/Scope 綁定是**實質要求** | **降級不成立。** B8 應記 `REAL_BLOCK`，解法是「版本化的等價規則 + 原 Reader 核准」或重新取得 provenance，不是無條件 grandfathering |

**仍存在的分歧**：PLAN 把 B1/B2/B5/B7 都判 `REAL_BLOCK`，我判「狀態／缺採用／控制平面缺陷／部分」。
差異在**語彙**而非事實：它用「阻斷某個特定宣稱」，我用「阻斷 W0 結案」。兩者在 handoff 都保留，交由 owner 選定 W0 的結案定義（`OQ-01`）。

### 6.1 對「最高信心建議」的修訂

原 §4 的第 4 點「不要把 release 塞進 owner 視窗」需要修正為：
**不要把 release 當成一般視窗可以順手簽的東西**——它需要 `--allow-dedicated release` 的專用視窗（TTL ≤ 1h、max_ops ≤ 4），
而且即使簽了，仍缺 Publisher/原 consumer 的受理。兩件事不要混為一談。

---

## 7. 更正（owner 指出的兩個資料夾）：31 份文件**在**，B4 的「corpus 不可達」是錯的

owner 指出兩個資料夾後，我用 `SOURCE_LOCK_V3.json` 的 **declared sha256** 逐一比對，不是靠檔名：

```
declared sources: 31
MATCHED: 31   MISSING: 0
totals: declared_lines_sum 111331 / observed_bytes_sum 22281767 / sha256 match 31
```

兩個資料夾合起來剛好是那 31 份（`SBL_PIPD-LS-PKG_DOC-00..13` + `01_FHS-MSC_PIPD-LS-PKG_BODY` 的 17 份）。
我先前寫「corpus 已處置、bounded find 0 hits」——**我找的是 round 目錄名，不是 declared digest**。這是搜尋方法的錯，不是資料的錯。

### 7.1 可執行的修復與其結果

把 31 份以 declared 檔名複製成一個 corpus 目錄（逐一 assert sha256 相等），再跑正確呼叫：

| 呼叫 | 結果 |
|---|---|
| `gate_r20.py --round .`（我先前那次） | `VERDICT FAIL pass=16/22 blocking=4`（G13 31 冊不可達、G19 roots 消失、G16a/b、G24 缺） |
| `--profile round --scope full --sources <BODY>`（PLAN 指出的正確參數） | `pass=15/22 blocking=5`（G11 `ABSENT:SBL_PIPD-LS-PKG_DOC-00(1).md`：檔名帶 `(1)` 的 round 佈局） |
| `--profile round --scope full --sources ./corpus`（31 份按 declared 檔名 staged） | **`pass=17/22 blocking=3`：G11 LINE_CONVENTION 與 G13 COUNT_SCOPE 雙雙轉綠** |

**因此 B4 的判定改為 `ALREADY_AVAILABLE`（可達性 31/31 已驗），剩下的 3 個 blocking 全是路徑搬遷，不是語義：**

| 殘餘 | 原因 | 修法 |
|---|---|---|
| `G16a`/`G16b` `ARTIFACT_ABSENT` | 找 `C:/Projects/Agent_Workspace/HG-KSEOS/pyproject.toml`，該 repo 已搬到 `C:/Projects/Agent_Workspace/FHS/HG-KSEOS` | 一個 junction/symlink，或 gate 的 root 設定改指新路徑 |
| `G19` `ROOT_ABSENT` 24/25 | copy-register 宣告的 25 個 root 在 2026-11-10 清理中被處置 | 由 owner 決定：重建 roots、或以「歷史 root 已處置」為由降級為 REPORTING |
| `G24` `ARTIFACT_ABSENT` | 找 `evidence/FHS_ORIGINAL_ACK.json`，本 round 佈局在 `out/` | staging 時把 `out/FHS_ORIGINAL_ACK.json` 對映到 `evidence/`（`stage_r26.py` 這類工具本來就做這件事） |

### 7.2 對「最高信心建議」的第二次修訂

原本我說「B4 若你裁定要 full，就得重建 31 冊，成本高於 W0 價值」。**這句話作廢**：
31 冊已在知識庫，複製＋改名＋一個 `--sources` 就是**幾分鐘的事**，而且已經跑出 17/22。
剩下的只有三個路徑搬遷與一個 owner 對 G19 的裁決。
