# CHECKPOINT / RESUME — 工程 `SKILL-CONVERGENCE-20261014`

（本檔為續作入口。新 session 請先讀本檔，再讀 `evidence/postfreeze/SESSION_CLOSURE.md`。）

## 一句話狀態

本回合已完成「無損抽取＋主題整併試點＋consumer 複用＋回退點與收斂不變式＋兩軸獨立查核＋Fabric 本機 repo 維護＋對外發佈＋結案移交」。狀態：**候選（candidate-only）**，無 acceptance、無 promotion、無 canonical 寫入。

## 續作時必讀

| 檔案 | 用途 |
|---|---|
| `evidence/postfreeze/SESSION_CLOSURE.md` | 結案紀錄：交付項、天花板、殘留缺口 R1–R7、失敗紀錄、移交指示 |
| `evidence/postfreeze/CLOSURE_MANIFEST.json` | 結案產物清單（逐檔 sha256）|
| `evidence/postfreeze/FAR_CLOSURE_REPORT.md` | 本次結案 FAR 裁決 R1–R4 與計畫 X1–X5 |
| `evidence/postfreeze/FAR_REMEDIATION_REPORT.md` | 前次 FAR 裁決 R1–R5（含主題群清單）|
| `evidence/subject_manifest.json` | 受測體綁定：gen2 370 列、樹摘要 `b050a025…ba16b48e8fa` |
| `evidence/postfreeze/publish_readback.json` | 發佈讀回（三通道，免憑證）|
| `evidence/postfreeze/packet_readback.json` | 回傳包位元可重現性（committed blob 與 checkout 兩者）|
| `evidence/postfreeze/commit_digest_classification.json` | Fabric 提交位元與掃描位元的差異分類 |

## 關鍵常數

- 凍結世代：gen2 **370 檔**、樹摘要 `b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa`（組成：`sha256('\n'.join("<sha256> <path>"))`，無尾端分隔符）。
- gen1（374 檔／`9b68418b…36cb`）**superseded**，未刪。
- canonical 分派器 `HG-KSEOS/scripts/hgk-lane-dispatch.py` sha256 `17e667d136f1463609a44e2de6a8f7ba9aab07653f6ea4490178fc4ff93a6c56`（未變）。
- 對外分支：`feat/skill-convergence-return-20261014`，最終 tip `dcdc46295bacd829f1bd1d611f3b478e3646a93e`（632 檔／5,540,242 bytes；修訂鏈 v1→v5 皆為 additive）。`main` 未移動（`f4021ae`）。匿名 clone 逐檔 `files 632 mismatch []`、`NO_HITS`、免憑證 → `ENTRY_DOCUMENT_COMMAND_SUCCEEDS_ANONYMOUSLY`；提交位元複驗 `PACKET_BYTES_REPRODUCIBLE_FROM_THE_CLONE`（632/632）。
  - 本檔在 v5 之後更新；**回傳包內為 v5 當時的快照**（包內檔案的 tip 一律比分支 tip 舊，這是 fixed point 的必然）。最終狀態另記於 `evidence/postfreeze/PUBLICATION_FINAL_v5.json`。
- Fabric 本機三提交：`8b59155`、`8bd3685`、`abb70eb`（工作區 0 筆異動）。

## 已知殘留（不得讀成完成）

1. references 檔數 94（90＋4）vs 上限 60（差 34）。
2. 其餘主題群未整併。
3. canonical 逾時補丁未落地（僅候選，2,621 bytes）。
4. guarded apply 僅 fixture。
5. 無 apply／promotion／acceptance。
6. live 樹被 runtime curator 推進，byte-exact 僅對凍結世代成立。
7. 失敗紀錄保留：逾時 12、無 nonce 2、污染 1、空答案 1。

## 續作第一步

依 `SESSION_CLOSURE.md` 第 6 節：先解 R1，再依前次 FAR 的主題群清單擴做整併，最後處理 R3 的 canonical 補丁（走獨立 admission 與 governed landing）。

## 環境備註（避免重踩）

- 本機 python 只在 `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`。
- lane 內為 pwsh：禁 heredoc；`rg`／bare `python` 不在 PATH。
- lane 的 token 收尾請放**結尾**（放開頭會讓 turn 可以只回 token 就滿足傳輸 gate）。
- 逾時屬 system 性：真兇是「brief 寬度 × 預算」；縮窄 brief 已多次奏效。
