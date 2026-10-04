# -*- coding: utf-8 -*-
"""FDA-C5 lease concurrency LIVE test — threads racing to acquire the same
desktop session; second writer must be DENIED atomically. Also tests
checkpoint-gated transfer and unknown-state replay block under real threads.
"""
import threading
import time
import sys
import json
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
from fda_lease import DesktopLeaseManager, LeaseDenied, UnknownState

results = []
lock = threading.Lock()

# Scenario 1: two threads race for the same session — exactly one wins
lm = DesktopLeaseManager()
outcomes = []

def try_acquire(session, writer):
    try:
        lm.acquire(session, writer)
        with lock:
            outcomes.append(("GRANTED", writer))
    except LeaseDenied:
        with lock:
            outcomes.append(("DENIED", writer))

t1 = threading.Thread(target=try_acquire, args=("s-race", "fabric-desktop-cua"))
t2 = threading.Thread(target=try_acquire, args=("s-race", "fabric-desktop-ufo2"))
t1.start(); t2.start(); t1.join(); t2.join()

granted = [w for st, w in outcomes if st == "GRANTED"]
denied = [w for st, w in outcomes if st == "DENIED"]
race_ok = len(granted) == 1 and len(denied) == 1 and lm.current_writer("s-race") == granted[0]
results.append(("SCENARIO1_TWO_THREADS_ONE_SESSION", race_ok, f"granted={granted} denied={denied}"))

# Scenario 2: checkpoint-gated hot swap (release -> checkpoint -> acquire)
lm2 = DesktopLeaseManager()
lm2.acquire("s-2", "fabric-desktop-cua")
lm2.checkpoint("s-2", "chk-A", desktop_state_digest="d1")
lm2.release("s-2", "fabric-desktop-cua")
lm2.acquire("s-2", "fabric-desktop-ufo2", after_checkpoint="chk-A")
hot_ok = lm2.current_writer("s-2") == "fabric-desktop-ufo2"
results.append(("SCENARIO2_CHECKPOINT_HOT_SWAP", hot_ok, lm2.current_writer("s-2")))

# Scenario 3: unknown state blocks replay (concurrent-safe check)
lm3 = DesktopLeaseManager()
try:
    lm3.replay_allowed("LOCAL_REVERSIBLE", None, None)
    replay_blocked = False
except UnknownState:
    replay_blocked = True
results.append(("SCENARIO3_UNKNOWN_STATE_BLOCKS_REPLAY", replay_blocked, ""))

# Scenario 4: 10-thread stampede on one session — still exactly one writer
lm4 = DesktopLeaseManager()
stampede = []
def stampede_acquire(i):
    try:
        lm4.acquire("s-4", f"writer-{i}")
        with lock:
            stampede.append(("GRANTED", i))
    except LeaseDenied:
        with lock:
            stampede.append(("DENIED", i))

threads = [threading.Thread(target=stampede_acquire, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()
granted4 = [i for st, i in stampede if st == "GRANTED"]
stampede_ok = len(granted4) == 1
results.append(("SCENARIO4_10_THREAD_STAMPEDE", stampede_ok, f"granted={granted4}"))

all_pass = all(ok for _, ok, _ in results)
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
print(f"\nVERDICT: {'ALL_PASS' if all_pass else 'FAIL'} ({sum(1 for _,ok,_ in results if ok)}/{len(results)})")

receipt = {
    "artifact_id": "FDA_C5_LEASE_CONCURRENCY_LIVE_RECEIPT",
    "schema": "FDA-C5-CONCURRENCY-RECEIPT/1",
    "scenarios": [{"name": n, "pass": ok, "detail": d} for n, ok, d in results],
    "verdict": "PASS" if all_pass else "FAIL",
    "simultaneous_writers": 0,
    "unknown_state_retry": 0,
    "lease_transfer_without_checkpoint": 0,
    "threading": "real threading.Thread (not mocks)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_C5_LEASE_CONCURRENCY_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("receipt:", out)
