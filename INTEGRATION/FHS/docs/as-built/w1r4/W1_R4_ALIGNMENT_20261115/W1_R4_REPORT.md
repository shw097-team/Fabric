# W1 r4｜把 W1 補齊到 13 章（2026-11-15）

**輪次**：`W1_R4_ALIGNMENT_20261115`｜**母本**：`W1-REPAIR-r3-2026-11-15` sha256 `5aca7b5e2bdc…`
**依據**：FAR `FAR-W1R3-ALIGN-20261115` 裁決 D1／D2／D6／D8／D9（owner 2026-11-15 授權執行）
**Claim ceiling**：`AUTHOR_W1_CHECK / LOCAL_CHECK / NOT_NATIVE / NOT_INDEPENDENT / NOT_RELEASE`

---

## 一、這一輪修的是 FAR 抓到的什麼

FAR 的 F2／F3 證明：W0 交付版把 **13 章**指派給 W1，r3 的八張 WP 卡只覆蓋 **8 章**，
`CH-13／CH-14／CH-16／CH-20／CH-39` 五章有主責契約卻沒有卡、沒有裁判、沒有案例；而它們不是 W2–W4 的工作。
本輪把這五章補成可執行裁判，並補上 FAR 列為欠帳的三件（七個 VN 增量、24 槽一版決定內容、gate 逐檔 SHA）
與 D6 的四件無人值守閉環契約。

## 二、實測（全部由收據計算）

| 段 | 內容 | 結果 |
|---|---|---|
| A | 八張 r3 WP 卡 ＋ 五張章卡 ＋ 七個 VN ＋ 24 槽 ＋ 四契約 | **142/142 PASS** |
| B | F01–F18 證據存在 | **18/18** |
| B2 | F01–F18 證據**逐檔重算 sha256** 且 JSON 可解析 | **18/18** |
| C | GJ01–GJ03 旅程 | **17/17** |
| D | 六效果條款 | **6/6** |
| E | **13 個 W1 章各有一張卡且 POS 通過** | **13/13** |
| SELFTEST | 變異自檢（清空 evidence／借別 scope／刪必要欄位） | **8/8** |
| 合計 | gate | **`PASS`，failures 0** |
| NEG 導出 | 由 POS 單點變異導出並寫入 | **70 案** |

裁判模組（逐檔 sha256 前 16 碼）：

| 模組 | bytes | sha256 |
|---|---|---|
| `ch_ch13.py` | 3,371 | `336fc7e7e820472c…` |
| `ch_ch14.py` | 3,703 | `219f3eb3c122a21f…` |
| `ch_ch16.py` | 3,004 | `f035bb11a08349e5…` |
| `ch_ch20.py` | 2,963 | `fbb989974bf2ce1e…` |
| `ch_ch39.py` | 3,487 | `0e2973f1117b8c04…` |
| `vn_referee.py` | 4,277 | `aa3d6769d2bd7a07…` |
| `slot_referee.py` | 4,081 | `802cab5c7e6ad855…` |
| `loop_referee.py` | 4,968 | `46b8fbfb2cd1483e…` |

## 三、五章卡各自的拒收語義（正文原文碼，未新造）

| 章 | 卡 | 層數 | 首拒碼 | 典型 NEG |
|---|---|---|---|---|
| CH-13 Authority SourceFreeze／Profile／18 PI | `ch_ch13.py` | 6 | `SOURCE_POLARITY_OR_PARENT_LOSS` | 丟「不得」、Parent 計數冒 Child、taxonomy 改 OriginalID、veto 減義、PI 領域空 |
| CH-14 PD-01..10／RepoContext／晚綁 | `ch_ch14.py` | 6 | `PD_CONTEXT_STALE_OR_UNBOUND` | remote main 冒本機 HEAD、path 字串冒權限、reparse 未宣告、dirty 自動 clean、前像缺 |
| CH-16 跨庫 Typed ABI／五 Seam | `ch_ch16.py` | 5 | `ABI_JOIN_MISMATCH` | 只畫箭頭、五 seam 共用一個 ACK、join key 缺、timeout 猜成 ACK |
| CH-20 Hermes Kanban／Delegation／Swarm | `ch_ch20.py` | 6 | `UNKNOWN_RECONCILE_REQUIRED` | 第二排程器、lease 缺、blind retry、卡片 Done 冒世界結果、共用 home |
| CH-39 安全 SoD／ACL／秘鑰／Consent | `ch_ch39.py` | 6 | `AUTHORITY_OR_SECRET_SCOPE_DENY` | 四角色同一 principal、argv 帶 secret、來源指令擴權、DEV grant 做 HOST_OPS、自簽 independent |

## 四、三件欠帳怎麼補

1. **七個 VN 增量（VN-08…VN-14）**：`vn_referee.py` 逐增量驗「原域 writer 產出 ＋ 同 scope ACK ＋ 該增量自己的 POS 條件」，全部以 `ORIGINAL_SCOPE_NACK` 拒收；七個增量各 4–5 案。
2. **24 槽一版決定（CH-22）**：由 r3 的 24 個 `R6:SLOT` 區塊機械抽出（occupant／pin／POS／NEG／license／primary wave+WP，逐槽帶行號），落成 `slot_referee.py` 的內容判準：24/24 覆蓋、欄位非空、license 狀態明示、W1 槽的 WP 必須是八個 W1 WP 之一、每槽恰一個 active occupant。抽出的 24 槽中有 **3 槽** 的 license 記 `HOLD`（Fabric/HGK 根 LICENSE 未取得），如實標示。
3. **gate 逐檔 SHA（原 r3 的 B 段只驗存在）**：B2 段對 F01–F18 引用的每個檔案**重算 sha256**，並要求 `.json` 可解析、bytes > 0；18/18 通過，逐檔 digest 落 `out/GATE_W1R4.json`。

## 五、四件無人值守閉環契約（D6）

`loop_referee.py`：`checkpoint`（work_id／cursor／artifact_digests／written_at）、`resume`（same_key、不重播、completed 不得回到 to_run）、
`watchdog`（evidence_delta > 0、identical_action_repeat ≤ 3）、`budget`（turns／tokens 上限，耗盡須落 `ABORTED_OR_PARTIAL` 而非靜默停）。
四契約各有 POS 與一個 NEG，全部在第一層拒絕。

## 六、怎麼跑

```bash
PY=C:/Users/user/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe
cd C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W1_R4_ALIGNMENT_20261115
$PY build/normalise_pos.py          # 只補結構信封，不動 evidence
$PY build/derive_r4.py              # POS＋單點變異 → 全部 NEG
$PY build/loop_negs.py              # 四契約各自的 NEG
$PY build/gate_w1r4.py --selftest   # 期望 PASS，failures 0
```

## 七、未主張與 HOLD

- 未主張：`NATIVE_SIGNED`、`INDEPENDENT_PASS`、`RELEASE_GRANTED`、原域接受。
- 原權限 HOLD 未解（本輪不碰）：`H-ENTRY`、`H-GUARD-RAW-MISMATCH`、`H-RETIREMENT-BOUNDARY`、`H-READER-PIPD`、`H-SUPPLYCHAIN-RAW`、`H-ORIGINAL-CASE-RUNNER`。
- 24 槽中 3 槽的 license 仍是 `HOLD`；本輪只把它標示出來，沒有替原 Owner 補 LICENSE。

## 八、更正紀錄

`docs/CORRECTIONS.json` RC-R4-1…RC-R4-6：無工具派工失敗、三次 lane 產物不一致後的升級、core 的 require 簽名、fixture 結構信封、CH-16 層位修正、FALSE_GREEN 自檢的 N/A 判定。
