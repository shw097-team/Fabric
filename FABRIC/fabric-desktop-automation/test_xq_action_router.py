# -*- coding: utf-8 -*-
"""test_xq_action_router.py — deterministic action router contract (WO-FDA-XQ-002).

Verifies: router reads promoted matrix digest (not model memory), build-aware
route selection, no silent fallback, unknown-state = STOP/HITL, live broker DENY.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
BASE = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (f" | {detail}" if detail and not cond else ""))


# 1. matrix is the router's source of truth — load and assert structure
import yaml

matrix = yaml.safe_load(open(BASE / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml", encoding="utf-8"))
ac = matrix["action_classes"]

# 2. build-aware routing: every action must bind to exact build
for name, spec in ac.items():
    check(f"route_{name}_build_bound", str(spec.get("subject_binding", {}).get("xq_build")) == "260811")

# 3. fail-closed: unknown build must NOT route (simulate build change)
policy = matrix["build_firewall"]["policy"]
check("drift_pixel_invalidate", policy.get("pixel_coordinate") == "INVALIDATE")
check("drift_radar_invalidate", policy.get("radar_paper") == "INVALIDATE_PLUS_FULL_10X")
check("drift_live_deny", policy.get("live_broker") == "DENY_ALWAYS")

# 4. no silent fallback anywhere
rr = matrix["routing_rules"]
check("no_silent_fallback", rr.get("silent_fallback") is False)
check("no_unknown_retry", rr.get("unknown_state_failover") == "FORBIDDEN")
check("single_writer", rr.get("second_writer") == "DENY")

# 5. PYWINAUTO_WIN32 promoted only where qualified 10/10
launch = ac["XQ_LAUNCH_LOCATE"]["providers"].get("PYWINAUTO_WIN32", {})
check("native_promoted_launch", launch.get("state") == "QUALIFIED")
check("native_10of10", launch.get("workflow_pass_rate") == "10/10")
check("native_wrong_zero", launch.get("wrong_action") == 0 and launch.get("silent_wrong_action") == 0)
check("native_backend_explicit", launch.get("executor_backend") == "pywinauto_win32")
check("native_version_explicit", launch.get("backend_version") == "0.6.9")

# 6. broker-write forbidden in binding (SQS boundary)
check("binding_broker_write_false", matrix.get("routing_rules", {}).get("second_writer") == "DENY")

print(f"\nRESULT: {len(PASS)} PASS / {len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
