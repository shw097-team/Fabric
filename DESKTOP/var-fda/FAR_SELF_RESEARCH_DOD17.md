# FAR 自研究 + 自進化報告：FDA DoD-17 效率與失敗根因分析
# 2026-08-13 | 依 user 最高授權啟用 FAR 框架

## 一、進度極慢與多次失敗的根因（依證據）

### 根因 1（最致命）：delivery_mode 用錯 — foreground 搶佔用戶滑鼠與焦點
- **證據**：本 session 幾乎所有 cua-driver click/hotkey/press_key 都帶 `delivery_mode: "foreground"`
- **官方文檔（cua.ai/docs/concepts/capture-and-delivery-modalities）權威**：
  > "background (default): Input is routed to the target process/window/element directly. **The user's frontmost app, real cursor, and window z-order are untouched**"
  > "foreground: The target is briefly fronted for that action... **Use this when a background attempt did not land**"
- **影響**：foreground 每次動作都會把 XQ 視窗拉到最前，搶走用戶正在操作的視窗焦點；且 XQ 是 Afx 老應用，foreground 觸發的 UI 操作更容易卡死
- **對用戶問題的直接回答**：**會**。我用 foreground + 自寫 SendInput/SetCursorPos 真實滑鼠移動，用戶滑鼠操作被我搶占、干擾（游標被 SetCursorPos 移走、點擊被 SendInput 搶走）

### 根因 2：自寫 Win32 SendInput/SetCursorPos — 直接移動真實滑鼠
- 我寫了 `SetCursorPos` + `SendInput` 真實滑鼠事件（sendinput_name.py / run_conservative.py 等）
- **這直接移動用戶的真實游標並搶佔輸入** — 與用戶同時操作滑鼠完全衝突
- cua-driver background 模式本來就是為了解決這個（"without stealing the cursor or focus"），我卻繞過它用原生 SendInput

### 根因 3：反覆用 Enter 鍵觸發 dialog 確認 → XQ 崩潰 ×3
- **證據**：3 個 crash dump（7580×2、14200）都在 SendInput/Enter 操作後產生
- Enter 在 Win32 dialog 中會觸發默認按鈕，且 SendInput 真實鍵盤在 XQ 上不穩定
- 每次崩潰 → 重啟 XQ（35s）→ 重開編輯器（10s+）→ 重做 → 再崩潰 = **無窮重啟循環**

### 根因 4：UIA vs Win32 雙軌混用造成狀態紊亂
- 我同時用 cua-driver UIA（get_window_state/element_token）與原生 Win32 API（EnumWindows/PostMessage）
- 兩套工具的窗口 handle 標識不同（cua window_id vs Win32 hwnd），**誤判窗口、點錯按鈕**（選股中心被誤開、加入雷達點到錯誤座標）
- cua window_id 與 hwnd 恰好數值相同（0x2210b8e = 35720078）但語義不同，容易混用

### 根因 5：缺少對 XQ 交互模式的系統性認知（違反 search-before-trial）
- 教程 005 早就寫明正確流程（新增警示腳本 → 右鍵加入策略雷達），我卻在「找啟動按鈕」上繞了數十輪
- 根因分析後發現：**策略雷達的「啟動」根本不需要按按鈕 — 「加入策略雷達」即自動開始執行**（教程 002/005 明載）

### 根因 6：pixel click 猜測座標（違反 search-before-trial + force-pause）
- 多輪 pixel click（881/948/1007/1785/2320…）全屬亂試，已被用戶糾正並建立 search-before-trial skill

## 二、高效解決方案（擬定）

### 原則 1：全背景模式，零搶佔
- **所有 cua-driver 動作：不帶 delivery_mode（默認 background）或明確 `"delivery_mode": "background"`**
- 絕不再用 SetCursorPos/SendInput/SetForegroundWindow 原生真實輸入
- 需要真實鍵盤時用 cua-driver 的 `type_text`（background 路由，不搶焦點）

### 原則 2：單一窗口標識系統
- 只用 cua-driver 的 `(pid, window_id)` 作為唯一標識
- Win32 API 僅作為「唯讀觀察」輔助（EnumWindows 列出 dialog 是否存在），**不用 Win32 做輸入**
- 輸入一律走 cua-driver（background）

### 原則 3：Win32 dialog 用 PostMessage BM_CLICK（不搶焦點）
- 對 UIA 不可見的 #32770 dialog：用 PostMessage BM_CLICK 點按鈕（先前「警示」類型點擊成功證明有效）
- **禁用 Enter/SendInput 真實鍵盤**（崩潰根源）
- 名稱輸入：嘗試 PostMessage WM_SETTEXT（先前部分成功）；若無效則 cua-driver type_text（background）

### 原則 4：正確流程一次到位（教程 005 權威）
1. 重啟 XQ（乾淨）→ 開 XS 編輯器
2. 檔案(F)→新增(N)→「警示腳本」類型（PostMessage BM_CLICK，已驗證成功）
3. 填名稱 FDA_PAPER_ALERT → 確認
4. 貼入 ret=1 警示腳本 → Ctrl+S 儲存 → F6 編譯 → **DB Sensor 表 readback CompileStatus=1**（已完成 ✓）
5. **右鍵腳本 → 加入策略雷達**（或「加入雷達」按鈕，用 background element click）
6. dialog 出現 → PostMessage BM_CLICK「加入」（名稱已預填）→ **自動開始執行（綠燈）**
7. readback：「執行中」分類 + SensorLog + DB Enable/LastExecuteTime

### 原則 5：執行前先確認用戶可用性
- **每次執行前確認用戶是否正在使用滑鼠/鍵盤** — 若用戶在用，告知並等待
- background 模式本身不干擾用戶，但 XQ 崩潰重啟會佔用資源

## 三、對用戶問題的直接回答

> 「用戶也再用滑鼠處理其他事務，對你的進行是否會有影響？」

**會有影響 — 而且是雙向的：**
1. **我影響用戶**（根因 1/2）：foreground delivery + SetCursorPos/SendInput 真實輸入 = 搶用戶游標、搶焦點、搶點擊。用戶會看到游標亂跑、視窗跳來跳去、點擊被搶
2. **用戶影響我**：用戶的滑鼠/鍵盤輸入會與我的 SendInput 混在一起，我的點擊可能落在用戶正在操作的位置（誤觸其他東西），或用戶的移動讓我的座標失效

**修正後**：全部改 background delivery 後，cua-driver 直接路由輸入到目標窗口（官方保證不碰用戶的 frontmost app、真實 cursor、z-order），用戶可正常使用滑鼠，互不干擾。

## 四、執行計畫（待用戶確認後啟動）
1. 重啟 XQ（乾淨狀態）
2. 用 background 模式完成：新增警示腳本（FDA_PAPER_ALERT 已存在，直接載入）→ 加入策略雷達 → 自動啟動 → 停止
3. 全程 readback（DB + 執行紀錄 + 綠燈）
4. 更新證據 MD → 內部驗收 ALL PASS
