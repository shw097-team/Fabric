# FAR-036｜從「找不到」到「表面不同」：四包殘留的精確工作量與可達路徑

日期：2026-10-31（台北）
路由：Fabric 治理契約 → SBL 產品工程指揮入口 → HG-KSEOS 授權／狀態／驗收控制平面
車道：PLAN `openai-codex/gpt-6.1-sol`｜EXECUTE `opencode-go/deepseek-v4.1-flash`｜VERIFY `openai-codex/gpt-6.1-sol`
權威：`work_queue` — 22 條 = **18 PASS / 4 FAIL / 0 NOT_RUN**

---

## 0. 本輪新增的實測（不是推論）

| 事實 | 量測 |
| --- | --- |
| 原 packager 現在跑得動 | `pipd export` → `fhs-wp11-portable-sp.tar.gz`，77 檔，archive `6062c729a05b`，manifest `c161286a1dba`，77/77 成員逐檔重驗 0 不符 |
| 兩個真實缺陷已修 | ① 死連結使 `rglob` 中止整個 walk（WinError 1920，卻顯示 `INPUT_SHAPE_INVALID`）② repo 級 secret 掃描否決了它影響不到的 bundle |
| WP-11 第 1 格真的在 Hermes 上跑完 | install→register→effective load→trigger→unload 全量測；收據 `CELL1_RECEIPT.json`；裁決 **PARTIAL** |
| 四個宿主的真實表面 | Hermes：`skills/`（57→56）｜Codex：`~/.codex/skills`（實有 2 個在用）｜Claude Code：`~/.claude/agents`（實有 5 個在用）｜ChatGPT：無本地 runner |

**第 1 格是 PARTIAL 不是 PASS**，兩個未量欄位照實寫進收據：`provider_off_parity` 未量、`nontrigger` 只有清單事實沒有行為測試。

---

## 1. 尚未 PASS 的完整清單與精確工作量

| 包 | 缺什麼（精確） | 工作量 | 可達性 |
| --- | --- | --- | --- |
| **WP-11** Portable Host Dogfood | 9 格（3 SP × 3 宿主）。已量 1 格 PARTIAL | 每格 ≈ 一次 install/load/trigger/unload；宿主表面不同（Hermes=skills、Codex=skills、Claude=agents） | **可達**，機械但需逐格 |
| **WP-12** W18 Normal Mode | ① `C:/wg/queue/WP-FHS-12` 目錄不存在（brief 從未寫）② 一次普通 Goal 的 W18 實跑與 E33–E42 raw | 1 brief + 1 次 normal-mode 會話 | **可達** |
| **WP-13** CAP On-Demand + HotSwap | HotSwap 0 實作（規格 81 處）；TechnologyAdmission 已存在 | 一支換手程式 + POS/NEG parity | **可達**（唯一需要新寫程式的包） |
| **WP-20** 192 Cell | 8 Kind 只建 1 列；分母含 48 個 ChatGPT cell 在定義上不可能 native | 144 admitted cell（若簽 D-A） | **部分可達**：ChatGPT 48 格永遠 NOT_ADMITTED |

---

## 2. 再跳脫一次框架：這次的答案不是「找不到」，是「表面不同」

上一輪我承認誤讀（把「原 Host」讀成一支叫 `host_loader` 的程式）。這一輪把誤讀推到下一層：

**四個宿主的「loader」根本不是同一種東西，所以「同一支腳本跑四次」從一開始就是錯的模型。**

| Host | 真實 surface | 已驗證在用 | 該做的 cell |
| --- | --- | --- | --- |
| Hermes Agent | `profiles/<p>/skills/<name>/SKILL.md` | 57 個 | 已量（cell 1） |
| Codex | `~/.codex/skills/<name>/` + `codex plugin` | 2 個（mem0、security-threat-model） | 同形，換根目錄 |
| Claude Code | `~/.claude/agents/<name>.md` + `--agents` | 5 個（ocx-*） | **不同形**：agent 而非 skill |
| ChatGPT | 無本地 runner（規格自述） | — | 只能 NOT_ADMITTED |

這是本輪最重要的裁示：**WP-11 的 9 格不是 9 次同樣的操作，是 3 種不同的宿主契約 × 3 個 SP。** 把它當 9 次複製貼上，會在 Claude Code 那 3 格全部失敗，然後又被誤讀成「宿主不支援」。

### 三個替代路徑複評（你點名的）

| 路徑 | 判定 | 依據 |
| --- | --- | --- |
| 獨立車道 | 可用，不解決 | 三車道 `required==served` 已固化；車道加速「做」，不替代宿主 install |
| Docker 沙盒 | **不可用於此四包** | daemon 未啟動（npipe 不存在）、WSL 兩發行版 Stopped；三宿主皆 Windows 原生 CLI；容器內 DPAPI 更不可用 |
| owner envelope | 已開可用，是授權不是能力 | `WIN-68f2056b1972` 剩 21,654 s、0/40 ops、指紋一致；能簽 install，不能生 HotSwap |

---

## 3. 第 1 格為什麼是 PARTIAL，以及怎麼補成 PASS

| 未量欄位 | 為什麼沒量 | 補量方法（可執行） |
| --- | --- | --- |
| `provider_off_parity` | 靜態 SKILL.md 由 loader 服務，session 內無法關 provider | 用 `hgk-lane-dispatch --provider-off`（或等價的離線 loader 呼叫）在**不呼叫任何 provider** 的路徑下重取同一 skill，比對 sha；相同即 parity |
| `nontrigger` | 只做了「token 只存在一個檔案」的清單事實 | 開一個**新 session**、給一個無關 Goal，證明 token 不出現；再給觸發 Goal，證明出現 |

兩者都是可執行的量測，不是能力缺口。**在補完之前，第 1 格不得升格。**

---

## 4. 規格缺口／筆誤的裁示

| 疑點 | 裁示 | 需不需要反向修正規格 |
| --- | --- | --- |
| 「原 Host 不存在」 | 我的誤讀（已撤回三份記錄） | 否 |
| 四宿主 loader 同形 | 我的誤讀（本輪） | 否 |
| WP-20 192 含 48 個 ChatGPT cell | **規格缺口**：要求規格自己禁止的結果 | **是**：分母 192 → `144 admitted + 48 NOT_ADMITTED_BY_SPEC`，需 owner 簽 |
| HotSwap | 實作缺口（規格 81 處、程式 0） | 否，立項即可 |
| packager 死連結／repo 級 secret 否決 | **設計缺口**（已修，`b88ae1c`） | 否，已修並保留 repo_hygiene 報告 |

---

## 5. 全部殘留如何關閉（每項都有會拒絕假關閉的 gate）

| 殘留 | 關閉物 | 拒絕假關閉的 gate |
| --- | --- | --- |
| WP-11 8 格未量 | 逐格收據（13 欄位） | 空 trigger 或只有 install log → `HOST_NOT_EFFECTIVE`（規格原文） |
| WP-11 cell 1 兩個欄位 | provider-off 重取 + 新 session nontrigger | 收據缺欄位即 PARTIAL，不得升格 |
| WP-12 無目錄 | 立 brief | `work_queue` DELIVERY 量測解析 |
| WP-13 HotSwap | 換手程式 + parity | `CAPABILITY_PARITY_NOT_PROVEN` |
| WP-20 分母 | owner 簽 D-A | `refusal_gate`（需 cited_text/falsifier/expiry） |
| genie-adapter projection stale | 重新推導過 `--strict` | `MUT-STALE-SOURCE` / `MUT-WEB-WRONGSET`（已實測會拒） |
| rollout 身份未綁定 | `REQ-SEC-ROLLOUT-BINDING` | `--require-rollout-binding` 目前拒絕 |
| repo 內憑證檔 | 由 owner 處置（`PIPD/Fine-grained personal access tokens.txt`） | `repo_hygiene: FAIL` 已持續報告 |

---

## 6. 待 OWNER / issuer 決策（全部可在現有 envelope 內簽完）

| # | 決策 | 建議 | scope | 不簽的後果 |
| --- | --- | --- | --- | --- |
| **D-A** | WP-20 分母 192→144，ChatGPT 48 格 `NOT_ADMITTED_BY_SPEC` | **簽** | `registry_row_sign` | 192 永遠不可能全 PASS |
| **D-B** | live HGK/GENIE 整合授權（S5/S6） | **有條件簽**：單格 fixture→live 試點 | `admission_bundle_sign` | WP-11 native 永遠 HOLD |
| **D-C** | HotSwap 立項（WP-13） | **簽** | `permit_sign` | WP-13 永遠 FAIL |
| **D-D** | r18 具名 graft 併 main | **簽** | `registry_row_sign` | 本輪 20+ commits 只存在 r18 |
| **D-E** | `lane/epoch-40` 併 main（4 ahead / 0 behind） | **簽**（fast-forward） | `registry_row_sign` | epoch 40 只在分支 |
| **D-F** | FAR 分支 | 保留 audit，不合 main | — | — |
| **D-G** | PIPD packager 修復併 main（`hgk/fhs-wp11-packager-repair-20261031`） | **簽** | `registry_row_sign` | 其他團隊仍拿不到能跑的 packager |
| **D-H** | `PIPD/Fine-grained personal access tokens.txt` 處置 | **簽：移出 repo 並輪替** | `permit_sign` | 憑證持續在 repo 內 |

**否決**：bounded 改叫 native；ChatGPT cell 算 PASS；把 `provider_off_parity` 留空卻標 PASS。

---

## 7. 升格與併 MAIN（實測拓撲）

| 分支／候選 | 拓撲（實測） | 判定 |
| --- | --- | --- |
| `lane/epoch-40-identity-source-20261031` | merge-base `303395be`，**4 ahead / 0 behind** | **可併**（fast-forward）→ D-E |
| `hgk/fhs-wp11-packager-repair-20261031`（PIPD） | 1 commit，PR 已可開 | **可併** → D-G |
| `candidate/r18-fhs-skeleton-spine-20261029` | merge-base **NONE**（unrelated histories） | 需**具名 graft** → D-D |
| `candidate/r19-fhs-implementation` | merge-base **NONE** | 同上 |
| `far/far-031-…`（Fabric） | 獨立 audit branch | 保留 |
| WP-11 cell 1 | PARTIAL（2 欄位未量） | **不可升格**，補量後再議 |
| WP-FHS-17 bounded PASS | `EVT-e7a55272fd18a6ac` | **可升格為模板**（已用於 WP-11 規劃） |

---

## 8. 達成 ALL PASS 的執行計畫（含成本）

| 階段 | 內容 | 格數 | 預估 |
| --- | --- | --- | --- |
| A1 | 補量 cell 1 兩欄位（provider-off + 新 session nontrigger） | 1 | 短 |
| A2 | Codex cell（`~/.codex/skills`，同形） | 3 | 中 |
| A3 | Claude Code cell（`~/.claude/agents`，**不同形**，需 agent 包裝） | 3 | 中偏長 |
| B | WP-12：立 brief + 一次 W18 normal-mode 實跑 | 1 | 中 |
| C | WP-13：HotSwap 實作 + POS/NEG parity | 1 | 長（唯一新程式） |
| D | WP-20：144 admitted cell 逐列建 | 144 | 最長，建議先簽 D-A 再排程 |

**順序理由**：A1 最便宜且能立刻把 1 PARTIAL 變 1 PASS；A2/A3 建立三宿主模板；B 獨立；C 需新程式；D 成本隨產品規模線性成長，必須先修正分母。

---

## 9. 下一步（單一指令）

```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS && python scripts/work_queue.py show    # 18/4/0
# A1 補量：
#   provider-off 重取 fhs-wp11-probe 並比對 sha
#   新 session 給無關 Goal，確認 TRIGGER_TOKEN 不出現
```

**不要做**：不要用 Docker 繞簽章；不要把 Claude Code 的 agent 表面當成 skill 表面硬套；不要為讓 gate 變綠手改投影。
