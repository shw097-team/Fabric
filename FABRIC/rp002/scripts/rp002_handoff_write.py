# -*- coding: utf-8 -*-
"""RP-002 pre-reinstall handoff — collect identities, write frozen MD, readback + hash."""
import datetime, hashlib, json, sqlite3, subprocess
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
REVIEW = FAB / "evidence" / "review"
REVIEW.mkdir(parents=True, exist_ok=True)
OUT = REVIEW / "RP002_PRE_HERMES_REINSTALL_HANDOFF.md"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
hgk_head = git(HGK, "rev-parse", "HEAD")
sqs_head = git(Path(r"C:\Projects\Agent_Workspace\SQS-THC"), "rev-parse", "HEAD")
fab_head = git(FAB, "rev-parse", "HEAD")

# spine facts
con = sqlite3.connect(str(HGK / "var" / "shared-spine" / "hg-kseos.db"))
con.row_factory = sqlite3.Row
proj = dict(con.execute("SELECT * FROM project_lifecycles WHERE project_id='HGK-REFERENCE-PROJECT-002'").fetchone())
wo_states = con.execute("SELECT state, COUNT(*) c FROM workorders WHERE workorder_id LIKE 'WO-RP2-%' GROUP BY state").fetchall()
tt_open = [dict(r) for r in con.execute("SELECT tt_id,status,blocking,subject FROM tt_records WHERE status!='CLOSED'")]
blocking = con.execute("SELECT COUNT(*) FROM tt_records WHERE blocking=1 AND status!='CLOSED'").fetchone()[0]
con.close()

gates = {
    "G0": "SEALED", "G1": "SEALED", "K1": "SEALED", "D1": "SEALED", "C1": "SEALED",
    "H1": "MAKER_ONLY (independent checker FAILED on temp-dir collision; re-run needed)",
    "O1": "SEALED (promotion receipt PENDING_EXTERNAL_META_ORACLE)",
    "B1": "SEALED", "F0": "SEALED", "CF1": "SEALED (honest degrade: ContextForge DEGRADED/OASF N/A/OTel DEFERRED)",
    "F1": "SEALED", "KG1": "PARTIAL (crashed at remember() signature; provider-state ledger written)",
    "SQP1": "NOT_STARTED", "S1": "NOT_STARTED", "E1": "NOT_STARTED", "E2": "NOT_STARTED",
    "E3": "NOT_STARTED (conditional)", "R1": "NOT_STARTED",
}

md = f"""# RP-002 PRE-HERMES-REINSTALL HANDOFF (frozen)

> artifact: RP002_PRE_HERMES_REINSTALL_HANDOFF
> frozen_at_utc: {now}
> reason: user directive RESUME:RP002_FREEZE_PROGRESS_AND_HANDOFF_BEFORE_HERMES_REINSTALL
> construction STOPPED at this point; no further RP-002 mutation after this freeze.

## 1. Project / Run / Checkpoint identity
- project_id: HGK-REFERENCE-PROJECT-002 (RP-001 closure identity NOT reused)
- run_id: RUN-1217AA88
- spine state: {proj.get('state')}
- checkpoint file: C:\\Projects\\Agent_Workspace\\Fabric\\rp002\\CHECKPOINT.json (CP-003 — stale by design: written after D1; later gates carry their own evidence)
- oracle: EXTERNAL_FROZEN_BOOTSTRAP_ORACLE (G0 freeze); internal Oracle candidate materialized at O1, promotion PENDING external Meta-Oracle
- claim ceiling: RP002_LOCAL_ACCEPTANCE_PASS **NOT** claimed; PRODUCTION_AUTONOMY=NOT_CLAIMED; SQS_LIVE_TRADING=NOT_AUTHORIZED; REMOTE_DEPLOYMENT=NOT_CLAIMED

## 2. Current subject digests
- HGK HEAD: {hgk_head} (branch codex/hgk-final-closure-002; working tree has external + RP-002 changes, see §6)
- SQS HEAD: {sqs_head} (branch main; pre-existing deletions + untracked handoff dirs)
- Fabric HEAD: {fab_head} (git init'd 2026-08-11 for distribution commit binding)
- denominator jsonl sha256: 9ac92e9f05a2509d95f26c989ea1bf2ffd893e8865f72652fb9fafcca470149a (30372 files)
- G0 freeze sha256: 80759903e44895e30a209cbaa4b602eb5f95123cd36d5d31b11d4a6c1ac8be0a
- prompt r1 digest: c3f34ca28a6bc8c8b7255c721173ff00e694366eb3b15891d15b3b97f5453c70
- blueprint r3 digest: 6900e451e578bdcbb9b6e4fa5792277ef11a8389ae9b7fced94254d89d00f147
- KP00~19 pack digest: 24aa0390a0d27ea3049db0e6499f2e1cd3e4b5bd4cfdf5b24016fe4c82f1d4c7
- prompt compiler digest: 214c7f048f7361fe0bc4a324a0c99aaaf0df4191a430b645b8a97d24620064b6
- oracle package digest (O1 candidate): 8b43e00d2ba7fdc5a252cc371d854f2f1475e08730fd3e361c3b51b7cfbbece4
- oracle acceptance digest: 246d50bd71c92f09e0f2af3bb0a639197e8e9694c0bf2893758661b829deaa8f

## 3. Gate table
| Gate | Status | Evidence |
|---|---|---|
| G0 | SEALED | rp002/G0/RP002_G0_EVIDENCE.json + RP002_G0_INDEPENDENT_CHECKER.json (18/18) |
| G1 | SEALED | rp002/G1/RP002_G1_EVIDENCE.json (28/28) + RP002_G1_INDEPENDENT_CHECKER.json (10/10); real worker pid 14512 |
| K1 | SEALED | rp002/K1/* — governance 4717 files; norms source-bound; independent re-derive 7/7 |
| D1 | SEALED | rp002/D1/RP002_D1_EVIDENCE.json (orphan=0) + INDEPENDENT_CHECKER (9/9) |
| C1 | SEALED | rp002/C1/* (23/23 + independent); Fabric HEAD 68e4881 at seal |
| H1 | MAKER_ONLY | rp002/H1/RP002_H1_EVIDENCE.json (26/26) — **INDEPENDENT_CHECKER.json MISSING** (copytree temp-dir collision FileExistsError; rerun needed) |
| O1 | SEALED* | rp002/O1/RP002_O1_EVIDENCE.json (10/10) + INDEPENDENT_CHECKER — *promotion receipt PENDING_EXTERNAL_META_ORACLE per §7.4 |
| B1 | SEALED | rp002/B1/RP002_B1_EVIDENCE.json + INDEPENDENT_CHECKER; board rp002-fabric-bootstrap |
| F0 | SEALED | rp002/F0/RP002_F0_EVIDENCE.json + INDEPENDENT_CHECKER; consumer traces |
| CF1 | SEALED | rp002/CF1/* — honest degrade: ContextForge DEGRADED, OASF N/A, OTel DEFERRED; MCP server-mode handshake PASS |
| F1 | SEALED | rp002/F1/RP002_F1_EVIDENCE.json + INDEPENDENT_CHECKER; SELF_HOSTING_CUTOVER=true |
| KG1 | PARTIAL | rp002/KG1/RP002_KNOWLEDGE_PROVIDER_STATE.json only; crashed at KnowledgeFactory.remember() signature (ttl_seconds kwarg removed); fix + rerun |
| SQP1..R1 | NOT_STARTED | — |

## 4. Completed work (sealed)
- 11 gates fully sealed with maker + independent checker: G0 G1 K1 D1 C1 O1 B1 F0 CF1 F1 (+H1 maker-only)
- 4 HGK profile distributions materialized + installed in canonical home (hgk-orchestrator / -knowledge-factory / -document-factory / -coding-factory @0.1.0)
- construction-acceptance-oracle distribution materialized (Core+10 packs+3 validators+4 test suites+CHECKER recipe)
- Fabric git repo initialized (commit binding); HGK/TEAM.md, RP002/TEAM.md, HGK_STACK_MANIFEST.yaml, fabric contracts (AUTHORITY_MATRIX/RISK_CLASSES/PROMOTION_POLICY) + hgk_policy_consumer
- Shared Spine: 18 REQ-RP2-* FROZEN, 18 TS-RP2-* ADMITTED, 18 WO-RP2-* CREATED, 18 EVD1-* evidence refs
- blocking_tt = 0 (TT-A3-HERMES-RUNTIME closed with G1 evidence via ledger + reconcile)
- 教程字幕 corpus governed: 4717 files, 1061 dup groups, dispositions CURRENT 2992 / SUPERSEDED 31 / CONDITIONAL 1694
- mcp 1.28.1 + deps installed OFFLINE into canonical venv (see §8 — reinstall-sensitive)

## 5. Unfinished work
- KG1 (in progress; one script fix away: use positional args for remember() — see rp002_kg1_knowledge.py line ~99; evidence file incomplete)
- H1 independent checker re-run (evidence dir has maker only)
- SQP1 (3 SQS profiles + SQS/TEAM.md + SQS_STACK_MANIFEST.yaml)
- S1 (real SQS LOCAL/PAPER/NO-LIVE-WRITE canary)
- E1 (cross-stack evolution; fault-injection canary acceptable if no natural defect)
- E2 (behavioral artifact evolution; mandatory)
- E3 (conditional — N/A_WITH_SOURCE_LOCATOR unless Oracle changed)
- R1 (final aggregate acceptance + package readback + single external review MD per prompt §8)
- O1 promotion receipt (external Meta-Oracle confirmation via single review MD)

## 6. Git / worktree state
### HGK (C:\\Projects\\Agent_Workspace\\HG-KSEOS)
- HEAD {hgk_head}; branch codex/hgk-final-closure-002
- MODIFIED (uncommitted): docs/HG-KSEOS使用說明文檔.md (§11.1 Codex Desktop/Hermes provider lane isolation — EXTERNAL session change, not RP-002); source-freeze/TT_LEDGER.csv (RP-002: TT-A3 closed E-RP002-G1-PROVIDER-PILOT+TST-054-NRTV-SYMLINK-DISPOSITION — MINE)
- UNTRACKED (EXTERNAL session, not RP-002): SSOT/, config/hermes-codex-lane.json, evidence/review/HGK_CODEX_PROVIDER_LANE_ISOLATION_*.md/.json, scripts/start-hgk-hermes.ps1, scripts/test-hermes-codex-lane.ps1
### SQS (C:\\Projects\\Agent_Workspace\\SQS-THC)
- HEAD {sqs_head}; branch main; pre-existing deletions under 實作執行/實作方案、評估 + untracked 任務交接報告/ + 使用說明文檔/ (RP-001-era; not touched by RP-002)
### Fabric (C:\\Projects\\Agent_Workspace\\Fabric)
- HEAD {fab_head}; UNTRACKED: rp002/CF1/, rp002/F1/, rp002/KG1/, rp002/scripts/* (cf1/f1/kg1 helpers), RP-002_DOC/PROMPT/RP002_RUNTIME_BINDING_G1_REPAIR_AND_RESUME_PROMPT_r1_2026-08-12.md (EXTERNAL, 20089 bytes, NOT executed by me)
- Commit history: 68e4881 (c1 materialize) -> 8e07851 (c1-f0 profiles/team/oracle/contracts)
- Worktrees referenced by WO rows: rp002/worktrees/<gate> (path placeholders in spine; not materialized)

## 7. Evidence pointers (canonical)
- Gate evidence root: C:\\Projects\\Agent_Workspace\\Fabric\\rp002\\<GATE>\\
- Canonical single-review MD target (prompt §8): C:\\Projects\\Agent_Workspace\\Fabric\\evidence\\review\\RP002_EVIDENCE_FOR_EXTERNAL_REVIEW.md (NOT yet generated — next run must generate before ANY external upload)
- Denominator: rp002/G0/RP002_INPUT_DENOMINATOR.jsonl (+ .sha256, classification tsv)
- Spine DB: C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\shared-spine\\hg-kseos.db (project lifecycles / requirements / taskspecs / workorders / evidence_refs / tt_records)
- TT ledger: HG-KSEOS\\source-freeze\\TT_LEDGER.csv (TT-A3 row updated; reconcile-tt run)

## 8. Reinstall-sensitive runtime state (MUST preserve across Hermes reinstall)
- Canonical Hermes home: HG-KSEOS\\var\\hermes-v020\\home (isolated HERMES_HOME; kanban.db; sessions; 5 profiles installed: default + 4 HGK)
- Canonical executable/venv: HG-KSEOS\\var\\hermes-v020\\venv (Hermes v0.20.0 / v2026.8.3 / commit 3c27eb6234bf91b8ceee9e9071591b31e9b148cb)
- **OFFLINE package installs into canonical venv (mcp 1.28.1 + jsonschema/referencing/rpds/attrs/httpx_sse/sse_starlette/pydantic_settings) — copied from desktop hermes venv; will be LOST on venv rebuild; reinstall via Fabric\\rp002\\scripts\\install_mcp_offline.py**
- Kanban board rp002-fabric-bootstrap: 21 ready / 1 running (t_75e7d480 "B1 heartbeat probe" — claimed by B1 test, no real worker; reclaim/archive after reinstall) / 3 todo
- Profile distributions source: Fabric\\profiles\\ (git-tracked in Fabric)
- Provider credential: OPENCODE_GO_API_KEY is a process-scoped env-ref in %LOCALAPPDATA%\\hermes\\.env (desktop) — never stored in evidence
- Rollback baseline: Hermes v0.18.2 (9de9c25f) sealed per config/hermes.json

## 9. Open blockers / TT / CR
- blocking_tt = 0
- OPEN non-blocking TT: TT-HLPE-SRU-DRIFT (OPEN_NONBLOCKING_FOR_HLPE_BIND — pre-existing, not RP-002)
- O1 promotion: PENDING_EXTERNAL_META_ORACLE (GPT-5.6 Sol via single review MD) — HITL per prompt §7.4
- CF1 degrades (honest): ContextForge DEGRADED (offline), OASF SDK N/A_WITH_UPSTREAM_LOCATOR, OTel DEFERRED_CONDITIONAL
- External uncommitted changes in HGK (Codex provider lane isolation) — NOT RP-002's; coexist in same worktree; do not revert without user decision
- New external prompt RP002_RUNTIME_BINDING_G1_REPAIR_AND_RESUME_PROMPT_r1_2026-08-12.md — NOT executed by me; resolve with user whether it supersedes RP-002 continuation

## 10. Rollback pointers
- Fabric: git HEAD {fab_head} (all RP-002 artifacts versioned; revert = git reset/checkout)
- HGK: HEAD {hgk_head} clean baseline; uncommitted = TT ledger close + external lane-isolation set
- Hermes: v0.18.2 rollback baseline sealed (config/hermes.json)
- Profiles: uninstall via `hermes profile delete <name>`; distributions reinstallable from Fabric\\profiles\\
- mcp offline install: delete Fabric\\rp002\\scripts\\install_mcp_offline.py-installed packages from canonical venv site-packages
- Kanban: board rp002-fabric-bootstrap archive/disable returns to pre-F1 bootstrap path

## 11. RESUME_FROM recommendation
RESUME:KG1 -> SQP1 -> S1 -> E1 -> E2 -> E3(conditional) -> R1
1. Fix rp002_kg1_knowledge.py remember() call (remove ttl_seconds kwarg; check current signature), re-run KG1 maker + independent checker.
2. Re-run rp002_h1_independent_checker.py (temp-dir collision was environmental; rerun produces RP002_H1_INDEPENDENT_CHECKER.json).
3. Then SQP1..R1 per canonical RP002_EXECUTION_GRAPH.yaml.
4. Generate single external review MD (Fabric\\evidence\\review\\RP002_EVIDENCE_FOR_EXTERNAL_REVIEW.md) BEFORE any external upload; O1 promotion receipt to be granted by external Meta-Oracle.
Only R1 reducer exit 0 (all mandatory gates PASS, blocking_tt=0) may claim RP002_LOCAL_ACCEPTANCE_PASS.

## 12. Do-not-discard list
- Fabric\\rp002\\ (all gate evidence + scripts + machine-truth artifacts) — the single most valuable tree
- Fabric\\profiles\\ (8 profile distribution sources)
- Fabric\\fabric\\ (governance contracts + consumer)
- HG-KSEOS\\var\\shared-spine\\hg-kseos.db (normative spine)
- HG-KSEOS\\var\\hermes-v020\\home + \\venv (runtime; mcp offline install inside)
- 教程字幕 corpus governance outputs (rp002/K1/*) — corpus itself untouched (provenance-ledger only)
- source-freeze/TT_LEDGER.csv current state (TT-A3 closure row)
"""

OUT.write_text(md, encoding="utf-8")
raw = OUT.read_bytes()
digest = hashlib.sha256(raw).hexdigest()
readback = {
    "path": str(OUT), "bytes": len(raw), "sha256": digest,
    "first_line": raw.decode("utf-8").splitlines()[0],
    "readback_ok": True,
}
(REVIEW / "RP002_PRE_HERMES_REINSTALL_HANDOFF.sha256").write_text(digest + "\n", encoding="ascii")
print(json.dumps(readback, ensure_ascii=False, indent=2))
