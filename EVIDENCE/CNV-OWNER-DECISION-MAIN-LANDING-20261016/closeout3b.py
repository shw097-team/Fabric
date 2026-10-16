"""Spine closeout, take 2 — the first attempt's filter was wrong and this seals the write set first.

Defect found in take 1: `workorders` has no project column, so filtering on `project_id` selected the whole
table (587 rows) and the loop would have recorded results for every workorder in the spine. The process aborted
on a broken pipe during listing, before the loop, and a read of the database confirmed no state changed. This
version resolves the project through `taskspecs`, prints the sealed write set, refuses to write unless the set is
non-empty and small, and records what it skipped.
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
sys.path.insert(0, str(ROOT / "src"))
from hg_kseos.cli import spine_for                                     # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController as PLC       # noqa: E402

PROJECT = "CNV-OWNER-DECISION-LANDING"
PREFIX = "EVIDENCE/CNV-OWNER-DECISION-MAIN-LANDING-20261016"
WRITER = "codex/opencode-go-deepseek-v4.1-flash"
CHECKER = "codex-verify/openai-codex-gpt-6.1-sol"
EVIDENCE = [PREFIX + "/FAR_RULING_2.json", PREFIX + "/MERGE_DECISION.json",
            PREFIX + "/VERDICT3_RECHECK.md", PREFIX + "/LANE_EXEC_RECEIPT.json",
            PREFIX + "/LANE_VERIFY_RECEIPT_2.json", PREFIX + "/SELF_CHECK_RECEIPT_2.json"]
TERMINAL = ("DELIVERED", "CLOSED", "ACCEPTED", "CANCELLED", "VERIFIED")
OUT = Path("C:/Projects/Agent_Workspace/_handover/CNV-OWNER-DECISION-MAIN-LANDING-20261016/SPINE_CLOSEOUT.json")

con = sqlite3.connect(str(ROOT / "var" / "shared-spine" / "hg-kseos.db"))
tcols = [r[1] for r in con.execute("PRAGMA table_info(taskspecs)")]
print("taskspecs columns:", tcols)
join = ("SELECT w.workorder_id, w.state, t.taskspec_id FROM workorders w JOIN taskspecs t "
        "ON w.taskspec_id = t.taskspec_id")
if "project_id" in tcols:
    sel = join + " WHERE t.project_id = ?"
    rows = con.execute(sel, (PROJECT,)).fetchall()
else:
    pcols = [r[1] for r in con.execute("PRAGMA table_info(projects)")]
    print("projects columns:", pcols, "| no project_id on taskspecs -> manual seal only")
    rows = []
print("sealed write set (%s): %d workorders" % (PROJECT, len(rows)))
for wid, st, ts in rows:
    print("   %-34s %-20s %s" % (wid, st, ts))
if not rows or len(rows) > 12:
    print("REFUSING TO WRITE: sealed set is empty or implausibly large (%d)" % len(rows))
    OUT.write_text(json.dumps({"schema": "CNV-OWNER-DECISION/SPINE-CLOSEOUT/1", "project": PROJECT,
                               "write_set_sealed": len(rows), "wrote": False,
                               "reason": "sealed set empty or implausible; no write attempted"}, indent=1),
                   encoding="utf-8")
    sys.exit(0)

spine = spine_for(ROOT)
lc = PLC(spine)
outcomes = []
for wid, st, ts in rows:
    if st in TERMINAL:
        outcomes.append({"workorder": wid, "state": st, "skipped": "already terminal"})
        continue
    try:
        r = spine.record_workorder_result(wid, writer=WRITER, checker=CHECKER, verdict="DELIVERED",
                                          evidence_refs=EVIDENCE,
                                          evidence_subject=PREFIX + "/SELF_CHECK_RECEIPT_2.json")
        outcomes.append({"workorder": wid, "state_before": st, "recorded": True,
                         "result_verdict": (r or {}).get("verdict") if isinstance(r, dict) else str(r)[:80]})
    except Exception as e:                                              # noqa: BLE001
        outcomes.append({"workorder": wid, "state_before": st, "recorded": False,
                         "error": "%s: %s" % (type(e).__name__, e)})
for label, fn in (("status", lc.status), ("completion_sweep", lc.completion_sweep), ("denominator", lc.denominator)):
    try:
        outcomes.append({label: fn(PROJECT)})
    except Exception as e:                                              # noqa: BLE001
        outcomes.append({label + "_error": "%s: %s" % (type(e).__name__, e)})
for target in ("DELIVERED", "EVOLUTION_REVIEW"):
    try:
        outcomes.append({"transition_%s" % target: lc.transition(PROJECT, target)})
        break
    except Exception as e:                                              # noqa: BLE001
        outcomes.append({"transition_%s_error" % target: "%s: %s" % (type(e).__name__, e)})

rec = {"schema": "CNV-OWNER-DECISION/SPINE-CLOSEOUT/1", "project": PROJECT, "write_set_sealed": len(rows),
       "writer": WRITER, "checker": CHECKER,
       "model_axis_separation": "real: opencode-go/deepseek-v4.1-flash writer vs openai-codex/gpt-6.1-sol checker",
       "evidence_refs": EVIDENCE, "outcomes": outcomes}
OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("--- outcomes ---")
for o in outcomes:
    print(json.dumps(o, ensure_ascii=False)[:220])
print("wrote", OUT.name, OUT.stat().st_size, "bytes")
