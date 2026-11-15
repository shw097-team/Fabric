# UPGRADE_CLOSEOUT — Hermes v0.22.5 Desktop 收尾與正式驗收（第二輪）

2026-11-02（Asia/Taipei）。延續 [PR #21](https://github.com/shw097-team/Fabric/pull/21)（Draft，head `50782d14adbd9cded8d1ade17832c390a0472cd8`）之交接，只補做本輪具權限且可實跑的收尾切片；不重跑升級計畫、不建第二套 Shadow、不重做全量備份。

## 0. 終態裁決

| 判準 | 結果 | 證據層級 |
|---|---|---|
| `DESKTOP_DAILY_READY` | **PASS** | 新版 Desktop 從正常入口啟動、真實 GUI 對話、Session 持久化、關閉後重啟仍為同一 Runtime |
| `ENTRY_UNIFIED` | **PARTIAL** | 桌面捷徑與開始功能表已同啟動器／同 Home；工作列釘選需使用者一次手動確認（見 §2） |
| `PRESERVATION` | **HOLD** | 本輪新增可驗還原的收尾增量包；前輪備份與受保護 ACL 缺口未閉合（見 §5） |
| `MODEL_ROUTE` | **PARTIAL** | requested/configured/billing_provider 已記錄；`ACTUAL_SERVED` 未捕捉（見 §6） |
| `FHS_NATIVE_READY` | **HOLD** | Fabric policy consumer 讀路徑實跑 PASS；無 HGK Permit／Consumer ACK／Native 世界效果（見 §7） |
| `CUTOVER_DONE` | **false** | 未停舊 Gateway、未改 Issuer/Trust、未代簽、未合併／Release（見 §9） |

## 1. 入口真實身份（唯讀＋一處授權變更）

| 入口 | 變更前 | 變更後（已讀回） | 判定 |
|---|---|---|---|
| 桌面 `Hermes.lnk` | → `wscript launch-desktop.vbs` → `h22\Hermes.exe`，`HERMES_HOME=<recovery home>`、`HERMES_DESKTOP_HERMES_ROOT=<h22>` | 未變更；同鏈路 | PASS（原本已正確） |
| 開始功能表 `Hermes.lnk` | 直接指向 `h22\Hermes.exe`，**未帶 `HERMES_HOME`** → 可能落到舊 Home／舊 Profile | 已改為與桌面同一個 `launch-desktop.vbs` 啟動器（原檔已備份） | PASS（本輪修正） |
| 工作列釘選 | **實際已無任何 Hermes 釘選**（釘選目錄僅 Explorer／Chrome 等；Taskband Favorites 亦無舊 v0.21.5 條目） | 已放入指向同一啟動器的釘選 `.lnk`；Windows 11 不接受程式化註冊（`Taskband` 未寫入、shell 動詞阻塞） | PARTIAL：需使用者右鍵「釘選到工作列」一次 |

**結論**：舊 v0.21.5 不再是任何日常入口（桌面、開始功能表、工作列皆非）。前輪「工作列舊圖示仍啟動 v0.21.5」的敘述在本輪已不成立，屬實況變化而非修補結果。

執行中程序（重啟後讀回）：4 個 `Hermes.exe` 全部來自 `h22\apps\desktop\release\win-unpacked\Hermes.exe`，視窗標題 `Hermes`；舊版安裝（`pyproject 0.21.5`／`f97608f178`）僅存在於磁碟與其 Gateway 程序，未刪除。

## 2. Desktop UAT 實跑

| 項目 | 結果 | 讀回 |
|---|---|---|
| ① 入口同版 | PASS | 桌面／開始功能表同啟動器 → 同一 `h22` EXE |
| ② GUI 啟動、送出／回覆、Session 持久化 | PASS | 同一 Session 於 profile `hgk-governed`：`source=gui`、`model=deepseek-v4.1-flash`、`billing_provider=opencode-go`、**49 API calls／137 messages** |
| ③ 關閉後重啟仍為 h22 | PASS | 關閉 5 個程序 → 5 秒後為 0 → 由 vbs 重新啟動 → 4 個新 PID，EXE 路徑同 `h22`；Gateway 未重啟（`16952` 存活）；同一 Session 續用（就緒後 message 由 53 增至 137） |
| ④ 原 Profile／Skills／歷史 Session 非破壞讀回 | PASS | 舊 Home `state.db` 唯讀可讀：971 sessions／189,889 messages；`skills/` 目錄存在；recovery Home profile 清單可讀（`hgk-governed`） |
| ⑤ 合法 Model／Profile 真切換 | HOLD | 日常 Home 僅一個 profile；GUI 內真切換未執行（未以設定頁可見冒充切換） |

Session 持久化證據取自 profile `state.db` 唯讀查詢（`mode=ro`），未寫入、未刪除任何 Session／DB。

## 3. Gateway／Home／Profile／Cron 隔離（本輪 Delta）

- 三個 `state.db` 為**不同檔案**（不同 `st_dev`／`st_ino`）：舊 Home、recovery Home、profile `hgk-governed`。舊 Home `state.db` 1,384,513,536 B；recovery Home 1,265,934,336 B。
- Gateway 並存但分離：舊版 `12688 → 6096`（埠 4976）、recovery `16952`（埠 4971／4975，`/health` 200）。**未停止任何 Gateway、未搶接埠。**
- recovery Home `cron/jobs.json` 3 個 job，**全部 `enabled=false`**；本輪未見同 ID 雙邊啟用或重複派工。
- 未變更 Issuer／Trust Root／Policy／Queue／Checker；未重播 `UNKNOWN_EFFECT`。

## 4. 保全增量與代表性隔離還原讀回

- 本輪新增 `closeout_delta_20261102.zip`（14 members、706,360 B、`sha256 a9ca9e14bac62f76e2e268c56e455b0f53ace876f3fcb2bccac9c57f8900c94a`），內容僅：四庫 tracked-diff patch、`git status -uall` 名稱清單、recovery `config.yaml`／`cron/jobs.json`、桌面／開始功能表／工作列捷徑（含變更前備份）。**排除** DB／Session 內容、`auth.json`、受保護 Trust／金鑰、完整 repo 樹。
- 隔離還原抽驗：ZIP CRC 無錯、解壓後 **14/14 member SHA-256 相符**。
- 差分可重放性：Fabric（70,600 B）與 PIPD（7,372 B）patch 以 `git apply --check --reverse` **rc=0** → patch 與現行工作樹修改完全對應（非推測）。
- 前輪備份（7 份 archive 之 SHA／bytes 見 `MANIFEST.json`）本輪沿用、**未重跑全量**；但本輪有界搜尋未在預期深度找到 archive 本體，故不宣稱「SHA 對實體檔」本輪已覆核 → `RESTORE_SCOPE_HOLD` 維持。
- SBL 36 未綁項、HGK 975／SBL 4 拒絕存取路徑：沿用前輪分類，本輪未再掃描、未刪除、未改 ACL。`PRESERVATION=HOLD` 不變。

## 5. 工作樹基線校正（重要，避免誤判）

前輪 `status_entries_initial`（SBL 58,837／PIPD 25,598）與本輪 `status --porcelain`（47／239）之差，經 `-uall` 展開後為 **58,837／25,604**：差異僅為未追蹤目錄是否展開，**不是** dirty 大幅減少。
Δ：PIPD +6 entries（25,598 → 25,604），成因未定；依規則只報事實，未做任何還原或清理。四庫 HEAD 與前輪完全相同（Fabric `765df62`、HG-KSEOS `f547425`、SBL `826ca06`、PIPD `3b48c26`），staged 皆 0。

## 6. 模型路由

- `configured／requested`：`deepseek-v4.1-flash`、provider `opencode-go`、`base_url https://opencode.ai/zen/go`、`api_mode=anthropic_messages`；Session 記錄 `billing_provider=opencode-go`。
- `actual served`：**未捕捉**。憑證存放僅有 fingerprint、無可取用之明文金鑰，且不得為取證而匯出 Token；本輪未以 `billing_config` 冒充 served → `ACTUAL_SERVED=HOLD`。
- OpenAI：無合法未到期授權可用 → `OPENAI_AUTH_HOLD`（未刷新、未複製、未輸出 Token）。

## 7. FHS 受影接線（本輪唯一新增實跑）

- `FABRIC/fabric/consumers/hgk_policy_consumer.py`：以 Python 3.11 + PyYAML 6.0.3 實跑單元測試 **5/5 OK**（重複 key／空 mapping／malformed YAML 拒絕、snapshot 不得宣稱 apply/load/ACK、未知 change class `FAIL_CLOSED`）。
- `selfcheck` 實跑：9 個 change class 全部 `ROUTE_OK` 且路由正確；`UNKNOWN_X` → `FAIL_CLOSED`。此為 **Effective Loaded／Invoked**（模組載入、真實 router YAML 由 Fabric 樹讀取、決策產生）。
- 明確限制：模組自陳 snapshot 檢查 `consumer_ack=false`、`native_acceptance=false`；本輪**沒有** Consumer ACK、HGK Admission、WorkID／Lease／PolicyEpoch／Permit、世界效果、UNKNOWN_EFFECT Reconcile 或獨立 Checker。
- 日常 Home **無原生 `fhs` profile**（僅 `hgk-governed`）；本輪未在現役 Home 新建 profile → `H01`／`H22` 維持 HOLD。

## 8. H01–H22 受影狀態（僅列本輪變動與維持項）

| ID | 前輪 | 本輪 | 說明 |
|---|---|---|---|
| H01 | HOLD | HOLD | 日常 Home 無 `fhs` profile；Desktop→fhs 未測 |
| H02 | PASS | **PASS** | 新增：關閉／重啟後同 Runtime、同一 Session 續用 |
| H05 | HOLD | HOLD | `ACTUAL_SERVED` 未捕捉 |
| H06／H07 | HOLD | HOLD | 三 Lane served 未測；錯 Provider×Model 拒絕仍沿用前輪 PASS |
| H13 | HOLD | HOLD（部分強化） | 重啟後 Session 續用 PASS；舊長 Session／效果 Reconcile 未測 |
| H15 | NOT_RUN | HOLD | 未做 GUI Model／Profile 真切換 |
| H17 | HOLD | HOLD | 無本輪原 Protected Checker 收據 |
| H20 | HOLD | HOLD（切片 PASS） | 本輪 14/14 member 還原讀回＋patch 反證 PASS；全套回退閉包未成立 |
| H21 | PASS | PASS | 受保護項 HOLD 下仍完成合法 Read／Draft 與唯讀驗證 |
| H22 | HOLD | HOLD | 無 Native 全鏈／Checker／actual-served |

其餘 H03、H04、H08–H12、H14、H16、H18、H19 狀態不變（HOLD／NOT_RUN），本輪未重跑無關情境。

## 9. 切換與回退

`CUTOVER_DONE=false`：未執行 Backend Cutover；工作列／開始功能表調整**不是**正式切換。舊版安裝、舊 Home、recovery Home 與前輪快照全部保留可回退；本輪未刪除任何版本、DB、Session 或 Stash。

回退方式（若需）：入口層＝還原兩個 `.lnk` 備份（本輪 bundle 內附）；執行層＝維持現有 recovery／舊 Home 並行，不做單檔 EXE 替換。

## 10. 未解 HOLD 與下一位責任人

| HOLD | FirstFail | Next Owner Action |
|---|---|---|
| `ENTRY_UNIFIED`（工作列） | Windows 11 拒絕程式化釘選（shell 動詞阻塞、`Taskband` 未寫入） | 使用者：開始功能表 Hermes → 右鍵「釘選到工作列」（一次），之後讀回即可 |
| `ACTUAL_SERVED` | 憑證存放僅 fingerprint；provider 回應模型未落到可讀 receiver | Provider／Credential Owner：以合法 receiver 或服務端回執取得 wire model |
| `OPENAI_AUTH_HOLD` | 無合法未到期 access-only 授權 | Credential Owner 依原程序補授權 |
| `RESTORE_SCOPE_HOLD` | 前輪 archive 本體未在本輪有界搜尋中定位；受保護 ACL／歷史成果未閉合 | 各資料／Trust Owner：先定位並核 SHA，再受影備份與還原抽驗 |
| `FHS_NATIVE_READY` | 無 HGK Permit／Consumer ACK／原生 `fhs` profile | SBL／PIPD／Fabric／HGK 原 Owner：綁 Reader、Envelope、WorkID／Lease／PolicyEpoch／Permit 後由獨立 Checker 驗收 |
| `DESKTOP_UAT`（⑤） | 僅一個日常 profile；GUI 真切換未執行 | Desktop Owner：於使用者空閒時做一次真切換 |

## 11. 復現

1. 入口讀回：`WScript.Shell.CreateShortcut()` 讀 `Desktop\Hermes.lnk`、`Start Menu\...\Hermes.lnk`，比對 TargetPath／Arguments／WorkingDirectory。
2. 重啟驗證：結束 `Hermes.exe` 程序樹 → 以 `wscript launch-desktop.vbs` 重啟 → 比對新 PID 的 `Path` 與視窗標題。
3. Session 持久化：對 profile `state.db` 以 `file:...?mode=ro` 查 `sessions`／`messages`（勿寫入）。
4. 保全還原抽驗：解壓 bundle → 逐 member `sha256` 比對 → 對 repo 執行 `git apply --check --reverse <patch>`。
5. Fabric consumer：`python -m unittest FABRIC.tests.test_b1_policy_inspection -v` 與 `python FABRIC/fabric/consumers/hgk_policy_consumer.py selfcheck`（需 PyYAML）。

本檔僅含去敏摘要；未上傳備份本體、DB／Session 內容、憑證、受保護 Evidence、私有絕對路徑或原始 provider／lane 日誌。
