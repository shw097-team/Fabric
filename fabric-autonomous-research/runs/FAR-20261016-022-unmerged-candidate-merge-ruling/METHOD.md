# FAR-20261016-022 — Method

## 受測總體（21 條，非抽樣）

`git branch -r --no-merged origin/main`（fetch 全部 head 後）＝ 21 條；另以 **credential-free 公開 API**
讀回開放 PR 4 條（#18／#17 ready；#14／#15 draft）。兩份清單互相對帳，無遺漏。

## 量測（唯讀；`checks/candidate_inventory.py`，輸出 `candidate_inventory.json`）

對每條分支量四件事——這四件足以決定一條分支該不該併：

1. **併入會實際加入什麼**：`git diff --name-status origin/main...<b>` 的檔數與 `--shortstat`。
   空 diff ⇒ 內容已由他路徑落地 ⇒ 併入無意義（**取代性判定**，不需人為記憶歷史）。
2. **衝突性**：`git merge-tree --write-tree origin/main <b>`（不改工作區）判定是否 CONFLICT。
3. **是否觸及 `src/`／`schemas/`／`skills/`**：決定併入是否需要重跑全套產品測試。
4. **分支性質**：evidence／closeout／readme 命名與其頂層目錄形狀。

## 判準（依序，先到先決）

| 順位 | 條件 | 裁決 |
|---|---|---|
| 1 | 相對 main 的 diff 為空 | `SUPERSEDED`（不併） |
| 2 | 與現行 main 衝突 | `DO_NOT_MERGE`（併入即需人工解衝突＝違反低阻力） |
| 3 | 性質為證據／回證分支（其存在目的即為承載證據） | `EVIDENCE_ONLY`（永不併入 main） |
| 4 | 小、乾淨、具明示外部放行或本回合已驗 | `MERGE_NOW` |
| 5 | 其餘（大、陳舊、意圖不明） | `NOT_RECOMMENDED`（交 Owner 明示意圖） |

## 安全閘門（執行前必過，任一不過即停）

- **G1** 併後在**本地**跑全套產品測試（`pytest -q`）——先於任何 push。
- **G2** 併後對現行 main 跑 PR #18 帶來的 `doc-identity guard`（本回合新增的相容性問題：我的 docs 候選與
  #18 是否互相破壞）。
- **G3** `v0.1.1-preview.4` tag 物件與資產、`src/` 內容、`schemas/` 內容在併後**逐位元不變**（除 #18 帶來的
  測試／workflow 檔）。
- **G4** 單一 push、`--no-ff` 保留合併歷史、**禁用 force**；推後立刻遠端回讀尖端。

## 不做

重構、Tag、Release、資產替換、刪遠端分支、關閉 PR、動 `.hgk` 內容。
