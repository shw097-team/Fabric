# FAR-041｜三個「做不到」，一個被我讀錯、一個被我查錯、一個其實只是沒去量

日期：2026-11-01（台北）
路由：Fabric 治理契約 → SBL 產品工程指揮入口 → HG-KSEOS 授權／狀態／驗收控制平面
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`

---

## 0. 一頁結論

| 單元 | 我先前的說法 | 本輪查證 | 裁示 |
|---|---|---|---|
| **WP-20** | 需要 owner 裁決四 Host（ChatGPT vs DeepSeek Harness），D-A 曾把分母砍到 144 | **交付文件自己已經裁了。** 09B 的 48 筆 `PROPOSAL-CHATGPT-*` 每一筆都寫「源身份 `CELL-…` / `DeepSeek Harness`（保留，不改名）；本 ID **尚非 Original 192 Cell**」，退出條件 `CR-HOST-192` 下 `MIGRATION_HOLD`。實測：48 筆提案、48 次 `MIGRATION_HOLD`、48 筆源身份全是 DeepSeek Harness | **不需要裁決。** Original 192 = Hermes／Codex／Claude Code／**DeepSeek Harness**；ChatGPT 那 48 筆是**凍結中的遷移提案**，不是第四個 Host，也不是被排除的格。D-A 撤回，分母 192 |
| **WP-12** | `HOST_RUNTIME_FROZEN`：沒有 `site-packages/openai` 可升級、啟動器是凍結的 | **查錯了。** profile venv 裡 `openai 2.24.0` 實際存在，而且 `openai.types.responses.response_computer_tool_call_output_screenshot_param` **可以 import**（我直接跑成功）。失敗發生在 `D:\Hermes-Recovery\h22` 那個行程裡 | **不是「凍結」，是「該行程解析到哪一份 openai」的問題。** 阻斷改判為 `RUNTIME_PATH_UNRESOLVED`，unblock 縮小成「讓 CLI 行程解析到 venv 的 openai，或改用 skill loader 量 Hermes 格」 |
| **WP-11** | 6 格卡在 LITE==STANDARD | 已解：LITE 15 檔 / STANDARD 52 檔，digest 不同；**4 格已實測 PASS** | 剩 3 格 Hermes，卡的是 WP-12 的同一個行程問題，不是新問題 |

**一句話**：三個未完成項裡，有一個是我把「遷移提案」讀成「Host 替換」，有一個是我把「某個行程找不到模組」寫成「發行版凍結」，第三個則已經量完 4/9 格。

---

## 1. WP-20：交付文件已經自己裁決，我只是沒讀到

### 1.1 我原本的誤讀

我把 09A 的「四 Host：Hermes Agent、Codex、Claude Code、ChatGPT」與 R2 的「四 Host 是 Hermes、Codex、Claude Code、DeepSeek Harness」當成**兩個互斥的列舉**，於是開了一個「待 owner 裁決」的洞（D-A2）。

### 1.2 文件實際長什麼樣

`09B_KIND_MODE_HOST_192.md` 第 2709 行標題是「**R2 四 Host 衝突的完整受影遷移候選（48/48，不覆寫原 CellID）**」。每一筆的內文都一樣：

```
源身份：CELL-2738990e2c09 / DeepSeek Harness（保留，不改名）；
        產品要求另為 ChatGPT，本 ID 尚非 Original 192 Cell。
退出：  Original ID untouched；未有核定版本/HostCaps/ProviderToken
        就 CR-HOST-192 下 MIGRATION_HOLD。
```

實測：

```
grep -c "^### PROPOSAL-CHATGPT-"   09B_KIND_MODE_HOST_192.md  → 48
grep -c "MIGRATION_HOLD"           09B_KIND_MODE_HOST_192.md  → 48
源身份 / `DeepSeek Harness` 的提案數                            → 48
```

### 1.3 裁示

- **Original 192 = Hermes／Codex／Claude Code／DeepSeek Harness。** 這 48 格是 **DeepSeek Harness 的格，而且已 admitted**。
- **ChatGPT 不是第四個 Host**，是對這 48 格提出的**遷移提案**，狀態 `MIGRATION_HOLD`，**不得覆寫原 CellID**。
- 因此分母 **192**，`admitted = 192`，`held proposals = 48`（另一條軸，不進分母）。
- **D-A 撤回的原因要改寫**：不是「ChatGPT 48 格 not admitted by spec」，而是「我把 admitted 的 DeepSeek 格當成被排除的格」。這是**過度解讀＋看錯**，不是設計缺口。

**這不是設計筆誤。** 交付文件寫得很清楚，是我的讀法有問題。反向修正要修的是**我的登記器**，不是規格：`wp20_cell_registry.py` 已改為 `ORIGINAL_192` 為預設，並把 48 筆提案放進 `held_proposals` 側欄。

---

## 2. WP-12：我查錯了一個地方，然後把結論寫成「不可修」

### 2.1 我先前的說法

「`D:/Hermes-Recovery` 深度 6 沒有 `site-packages/openai`；`live22/bin/hermes` 是 114,995 bytes 的凍結啟動器；`pip install -U openai` 沒有對象可作用 → 只能重建發行版（超出授權）」。

### 2.2 本輪實測

```
venv\Scripts\python.exe -c "import openai; print(openai.__version__)"
  → 2.24.0   (…\hermes-agent\venv\Lib\site-packages\openai\__init__.py)

venv\Scripts\python.exe -c "import openai.types.responses.response_computer_tool_call_output_screenshot_param"
  → OK        ← 模組在，而且 import 得動
```

**「沒有 openai 可升級」是錯的。** 我看的是 `D:\Hermes-Recovery`（安裝目錄），真正的套件樹在 profile 的 venv 裡。

### 2.3 那為什麼 CLI 還是失敗

失敗發生在 `D:\Hermes-Recovery\h22\agent\agent_init.py:1027` 那個行程：

```
RuntimeError: Failed to initialize OpenAI client:
  No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'
```

同一個模組，在 venv 直譯器裡 import 成功，在 CLI 行程裡找不到 → **問題是「那個行程解析到哪一份 openai」，不是「發行版凍結」**。
我試過 `PYTHONPATH=<venv site-packages> hermes -z …`：`ModuleNotFoundError` 消失，但 gateway 仍然回同一個 `RuntimeError`。**所以不是單純的 sys.path 問題，我還沒隔離出來。**

### 2.4 裁示

- 阻斷碼由 `HOST_RUNTIME_FROZEN` 改為 **`RUNTIME_PATH_UNRESOLVED`**。
- **「重建 Hermes CLI 發行版」這個結論撤回**——它建立在錯誤的前提上，而且代價最高。
- 兩條真正可走的路（依上位裁決順序，對齊交付優先）：
  1. **讓 CLI 行程解析到 venv 的 openai**（bounded、可回滾；先印出該行程的 `sys.path` 與 `openai.__file__` 再改）。
  2. **Hermes 格改用 skill loader 量**，不走 `-z`：Hermes 的載入面是 `profiles/<p>/skills/<n>/SKILL.md`，`skills_list` + `skill_view` 已經量得到 `readiness_status: available`。這是**同一個 Host 契約的另一個入口**，不是降低標準——但必須說清楚：loader 格證明「載入」，`-z` 格才證明「模型經由該載入面回答」。
- **Docker 沙盒不適用**（已測）：daemon 未啟動、WSL 兩個發行版 Stopped、三個 Host 都是 Windows 原生 CLI、容器內 DPAPI 不可用。
- **獨立車道不適用**：這不是車道問題，是本機行程解析問題；換車道不會讓同一個行程找到模組。

---

## 3. WP-11：4 格實測 PASS，剩 3 格是 WP-12 的影子

### 3.1 已量

| 格 | 結果 | digest | 來源分離 |
|---|---|---|---|
| Codex × LITE | **PASS** | `e3e993b0e079` | digest 來自 cwd 裡的 SP；badge 只來自 host loader |
| Codex × STANDARD | **PASS** | `52712b6316fb` | 同上 |
| Claude Code × LITE | **PASS** | `e3e993b0e079` | 同上 |
| Claude Code × STANDARD | **PASS** | `52712b6316fb` | 同上 |

每個格的負例都是：移除 probe 後，badge 消失、digest 仍在 → 證明 badge 只可能來自 Host 載入面。

### 3.2 前兩版是空的（已寫進收據）

1. 第一版問「hidden host instructions 裡的 token」→ 模型**正確拒答**（它不肯洩漏隱藏指令）。
2. 第二版把 token **寫進問題**→ 模型原樣回傳。**這是把答案交給考生的考題。**

第三版才成立：badge 只存在於 Host 載入面，問題只問「這個環境的 SP-BADGE 是什麼」。

### 3.3 兩份 SP 本身的獨立驗證

| SP | 檔數 | digest | 解包 | 成員重驗 | 從解包樹 import |
|---|---|---|---|---|---|
| LITE | 15 | `e3e993b0e079` | OK | 15/15 | `IMPORT_OK` |
| STANDARD | 52 | `52712b6316fb` | OK | 52/52 | `IMPORT_OK` |

---

## 4. 全部「殘留／缺口／阻斷／未關閉」的關閉方式

| 項 | 現況 | 關閉動作 | 誰能做 |
|---|---|---|---|
| **WP-11**（3 格） | 4/9 PASS，3 格 Hermes 不可跑 | 走 WP-12 的 `RUNTIME_PATH_UNRESOLVED` 解 | 我（bounded） |
| **WP-12** | `RUNTIME_PATH_UNRESOLVED` | 印出 CLI 行程的 `sys.path`／`openai.__file__`，再決定是 pin 路徑還是改用 loader 格 | 我（bounded） |
| **WP-20** | 阻斷已解；192 格 `NOT_MEASURED` | 逐格量測（8 Kind × 3 Mode × 4 Host × 2 Provider），先量 Hermes/Codex/Claude，DeepSeek Harness 另案 | 我（長工時） |
| **F-01** `PACKAGE_READBACK.json` 缺席 | 未產 | 從 `/c/wg/pkg` 重算 909/909 並落 readback 收據 | 我 |
| **P5C_LANE_VERIFY_BLOCKED.json** | 歷史收據仍掛著 | 以 `WITHDRAWN_PENDING_REWORK` 標記，不刪檔（verdict 詞彙只有 PASS/FAIL） | 我 |
| **R-1 `halted_repeat`** | 只留在日誌 | 已由 `stall_monitor` 的時間窗＋`round_continuation_gate` 五種具名理由承接；把歷史 halt 記為 `SUPERSEDED_BY_WINDOWED_MONITOR` | 我 |
| **D-D** `candidate/r18` 與 main 無共同祖先 | 264 ahead / 83 behind | **graft merge**（`--allow-unrelated-histories`）並在 commit message 記明是 graft；或維持分支不合 | **需 owner 決定**（改寫 main 的歷史拓撲） |
| **D-E** `lane/epoch-40-identity-source-20261031` | 4 ahead / 0 behind | fast-forward 併入 main | **需 owner 授權**（動 main） |
| **D-B** live HGK/GENIE（S5/S6） | 只到 fixture | 需 live 服務憑證與授權 | **需 owner** |
| **D-H** `PIPD/Fine-grained personal access tokens.txt` 在 repo 內 | 未移出 | 移出並輪替；`export` 已改為只掃出貨成員，但 repo hygiene 仍是真缺陷 | 我（移檔）＋**owner（輪替）** |
| **D-I** 簽章 | **已撤回**（issuer 可用，`GRANT_VALID`） | 關閉 | 已關 |
| **D-A** WP-20 分母 | **已撤回**（誤讀遷移提案） | 關閉，分母 192 | 已關 |
| **視窗風暴** | 迴圈 paused；4 站點已改 `CREATE_NEW_CONSOLE+SW_HIDE` | 儀器（`window_watch`）需修到正控打響，才可重新 arm | 我，但**需你親眼所見的那次當正控** |

---

## 5. 待 owner / issuer 的決策與授權

### 5.1 只有三件真的需要你

| # | 決策 | 選項 | 我的建議 |
|---|---|---|---|
| **O-1** | `candidate/r18` 要不要進 main | (a) graft merge，保留兩段歷史 (b) 不合，維持分支 (c) 重寫成單一線性歷史 | **(a)**。r18 是本次 19 PASS 的載體，不合就等於成果留在分支；graft 是唯一不重寫歷史又能併的手段 |
| **O-2** | `lane/epoch-40-identity-source-20261031` 併入 main | (a) fast-forward (b) 不合 | **(a)**。4 ahead / 0 behind，零衝突 |
| **O-3** | `D-H` 憑證輪替 | (a) 你輪替後我移檔 (b) 我先移檔你再輪替 | **(b)**，先止血 |

### 5.2 不需要你裁決的（本輪已自行裁示並留證）

- **D-A / WP-20 分母**：交付文件已裁，192，48 筆 ChatGPT 提案 `MIGRATION_HOLD` 不進分母。
- **D-I 簽章**：issuer 可用，`GRANT_VALID`。
- **WP-13 驗收**：`GRANTED`，5 條 clause 全 PASS。
- **WP-11 前 4 格**：PASS，收據已進控制平面（`ops/.../WP-FHS-11/cells/`）。

---

## 6. 候選升格與分支併入（已檢測）

### 6.1 可升格為實用（已有實測，不是設計稿）

| 候選 | 證據 | 建議 |
|---|---|---|
| `--profile` 的 artifact depth | LITE 15 / STANDARD 52，digest 不同；13/13 測試 | **升格**：這是 SP 軸第一次真的改變產物 |
| Need/Occupant ABI + Consumer | `abi.py` 7/7；swap 由 consumer 觀察到；acceptance GRANTED | **升格**：HotSwap 從「換檔案」變成「換能力」 |
| `issue_grant.py` Ed25519 發行 | `GRANT_VALID`，綁 owner authorization sha | **升格**：這是 HOST_OP 的授權平面 |
| `round_continuation_gate` 五種具名拒絕 | 10/10 | **升格**：續行從散文變成狀態機 |
| `work_queue_block` 具名阻斷 | 無 unblock 即 exit 2；JSON 由 DB 重生 | **升格** |
| `console_guard_gate` profile 掃描 + 逐呼叫點 AST | 33/33、4/4 | **升格** |
| `stall_monitor` 時間窗 | 13 小時前的 47 次不再被當成現在 | **升格** |
| `wp20_cell_registry` | 192 格、雙讀法、held proposals 側欄 | **升格** |

### 6.2 不建議升格

| 候選 | 理由 |
|---|---|
| `owner_window.py` | 起不來（缺 `owner_vault`），且 issuer 已有替代入口；保留為歷史，不列為工具 |
| `window_probe.py` / `window_probe3.py` | 正控打不響（`PROBE_BLIND`）；在有能打響的儀器前不得作為證據來源 |
| `DETACHED_PROCESS` 路徑 | 是視窗工廠，已列為禁止 |

---

## 7. 建議執行方案（依上位裁決順序）

**A1｜WP-12 隔離（30 分鐘，bounded）**
在 CLI 行程內印出 `sys.path`、`openai.__file__`、`openai.__version__`；對照 venv。若只是路徑順序 → pin；若是兩個 openai → 移除干擾者。**不重建發行版。**

**A2｜WP-11 剩 3 格**
A1 成功 → 跑 Hermes × 3 SP（LITE/STANDARD/ASSURED，ASSURED 預期 `PROFILE_VETO`）。
A1 失敗 → 改用 skill loader 量，並在收據明寫「loader 格，非 `-z` 格」。

**A3｜WP-20 量測（長工時）**
192 格分批：先 Hermes/Codex/Claude Code 各 48 格（有真 loader），DeepSeek Harness 48 格另案（無本地 runner）。每格 `cell_id` + 結果 + 證據路徑；禁止用「一格成功冒稱 12 格」。

**B｜殘留收尾**
F-01 readback、P5C 標記、R-1 標記、D-H 移檔。全部落收據，不靠對話。

**C｜決策落地**
O-1／O-2 依你的裁示執行 merge；O-3 先移檔。

**D｜視窗儀器**
`window_watch` 修到正控打響（用你親眼看到的那次當 fixture）之前，supervisor 保持 paused。

---

## 8. 我這輪做錯的三件事（記錄，不粉飾）

1. **把遷移提案讀成 Host 替換** → 開了一個不存在的 owner 裁決洞，還兩次改分母。
2. **查錯目錄就下「不可修」結論** → 我看 `D:\Hermes-Recovery`，套件其實在 profile venv；代價最高的方案（重建發行版）因此被寫成「唯一解」。
3. **量測兩次是空的** → `MainWindowHandle` 取樣與「把 token 寫進問題」的 cell，都回報了假數字。

三件的共同形狀：**我用一個代理量測（proxy）取代了實物**——代理檔案樹、代理視窗計數、代理題目。修法都一樣：量實物，並讓代理能被證偽（正控）。
