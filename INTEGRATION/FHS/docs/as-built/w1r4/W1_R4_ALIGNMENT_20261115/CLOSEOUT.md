# CLOSEOUT｜W1_R4_ALIGNMENT_20261115

## 一、這一輪的目標與依據
FAR `FAR-W1R3-ALIGN-20261115` 裁決 D1／D6／D8／D9，owner 2026-11-15 授權執行：
把 W1 從 r3 的 **八章** 補到 W0 交付版指派的 **十三章**，並補齊三件欠帳與四件閉環契約。

## 二、實測結果（全部來自收據）

| 段 | 內容 | 結果 |
|---|---|---|
| A | 八 WP ＋ 五章 ＋ 七 VN ＋ 24 槽 ＋ 四契約 | 142/142 |
| B | F01–F18 存在 | 18/18 |
| B2 | F01–F18 **逐檔 sha256 重算** ＋ JSON 解析 | 18/18 |
| C | GJ01–GJ03 | 17/17 |
| D | 六效果 | 6/6 |
| E | **13 章覆蓋** | 13/13 |
| SELFTEST | 變異自檢 | 8/8 |
| gate | — | **`PASS`，failures 0** |
| NEG 導出 | 單點變異 | 75 案，0 未寫入 |

## 三、收斂（凍結判準 V1–V8）
| 輪 | 失敗 | 判定 | 原因 |
|---|---|---|---|
| 1 | 6/8 | `REVISE` | V2 | chapter-specific refusal code | `got=NACK` does not evidence each declared  |
| 2 | 1/8 | `REVISE` | V8 | every NEG has a single-point derivation | 70 rows equal 29 chapter + 34 VN  |
| 3 | 0/8 | `APPROVED` | NONE |

最終 `APPROVED`。失敗數 6→1→0，單調不增。
**不宣稱 `INDEPENDENT_PASS`**：同家族模型、另一 context／lane 的 verify。

## 四、交付
- Fabric：`shw097-team/Fabric` PR **#65**，commit `37aa6d55`，分支 `w1r4/evidence-20261115`（10 檔，逐檔 byte 回讀一致）。
- 產品：`shw097-team/FHS_vNEXT` PR **#2**，commit `9e305fab`，分支 `w1r4/referees-20261115`（138 檔，逐檔 byte 回讀一致）。
- OpenSpec：`w1r4-thirteen-chapter-w1-closure`，`openspec validate --strict` 通過。
- 回寫帳：`out/WRITEBACK_LEDGER.json`（6 條；上游 L0／L1／L2 判定 `NOT_PERFORMED_BY_DESIGN`）。

## 五、未主張、未解、留在原域
- 未主張：`NATIVE_SIGNED`、`INDEPENDENT_PASS`、`RELEASE_GRANTED`、原域接受。
- 六個原域 HOLD 未解：`H-ENTRY`、`H-GUARD-RAW-MISMATCH`、`H-RETIREMENT-BOUNDARY`、`H-READER-PIPD`、`H-SUPPLYCHAIN-RAW`、`H-ORIGINAL-CASE-RUNNER`。
- 24 槽中 3 槽 licence 記 `HOLD`（原 Owner 未提供 LICENSE），本輪只標示未補。
- D7：FAR memory 通道 `UNAVAILABLE`（spine DB 不存在，已實測）、web `DECLARED_NONE`；以 `docs/FAR_CHANNEL_WAIVER.json` 具名 waiver，未自授。

## 六、車道誠實紀錄
EXECUTE 車道（Codex CLI，deepseek-v4.1-flash）第一輪因提示含工具指令而全數空轉；第二、三輪產出的章卡自相矛盾
（POS 過不了自己的層、`Refusal` 缺層號、簽名漂移）。**已升級為 Commander 親寫五張章卡與 VN 裁判**，並在
`docs/CORRECTIONS.json` RC-R4-2 記為 `LANE_ESCALATION`。裁判仍是 gate 判，不是作者判。
