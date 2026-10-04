# -*- coding: utf-8 -*-
"""Update FDA capability matrix with live qualification results (2026-08-13).
F01 10/10, F06 10/10, F07 PASS, F09 PASS, F10/F11 PASS -> CUA QUALIFIED rows.
"""
import yaml
from pathlib import Path

P = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_DESKTOP_CAPABILITY_MATRIX.yaml")
d = yaml.safe_load(P.read_text(encoding="utf-8"))

VER = "XQLite-3.20.02-260811"
classes = d["action_classes"]

# per-class CUA qualification facts
qual = {
    "XQ_LAUNCH_LOCATE": {
        "state": "QUALIFIED", "digest": "FDA-F01-LIVE-20260813", "rate": "10/10",
        "silent": 0, "wrong": 0, "dfr": 0, "recovery": 0, "ms": 109,
        "structured": "UIA-STRUCTURED", "vision": 0, "human": 0, "restart": 1.0,
        "drift": "CURRENT", "evidence": ["FDA_F01_LIVE_FIXTURE_RECEIPT.json"],
        "routing": {"preferred": "CUA", "alternate": "UFO2", "reason_code": "CUA_10_OF_10_LIVE_QUALIFIED", "hot_swap_allowed": True},
    },
    "XS_COMPILE_PASS": {
        "state": "QUALIFIED", "digest": "FDA-F06-LIVE-20260813", "rate": "10/10",
        "silent": 0, "wrong": 0, "dfr": 0, "recovery": 0, "ms": 6000,
        "structured": "FILE-READBACK", "vision": 0, "human": 0, "restart": 1.0,
        "drift": "CURRENT", "evidence": ["FDA_F06_TEN_RUN_RECEIPT.json", "FDA_F06_CLOSURE_V8_RECEIPT.json"],
        "routing": {"preferred": "CUA", "alternate": "UFO2", "reason_code": "CUA_10_OF_10_FILE_READBACK_COMPILE_PASS", "hot_swap_allowed": True},
    },
    "XS_COMPILE_FAIL_READBACK": {
        "state": "QUALIFIED", "digest": "FDA-F07-LIVE-20260813", "rate": "10/10",
        "silent": 0, "wrong": 0, "dfr": 0, "recovery": 0, "ms": 1000,
        "structured": "FILE-READBACK", "vision": 0, "human": 0, "restart": 1.0,
        "drift": "CURRENT", "evidence": ["FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json"],
        "routing": {"preferred": "CUA", "alternate": "UFO2", "reason_code": "CUA_ERROR_READBACK_VERIFIED", "hot_swap_allowed": True},
    },
    "XQ_PAPER_CONFIG": {
        "state": "QUALIFIED_SURFACE", "digest": "FDA-F09-LIVE-20260813", "rate": "n/a-surface",
        "silent": 0, "wrong": 0, "dfr": 0, "recovery": 0, "ms": 0,
        "structured": "UIA-STRUCTURED", "vision": 0, "human": 0, "restart": 1.0,
        "drift": "CURRENT", "evidence": ["FDA_F09_RADAR_RECEIPT.json"],
        "routing": {"preferred": "CUA", "alternate": "UFO2", "reason_code": "RADAR_SURFACE_OPEN_READBACK_PASS_NO_MUTATION", "hot_swap_allowed": True},
    },
    "XQ_LOG_EXPORT_READBACK": {
        "state": "QUALIFIED", "digest": "FDA-F10F11-LIVE-20260813", "rate": "4/4",
        "silent": 0, "wrong": 0, "dfr": 0, "recovery": 0, "ms": 0,
        "structured": "FILE-READBACK", "vision": 0, "human": 0, "restart": 1.0,
        "drift": "CURRENT", "evidence": ["FDA_F10_F11_READBACK_RECEIPT.json"],
        "routing": {"preferred": "CUA", "alternate": "UFO2", "reason_code": "FILE_LOGGING_READBACK_PASS", "hot_swap_allowed": True},
    },
}

for cls, facts in qual.items():
    row = classes[cls]
    row["application"]["version"] = VER
    row["providers"]["CUA"].update({
        "state": facts["state"], "qualification_subject_digest": facts["digest"],
        "workflow_pass_rate": facts["rate"], "silent_wrong_action": facts["silent"],
        "wrong_action": facts["wrong"], "detected_failure_rate": facts["dfr"],
        "mean_recovery_count": facts["recovery"], "median_completion_time_ms": facts["ms"],
        "structured_control_coverage": facts["structured"], "vision_fallback_rate": facts["vision"],
        "human_intervention_count": facts["human"], "restart_recovery_rate": facts["restart"],
        "version_drift_state": facts["drift"], "evidence_refs": facts["evidence"],
    })
    row["providers"]["UFO2"].update({
        "state": "DEFERRED", "version_drift_state": "REQUALIFY_REQUIRED",
        "qualification_subject_digest": "UFO2-v3.0.8-PIN-20260813",
        "evidence_refs": ["FDA_C3_UFO2_QUALIFICATION_RECEIPT.json"],
    })
    row["routing"] = facts["routing"]

d["subject_digest"] = "FDA-MATRIX-20260813-LIVE-QUALIFICATION"
d["promoted_at"] = None

P.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False, default_flow_style=False), encoding="utf-8")
print("matrix updated OK")
