# FAR 研究與最佳工程裁決 — CNV-HYGIENE-README-CLOSURE-20261016

**方法**：以上一節 A00 的實測結果為唯一輸入，對照上位藍圖控制包（PKG v2.0.0）與外部獨立驗收報告
（EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016）逐條偏離分析；每個選項附『低阻力／高可行／高必要性』三項
評級、對齊論證與回復方式。凡列 NOT_NOW／OWNER_GATED 者為具名延後，不是遺漏。

## 本輪裁決即執行（Tier A）

| ID | 主題 | 裁決 | 阻力 | 可行 | 必要性 |
|---|---|---|---|---|---|
| R1 | REPO_HOMEPAGE_README | 重寫 root README.md 成為外部入口（單一檔） | LOW | HIGH | HIGH |
| R5 | REPO_HYGIENE_BRANCHES | 逐一驗證後刪除已合併的遠端 evidence/pub/docs 分支 | LOW | HIGH | HIGH |
| R7 | LOCAL_HYGIENE_NONDESTRUCTIVE | 非破壞性衛生：自我修補譜系合併 + 16 個 handover 目錄索引 | LOW | HIGH | HIGH |
| R8 | GOVERNANCE_TRACE | 以 errata 記錄已發布 OpenSpec 變更記錄中未回填的 `[ ]`（不重寫歷史） | LOW | HIGH | HIGH |
| R9 | SESSION_CLOSURE | 產出 session 結案與移交文件 + resume pointer | LOW | HIGH | HIGH |

## 具名延後／owner-gated

| ID | 處置 | 標的 | 理由 |
|---|---|---|---|
| R2 | `CONSIDERED_AND_REJECTED` | 不新增第二個 root 入口文件（不加 MAIN.md） | 報告 §8 與 KP 反覆要求『不得建立第二個控制平面／第二套 manifest 架構』。新增 MAIN.md 會製造與 HG-KSEOS canonical 文件競爭的第二份目錄，屬於過度工程化。 |
| R3 | `OWNER_GATED` | 本輪不新增 LICENSE 檔案 | 授權是 owner/法務決定，不是工程衛生裁決；擅自選定條款會創造本輪無權承擔的外部承諾。 |
| R4 | `DEFERRED_ALIGNED_WITH_EIA_019_10` | 本輪不建立 .github/workflows | 新增 workflow 會改變本輪變更類別並引入自動執行面，正是報告禁止『未審 hook/workflow』的方向；驗收報告本身只要求揭露，不要求補 CI。 |
| R6 | `OWNER_GATED_WITH_TABLE` | 本機破壞性清理（DB 副本、worktree、junk dirs）列 owner-gated，不在本輪執行 | spine DB 副本與 worktree 是本會話各輪的證據與回復點；本輪授權範圍是 REPO 與 session 結案，不包含刪除本機證據。破壞性動作留給 owner 是誠實的邊界，而非推託。 |
| R10 | `OWNER_GATED` | PR #15 的處置保留給 owner（不自行合併） | 合併自己輪次的返證包等於自我接受；報告 §7 明示 maker 不得自簽 AO/Release。 |
| R11 | `CONSIDERED_AND_REJECTED` | 不改 repo metadata（topics／homepage） | 上級文件未要求，且 metadata 變更不在本輪變更類別的證據面內；非必要不做（避免非必要表面變動）。 |

## 逐項偏離分析

### R1 — 重寫 root README.md 成為外部入口（單一檔）（REPO_HOMEPAGE_README）
- 對應發現：HY-01, HY-02
- 實測：root 只有 README.md(4732 B) 與 .gitignore；README 早於現行治理契約，無 evidence 前綴地圖、無 claim ceiling、無 PR 索引、無非宣稱區
- 動作：以受治理 bounded writer 車道重寫 /README.md：repo 定位（HG-KSEOS 為唯一控制平面、Hermes 為受治理 Runtime/Orchestration Plane）、EVIDENCE 前綴地圖、PR #3..#15 索引與 merge SHA、外部團隊閱讀順序、以及明確非宣稱框（NO_VERDICTS_FOUND／TIMEOUT／同模型軸／candidate-only／無 LICENSE／無 CI）。
- 評級：阻力 LOW／可行 HIGH／必要性 HIGH
- 對齊論證：外部工程團隊的參照入口就是 repo 首頁；目前首頁讀不出治理結構與宣稱上限，正是驗收報告要求『不得以合併代替 AO/production』時最容易被誤讀的一頁。一個檔案、無新架構。
- 本輪處置：已執行
- 回復：以 revert 本輪 PR 的該檔 commit 還原（原 README 的 blob sha 9dd1946c3a7c9c76089c814b7ec75c46ab1210b2 已記錄）

### R2 — 不新增第二個 root 入口文件（不加 MAIN.md）（REPO_HOMEPAGE_MAIN）
- 對應發現：HY-02
- 實測：root 目前只有 .gitignore 與 README.md；repo metadata 顯示 default_branch=main、has_wiki=false、has_pages=false、topics=[]、homepage=null
- 動作：維持單一入口：README.md 即首頁索引，不建立 MAIN.md 或第二套索引架構。
- 評級：阻力 NONE／可行 HIGH／必要性 HIGH
- 對齊論證：報告 §8 與 KP 反覆要求『不得建立第二個控制平面／第二套 manifest 架構』。新增 MAIN.md 會製造與 HG-KSEOS canonical 文件競爭的第二份目錄，屬於過度工程化。
- 本輪處置：`CONSIDERED_AND_REJECTED`
- 回復：n/a

### R3 — 本輪不新增 LICENSE 檔案（REPO_LICENSE）
- 對應發現：HY-01
- 實測：GET /license 回報無授權檔（root 僅 .gitignore、README.md）
- 動作：不代替 owner 決定授權條款；列為 owner-gated 決策，附最小動作（新增 LICENSE + 於 README 標示）。
- 評級：阻力 LOW／可行 HIGH／必要性 MEDIUM
- 對齊論證：授權是 owner/法務決定，不是工程衛生裁決；擅自選定條款會創造本輪無權承擔的外部承諾。
- 本輪處置：`OWNER_GATED`
- 回復：n/a

### R4 — 本輪不建立 .github/workflows（REPO_CI）
- 對應發現：HY-03
- 實測：repo tree 內 0 個 workflow 檔；報告 EIA-019-10 已將『無 GitHub CI status』列為 NON_BLOCKING_OBSERVATION 並說『不可聲稱 CI PASS』
- 動作：維持無 CI；不新增 workflow。若未來要自動發布，另立窄 Gate 與變更類別。
- 評級：阻力 LOW／可行 HIGH／必要性 LOW
- 對齊論證：新增 workflow 會改變本輪變更類別並引入自動執行面，正是報告禁止『未審 hook/workflow』的方向；驗收報告本身只要求揭露，不要求補 CI。
- 本輪處置：`DEFERRED_ALIGNED_WITH_EIA_019_10`
- 回復：n/a

### R5 — 逐一驗證後刪除已合併的遠端 evidence/pub/docs 分支（REPO_HYGIENE_BRANCHES）
- 對應發現：HY-04
- 實測：17 個遠端分支中，11 個 evidence/* 分支的 PR 已合併（#3..#14），另有 pub/*、docs/* 分支；唯一未合併的是本輪之前的 evidence/cnv-far018-far019-archive（PR #15 仍 open）
- 動作：對每個分支先以 /pulls?state=all&head= 驗證其 PR 已 merged；已合併者記錄 tip SHA 後刪除 ref（可逆：以 SHA 重建 ref）；PR 仍 open 或無 PR 者一律保留。
- 評級：阻力 LOW／可行 HIGH／必要性 HIGH
- 對齊論證：分支清單是外部團隊最先看到的『未完成訊號』；11 個已完成分支留在遠端會讓已結案的 archive 階段看起來仍在進行。刪除不影響 main 的證據（合併提交已在 main），且每筆都有 SHA 可還原。
- 本輪處置：已執行
- 回復：POST /git/refs 以記錄的 tip SHA 重建該分支

### R6 — 本機破壞性清理（DB 副本、worktree、junk dirs）列 owner-gated，不在本輪執行（LOCAL_HYGIENE_DESTRUCTIVE）
- 對應發現：HY-07-hgk_control, HY-08-hgk_control, HY-09-hgk_control, HY-07-fabric_clone, HY-09-fabric_clone
- 實測：HG-KSEOS：283 筆 dirty、20 個 worktree、var 下 4 份約 823 MB 與 1 份約 793 MB spine DB 副本、多份 297-334 MB 巢狀 codex.exe、1 個 326 MB 安裝檔；Fabric clone 在舊分支、8 個 worktree、5 個 >5 MB 檔（含重複 vendored PDF）
- 動作：只產出 owner-gated 候選表（路徑、大小、為何具破壞性、精確且安全的最小指令），不執行任何刪除。
- 評級：阻力 LOW／可行 HIGH／必要性 MEDIUM
- 對齊論證：spine DB 副本與 worktree 是本會話各輪的證據與回復點；本輪授權範圍是 REPO 與 session 結案，不包含刪除本機證據。破壞性動作留給 owner 是誠實的邊界，而非推託。
- 本輪處置：`OWNER_GATED_WITH_TABLE`
- 回復：n/a

### R7 — 非破壞性衛生：自我修補譜系合併 + 16 個 handover 目錄索引（LOCAL_HYGIENE_NONDESTRUCTIVE）
- 對應發現：HY-10, HY-11
- 實測：上一輪遺留 ['fix_self_check_defects.py'] 等 3 支修補腳本；_handover 下累積 16 個輪次目錄且無索引
- 動作：① 產出一份 SELF_CHECK_REPAIR_LOG.md 記錄三次 harness 修補的譜系（保留原腳本為證據，不刪）；② 產出 _handover/INDEX.md 列出 16 個輪次目錄、其 verdict 與 claim ceiling 與該讀什麼。
- 評級：阻力 LOW／可行 HIGH／必要性 HIGH
- 對齊論證：移交品質取決於『下一個人知道去哪裡讀什麼』；這是本輪任務明文要求的結案/移交事項，且完全不動既有證據檔。
- 本輪處置：已執行
- 回復：刪除本輪新增的兩個 md 即可；不觸及任何既有檔

### R8 — 以 errata 記錄已發布 OpenSpec 變更記錄中未回填的 `[ ]`（不重寫歷史）（GOVERNANCE_TRACE）
- 對應發現：HY-10
- 實測：上一輪發布的 openspec_change/tasks.md 內 3.3/3.4/4.1/4.2 四項在交付時仍為 `[ ]`，實際工作已完成
- 動作：在本輪 ERRATA 具名記錄（計畫清單未在證據 commit 前回填＝痕跡與事實不符），並確保本輪的 OpenSpec 記錄在發布前 0 個殘留 `[ ]`。
- 評級：阻力 LOW／可行 HIGH／必要性 HIGH
- 對齊論證：治理可信度建立在痕跡與事實一致；已發布的變更記錄屬不可改寫證據，正確處置是 errata 而非回改。
- 本輪處置：已執行
- 回復：errata 為新增檔，刪除即回復

### R9 — 產出 session 結案與移交文件 + resume pointer（SESSION_CLOSURE）
- 對應發現：HY-11
- 實測：本會話已完成 FAR-018／FAR-019／archive 三輪；archive 輪 verdict=ARCHIVE_MERGED_READBACK_PASS （逐支）、self-check 12/12、PR #15 仍 open
- 動作：HANDOVER_SESSION_20261016.md：逐輪 verdict 與 claim ceiling、未宣稱清單、open items 與 owner、resume pointer（控制平面、輪次目錄、可直接沿用的 id）、以及不可重做的事項。
- 評級：阻力 LOW／可行 HIGH／必要性 HIGH
- 對齊論證：任務明文要求『對本 SESSION 進行結案/移送的相關事項』研究；沒有移交文件的結案等於下一輪必須重新推導全部狀態。
- 本輪處置：已執行
- 回復：文件為新增檔

### R10 — PR #15 的處置保留給 owner（不自行合併）（SESSION_CLOSURE）
- 對應發現：HY-05
- 實測：PR #15 為本會話 archive 輪的返證包（31 檔、非 draft、branch tip a22ad7e17559），未合併
- 動作：只提出建議與理由，不合併：由 owner 決定以一般 merge 收入 main 或退回。
- 評級：阻力 NONE／可行 HIGH／必要性 HIGH
- 對齊論證：合併自己輪次的返證包等於自我接受；報告 §7 明示 maker 不得自簽 AO/Release。
- 本輪處置：`OWNER_GATED`
- 回復：n/a

### R11 — 不改 repo metadata（topics／homepage）（REPO_METADATA）
- 對應發現：HY-01
- 實測：topics=[]、homepage=null、description 已準確描述治理定位
- 動作：不動。
- 評級：阻力 LOW／可行 HIGH／必要性 LOW
- 對齊論證：上級文件未要求，且 metadata 變更不在本輪變更類別的證據面內；非必要不做（避免非必要表面變動）。
- 本輪處置：`CONSIDERED_AND_REJECTED`
- 回復：n/a

## 上限

本裁決為工程決策記錄，`claim_ceiling = LOCAL`；不構成驗收、核准或任何 Gate，也不改變 `canonical_AO=NOT_ISSUED`／`production=FAIL_CLOSED`。
