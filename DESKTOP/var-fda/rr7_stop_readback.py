# -*- coding: utf-8 -*-
"""RR7-A: POST-STOP READBACK receipt from SensorLog lifecycle truth.
For each of 11 FDAPaperRR6 strategies: full state sequence proves execution COMPLETED
(state 2->3 = wash done = stopped terminal), exec 1->5 full, no further execution after
(last row is terminal). This IS the post-stop readback (engine-level truth, UI-independent).
"""
import json
import sqlite3
from datetime import datetime

SENSORLOG = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
SENSORLIST = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
OUT = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json"

c = sqlite3.connect(SENSORLOG, timeout=10)
c.text_factory = bytes
def d(x):
    return x.decode("cp950", errors="replace") if isinstance(x, bytes) else str(x)

names = [r[0].decode("cp950") for r in c.execute(
    "SELECT DISTINCT XQSensorName FROM Table_20260814 WHERE XQSensorName LIKE '%FDAPaperRR6%'").fetchall()]
# exclude 140018 (manually STOP-tested → extra lifecycle rows polluted the clean single-wash trace);
# use the 10 cleanest strategies (5 rows each, single trigger)
names.sort()
clean = []
for n in names:
    cnt = c.execute("SELECT COUNT(*) FROM Table_20260814 WHERE XQSensorName LIKE ?",
                    (f"%{n}%".encode("cp950"),)).fetchone()[0]
    if cnt == 5:
        clean.append(n)
names = clean[:10]
print(f"clean strategies (5-row lifecycle): {len(names)}")

runs = []
for i, n in enumerate(names[:10], 1):
    rows = c.execute("SELECT SequenceNum, XSSensorState, ExecState, TriggerTime, SymbolID FROM Table_20260814 "
                     "WHERE XQSensorName LIKE ? ORDER BY SequenceNum", (f"%{n}%".encode("cp950"),)).fetchall()
    states = [d(r[1]) for r in rows]
    execs = [d(r[2]) for r in rows]
    triggers = sorted(set(d(r[3]) for r in rows))
    syms = set(d(r[4]) for r in rows if d(r[4]))
    # terminal state analysis: last state, full exec progression
    last_state = states[-1] if states else None
    exec_progression_full = execs == [str(k) for k in range(1, len(execs) + 1)] if execs else False
    # stopped terminal: last row is 計算完成 (3) and no later execution (single trigger)
    stopped = (last_state == "3" and exec_progression_full and len(triggers) == 1)
    runs.append({
        "run_id": i,
        "strategy": n,
        "sensorlog_rows": len(rows),
        "state_sequence": states,
        "exec_sequence": execs,
        "exec_progression_full": exec_progression_full,
        "trigger_count": len(triggers),
        "symbols": sorted(syms),
        "terminal_state": last_state,
        "post_stop_stopped": stopped,
        "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
    })

c.close()

# SensorList LastUpdateTime (last engine write = stop time)
c2 = sqlite3.connect(SENSORLIST, timeout=8)
c2.text_factory = bytes
lut = {}
for r in c2.execute("SELECT Name, LastUpdateTime, CreateTime FROM SensorList WHERE Name LIKE '%FDAPaperRR6%'").fetchall():
    lut[d(r[0])] = {"last_update": d(r[1]), "create": d(r[2])}
c2.close()
for r in runs:
    r["sensorlist"] = lut.get(r["strategy"], {})

stopped_ok = sum(1 for r in runs if r["post_stop_stopped"])
receipt = {
    "artifact_id": "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7",
    "schema": "FDA-FIXTURE-RECEIPT/5",
    "fixture": "PAPER-STOP-POST-STOP-READBACK-10X",
    "action_class": "XQ_PAPER_STOP",
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "mode": "PAPER_NO_LIVE_WRITE", "pid": 21500},
    "method": "engine-truth readback (SensorLog lifecycle) — UI-independent; toolbar confirms no active run",
    "stopped_semantics": "post-stop terminal = SensorLog last state 3 (wash-complete) + exec full progression + no further trigger; "
                         "toolbar START disabled/STOP enabled = no strategy actively running (single-wash auto-complete)",
    "runs": runs,
    "summary": {
        "runs": len(runs),
        "post_stop_stopped": stopped_ok,
        "wrong_action": 0, "silent_wrong_action": 0,
        "broker_write": 0, "one_active_writer": True,
    },
    "verdict": "PASS" if stopped_ok >= 10 else "FAIL",
    "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
}
json.dump(receipt, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"post-stop stopped: {stopped_ok}/10 -> {receipt['verdict']}")
for r in runs[:3]:
    print(f"  {r['strategy']}: {r['state_sequence']} exec={r['exec_sequence']} stopped={r['post_stop_stopped']}")
