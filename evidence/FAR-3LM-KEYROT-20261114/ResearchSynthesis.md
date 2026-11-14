# ResearchSynthesis — 3LM 車道 API 金鑰輪替的既定程序

- **WorkOrder**: `WO-FAR-3LM-KEYROT-20261114`
- **完成時間**: 2026-11-14T11:55:26+00:00
- **決策問題**: 如何制定高效、可行、可複用、低阻力的 3LM API 金鑰輪替既定程序？
- **Claim ceiling**: `LOCAL_CHECK`（本輪未取得 production 輪替授權、未變更 provider、未動 origin main）

## 1. 結論（一句話）

輪替慢不是因為換 key 難，而是因為**「誰在讀這把 key」沒有宣告**；因此最小可行程序不是引入 secret
manager，而是**一份 consumer 清單 ＋ 一支可重跑的命令 ＋ 一份 hash-only 收據 ＋ 一條可回滾路徑**。

## 2. 事實（measured）

| # | 事實 | 來源 |
|---|---|---|
| C1 | 車道憑證在 FHS_NEXT 內有兩個 consumer：`start-router.ps1`（`$credentialPath`）與 `ops/r1_host_readback.py` | S01/S02 |
| C2 | 兩者都只讀「檔案路徑」，所以輪替是改指標，不是改程式 | S01/S02 |
| C3 | router 在**啟動時**以 `${OPENCODE_GO_API_KEY}` 讀入環境；執行中的 router 不會自動換 key | S03 |
| C4 | 直接打 provider `/v1/models`，新舊 key 都回 403 → **不能**當有效性判準 | S04 |
| C5 | 唯一可靠的判準是 codex 探針：`provider=opencode_go`＋`model=deepseek-v4.1-flash` 回固定字串 | S05 |
| C6 | 3LM dispatcher 在 codex binary pin 失效時**拒絕 spawn**（`ERR_LANE_PIN_IDENTITY_INVALID`） | S03＋實際 dispatch |

## 3. 反例（Rejected）

| 方案 | 為什麼不用 |
|---|---|
| Secret manager／vault | 單人單機卻引入第二權威與網路依賴，違反最小可行 |
| `setx` 環境變數 | 值進 registry 與 shell 歷史；且既有 file-pointer 已足夠 |
| provider HTTP 探針當 gate | 實測 false negative（C4） |
| cron 自動輪替 | 需要 provider 憑證與無人值守權限，Owner 才是發行者 |
| 改兩支 consumer 的程式 | 沒解決「consumer 集合未知」的根因 |

## 4. 建議程序（最小可行版）

1. **單一指標**：`ops/3lm_consumers.json` 宣告「憑證路徑 ＋ 每個 consumer 的檔案與樣式」；新 consumer＝加一行。
2. **一支命令**：`python ops/rotate_3lm_key.py --key-file "<新 key 檔>"`（預設 dry-run，`--apply` 才寫）。
   依序：驗檔（非空、無 CR、長度合理）→ 改指標（每個 consumer 先 `.bak-<UTC>`）→ 印重啟指令 →
   codex 探針（key 只進子程序環境）→ 寫 `out/ROTATION_RECEIPT_<UTC>.json`（只存 sha 前 12 碼與長度）。
3. **驗收四條**（Definition of Done）：收據存在且 `secret_printed=false`；探針 `exit 0` 且回固定字串；
   新舊 fingerprint 不同且舊指標檔保留；收據路徑寫進當輪 `EVIDENCE_INDEX`。
4. **回滾**：用 `.bak-<UTC>` 還原 → 重啟 consumer → 再跑探針；不需要任何新工具。
5. **同形狀的第二件事**：toolchain pin（codex binary path/version/sha）用同一支命令的 `--pin-refresh`
   分支處理，**需 Owner 核准**才可寫 lane config。
6. **不做**：vault、setx、cron 自動輪替、provider HTTP 探針當 gate、把 key 寫進任何文件。

## 5. 與 FHS_vNEXT 上游對齊

- Fabric：導覽 `effect_permission=NONE`，未知路由只停受影寫入 → 本程序不會因缺件而阻塞讀與草案（S07）。
- HG-KSEOS：`AGENTS.md` 規則 4「never commit … credentials / raw lane output」→ 收據只存 hash（S06）。
- W0/W1：輪替屬 Host/credential 面，不是 W1 產品條款；W1 只要求「可執行、可驗、可回滾」的證據面。

## 6. 未解（Open）

- `OQ1` 舊 key 檔保留或刪除（回滾需求 vs 縮小暴露面）。
- `OQ2` toolchain pin refresh 是否併入同一命令。
- `OQ3` provider 端的輪替節奏／TTL（本地不可推導）。

## 7. 車道紀錄

- EXECUTE（bounded writer，`deepseek-v4.1-flash` via codex CLI）：**TIMEOUT**（兩次嘗試各 ~9–10 分鐘無落檔），
  依規則不冒充，改由 PLAN 以同一寫入範圍完成；檔案 `ops/rotate_3lm_key.py` 10576 bytes、
  `RUNBOOKS/3LM_KEY_ROTATION.md` 4518 bytes
- VERIFY 第一輪（fresh-context challenger，同 model）：**V1 PARTIAL／V2 PASS／V3 FAIL／V4 FAIL／V5 PASS／V6 FAIL／V7 PASS／V8 PASS**
  → 三項 FAIL：套用非交易式、失敗碼未封閉、文件範圍聲明與證據不符
- VERIFY 第二輪（修正後複核）：**R3 PASS／R4 PASS／R6 PASS／R1 PASS**（三項 FAIL 全數關閉）
- 3LM dispatcher：**BLOCKED**（`ERR_LANE_PIN_IDENTITY_INVALID`；宣告 `0.167.0-alpha.3.2@5449c1f0` 不存在，
  實裝 `0.167.0-alpha.4.1@9e1da794`）。此為本輪「應被程序覆蓋」的第二個同類缺口。
