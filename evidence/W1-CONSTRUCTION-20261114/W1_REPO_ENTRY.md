# W1RepoEntry／SourceImportMap／ABI joins（W1 交付物，設計態）

**效力**：`LOCAL_DRAFT_WRITE / AUTHOR_DESIGN`。本檔是 L2 §04 W1 第一項交付（`W1RepoEntry/SourceImportMap/ABI joins`）的成文版本。
**不主張**：Repo 已建立、submodule 已接入、CI 已啟用、任何 Host 變更。`
OWNER_RULED_CONSTRUCTION_BASELINE / H-REPO-CREATE 未解除 / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / RELEASE_NOT_GRANTED`
**依據**：`FHS_vNEXT_PLP_W1_實質正文_施工定案版_2026-11-14_r1` §D.2（逐路徑抽取）；L2 §04 W1（`L2:L2685–2703`）；匯入白名單條款 `L2:L6211`／`L1:L7194`（`R4-ENG.4`）。

---

## 1｜W1RepoEntry（設計，不建立）

| 項 | 值 | 依據／限制 |
|---|---|---|
| 名稱 | `shw097-team/FHS_vNEXT`（備選 `shw097-team/FHS-vNEXT`） | 與既有 `FHS`、`FHS_NEXT` 不撞名；建立前需 Owner 核可用性 |
| 可見性 | private（預設） | 內含產品設計與原域條款；公開需 Owner 另裁 |
| Owner／權限 | `shw097-team`；admin 僅 Owner 一人 | 單人單機；不給 bot admin |
| 單一 Git root | repo 根即 root | `SBL`／`HG-KSEOS`／`Fabric` 以 **submodule 或 immutable snapshot** 接入（ADR-W1-01：不複製成第二 Compiler／Issuer／Policy Writer） |
| 分支 | `main` 受保護（禁 force-push、需 review）；工作分支 `w1/*` | 對齊三庫 `AGENTS.md` 的 candidate-only |
| CI | lint ＋ schema validate ＋ selfcheck ＋ ZIP CRC | **不做** Native／Release；CI 不得冒 Issuer／Checker |
| 法務 | `LICENSE`（Owner 選）、`NOTICE`（三庫原授權與來源）、`SBOM`（每 donor 的 tag/commit／license） | donor license 未證即 `NOT_BOUND` |
| 回退 | 刪分支或回上一個 `CURRENT.json` 指針 | 不改三庫 `main` |

**目前狀態**：`NOT_CREATED`（`H-REPO-CREATE`）。本輪只交付上表與第 2、3 節的 join，不執行 `git init`／`gh repo create`。

## 2｜SourceImportMap join（實測 433 檔／3,787,417 bytes）

| 來源庫 | branch | commit | 匯入檔數 | 授權檔 | 本輪用途 |
|---|---|---|---|---|---|
| `shw097-team/Fabric` | `main` | `a6f1fa897052` | 76 | `ABSENT_IN_REPO` | 治理契約、FHS 工程入口、6 routes |
| `shw097-team/SBL` | `main` | `a6003c3da3dd` | 195 | `LICENSE`（在場） | PIPD canonical compiler（13 verbs） |
| `shw097-team/HG-KSEOS` | `docs/fhs-w0-lane-routing-drift-20261111` | `696c30d71d00` | 159（＋local-worktree 2） | `ABSENT_IN_REPO` | 原生平面、lane 配置、guard/spine |
| 本機唯讀根 `<WORKSPACE>/FHS` | — | — | 1 | 繼承 origin | W0 驗收權威（只讀） |

**白名單規則（本輪實際套用）**：`policy.mode = SOURCE_ONLY_WHITELIST`，`byte_identical_required = true`；排除 `git history`、`evidence packs`、`databases/WAL`、`key material/tokens`、`venvs/node_modules`、`cron/session state`、`mirror duplication`、`symlinks`。
→ 這一條就是 `R4-ENG.4` 的「白名單 source-only import，原 Repo SHA 對得上；NEG＝拷貝 db/key/raw 或 blanket copy」。

**逐路徑處置（§D.2 的落地對照）**

| 類別 | 實際路徑樣式 | 處置 | 回退 |
|---|---|---|---|
| 來源匯入（只讀） | `FHS_NEXT/{Fabric,SBL,HG-KSEOS}/**` | 以原 commit 為 pin 的 snapshot／submodule；每檔 `target_sha256` 進 map | 刪 snapshot，不動原庫 |
| 產品程式 | `FHS_NEXT/SBL/integrations/pipd/**` | 原地保留、逐檔 SHA 對齊；改動走 PR | `git revert` 該 PR（僅程式，非 Host 狀態） |
| 作者文件 | `FHS_NEXT/deliverables/**`、`_local/**` | 隨 repo 版本化；`CURRENT.json` 指針 | 回上一個指針 |
| 環境設定／秘密 | `.env`、`*.key`、`*.enc`、token、DB、WAL | **不進版控**，交 Host secret | 不進版控即無須回退 |
| 需原 Reader／Issuer 才能執行的寫 | Host install、native effect、policy publish、release | 只寫設計與 HOLD，不代簽 | 由原域各自回退 |

**已量測的一個具體落差**：Fabric 入口的 `tests/test_manifest_admission.py` 讀 `INTEGRATION/FHS/docs/as-built/W0/r26/FHS_PIPD-LS-PKG_W0_r26.md`；該檔在 origin `main` 存在（668,540 bytes、blob `dfa7f0e6…`），但 `docs/as-built/**` 屬 evidence，**不在 source-only 白名單內**，故本樹沒有它。依 `R4-ENG.4` 的共識，正確解是**縮該測試的範圍（由 Fabric 原域）**，不是擴白名單去匯入證據；本輪不擴、不改 origin。

## 3｜ABI joins（13／19／8／6／3／12／57，逐項對 registry 實檔）

| 集合 | 數量 | 本輪在哪裡被實測 | 原 Consumer |
|---|---|---|---|
| CLI verbs | 13 | `pipd_ls_sp.cli --help` 實印（WP-05 R0） | PIPD 原 Compiler |
| Contract families | 19 | `pipd init` 回 `contract_families: 19` | PIPD 原 Registry |
| Skills | 8 | `pipd-authority-source` … `pipd-package-project`（registry 名錄） | PIPD 原 Reader |
| Effects | 6 | `SOURCE_READ／LOCAL_DRAFT_WRITE／DEV_REPO_WRITE／HOST_OPS／USER_EFFECT／RELEASE_EFFECT` | 各 effect 原 Owner |
| Lanes | 3 | `PLAN／EXECUTE／VERIFY_SECURITY`（menu＋guard 讀回） | HGK lane plane |
| Host surfaces | 12 | 宿主矩陣 12 格（`out/WP20_MATRIX.json`） | 各 Host Reader |
| Capability cards | 57 | `A01`–`A57`（§B2 名錄） | 原 Tech Registry |

**join 的語義**：每一列都是「同一個 Need → 一個 Occupant → 一個原 Consumer」，不靠數量相加；485 槽另有逐鍵清冊（`out/WP17_485_LEDGER.json`），不以 485 當作 57／13／19 的替代分母。

## 4｜未做與續行

- 未 `git init`／未建 GitHub repo／未改三庫 `main`／未加 CI（皆需 Owner 明示）。
- 續行條件：Owner 核可 repo 名稱與可見性 → 建空 repo（private）→ 以本檔 §2 的 pin 建 snapshot（非 blanket copy）→ 匯入 `provenance/SOURCE_IMPORT_MAP.json` 與本檔 → 開第一個 `w1/*` 分支跑 CI（lint／schema／selfcheck／ZIP CRC）。

## 5｜重現命令

```bash
PY="<HOST_HOME>/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
"$PY" "<WORKSPACE>/FHS_NEXT/ops/selfcheck.py"            # 期望 16/16、POS-01 綠
"$PY" "<WORKSPACE>/FHS_NEXT/ops/tools/spec_identity_check.py" --help
"$PY" -c "import json;d=json.load(open(r'<WORKSPACE>/FHS_NEXT/provenance/SOURCE_IMPORT_MAP.json',encoding='utf-8'));print(d['counts'])"
"$PY" -c "import json;d=json.load(open(r'<WORKSPACE>/FHS_NEXT_Workspace/W1_R2_CONSTRUCTION_20261114/out/WP02_WP03_READONLY.json',encoding='utf-8'));print(d['fabric']['route_runs'].keys())"
```
