# FAR RULING — FAR-20261016-018 (R7～R11 殘留結案與移交)

generated: 2026-10-16 · round `FAR-20261016-018-r7r11-residual-closure-and-handover`
inputs: `W1_RESIDUAL_UNIVERSE.json` (118 items, independent lane), `W2_DEFECT_DOSSIER.json` (5 defects,
independent lane, measured), `ROUTE_CHECK.json` (this round's live measurements)
claim ceiling: **LOCAL** — 本地可重導的完成；外部接受仍待真實驗收官。

## 0. 計數（全部自 artifact 導出）

| 來源 | 數量 |
|---|---|
| W1 殘留總數 | 118（RESIDUAL 18／GAP 28／BLOCKED 14／OWNER_DECISION 14／UNLANDED 13／CLOSED_ALREADY 31） |
| 其中 agent 可執行 | 11（8 已結案，**3 仍開放**） |
| owner-gated | 58（P0：`R7-03-ISOLATE`、`R7-04-FRESH-G1`、`CANONICAL-CODEX-PIN`） |
| other-round | 49 |
| W2 缺陷 | 5（D0 guard 誤擋、D1 車道 pin stale、D2 T2 傳輸敘述修正、D3 隔離可行性、D4 索引僅部分可重建） |

## 1. 可立即執行集（agent 已執行，非計畫）

| # | 動作 | 摩擦 | 可行 | 必要性 | 過度工程？ | 對齊 | 授權 |
|---|---|---|---|---|---|---|---|
| **A1** | 落地可失敗的 OS 強制唯讀 harness（`checker_isolation_probe.py`）＋ 自測變異必須被抓到 | 低（僅用既有 `icacls` 與既有 probe 模式） | 高（已實測可行） | **P0**：`EIA-02`／`R7-03` 的機制從未以可重導形式落地 | 否：不引入新 verifier 系統，只把已證機制收斂成一個可重用探針 | 直接對應驗收報告對 checker 隔離的要求 | 本輪 |
| **A2** | 去真空化上一輪 harness 的 S8b（`self_check_v2.py`，含負控制） | 低 | 高 | **P1**：上一輪的 S8b 把成功值寫成字面 `True`，探針不可能失敗（W1 證實） | 否：修一個既有檢查，不新增平台 | KP11-R01「PASS 需 raw evidence」 | 本輪 |
| **A3** | 由 5 條已驗證指標重建 skill 索引（`regen_entry_map.py` ＋ `entry_map.json`），並宣告僅為部分重建 | 低（指標 offset/length/sha256 **5/5 全等**） | 高 | **P1**：該 skill 自身的 refusal-first 規則目前無法滿足 | 否：從既有指標資料生成，不重建已搬移內容 | `EIA-07` | 本輪 |
| **A4** | 可變活體來源的 metadata 語義（`subject_mutability`／`hashed_at`／排除於 byte-exact 主張） | 低 | 高 | **P2**：`E2` 已量到 stale snapshot 被當 byte-exact | 否：欄位語義修補，非新 DB | `EIA-06` 家族、KP16-R01 | 本輪 |
| **A5** | 去真空化 K-ledger 的 `source_linked` 存在指示（改為對照 ledger ID 集，可失敗） | 低 | 高 | **P2**：`E4` 證實該子欄位逐列硬編 | 否：同一 artifact 內修規則 | KP11-R01 | 本輪 |
| **A6** | 殘留暫存器（W1＋W2 合併）＋本裁決 ＋ 移交 checkpoint ＋ 單一證據 MD ＋ 推送新前綴並遠端 readback | 中（發布需 broker） | 高 | **P0**：指令明列結案／移交為交付物 | 否：沿用既有 publish broker 與 pack builder | 指令第 8／9 節 | 本輪 |

## 2. OWNER-gated（僅備妥單一動作形式，**未執行**）

分界線是**授權**，不是難度。以下即使有「預先授權執行裁決」也不能由 agent 完成：

| # | 項目 | 為何必須 OWNER | 備妥形式 |
|---|---|---|---|
| **OG1** | peer chain `#6/#8/#10` 合併 | 合併＝維護者權力；你已指示「另批」 | 三支 `mergeable=true`；dry-run 收據已有；一句授權即可執行 |
| **OG2** | `R7-02` validator 程式碼跨 REPO 晉升 | 另一 repo 的 code release | 需 PIPD Validator Owner 的變更集與 oracle |
| **OG3** | `R7-04` Fresh G1 | 需 Owner 對「最終生效 runtime」簽核 | 需一筆 owner 現場紀錄（binary hash／version／epoch／served arm） |
| **OG4** | canonical `codex_executable` pin 修復（D1） | 控制平面編輯，超出本輪 change class | 單行替換＋hash readback＋T1 重跑；已有效能等價的 round-local 繞行 |
| **OG5** | KP R04 極性 20 條 ＋ source#6 狀態 | 條文所有權 | 需 Authority/KP Policy Owner 文字修補與反例測試 |
| **OG6** | **真不可解除的 checker 隔離邊界**（D3 新裁決） | 需要**不同 OS 身分**或特權 ACL 決策 | 本輪已證「普通拒絕可行、同身分可自行解除」；要正式關 `R7-03` 必須由 Owner 決定身分模型 |
| **OG7** | `PR #12` 轉 Ready／合併 | 發布權 | 維持 Draft；33 檔、head `0a30e5a8` |
| **OG8** | guard 誤擋精度修正（D0，新） | Hermes runtime plane 政策 | 誤擋實例已留存；修法是讓 guard 回到其自述的「意圖動詞 ∧ 目標詞」雙條件 |

## 3. 新裁決（本輪才量到，必須記入移交）

1. **`R7-03` 只能部分由 agent 達成。** 實測：owned 目錄 → baseline 寫入成功 → `icacls /deny <identity>:(OI)(CI)(W)`
   → `PermissionError [Errno 13]` → 移除 ACE → 寫入恢復 → 清理已驗證。但**同一個身分可以解除自己的 deny ACE**，
   故證明的是「普通 OS 拒絕」，**不是不可解除的安全邊界**。正式關閉 `R7-03` 需要 OG6。
2. **上一輪的自我檢測有真空探針。** `S8b` 的成功值是字面 `True`，且計算出的變數從未被使用 →
   不可能失敗。這是獨立車道對 maker 綠燈的成功偽證，已列 A2。
3. **`T2` 缺陷的敘述要修正（D2）。** 準確說法是：T2 的 throwaway home **未提供傳輸覆寫**，
   而不必然是「打到公開端點」；dispatcher 則顯式覆寫到 relay（量測當下 relay 傾聽中）。
   先前較粗的敘述應以本條取代。
4. **guard 有一類系統性誤擋（D0）。** 一份**僅列舉該 skill reference 檔名**的證據 artifact 被 fail-closed
   擋下；子代理正確停手回報而非繞道。修復屬 OG8。
5. **contract schema 無處安放「應存在而缺席的檔」。** `source_scan.missing` 是來源**家族**集合，
   且禁止額外頂層鍵，故缺席的 `Fabric/AGENTS.md` 無法在 contract 內宣告，只能在殘留暫存器具名。
   （上一輪 contract 同樣是空清單，同一原因。）
6. **「搜尋＋複用」與 prompt 去重彼此拉扯。** 本輪 contract 沿用上輪 scaffold，duplication 比 **0.596**。
   裁決：結構 scaffold 複用勝出（本地治理一致性 > shingle 相似度），但**實際餵給執行車道的 writer brief 為新撰**，
   且 duplication 應以「被執行的 prompt」而非「計畫 contract」為標的。

## 4. 非目標（不重新開啟）

full 221／G-A～H、production 晉升、`.hgk/` 遷移、任何已合併 R6～R11 證據的改寫、重新瘦身兩支 skills。
`full_convergence_verdict` 維持 `TEMP_CLOSED_CHALLENGE`、`production_verdict` 維持 `FAIL_CLOSED`、
`canonical_AO_acceptance` 維持 `NOT_ISSUED`。

## 5. 執行順序與停止語義

執行 A1→A6（EXECUTE 車道 `opencode-go/deepseek-v4.1-flash`）→ 以**不同模型軸**覆核
（VERIFY pinned `openai-codex/gpt-6.1-sol` rank2，`--require-arm`）→ 發布 → readback → 移交。
任一 stop condition（`ERR_LANE_REQUIRED_ARM_ABSENT`、`PREFIX_ESCAPE`、`SECRET_FOUND`、
`CHECKER_CAN_MUTATE_SUBJECT`、`ACL_UNENFORCEABLE`）只停受影響動作，記錄 raw first-fail 與最小下一步，**不向上取整為 PASS**。
