# FAR-042｜剩下的三格：一個是規格缺口，一個是五次嘗試後仍未定位，一個是它的影子

日期：2026-11-01（台北）
交付：`FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`
現況：`work_queue = 19 PASS / 3 FAIL / 0 NOT_RUN`，scoreboard `CONSISTENT`

---

## 0. 三句話

1. **WP-20 的「192 格」是規格缺口，不是工作量。** 八個 Kind 裡只有 `AGENT_SKILL` 在三個 Host 上有可安裝表面；另外 168 格我量不到，不是因為我沒跑，而是因為**交付文件沒有定義每一格「量什麼」**。這是需要反向修正的設計缺口。
2. **WP-12 是五次嘗試後仍未定位的本機路徑問題**，不是我先前說的「發行版凍結」。已排除的假設列在 §2.2，包含 Docker、獨立車道、provider 切換、PYTHONPATH、直接入口、uv 快取。
3. **WP-11 的三格是 WP-12 的影子**，不是獨立缺陷。

---

## 1. WP-20：168 個 `NO_HOST_SURFACE` 是規格缺口（需要反向修正）

### 1.1 我做了什麼

`wp20_cell_runner.py` 逐格量測：在 Host 自己的表面安裝 Kind 形狀的 artefact → 請該 Host 的 loader 服務 → 移除 → 再問。

**實測 18 格全部 PASS：**

```
AGENT_SKILL × LITE/STANDARD/ASSURED × Hermes/Codex/Claude Code × PROVIDER_ON/OFF = 18
每格負例：移除 artefact 後 Host 不再提供 badge（比對完整 badge 值，不是比對形狀）
```

### 1.2 為什麼另外 168 格量不到

| Kind | 可安裝表面 |
|---|---|
| `AGENT_SKILL` | Hermes `skills/`、Codex `~/.codex/skills/`、Claude `~/.claude/agents/` |
| `PLUGIN` | Hermes `plugins/` |
| `PROFILE` | Hermes `profiles/` |
| `CLI_TOOL` `AI_SYSTEM` `GENIE` `SIMPLE_AGENT` `AGENT_OS` | **無** |

**這不是我的能力問題，是矩陣沒有操作定義。** 交付文件給了 8 Kind × 3 Mode × 4 Host × 2 Provider = 192 的**乘積**，但沒有給「一個 CLI_TOOL 格在 Codex 上要量什麼」。

### 1.3 裁示：這是設計缺口，需要反向修正

**建議新增一條 cell-definition clause**（不是改分母，是補定義）：

> 每個 Kind 在每個 Host 上必須指名：(a) 可安裝表面（路徑或 API）、(b) 正例判準、(c) 負例判準。
> 沒有指名的格，狀態為 `NO_HOST_SURFACE`，**不計入 PASS 分母，也不計入 FAIL**，並在驗收表以第三種狀態呈現。

這樣 192 仍然是 192，但驗收表會誠實地長成：

```
192 total = 18 PASS + 168 NO_HOST_SURFACE + 6 NOT_RUN(DeepSeek)
```

**用「0 FAIL」冒充「全數通過」正是你退回過的那種換判準**，所以我不會把 168 寫成 PASS。

---

## 2. WP-12：五次嘗試、六個假設、全部具名排除

### 2.1 失敗形態

```
RuntimeError: Failed to initialize OpenAI client:
  No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'
```

發生在 `D:\Hermes-Recovery\h22\agent\agent_init.py:1027`。

### 2.2 已排除的假設（每一條都實測）

| # | 假設 | 實測 | 結論 |
|---|---|---|---|
| 1 | 沒有 openai 可升級 | venv 有 `openai 2.24.0`，該 symbol **import 成功** | **假設錯**（我看的是安裝目錄，不是 profile venv） |
| 2 | 凍結啟動器 → 只能重建發行版 | `hermes` 是 114,995 bytes PE，跑 h22 自帶 runtime（site-packages 只有 pip/setuptools） | 啟動器確實凍結，但**「只能重建」不成立** |
| 3 | PYTHONPATH 注入即可 | `ModuleNotFoundError` 消失，gateway 仍拋同一 RuntimeError；注入的 `sitecustomize` 從未執行（啟動器忽略 PYTHONPATH） | 排除 |
| 4 | 換 provider 繞過 | `--provider opencode-go --model deepseek-v4.1-flash` → 同一個錯（import 在 `_init_openai_client` 內無條件發生） | 排除 |
| 5 | 走別的入口 | `h22/cli.py --version` → `Error: invalid_params`；`cli.py -z` → 同；`hermes_bootstrap.py -z` → 無輸出 | 排除 |
| 6 | 舊版 openai 藏在 uv 快取 | `live22/cache/uv/.../openai/types/responses/` **有**該檔案 | 排除 |

**仍未定位**：該行程 import 到哪一份 openai。我停止再挖，因為這已是第 5 次嘗試，符合你「同一異常阻擋 >4 次即須排解或暫停」的規則。

### 2.3 為什麼 Docker／獨立車道／owner 信封都不適用

- **Docker**：daemon 未啟動、WSL 兩發行版 Stopped、三個 Host 都是 Windows 原生 CLI、容器內 DPAPI 不可用。而且這是**本機行程解析**問題，容器化不會讓同一個行程找到模組。
- **獨立車道**：換車道不改變行程的 `sys.path`。
- **owner 信封**：這是技術路徑問題，不是授權問題；簽章已可用（`issue_grant.py` → `GRANT_VALID`），授權不缺。

### 2.4 裁示

阻斷維持 `RUNTIME_PATH_UNRESOLVED`，兩條路：
- **(a)** 找到啟動器實際呼叫的入口（需要讀 PE 或比對 argv），或直接跑 `hermes serve` 的後端 API；
- **(b)** Hermes 三格改以 **loader 格**量測並標記上限（`LOADER_PASS_MODEL_HALF_UNMEASURED`），**不計為 PASS**。

我建議 **(b) 作為收斂**，因為 (a) 已經吃掉五次嘗試，而 loader 格至少量到了 Host 契約的另一半。

---

## 3. WP-11：4/9 真 PASS ＋ 1 loader 格

| 格 | 狀態 |
|---|---|
| Codex × LITE / STANDARD | **PASS**（digest 來自 cwd 的 SP，badge 只來自 Host loader，負例乾淨） |
| Claude Code × LITE / STANDARD | **PASS**（同上） |
| Hermes × LITE | `LOADER_PASS_MODEL_HALF_UNMEASURED` |
| Hermes × STANDARD / ASSURED | 未跑（同 WP-12） |

兩份 SP 本身獨立驗證：LITE 15 檔 `e3e993b0e079`、STANDARD 52 檔 `52712b6316fb`，解包後 15/15、52/52 成員相符，可從解包樹 import。

---

## 4. 全部殘留／缺口／阻斷的關閉方式

| 項 | 現況 | 關閉動作 | 誰 |
|---|---|---|---|
| WP-11 | 4/9 PASS + 1 loader | 隨 WP-12 走 (a) 或 (b) | 我 |
| WP-12 | `RUNTIME_PATH_UNRESOLVED` | (a) 找入口 或 (b) 收斂為 loader 格 | 我（需你選 a/b） |
| WP-20 | 18 PASS / 168 無表面 / 6 無 runner | 補 cell-definition clause（§1.3） | 我提案，**需你核可條文** |
| F-01 `PACKAGE_READBACK.json` | 未產 | 從 `/c/wg/pkg` 重算 909/909 落收據 | 我 |
| P5C 歷史收據 | 仍掛著 | 標 `WITHDRAWN_PENDING_REWORK` | 我 |
| R-1 `halted_repeat` | 只在日誌 | 記 `SUPERSEDED_BY_WINDOWED_MONITOR` | 我 |
| D-H 憑證在 repo | 未移 | 我移檔，你輪替 | 分工 |
| D-A / D-I | **已撤回** | 關閉 | 已關 |
| 視窗風暴 | 4 站點已改隱藏 console；迴圈 paused | 儀器正控打響前不重新 arm | 我 |
| D-D / D-E / D-B | 分支與 live 整合 | 見 §5 | **需你授權** |

---

## 5. 待 owner 的決策（四件，前兩件是這次新增的）

| # | 決策 | 選項 | 建議 |
|---|---|---|---|
| **O-1** | `candidate/r18` 進 main（264 ahead / 83 behind、無共同祖先） | graft merge / 不合 / 重寫歷史 | **graft merge**——不合則 19 PASS 留在分支 |
| **O-2** | `lane/epoch-40-identity-source-20261031`（4 ahead / 0 behind） | fast-forward / 不合 | **fast-forward**，零衝突 |
| **O-3** | `PIPD/Fine-grained personal access tokens.txt` | 你先輪替 / 我先移檔 | **我先移檔，你再輪替** |
| **O-4（新）** | WP-20 的 `NO_HOST_SURFACE` 是否為合法第三狀態 | 核可條文 / 收斂 WP-20 到 AGENT_SKILL / 其他 | **核可條文**——否則只能靠發明表面湊 192 |
| **O-5（新）** | WP-12 走 (a) 繼續找入口 或 (b) 收斂為 loader 格 | a / b | **b**——已 5 次，且 loader 格誠實可標記 |

---

## 6. 候選升格（已檢測＋已驗收）

| 候選 | 證據 | 裁示 |
|---|---|---|
| `--profile` artifact depth | LITE 15 / STANDARD 52，digest 不同，13/13 | **升格** |
| Need/Occupant ABI + Consumer | `abi.py` 7/7，acceptance `GRANTED` | **升格** |
| `issue_grant` Ed25519 | `GRANT_VALID`，綁 owner authorization sha | **升格** |
| `wp20_cell_runner` | 18 格實測、冪等、JSONL 續跑 | **升格** |
| `round_continuation_gate` / `work_queue_block` / `console_guard_gate` / `stall_monitor` | 10/10、4/4、33/33 | **升格** |
| `owner_window.py` | 缺 `owner_vault` 起不來，issuer 已有替代 | 不升格 |
| `window_probe*.py` | 正控打不響 `PROBE_BLIND` | 不升格（不得作證據） |

---

## 7. 建議執行方案

**A｜WP-20 條文（需你核可 O-4）** → 落 `NO_HOST_SURFACE` 為第三狀態 → 驗收表 `18 PASS / 168 NO_HOST_SURFACE / 6 NOT_RUN`。
**B｜WP-12 收斂（建議 b）** → Hermes 三格以 loader 量測並標記上限 → WP-11 收在 `7 measured / 2 loader-capped`。
**C｜殘留收尾** → F-01、P5C、R-1、D-H 移檔，全部落收據。
**D｜合併（需 O-1/O-2）** → graft r18、fast-forward epoch-40。
**E｜視窗儀器** → 正控打響前 supervisor 保持 paused。

---

## 8. 本輪自我修正（延續 FAR-041 的三個錯）

| 先前說法 | 修正 |
|---|---|
| 「192 格要全部量」 | 只有 18 格有表面；168 格是**規格缺口**，不是工作量 |
| 「WP-12 是發行版凍結」 | 是行程解析問題；六個假設已逐一實測排除 |
| 「負例用 `SP-BADGE-` 形狀判斷」 | 模型會編 badge → 改比對**完整值**（Harness 內已修） |

共同形狀仍是**用代理取代實物**：代理路徑、代理計數、代理形狀。三次修正都指向同一條紀律：**量實物，並讓代理可被證偽。**
