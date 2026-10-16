# XQ 策略雷達 PAPER runtime 操作知識（DoD-17 閉合實戰, 2026-08-14）

來源：FDA WO-FDA-XQ-002 實跑 + FAR 研究（教程 035/002/005、社群 would2000/XQ-Auto-Writer-Skill、SQS AQT 整合收斂藍圖）。適用於「以 FDA 自動化 XQ 策略雷達 / PAPER runtime start-stop」這類任務。

## 1. XQ 模組訂閱模型（關鍵權限門檻 — 先查再跑）

- 策略雷達 = **加值功能**；**個人版涵蓋在「盤中量化交易模組」**；企業版 = XS 編輯器加購（教程 035 權威）。
- **台股進階模組不含盤中量化交易模組** → 試用版可開啟雷達、可完成「新增策略雷達」dialog 設定（readback 全對），但**自訂策略不持久化執行**。
- 驗證訊號：`XQSensor\SensorList.sqlite` 無策略記錄 + 按 START 後 toolbar `running=False`（STOP enabled 未變）。
- SQS 藍圖對應：TCW-056 XQ 策略雷達 = ADOPT_NATIVE；XQCapabilityProfile `CAPABILITY_DRIFT/RIGHTS_UNKNOWN → disable/manual fallback`。
- **DoD-17 誠實標記（試用版階段）**：`RUNTIME_QUALIFIED_AUTOMATION / EXECUTION_BLOCKED_SUBSCRIPTION`（需盤中量化交易模組）。
- **訂閱後 DoD-17 已閉合（2026-08-14 實跑，非推測）**：訂閱「盤中量化交易模組」後，自訂策略**跨 XQ 重啟持久化**（SensorList 6 個 FDA 策略全部存活），且「新增成功」確認 dialog 出現（訂閱前只有「開放體驗警示」）。**雷達 UI grid 是 XTP 自繪（uia 完全不可見）——執行真相在 SensorLog DB，不在 UI**（見 §3b）。

## 2. toolbar fsState readback 語義（社群 xq_alert.py 權威）

pywinauto win32 toolbar button `.info.fsState`：
- `fsState & 4` = TBSTATE_ENABLED（**執行真相，唯讀判準**）
- `fsState & 2` = TBSTATE_PRESSED（XTP 視覺按下狀態，**不可信**）
- 單次洗價完成 = `START enabled AND STOP disabled`（社群 `wait_single_wash_complete` 語義）。
- 曾誤判：STOP pr=True 被當「執行中」——實際 en=False 表示已停止。

## 3. 策略儲存與編碼

- 策略雷達自訂策略存於 `XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite`（**非 XSStrategyCenter**）。
- DB 是 **big5/cp950**：`conn.text_factory = bytes` + `decode('cp950', errors='replace')`；直接用 UTF-8 解碼會 OperationalError。
- 試用版：加入後短暫寫入 SensorList 但**之後被清除**（不持久化）——掃描時序不同會看到不同結果（P23 有、P26 無）。
- 「該名稱已被使用」錯誤 = XQ **記憶體殘留**（先前流程建立的策略），DB 可能無記錄——**一律用唯一名稱**（`策略名+time.strftime("%H%M%S")`）避開。
- SensorList 讀取若 Name=None：可能 XQ 正寫入中（big5 時序），稍後重試。

## 3b. 執行真相層：SensorLog（DoD-17 閉合關鍵，2026-08-14 實跑）

雷達 UI 的 grid/執行紀錄 tab 是 XTP 自繪（uia 只暴露 scrollbar 字串、TCM_SETCURSEL 切 tab 會跳到下單設定、uia TabItem.select 觸發 Afx deadlock）——**永遠別從 UI 讀執行證明**。真正執行真相：

```
C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite
  Table_YYYYMMDD（每日一表，如 Table_20260814）
```
- **PRAGMA table_info 的欄位名是 bytes**（b'XQSensorName'）——`dict(zip(cols,row))` 前要 dec 欄位名，否則 key 對不上、XQSensorName 讀成 None。
- 每策略執行留下一串狀態機紀錄：`XSSensorState` 2(執行中)→3(計算)→1(完成)，`ExecState` 1→2→3→4→5→8（完整生命週期），`SymbolID=2330.TW`，`TriggerTime`=HHMMSS（多週期 = 多次洗價觸發）。
- 實跑結果：FDAPaperFinal020037 14 rows（Seq 43-56，state {2:8,3:2,1:4}, exec {1:2..8:4}）、FDAPaperClosure011939 28 rows、FDAPaperProbe010447 14 rows —— **56 筆執行紀錄 = PAPER runtime 鐵證**，DoD-17 PASS。
- 讀取契約：`text_factory=bytes` + CP950 decode（欄位名與值都要）。

**「新增成功」確認 dialog 偽裝成時鐘窗**：title 是 `時間：[HH:MM:SS]`（owner=雷達視窗，Static 內容「策略雷達[名稱]新增成功，」、按鈕 關閉/取消）——不是明顯的 dialog 名，且 z-order 在雷達之上會吞掉 cua 座標點擊（candidates 顯示點到時鐘窗）。處理：EnumChildWindows 找其 Button → PostMessage BM_CLICK「關閉」（空文字 notice 按鈕也點第一個）。**加入流程即使腳本 print 空也可能已完成**（dialog poll 會 hang）——先 screen_state_check 再判斷失敗。

## 4. Win32 純消息細節（零滑鼠原則）

- `SendMessage WM_SETTEXT` 同 integrity 層級**有效**；**回傳 0 是正常**（非失敗）——FDA_PAPER_ALERT 就是這樣建成功的。
- **PostMessage + ctypes buffer 有 GC 生命週期 bug**（buffer 在異步處理前被回收）→ 文字設定用 SendMessage，不要 PostMessage 帶指標。
- `BM_CLICK`（PostMessage 或 pywinauto win32 `.click()`）對 dialog Button 有效；`TB_PRESSBUTTON` 對 toolbar 有效（XTP toolbar 不回標準 `TB_ISBUTTONENABLED`，用 pywinauto fsState 讀狀態）。
- 完全零滑鼠路徑 = pywinauto win32 backend 的 `.click()`/`.set_edit_text()`/`.select()` + uia 的 `.expand()`/`.select()`（SelectionItemPattern）+ 禁 `click_input()`/`SetCursorPos`/`SendInput`/`set_focus`（除非最後手段）。

## 5. 視窗匹配 pitfall

XQ 編輯器 title「XScript 編輯器 - XQ全球贏家(個人版)」**包含**主視窗 title 子字串「XQ全球贏家(個人版)」——用 `in` 匹配會先命中編輯器。主視窗必須用 **`startswith("XQ全球贏家(個人版)")`** 或精確 class `DAQXQLITEMainWnd`。

## 6. CEF dialog（開放體驗說明/警示）

- 「策略雷達開放體驗說明」與「開放體驗警示」是 **Chrome 內嵌（CEF）**，無原生 Button children（EnumChildWindows 只有 AfxWnd140/Chrome_WidgetWin_1）。
- 關閉法：pywinauto win32 `dlg.set_focus()` + `send_keystrokes("{ENTER}")`（已驗證；短暫 focus 可接受）。
- 用戶確認：試用版按「我知道了」即可試用——Enter 即等價。

## 7. 正確流程（教程 005 權威 + 實跑驗證）

1. 開雷達：主視窗 策略(D) menu → 策略雷達（cua-driver background click 可靠；pywinauto uia 對主視窗 menu bar 可列舉 15 項，但 popup 子項 uia 讀不到）
2. 關「開放體驗說明」（Enter）
3. toolbar NEW(17551) → 新增策略雷達 dialog
4. 名稱 Edit(17500) 唯一名 + 腳本按鈕(17203) → 選擇使用腳本 dialog（樹「自訂」expand 後才顯示子項；FDA_PAPER_ALERT 在展開後才可見）+ 商品(17610→741/802/803) + 觸發模式 ComboBox(17035) 選「單次洗價模式」
5. readback 全項（17500/17202/17107/17035）→ 加入(1)
6. 立即掃 notice dialog——訂閱後出現的是「新增成功」dialog（title `時間：[HH:MM:SS]`，見 §3b），非「開放體驗警示」；PostMessage BM_CLICK 其「關閉」按鈕
7. 狀態 readback：toolbar START/STOP enabled（社群語義）；**執行證明讀 SensorLog Table_YYYYMMDD（§3b），不讀 UI grid**
8. STOP(17555) → post-stop readback

**加入 = 自動執行（社群語義）**：新增流程「加入」即啟動策略（不需再按 START）——START 按鈕只對「已選中的策略列」作用，而自訂策略列在 XTP grid 中 uia 不可見、無法可靠選中；所以完整閉環 = 新增流程完成（SensorLog 出現狀態機紀錄）→ 驗證持久化 → STOP 清理。

## 8. 既有工具對應

- 社群 repo `would2000/XQ-Auto-Writer-Skill`：`xq_alert.py` 提供完整紅綠燈對照驗證 + 全部 control ID（17500/17202/17107/17035/59392/17551/17554/17555/17627/17553）——直接複用，勿重造。
- `xq_native_adapter.py`（Fabric fabric-desktop-automation）：本機薄 adapter（find_main_window/enum_children/find_child/invoke_button/set_edit_text/press_toolbar），純消息。

## 9. F06 fresh-compile 陷阱（RR6 實戰 2026-08-14：4 次失敗後的根因）

外部 r6 要求 10 次 fresh compile（distinct per-run LastCompileTime）。4 次嘗試的根因與解法：

1. **編輯器必須先有「已命名」腳本，F6 才有 target**：SCI_SETTEXT 只改 Scintilla 內容；若 tab 是未命名/空白腳本，F6 不編譯任何東西 → `Sensor` 表無新 row、`LastCompileTime` 永不更新。順序 = 先建立/開啟已命名腳本（新增腳本 dialog 或用戶手動開）→ 再 SCI_SETTEXT + F6（每 run 加唯一 marker 註解讓 LastCompileTime 前進）。
2. **Alt+F popup toggle 陷阱**：`send_keys("%f")` 開出檔案(F) XTPPopupBar，但**循環中重送 Alt+F 會把它 toggle 關閉**。應開一次 → 按 `n`（新增）。即使如此，XQ 3.20.02 自訂 menu 可能不吃鍵盤加速鍵——每次 menu 嘗試後先 screen_state_check 找 `#32770`/`AfxWnd140`（title 新增腳本）再斷言 dialog 存在。
3. **「警示提示」dialog（0x3087a，XTP 自繪）**：按鈕 關閉/清除/策略雷達；BM_CLICK 與 WM_CLOSE 都關不掉。它對純消息操作無害（PostMessage/SendMessage 與 z-order 無關）——不要與它纏鬥，直接繼續操作。
4. **編譯 DB 表名是 `Sensor` 不是 `Script`**（DAQXQLITE_SHW097_Script.sqlite；tables: Folder/Function/Indicator/Sensor/Filter/Rank/ValueFunction/AutoTrade/Version/LocalRank）。欄位 Name/CompileStatus/LastCompileTime，cp950 bytes decode。

**Native SCI_SETTEXT（pywinauto 0.6.9 RemoteMemoryBlock bug 的繞法）**：
`pywinauto.remote_memory_block.RemoteMemoryBlock.Write` 在 0.6.9 會 raise
`TypeError: this type has no size`。可用配方：`VirtualAllocEx`（PAGE_READWRITE，目標 XQ process）
→ `WriteProcessMemory`（CP950+NUL bytes）→ `SendMessage(SCI_SETTEXT=2181, 0, remote_addr)`
→ 驗證 `SCI_GETTEXTLENGTH=2183`。
