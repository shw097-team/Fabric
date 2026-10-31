# FAR round 028 — the window storm and the CPU load: one class, three multipliers, five fixes

| | |
|---|---|
| schema | `FAR-ROUND-REPORT/1` |
| round | `FAR-20261031-028-console-window-cpu-root-cause` |
| control plane | HG-KSEOS (authority, state, acceptance) |
| governance contract | Fabric (`contracts/`, `assurance/`, `control/`) |
| product engineering entry | SBL / FHS-MSC HANDOFF-PATCH-v1 |
| method | FAR (measure → attribute → eliminate → verify), routed per `fabric-autonomous-research` |
| claim ceiling | **MEASURED_LOCAL** for attribution; **INCONCLUSIVE** for synthetic reproduction (positive control failed — §6) |
| self-acceptance | none (this report proposes; the AO verdict is a separate lane artifact) |

## 1. The answer in one paragraph

The windows are not one bug and not one script. They are a **class**: every *console-subsystem* process
started from a context that has no console gets a **brand-new console** from Windows, and on this host the
default console host is **Windows Terminal**, so each one becomes a terminal window plus a conhost/OpenConsole
pair. The instrument recorded **170 such windows between 01:58:23 and 09:00:04**, owned by
WindowsTerminal.exe 121, python.exe 15, cmd.exe 14, powershell.exe 7, bun.exe 2 — with titles
`powershell.exe` 26, `git.EXE` 22, `cmd.exe` 16 and the Codex package path 16, i.e. the **grandchildren** of
headless launchers, not the launchers themselves. Three independent loops multiplied the rate (lane fan-out
relaunch, a mis-counted retry budget, and a WMI+PowerShell detach path), and two pre-existing scheduled
tasks contribute their own periodic windows. The CPU load is the same fact seen from the other side: **process
churn**, not model work — 517 churn records and 48 refused ticks in one driver log, `pwsh`/WMI startup per
launch, 229 live processes, and a second Hermes instance (`D:\Hermes-Recovery\live22` → `hermes_cli.main gate`)
taking ~2.6 % on its own.

Why it kept coming back: **every previous fix replaced the launcher host for one named task** (wscript for
`\Root\HGK-OpenCodex-Sealed-10101`, wscript for `\Codex Desktop OpenAI and DeepSeek Router`). The class does
not live in a task; it lives at the spawn site. There are 31 scripts that spawn children, and each new spawn
site silently reintroduced the class. A root fix therefore cannot be another host substitution — it has to be
**one choke point, one invariant, one gate**.

## 2. Cross-session history (what was already known, and what it missed)

| round | artefact | conclusion then | what it missed |
|---|---|---|---|
| `FAR_LANE_SOD_008` | RCA | visible console from a scheduled task on a Windows Terminal host | scoped to one task |
| `FAR_LANE_SOD_009` | report | governance of the above | same scope |
| `FAR_LANE_SOD_010` | `evidence/review/FAR_LANE_SOD_010_CONSOLE_WINDOW_CONVERGENCE_2026-10-08.md` | task `\Root\HGK-OpenCodex-Sealed-10101`, `pwsh.exe` direct launch, `PT5M`, fixed by `wscript.exe` + `WScript.Shell.Run(cmd,0)`; "a window with no task running is a **timer**, not activity" | treated the **task** as the unit; did not generalise to spawn sites |
| `FAR_LANE_SOD_011` | `evidence/review/FAR_LANE_SOD_011_ROUTER_WINDOW_2026-10-09.md` | `-WindowStyle Hidden` still opens a visible window; wscript host → 0 | same — one more named task |
| `scripts/detach.py` | docstring | `CREATE_BREAKAWAY_FROM_JOB` fails inside a nested job; `Win32_Process.Create` survives the turn | WMI `Create` reports success for a child that dies instantly, and its PowerShell call is itself a console program |
| `scripts/winproc.py` | docstring | `CREATE_NO_WINDOW` is "the only way to keep it hidden" | hides **one level**; the child is left *consoleless*, so its grandchildren pop |
| `scripts/console_guard_gate.py` | AST gate, 31 entry points | `DETACHED_PROCESS` is a window factory | did not model *console inheritance depth* |

The frame shift this round: **stop asking "which task opened the window" and start asking "which process had
no console when it spawned a console program".** Under that question the scheduled tasks are a minority
contributor; the majority is the lane toolchain's own process tree.

## 3. Measured attribution (`evidence/console-window-events.jsonl`, sha256 in `EVIDENCE_INDEX.json`)

| fact | value |
|---|---|
| events | 170, from `2026-10-31T01:58:23` to `09:00:04` |
| per hour | 01 → 7, 02 → 46, 07 → 72, 08 → 44, 09 → 1, **03–06 → 0** |
| owners | WindowsTerminal 121 · python 15 · cmd 14 · powershell 7 · unresolved 10 · bun 2 · OpenConsole 1 |
| classes | `CASCADIA_HOSTING_WINDOW_CLASS` 123 · `PseudoConsoleWindow` 44 · `ConsoleWindowClass` 3 |
| titles | `Terminal` 30 · `powershell.exe` 26 · `git.EXE` 22 · Codex package path 16 · `cmd.exe` 16 |
| bursts (≥5 within 5 s) | 8, largest **38 windows**; starts 02:01:31, 07:42:00, 07:42:44, 07:43:06, 07:46:26, 08:41:52, 08:42:37, 08:58:41 |

Two decisive readings:

1. **Zero events in the hours when nothing was running.** The windows track *work*, not a timer alone.
2. **The owners are console children, and the titles are the console applications' own names**
   (`powershell.exe`, `git.EXE`, `cmd.exe`). A window titled `git.EXE` is not "a git window"; it is a
   console host created *for* git's console, which is only possible when git was started by something that
   had none.

## 4. Root-cause chain (six findings, each with its own evidence)

| id | finding | evidence | class |
|---|---|---|---|
| **RC-1** | Console inheritance: a console-subsystem child of a consoleless process gets a new console; Windows Terminal is the default host, so the console is visible and costs a terminal + conhost pair | 170 events; owners/titles §3; zero in idle hours | mechanism |
| **RC-2** | The lane fan-out relaunched units it had already halted, every ~8–10 s (`PRE_ATTEMPT` receipts 10:38:54/10:39:02/10:39:14…), each relaunch paying the full spawn cost | `driver.log`: 517 churn records, 48 `tick_refused`; receipts at 8–12 s spacing | multiplier |
| **RC-3** | Retry budget counted **orphan launch markers** as spent rounds (six 310-byte `PRE_ATTEMPT` receipts with no `attempts[]`), halting all three open units while the loop kept churning | `WP-FHS-11/17/20` receipts; `execute_rounds()` before/after: 6 → 0 | multiplier |
| **RC-4** | `detach` launches through **PowerShell → WMI `Win32_Process.Create`**: one console program per launch (title `powershell.exe`, 26 events) and a success verdict for children that die instantly (`{"ok": true, "pid": …}` then no process; `ReturnValue 9` on a bare command) | `probe_legacy_consoleless_root.json`; detach stderr `error: "|9"`; 30 vanished attempts on WP-FHS-17 | multiplier |
| **RC-5** | Two owner-level scheduled tasks are `STATE=Running` on the same desktop and supervise with console children every 5 min / on failure (`RestartOnFailure 3×PT1M`) | `Get-ScheduledTask`: `\Root\HGK-OpenCodex-Sealed-10101` (`wscript` → `supervise-hgk-opencodex.run.vbs`, `PT5M`), `\Codex Desktop OpenAI and DeepSeek Router` (`wscript` → `router-windowless-host.vbs`, listens 10102) | independent contributor |
| **RC-6** | CPU load is process churn, not inference: `pwsh`/WMI spawn cost per launch, 229 live processes, and a **second Hermes instance** (`D:\Hermes-Recovery\live22\tools\python-3.14.9…\python.exe -m hermes_cli.main gate`) at ~2.6 % | CPU samples 7–32 % idle-ish; top consumers Hermes 14.8 %, python 10.0 %, chrome 16.1 %, second Hermes 2.6 % | amplifier |

## 5. Why "fix the launcher host" could never hold

`wscript.exe` + `WScript.Shell.Run(cmd, 0)` is a correct fix **for a task that launches one child**. It is
not a fix for a *tree*: the child still runs `pwsh`, which starts `ocx`, which starts `node`, which starts
`git`; each of those inherits whatever console the VBS host created (none), and the class reappears one
level deeper. The same shape appears in the lane: `pythonw` (no console) → `python`/`cmd`/`pwsh` (new
console) → `git`/`node` (another). **A hiding flag applied at one edge of a tree cannot govern the tree.**

## 6. What this round could NOT prove (recorded, not hidden)

A synthetic positive control was built (`scripts/winproc_tree_probe.py`): a consoleless root spawning
`cmd → git`, `python → cmd → git`, and `python → python → cmd → git`, in `--legacy` mode (hide the direct
child only) and in patched mode, with the console windows enumerated from `EnumWindows`.

| run | root context | new console windows |
|---|---|---|
| `probe_legacy_console_parent.json` | my shell (has a console) | 0 |
| `probe_legacy_consoleless_root.json` | `detach.py` (no console) | **0 — the control did not fire** |
| `probe_patched_consoleless_root.json` | `detach.py` (no console) | 0 |

The positive control **failed**: the legacy path produced no observable window at 1.5 s sampling. Therefore
**the mechanism is attributed from the instrument's history (§3) and not from a reproduced failure**, and this
report does **not** claim "root cause proven by reproduction". Two admissible explanations remain
(Windows Terminal may attach very short-lived consoles as a *tab* in an existing window rather than a new
top-level window; and `EnumWindows` at 1.5 s cannot see a window that lived 200 ms), which is exactly why the
deciding test must be the 20 ms watcher (§7, F3) and not a snapshot.

**This is the honest ceiling of this round: MEASURED_LOCAL attribution, INCONCLUSIVE reproduction.**

## 7. The upgrade (root fix, not another host substitution)

| id | change | status |
|---|---|---|
| **F1** | `scripts/winproc.py`: give every child **one console created hidden** (`CREATE_NEW_CONSOLE` + `STARTF_USESHOWWINDOW`, `wShowWindow=0`) instead of `CREATE_NO_WINDOW`, so the whole tree inherits an invisible console and no descendant can allocate a visible one | **APPLIED** in this round (syntax + `console_guard_gate --all` 31/31) |
| **F2** | `scripts/detach.py`: drop the PowerShell/WMI indirection (one console program and one silent-failure mode per launch); launch directly with `CREATE_NEW_CONSOLE\|SW_HIDE` **and** prove liveness (pid alive + image name matches within 500 ms) before returning `ok` | proposed (bounded writer) |
| **F3** | Per-dispatch invariant: `window_watch` delta across the dispatch window must be **0**; the receipt carries `console_window_delta`, and a nonzero delta refuses the receipt (`ERR_CONSOLE_WINDOW_EMITTED`) instead of logging a warning | proposed (this is the gate that makes the class impossible to reintroduce) |
| **F4** | Lane loop: never top up a unit whose budget is spent (**APPLIED**), per-unit locks so parallel units cannot collide (**APPLIED**), and exponential backoff instead of a fixed ~10 s relaunch | 2 of 3 applied |
| **F5** | Budget accounting: an orphan `PRE_ATTEMPT` older than the lane timeout is a dead attempt, not a spent round (**APPLIED**: rounds 6 → 0) | **APPLIED** |
| **F6** | `console_guard_gate`: extend the AST rule from "bans `DETACHED_PROCESS`" to "requires a hidden console for every spawn site, and refuses a bare `subprocess.*(` in an entry point" | proposed |
| **F7** | Scheduled tasks: keep the `wscript` host, add a **measured** no-window assertion to their receipts; changing the `PT5M` interval is an owner decision, not an engineering one | proposed (interval = owner) |
| **F8** | The second Hermes instance (`D:\Hermes-Recovery\live22`) is a CPU consumer outside this repo. Stop / keep is an owner decision; recorded as `TT-HOST-SECOND-HERMES-001` | open TT |

## 8. Engineering ruling

Adopt **F1–F6 now**: reversible, code-scoped, no authority change, and each is measurable. F1/F4/F5 are
already in the tree; F2/F3/F6 are one bounded write each. **F7's interval change and F8 are owner decisions**
and are not taken here. Nothing in this package touches Stage-3, production, or any live path.

The governing sentence, for the gate to enforce rather than the operator to remember:

> A governed dispatch may not put a window on the owner's desktop, and may not report success for a child it
> cannot see.
