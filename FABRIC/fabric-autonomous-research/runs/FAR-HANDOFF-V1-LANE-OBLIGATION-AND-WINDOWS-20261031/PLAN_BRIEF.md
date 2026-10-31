NONCE-ECHO: NONCE-FAR-LANEOBL-20261031080129

# PLAN lane brief — why the mandate's three lanes were not used, and why console windows keep appearing

You are the PLAN lane (`openai-codex/gpt-6.1-sol`, medium). The interactive session that produced the artefacts below
runs on `opencode-go/deepseek-v4.1-flash` — the EXECUTE arm — so every previous "FAR research report" was written by
the execution model wearing a research label. Your job is to reason from the measured evidence, not to restate it.

## The two questions the owner asked

Q1. Why did earlier FAR work not use the three lanes and the specified models, when the mandate has said so for weeks?
    This is the same complaint more than once. Find the root cause, not the symptom.
Q2. Why do console windows keep appearing on the owner's desktop during work — worse over time, sometimes in a
    repeating loop — when earlier FAR rounds already "fixed" it twice?

## Measured evidence (all produced on this host, 2026-10-31)

1. Lane receipts in `C:\wg\queue` (every dispatch the loop ever made): EXECUTE 18, VERIFY_SECURITY 8, **PLAN 2**.
   The two PLAN receipts are dated 22:57 and 23:44 on 2026-10-30 — both after the owner had asked three times.
2. FAR runs in `.../fabric-autonomous-research/runs`: 8 directories from this session. None carries a PLAN receipt;
   one carries a single lane receipt of any kind. The research text itself has no author binding.
3. `scripts/console_guard_gate.py` (written today) parses each entry point with `ast` and looks for the guard as an
   executed module-level node. Before today: **7 entry points had the guard as text inside the module docstring** —
   `hgk-lane-dispatch.py`, `ops_status.py`, `stall_monitor.py`, `review_lock.py` and three others. Text in a docstring
   never runs, so `winproc.install()` never ran, so every `codex.exe` / `powershell.exe` child got a NEW console.
4. A new console on Windows 11 is a Windows Terminal window on the desktop. Measured window events: 02:01-02:18
   bursts of 46 events/hour during dispatch, all `powershell.exe`/`cmd.exe`/`WindowsTerminal.exe`.
5. After the repair, one measurement: **17 lane processes live, 0 window events in 75 s**.
6. Three independent autostart entries existed for the single 10101 relay: a Startup-folder `.cmd`
   (`start "" /min ocx.cmd start --port 10101`, which Windows runs through a console host → visible at every logon),
   a scheduled task (`Hidden: true`, launched through `wscript` → genuinely windowless), and `scripts/relay_daemon.py`.
7. `scripts/detach.py` was written today to escape the Hermes job object; its first version wrapped every launch in
   `cmd /c ... >> log`, and `Win32_Process.Create` starts `cmd.exe` **with** a console — 10 cmd.exe windows and 20
   Windows Terminal windows in three minutes. It now launches `pythonw.exe` directly.

## What the answer must contain

1. **A root cause for Q1 that is structural, not personal.** Something about the workflow made "the research is
   written in-session" the path of least resistance, every time. Name the missing obligation and where it must live so
   it cannot be skipped again (a gate, a receipt requirement, a required field — say which and why that layer).
2. **A root cause for Q2 that explains recurrence after two "fixes".** Consider: what did both fixes verify, and what
   would have caught the defect? State the general principle (not "be careful").
3. The **smallest set of changes** that makes each failure mode impossible rather than unlikely, ordered by
   necessity, and say explicitly which proposed change you would NOT make because it is over-engineering.
4. A **falsifier** for each root cause: the observation that would prove your diagnosis wrong.

Constraints: the answer must be usable as engineering rulings (each ruling names the artefact it changes and the gate
that enforces it). No new scheduler, no second issuer, no second queue. Governance weight must stay proportional to
risk. Chinese or English is fine; keep it dense.
