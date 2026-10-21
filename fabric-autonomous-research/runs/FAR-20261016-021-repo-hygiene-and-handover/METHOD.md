# FAR-20261016-021 — Method

## Frozen inputs

- 《S4 最終獨立驗收報告》§0 STOP RULE、§3.1、§8「不批准」清單、§10 最後一句 Gate 裁決。
- 本 SESSION 前一回合的最終狀態（`ROUND_STATE.json`，證據尖端 `5750c690…`）。
- repo 內**既有歸宿**：root `README.md`（492 行、34,099 B，含 `## Current state and evidence entry points (2026-10-14)`）、
  `docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md`（126 行）、
  `docs/adr/ADR-0009-session-handover-and-next-session-start.md`（144 行）、`docs/FRONT_PAGE_HISTORY.md`（48 行）、
  `docs/install/README.md`（安裝 SSOT）、`docs/USER_GUIDE.md`（唯一使用手冊）。
- 遠端凍結值：`main d3bd5456…`、PR #18 `c17aa761…`、PR #17 `97a01dab…`、`.4` tag `0618d73c…`→`cc6c1930…`。

## Measurements（全部為可重跑命令，非敘述）

| 量測 | 命令 | 證據 |
|---|---|---|
| 本地衛生清冊 | `checks/hygiene_inventory.py`（唯讀；逐 worktree 走訪） | `hygiene_inventory.json` |
| 首頁樹是否被回合目錄污染 | `git ls-tree main --name-only` | main 樹清單（無 `far-r17/`、無 `*_RETURN/`） |
| README 過期程度 | `grep -n "2026-10-14\|Current state"` ＋ 節內逐列 | 行號與內容 |
| 主 clone 未提交工作 | `git status --porcelain` ＋ `git diff --stat -- src tests skills` | 6 修改／218 未追蹤；`src` +203/−6 |
| worktree 可回收性 | dirty==0 **且** `refs/remotes/origin/<branch>` == 分支尖端 | 13 候選 |

## Reuse-first rule（本輪的核心方法）

四個題目**在 repo 內都已有歸宿**：衛生→ADR-0008；首頁→README 的 current-state 節；README 重構→已於先前回合完成；
移交→ADR-0009。因此方法的預設答案是**就地更新既有歸宿**，而不是新建文件；
只有在「既有歸宿不存在或語義不合」時才允許新增，且必須在裁決內明示理由。

## What is measured vs. what is asserted

- **測得**：清單、行號、git 事實、遠端 API 事實。
- **斷言**（無獨立證據者一律標明）：README 的「重構已完成」是**判斷**，依據是節點結構（導覽表、錨點、Claim
  ceiling、State 節）而非任何驗收官的核可；本 FAR 不把它升格為驗收結論。
- 本輪**不做**任何 live 宿主 UAT、不重跑產品測試（產品 0 行變更時，重跑只能證明未動，不是新證據）。
