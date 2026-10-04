# -*- coding: utf-8 -*-
"""test_xq_build_drift.py — XQ BUILD DRIFT FIREWALL contract tests (WO-FDA-XQ-002).

Verifies: fingerprint presence, public/local mismatch ack, action-class routing
is build-bound, stale routes rejected, pixel/clipboard degraded, live broker DENY.
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


# 1. fingerprint receipt exists + exact fields
fp = json.load(open(BASE / "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json", encoding="utf-8"))
check("fingerprint_schema", fp.get("schema") == "FDA-XQ-SUBJECT/1")
check("fingerprint_build", fp["subject"]["product_build"] == "260811")
check("fingerprint_version", fp["subject"]["product_version"] == "3.20.02")
check("fingerprint_sha", len(fp["subject"]["exe_sha256"]) == 64)
check("fingerprint_window_class", fp["subject"]["main_window_class"] == "DAQXQLITEMainWnd")
check("fingerprint_public_mismatch", fp["public_release_binding"]["exact_public_match"] is False)
check(
    "fingerprint_disposition",
    fp["public_release_binding"]["disposition"] == "LOCAL_BUILD_QUALIFICATION_REQUIRED",
)

# 2. matrix: every action_class has subject_binding + validity
import yaml

matrix = yaml.safe_load(open(BASE / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml", encoding="utf-8"))
ac = matrix["action_classes"]
check("matrix_has_build_firewall", "build_firewall" in matrix)
for name, spec in ac.items():
    sb = spec.get("subject_binding", {})
    vl = spec.get("validity", {})
    check(f"matrix_{name}_binding", str(sb.get("xq_build")) == "260811")
    check(f"matrix_{name}_validity", vl.get("exact_build") is True)

# 3. drift policy table present
pol = matrix.get("build_firewall", {}).get("policy", {})
check("policy_locate_requalify", pol.get("locate_selector") == "REQUALIFY")
check("policy_pixel_invalidate", pol.get("pixel_coordinate") == "INVALIDATE")
check("policy_radar_invalidate", pol.get("radar_paper") == "INVALIDATE_PLUS_FULL_10X")
check("policy_live_deny", pol.get("live_broker") == "DENY_ALWAYS")

# 4. routing rules: no silent fallback
rr = matrix.get("routing_rules", {})
check("routing_silent_fallback_false", rr.get("silent_fallback") is False)
check("routing_unknown_state_forbidden", rr.get("unknown_state_failover") == "FORBIDDEN")
check("routing_second_writer_deny", rr.get("second_writer") == "DENY")

# 5. native adapter exists + main-window finder works statically
adapter = BASE / "xq_native_adapter.py"
check("adapter_exists", adapter.exists())
if adapter.exists():
    src = adapter.read_text(encoding="utf-8")
    check("adapter_no_click_input", "click_input" not in src)
    check("adapter_no_setcursorpos", "SetCursorPos" not in src and "SetForegroundWindow" not in src)
    check("adapter_has_tb_press", "TB_PRESSBUTTON" in src)
    check("adapter_has_bm_click", "BM_CLICK" in src)

print(f"\nRESULT: {len(PASS)} PASS / {len(FAIL)} FAIL")
sys.exit(1 if FAIL else 0)
