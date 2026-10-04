# Fabric Desktop Automation (FDA)

> **Status: ✅ EXTERNAL ACCEPTANCE GRANTED** — r11 ALL PASS (2026-08-14)
> Fabric-governed bounded Windows desktop automation · LOCAL / PAPER / NO-LIVE-WRITE

Fabric Desktop Automation (FDA) 是在 HG-KSEOS 治理下，透過純消息/背景路徑自動化 **XQ (XQ全球贏家) 與 XS (XScript)** 桌面操作的能力層——用於策略雷達建立、PAPER 策略執行、編譯驗證、log readback 與外部驗收證據產生。**全程零滑鼠搶奪、零焦點竊取、零實單交易。**

## 🏆 驗收狀態

| 項目 | 狀態 |
|---|---|
| FDA blueprint / architecture / runtime / implementation | **PASS** |
| FDA_PROFILE_TEAM_ACTIVE | **PASS**（r11 2026-08-14）|
| XQ 3.20.02-260811 exact-build | PASS |
| F01 current-build 10/10 · F06 fresh compile 10x | PASS |
| UFO² v3.0.8 effective-load 7/7 | PASS |
| PAPER single-wash 10x + terminal readback | PASS |
| final checker 194/194（evaluator 9009713）| PASS |
| canonical manifest（63 entries, sha a3496336）| PASS |
| SQS_LIVE_TRADING | **NOT_AUTHORIZED** |

## 📁 核心資產

| 資產 | 用途 |
|---|---|
| `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` | action class × backend × build firewall（canonical 能力矩陣）|
| `xq_native_adapter.py` | 純消息 adapter（find_window/invoke_button/set_edit_text/press_toolbar）|
| `fda_router.py` | fail-closed 路由（讀 matrix digest，無 silent fallback）|
| `FDA_ASSET_REGISTRY.json` | canonical 資產清單（REUSE-FIRST 查詢）|
| `independent_checker.py` | 194 項驗證（VERIFY_ONLY，maker≠checker）|
| `evidence/receipts/` | 全部 qualification receipts（F01/F06/PAPER/STOP/checker）|
| `docs/FDA_USER_GUIDE.md` | 操作手冊（完整流程路由）|
| `AGENTS.md` | agent 操作契約 |
| `TEAM.md` | Shared Infrastructure Profile Team 宣告 |

## 🚀 快速開始

```bash
# 1. 確認 XQ 狀態（動態 pid 偵測；NOT_RUNNING → 重啟 XQ）
python var/fda/screen_state_check.py

# 2. 載入 skill（完整操作流程路由）
#    skill_view(name='fda-desktop-automation')

# 3. 執行 FDA 腳本（統一執行器：preflight → 執行 → 異常自動查螢幕）
python var/fda/fda_run.py <script.py>

# 4. 外部提交前
python var/fda/hgk_evidence_preflight.py   # 必須 PASS
```

## 🛡️ 強制規則

- **異常固定路由**：任何異常 → 先 `screen_state_check.py`（SSC-V2），禁止直接重試
- **零滑鼠硬路由**：禁 click_input/set_focus/foreground/SendInput；只准 PostMessage/SendMessage/pywinauto click/uia pattern/cua background
- **REUSE-FIRST**：查 `FDA_ASSET_REGISTRY.json`，有現成資產就 CALL
- **所有腳本經 fda_run.py**：preflight guard + 異常自動查螢幕（程式化強制）

## 🔍 操作異常時（第一動作，勿直接判卡死）

```text
XQ 很少真的卡死——通常是「有沒看見的小視窗」需確認（新增成功通知/停止確認/警示提示）。
任何異常 → 第一步跑 screen_state_check.py（含 hidden 視窗 + NEEDS_CONFIRM 標記）
→ 依實況處置（BM_CLICK 或 WM_CLOSE 小視窗）→ 才重試原操作。
全程零滑鼠搶奪、零焦點竊取。完整流程見 docs/FDA_USER_GUIDE.md §10.0 + §5/§6。
```

## 🧭 成功流程整合（XQ/XS 操作，2026-08-14 全部實戰 verified）

```text
開雷達: 警示提示 dialog → 策略雷達(&A) 按鈕 BM_CLICK（或 cua background menu）
建 PAPER: toolbar NEW(17551) pywinauto click → dialog(17500 名稱/17203 腳本/17610 商品/17035 單次洗價/加入=1)
驗證:    SensorList 延遲重讀（flush>15s）+ SensorLog LIKE '%name%'（state 2→3/exec 1→5/單次觸發 = stopped terminal）
toolbar: START=17554 STOP=17555（TB_PRESSBUTTON 無效 → pywinauto tb.button(i).click()）
陷阱:    XTP 自繪按鈕→WM_CLOSE · 新增成功通知 title "時間：[HH:MM:SS]" · 錯誤 dialog 以「加入(&A)」辨識
完整食譜: docs/FDA_USER_GUIDE.md §6 + skill §0 QUICKSTART
```

## ⚠️ Claim Ceiling

```
FDA 驗收 ≠ 實單交易授權 ≠ 生產自主 ≠ 遠端部署
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

## 📚 相關

- 治理：HG-KSEOS（WorkOrder/Kanban/reducer 控制面）
- Skill：`fda-desktop-automation`（操作路由）· `hgk-governed-execution`（治理）
- 藍圖：`fabric-desktop-automation_藍圖_v2026.08.13-r2`（PASS）
