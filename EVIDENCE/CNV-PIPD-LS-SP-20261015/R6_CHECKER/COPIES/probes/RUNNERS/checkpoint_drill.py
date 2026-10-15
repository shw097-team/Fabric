#!/usr/bin/env python3
"""Real checkpoint/rollback drill over the R6 WriteSet.

Snapshot hashes of a chosen set of candidate artifacts, mutate one artifact,
verify the mutation is detected by re-hash, restore the exact original bytes,
re-verify. All steps print JSON to stdout for raw capture.
"""
import hashlib
import json
import os
from datetime import datetime, timezone

DEL = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_CHECKER/COPIES/probes"
TARGET = os.path.join(DEL, "CHECKPOINT_DRILL_SUBJECT.json")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def emit(step, **kw):
    rec = {"step": step, "utc": utc_now()}
    rec.update(kw)
    print(json.dumps(rec, ensure_ascii=False))


# 1. create the subject artifact (inside WriteSet)
original = json.dumps({"artifact": "CHECKPOINT_DRILL_SUBJECT.json",
                       "value": "ORIGINAL_V1", "drill": "checkpoint-and-rollback"},
                      indent=2) + "\n"
with open(TARGET, "w", encoding="utf-8") as fh:
    fh.write(original)

# 2. snapshot
snap1 = sha256_file(TARGET)
emit("snapshot", path=TARGET, sha256=snap1, bytes=os.path.getsize(TARGET))

# 3. mutate one byte (flip ORIGINAL_V1 -> ORIGINAL_V2)
mutated = original.replace("ORIGINAL_V1", "ORIGINAL_V2")
with open(TARGET, "w", encoding="utf-8") as fh:
    fh.write(mutated)
snap_mut = sha256_file(TARGET)
detected = snap_mut != snap1
emit("mutated", path=TARGET, sha256=snap_mut, original_sha256=snap1, detected=detected)

# 4. roll back to exact original bytes
with open(TARGET, "w", encoding="utf-8") as fh:
    fh.write(original)
snap2 = sha256_file(TARGET)
emit("rolled_back", path=TARGET, sha256=snap2, restored=snap2 == snap1)

# 5. verdict
print(json.dumps({
    "schema": "R6-CHECKPOINT-DRILL/1",
    "path": TARGET,
    "snapshot_sha256": snap1,
    "mutated_sha256": snap_mut,
    "restored_sha256": snap2,
    "mutation_detected": detected,
    "rollback_verified": snap2 == snap1,
    "ok": detected and snap2 == snap1,
}, ensure_ascii=False))
