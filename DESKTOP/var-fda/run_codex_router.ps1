$ErrorActionPreference = "Continue"

$codexExe = $env:LOCALAPPDATA + "\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe"
$codexHome = $env:LOCALAPPDATA + "\HG-KSEOS\codex-hermes"
$openCodexHome = $env:LOCALAPPDATA + "\HG-KSEOS\opencodex-hermes"
$root = "C:\Projects\Agent_Workspace\Fabric"

$envFile = $env:LOCALAPPDATA + "\hermes\.env"
$cred = $null
foreach ($line in [System.IO.File]::ReadAllLines($envFile)) {
    if ($line -like "OPENCODE_GO_API_KEY=*") {
        $cred = $line.Substring("OPENCODE_GO_API_KEY=".Length).Trim()
        break
    }
}
if (-not $cred) { Write-Host "CREDENTIAL_MISSING"; exit 2 }
$env:OPENCODE_GO_API_KEY = $cred
$env:CODEX_HOME = $codexHome
$env:OPENCODEX_HOME = $openCodexHome

$prompt = @'
You are the bounded tracked writer for WorkOrder WO-FDA-001 (FDA ChangeSet).
Write exactly TWO files under C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\
(ENGLISH ONLY content).

FILE 1: fda_router.py — implement a deterministic provider router.
Requirements:
- from dataclasses import dataclass
- from typing import Literal
- Provider = Literal['CUA', 'UFO2', 'HITL', 'BLOCKED']
- @dataclass(frozen=True) class Request with fields: app: str, app_version: str,
  action_class: str, risk_class: str, requires_secret: bool,
  financial_side_effect: bool, active_position_policy_mutation: bool
- def route(req: Request, matrix: dict) -> Provider:
    - if req.requires_secret: return 'HITL'
    - if req.financial_side_effect: return 'HITL'
    - if req.active_position_policy_mutation: return 'BLOCKED'
    - key = (req.app, req.app_version, req.action_class)
    - certified = matrix.get(key, {})
    - if certified.get('cua') == 'PASS': return 'CUA'
    - if certified.get('ufo2') == 'PASS': return 'UFO2'
    - return 'BLOCKED'
- def failover(primary: Provider, outcome: str, alternate_certified: bool) -> Provider:
    - if outcome == 'PASS': return primary
    - if outcome not in ('DETECTED_FAIL', 'SAFE_HALT'): return 'BLOCKED'
    - if not alternate_certified: return 'BLOCKED'
    - return 'UFO2' if primary == 'CUA' else 'CUA'
- No prints, no side effects, no external imports beyond dataclasses/typing.

FILE 2: fda_lease.py — implement one-active-writer lease + idempotency helpers.
Requirements:
- class LeaseDenied(Exception): pass
- class UnknownState(Exception): pass
- class DesktopLeaseManager:
    - __init__: self._writers = {} (session_id -> writer_profile), self._checkpoints = {}
    - def acquire(self, session_id: str, writer_profile: str, after_checkpoint=None) -> str:
        - if session_id in self._writers: raise LeaseDenied('second writer denied for session ' + session_id)
        - if after_checkpoint is not None:
            - if session_id not in self._checkpoints: raise ValueError('no checkpoint')
            - if self._checkpoints[session_id]['ref'] != after_checkpoint: raise ValueError('stale checkpoint')
        - self._writers[session_id] = writer_profile
        - return writer_profile
    - def current_writer(self, session_id: str):
        - return self._writers.get(session_id)
    - def release(self, session_id: str, writer_profile: str) -> None:
        - if self._writers.get(session_id) == writer_profile: del self._writers[session_id]
    - def checkpoint(self, session_id: str, ref: str, desktop_state_digest=None) -> None:
        - self._checkpoints[session_id] = {'ref': ref, 'desktop_state_digest': desktop_state_digest}
    - def transfer(self, session_id: str, from_writer: str, to_writer: str) -> str:
        - if self._writers.get(session_id) != from_writer: raise LeaseDenied('not holder')
        - if session_id not in self._checkpoints: raise ValueError('transfer requires checkpoint first')
        - del self._writers[session_id]
        - self._writers[session_id] = to_writer
        - return to_writer
    - def replay_allowed(self, side_effect_class: str, prior_effect_receipt_ref, current_state_confirms_applied) -> bool:
        - if current_state_confirms_applied is None: raise UnknownState('desktop state unknown')
        - if prior_effect_receipt_ref is not None and current_state_confirms_applied: return False
        - if side_effect_class == 'NONE': return True
        - if side_effect_class == 'EXTERNAL_APPROVAL_GATED': return False
        - return True
- import hashlib at top
- def idempotency_key(workorder_id: str, task_id: str, application_id: str,
                      application_version: str, action_class: str, target_identity: str) -> str:
    - payload = '|'.join([workorder_id, task_id, application_id, application_version,
                          action_class, target_identity])
    - return hashlib.sha256(payload.encode('utf-8')).hexdigest()

Write both files exactly at those paths. Do not touch any other file. Do not modify
existing files. Report the full content of both files in your final message.
'@

$promptFile = "C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\codex_prompt_fda_router.txt"
[System.IO.File]::WriteAllText($promptFile, $prompt, [System.Text.Encoding]::ASCII)

$codexOut = "C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\codex_fda_router.ndjson"
if (Test-Path $codexOut) { Remove-Item $codexOut -Force }

$codexArgs = @(
    "--model", "deepseek-v4-flash",
    "--sandbox", "danger-full-access",
    "--ask-for-approval", "never",
    "--cd", $root,
    "exec", "--skip-git-repo-check", "--ephemeral", "--json",
    $prompt
)

Push-Location $root
try {
    & $codexExe @codexArgs *> $codexOut
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

Write-Host "CODEX_EXIT=$exitCode"
Write-Host "OUTPUT_FILE=$codexOut"
if (Test-Path $codexOut) {
    $text = [System.IO.File]::ReadAllText($codexOut, [System.Text.Encoding]::Unicode)
    $lastAgent = ""
    foreach ($line in ($text -split "`r?`n")) {
        if ($line.Trim().Length -eq 0) { continue }
        try {
            $evt = $line | ConvertFrom-Json
            if ($evt.type -eq "item.completed" -and $evt.item.type -eq "agent_message") {
                $lastAgent = [string]$evt.item.text
            }
        } catch { }
    }
    Write-Host "=== AGENT MESSAGE ==="
    Write-Host $lastAgent
}
