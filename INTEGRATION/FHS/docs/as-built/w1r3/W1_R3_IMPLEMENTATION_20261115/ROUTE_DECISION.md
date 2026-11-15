# 路線決定：EXECUTE 車道走哪條路（2026-11-15，業主裁定後）

## 一、被廢止的路線（已排除，不再嘗試）

**Codex CLI 沙盒路線**：`codex exec -s workspace-write -C <round> <brief>`，8 個工作包並行派工。

- 實測結果：8 個回合**全部**在 Codex 自己的 unified-exec 助手啟動階段失敗
  （`Failed to create unified exec process: orchestrator_helper_incomplete: setup helper exited successfully before setup completed`），
  每個回合耗掉一次模型呼叫卻**零檔案產出**。
- 業主裁定：Codex 沙盒是錯誤路由，不可再繼續嘗試。
- 處置：停止全部回合（kill），刪除該路線的 log，改走下列路線；本輪不再使用 Codex CLI 寫入。

## 二、採用的路線：已建成的 3L&M 入口 ＋ 直連 loopback router

| 步驟 | 指令（實際執行過） | 產出 |
|---|---|---|
| 1. 選單 | `ops/tools/fhs_3lm_pathadapter.py --menu` | epoch `registry_sha256 3583f71b…`、`pool_sha256 7a164911…`、per-lane slot 表 |
| 2. 綁定 EXECUTE | `… --bind EXECUTE primary` | `lanes/bindings/EXECUTE_primary.json`（DEEPSEEK V4.1 FLASH／opencode-go，pool_rank 1） |
| 3. 綁定 VERIFY | `… --bind VERIFY opt1` | `lanes/bindings/VERIFY_opt1.json`（同上 arm；本輪 owner 指定 verify 同模型） |
| 4. 寫入回合 | `POST http://127.0.0.1:10102/v1/chat/completions`，`model=deepseek-v4.1-flash` | 每個回合的 reply＋receipt（`out/EXECUTE_RUNS*.json`、`out/_prompt_*.txt`） |
| 5. 獨立回合 | 同端點、同一 arm、**另一個 context** | `out/REVIEW_CYCLES.json`、`out/VERIFY_REPLY_0N.txt` |

**為什麼是 10102**：那是本機 owner 的 `desktop-model-router`（`model_provider = "desktop_router"`、
`openai_base_url = http://127.0.0.1:10102/v1`），持有 provider 憑證；本輪因此**完全不接觸任何 key 值**，
`build/lane_call.py` 只做一次 HTTP POST，收據只記 sha256 前 12 碼與長度（`secret_printed: false`）。

## 三、被否決但仍記錄的第三條

直連 `https://opencode.ai/zen/go/v1/chat/completions`（Bearer key）對本機三把 key 全部回
`HTTP 403`、body `error code: 1010`（邊緣阻擋，非憑證失效）。此路線**不做**，記錄以免下一次重試。

## 四、這條路線的限制（不可被說成 Native）

- 3L&M 只回答「這個 epoch 下這條 arm 可否被選」；它不簽 Permit、不做 Native 准入。
- 本輪的「獨立回合」是**同家族模型 + 另一個 context + 另一條 lane 綁定**的獨立回合，
  不是原域 Protected Checker，因此 `INDEPENDENT_PASS` 不在本輪 claim ceiling 內。
- 回合歸屬：早先三個 WP 的寫入回合以 receipt（prompt sha ＋ reply sha ＋ usage）歸屬；
  加入 run-token 後，WP-FHS-02 的兩個回合同時有 token 回顯。WP-03…20 的回合收據被後續重跑覆蓋，記 RC-3。
