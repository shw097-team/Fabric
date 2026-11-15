# Owner key 需求評估（本輪，2026-11-15）

**輪次**：`W1_R3_IMPLEMENTATION_20261115`（FHS vNEXT W1 r3 八 WP 作者契約可執行化）
**評估人**：FHS_NEXT 工作 profile（Maker／Commander）
**裁定依據**：業主指令「先評估，若可能需 OWNER 授權，就搜尋既有 owner key passphrase envelope 並開窗預授權」

## 一、本輪真的會發生的效果

| 效果 | 有沒有 | 承載 |
|---|---|---|
| `SOURCE_READ` | 有 | 讀 r3 正文、三庫進口位元、CATALOG／registry 唯讀 |
| `LOCAL_DRAFT` | 有 | 輪次內 `build/ out/ tests/ briefs/ openspec/` |
| `REPOSITORY_WRITE` | 有（後段） | Fabric `candidate` 分支＋PR、`shw097-team/FHS_vNEXT` 分支；憑證為 fine-grained PAT，非 owner key |
| `HOST_OPS` | 無 | 未安裝、未註冊、未改 Host profile |
| `USER` | 無 | 空寫集 |
| `RELEASE` | 無 | 未發行、未簽 release |

## 二、需要 owner key 的消費者（只有一個）

| kind | 為什麼需要 | 消費者 | 缺了會怎樣 |
|---|---|---|---|
| `owner_semantic_accept` | 讓本輪交付物由業主作「語義接受」，而不是由 Maker 自稱完成 | 業主本人（本輪 closeout、Fabric／產品 repo 交付） | 本輪停在 `AUTHOR_SELF_CHECKED_NOT_OWNER_ACCEPTED`；其餘 READ／DRAFT／推送不受阻 |

**明確不需要、也不會去簽**：`release`、`sourcefreeze`、`policy_authority`、`trust_anchor`、
`original_reader_ack`（原域 Reader 的角色，Maker 不得代簽）。

## 三、Op 預算（一次口令、批次簽）

| # | 擬簽 body | ops |
|---|---|---|
| 1 | 輪次交付摘要（gate 收據 digest＋cycles 最終 APPROVED＋逐檔 sha 清單 digest） | 1 |
| 合計 | | **1**（max_ops 設 8，留給補簽同一任務的同一 body 修正） |

## 四、開窗參數

```bash
python FHS_NEXT/owner_envelope/code/owner_window.py open \
  --task W1_R3_IMPLEMENTATION_20261115 \
  --ttl-hours 3 --max-ops 8 \
  --scope owner_semantic_accept \
  --workspace C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W1_R3_IMPLEMENTATION_20261115
```

口令只在 `open` 那一次輸入（遮罩視窗），之後 broker 以 headless 方式簽；桌面沒有視窗是正常狀態。
業主裁定：同一任務輸入一次口令即授權該任務的全部簽章，不逐件再問。

## 五、拒絕條件（fail closed）

- 窗過期／ops 用盡 → 不簽，交付物停在 `NOT_OWNER_ACCEPTED` 並在 closeout 具名。
- body digest 與收據不符 → 不簽（`REFUSED_PAYLOAD_SHA_MISMATCH`）。
- 任何要求把作者自檢寫成 Native／Independent／Release 的 body → 不簽。
