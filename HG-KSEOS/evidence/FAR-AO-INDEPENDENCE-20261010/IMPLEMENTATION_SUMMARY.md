# FAR-AO-INDEPENDENCE-20261010 — 實作整理

> 本文件是 `FAR-AO-INDEPENDENCE-20261010` 輪的**實作整理**，與 `FAR-AO-INDEPENDENCE-20261010_EVIDENCE.md` 成對。
> 完整敘事、逐項探針、裁決與揭露見 EVIDENCE 文件；本文件只收斂「做了什麼、怎麼做、上限在哪」。

## 1. 一句話

把 AO/VERIFY/SECURITY 這條 lane 從「**看起來**獨立查核」改成「**在無人窗口下可被證明地獨立查核**」：閘門在 spawn 前 fail-closed 驗證 arm；被點名的 arm 必須**實際服務**該回合；受檢主體被改動時該回合**自我作廢**；回合的完整原始 bytes 落檔且可被第三方獨立重算。

## 2. 交付物（canonical subject）

| 檔案 | 角色 | sha256（前 16） |
|---|---|---|
| `scripts/hgk-lane-dispatch.py` | 派送器：身分閘門、required-arm、非變異守衛、原始 bytes 持久化、`--codex-executable` 接縫 | `5ee625a11fe5aa25` |
| `config/lane-route-slots.candidate.json` | pool 宣告（每 arm `identity_requirement`），status `CANDIDATE` | `c6e6c21fdf7bc04f` |
| `tests/test_lane_dispatch_ao_guard.py` | 34 個回歸測試（含以對抗式發現 F1–F13 命名的類） | `4d214dc5f0f911d4` |
| `tests/fixtures/stub_lane_child.py` | **確定性** checked child：在無模型情況下驅動守衛作廢路徑 | `8dc7e9d08235dc78` |
| `openspec/specs/ao-lane-independent-verify/spec.md` | main spec（+16 requirements，已由 archive 套用） | `c211866296ca3b40` |

## 3. 機制（四個關鍵設計）

1. **驗證後放行，不是排除**：OAuth arm **留在**無人 pool 內；閘門在 spawn 前檢查其憑證可 refresh。不健康 → `ERR_RELAY_OAUTH_NEEDS_REAUTH`（exit 4）並且**不 spawn**，**不**靜默改跑別的 arm。
2. **required ＝ served**：`--require-arm` 的檢查在 gate 分支**之外**，且以 **pre-gate 候選集**判定；閘門放行卻由別的 arm 服務 → `ERR_REQUIRED_ARM_NOT_SERVED`（exit 3）。要確保用到某 arm，必須**同時**釘 rank。
3. **守衛是條件必備**：升權 lane 必須帶 `--guard-subject`；根無法解析 → `ERR_GUARD_ROOT_MISSING`（0 attempts）；根包含 harness 自身輸出 → `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`；`removed/changed` 使該回合 verdict 作廢（`added` 記錄但不致命）。
4. **位元組保真**：子行程輸出以 bytes 捕獲、原樣落檔；receipt 記 `stdout_bytes` / `stdout_byte_exact`，第三方可重算（E6c/E6d 已示範 `MATCH_ALL=True`）。

## 4. 測試狀態

- `tests/test_lane_dispatch_ao_guard.py` → **34/34 OK**。
- 全量 holdout：**366 tests / 7 FAIL**，失敗 ID 集合與變更前基線**完全相同** → **0 引入**。
- 確定性負測矩陣 E11a–E11e **全 PASS**（其中 E11b/E11c 是「本應通過卻被守衛作廢」的最強形式）。
- `openspec validate --strict` → valid。

## 5. 獨立驗收（已落帳，非自判）

`REQ-AO-INDEP-012` → **ACCEPTED**（v4）；`ACC-AO-INDEP-012` → **PASS**。判決由**獨立 checker lane**（獨立 CODEX CLI 行程，338.72s，`usage 200`）產生，且該 lane **自行再跑了一次巢狀 `--force-rank 4 --require-arm` 實測**；maker 僅以 fail-closed 規則**機械化轉錄** verdict。5 筆 canonical events、2 筆 evidence_refs 皆走型別化 API。

## 6. 上限（不可越界）

- 本輪為 **local verification ＋ owner-approved promotion ＋ process-only independence**；**promotion ≠ acceptance**。
- 三條 lane **同模型**（owner D-3 裁決）：maker==checker 在構造上可達，**不得**宣稱模型多樣性。
- 守衛是**偵測非阻止**；瞬時改寫／還原偵測不到；守衛根以外未量測；F10／F13 未關閉。
- AO / checker verdict 一律 **ADVISORY**。
- `(ii)` 專用 relay-pool 帳號**撤銷為 NOT APPLICABLE**（owner 僅一個帳號）；殘餘為**共用失效域**，緩解是閘門 fail-closed 而非身分分離。

## 7. 本輪自我揭露（實作面）

首版守衛根缺失回報「乾淨」（D-4 空泛通過）、A1–A4 首版 A3 假陽性、manifest／run log 自我指涉 3 次、首版 F6 測試誤 spawn 一回合、acceptance 步驟成本低估（實測 27 列 `usage 200`）。全部已修並在 EVIDENCE §7 具名揭露。
