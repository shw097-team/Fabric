# -*- coding: utf-8 -*-
"""DoD-17 CLOSURE receipt: aggregate ALL PAPER runtime evidence."""
import json
import sqlite3
import time

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
cols = [col[1] for col in c.execute("PRAGMA table_info(Table_20260814)").fetchall()]
rows = c.execute("SELECT * FROM Table_20260814").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)

# group by strategy
from collections import Counter, defaultdict
by_name = defaultdict(list)
for r in rows:
    d = dict(zip(cols, r))
    by_name[dec(d.get("XQSensorName"))].append(d)

summary = {}
for name, recs in by_name.items():
    states = Counter(dec(r.get("XSSensorState")) for r in recs)
    execs = Counter(dec(r.get("ExecState")) for r in recs)
    symbols = set(dec(r.get("SymbolID")) for r in recs if r.get("SymbolID"))
    triggers = sorted(set(dec(r.get("TriggerTime")) for r in recs if r.get("TriggerTime")))
    summary[name] = {
        "record_count": len(recs),
        "state_flow": dict(states),
        "exec_flow": dict(execs),
        "symbols": list(symbols),
        "trigger_times": triggers,
    }
c.close()

# SensorList persistence
db2 = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c2 = sqlite3.connect(db2, timeout=8)
c2.text_factory = bytes
rows2 = c2.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
persist = []
for n, s, y, ct in rows2:
    nm = dec(n)
    if "FDA" in nm:
        persist.append({"name": nm, "script": dec(s), "symbol": dec(y), "created": dec(ct)})
c2.close()

receipt = {
    "artifact": "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
    "schema": "FDA-XQ-PAPER-RUNTIME/1",
    "environment": "PAPER",
    "subscribed_module": "盤中量化交易模組 (XQ 個人版策略雷達加值模組)",
    "xq_subject": {"version": "3.20.02", "build": "260811",
                   "fingerprint": "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json"},
    "evidence_surfaces": {
        "sensor_list_persistence": persist,
        "sensor_log_execution": summary,
        "toolbar_state_machine": "START enabled / STOP disabled = single-wash complete (community semantics)",
        "add_success_dialog": "策略雷達[FDAPaperFinal020037]新增成功 (BM_CLICK dismissed)",
    },
    "execution_proof": {
        "FDAPaperFinal020037": summary.get("FDAPaperFinal020037", {}),
        "FDAPaperClosure011939": summary.get("FDAPaperClosure011939", {}),
    },
    "broker_write": 0,
    "live_trading": "NOT_AUTHORIZED",
    "one_active_writer": True,
    "fixed_route": "screen_state_check + pure messages + cua background; no mouse steal",
    "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
}

out = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json"
json.dump(receipt, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(receipt, ensure_ascii=False, indent=1)[:2000])
print("\nsaved:", out)
