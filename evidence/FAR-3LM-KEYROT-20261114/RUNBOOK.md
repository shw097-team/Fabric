# 3LM 車道憑證輪替｜Runbook（v1，施工定案）

> 適用：`OPENCODE_GO_API_KEY`（3LM lane provider key）。單人單機。
> 原則：金鑰值**只**出現在兩個地方——原始憑證檔，與子程序的環境變數。不出現在 argv、日誌、收據、文件、commit。
> 本 runbook 不含任何金鑰值；收據只記 `sha256` 前 12 碼與長度。
> **本文件狀態**：v2 腳本已在 2026-11-14 以 dry-run 與 `--pin-refresh`（唯讀）實跑通過；**尚未**對任何新憑證執行 `--apply`。

## 0. 前置（一次就好）

1. 確認 `ops/3lm_consumers.json` 的 `consumers` 清單是完整的（目前 2 筆）。
2. 確認 Python：`<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe`。

## 1. 取得新金鑰（Owner）

把新 key 存成單行、無 CR、無尾隨換行的 UTF-8 檔，例如
`<WORKSPACE>\API KEY\shw098_OPENCODEGO_KEY.txt`。
**不要**貼進聊天、命令列參數或工單。

## 2. 乾跑（不改任何檔案）

```bash
cd <WORKSPACE>/FHS_NEXT_Workspace/FAR_3LM_KEYROT_20261114
PY="<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
"$PY" ops/rotate_3lm_key.py --key-file "<WORKSPACE>/API KEY/shw098_OPENCODEGO_KEY.txt"
```

預期：`verdict: PASS`、列出每個 consumer 的 `changed`、`probe_ok: true`、`secret_printed: false`。
若 `changed: true` 的 consumer 與你預期不符 → **停**，修 manifest 的 `pattern`。
（設計註記：本輪建置期間，`r1_host_readback.py` 的樣式曾誤命中另一行 `pathlib.Path(...)`；已改為
`keyf\s*=\s*pathlib\.Path\(...\)`。乾跑預設就是為了在寫檔前抓到這一類誤命中。）

失敗碼：`2 KEY_FILE_MISSING`／`3 KEY_FILE_MALFORMED`／`4 CONSUMER_PATTERN_MISS`／`6 PROBE_FAILED`／`7 PROBE_BINARY_MISSING`。

## 3. 套用

```bash
"$PY" ops/rotate_3lm_key.py --key-file ".../shw098_OPENCODEGO_KEY.txt" --apply
```

它會：每個 consumer 先備份 `<file>.bak-<UTC>` → 改指標 → 印出重啟指令 → 跑探針 → 寫
`out/ROTATION_RECEIPT_<UTC>.json`。

## 4. 重啟（唯一的手動步驟）

- `desktop-model-router`：重新啟動 router 或重啟 Codex 桌面 App（它只在啟動時讀 `$env:OPENCODE_GO_API_KEY`）。
- `hgk-host-readback`：無常駐程序，下次執行即生效。

## 5. 驗收（Definition of Done，四條）

1. 收據存在且 `secret_printed = false`。
2. 探針 `exit 0`，stdout 含 `CHECKER_OK`（provider `opencode_go`、model `deepseek-v4.1-flash`）。
3. 新舊 fingerprint 不同；舊指標檔仍在（回滾窗口）。
4. 收據路徑寫進當輪的 evidence index。

再跑一次乾跑即可確認可重跑（乾跑本身就是完整驗證，不寫檔）：

```bash
"$PY" ops/rotate_3lm_key.py
```

## 6. 回滾

```bash
# 逐檔還原（把 <UTC> 換成收據裡的時間戳）
cp "<consumer 檔>.bak-<UTC>" "<consumer 檔>"
# 重啟 consumer，再跑乾跑（等同驗證）
"$PY" ops/rotate_3lm_key.py
```

## 7. 同一個形狀的第二件事：toolchain pin

3LM dispatcher 在 codex binary pin 失效時會直接拒絕 spawn（`ERR_LANE_PIN_IDENTITY_INVALID`）。
這與金鑰漂移是**同一類**問題，用同一支命令處理，但預設關閉、需 Owner 核准：

```bash
"$PY" ops/rotate_3lm_key.py --pin-refresh                                  # 唯讀漂移報告，不改任何檔
"$PY" ops/rotate_3lm_key.py --pin-refresh --i-approve-pin-change --apply  # 需 Owner 明確核准才寫入
```

核准後才會備份 `HG-KSEOS/config/hermes-codex-lane.json` 並更新 `codex_executable`／`codex_version`／`codex_sha256`；
未核准時只輸出 `pin_drift`（宣告路徑是否存在、實裝路徑與版本），不改檔。

## 8. 不要做

- ✗ 用 provider `/v1/models` 當有效性判準（有效與無效 key 都回 403，2026-11-14 實測）。
- ✗ `setx` 或寫進 shell profile（值會進 registry／歷史，且既有 file-pointer 已足夠）。
- ✗ 把 key 貼進聊天、argv、日誌、收據、commit。
- ✗ 建 cron 自動輪替（Owner 才是發行者；無人值守會多出一個特權）。
- ✗ 為了輪替而引入 vault／secret service（單人單機，違反最小可行）。

## 9. 維護面

- 新增 consumer：在 `ops/3lm_consumers.json` 加一筆（`label`／`file`／`pattern`／`restart`），乾跑確認 `changed` 正確即可。
- 這份 runbook 與 manifest 是**唯一**需要長期維護的兩份東西。
