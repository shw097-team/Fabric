' CANDIDATE ONLY; not installed.
' Rollback (authorised writer only): invoke exec\rollback\ROLLBACK.ps1 -HumanAuthorised.
' Restores the original pwsh task action and exact supervisor preimage.
' ============================================================================
' CANDIDATE FIX (not applied) - windowless host for the HGK sealed-relay supervisor.
' Purpose: launch the governed supervisor with NO console window at all, so the
' Task Scheduler action never produces a visible 命令列視窗 (proven by FAR probe C:
' sh.Run(cmd, 0, ...) yields only a hidden ConsoleWindowClass window, whereas a
' direct pwsh.exe action yields a visible Windows Terminal window even with
' -WindowStyle Hidden and Task <Hidden>true</Hidden>).
' Claim ceiling: CANDIDATE_ONLY - requires user/HGK approval + Codex tracked write.
' ============================================================================
Option Explicit
Dim sh, pwsh, script, cmd, rc
Set sh = CreateObject("WScript.Shell")

pwsh   = "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe"
script = "C:\projects\Agent_Workspace\HG-KSEOS\scripts\supervise-hgk-opencodex.ps1"

cmd = """" & pwsh & """" & " -NoProfile -NonInteractive -ExecutionPolicy Bypass" & _
      " -File """ & script & """ -Action Run -MaxRestarts 3 -WindowSeconds 300"

' 0 = hidden window, True = wait for exit so the task result/limit still apply.
rc = sh.Run(cmd, 0, True)
WScript.Quit rc
