# FSDT-Stack DOC 系列 + TW-ICT v3.0 DOC-05：方法流程與當沖技術定位

用於 HG-KSEOS 下 SQS-THC / FSDT-Stack 的 FAR 唯讀研究子任務，目標是**方法/MethodSpec 制定流程**與**當沖/ICT 技術參考**。
姊妹檔：`sqs-thc-knowledge-base-research.md`（RBWI + Spartoi 家族：MethodCard/MethodSpec 差異、兩種 markdown 結構、JSON 產出契約）。本檔補 FSDT-Stack DOC 系列與 TW-ICT v3.0 DOC-05。

## 檔案實體位置（很重要，任務給的路徑常是錯的）

- 知識庫根：`C:\Projects\Agent_Workspace\知識庫\`
- FSDT-Stack 家族：`知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\TW-ICT_FSDT-Stack_專業技術文檔\` → 檔案 `TW-ICT_FSDT-Stack_專業技術文檔_DOC-NN_2026-07-31_rN.md`（DOC-00..29）。（SSOT 根同層還有 SQS-THC_工程開發文檔、TW-ICT_FSDT-Stack_藍圖、TW-ICT_RBWI_v3.0.0 等。）
- TW-ICT v3.0 家族：`知識庫\SQS-THC資料庫\TW-ICT_v3.0_專業技術文檔\` → `TW-ICT_專業技術文檔_v3.0_DOC-NN_...r2.md`（DOC-00..11）。
- 另有鏡像重複副本在 `C:\Projects\專業技術文檔\STOCK\TW-ICT\...`；兩家族同名檔會重複出現，用「家族根目錄」指到正確那套。

**發現技巧（本任務踩過）：** 若任務把路徑寫成 `C:\Users\user\...\TW-ICT_...`，那多半是錯的（真實文件在 `.txt` 之外另有 `C:\Projects\...` 根）。`find /c/Users -iname "*TW-ICT*"` 常空手。可靠正解：對 `C:\Projects` 做 `find ... -type d \( -iname "*SQS-THC*" -o -iname "*TW-ICT_v3.0*" -o -iname "*FSDT*" \)`，或用「執行超時後 cwd 被 echo 出來」的技巧揪出真實根（之前的一次 terminal timeout 在 cwd 欄洩漏了 `C:\Projects\Agent_Workspace\知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\...`）。

## DOC 分工地圖（先定位再深讀，別掃全文）

| 檔 | 角色 | 方法/當沖關鍵位（本次驗證 L 號） |
|---|---|---|
| FSDT-Stack **DOC-29**（r2, 14813 行） | 工具/元件/資格（Tool Qualification）：named item → disposition → qualification/benchmark/exit | 方法/當沖來源跨鑑定：L174-176（SC-D29-040/041，`Spartoi RUNBOOK&WI v2.0.0` = ADOPT_DOC29_SUPPORT）；L685/689/857（ICT 1~107 法律地位 = METHOD/TA/TRANSLATE legacy corpus）；L1543-1592（CH-D29-29 Spartoi/SEM8/SEM³/AgentOS = legacy donor，不得回任 SSOT）；L5270-5420（ITEM-215..224，TRADING_METHOD_OR_FEATURE_SPEC 一律 ROUTE_OUT 給 D03/D04/G04） |
| FSDT-Stack **DOC-27**（r2） | Evidence/NRTV 保證：Body→Evidence→NRTV→Release→Package→Drift 正交狀態面；35 Obj/21 SPEC/20 WF | L36-49（Exec Verdict / Claim Ceiling，禁未驗證 NRTV_PASS）；L1678-1700（D27-19 NRTV Question Bank 由 source-obligation 導出） |
| FSDT-Stack **DOC-28**（r2） | 成本/流動性/容量/組合(TCA) + 具名工具表 | L3652-4032（CH-23A 防降級表：NumPy/SciPy/pandas…工程工具，無交易權威）；L2728（CH-20 components） |
| FSDT-Stack **DOC-14**（r3, 9318 行） | **MethodSpec 定案流程的 Canonical 家**（S5 營運、Slow/Fast Loop + JobCard） | L77/L190（SOP 週期 review→change→獨立檢查→影響分析→批准/effective→每日 freeze→盤中 admission）；L949（「直接改 MethodSpec…Fast/Slow Loop 穿透 → Kill session 並建立 Engineering/Method Change」⇒ 方法定案在 Slow Loop，盤中不得改）；L301（JobCard spec） |
| FSDT-Stack **DOC-20** | MethodSpec 密集（59 次引用）；與 DOC-05（v3.0）ORIGIN parallelism | 方法/物件 Spec 第二密集家（DOC-14 162 次、DOC-20 59 次最密） |
| TW-ICT v3.0 **DOC-05**（r2, 8040 行） | **方法執行鏈**：Universe→Candidate→MTF Bias→五分支 Scenario→TradeHypothesis | L53-69（Executive Synthesis compile chain）；L85-281（32 donor→16 capsule source-to-prose，即方法採納/對齊上游）；L2986-3016（CH-11.6 SOP + CH-11.7 一級技術）；L3034（CH-12.4 state path）；L4463-4494（CH-12.6 SOP + CH-12.7 一級技術） |

## 三問速答（本子任務的結論模板）

1. **是否有方法/策略制定流程？** 是，但分散：上游採納 = v3.0 DOC-05（32-donor→16-capsule）；執行鏈 = DOC-05 CH-11/CH-12；真值/定案 owner = D03/D04/G04 與 CA-METHOD（DOC-29 只 route-out，方法卡現為 `PLACEHOLDER_PENDING_CA_METHOD`）；MethodSpec 最終定案 = DOC-14 Slow-Loop Method Change + 批准 gate + 每日 freeze。
2. **當沖技術（ICT 模組 #1-#107）規範？** DOC-29 明文：ICT 1~107 = `METHOD / TA / TRANSLATE` 的 **legacy semantic corpus + calibration reference**，**不拆成 107 個 owner 模組**（L689/L857）。v3.0 DOC-05 CH-11.7/CH-12.7 列出第一級當沖/ICT 技術（Full-market Denominator、Rule/Data/Eligibility gate、MTF Responsibility Mapping、Dealing Range、Daily/Weekly Bias、SMT、Relative Strength、Correlation Regime、五分支 ScenarioTree、Branch Switch、PO3/AMD/Profile、TradeHypothesis）。DOC-29 引用之當沖原文料：ICT台股當沖流程總表 v1.7.0、細部手冊v2、藍圖v2.3.0、當沖流程框架_1014、OBI v3.1、Spartoi RUNBOOK&WI v2.0.0、Spartoi P1執行手冊 v2.1.0、TW-ICT_RBWI_v3.0.0。
3. **明文指向 Spartoi/SQS 用哪些技術？** DOC-29 CH-D29-29 將 Spartoi/SEM8/SEM³/AgentOS 拆解為 legacy donor/reusable procedure/alias，**不得回任 global SSOT 或 policy brain**；未單獨授權技術，方法權威全部 route-out。

## 易踩雷
- **別把所有 DOC 當成「方法正文」**：DOC-29 是工具資格、DOC-28 是成本/組合/TCA，方法/當沖真值在 v3.0 DOC-05 與 DOC-14（S5 營運）。任務若點名 DOC-29 為「方法密集」，指的是它對當沖來源的 cross-DOC 鑑定與 route-out，不是它定義方法。
- **DOC 檔案極大（0.2–1.4MB）**：一律 `grep -nE "^# CH|^## CH|MethodSpec|定案|ICT 1~107|PLACEHOLDER_PENDING"` 圈行號，再 `read_file offset=` 精讀；`.state path`、`ITC ITEM-###`、`SC-D29-###`、`XR-D29-###` 是定位錨。
- 產出契約同姊妹檔：JSON `{source_family, findings[], has_method_workflow, has_daytrading_reference, summary, quote_locations}`，quote_locations 附「檔 + L行號段」；outcome-first，不 replay 過程。
