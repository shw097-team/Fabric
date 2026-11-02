# UPGRADE_RETURN — Hermes Windows Desktop／FHS 保全候選

2026-11-02（Asia/Taipei）。**最高安全狀態：既有最新版 Desktop 可從桌面開啟，一次真實 Go 對話 PASS；FHS Read/Draft 已跑。完整產品驗收尚未完成。**

`SHADOW_QUALIFIED=HOLD` · `NATIVE_E2E=HOLD` · `CUTOVER_DONE=false` · `PRODUCT_DELIVERY_COMPLETE=false`。本次未重做 M0–M4、未建第二份 Shadow、未啟動新全量封存。以下 PASS 均限明示的本地切片，沒有獨立 Checker/Release 宣告。

## 1. 身份、正常入口及真實 GUI 驗收

| 元件 | 精確身份／讀回 | 結論 |
|---|---|---|
| 原舊 Source/Desktop | `f97608f178d1ffeca59860195ab7da295f7c8e5f`；source tag `v2026.9.24`、pyproject `0.21.5`；GUI 曾顯示 `v0.21.5 (+19514)` | 原件保留；工作列舊圖示仍啟動這份 |
| 既有 recovery h22 | `bf0203a794a07aac3ff764972ab9087baa4e4f4e`，Runtime `0.22.5` | 直接復用，未重裝 |
| recovery Desktop | install-stamp 同一完整 SHA、dirty=false、local/bootstrap；EXE/package `0.0.0` | 以 stamp/runtime 辨識；不是另行驗證過的 Store/MSIX 正式包 |
| Shadow | 同一官方 Stable SHA、原生 `fhs`、官方隔離 developer setup；Python `3.14.9`、OpenAI SDK `2.24.0` | 獨立 Home/UV/工具/埠，測試後停止 |
| 系統工具 | Node `v24.19.0` | 不將此值冒充 recovery 的選中 Python 或 PM Node |

官方已發布最新 Stable 為 [v0.22.5](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5)，解參照 SHA 如上；annotated tag object `56b6a31fededdf7364e1a0a79548d144e7fd81a3`。版本核對沿用本輪已完成結果。

- **實際 Windows 操作 PASS**：透過 File Explorer 雙擊正常桌面 Hermes 捷徑，窗口實際來自 recovery Desktop；Backend 就緒，建立新對話、只送一次合成 nonce、收到精確回覆。持久 Session 讀回：default、`deepseek-v4.1-flash`、billing_provider=`opencode-go`、1 API call、0 tool calls、15352 input/13 output tokens。沒有點擊或重播舊工作。
- **入口混淆已釐清**：期間另出現舊 Desktop。使用者明確確認是自行點擊工作列舊圖示，並確認桌面捷徑可正常開新版；不是新版自行降版。最後只讀 GUI 版本顯示 `v0.22.5`。本任務未修改任何捷徑、工作列釘選或關閉使用者視窗。
- 原歷史 Session 清單可見，設定頁可見 default/hgk-governed 與 Go 模型。這不等於舊 Session 內容、Skills GUI、真 Profile/Model 切換或重登/重啟全部通過；這些仍 NOT_RUN/HOLD。recovery 實際選中 Python 版本尚未完整綁定收據。
- **Go 金鑰依使用者指定檔案**：記憶體中核對既有 recovery/old key 相同；未改原憑證。GUI 有真回覆與持久 usage，未捕捉服務端 wire model，故 requested/selected 不能當成 **actual served** 證明。Shadow 的 Go 路由仍是另一個 HOLD。

## 2. Gateway／Home／派工與原成果保留

既有只讀快照：舊 Gateway child PID 6096、埠 4976；recovery PID 16952、HTTP 4971/另埠 4975，status=`0.22.5`/running；Shadow 測試後 active=0。PID/埠為時間點快照，不保證後續長存。非 HTTP 埠 BadStatusLine 不作服務失效判定。

舊 MSIX 虛擬路徑與 local-default alias 的 state.db 是同一檔；old、recovery、Shadow 的已檢查 state.db 非同一檔。其他具名 kanban/projects/shared-state DB 的存在項也分離；缺檔不算 PASS。曾有新舊 Desktop 都使用 recovery desktop-state 的程序觀察，故不宣稱全部 UI 狀態完全無共用。未更動該設定。

原 Cron default 4/3 enabled、governed 1/0；recovery 3/0，三個 job ID 跨 Home 重複但 recovery 全停用，快照未見同 ID 雙邊 enabled。外部平台輪詢/重複世界效果仍未排除；原 Current Work Reader 尚未為本次綁 WorkID/Lease/PolicyEpoch/Permit。未停現役 Gateway、未 replay UNKNOWN_EFFECT。

四庫本機原 HEAD（不以遠端 main 代替）與五份原 config SHA 末次讀回未變；四庫 staged=0。原舊 Hermes 三個 tracked 修改均與獨立捕捉副本同 bytes；recovery/Shadow Source clean。本任務無四庫核心或現役 Source 寫入。初始 SBL 曾列 4 個修改、末次 diff=0，未歸因且初始 dirty bytes 未全部凍結，因此**不宣稱完整工作樹逐位元保全**。另已針對當初具名 9 檔和當下 patches/indices 做小型保全。

| 庫 | 原本機 HEAD | 本機 Branch | 初始 status entries | local-only（cached refs） | worktrees |
|---|---|---|---:|---:|---:|
| Fabric | `765df6289cfb7730aa56efbd522d76df6ec9809a` | `far/far-031-fhs-msc-all-pass-20261031` | 8 | 37 | 11 |
| HG-KSEOS | `f5474257aa7d2005937867340f4cd01b39751129` | `candidate/r18-fhs-skeleton-spine-20261029` | 2 | 19 | 28 |
| SBL | `826ca066a1c2df2976c0d402018b79e1c79a444f` | `candidate/r14-ts15-kinds` | 58837 | 4 | 10 |
| PIPD | `3b48c262f4174217cb35391c6da22bc53f068755` | `candidate/r21-far-20261101` | 25598 | 3 | 16 |

初始 Stash 均 0，未清除。初始 status 首列曾 trim 空白，不從其極性推論 staged；詳值沿用私有基準。任務寫入限工作區 helpers/evidence、隔離 Shadow、候選 clone、輸出，以及官方 backup lock 和授權 GUI 新測試 Session；正常使用中的 DB 不宣稱 bytes 不變。原 B1/R20/R21/v1 證據未歸零或改標新版驗收。

## 3. M1 保全收尾與還原

- 官方 current 第二輪與 recovery Home backup 完整且 ZIP CRC 通過；current 首輪遇消失 Cron 檔不完整，保留但不當成功。Fabric、PIPD、兩份 Source、Launcher 封存按既定排除範圍完成；SHA/尺寸見 `MANIFEST.json`。含排除項的 complete 只指該捕捉範圍。
- **SBL 為中斷的部分封存**：218537 已捕捉成員；僅 append 中央目錄安全收尾，原前綴不變，36 個未綁/不完整項未索引；未重開全量備份。HGK 280827 已捕捉檔案仍有 scan 缺口。沒有進行中的本任務全量封存。
- 11 份 receipt 對應 ZIP 目錄與代表 CRC 讀取通過；這不是所有 archive 全 CRC 或完整還原。隔離 recovery SQLite integrity PASS，917 Sessions/172887 Messages；官方 SessionDB 真讀回 86 則訊息。隔離 Fabric Git HEAD 與代表 blob 還原 PASS；nested worktree 絕對接線/未追蹤呈現不同，不能稱全機還原。
- **拒絕存取只分類一次，不重掃**：HGK 975＝922 關鍵/未釐清歷史成果＋53 原 Owner 受保護資料；SBL 4＝1 可重建 cache 候選＋3 受保護 Checker 資料。分類不等於可刪除、可忽略或缺口已關閉。
- **M1 整體 HOLD**：SBL 中斷範圍、上述 ACL/歷史成果、原 Owner Trust/金鑰、外部 worktree 未提交成果、庫外全部 Evidence 與 dirty-baseline 尚未形成完整可回復閉包。不得據此正式覆寫/切換。備份本體與拒絕路徑只留本機。

## 4. 最小實跑、差額與路由

1. 原生隔離 Backend 五項 PASS：fhs 身份、Session idempotent create、錯 Provider×Model 拒絕、不同 Backend PID 用 stored_session_id Resume、新/不存在 Session 邊界。Resume 用新建空白測試 Session，非大型舊 Session。只停止自己的測試程序樹。
2. 原 SBL M01/M02 →3 atoms、原 PIPD PI→4 atoms/PD 綁真 fixture Git HEAD、三份 Product/System/Program Draft SPEC；原 Fabric transient/upgrade/unknown 與缺 Native ACK、缺 RepoContext、FRESH/stale HEAD 負例，共 10 個本地檢查 PASS。沒有原 Reader ACK、durable Queue/Permit 或 Native 世界效果。
3. **Shadow Go HOLD 且停止重試**：選定 Anthropic SDK 的 262 字元模組普通路徑不存在、extended path 存在。最後一輪只用 task-local junction 指向同一 pinned SDK；短路徑直接 import PASS，但 native AIAgent 仍 ImportError、wire/actual-served 空。未換 endpoint、未繞安全審查或增加修補輪次。GUI recovery 成功不替代 Shadow 正例。
4. **OpenAI HOLD**：未取得可不刷新原憑證的合法未到期 access-only 授權；本輪最後測試未讀取/刷新它，未真呼叫。外部載荷審查曾拒絕傳送本機 Skill；該動作未執行。後獲准的 Shadow nonce 測試不含本機 Skill/文件/記憶/工具資料。
5. 原 Fabric Consumer 已有 root discovery，無需再改；本機 PIPD COMMANDS=14（含 repair）與文件 13 有差額；選定 SBL 分支缺當期 harness/stack，僅直接 core 可跑；HGK 靜態 resolver import/Lane registry epoch 40 不是 Active Served/Native PolicyEpoch。本次沒有建第二個 Issuer/Policy/Queue/Checker。

## 5. H01–H22 受影對應

沿用原 H ID；PASS 限明示切片，未重跑無關完整原分母，HOLD 不自簽。

| ID | 狀態 | 證據層級／缺口 |
|---|---|---|
| H01 | HOLD | 原生 fhs Backend 身份 PASS；GUI recovery/default PASS；Desktop→fhs 未測 |
| H02 | PASS | 隔離 Backend 啟動；既有新版 Desktop 真啟動及單次對話，限此切片 |
| H03 | HOLD | 原 Skill 位元同一且 native skill_view 真載入；Startup 自動觸發未測 |
| H04 | HOLD | r2 副本同 SHA；原 Reader 對本次 v2 Source 採納未綁 |
| H05 | HOLD | GUI 選用 Go model 並有 usage/回覆；服務端實際模型身份未捕捉 |
| H06 | HOLD | 原三 Lane actual-served 未測 |
| H07 | HOLD | 錯 Provider×Model 拒絕 PASS；GUI Go 正例 PASS；Shadow Go/OpenAI HOLD |
| H08 | HOLD | 原生 Session 建立/持久 ID PASS；原 durable Goal Queue ACK 未證 |
| H09 | HOLD | 原 SBL/PIPD 真編譯 PI/PD 和三份 Draft SPEC；原 Owner/Reader ACK 未證 |
| H10 | HOLD | 原 Fabric 分流正反例 PASS；Active→Loaded→Consumed/Native 准入未證 |
| H11 | HOLD | 缺本次原 Owner Envelope/Permit；未自簽 |
| H12 | NOT_RUN | 未執行受原 HGK Permit 管控的世界效果 |
| H13 | HOLD | 新空白測試 Session Backend 重啟 Resume PASS；舊 Session/效果 Reconcile 未測 |
| H14 | NOT_RUN | 多 Session 競爭與 WorkID 隔離未測 |
| H15 | NOT_RUN | 真切換正式 Profile/Model 未測；設定頁選項可見而已 |
| H16 | HOLD | 缺 Native ACK 拒絕 PASS；完整 Injection/YOLO 未測 |
| H17 | HOLD | 無本次原 Protected Checker 收據 |
| H18 | HOLD | Skill copy/load/view PASS；Plugin ConsumerUsed 未證 |
| H19 | HOLD | Session idempotency retry 去重 PASS；原 Grant/Settlement/UNKNOWN_EFFECT 未重測 |
| H20 | HOLD | Git HEAD/blob、SQLite/Session 還原抽驗 PASS；全套回退保全未閉合 |
| H21 | PASS | 受保護項 HOLD 時仍完成合法 Read/Draft SPEC/PI/PD |
| H22 | HOLD | 本次無原 Native 全鏈/Checker/actual-served 完整證據 |

## 6. 切換、回退及外部團隊下一步

**M9 Cutover NOT_RUN**：桌面入口原本已指向既有 recovery Stable，這次是復用/驗證，沒有把它冒稱本任務正式切換。未停止舊 Gateway、未更動 Issuer/Trust Root、未代簽、未合併或 Release。保全與原合法 Gate 未齊，完整產品交付仍 HOLD。

| Blocker | FirstFail／後續作業 | 原責任 |
|---|---|---|
| RESTORE_SCOPE_HOLD | 補受保護 ACL/歷史成果、SBL 部分封存及外部 worktree；先受影範圍備份並抽驗可還原，避免新無界全量作業 | 各資料/Trust Owner |
| SHADOW_GO_HOLD | 保留本輪 ImportError/SDK generation 診斷；最後一輪已用完，不在此重試 | Hermes Host Owner |
| ACTUAL_SERVED_HOLD / OPENAI_ACCESS_HOLD | 以合法既有 receiver/credential 程序取得 wire/deployment model 與 OpenAI 測試授權；不改標 billing/config 為 served | Provider/Credential Owner |
| DESKTOP_UAT_HOLD | 使用者空閒時驗真 Model/Profile 切換、舊 Session/Skills 適用讀回、重啟後同一 Runtime；恢復兩條入口的明確標示/釘選另做授權變更 | Desktop Owner |
| NATIVE_CHECKER_HOLD | 綁原 Source Reader、Owner Envelope、WorkID/Lease/PolicyEpoch/Permit/Consumer；原獨立 Checker 依 subject-bound evidence 驗收 | SBL/PIPD/Fabric/HGK 原 Owner/Checker |

正式切換只能在上述必要 Gate、原合法核准與可回退成立後：先原 Current Work Reader 處理在途/UNKNOWN_EFFECT，再做 Canary 與 Gateway/Profile/Model/Consumer 讀回。若須降版，恢復相容的整套 Runtime+DB 快照，外部效果依原 ECP Reconcile；不能只換 EXE 或盲重播。現有舊 Source/Home 與快照保留，但全套回退合格仍 HOLD。

## 7. GitHub 交付與復現

僅 Fabric [候選分支](https://github.com/shw097-team/Fabric/tree/candidate/hermes-stable-shadow-20261102) 新增這份去敏報告、manifest/test summary、reproducer 和索引。四庫核心程式差額=0；其他庫只連結：[HG-KSEOS](https://github.com/shw097-team/HG-KSEOS)、[SBL](https://github.com/shw097-team/SBL)、[PIPD-LS-SP](https://github.com/shw097-team/PIPD-LS-SP)，無空提交。

`TEST_RESULTS.json` 含實跑切片與限制；`MANIFEST.json` 含來源/版本/備份及公開 payload SHA。公開 `REPRODUCE.ps1`/`SMOKE_BACKEND.py` 只供新的隔離目錄重現 upstream Backend 契約，已做語法檢查，未把腳本另稱本輪獨立重跑。原四庫實跑須各自合法 RepoContext；它們不是原 Native Receiver 的公開替身。

推送前依原 AGENTS 做一次 exact-staged 機密/path 掃描、diff 與 remote/branch 權限驗證；正常 push 後建立 Draft PR 並讀回 commit/PR。實際 publication receipt 另附本機交付，不預稱發布成功。備份、Profile/DB 本體、憑證、敏感 WorkID/路徑、原 Session 內容/畫面、raw provider/lane logs 不公開。
