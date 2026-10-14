# FAR — 結案裁決：執行缺口、REPO 維護、SESSION 結案

方法：先事實、再依五項標準（低阻力、高可行、高工程必要性、低回歸風險、不過度工程化）評估、最後裁決與執行計畫。本檔為本回合的 PLAN 產物，於 Hermes 內執行。路由揭露與前次相同：本 session runtime metadata 為 `deepseek-v4.1-flash`；EXECUTE lane 走 `opencode-go/deepseek-v4.1-flash`、VERIFY／SECURITY lane 走 `opencode-go/glm-5.3-flash`，各以自身 dispatch receipt 為證（required＝served）。

## 一、事實（實測）

### 1.1 四個 repo 的實況

| repo | remote | 分支 | 工作區 |
|---|---|---|---|
| `Fabric/` | **無**（`git remote -v` 空） | 只有 `main` | 51 未追蹤 + 6 已修改 |
| `HG-KSEOS/` | 無 | `codex/hgk-final-closure-002` | 252 筆異動 |
| `PIPD/` | `shw097-team/PIPD-LS-SP.git` | `r5p-post-challenge-repair` | 216 筆異動 |
| `SWOF/` | `shw097-team/SWOF.git` | `evidence/swof-w2r5-closure-repair` | 9 筆異動 |

`Fabric/` 是**沒有 remote** 的本機 repo，因此「完整更新、MERGE」在本機只能落成：把工作區納入版本控制並提交到 `main`。

`Fabric/` 自身衛生狀態：**完全沒有 `.gitignore`**；`__pycache__` 與 `.pyc` 未追蹤地散在 `fabric/consumers/`、`fabric-autonomous-research/` 與子目錄 `desktop-automation/tests/`；**`README.md`（5,344 B、2026-10-13）存在於磁碟卻未追蹤——repo 的首頁不在 repo 裡**；`AGENTS.md`（10,894 B）與 `docs` 說明文檔（32,790 B）已修改未提交；另有約四十個先前回合累積、從未提交的 review 證據檔（`evidence/review/` 之下），以及少量真垃圾（byte-cache、`worker.log`、`runs/`）。

### 1.2 發佈標的（以探測證明，不靠推論）

`shw097-team/PIPD-LS-SP` 為公開 repo，預設分支 `main` 位於 `f4021ae`；**匿名 `ls-remote` 成功** → 外部讀者不需任何憑證。owner 提供的憑證 93 bytes，只從指定檔讀取，離開腳本的僅有長度與布林值。**可逆寫入探測**（在遠端已有的 commit 上建一個分支 ref，再刪除）：建立回 `201`、刪除回 `204`、回讀 `404` → **寫入能力已證實且未留下任何東西**。讀取 scope 無法證明此事（GitHub 的 `permissions` 物件反映的是使用者角色，不是憑證授權）。

版面慣例自 repo 本身讀出：回合交付物以根目錄 `*_RETURN/` 目錄、掛在 `feat/<round>-YYYYMMDD` 分支（例如 `feat/s4r7-main-upgrade-and-repo-state-20261014`、`feat/s4r5z-evidence-readme-20261014`；本機 `PIPD/` 內有 `PIPD_S4_R7_RETURN/`）。`main` 上沒有任何 `*_RETURN` 目錄 → 那些分支才是交付面。

**改變計畫的碰撞訊號**：遠端存在分支 `fix/s4r7-readme-main-sha-truthfulness-20261014`，且 `_handover/CHECKPOINT_R7_FINAL_20261014.md` 於今日 14:41 寫入 → **另一個 workstream 正在改同一個 repo 的 README 與 main sha 真實性**。第二個 session 去改同一份 README 就是與進行中的變更相撞。

### 1.3 帶入本次裁決的缺口與待決事項

| 編號 | 項目 | 狀態 |
|---|---|---|
| G1 | HGK 參考檔 95 檔，仍高於 linter 的 60 檔警告線 | 已量測，試點完成，**上限未達成** |
| G2 | 其餘主題群未整併（AVR 約 17、HGK 約 86 檔未動） | 依前次裁決延後 |
| G3 | generation 2 **沒有可採信的安全 verdict**：一次無 nonce、一次預算耗盡、一次空 token | 已暫停，待授權 |
| G4 | canonical dispatcher 的逾時 partial-capture 補丁已備、**未落地** | 候選產物 |
| G5 | guarded apply 只跑過 fixture | 超出本回合 |
| G6 | 無 canonical apply、無 promotion | 依裁決拒絕自我授權 |
| G7 | harness 缺陷：假 stub 訊號、我自己的空真 I5b | 已修並揭露 |
| G8 | 紀律紀錄：12 次逾時、2 次無 nonce、1 次污染、1 次空答案 | 保留，不因結案消失 |
| P1 | 我先前列出的三個安全軸選項 | 本指令把裁決權交給本 FAR，並要求執行到可結案 |

## 二、評估與裁決

| 項目 | 必要性 | 阻力 | 可行 | 回歸風險 | 過度工程 | 裁決 |
|---|---|---|---|---|---|---|
| G3 一次修正版安全 lane（token 只放結尾＋最小內容規則） | 高——這是唯一沒有 verdict 的軸 | 低 | 高 | 無 | 無 | **做，且只做一次** |
| G2 把所有剩餘主題群整併完 | 低——兩入口已在硬限的約兩成，整併不帶來限額緩解 | 高 | 高 | 低 | 中 | **延後並說明理由** |
| G4 落地 dispatcher 補丁 | 原則上高 | 高——那是控制平面自身的車道機制 | 中 | 中 | 低 | **僅移交候選，不落地** |
| G5／G6 真寫入與 promotion | 超出授權 | 高 | — | 高 | — | **拒絕，並明白寫出** |
| Fabric 衛生：`.gitignore`、清掉 byte-cache、提交未追蹤的首頁與說明文檔 | 高——repo 首頁不在 repo 內，且沒有任何排除規則 | 極低 | 高 | 無（本機、無 remote） | 無 | **做** |
| Fabric 既有 review 證據納版 | 中高——那是該 repo 自己的 review 面 | 低 | 高 | 低（先掃密鑰、原樣提交、附雜湊清單） | 低 | **做，獨立一個 commit** |
| 改 GitHub repo 的 `main`／README | — | — | — | **中高：與進行中的 README 修正分支相撞** | — | **縮手**：只把本機 README 與文檔原樣提交，**不碰遠端 README 與 `main`** |
| 把本次實作與證據發佈到 `shw097-team/PIPD-LS-SP` | 指令要求 | 中 | 高 | 低（新分支、只加一個目錄） | 低 | **做：新分支、根目錄 return 目錄、逐位元回讀** |
| SESSION 結案：checkpoint、移交、產物清單、看板收尾、生命週期狀態 | 指令要求「執行到可完整結案」 | 低 | 高 | 無 | 無 | **做** |

### 裁決

**R1**｜安全軸**只補一次**修正版 lane，然後無論結果都收尾：若取得可採信 verdict，兩軸齊備後結案；若第四種失敗，則以「generation 2 安全軸**未經獨立驗證**」入帳，並附三次失敗事實。**不再換第三種變體，也不用我自己的判讀冒充 verdict。**

**R2**｜把 Fabric 工作區納入版本控制（本機 `main`），切成三個 commit：衛生（`.gitignore`）、首頁與文檔（未追蹤的 `README.md`＋已修改的 `AGENTS.md`／docs）、先前回合的 review 證據。每個 commit 前先掃密鑰，附生成式雜湊清單，垃圾排除而非提交。**不碰遠端 README 與 `main`**：那個面上有別人正在進行的變更，正確做法是讓開並說明。

**R3**｜把本次實作與證據交付到 `shw097-team/PIPD-LS-SP` 的**新分支** `feat/skill-convergence-return-20261014`，根目錄 `SKILL_CONVERGENCE_RETURN_20261014/`，內含入口文檔、生成式證據清單（含 sha256 與處置）、受測候選世代（兩份主檔、slice map、topic payload、批次紀錄），以及本回合每一份 verdict／裁決／收據——**含失敗**。驗證方式：從遠端回讀位元、匿名免憑證回讀、確認 `main` 未移動。

**R4**｜以標準產物結案：回合 `var/` 下的 resume checkpoint、`_handover/` 內的移交 checkpoint、產物 sha256 清單、看板任務收尾、生命週期狀態記為「已結案的候選」。**不給 acceptance、不給 promotion**：agent 不替自己發放這兩者。

## 三、執行計畫

- X1：一次修正版 SECURITY lane（gen2，唯讀、強制 GLM arm、token 僅放結尾）。
- X2：Fabric 衛生與提交集（本機 `main`），含密鑰掃描與雜湊清單。
- X3：SESSION 結案產物（checkpoint、移交、清單、看板、生命週期紀錄）。
- X4：發佈分支至 `shw097-team/PIPD-LS-SP`，含逐位元回讀與匿名驗證。
- X5：一次獨立 VERIFY lane 覆核結案包與已發佈的 return 目錄。

全案天花板：受測體維持候選、本機無 remote 的 repo 只做本機維護、對公開 repo 做一次供外部設計參照的 advisory 發佈；**無 acceptance、無 promotion、無 canonical apply**，且不修補紀錄上既有的失敗。
