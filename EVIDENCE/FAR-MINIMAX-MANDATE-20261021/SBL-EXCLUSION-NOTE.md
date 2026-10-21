# SBL 施工干擾排除聲明（FAR-MINIMAX-MANDATE-20261021）

**發起回合：** FAR-MINIMAX-MANDATE-20261021（2026-10-21，業主模型方案：PLAN / EXECUTE / VERIFY_SECURITY
全部改用 `opencode-go/minimax-m3.1-flash-free`）
**控制平面：** HG-KSEOS
**狀態：** 本回合**未**在下列 SBL 施工路徑執行任何寫入、刪除、移動、git 寫入或提交。

## 辨識到的並行施工

盤點時發現 Fabric 倉庫內有**兩個其他 session 正在寫入**的 SBL 回合目錄（檔案 mtime 落在
2026-10-21 13:36–13:38，即本回合執行期間）：

```
fabric-autonomous-research/runs/FAR-20261021-023-sbl-r7-residual-closure/
fabric-autonomous-research/runs/FAR-20261021-024-fallback-chain-reorder/
```

第一個目錄在唯讀盤點時已含下列治理工件（皆為其他 session 的產物，本回合**只讀不寫**）：

```
CandidateResearch.yaml   ClaimLedger.tsv      ContradictionLedger.tsv
DisagreementLedger.tsv   ExtractionLedger.jsonl  FitGapLedger.tsv
HypothesisLedger.tsv     OpenQuestionLedger.tsv  QueryLedger.tsv
```

## 本回合的排除規則（已實際執行）

| 規則 | 實作方式 |
|---|---|
| 不寫入 SBL 目錄 | 本回合所有的 `write_file` / `patch` 目標路徑全部在 `C:\Projects\Agent_Workspace\HG-KSEOS\` 或 `C:\Projects\Agent_Workspace\Fabric\EVIDENCE\` 之下；`fabric-autonomous-research/` 從未被寫入。 |
| 不刪除、不移動 | 本回合沒有任何刪除或搬移操作。 |
| 不提交 SBL 產物 | 兩次 Fabric 提交（`cf93dab`、`ec77d41`）的檔案清單只含 `EVIDENCE/FAR-LANE-REMEDIATION-20261021/` 與 `INTEGRATION/KNOWN-FINDINGS.md`；`git add` 從未以 `fabric-autonomous-research` 為目標。 |
| 不與其搶同一分支 | 本回合的 Fabric 分支是 `pub/far-lane-remediation-20261021`；SBL 施工使用 `runs/FAR-20261021-02x-*` 的回合目錄，兩者不重疊。 |
| 不改變其他 session 的工作樹狀態 | Fabric 工作樹中 `?? fabric-autonomous-research/runs/FAR-20261021-02x-*/` 兩個項目在本回合結束時仍為 untracked，**未被本回合 stage 或 commit**——它們留給施工中的 session 自行處置。 |

## 殘留狀態（刻意留下的）

Fabric 工作樹在發布後仍顯示：

```
?? fabric-autonomous-research/runs/FAR-20261021-023-sbl-r7-residual-closure/
?? fabric-autonomous-research/runs/FAR-20261021-024-fallback-chain-reorder/
```

這兩個 untracked 項目是**其他 session 的在建產物**。把它們 stage 進本回合的發布會把別人的
半成品混入本回合的證據包；把它們刪掉會破壞施工。所以本回合**刻意不碰**，並在此明確揭露。

## 與 SBL 的關係

本回合的 FAR 研究主題（33 個 OpenSpec change 的未勾項目、114 個 `var/` 目錄、2 個 TT ledger OPEN）
與 SBL 施工的主題是**不同的專案面**。研究代理讀到 `var/` 時可能會看到 SBL 產物；它們被歸類為
「其他 session 的在建產物」，不屬本回合的處置對象。Far 研究代理被明確告知只做唯讀。

## 對「低風險」原則的影響

FAR 裁決若建議對 `var/` 做批次處置（歸檔、標記、刪除），本回合**不採用任何刪除**：

- `var/` 底下可能正在被其他 session 寫入（同一個 `var/` 根被多個回合共用）；
- 刪除不可逆，且會摧毀其他 session 的收據；
- 因此裁決只會建議「標記 / 歸檔索引 / disposition 記錄」，不建議刪除。
