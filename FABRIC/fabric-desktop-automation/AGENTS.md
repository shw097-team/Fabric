# AGENTS.md — Fabric Desktop Automation (FDA) Agent Operating Contract

> **Status: EXTERNAL_ACCEPTANCE GRANTED (r11 ALL PASS, 2026-08-14)**
> Scope: LOCAL / PAPER / NO-LIVE-WRITE. SQS_LIVE_TRADING = NOT_AUTHORIZED.

本文件是 **agent 操作 FDA 的強制契約**。任何 agent 操控 XQ/XS、執行 FDA 腳本、打包驗收證據前，**必須**先讀本文件 + 載入 `fda-desktop-automation` skill。

## 0. 強制前置（不可跳過）

1. **載入 skill**：`skill_view(name='fda-desktop-automation')` — 內含完整操作流程路由（§0 QUICKSTART）、全部 verified control IDs、陷阱。
2. **異常固定路由**：任何操作異常 → **第一個動作**是跑 `screen_state_check.py`（SSC-V2，動態 pid/含 hidden/NEEDS_CONFIRM），**禁止直接重試**。
3. **REUSE-FIRST**：任何操作前查 `FDA_ASSET_REGISTRY.json`（adapter 函數 / matrix / receipts）— 有現成資產就 CALL，禁止重寫。

## 1. 機械強制（程式化，不可繞過）

```text
執行:  python fda_run.py <script.py>        # 統一執行器：preflight → 執行 → exit≠0 自動 screen_state_check
掃描:  python fda_script_guard.py <script>  # 違規 API → BLOCK（click_input/set_focus/foreground 等；formerly FDA_PREFLIGHT_GUARD.py）
檢查:  python hgk_evidence_preflight.py     # 外部提交前：單一 checker/無 stale/三向綁定
```

**禁止**：直接 `python <script>` 執行 FDA 腳本（繞過 fda_run.py）；手寫 ctypes 取代 adapter；任何滑鼠/焦點搶奪 API。

## 2. 零滑鼠硬路由

```text
FORBIDDEN: click_input / set_focus / send_keystrokes / SetCursorPos / SendInput /
           SetForegroundWindow / cua foreground / bring_to_front / pixel-first
ALLOWED:   PostMessage BM_CLICK · SendMessage WM_SETTEXT · pywinauto tb.button(i).click()
           uia expand/select pattern · cua background · screen_state_check.py
```

## 3. 驗收狀態（已閉合，勿重開）

```text
F01 current 260811 10/10        = PASS（receipt: FDA_F01_CURRENT_260811_RECEIPT.json）
F06 fresh compile 10x           = PASS（FDA_F06_FRESH_10RUN_RECEIPT_RR6.json）
UFO² v3.0.8 effective-load 7/7  = PASS（carried）
PAPER single-wash 10x           = PASS（FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json）
PAPER STOP semantics            = PASS（FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json）
final checker 194/194           = PASS（FDA_CHECKER_FINAL_RR7.json, evaluator 9009713）
canonical manifest              = PASS（63 entries, sha a3496336 embedded body）
```

## 4. Claim Ceiling（不得超越）

```text
FDA 驗收 = Fabric-governed 本機/PAPER/無實單桌面自動化。
不得宣稱: LIVE_TRADING / PRODUCTION_AUTONOMY / REMOTE_DEPLOYMENT / 策略獲利保證
```

## 5. 外部證據打包（單一 MD）

依 hgk skill Step 6C/6D：全量 raw 內嵌、無 self-hash、manifest raw body 內嵌（宣告 sha=內嵌 body sha）、3-way mirror、提交前跑 hgk_evidence_preflight.py PASS。

## 6. 已知陷阱速查（2026-08-14 實戰 verified）

```text
- XQ toolbar TB_PRESSBUTTON 無效 → 用 pywinauto tb.button(i).click()
- XTP 自繪按鈕 BM_CLICK 無效 → PostMessageW(dlg, WM_CLOSE)
- SensorList flush 延遲 >15s（最長 30s）→ 延遲重讀驗證持久化
- SensorLog 查詢必須 LIKE '%name%'（= 查不到）
- 單次洗價 terminal = state 2→3 / exec 1→5 / 單次 trigger（RR8 authority）
- 主視窗匹配 startswith("XQ全球贏家")（不可用 in — 編輯器 title 含子字串）
- 新增成功通知 title = "時間：[HH:MM:SS]"
- 錯誤 dialog 與主 dialog 同 title「新增策略雷達」→ 以「加入(&A)」按鈕辨識
```
