# 每 Host 安裝／載入／調用／卸載方案（W1 交付物，設計態）

**效力**：`LOCAL_DRAFT_WRITE / AUTHOR_DESIGN`。本檔是 L2 §04 W1 第三項交付（`每Host安裝/載入/調用/卸載方案`）的成文版本，
對應 `WP-FHS-11`（Portable Host Dogfood，原 EffectClass `HOST_OP`）。
**不主張**：任何 SP 已安裝、已載入、已調用、已卸載。每個 `HOST_OP` 步驟都需要 OPS ECP ＋ 原 Issuer ＋ nonce/TTL/epoch。
**已量測的現況**（`out/WP11_HOST_DOGFOOD.json`）：`Installed / Loaded / Invoked / Consumed = OBSERVED`（以既有 tree 與 profile 為證），
`Uninstalled = NOT_PROBED`（活機不卸載、不刪任何檔）；Portable SP：`TPM = PRESENT_IN_TREE`、`Commander = NOT_OBSERVED`、`Challenge = NOT_OBSERVED`。

---

## 1｜三個 Portable SP 的實際落點（量測，不是推論）

| SP | 在樹內的位置（量測） | 宿主落點（量測） | 狀態 |
|---|---|---|---|
| TPM | `FHS_NEXT/SBL/sbl_sp/plugins/tpm_sp` | Codex plugin cache：`%USERPROFILE%/.codex/plugins/cache/created-by-me-remote/sbl-tpm-sp`；Hermes profile 內**無**同名 skill | `PRESENT_IN_TREE`＋Codex 端 `PRESENT` |
| Challenge | 樹內僅見 `sbl-external-challenge-sp` 於 Codex plugin cache | `%USERPROFILE%/.codex/plugins/cache/created-by-me-remote/sbl-external-challenge-sp` | Codex 端 `PRESENT`；Hermes 端 `NOT_OBSERVED` |
| Commander | 無獨立套件（功能以 FHS skill 與 `WP07_COMMANDER_ABC` 呈現） | 無 | `NOT_OBSERVED` |

**宿主現況**：Hermes profiles `fhs_next`(45 skills)、`hgk-governed`(48)、`default`(90)；Codex lane home `%LOCALAPPDATA%/HG-KSEOS/codex-hermes`；
lane 宣告的執行檔 `…/OpenAI/Codex/bin/9e1da79431da526b/codex.exe`。四宿主中 `ChatGPT` 無本機安裝路徑。

## 2｜四宿主 × 三 SP × 五階段（每格：要做什麼／證據長什麼樣）

| 階段 | Hermes | Codex | ClaudeCode | ChatGPT |
|---|---|---|---|---|
| **Installed** | 把 SP 目錄放進 `%LOCALAPPDATA%/hermes/profiles/<profile>/skills/<category>/<sp>/`（內含 `SKILL.md`）；證據＝目錄存在＋`SKILL.md` 的 sha256 | 把套件放進 `%USERPROFILE%/.codex/plugins/cache/<vendor>/<sp>/`（內含 `plugin.json` 或 `manifest.json`）；證據＝同上 | `%USERPROFILE%/.claude/skills/<sp>/SKILL.md`；本機無此根 → `NOT_PROBED` | 無本機安裝面 → `NoFit: NO_LOCAL_SURFACE` |
| **Loaded** | 重啟該 profile 後，於該 profile 的 skill 清單看到該名稱；證據＝清單輸出（不是檔案存在） | `codex` 啟動載入 plugin；證據＝plugin 載入 log／`/plugins` 讀回 | 同上（無根則 `NOT_PROBED`） | `NoFit` |
| **Invoked** | 在同 profile 下實際觸發一次（例：TPM 產生一份 SPEC 草案）；證據＝該次輸出＋模型 `ActualServed` | 一個 `codex exec` 回合實際引用該 plugin；證據＝attempt log 的 `item.completed` | `NOT_PROBED` | `NoFit` |
| **Consumed** | 下游客戶端讀到該輸出（例：`pipd validate` 讀該 SPEC 草案） | 同左，以同 scope 的 Raw 為證 | `NOT_PROBED` | `NoFit` |
| **Uninstalled** | 移除目錄＋重啟 profile；證據＝清單不再列出、目錄不存在 | 移除 plugin 目錄＋重啟；證據＝同上 | `NOT_PROBED` | `NoFit` |

**不可跳階**：`檔案存在` 只能證 `Installed`；`清單列出` 才證 `Loaded`；`有一次真實輸出` 才證 `Invoked`；`下游客戶端讀到` 才證 `Consumed`。四者不得互推——這正是 `WP-FHS-11.FIRST_FAIL:HOST_SP_MATRIX_INCOMPLETE` 要擋的樣態（把一張安裝收據當成三 SP × 九格的完成）。

## 3｜逐步命令（可貼上；`$PY` 為釘定直譯器）

```bash
PY="<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
HM="<HOST_HOME>/AppData/Local/hermes"
SP="<WORKSPACE>/FHS_NEXT/SBL/sbl_sp/plugins/tpm_sp"

# Installed（HOST_OP；需 OPS ECP + 原 Issuer；未取得前只做 dry-run 檢查）
ls -la "$SP/SKILL.md"
"$PY" -c "import hashlib,pathlib;p=pathlib.Path(r'$SP/SKILL.md');print(len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest()[:16])"

# Loaded（重啟 profile 後讀清單；讀操作，不需 permit）
find "$HM/profiles/fhs_next/skills" -maxdepth 3 -name SKILL.md | sed 's#.*/skills/##' | sort | grep -i tpm || echo "NOT_LOADED"

# Invoked / Consumed（需在該 profile 的一次真實回合；輸出與 ActualServed 一起記）
#   → 證據落在該回合的 attempt log 與 out/ 下的新收據；本輪不執行

# Uninstalled（HOST_OP，且屬破壞性；活機不執行）
#   rm -rf "$HM/profiles/fhs_next/skills/<category>/<sp>"  ← 只在 Owner 授權且已備份時
```

## 4｜POS／NEG（每階段一組）

| 階段 | POS（可判定） | NEG（應拒／應標） |
|---|---|---|
| Installed | 目錄存在且 `SKILL.md` sha256 可重算 | 只放資料夾沒有 `SKILL.md` → `NOT_A_LOADABLE_UNIT` |
| Loaded | profile 清單列出該名稱 | 檔案在但清單沒有 → `INSTALLED_NOT_LOADED` |
| Invoked | 一次真實回合的 `agent_message` 引用了它，且 `ActualServed` 有列 | 只有「Selected」沒有 served → `SELECTED_NOT_SERVED` |
| Consumed | 下游客戶端（如 `pipd validate`）讀到該輸出 | 用宿主自己的 log 當下游證據 → `FOREIGN_EVIDENCE` |
| Uninstalled | 清單不再列出、目錄不存在、原檔有備份可還原 | 直接刪除無備份 → `NO_ROLLBACK` |

## 5｜HOLD／續行

- `H-SP-INSTALL`：任何 `Installed`／`Uninstalled` 皆為 `HOST_OP`，需 OPS ECP ＋ 原 Issuer；未取得前本方案只到 dry-run。
- `H-SP-MATRIX`：`ClaudeCode` 與 `ChatGPT` 在本機沒有安裝面 → 各自 `NOT_PROBED`／`NoFit: NO_LOCAL_SURFACE`，不得以 Hermes／Codex 的收據代填。
- 續行：先補 `TPM` 在 Hermes profile 的安裝（有備份、可逆），再依 §2 逐階收證；`Commander`／`Challenge` 需先確定套件來源（目前樹內只有 Codex plugin cache 的那兩份）。

## 6｜重現命令（驗證本方案與量測一致）

```bash
"$PY" -c "import json;d=json.load(open(r'<WORKSPACE>/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114/out/WP11_HOST_DOGFOOD.json',encoding='utf-8'));print({k:v['state'] for k,v in d['stages'].items()});print({k:v['state'] for k,v in d['portable_sp'].items()})"
"$PY" -c "import json;d=json.load(open(r'<WORKSPACE>/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114/out/WP20_MATRIX.json',encoding='utf-8'));print(d['counts'])"
```
