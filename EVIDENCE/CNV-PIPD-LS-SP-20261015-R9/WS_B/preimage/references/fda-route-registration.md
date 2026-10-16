# FDA Route Registration (條件 2 常設路由) — 完整配方

Executed 2026-08-15 for WO-SQS-FDA-XQ-ROUTE-001 (ROUTE-SQS-XQ-GLOBALWINNER-001).
Reuse for ANY future "register a governed FDA route" work order. Load
`hgk-governed-execution` + `fda-desktop-automation` (§2.0a 授權前置檢查) first.

## Preconditions
- binding_wo MUST already exist in shared-spine `workorders` table
  (`C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db`).
  Missing row = the AO G1 failure mode that got ROUTE-WO-FDA-XQ-002 removed.
- Registry: `references/FDA_ROUTE_REGISTRY.json`, schema FDA-ROUTE-REGISTRY/1,
  mutation_authority=ADMITTED_HGK_WORKORDER_ONLY (本 WO 即授權).

## Digest formula (VERIFY against stored value BEFORE any mutation)
```python
canon = json.dumps({k: v for k, v in data.items() if k != 'digest'},
                   ensure_ascii=False, sort_keys=True, indent=2)
digest = hashlib.sha256(canon.encode('utf-8')).hexdigest()
```
- Recompute on current file first; MUST equal stored `digest` (else stop — file drifted).
- The HASH uses sort_keys=True, but the FILE on disk is written in INSERTION order
  (human-friendly field order). Write back with `json.dumps(data, ensure_ascii=False, indent=2) + '\n'`, UTF-8.
- New route entry field order should mirror existing entries:
  route_id, owner, scope, app, action_classes, allowed_scripts, binding_wo, binding_ref, status, expires.

## Mutation + self-verify (all in one script, assert-heavy)
1. Load JSON; assert target route_id NOT already present; assert existing route count.
2. Append new route dict (old entries untouched — byte-identical fields).
3. If touching the top-level `note`: APPEND text (additive, preserve audit trail).
   ⚠️ Appending note changes the digest vs. a bare route-add — record `digest_before/after`
   in the receipt so auditors can reproduce.
4. Recompute digest → set `data['digest']` → write back.
5. Reload → recompute → assert == stored; assert routes count; assert old route_ids
   unchanged; assert `'\ufffd' not in raw` (CJK UTF-8 integrity).

## Spine binding check (read-only)
```sql
SELECT workorder_id, state FROM workorders WHERE workorder_id='<binding_wo>';
```
Expect exactly 1 row, state=CREATED.

## SQS-side artifacts (owner=SQS)
- `SQS-THC/adapters/fda-xq-globalwinner-route.yaml` — route declaration: route_id/binding_wo/
  scope/action_classes/allowed_scripts + NO-LIVE-WRITE boundary (`live_write: false`,
  `broker_write: false`, `autonomous_order_submission: false`) + HITL gate
  (ACTIVE_POSITION → HUMAN_ENTRY_APPROVAL) + forbidden list. Model style on existing
  `adapters/xq-read-watch.yaml`. Cross-reference `FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml`.
- `SQS-THC/docs/DOC-11-*.md` — 用途/授權條件/操作邊界表/查詢方式 (4 條唯讀指令).
- Verify CJK: no U+FFFD after write.

## Verification (MUST run both, record raw output)
a. Preflight (venv python has pyyaml/pywinauto):
   `C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe fda_preflight.py
   --action-class XQ_LAUNCH_LOCATE --route-id <ROUTE>` → exit 0,
   `authorization.source == "route"`, `route_result.route` QUALIFIED (e.g. CUA),
   channels background-only.
b. Hook stdin test — PROVE route path (not condition-1 token): pipe JSON with a
   **no-token session id** (e.g. `verify-route-only-XXXX`) to fda_guard_hook.py:
   ```bash
   echo '{"hook_event_name":"pre_tool_call","tool_name":"terminal","tool_input":{"command":"python fda_preflight.py --action-class XQ_LAUNCH_LOCATE --route-id <ROUTE>"},"session_id":"verify-route-only-9f3a"}' \
     | "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe" fda_guard_hook.py; echo $?
   ```
   exit 0 + also confirm no stray token file for that session id in
   `~/AppData/Local/hermes/var/fda-auth/` (ls | grep).

## Receipt
Write `<HGK-KSEOS>/var/a2/<WO>_RECEIPT.json`, schema `<OWNER>-FDA-ROUTE-REGISTRATION-RECEIPT/1`:
route entry, registry path + digest_before/after + recompute match + routes_total/ids +
old_routes_preserved, spine query + result rows, preflight command/exit/authorization/
blocked_reasons/route_result, hook command/exit/stdout + authorization_path=route,
SQS artifact paths + cjk_utf8_ok, constraint flags (no_xq_desktop_operations,
registry_old_entries_untouched, frozen_assets_untouched).

## Pitfalls
- Don't write the file with sort_keys=True — that reorders top-level keys and breaks
  the human-friendly layout; only the hash uses sort_keys.
- Don't skip the pre-mutation digest verification; a drifted file fails silently later.
- Hook test with a session id that has a live token would pass via condition 1 and
  prove nothing about the route — always use a fresh no-token session id.
- Registry mutation via heredoc python gets flagged by approval; that is expected,
  keep the script assert-heavy so it fails loudly rather than half-writing.
