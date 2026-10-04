# FAR r8 歷史接受基準（Historical Baseline — Immutable Record）

> Document ID: `FAR-R8-HISTORICAL-BASELINE-20260813`
> 本檔記錄 FAR 外部驗收歷史基準與其後 supersession 鏈，確保 r8 驗收 verdict 永不模糊。

## r8 外部驗收（原始接受基準）

```text
report_id          = FAR_FINAL_EXTERNAL_ACCEPTANCE_REPORT_20260813_R7_ALL_PASS（+ r8 master 延伸）
verdict            = PASS_CHALLENGE / FAR_EXTERNAL_FINAL_ACCEPTANCE = GRANTED / FAR-R1 = PASS
conditions         = 14/14 PASS; blocking contradiction = 0; blocking evidence gap = 0
evidence_md        = FAR_FINAL_ACCEPTANCE_EVIDENCE.md
evidence_sha256    = 58de08155b2565c342a3df28cfa3c2f899bd5603f7047cf51e94f0c9860738f2
evidence_bytes     = 76,214
subject_root       = 5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a（95 files）
reviewer           = Fabric External Independent Challenge Reviewer（challenge-review; read-only）
acceptance_scope   = local implementation conformance; production/SQS live/remote = NOT_CLAIMED
```

## Supersession 鏈（post-acceptance additive updates）

| 階段 | 事件 | Evidence MD hash | 說明 |
|---|---|---|---|
| r8 | 外部驗收簽發（58de0815 由 reviewer 全量 readback 驗證） | `58de0815…` | immutable verdict; 檔後續被 additive 更新（不變 verdict 本身） |
| post-activation | FAR 啟用 + docs（README/USERGUIDE/AGENTS）+ NBO-01/02/04 清理 | `eff79b73…`（歸檔: `FAR_FINAL_ACCEPTANCE_EVIDENCE_post-activation_eff79b73.md`） | additive; 驗證核心證據不變 |
| TRI-SOURCE | WO-FAR-TRISOURCE-001 ChangeSet（本輪） | `b0b21ced799face7…`（canonical current） | 新 subject; 依 TRI-SOURCE §1: new bytes = new post-acceptance subject, 需 focused acceptance |

## 規則

```text
1. r8 verdict（PASS_CHALLENGE / GRANTED / FAR-R1 PASS）為不可變治理記錄（r7/r8 報告檔 immutable）
2. Evidence MD 檔為 per-subject evidence wrapper; post-acceptance ChangeSet 產生新 subject 並重新 frozen
3. 58de0815（76,214B）為歷史接受基準; 不 pretend 覆蓋新 bytes（TRI-SOURCE §1 精神）
4. 所有 hash 引用指向 canonical current（b0b21ced799face7…, 四處 mirror byte-identical）
```

```text
STOP
R8_BASELINE = 58de0815…（historical, verdict immutable）
CANONICAL_CURRENT = b0b21ced799face7…（TRI-SOURCE subject; focused acceptance in progress）
```
