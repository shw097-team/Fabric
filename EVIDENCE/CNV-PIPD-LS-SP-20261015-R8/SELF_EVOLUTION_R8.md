# 受 FABRIC × HGK 治理的自我研究／學習／迭代／進化 — R8-0 回合

Mission `CNV-PIPD-LS-SP-20261015` · ChangeSet `R8-0` · 產出於 2026-10-16
權威：`Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` v2.0.0、`HG-KSEOS/AGENTS.md`（控制平面規則）、
`Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md`
機器可讀版本：`SELF_EVOLUTION_R8.json`（25 條，含 owner／gate／證據路徑）
Claim ceiling：**LOCAL / candidate-only**。本檔不是驗收、不是批准、不是閘門 PASS、不是政策變更；每一條都可被其引用的證據路徑否證。

## 0. 方法與界限
本檔是**執行者自己**對本回合的治理性回顧，因此**不是對自身的獨立審查**——獨立裁決由 VERIFY 車道（`R8_VERIFY/`）與外部驗收官產出。原則：**先重跑該結論自己的檢查，再寫工作單**；沒有原始輸出的結論不寫進這裡。

## 1. 自研究（本回合用原始證據換到的知識）
| id | 問題 | 方法 | 結果 |
|---|---|---|---|
| SR-1 | 九條外部 finding 哪些仍成立？ | 逐條以其自身反例重測（GitHub tree/manifest 集合差、ACL 讀取、變異重測、技能庫掃描） | 06 本地閉合；01/02 收斂為「2 個未發佈快取路徑」；03 找到根因；04 在 main 上反例已關；05/07/08 確認需 owner/授權；09 已量測處理中 |
| SR-2 | 受守護主體是否仍等於已發佈內容？ | 300 檔逐一比對 git blob sha1 vs 合併 packet `b8ff8104` | **300/300 逐位元相同**，0 mismatch |
| SR-3 | R6 packet 宣告集與實到集是否相等？ | tree API blob 集合 vs manifest `files[]` | 不等：**583 宣告 / 581 實到**，兩個多餘項皆為 `__pycache__` `.pyc` → 由未知變成**已定位** |
| SR-4 | 瘦身候選是否真的無損？ | 六項回歸閘（含 references 覆蓋） | AVR 候選兩處缺陷→修補→上線→無損驗證通過；**HGK 候選不可上線**（2 份 reference 原文消失） |
| SR-5 | 受守護主體有無 OS 層保護？ | 有效 ACL 讀取＋scratch deny-ACE 機制實證 | **無任何 deny ACE**；機制可用且可逆，但單一身分只能做「不可變」，做不到 maker/checker 分離 |
| SR-6 | 硬化移植到 main 是否乾淨？ | `dba4b19` 重建＋全套測試＋18 變異 | 反例在 main 上已關（10/10 detected、M04/M06/M16 REJECT、8 NOT_RUN 逐條重判）；**但移植引入 2 個 main 分歧失敗**（其一為崩潰路徑），已記錄未修 |
| SR-7 | 控制平面的平面實際綁到什麼？ | 讀車道池、governed profile、delegation 設定 | PLAN 與 VERIFY 在車道池 rank 1 同模型（`gpt-6.1-sol`）；EXECUTE 為 `deepseek-v4.1-flash`；**PLAN/VERIFY 無模型軸獨立性（owner 設計）** |

## 2. 自學習（迴圈自身缺陷與修正）
| id | 教訓 | 觸發 | 處置 |
|---|---|---|---|
| SL-1 | **只比對「宣告數量」的清單，會在內容被靜默刪除時照樣通過**；無損必須用 byte 存在性驗證 | HGK 候選在我第一版 harness 下 PASS，補上 references 覆蓋後才現形 | 新增 C6 並**撤回**先前的 PASS，兩個候選重判 |
| SL-2 | 建置期硬編碼的期望值必然在受測體演化後變成假紅；正解是**推導期望**，不是刪斷言 | TF-10 | harness 改為執行期推導＋保留負向控制＋7 個回歸測試 |
| SL-3 | **上線後的無損證明必須對 pre-image 跑**，不能對上線後的樹跑（等於自己比自己） | 我第一次重跑得到 6 個假 sha mismatch | 改以 subject=live、live=preimage 重跑 → 0 遺失 |
| SL-4 | 車道無法證明「哪個 arm 服務了這一回合」時，產物仍可驗，但**必須放棄歸屬宣稱** | dispatcher `EXIT 3`、nonce 缺席（本任務第 8 次） | 記為未證歸屬並留在帳上，未軟化 |
| SL-5 | 守衛擋下自己的寫入是**功能**：正解是詢問 owner 並走受制裁的授權路徑，**不是改寫 payload 鑽過去** | 兩份子代理收據被前置守衛拒絕 | 已詢問 owner → 取得受制裁的時限授權 → 具名披露後補寫 |
| SL-6 | 發佈必須宣告「刻意排除了什麼」，而非只宣告「包含了什麼」 | R6 manifest 不符＋技能樹內快取檔 | R8 manifest 新增 `excluded_scratch[]`，逐路徑附理由 |

## 3. 自迭代（本回合實際改動的流程工件）
`ws_a_skill_slim_regression.py`（＋C6、stub 分類修正）｜`WS_H/round_selfcheck_r8.py`＋`test_tf10.py`（期望推導＋負向控制）｜`publish_r8.py`（新前綴參數化＋排除帳）｜`R8_VERIFIER_BRIEF_WSAB.md`（驗收官寫入根一律在主體外）｜KANBAN 卡片以可機讀證據字串結案｜OpenSpec 提案把本回合的契約寫成可嚴格驗證的變更提案。

## 4. 自進化（提案，附 owner 與閘門；無一項由代理自行授予）
| id | 提案 | 最早 owner | 為何需要 | 證據 |
|---|---|---|---|---|
| SE-1 | 給 checker 獨立 OS 身分或受限沙箱，使 maker/checker 分離「被強制」而非「被記載」 | HGK Checker Harness Owner | 單一身分下最強控制僅為不可變 | `WS_C/…EVIDENCE.json` |
| SE-2 | 把車道 arm 歸屬做成收據的一級欄位，nonce 缺席時收據 fail-closed | HGK lane/dispatcher owner | 產物可驗而歸屬不可驗，claim ceiling 應自動降級 | TF-06 |
| SE-3 | 硬化必須先適配 main 的新契約才可出貨：修 `derive_frozen_context` 對字串型欄位的處理，並只在校驗情境合法缺席時放行 | DOC-07 Oracle/Validator Owner | 移植關掉反例卻引入 2 個失敗（含崩潰） | `WS_B/WS_B_RECEIPT.md` §4.2 / §5.2 |
| SE-4 | HGK 瘦身候選改為「修復後再上線」：補回 2 份遺失 reference、移除快取檔、重跑閘門 | Skill Owner | 現狀上線等於刪教學內容 | `WS_A_HGK_APPLY_DECISION.json` |
| SE-5 | 出具 R6 版本化 errata（2 個未發佈快取路徑＋失效數字），不改寫已合併 packet | Fabric publication owner | 把計數不符變成可重現的已記錄差異 | `WS_D/EIA_R6_RECONCILIATION.json` |
| SE-6 | 維持 >60 references 為 warning、超容量主檔列為待辦隊列，**不得升為硬閘門** | Skill Owner | 2 個主檔超 10 萬 byte、1 個技能 118 refs；機械切分而無無損閘門＝以警告換靜默遺失 | `WS_A_LIBRARY_SCAN.json` |
| SE-7 | 維持殘餘 SoD 揭露為常設項：PLAN 與 VERIFY 同模型家族係 owner 決定，獨立性落在程序／車道／收據／寫入根（SE-1 落地後再加上 OS 身分） | Owner（SoD 方案持有人） | 宣稱模型軸獨立會是假的 | `R8_MISSION_PLAN.md` §2、`WS_G/…ROLEMAP.json` |

## 5. 否證條件（本檔如何被推翻）
- SR-2：受守護主體任一檔的 git-blob sha1 與合併 packet 不同。
- SR-4：在上線後的語料中找不到某份 live reference 的原文。
- SR-6：main 上任一變異回 `ACCEPT` 而應為 `REJECT`，或測試重跑沒有那兩個已記錄的失敗。
- SE-1：**今日已觀測到的狀態本身即否證**——同身分的一般程序可以寫入受守護主體。

## 6. 非宣稱
不是驗收／批准／閘門 PASS／生產陳述；本檔不升級任何裁決；不創造任何權限（每一條 SE 都指明 owner 與閘門）；本檔由執行本回合的 orchestrator 撰寫，**不構成對自身的獨立審查**。
