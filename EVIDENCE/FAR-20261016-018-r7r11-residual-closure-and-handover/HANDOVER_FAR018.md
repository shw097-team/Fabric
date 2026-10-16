# HANDOVER — FAR-20261016-018 (R7～R11 殘留結案與移交)

checkpoint: `CK-FAR018-R7R11-RESIDUAL`
generated_utc: 2026-10-16T11:30:48.708584+00:00
claim ceiling: **LOCAL**；`canonical_AO_acceptance` = `NOT_ISSUED`

## 1. 這一輪做了什麼（一句）
在 HG-KSEOS 為唯一控制平面下，用 FAR 對 R7～R11 歸檔輪的 118 項殘留做研究，產出一份排名裁決，
並執行其中 agent 可執行者（A1–A6），其餘（OG1–OG8）只備妥單一動作形式。

## 2. 交接狀態
- 殘留總數 **118**；W2 缺陷 **5**
- 本輪動作：A1–A6；其中 A1 機制已證、A2/A3/A4/A5 產物齊備並各自通過自測
- WorkOrders: 0（project `FAR-018-R7R11-RESIDUAL`）
- Kanban：17 卡 / 67 次 CLI

## 3. 車道與模型（本輪實測）
- EXECUTE：`opencode-go/deepseek-v4.1-flash`，required==served，nonce 存在，exit 0，804.28s
- VERIFY：`openai-codex/gpt-6.1-sol`，required==served，nonce 存在，exit 0，187.73s
- 模型軸多樣性：**PRESENT**
- checker 未動受測物：`CLEAN`（9 檔前後一致）

## 4. 獨立覆核結果（原話保留）
- overall `PARTIAL`；逐項 {"V1": "AGREE", "V2": "UNVERIFIABLE", "V3": "AGREE", "V4": "AGREE", "V5": "AGREE", "V6": "AGREE", "V7": "UNVERIFIABLE"}
- disagreements（未吞）：0
- UNVERIFIABLE 兩項已在 `ADJUDICATION_AND_LIMITATIONS.json` 逐項裁定並**收斂主張**，未向上取整。

## 5. 下一步（單一動作形式，等 OWNER）
| id | 動作 | 為什麼必須 OWNER |
|---|---|---|
| `OG1` | peer chain #6/#8/#10 merge | 授權邊界，非技術難度 |
| `OG2` | R7-02 validator cross-repo code promotion | 授權邊界，非技術難度 |
| `OG3` | R7-04 Fresh G1 owner certificate | 授權邊界，非技術難度 |
| `OG4` | canonical codex_executable pin repair | 授權邊界，非技術難度 |
| `OG5` | KP R04 polarity (20 clauses) + source#6 status | 授權邊界，非技術難度 |
| `OG6` | immutable checker boundary (distinct OS identity) | 授權邊界，非技術難度 |
| `OG7` | PR #12 promotion out of draft | 授權邊界，非技術難度 |
| `OG8` | guard predicate precision (runtime plane) | 授權邊界，非技術難度 |

## 6. 復原指引（resume）
1. 讀 `RESIDUAL_REGISTER.json`（每項殘留的 owner 與殘留說明）
2. 讀 `FAR_RULING.md`（裁決與非目標）
3. 讀 `ADJUDICATION_AND_LIMITATIONS.json`（checker 的 UNVERIFIABLE 如何被收斂）
4. 讀 `lane/VERIFY_ATTEMPT1_REFUSED.json`（第一失敗與其修法）
5. 重導：`python -B self_check.py --negative-control`（14 項＋14 種注入變異）

## 7. 未關閉者（誠實清單）
- `R7-03` 的**正式**關閉：本輪只證機制＋收斂，邊界不可解除需要不同 OS 身分（OG6）
- `R7-02`、`R7-04`、canonical pin、peer chain、KP R04、PR #12、guard 精度：皆 OG
- A1 的「由 checker 本人執行」：其沙箱為唯讀，故仍開放（已載於裁定檔）
- `Fabric` root `AGENTS.md` 缺席：已具名，未補（屬 Fabric 擁有者）

