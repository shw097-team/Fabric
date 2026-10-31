# FAR-039｜視窗又跳出來：我自己把父行程藏起來，然後讓每個子行程各自開一個新視窗

日期：2026-10-31（台北）
路由：Fabric 治理契約 → SBL 產品工程指揮入口 → HG-KSEOS 授權／狀態／驗收控制平面

---

## 0. 事實

我在上一輪把 `hgk-continuation-supervisor`（every 3m）resume，用來治「一直停下」。**幾分鐘後你回報視窗又開始跳。**

這是第三次同類事件：
- 早前一次 tick 實測 **14 個 git.EXE 視窗**；
- `console_guard_gate` 的 F6 記錄：`CREATE_NO_WINDOW` 只藏一層，孫行程仍會各開一個 console；
- 本輪：resume 之後重演。

**我先停血**：`hermes cron pause 2d9fbc9715e7` → `Paused job: hgk-continuation-supervisor`，並確認沒有任何 loop 行程存活（查詢本身會被 `CommandLine -match` 命中，這是已知陷阱，已排除）。

---

## 1. 根因（單一、可指到行）

`profiles/hgk-governed/scripts/hgk_continuation.py`：

```python
# 檔頭：把自己 re-exec 成 pythonw（GUI subsystem，沒有 console）—— 這一步是對的
_sp.Popen([_pw, ...], creationflags=0x08000000)

# 但實際派工的 helper：
def run(args, timeout):
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=timeout)   # ← 沒有 creationflags
```

`PY` 是 venv 的 `python.exe`，**console 程式**。Windows 規則：**沒有 console 的父行程**啟動 console 子行程時，子行程會**配置一個新的 console**，而新 console 就是一個可見視窗。

所以：**把父行程藏起來，正好讓每個子行程變可見。** 每個 tick 呼叫 `run()` 數次 → 每 tick 數個視窗。修法本身在製造症狀。

---

## 2. 為什麼 gate 沒攔住（第二個根因：掃錯範圍）

`console_guard_gate.py` 只掃 `HG-KSEOS/scripts/*.py`（33 檔）。**cron 每 3 分鐘真正執行的那支檔案在 profile 裡**，從來不在掃描範圍內。

而且它的判定是**整檔 token 搜尋**：`hgk_continuation.py` 因為自己那行 re-exec 帶了 `creationflags`，整檔搜尋會判定「有守衛」——**實際的每個子行程都沒有**。

**Gate 回報 32/33 OK 的那個當下，肇事檔案根本沒被看過。**

---

## 3. 修補（已實作並實測）

### 3.1 子行程一律帶 `CREATE_NO_WINDOW`

`hgk_continuation.py::run()` 現在：

```python
kw = {}
if os.name == "nt":
    kw["creationflags"] = 0x08000000   # CREATE_NO_WINDOW
return subprocess.run([PY, *args], capture_output=True, text=True, timeout=timeout, **kw)
```

不用 `DETACHED_PROCESS`（每個孫行程各開新 console），也不用 `CREATE_NEW_CONSOLE`（這個父行程沒有 console 可繼承）。

### 3.2 Gate 掃 profile，並改成「逐呼叫點」判定

- `profile_script_dirs()`：掃 `profiles/*/scripts/*.py`。
- `spawn_sites_without_flags()`：AST 逐個 `subprocess.run/Popen` 呼叫點檢查，不再整檔搜尋；`**kwargs` 只有在檔案真的提到 `creationflags` 時才算守衛；**本地同名 helper `run()` 不算**（否則會誤報那個已經帶 flag 的 wrapper，讓 gate 失去可信度）。

結果：`checked 33, ok 33, bad 0, hides_one_level_only 0`。4/4 新測試，其中一條專門釘住「pre-fix 的 body 必須被抓到」。

### 3.3 順帶修掉兩個在驗證時暴露的缺陷

**(a) stall monitor 的 spawn 計數沒有時間窗**
`repeated_blocks()` 對 receipt 有 mtime 視窗，但對 `driver.log` 的 spawn 掃描**讀完整個歷史**。23:51 它數到 10:39–10:44 的 47/50/46 次 spawn，判定 `REPEATED_SPAWN` 並 halt。**13 小時前的歷史被當成現在的重複**——正是「計數要開窗」那個坑。已加 `cutoff` 與 `at` 解析，無法解析的時間戳不算近期證據。
現在：`findings: []`、`exit 0`。

**(b) halt 時 pause 錯名字**
`CRON_NAME = "hgk-continuation"`，實際 job 叫 `hgk-continuation-supervisor`。於是 monitor 殺了行程、宣告 halted，但 **cron 照樣每 3 分鐘再來一次**。已改正。

---

## 4. 驗證（不是「我以為好了」）

| 項目 | 結果 |
|---|---|
| console gate | `checked 33 / ok 33 / bad 0` |
| 新測試 | 4/4 OK |
| stall monitor | `findings: []`，exit 0 |
| 真 tick 執行 | `executions` 19 → 21，`completed @ 23:51:38` |
| tick 前可見 console 視窗 | **0** |
| tick 後可見 console 視窗 | **0** |

**誠實的缺口**：23:51 那次 tick 跑的是**修好 monitor 之前**的版本；23:53 我手動 `hermes cron tick` 沒有產生新 execution（next_run 尚未到）。所以「下一個排程 tick 會越過 monitor 真正派工」**還沒被端到端證明**。這是我留下的第一驗證項，不是已知結論。

---

## 5. 跨 SESSION 交叉比對：為什麼會重複

| 事件 | 當時的修法 | 為什麼又回來 |
|---|---|---|
| 早前 14 個 git.EXE 視窗 | 改 `CREATE_NO_WINDOW` | 只藏一層，孫行程仍開窗 |
| F6 記錄 | 加 `console_guard_gate` | gate 只掃 HG-KSEOS，tick body 在 profile |
| 本輪 | resume supervisor | tick body 的 `run()` 從來沒帶 flag，而且 gate 看不到它 |

**共同型態**：每次都在「我看得到的那份檔案」修，而**真正在跑的是另一份**。skill 裡那句「A fix can be right in content and land on the wrong copy」就是這件事；我這次是自己踩。

---

## 6. 裁決建議

| # | 決策 | 建議 |
|---|---|---|
| D-P | `console_guard_gate` 必須掃 profile scripts（已實作） | 簽，並納入 pre-commit |
| D-Q | 任何 halt 必須用**真實 job id** 暫停，且把 halt 入列為待裁決項 | 簽 |
| D-R | 所有重複計數器一律開時間窗，無窗不得 halt | 簽（已套用到 spawn） |
| D-S | 「修完要跑一次真 tick，並在 tick 前後各數一次可見視窗」列為收尾必做 | 簽 |

---

## 7. 對「剩下四包」的影響

視窗風暴與四包無關，但它**阻斷了無人值守**：一條會彈視窗的迴圈，你不可能放任它跑。現在迴圈乾淨了，四包的 blocker 仍是上一輪那四條（`BLOCKED_PROFILE_CONTENT`、`HOST_RUNTIME_FROZEN`、`ABI_CONSUMER_MISSING`、`KIND_ENUM_UNREAD`），每一條都寫了 unblock。
