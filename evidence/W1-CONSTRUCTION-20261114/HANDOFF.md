# W1 交接（2026-11-14）｜W1_R2 施工輪 → W2／W3／W4

## 只交五件

| 交接物 | 內容 | 接收方 |
|---|---|---|
| Source | 每條引用的檔案＋sha256（見 `out/P0_SOURCE_IDENTITY.json`） | 原域 Reader |
| OriginalID | 485 逐鍵（`out/WP17_485_LEDGER.json`）、39 格（`out/WP20_MODEGATE39.json`）、13 主責章不改名 | 原 Writer |
| Case | `AUTHOR.W1.<WP>.POS/NEG/SEC`（本輪 7 個 typed NEG 已具名） | TQAEP／Oracle |
| ExpectedRaw | 每個 case 的退出碼與 typed code（見報告 §2、§3） | 原 Runner |
| HOLD | 報告 §9 六列，各列有解除條件 | 原 Owner |

## 不可交接
TraceClosure、獨立 Checker 結論、Publisher cutover、任何 Native／Release 狀態。

## 下一波入口

- W2 必讀：`out/WP02_WP03_READONLY.json`（policy/issuer 現況）、`out/WP05_BUNDLE4.json`（ECP/TQAEP 形狀）
- W3 必讀：`out/WP17_485_LEDGER.json`（Need→單一 Occupant 的母表）、`out/WP20_MATRIX.json`（Host×Kind）
- 續行：WorkID 與 cursor 在 `out/WP04_RUNTIME.json`；重跑順序見 `KANBAN_W1_R2.md`

