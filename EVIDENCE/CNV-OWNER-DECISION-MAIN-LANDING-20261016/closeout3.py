"""Spine closeout for CNV-OWNER-DECISION-MAIN-LANDING-20261016.

Writer and checker are genuinely different models this round: the EXECUTE lane ran
opencode-go/deepseek-v4.1-flash and the VERIFY lane ran openai-codex/gpt-6.1-sol, so the spine's
writer != checker requirement is satisfied on the model axis and not merely asserted.
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
sys.path.insert(0, str(ROOT / "src"))
from hg_kseos.cli import spine_for                      # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController as PLC   # noqa: E402

PROJECT = "CNV-OWNER-DECISION-LANDING"
PREFIX = "EVIDENCE/CNV-OWNER-DECISION-MAIN-LANDING-20261016"
WRITER = "codex/opencode-go-deepseek-v4.1-flash"
CHECKER = "codex-verify/openai-codex-gpt-6.1-sol"
EVIDENCE = [
    PREFIX + "/FAR_RULING_2.json",
    PREFIX + "/MERGE_DECISION.json",
    PREFIX + "/VERDICT3_RECHECK.md",
    PREFIX + "/LANE_EXEC_RECEIPT.json",
    PREFIX + "/LANE_VERIFY_RECEIPT_2.json",
    PREFIX + "/SELF_CHECK_RECEIPT_2.json",
]

db = ROOT / "var" / "shared-spine" / "hg-kseos.db"
con = sqlite3.connect(str(db))
tabs = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("tables:", [t for t in tabs if "work" in t or "project" in t or "task" in t])
wo_tab = next((t for t in ("workorders", "work_orders", "workorder") if t in tabs), None)
rows = []
if wo_tab:
    cols = [r[1] for r in con.execute("PRAGMA table_info(%s)" % wo_tab)]
    print("columns:", cols)
    pid_col = next((c for c in cols if c.lower() in ("project_id", "project")), None)
    sel = "SELECT %s, * FROM %s" % (",".join('"%s"' % c for c in cols), wo_tab)
    for r in con.execute(sel):
        d = dict(zip(cols, r))
        if pid_col and d.get(pid_col) != PROJECT:
            continue
        rows.append(d)
print("workorders for %s: %d" % (PROJECT, len(rows)))
for d in rows:
    print("  ", {k: d[k] for k in list(d)[:6]})

spine = spine_for(ROOT)
lc = PLC(spine)
out = []
for d in rows:
    wid = d.get("id") or d.get("workorder_id")
    state = (d.get("state") or d.get("status") or "").upper()
    if not wid or state in ("DELIVERED", "CLOSED", "ACCEPTED", "CANCELLED"):
        out.append({"workorder": wid, "state": state, "skipped": "already terminal"})
        continue
    try:
        r = spine.record_workorder_result(wid, writer=WRITER, checker=CHECKER, verdict="DELIVERED",
                                          evidence_refs=EVIDENCE,
                                          evidence_subject=PREFIX + "/SELF_CHECK_RECEIPT_2.json")
        out.append({"workorder": wid, "state": state, "recorded": True,
                    "result": {k: v for k, v in r.items() if not isinstance(v, (list, dict))}})
    except Exception as e:                                   # noqa: BLE001
        out.append({"workorder": wid, "state": state, "recorded": False, "error": "%s: %s" % (type(e).__name__, e)})
try:
    st = lc.status(PROJECT)
    out.append({"project_status": st})
except Exception as e:                                       # noqa: BLE001
    out.append({"project_status_error": "%s: %s" % (type(e).__name__, e)})
for name in ("completion_sweep", "denominator"):
    try:
        out.append({name: getattr(lc, name)(PROJECT)})
    except Exception as e:                                   # noqa: BLE001
        out.append({name + "_error": "%s: %s" % (type(e).__name__, e)})
try:
    out.append({"transition_to_DELIVERED": lc.transition(PROJECT, "DELIVERED")})
except Exception as e:                                       # noqa: BLE001
    out.append({"transition_error": "%s: %s" % (type(e).__name__, e)})

rec = {"schema": "CNV-OWNER-DECISION/SPINE-CLOSEOUT/1", "project": PROJECT, "writer": WRITER,
       "checker": CHECKER, "model_axis_separation": "real: deepseek writer vs gpt-6.1-sol checker",
       "evidence_refs": EVIDENCE, "outcomes": out}
p = Path("C:/Projects/Agent_Workspace/_handover/CNV-OWNER-DECISION-MAIN-LANDING-20261016/SPINE_CLOSEOUT.json")
p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("--- outcomes ---")
for o in out:
    print(json.dumps(o, ensure_ascii=False)[:300])
print("wrote", p.name, p.stat().st_size, "bytes")
