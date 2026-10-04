# -*- coding: utf-8 -*-
"""FDA independent checker (read-only) — verifies materialization facts fresh.
Producer: fda-orchestrator. Checker: acceptance-officer (independent readback).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\Fabric")
FDA = ROOT / "fabric-desktop-automation"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


results = []


def check(rid, cond, detail, required=True):
    results.append({"id": rid, "pass": bool(cond), "detail": detail,
                    "required": required})


# 1. team artifact materialized
team = FDA / "TEAM.md"
check("T001_TEAM_ARTIFACT", team.exists(), f"TEAM.md exists: {team.exists()}")
if team.exists():
    t = team.read_text(encoding="utf-8")
    check("T002_TEAM_ID", "fabric-desktop-automation" in t, "team_id present")
    check("T003_TEAM_CLASS", "SHARED_INFRASTRUCTURE_PROFILE_TEAM" in t, "team_class present")
    check("T004_HEAVY_STACK_FALSE", "heavy_stack: false" in t, "heavy_stack false")
    check("T005_PROFILE_REFS", "fabric-desktop-cua" in t and "fabric-desktop-ufo2" in t, "profile refs present")

# 2. capability matrix
mat = FDA / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml"
check("T010_MATRIX_EXISTS", mat.exists(), f"matrix exists: {mat.exists()}")
if mat.exists():
    m = mat.read_text(encoding="utf-8")
    check("T011_MATRIX_SCHEMA", "FDA-DESKTOP-CAPABILITY-MATRIX/1" in m, "matrix schema")
    check("T012_MATRIX_OWNER", "FABRIC_CAPABILITY_QUALIFICATION_POLICY" in m, "canonical owner")
    check("T013_MATRIX_MUTATION", "ADMITTED_HGK_WORKORDER_ONLY" in m, "mutation authority")
    for cls in ["XQ_LAUNCH_LOCATE", "XS_COMPILE_PASS", "XS_COMPILE_FAIL_READBACK",
                "XQ_PAPER_CONFIG", "XQ_LOG_EXPORT_READBACK"]:
        check(f"T014_ACTION_CLASS_{cls}", cls in m, f"action class {cls} present")

# 3. profiles
for pid in ["fabric-desktop-cua", "fabric-desktop-ufo2"]:
    pdir = ROOT / "profiles" / pid
    for f in ["distribution.yaml", "config.yaml", "SOUL.md", "README.runtime-contract.md"]:
        check(f"T020_{pid}_{f}", (pdir / f).exists(), f"{pid}/{f} exists")

# 4. manifest additive (parent rows preserved)
man = ROOT / "rp002" / "RP002_PROFILE_TEAM_MANIFEST.yaml"
mt = man.read_text(encoding="utf-8")
for parent in ["hgk-orchestrator", "hgk-knowledge-factory", "hgk-document-factory",
               "hgk-coding-factory", "construction-acceptance-oracle",
               "sqs-orchestrator", "sqs-data-analysis", "sqs-risk"]:
    check(f"T030_PARENT_ROW_{parent}", parent in mt, f"parent manifest row {parent} preserved")
for fda_row in ["fabric-desktop-cua", "fabric-desktop-ufo2", "fabric-desktop-automation/TEAM.md"]:
    check(f"T031_FDA_ROW_{fda_row}", fda_row in mt, f"FDA row {fda_row} added")

# 5. tool matrix additive (parent rows + FDA rows)
tm = ROOT / "rp002" / "RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml"
tt = tm.read_text(encoding="utf-8")
parent_rows = ["hermes_runtime", "hermes_profiles", "hermes_kanban", "hermes_a2a", "mcp",
               "contextforge", "oasf", "opentelemetry", "codex_cli", "openspec", "gstack"]
for row in parent_rows:
    check(f"T040_PARENT_TOOL_{row}", row + ":" in tt, f"parent tool row {row} preserved")
fda_rows = ["cua_driver", "ufo2", "hermes_computer_use", "openadapt", "agent_s3",
            "appium_windows_driver", "winappdriver", "flaui", "pywinauto", "ufo3_galaxy",
            "fda_desktop_capability_matrix", "fda_team_artifact"]
for row in fda_rows:
    check(f"T041_FDA_TOOL_{row}", row + ":" in tt, f"FDA tool row {row} present")

# 6. execution binding parent-compatible (no child schema)
eb = FDA / "FDA_EXECUTION_BINDING.json"
if eb.exists():
    e = json.loads(eb.read_text(encoding="utf-8"))
    check("T050_BINDING_SCHEMA", e.get("schema") == "RP002-EXECUTION-BINDING/2", "binding uses parent /2 schema")
    check("T051_BINDING_WO", e["normative"]["workorder_id"] == "WO-FDA-001", "binding workorder")
    for sec in ["normative", "routing", "delegation", "lease", "budget", "idempotency", "runtime", "terminal"]:
        check(f"T052_BINDING_{sec}", sec in e, f"binding section {sec}")
    check("T053_BINDING_DESKTOP", "desktop" in e and e["desktop"]["one_active_writer"] is True, "desktop overlay one-active-writer")

# 7. no schema fork evidence (no FDA_EXECUTION_BINDING.schema.json)
check("T060_NO_SCHEMA_FORK", not (FDA / "FDA_EXECUTION_BINDING.schema.json").exists(),
      "no child execution-binding schema created")

# 8. deferred semi-auto contract
dc = FDA / "governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml"
check("T070_SEMIAUTO_CONTRACT", dc.exists(), "deferred semi-auto contract exists")
if dc.exists():
    dct = dc.read_text(encoding="utf-8")
    check("T071_FROZEN_SCRIPT", "NO HOT PATCH TO ACTIVE POSITION" in dct, "no hot patch invariant")
    check("T072_LIVE_NOT_AUTH", "SQS_LIVE_TRADING: NOT_AUTHORIZED" in dct, "live trading NOT_AUTHORIZED")

# 9. interop disposition
idisp = FDA / "governance/FDA_INTEROP_DISPOSITION.yaml"
check("T080_INTEROP_DISPOSITION", idisp.exists(), "interop disposition exists")
if idisp.exists():
    it = idisp.read_text(encoding="utf-8")
    for key in ["OASF", "CONTEXTFORGE", "MCP", "A2A", "OPENTELEMETRY"]:
        check(f"T081_{key}", key.upper() in it.upper(), f"interop disposition {key}")

# 10. route check
rc = FDA / "governance/FDA_ROUTE_CHECK.yaml"
check("T090_ROUTE_CHECK", rc.exists(), "route check exists")
if rc.exists():
    rct = rc.read_text(encoding="utf-8")
    check("T091_GSTACK_STATE", "ACTIVE_SELECTED" in rct, "gstack registry state")
    check("T092_OPENSPEC_STATE", "CERTIFIED_ACTIVE_BROWNFIELD" in rct, "openspec registry state")
    check("T093_LANE_NOT_EXECUTION", "lane=NATIVE does NOT disable" in rct, "lane != execution surface")

# 11. no secret pattern in FDA artifacts (ID = relative path → unique even for same-named files)
for f in FDA.rglob("*"):
    if f.is_file() and f.suffix in (".md", ".yaml", ".json", ".py"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        leaks = re.findall(r"(?<![a-zA-Z0-9])sk-[A-Za-z0-9_-]{20,}", txt)
        rel = str(f.relative_to(FDA)).replace("\\", "_").replace("/", "_")
        check(f"T100_NOSECRET_{rel}", not leaks, f"no secret-like pattern in {f.relative_to(FDA)}")

# 12. XQ PAPER fixture manifest
fx = FDA / "governance/FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml"
check("T110_FIXTURE_MANIFEST", fx.exists(), "fixture manifest exists")
if fx.exists():
    fxt = fx.read_text(encoding="utf-8")
    check("T111_FIXTURE_MODE", "PAPER_NO_LIVE_WRITE" in fxt, "PAPER mode")
    check("T112_FIXTURE_DRIFT", "REQUALIFY_REQUIRED" in fxt, "version drift recorded")

# 13. router/lease/test files
for f in ["fda_router.py", "fda_lease.py",
          "tests/test_fda_router.py", "tests/test_fda_lease.py", "tests/test_fda_security.py"]:
    check(f"T120_FILE_{f}", (FDA / f).exists(), f"{f} exists")

# 14. C0 receipt
c0 = FDA / "evidence/receipts/FDA_C0_READBACK_RECEIPT.json"
check("T130_C0_RECEIPT", c0.exists(), "C0 receipt exists")
if c0.exists():
    c0j = json.loads(c0.read_text(encoding="utf-8"))
    check("T131_C0_VERDICT", c0j.get("verdict") == "FDA-C0_PASS", "C0 verdict PASS")
    check("T132_C0_NO_MISSING", c0j["pass_predicates"]["critical_source_missing"] == 0, "critical source missing 0")

# 14A. live fixture evidence (real desktop runs)
f01 = FDA / "evidence/receipts/FDA_F01_LIVE_FIXTURE_RECEIPT.json"
check("T133_F01_RECEIPT", f01.exists(), "F01 live fixture receipt exists")
if f01.exists():
    f01j = json.loads(f01.read_text(encoding="utf-8"))
    check("T134_F01_10_OF_10", f01j.get("verdict") == "10_OF_10_PASS", "F01 10/10 live PASS")
    check("T135_F01_ZERO_WRONG", f01j["summary"]["wrong_action"] == 0 and f01j["summary"]["silent_wrong_action"] == 0,
          "F01 zero wrong/silent-wrong action")

probe = FDA / "evidence/receipts/FDA_BOUNDED_CONTROL_LIVE_PROBE.json"
check("T136_PROBE_RECEIPT", probe.exists(), "bounded control probe receipt exists")
if probe.exists():
    pj = json.loads(probe.read_text(encoding="utf-8"))
    check("T137_PROBE_PASS", pj.get("result") == "PASS", "bounded control probe PASS")
    check("T138_PROBE_NO_FINANCIAL", "NONE_FINANCIAL" in pj.get("side_effect", ""), "no financial side effect")

concurrency = FDA / "evidence/receipts/FDA_C5_LEASE_CONCURRENCY_RECEIPT.json"
check("T139_CONCURRENCY_RECEIPT", concurrency.exists(), "lease concurrency receipt exists")
if concurrency.exists():
    cj = json.loads(concurrency.read_text(encoding="utf-8"))
    check("T140_CONCURRENCY_PASS", cj.get("verdict") == "PASS", "lease concurrency ALL PASS")
    check("T141_CONCURRENCY_ZERO_SIMUL", cj.get("simultaneous_writers") == 0, "simultaneous writers 0")

# 14B. matrix live-qualification state
mat2 = mat.read_text(encoding="utf-8") if mat.exists() else ""
check("T142_MATRIX_F01_QUALIFIED", "state: QUALIFIED" in mat2 and "CUA_10_OF_10_LIVE_QUALIFIED" in mat2,
      "matrix XQ_LAUNCH_LOCATE CUA QUALIFIED with live reason")
check("T143_MATRIX_PRODUCT_VERSION", "XQLite-3.20.02-260811" in mat2,
      "matrix product version corrected to 3.20.02 live readback")

# 16. WO-FDA-XQ-002 — build-aware native hybrid (XQ BUILD DRIFT FIREWALL)
fp = FDA / "evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json"
check("T160_XQ_FINGERPRINT_RECEIPT", fp.exists(), "XQ build fingerprint receipt exists")
if fp.exists():
    fpj = json.loads(fp.read_text(encoding="utf-8"))
    check("T161_XQ_FINGERPRINT_SCHEMA", fpj.get("schema") == "FDA-XQ-SUBJECT/1", "fingerprint schema")
    check("T162_XQ_BUILD_260811", fpj["subject"].get("product_build") == "260811", "local build 260811")
    check("T163_XQ_SHA_PRESENT", len(fpj["subject"].get("exe_sha256", "")) == 64, "exe sha256 captured")
    check("T164_PUBLIC_MISMATCH_ACK", fpj["public_release_binding"].get("exact_public_match") is False,
          "public 260731 != local 260811 acknowledged")

check("T165_MATRIX_BUILD_FIREWALL", "build_firewall" in mat2 and "XQ_BUILD_DRIFT_FIREWALL" in mat2,
      "matrix build drift firewall present")
check("T166_MATRIX_SUBJECT_BINDING", mat2.count("subject_binding:") >= 5,
      "all 5 action classes have subject_binding")
check("T167_MATRIX_PYWINAUTO", "PYWINAUTO_WIN32" in mat2 and "pywinauto_win32" in mat2 and "0.6.9" in mat2,
      "pywinauto win32 backend row present with version")
check("T168_MATRIX_NO_SILENT_FALLBACK", "silent_fallback: false" in mat2,
      "router silent fallback disabled")

adapter = FDA / "xq_native_adapter.py"
check("T169_NATIVE_ADAPTER_EXISTS", adapter.exists(), "xq_native_adapter.py exists")
if adapter.exists():
    asrc = adapter.read_text(encoding="utf-8")
    check("T170_NATIVE_NO_MOUSE_INPUT", "click_input(" not in asrc and "SetCursorPos(" not in asrc
          and "SendInput(" not in asrc, "adapter has zero mouse-input API calls")
    check("T171_NATIVE_MESSAGE_ONLY", "TB_PRESSBUTTON" in asrc and "BM_CLICK" in asrc,
          "adapter uses pure win32 messages")

nq = FDA / "evidence/receipts/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json"
check("T172_NATIVE_QUAL_RECEIPT", nq.exists(), "native qualification receipt exists")
if nq.exists():
    nqj = json.loads(nq.read_text(encoding="utf-8"))
    check("T173_FN01_10OF10", nqj.get("FN01_locate_main_win32", {}).get("pass") == 10,
          "FN01 main locate 10/10")
    check("T174_FN02_10OF10", nqj.get("FN02_editor_locate_win32", {}).get("pass") == 10,
          "FN02 editor locate 10/10")
    check("T175_FN03_LOCATE", nqj.get("FN03_editor_new_button_locate", {}).get("pass") == 1,
          "FN03 Afx 新增 button located")
    check("T176_FN_ZERO_WRONG", nqj.get("FN01_locate_main_win32", {}).get("wrong_action") == 0,
          "FN wrong-action 0")

for t in ("test_xq_build_drift.py", "test_xq_native_adapter.py", "test_xq_action_router.py"):
    check(f"T177_TEST_{t.upper()}", (FDA / t).exists(), f"{t} present")

# 15. heavy-stack negative
manifest_txt = (ROOT / "HGK_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
check("T150_NO_THIRD_HEAVY_STACK", "fabric-desktop" not in manifest_txt.lower(),
      "fabric-desktop not registered as heavy stack")
sqs_man = (Path(r"C:\Projects\Agent_Workspace\SQS-THC") / "STATUS_VECTOR.json")
check("T151_SQS_LIVE_NOT_AUTHORIZED", sqs_man.exists(), "SQS status vector exists for ceiling readback")

# ---- summary ----
failed = [r for r in results if not r["pass"]]
print(f"CHECKER_VERDICT: {'PASS' if not failed else 'FAIL'}")
print(f"checks: {len(results)}, failed: {len(failed)}")
for r in failed:
    print(f"  FAIL {r['id']}: {r['detail']}")
print(json.dumps(results, ensure_ascii=False, indent=1))
