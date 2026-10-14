# SKILL_CONVERGENCE_RETURN_20261014 — 外部設計參照包

## 這是什麼

這是工程 `SKILL-CONVERGENCE-20261014` 的回傳包，交付給外部設計團隊參照與規劃升級之用。

受測體是 canonical Hermes 的兩份治理技能入口，兩者都已頂到近 100,000 字元的硬限：`hgk-governed-execution`
與 `adversarial-verification-rounds`。本回合對它們做了：無損抽取（主檔瘦身、把內容切成 slice 併入
references）、主題 references 整併、既有 consumer 的複用驗證；同時建立回退點與全域收斂不變式，並以兩條
獨立 lane（VERIFY 與 SECURITY）對候選世代查核。

狀態：**候選（candidate-only）**。沒有 acceptance、沒有 promotion、沒有對 canonical 樹寫入任何位元。

## 分支與基準

- 分支：`feat/skill-convergence-return-20261014`，自 `main`（`f4021ae`）分出。
- 本包**只新增** `SKILL_CONVERGENCE_RETURN_20261014/` 一個目錄；`main`、repo 根 `README.md` 與任何既有
  路徑都未被改動。（原因見下方「併發揭露」。）

## 受測體綁定（要看哪一份位元）

- 凍結世代：**generation 2**，370 個檔案列。
- 樹摘要：`b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa`
  組成方式＝`sha256('\n'.join("<sha256> <path>"))`，**無尾端分隔符**（有尾端換行會得到 `2bb90bc2…`，
  CRLF 會得到 `18ca8eee…`）。
- 逐列清單與每一列自己的 sha256：`subject_frozen_generation/` 與 `EVIDENCE_MANIFEST.json`。
- 誠實提醒：本包把 370 列重新掛在 `subject_frozen_generation/` 之下，**路徑前綴已改變**，因此上面那個
  樹摘要**無法在包內原樣重算**；包內可驗的是**每一列檔案自己的 sha256**。

## 內容

| 路徑 | 內容 |
|---|---|
| `subject_frozen_generation/` | 凍結世代 2 的 370 列（baseline／candidates／qualification／verification）|
| `evidence/harness-and-records/` | 本回合的 harness、裁決腳本與紀錄 |
| `evidence/postfreeze/` | 凍結後收據：FAR 報告、世代切換、逾時分類、暫停收據、逐項裁決 |
| `evidence/prompts/` | 每條 lane 的 brief（含失敗版本與修正後版本）|
| `evidence/lanes/` | 每條 lane 的 verdict／dispatch receipt／result（不含量大之逐字稿）|
| `closure/` | 本機 repo 衛生、提交位元分類、結案腳本 |
| `EVIDENCE_MANIFEST.json` | 逐檔 sha256／大小／處置；**含被排除項、被排除理由與其雜湊** |
| `HASHES.sha256` | 平坦雜湊清單 |

## 獨立查核結果（皆為 advisory，不是 acceptance）

- VERIFY（gen2）：`PASS_ADVISORY`，17 個固定案例編號全符，含逐位元重算。
- SECURITY（gen2）：`PASS_ADVISORY`，6 個固定案例（5 個 PASS ＋ COVERAGE 為 PARTIAL）。
- 我方對兩者逐項重算：subject 樹摘要相符、370 列對磁碟 0 筆不符、14 檔併入後仍在 topic 內逐位元在位、
  候選補丁 18/18 context 與 canonical 相符、canonical 分派器 sha256 未變。
- 兩條 lane 的查核腳本（`adjudicate_*`、`check_*`）都在包內，可自行重跑。

## 未完成與已知缺口（不得讀成完成）

1. references 檔案數在整併後為 **94**（`references/` 90 檔＋`topics/` 4 檔），仍高於 linter 的 **60 檔**警告線（差 34）。初稿寫 95 為 harness 計數變體，已於結案紀錄中更正。
2. 其餘主題群的整併**延後**（本回合只做了一個 14 檔試點群）。
3. canonical dispatcher 的「逾時丟棄 partial capture」缺陷**只有候選補丁、未落地**；動控制平面必須走它
   自己的 admission 與 governed landing。
4. guarded apply **只跑過 fixture**，沒有任何真寫入。
5. **無 canonical apply、無 promotion**：agent 不對自己的產物發放這兩者。
6. 本回合紀錄上既有的失敗**全部保留、結案不修補**：12 次逾時派送、2 次無 nonce 回傳、1 次內容污染
   verdict、1 次空答案 turn、1 個 harness 假訊號欄位。

## 重跑方式與預期輸出

在一個**匿名** clone 內（不需要任何憑證）：

```bash
git clone --quiet https://github.com/shw097-team/PIPD-LS-SP.git
cd PIPD-LS-SP && git checkout feat/skill-convergence-return-20261014
cd SKILL_CONVERGENCE_RETURN_20261014
python -c "import json,hashlib,pathlib;m=json.load(open('EVIDENCE_MANIFEST.json',encoding='utf-8'));bad=[f['packet_path'] for f in m['files'] if hashlib.sha256(pathlib.Path(f['packet_path']).read_bytes()).hexdigest()!=f['sha256']];print('files',len(m['files']),'mismatch',bad)"
```

預期輸出：`files <N> mismatch []`

（位元保真說明：本包內含 `.gitattributes`，內容為 `* -text`，用來停用 repo 對這一子樹的換行正規化。
工程期間所有 digest 都是在作者主機上的原始位元上算的；若不停用正規化，clone 出來的檔案會被改寫換行，
讀者將**無法重現** `EVIDENCE_MANIFEST.json` 裡的任何一個 digest。若某個環境仍不正常，請以此指令診斷：）

```bash
git -c core.autocrlf=false cat-file -p HEAD:SKILL_CONVERGENCE_RETURN_20261014/EVIDENCE_MANIFEST.json > /dev/null
```

```bash
python -c "import json;m=json.load(open('EVIDENCE_MANIFEST.json',encoding='utf-8'));print(m['credential_scan']['outcome'],m['counts'])"
```

預期輸出：`NO_HITS {...}`（表示出廠前掃描無命中，且計數與上表一致）

## 本包的修訂與結案附帶物

- 本包在同一分支上以 **additive commit** 修訂（未改寫既有檔案語意）：初版 → 補上安全 lane 的 verdict 本體與結案紀錄 → 補上三通道讀回紀錄 → 補上結案/移交附帶物（board 結案回證、續作 checkpoint、移交 checkpoint、結案 manifest）。
- `closure/handover/` 內含：續作 checkpoint（`_CHECKPOINT_RESUME.md`）、移交 checkpoint（包內改名為 `HANDOVER_SKILL-CONVERGENCE-20261014.md`，因 repo 的 `.gitignore` 會排除 `CHECKPOINT_*.md`）、看板結案回證（以 board DB 直讀，不以 CLI exit code 為證）。
- **v4 的一次自我修正**：v4 的 manifest 曾把上述檔案列為已交付，但 repo 的 `.gitignore` 規則把它從 commit 中默默排除；我方的提交位元回讀抓到「blob 不存在」而判 `PACKET_BYTES_NOT_REPRODUCIBLE`，v5 以改名修正。此為「回讀抓到靜默排除」的實例，記錄於此。
- **v6 補上目標 repo 的更正**：owner 指出 **Fabric 的 repo 是 `shw097-team/Fabric`（Integrated Governance Mirror）**。檢查結果：本回合 Fabric 側的一切（`.gitignore`、`HYGIENE_MANIFEST`、首頁/文檔提交）原先**只在本機 working copy**，該 repo 無 remote；mirror 的 `main` 停在 2026-10-13 的 `71de521e`，**本回合未在其上新增任何 commit**。已以 change-set `docs/skill-convergence-20261014`（PR #1）併入 mirror `main` = `f14724dd`，匿名讀回 3/3 位元相符、新目錄 22 檔在位。
- `evidence/postfreeze/SESSION_CLOSURE.md` 是結案主文：交付項、天花板、殘留缺口 R1–R7、失敗紀錄、續作指示。
- 若 `publish_readback.json` 綁定的 tip 比本分支最新 tip 舊，那是設計上的必然（一個檔案無法綁定包含它自己的 commit），不是不一致。

## 併發揭露

遠端在同一天已有 `feat/s4r7-main-upgrade-and-repo-state-20261014` 與
`fix/s4r7-readme-main-sha-truthfulness-20261014`：**另一個 workstream 正在改 repo 根 README 與 main 的
sha 真實性**。本包因此**刻意不碰** `main` 與 repo 根 `README.md`，改以本目錄的 `README.md` 當入口。這是
一項刻意且已揭露的偏離（一般慣例是在同一份發佈內更新 repo 根 README）；理由是那個面上有進行中的變更，
動它就是把兩個 workstream 的成果互相破壞。

另揭露：本機 `Fabric/` repo **沒有 remote**，因此「Fabric repo 完整更新／MERGE」只能落成它**本機 `main`
的三個提交**（衛生、首頁與文檔、既有 review 證據納版），其證據在 `closure/`，並經提交位元回讀分類。

## 憑證

發佈使用 owner 提供的憑證。它只被程式讀取，離開腳本的只有長度與布林值；未進入 argv、未進入 URL、未進入
log、未進入任何發佈檔案。**憑證檔本身未被打包**，並在 `EVIDENCE_MANIFEST.json` 的排除清單中明確列出。

## 天花板

本包是 advisory 回傳包，供外部設計團隊參照與規劃升級之用。它**不是** acceptance、**不是** promotion、
**不構成**任何 canonical token 來源，也不代表 canonical 樹已被寫入或已被接受。
