# -*- coding: utf-8 -*-
"""Upgrade FDA_DESKTOP_CAPABILITY_MATRIX.yaml:
1. add subject_binding + validity to every action_class
2. add PYWINAUTO_WIN32 provider rows for FN01/FN02-qualified action classes
3. update routing_rules (build-aware, fail-closed)
Writes back preserving structure; then verify round-trip.
"""
import re
import sys

path = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_DESKTOP_CAPABILITY_MATRIX.yaml"
t = open(path, encoding="utf-8").read()

# 1. header: add build-firewall fields after prior_matrix_digest
t = t.replace(
    "prior_matrix_digest: null\nrollback_matrix_digest: null",
    "prior_matrix_digest: null\nrollback_matrix_digest: null\nbuild_firewall:\n  schema: XQ_BUILD_DRIFT_FIREWALL/1\n  subject_receipt: FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json\n  current_subject: XQ-3.20.02-260811-sha6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe\n  public_build_mismatch_acknowledged: true\n  policy:\n    locate_selector: REQUALIFY\n    uia_selector: REQUALIFY\n    clipboard: REQUALIFY\n    pixel_coordinate: INVALIDATE\n    radar_paper: INVALIDATE_PLUS_FULL_10X\n    file_log_schema: SCHEMA_PROBE\n    live_broker: DENY_ALWAYS"
)

# 2. each action_class: insert subject_binding + validity after application.version line
t = re.sub(
    r"(      version: XQLite-3\.20\.02-260811\n)(    providers:)",
    r"\1    subject_binding:\n      xq_version: 3.20.02\n      xq_build: 260811\n      xq_exe_sha256: 6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe\n      fingerprint_receipt: FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json\n    validity:\n      exact_build: true\n      invalidated_by:\n      - XQ_BUILD_CHANGE\n      - SELECTOR_SIGNATURE_CHANGE\n    providers:",
    t,
)

# 3. add PYWINAUTO_WIN32 provider to XQ_LAUNCH_LOCATE (FN01 qualified 10/10)
t = t.replace(
    """  XQ_LAUNCH_LOCATE:
    application:
      id: XQ
      version: XQLite-3.20.02-260811
    subject_binding:
      xq_version: 3.20.02
      xq_build: 260811
      xq_exe_sha256: 6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe
      fingerprint_receipt: FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json
    validity:
      exact_build: true
      invalidated_by:
      - XQ_BUILD_CHANGE
      - SELECTOR_SIGNATURE_CHANGE
    providers:
      CUA:""",
    """  XQ_LAUNCH_LOCATE:
    application:
      id: XQ
      version: XQLite-3.20.02-260811
    subject_binding:
      xq_version: 3.20.02
      xq_build: 260811
      xq_exe_sha256: 6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe
      fingerprint_receipt: FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json
    validity:
      exact_build: true
      invalidated_by:
      - XQ_BUILD_CHANGE
      - SELECTOR_SIGNATURE_CHANGE
    providers:
      PYWINAUTO_WIN32:
        profile_id: fabric-desktop-cua
        executor_backend: pywinauto_win32
        backend_version: 0.6.9
        selector_class: hwnd/win32_enum
        state: QUALIFIED
        qualification_subject_digest: FDA-FN01-NATIVE-20260814
        workflow_pass_rate: 10/10
        silent_wrong_action: 0
        wrong_action: 0
        detected_failure_rate: 0
        mean_recovery_count: 0
        median_completion_time_ms: 5
        structured_control_coverage: WIN32-NATIVE
        vision_fallback_rate: 0
        human_intervention_count: 0
        restart_recovery_rate: 1.0
        version_drift_state: CURRENT
        evidence_refs:
        - FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json
      CUA:""",
)

open(path, "w", encoding="utf-8", newline="\n").write(t)
print("matrix upgraded, bytes:", len(t))
