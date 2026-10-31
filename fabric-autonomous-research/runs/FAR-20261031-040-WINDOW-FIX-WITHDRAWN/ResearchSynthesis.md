# FAR-040｜撤回「已修好」：我修錯站點，而且我的量測是瞎的

日期：2026-10-31（台北）

---

## 0. 你問的「前輪根本沒修乾淨？」

**是。** 兩件事我都做錯了，分開講清楚。

### 錯一：修錯站點

上一輪我修的是 `hgk_continuation.py` 的 `run()`（supervisor 呼叫 stall_monitor / driver 的那個 helper）。
但真正生視窗的是**更下面兩層**：

| 站點 | 原本 | 後果 |
|---|---|---|
| `continuation_driver.py` 派工 spawn | `CREATE_NO_WINDOW` | dispatch 沒有 console → 它啟動的 `codex.exe` **配置一個新的可見 console** |
| `continuation_driver.py` 鏈式 tick | `CREATE_NO_WINDOW \| BREAKAWAY` | 下一個 tick 同樣沒有 console → 它的 `git.exe` / `codex.exe` 各開一個視窗 |
| `hgk-lane-dispatch.py:841` | `CREATE_NO_WINDOW` | 同上 |

`CREATE_NO_WINDOW` **只藏一層**：子行程拿到「沒有 console」，於是子行程啟動的 console 程式就得到一個全新的、可見的 console。
上一輪我以為「加了 flag 就是修好」，實際是把視窗往下推一層。

**證據就在你自己的儀器裡**：`var/console-window-events.jsonl` 170 筆事件中，最大宗是
`WindowsTerminal.exe / CASCADIA_HOSTING_WINDOW_CLASS`，標題是 **`C:\Program Files\Git\cmd\git.EXE`** ——
一個沒有 console 的父行程啟動的 git，正是上表第二列。

### 錯二：我的量測是瞎的

我先用「`MainWindowHandle != 0` 每 0.5 秒取樣」判斷有沒有視窗，回報 **0**。那是**假陰性**。
後來我寫了三層 probe 做正控（控制組用已知會彈窗的 `CREATE_NO_WINDOW`），結果：

```
control.events = 0   →  PROBE_BLIND
```

**控制組打不響，代表儀器看不到視窗。** 在這種情況下 `fix.events = 0` 一點意義都沒有。
更糟的是 `window_watch.py` 本身從 09:00 之後就沒再寫入任何事件（`--status` 說 alive，`events` 停在 170）。
所以本輪之前我說的每一次「0 個視窗」，**都不能當證據**。

---

## 1. 本輪實際做的事

### 1.1 先止血（已做）

- `hermes cron pause 2d9fbc9715e7` → **Paused**。
- 清掉所有 loop 行程，`remaining: 0`。

現在沒有東西在彈視窗，因為迴圈是停的。

### 1.2 把四個站點改成「一個隱藏 console，整棵樹繼承」

| 檔案 | 改法 |
|---|---|
| `continuation_driver.py` | 新增 `CREATE_NEW_CONSOLE` + `_hidden_startupinfo()` + `_hide_tree()`；`sp_run` / `sp_popen` / 派工 spawn / 鏈式 tick / 20s 探測全部走它 |
| `hgk-lane-dispatch.py` | 新增 `_hidden_spawn_kw()`；30s 探測改走它 |
| `hgk_continuation.py`（profile） | `run()` 由 `CREATE_NO_WINDOW` 改為 `CREATE_NEW_CONSOLE` + `SW_HIDE` |

`CREATE_NO_WINDOW` 與 `CREATE_NEW_CONSOLE` 是**互斥**的，`_hide_tree()` 會先把窄的那個清掉再加寬的；`DETACHED_PROCESS` 不動（它是視窗工廠）。

兩支檔案都通過 `py_compile`。（中途我確實打壞過一次縮排——`IndentationError` at line 547——已修正；這正是「字串替換打進 early-return 分支」的老坑。）

---

## 2. 我不能說的話

**「已修好、已驗證」我這輪不能說。** 理由：正控打不響，儀器是瞎的。

目前能誠實主張的只有：

1. 所有**已識別**的 `CREATE_NO_WINDOW` 站點都已改成隱藏 console 形態（可 grep 驗證）。
2. `console_guard_gate` 33/33、`bad 0`（但它只證明「每個 spawn 有 flag」，不證明「沒有視窗」）。
3. 迴圈目前是 **paused**，所以不會再有新視窗。

**不能主張**：重新 arm 之後不會再彈。那需要一個能打響的儀器。

---

## 3. 儀器為什麼瞎（已定位，未修完）

`window_watch.py` 用 20 ms `EnumWindows`，但它自己的紀錄停在 09:00；重啟後（pid 21884）仍不寫入新事件。
所以有兩個可能，我還沒有把它們分開：

- (a) watcher 的 `interesting()` 過濾把新事件濾掉了；
- (b) 這台機器在目前工作階段下，`CREATE_NO_WINDOW` 的 `cmd.exe` 子行程**真的不會**產生可見視窗——也就是我的控制組根本沒有重現你的現象。

**在你回報「又彈出來」的當下，你的觀察是 ground truth，我的 0 不是。** 這句話是本輪唯一站得住的量測結論。

---

## 4. 下一步（我不會自己重新 arm）

1. 修 `window_watch.py`：拿掉可疑過濾、把每一筆新視窗都寫入（含 parent pid 鏈），並用**你親自看到的那次**當正控。
2. 正控打響之後，才重新 arm supervisor，並且在 arm 的同時讓 watcher 跑滿一個 tick。
3. 只有在「正控響、fix 不響」成立時，才宣告視窗問題關閉。

**在那之前重新 arm，等於再讓你被彈一次視窗去換一個我無法驗證的假設。**

---

## 5. 對四包的影響

無。四包仍是 `18 PASS / 4 FAIL`，四條 blocker 各帶 unblock。視窗問題屬於「無人值守能力」，不屬於產品包。
