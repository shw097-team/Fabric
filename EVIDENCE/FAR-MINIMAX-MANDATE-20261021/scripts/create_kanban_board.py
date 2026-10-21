#!/usr/bin/env python
"""Create the KANBAN board for FAR-MINIMAX-MANDATE-20261021.

The board records THIS ROUND's work. It is created with the same schema the existing boards
use (board.json + kanban.db with the `tasks` table), because the KANBAN surface is a Hermes
runtime feature and the board is its data, not a document.

The board deliberately separates what was EXECUTED from what is AWAITING AN OWNER RULING:
the owner's instruction this round was "propose the ruling and let the user confirm", so the
ruling-dependent items are `blocked` with a reason, not `done`.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path

B = Path(os.environ["LOCALAPPDATA"]) / "Packages" / "OpenAI.Codex_2p2nqsd0c76g0" / \
    "LocalCache" / "Local" / "hermes" / "kanban" / "boards"
SLUG = "far-minimax-mandate-20261021"
WORKDIR = "C:/Projects/Agent_Workspace/HG-KSEOS"

TASKS = [
    # (title, status, result, priority)
    ("MiniMax three-lane feasibility probe (PLAN/EXECUTE/VERIFY_SECURITY)", "done",
     "all three lanes served opencode-go/minimax-m3.1-flash-free at required_arm == served_arm, exit 0, model drove a real shell tool", 0),
    ("HGK admission for the three MiniMax arms", "done",
     "PLAN=ADMITTED, EXECUTE=ADMITTED, VERIFY_SECURITY=ADMITTED (completed_tools>=1, identity match)", 0),
    ("epoch 25 binding: pool rank-1 + registry routes + assignment derivation + projection", "done",
     "epoch 24->25; MiniMax rank 1 in all three pools with contiguous ranks; all prior arms preserved as fallbacks; SOD006-C5 declared; EXECUTE->VERIFY distinct_required true->false with the reason recorded", 0),
    ("drift gate", "done", "check_drift() == [] (0 findings)", 0),
    ("SBL construction exclusion (parallel session in Fabric)", "done",
     "zero writes to fabric-autonomous-research/runs/FAR-20261021-02x-*; both untracked dirs left untouched for the constructing session", 0),
    ("var/ disposition index (measured, non-destructive)", "done",
     "120 top-level dirs indexed; classes ROUND_ARTIFACT=75, ROUND_OPEN=8, RUNTIME_OR_CACHE=3, EMPTY=2, UNCLASSIFIED=32; destructive_actions_taken=0", 1),
    ("OpenSpec unchecked index (measured, zero ticks applied)", "done",
     "38 active changes, 34 with unchecked items, 460 unchecked total (the owner's 471 is a stale estimate); ticks_applied_by_this_script=0", 1),
    ("TT ledger OPEN verification", "done",
     "exactly 2 rows with status == 'OPEN' (HGK-EBC-TT-001, HGK-EBC-TT-002); the third open-ish row has a different status value", 1),
    ("FAR ruling report (owner confirmation requested)", "done",
     "var/FAR-MINIMAX-MANDATE-20261021/FAR-RULING-REPORT.md: rulings A (460 ticks), B (120 dirs), C (2 TT rows), D (model-axis independence), E (delegation plane)", 0),
    ("research subagent: OpenSpec 460-item classification", "done",
     "deleg_4d2d40d9 (MiniMax): 19 tick-backfill candidates, 11 superseded dispositions, remainder needs real engineering work", 2),
    ("research subagent: knowledge-base cross-check", "done",
     "deleg_5ff913cf (MiniMax): reusable precedents vs other-project-surface files that do NOT apply", 2),
    ("independent acceptance (AO) on the MiniMax VERIFY lane", "done",
     "AO verdict recorded under var/FAR-MINIMAX-MANDATE-20261021/probes/; claim ceiling CANDIDATE_ONLY", 0),
    ("OWNER RULING A: tick 19 cross-verifiable OpenSpec items", "blocked",
     "awaiting the owner's confirmation of ruling A1; each tick must carry its own verification evidence (commit or file), never a batch", 3),
    ("OWNER RULING B: disposition of the 120 var/ directories", "blocked",
     "awaiting the owner's confirmation of ruling B1-B4; the recommendation is to delete NOTHING except possibly the 3 RUNTIME_OR_CACHE + 2 EMPTY dirs, which needs explicit approval", 3),
    ("OWNER RULING C: TT ledger HGK-EBC-TT-001 / -002 status", "blocked",
     "awaiting the owner's confirmation of ruling C1-C2; TT-001 needs a migration change, TT-002 needs a cross-entity contract decision", 3),
    ("OWNER RULING D: model-axis independence on the three lanes", "blocked",
     "SOD006-C5 is already declared (the collision is recorded, not hidden); the owner decides whether to restore separation by keeping gpt-6.1-sol as an operator-selectable VERIFY arm", 3),
    ("OWNER RULING E: make the delegation plane MiniMax permanently", "blocked",
     "this round pinned it temporarily (gpt-6.1-sol was rate-limited) and restored it; permanence needs the owner's confirmation", 3),
]


def main() -> None:
    d = B / SLUG
    d.mkdir(parents=True, exist_ok=True)
    (d / "board.json").write_text(json.dumps({
        "slug": SLUG,
        "name": "FAR MiniMax Mandate 20261021",
        "description": ("Owner order 2026-10-21: PLAN/EXECUTE/VERIFY_SECURITY all on MiniMax M3.1 "
                        "Flash (OPENCODE GO). FAR ruling over 460 unchecked OpenSpec items, 120 var/ "
                        "directories and 2 TT ledger OPEN rows. Ruling-dependent work is blocked "
                        "pending the owner's confirmation."),
        "icon": "", "color": "",
        "default_workdir": WORKDIR,
        "project_id": None,
        "created_at": int(time.time()),
        "archived": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    db = d / "kanban.db"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(str(db))
    con.execute("""CREATE TABLE tasks (
        id TEXT PRIMARY KEY, title TEXT, body TEXT, assignee TEXT, status TEXT,
        priority INTEGER, created_by TEXT, created_at INTEGER, started_at INTEGER,
        completed_at INTEGER, workspace_kind TEXT, workspace_path TEXT, branch_name TEXT,
        project_id TEXT, claim_lock TEXT, claim_expires INTEGER, tenant TEXT, result TEXT,
        idempotency_key TEXT, consecutive_failures INTEGER DEFAULT 0, worker_pid INTEGER,
        worker_started_at INTEGER, last_failure_error TEXT, max_runtime_seconds INTEGER,
        last_heartbeat_at INTEGER, current_run_id TEXT, workflow_template_id TEXT,
        current_step_key TEXT, skills TEXT, model_override TEXT, provider_override TEXT,
        reasoning_effort TEXT, max_retries INTEGER, goal_mode INTEGER DEFAULT 0,
        goal_max_turns INTEGER, session_id TEXT, block_kind TEXT, block_recurrences INTEGER DEFAULT 0,
        completion_contract TEXT DEFAULT 'local-only')""")
    con.execute("""CREATE TABLE task_links (
        parent_id TEXT, child_id TEXT, link_type TEXT, created_at INTEGER)""")
    con.execute("""CREATE TABLE task_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, author TEXT, body TEXT,
        created_at INTEGER)""")
    con.execute("""CREATE TABLE task_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, event_type TEXT, payload TEXT,
        created_at INTEGER)""")
    con.execute("""CREATE TABLE task_runs (
        id TEXT PRIMARY KEY, task_id TEXT, status TEXT, started_at INTEGER, finished_at INTEGER,
        result TEXT)""")
    con.execute("""CREATE TABLE task_attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT, path TEXT, kind TEXT, created_at INTEGER)""")
    con.execute("""CREATE TABLE kanban_notify_subs (board_slug TEXT, channel TEXT, target TEXT)""")

    now = int(time.time())
    for i, (title, status, result, pri) in enumerate(TASKS):
        tid = "t_%s%02d" % (SLUG[:4], i)
        con.execute(
            "INSERT INTO tasks (id,title,body,assignee,status,priority,created_by,created_at,"
            "started_at,completed_at,workspace_kind,workspace_path,result,completion_contract) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (tid, title, None, None, status, pri, "user", now,
             now if status == "done" else None,
             now if status == "done" else None,
             "scratch", None, result, "local-only"))
        con.execute("INSERT INTO task_events (task_id,event_type,payload,created_at) VALUES (?,?,?,?)",
                    (tid, "created", json.dumps({"title": title, "status": status}), now))
        if status == "done":
            con.execute("INSERT INTO task_events (task_id,event_type,payload,created_at) VALUES (?,?,?,?)",
                        (tid, "completed", json.dumps({"result": result}), now))
        else:
            con.execute("INSERT INTO task_events (task_id,event_type,payload,created_at) VALUES (?,?,?,?)",
                        (tid, "blocked", json.dumps({"reason": result}), now))
    con.commit()
    con.close()

    done = sum(1 for t in TASKS if t[1] == "done")
    blocked = sum(1 for t in TASKS if t[1] == "blocked")
    print(json.dumps({"board": SLUG, "cards": len(TASKS), "done": done,
                      "blocked_awaiting_owner": blocked}, ensure_ascii=False))


if __name__ == "__main__":
    main()
