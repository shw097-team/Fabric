1. 一句話

這個 evidence 包解決車道憑證輪替沒有既定程序的問題，提供 consumer 宣告、可重跑命令、hash-only 收據與可回滾路徑；其結論是輪替瓶頸主要來自 consumer 集合未宣告，因此以 manifest、rotate 命令與驗收收據形成最小程序（`research-product/ResearchSynthesis.md`）。

2. 邊界與 claim ceiling

- Claim ceiling 為 `LOCAL_CHECK`；本包是可交付的本地檢查證據，未執行 native acceptance、independent acceptance 或 release（`research-product/ResearchSynthesis.md`、`research-product/ResearchRunReceipt.json`、`research-product/CandidateResearch.yaml`）。
- Runbook 記載目前只以 dry-run 與唯讀 `--pin-refresh` 實跑通過，尚未對任何新憑證執行 `--apply`；本包不宣稱曾用新憑證執行輪替（`RUNBOOKS/3LM_KEY_ROTATION.md`、`out/VERIFY_RECEIPT_2.md`）。
- 本包未把金鑰值寫入任何檔案；rotate 腳本以子程序環境傳遞金鑰，收據只保留 fingerprint 與長度，探針只保留輸出 hash 與長度，並標記 `secret_printed: false`、`raw_output_stored: false`（`ops/rotate_3lm_key.py`、`ops/3lm_consumers.json`）。

3. 檔案清單

- `RUNBOOKS/3LM_KEY_ROTATION.md`：定義乾跑、套用、探針驗收、重啟、回滾、pin refresh 與禁止事項的操作程序。
- `ops/rotate_3lm_key.py`：執行預設乾跑、manifest 規劃、備份、探針、套用與 hash-only 收據寫入。
- `ops/3lm_consumers.json`：宣告憑證角色、consumer 清單、檔案樣式與 codex probe 條件。

FAR 產物（15 份）：

- `research-product/CandidateKnowledge.yaml`：保存候選知識命題及其證據編號。
- `research-product/CandidateResearch.yaml`：保存候選建議、信心、非 claim、未解項目與車道狀態。
- `research-product/ClaimLedger.tsv`：記錄可追蹤的 claim、類別、來源與信心。
- `research-product/ContradictionLedger.tsv`：記錄表面矛盾及判定為非矛盾的理由。
- `research-product/FitGapLedger.tsv`：記錄現況缺口與其處置方式。
- `research-product/HypothesisLedger.tsv`：記錄假設、支持或拒絕狀態及證據。
- `research-product/OpenQuestionLedger.tsv`：記錄尚待 Owner 決定的問題與原因。
- `research-product/ProposedEvolution.yaml`：記錄程序演進提案、驗收條件、Owner 核准項與風險。
- `research-product/QueryLedger.tsv`：記錄查詢通道、查詢主題與結果。
- `research-product/RejectedAlternativeLedger.tsv`：記錄已拒絕方案及其理由。
- `research-product/ResearchHandoff.yaml`：記錄研究交接狀態、交付物、車道狀態與 Owner 待辦。
- `research-product/ResearchPlan.yaml`：記錄研究子問題、claim 類別與停止條件。
- `research-product/ResearchRequest.yaml`：記錄研究範圍、排除範圍、預算、停止條件與 Owner 角色。
- `research-product/ResearchSourceDenominator.tsv`：記錄來源定位、hash、大小、角色與讀取狀態。
- `research-product/ResearchSynthesis.md`：彙整結論、事實、反例、建議程序、未解事項與兩輪驗證軌跡。

FAR 執行收據：

- `research-product/ResearchRunReceipt.json`：記錄 15 份 ledger、車道狀態、claim ceiling、產物 hash 與 dispatcher 狀態。

兩輪 VERIFY 收據：

- `out/VERIFY_RECEIPT.md`：記錄第一輪逐項判定、最嚴重缺陷與簡化建議。
- `out/VERIFY_RECEIPT_2.md`：記錄修正後的 R3、R4、R6、R1 複核結果。

4. 怎麼用（三步）

先將新的單行 UTF-8 憑證檔放在 runbook 指定的位置，且不要把金鑰值放進命令列參數或工單。以下命令取自 runbook（`RUNBOOKS/3LM_KEY_ROTATION.md`）：

```bash
cd <WORKSPACE>/FHS_NEXT_Workspace/FAR_3LM_KEYROT_20261114
PY="<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
```

第一步是乾跑；它完整檢查並執行探針，預期 `verdict: PASS`、各 consumer 的 `changed` 符合預期、`probe_ok: true`、`secret_printed: false`：

```bash
"$PY" ops/rotate_3lm_key.py --key-file "<WORKSPACE>/API KEY/shw098_OPENCODEGO_KEY.txt"
```

第二步是在確認乾跑結果後套用；腳本會先建立 `.bak-<UTC>`，再探針，探針成功後才改寫：

```bash
"$PY" ops/rotate_3lm_key.py --key-file "<WORKSPACE>/API KEY/shw098_OPENCODEGO_KEY.txt" --apply
```

第三步是再跑一次乾跑作為探針驗收，並檢查收據存在、`secret_printed = false`、探針 `exit 0`、stdout 含 `CHECKER_OK`、新舊 fingerprint 不同且舊指標檔仍在：

```bash
"$PY" ops/rotate_3lm_key.py
```

`desktop-model-router` 需要重新啟動才能讀取新值；`hgk-host-readback` 在下次執行時生效（`RUNBOOKS/3LM_KEY_ROTATION.md`、`ops/3lm_consumers.json`）。

5. 已知缺口

- 3LM dispatcher 需要 `--nonce`，且模型必須回傳 nonce；否則會出現 `ERR_NO_ARM_EMITTED_NONCE`。
- codex binary pin 會漂移；同一支 rotate 命令以 `--pin-refresh` 檢查漂移。唯讀報告不改檔，寫入 pin 必須使用 `--i-approve-pin-change --apply` 並取得 Owner 核准（`RUNBOOKS/3LM_KEY_ROTATION.md`、`ops/rotate_3lm_key.py`、`research-product/ResearchSynthesis.md`）。
- 485/舊 key 保留等未決事項不屬本包。

6. 給外部工程團隊的接手點

先讀 `RUNBOOKS/3LM_KEY_ROTATION.md` 掌握操作與回滾邊界，再讀 `ops/rotate_3lm_key.py` 核對 plan、backup、probe、apply 的實際順序，最後讀 `out/VERIFY_RECEIPT.md` 與 `out/VERIFY_RECEIPT_2.md` 的 FAIL→PASS 軌跡。第一輪將 V3、V4、V6 判為 FAIL；第二輪以 R3、R4、R6 PASS 對應關閉這三項，並另列 R1 PASS（`out/VERIFY_RECEIPT.md`、`out/VERIFY_RECEIPT_2.md`、`research-product/ResearchSynthesis.md`）。
