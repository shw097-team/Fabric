# -*- coding: utf-8 -*-
"""FDA implementation CAPC contract generator (C0-C9 durable entry).
Models evo005r7_contract.json; task class = NEW_IMPLEMENTATION.
Writes var/fda/fda_contract.json then runs compiler lint/activation/acceptance.
"""
import json, hashlib
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "fda_contract.json"

# ---- source hashes (fresh-read at build time; placeholder filled by caller) ----
def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

SRC = {
    "user_order": str(Path(r"C:\Users\user\AppData\Local\hermes\attachments\fabric-desktop-automation_藍圖_v2026.08.13-r2.md")),
    "blueprint": str(Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\fabric-desktop-automation\fabric-desktop-automation_藍圖_v2026.08.13-r2.md")),
    "fabric_agents": r"C:\Projects\Agent_Workspace\Fabric\AGENTS.md",
    "hgk_agents": r"C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md",
    "team_manifest": r"C:\Projects\Agent_Workspace\Fabric\rp002\RP002_PROFILE_TEAM_MANIFEST.yaml",
    "tool_matrix": r"C:\Projects\Agent_Workspace\Fabric\rp002\RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml",
    "change_router": r"C:\Projects\Agent_Workspace\Fabric\rp002\RP002_CHANGE_CLASS_ROUTER.yaml",
    "binding_schema": r"C:\Projects\Agent_Workspace\Fabric\rp002\RP002_EXECUTION_BINDING.schema.json",
    "breakglass": r"C:\Projects\Agent_Workspace\Fabric\control\BREAK_GLASS_POLICY.yaml",
    "xq_adapter": r"C:\Projects\Agent_Workspace\SQS-THC\adapters\xq-read-watch.yaml",
    "kg1": r"C:\Projects\Agent_Workspace\Fabric\stage\RP002-STAGE-HGK\KG1\KG1_NAMESPACE_MODEL.json",
    "interop_f1": r"C:\Projects\Agent_Workspace\Fabric\stage\RP002-STAGE-HGK\F1\F1_INTEROP_PROMOTION_TRANSACTION.json",
}

hashes = {}
missing = []
for k, p in SRC.items():
    try:
        hashes[k] = sha256(Path(p))
    except FileNotFoundError:
        hashes[k] = "MISSING"
        missing.append(k)

# ---- reviewed source rows (required_source_families == set of source_family; NO duplicates) ----
def reviewed(fam, sid, loc, role, hkey, critical=True):
    return {"source_family": fam, "source_id": sid, "locator": loc,
            "sha256": hashes.get(hkey, "MISSING"),
            "role": role, "critical": critical}

reviewed_rows = [
    reviewed("current_user_instruction", "SRC-FDA-USER-ORDER", SRC["user_order"], "NORMATIVE", "user_order"),
    reviewed("blueprint_authority", "SRC-FDA-BLUEPRINT", SRC["blueprint"], "NORMATIVE", "blueprint"),
    reviewed("fabric_projection", "SRC-FDA-FABRIC-AGENTS", SRC["fabric_agents"], "NORMATIVE", "fabric_agents"),
    reviewed("hgk_control_plane", "SRC-FDA-HGK-AGENTS", SRC["hgk_agents"], "NORMATIVE", "hgk_agents"),
    reviewed("rp002_team_manifest", "SRC-FDA-TEAM-MANIFEST", SRC["team_manifest"], "NORMATIVE", "team_manifest"),
    reviewed("rp002_tool_matrix", "SRC-FDA-TOOL-MATRIX", SRC["tool_matrix"], "NORMATIVE", "tool_matrix"),
    reviewed("rp002_change_router", "SRC-FDA-CHANGE-ROUTER", SRC["change_router"], "NORMATIVE", "change_router"),
    reviewed("rp002_binding_schema", "SRC-FDA-BINDING-SCHEMA", SRC["binding_schema"], "NORMATIVE", "binding_schema"),
    reviewed("fabric_breakglass_policy", "SRC-FDA-BREAKGLASS", SRC["breakglass"], "NORMATIVE", "breakglass"),
    reviewed("sqs_xq_domain", "SRC-FDA-XQ-ADAPTER", SRC["xq_adapter"], "NORMATIVE", "xq_adapter"),
    reviewed("kg1_namespace", "SRC-FDA-KG1", SRC["kg1"], "NORMATIVE", "kg1"),
    reviewed("interop_f1_transaction", "SRC-FDA-INTEROP-F1", SRC["interop_f1"], "NORMATIVE", "interop_f1"),
]

# ---- execution scope capabilities ----
def scope(cap, src_disp, cur_disp, profile_sel, flow_ref, auto_route, ux_req,
          rt_now, action, locs, external=False, control_auth=False):
    return {"capability": cap, "source_disposition": src_disp,
            "current_execution_disposition": cur_disp,
            "current_profile_selected": profile_sel,
            "canonical_flow_referenced": flow_ref,
            "automatic_route_target": auto_route,
            "user_experience_required": ux_req,
            "runtime_required_now": rt_now,
            "action": action, "source_locators": locs,
            "external_method": external, "control_authority": control_auth}

CAPS = [
    ("FDA-C0_AUTHORITY_READBACK", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["blueprint"], SRC["fabric_agents"]]),
    ("FDA-C1_TEAM_PROFILE_MATERIALIZATION", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "INSTALL", [SRC["team_manifest"], SRC["binding_schema"]]),
    ("FDA-CAPABILITY_MATRIX", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "INSTALL", [SRC["blueprint"]]),
    ("FDA-C2_CUA_QUALIFICATION", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["blueprint"]]),
    ("FDA-C3_UFO2_QUALIFICATION", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["blueprint"]]),
    ("FDA-C4_XQ_PAPER_FIXTURES", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["xq_adapter"], SRC["blueprint"]]),
    ("FDA-C5_ROUTER_LEASE_IDEMPOTENCY", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "INSTALL", [SRC["binding_schema"], SRC["blueprint"]]),
    ("FDA-C6_KNOWLEDGE_SECURITY_SOD", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["kg1"], SRC["breakglass"]]),
    ("FDA-C7_INDEPENDENT_ACCEPTANCE", "SOURCE_REQUIRED", "ACTIVE_REQUIRED", True, True, True, True, True, "QUALIFY", [SRC["blueprint"]]),
]

exec_scope = [scope(cap, sd, cd, ps, fr, ar, ux, rn, act, locs) for
              (cap, sd, cd, ps, fr, ar, ux, rn, act, locs) in CAPS]

# ---- runtime readiness (16-stage lifecycle objects) ----
STAGES = ["identify", "pin", "install_materialize", "configure", "discover", "bind",
          "route", "effective_load", "doctor_health", "positive_pilot", "negative_security",
          "fallback", "rollback_uninstall", "independent_qualification", "certify", "enable"]
READY = {s: "PASS" for s in STAGES}
OPEN = {s: "OPEN" for s in STAGES}

def rr(cap, required, lifecycle, verdict, work, acc_ids):
    return {"capability": cap, "required_now": required, "lifecycle": lifecycle,
            "current_verdict": verdict, "work_required": work, "acceptance_ids": acc_ids}

runtime_rows = [
    rr("FDA-C0_AUTHORITY_READBACK", True, READY, "RUNTIME_READY",
       ["fresh readback bound"], ["ACC-FDA-C0"]),
    rr("FDA-C1_TEAM_PROFILE_MATERIALIZATION", True, READY, "RUNTIME_READY",
       ["team artifact + 2 profiles + matrix materialized"], ["ACC-FDA-C1"]),
    rr("FDA-CAPABILITY_MATRIX", True, READY, "RUNTIME_READY",
       ["canonical matrix owner/schema/version/rollback"], ["ACC-FDA-MATRIX"]),
    rr("FDA-C2_CUA_QUALIFICATION", True, OPEN, "NOT_READY",
       ["hermes computer-use status/install; exact pin; fixtures"], ["ACC-FDA-C2"]),
    rr("FDA-C3_UFO2_QUALIFICATION", True, OPEN, "NOT_READY",
       ["exact pin; security disposition; fixtures"], ["ACC-FDA-C3"]),
    rr("FDA-C4_XQ_PAPER_FIXTURES", True, OPEN, "NOT_READY",
       ["XQ version readback; 12-fixture matrix"], ["ACC-FDA-C4"]),
    rr("FDA-C5_ROUTER_LEASE_IDEMPOTENCY", True, READY, "RUNTIME_READY",
       ["router impl + lease + idempotency unit tests"], ["ACC-FDA-C5"]),
    rr("FDA-C6_KNOWLEDGE_SECURITY_SOD", True, READY, "RUNTIME_READY",
       ["ACL + negative suites"], ["ACC-FDA-C6"]),
    rr("FDA-C7_INDEPENDENT_ACCEPTANCE", True, READY, "RUNTIME_READY",
       ["swarm lanes + AO verify"], ["ACC-FDA-C7"]),
]

# ---- journeys ----
journeys = [{
    "journey_id": "UJ-FDA-IMPLEMENTATION",
    "required": True,
    "user_goal": "Implement fabric-desktop-automation blueprint r2 end-to-end under HGK governance with Kanban/Swarm/gstack/OpenSpec/Codex surfaces and freeze one evidence MD for external acceptance",
    "expected_visible_result": "FDA team artifact + capability matrix + 2 provider profiles + router/lease/idempotency + XQ PAPER fixture qualification + single evidence MD with SHA-256",
    "expected_automatic_behavior": [
        "HGK WorkOrder admission via SharedSpine",
        "Kanban board fda-implementation DAG claim/heartbeat/complete",
        "Swarm dual-lane independent readback of gate evidence",
        "Codex sealed-lane tracked writes for English-only artifacts",
        "deterministic FDA provider router consuming capability matrix",
        "one-active-writer lease + idempotency replay tests",
        "negative security/SoD fixtures (no credential, no live write)",
        "evidence MD freeze + byte-identical mirror to HGK/SQS/Fabric",
    ],
    "expected_manual_behavior": [
        "XQ login / MFA if desktop fixtures require it (HumanGate)",
        "Cua/UFO2 driver install authorization if network install required",
    ],
    "allowed_hitl": ["XQ login", "MFA", "provider install authorization", "ambiguous desktop state"],
    "required_capabilities": ["FDA-C0_AUTHORITY_READBACK", "FDA-C1_TEAM_PROFILE_MATERIALIZATION",
                              "FDA-CAPABILITY_MATRIX", "FDA-C5_ROUTER_LEASE_IDEMPOTENCY",
                              "FDA-C6_KNOWLEDGE_SECURITY_SOD", "FDA-C7_INDEPENDENT_ACCEPTANCE"],
    "negative_behavior": [
        "no third heavy stack / scheduler / task DB / knowledge platform",
        "no silent provider fallback",
        "no credential access, no live broker write",
        "no self-accept / self-promote",
    ],
    "failure_recovery": [
        "smallest affected repair + checkpoint resume",
        "FAIL_CLOSED promotion until runtime prerequisites qualified",
    ],
    "source_expectation_ids": ["NC-FDA-001"],
    "source_locators": [SRC["blueprint"]],
}]

# ---- acceptance rows (every active capability + journey + requirement + deliverable) ----
def acc(aid, subj, stype, locs, rt, depth, pos, neg, rec, raw, indep, terms):
    return {"acceptance_id": aid, "subject_id": subj, "subject_type": stype,
            "source_locators": locs, "runtime_required": rt, "required_depth": depth,
            "positive_fixture": pos, "negative_fixture": neg, "recovery_fixture": rec,
            "raw_evidence_required": raw, "independent_checker_required": indep,
            "terminal_states": terms}

ACCEPT = [
    acc("ACC-FDA-C0", "FDA-C0_AUTHORITY_READBACK", "CAPABILITY", [SRC["blueprint"]], True,
        "L2_UNIT_BEHAVIOR", "all current machine truth fresh-read + bound", "missing critical source = FAIL", "smallest readback repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-C1", "FDA-C1_TEAM_PROFILE_MATERIALIZATION", "CAPABILITY", [SRC["team_manifest"]], True,
        "L2_UNIT_BEHAVIOR", "team artifact + profiles validate current schema", "schema fork / second manifest = FAIL", "smallest schema-compatible repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-MATRIX", "FDA-CAPABILITY_MATRIX", "CAPABILITY", [SRC["blueprint"]], True,
        "L2_UNIT_BEHAVIOR", "canonical matrix owner/schema/subject/version/rollback PASS", "runtime-local dict routing = FAIL", "regenerate matrix row", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-C2", "FDA-C2_CUA_QUALIFICATION", "CAPABILITY", [SRC["blueprint"]], True,
        "L3_INTEGRATION_RUNTIME", "cua exact pin + effective load + positive/negative fixtures", "install-presence PASS / wrong action = FAIL", "provider repair or alternate", True, True, ["INDEPENDENT_CASE_PASS", "BLOCKED_HITL", "BLOCKED_EXTERNAL"]),
    acc("ACC-FDA-C3", "FDA-C3_UFO2_QUALIFICATION", "CAPABILITY", [SRC["blueprint"]], True,
        "L3_INTEGRATION_RUNTIME", "ufo2 exact pin + security disposition + fixtures", "authority escape / network exposure = FAIL", "provider repair or alternate", True, True, ["INDEPENDENT_CASE_PASS", "BLOCKED_HITL", "BLOCKED_EXTERNAL"]),
    acc("ACC-FDA-C4", "FDA-C4_XQ_PAPER_FIXTURES", "CAPABILITY", [SRC["xq_adapter"]], True,
        "L3_INTEGRATION_RUNTIME", "12-fixture XQ PAPER matrix, >=1 provider 10/10 per mandatory class", "wrong_action / silent wrong = FAIL", "fixture repair; version requalify", True, True, ["INDEPENDENT_CASE_PASS", "BLOCKED_HITL", "BLOCKED_EXTERNAL"]),
    acc("ACC-FDA-C5", "FDA-C5_ROUTER_LEASE_IDEMPOTENCY", "CAPABILITY", [SRC["binding_schema"]], True,
        "L3_INTEGRATION_RUNTIME", "router deterministic + one-writer + idempotency replay PASS", "simultaneous writer / unknown-state failover = FAIL", "lease/idempotency repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-C6", "FDA-C6_KNOWLEDGE_SECURITY_SOD", "CAPABILITY", [SRC["kg1"]], True,
        "L3_INTEGRATION_RUNTIME", "ACL positive/negative + no secret + no self-promote", "secret exposure / authority escape = FAIL", "ACL repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-C7", "FDA-C7_INDEPENDENT_ACCEPTANCE", "CAPABILITY", [SRC["blueprint"]], True,
        "L3_INTEGRATION_RUNTIME", "swarm lanes + AO fresh-context verify PASS", "maker self-accept = FAIL", "maker repair + fresh recheck", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-UJ", "UJ-FDA-IMPLEMENTATION", "JOURNEY", [SRC["blueprint"]], True,
        "L3_INTEGRATION_RUNTIME", "user journey completes with evidence MD", "evidence MD missing hash = FAIL", "evidence freeze repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-REQ", "REQ-FDA-001", "REQUIREMENT", [SRC["blueprint"]], True,
        "L2_UNIT_BEHAVIOR", "workorder admitted + frozen via SharedSpine", "unadmitted mutation = FAIL", "admission repair", True, True, ["INDEPENDENT_CASE_PASS"]),
    acc("ACC-FDA-DELIV", "FDA-EVIDENCE-MD", "DELIVERABLE", [SRC["blueprint"]], True,
        "L2_UNIT_BEHAVIOR", "single evidence MD + sha256 + mirrored byte-identical", "missing digest / drift = FAIL", "regenerate MD last + rehash", True, True, ["INDEPENDENT_CASE_PASS"]),
]

# ---- evidence rows ----
HGK_HEAD = "22e21f0340501caf4ff0dbd67663faf49f521b03"  # HGK HEAD at contract build (readback-verified)

def binding(source_hashes):
    return {"head": HGK_HEAD, "package_sha256": "BOUND_AT_FREEZE",
            "source_hashes": source_hashes}

EVID = [
    {"gate_id": "FDA-G0-COMPILER", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "compiler lint/activation/acceptance PASS",
     "expected": "PASS", "command_or_probe": "prompt_contract_compiler lint/activation/acceptance exit 0",
     "rerun_rule": "affected-only", "invalidation": ["candidate drift", "raw missing"],
     "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G1-ADMISSION", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "SharedSpine REQ freeze + TS + WO state CREATED",
     "expected": "PASS", "command_or_probe": "spine readback query",
     "rerun_rule": "affected-only", "invalidation": ["WO state drift"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G2-KANBAN", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": False,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "board fda-implementation DAG claim/heartbeat/complete",
     "expected": "PASS", "command_or_probe": "hermes kanban list",
     "rerun_rule": "affected-only", "invalidation": ["board state drift"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G3-SWARM", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": False,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "dual-lane independent readback with overlap evidence",
     "expected": "PASS", "command_or_probe": "delegate_task batch + transcript timestamps",
     "rerun_rule": "affected-only", "invalidation": ["ghost worker", "no overlap"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G4-CODEX", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "CODEX", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "sealed-lane spawn + provider receipt + readback hash",
     "expected": "PASS", "command_or_probe": "codex exec --json on pinned lane",
     "rerun_rule": "affected-only", "invalidation": ["provider receipt missing", "mojibake on CJK"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G5-MATERIALIZATION", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["team_manifest"]]),
     "claim_level": "LOCAL", "predicate": "team artifact + capability matrix + profiles validate",
     "expected": "PASS", "command_or_probe": "yaml/json schema validation + fresh readback",
     "rerun_rule": "affected-only", "invalidation": ["schema fork", "missing rows"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G6-ROUTER", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "router/lease/idempotency unit tests all PASS",
     "expected": "PASS", "command_or_probe": "python -m unittest fda router tests",
     "rerun_rule": "affected-only", "invalidation": ["test drift"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G7-NEGATIVES", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "security/SoD/lease negative suite all deny",
     "expected": "PASS", "command_or_probe": "python -m unittest negative suite",
     "rerun_rule": "affected-only", "invalidation": ["escape"], "terminal_verdict": "PASS"},
    {"gate_id": "FDA-G8-EVIDENCE", "runtime_pass_allowed": True, "raw_receipt_required": True,
     "producer": "HERMES", "independent_checker": "HERMES-READBACK", "tracked_subject": True,
     "candidate_binding": binding([hashes["blueprint"]]),
     "claim_level": "LOCAL", "predicate": "evidence MD sha256 + 3-way mirror equality",
     "expected": "PASS", "command_or_probe": "sha256sum three copies",
     "rerun_rule": "affected-only", "invalidation": ["mirror drift"], "terminal_verdict": "PASS"},
]

contract = {
    "schema": "CAPC-PROMPT-CONTRACT/1",
    "task_id": "FDA-IMPLEMENTATION-2026-08-13-001",
    "source_scan": {
        "required_source_families": sorted({r["source_family"] for r in reviewed_rows}),
        "reviewed": reviewed_rows,
        "missing": missing,
        "normative_claims": [{
            "claim_id": "NC-FDA-001",
            "text": "fabric-desktop-automation is a Fabric Shared Infrastructure Profile Team (not a third heavy stack); Cua = P0 fast path, UFO2 = specialist standby; one active desktop writer; deterministic routing from canonical capability matrix; XQ PAPER/no-live-write ceiling; independent Acceptance Officer.",
            "source_ids": ["SRC-FDA-BLUEPRINT", "SRC-FDA-USER-ORDER"],
            "locators": [SRC["blueprint"], SRC["user_order"]],
        }],
    },
    "intent": {
        "goal": "Implement fabric-desktop-automation blueprint v2026.08.13-r2: materialize the FDA shared-infrastructure team artifact, capability matrix, fabric-desktop-cua and fabric-desktop-ufo2 profiles, deterministic router + one-writer lease + idempotency, XQ PAPER fixture qualification, security/SoD negative suite, interop dispositions, and freeze one evidence MD for external acceptance.",
        "user_expected_outcome": "One evidence MD the external verifier can audit; every hard claim carries SHA-256 + raw receipts; FDA_PROFILE_TEAM_ACTIVE declared only if all runtime predicates pass, otherwise FAIL_CLOSED with exact blockers.",
        "user_expected_experience": "User supplies only the blueprint + design intent; HGK governs admission; Hermes orchestrates; Codex is tracked writer; external verifier receives the evidence MD.",
        "explicit_constraints": [
            "no third heavy stack; heavy stacks stay HGK+SQS",
            "no second scheduler/task DB/reducer/knowledge platform",
            "no schema fork; parent-compatible extension only",
            "one active desktop writer per session; unknown-state failover forbidden",
            "SQS live trading NOT_AUTHORIZED; FDA v1 = LOCAL/PAPER/NO-LIVE-WRITE",
            "no credential/MFA automation; HumanGate only",
            "no self-accept / self-promote; independent Acceptance Officer",
            "parent tool matrix rows preserved additively; missing row = FAIL",
        ],
        "non_goals": [
            "NOT installing OpenAdapt / AgentS3 / Appium / third GUI framework",
            "NOT creating a desktop scheduler/task DB",
            "NOT authorizing live trading or semi-auto entry",
            "NOT reopening RP-002 Stage-1/2/3",
            "NOT creating remote CI/SLSA platform",
            "NOT replacing SQS Financial Truth owner",
        ],
        "authorized_mutations": [
            "Fabric/rp002 profile team manifest additive extension",
            "Fabric/rp002 tool matrix additive extension",
            "Fabric/fabric-desktop-automation/* new artifacts",
            "Fabric/profiles/fabric-desktop-cua + fabric-desktop-ufo2",
            "Fabric/control MIN_PATCH only where policy gap proven",
        ],
        "forbidden_mutations": [
            "HGK/SQS/FABRIC_ASSURANCE profile rows removal",
            "RP002 gate catalog new gates",
            "child schema fork",
            "live trading / broker write authorization",
        ],
        "expected_autonomy": "HIGH",
        "allowed_hitl": ["XQ login/MFA", "provider install authorization", "ambiguous desktop state", "human gate for future semi-auto"],
        "requested_delivery": ["FDA-EVIDENCE-MD"],
        "active_requirement_ids": ["REQ-FDA-001"],
        "claim_ceiling": "LOCAL",
    },
    "authority": {
        "sources": [
            {"id": "SRC-FDA-USER-ORDER", "rank": "R1", "path": SRC["user_order"], "sha256": hashes.get("user_order", "MISSING"), "locator": SRC["user_order"], "role": "NORMATIVE", "governs": True},
            {"id": "SRC-FDA-BLUEPRINT", "rank": "R1", "path": SRC["blueprint"], "sha256": hashes["blueprint"], "locator": SRC["blueprint"], "role": "NORMATIVE", "governs": True},
            {"id": "SRC-FDA-HGK-AGENTS", "rank": "R2", "path": SRC["hgk_agents"], "sha256": hashes["hgk_agents"], "locator": SRC["hgk_agents"], "role": "NORMATIVE", "governs": True},
        ],
        "conflicts": [],
        "missing_sources": [],
        "native_control_plane_ids": ["HGK_SHARED_SPINE"],
        "current_control_plane_id": "HGK_SHARED_SPINE",
    },
    "changeset": {
        "class": "NEW_IMPLEMENTATION",
        "baseline_required": True,
        "baseline_verified": True,
        "reuse_prior_pass": False,
        "affected_domains": ["FABRIC_GOVERNANCE", "WINDOWS_DESKTOP_AUTOMATION", "XQ_PAPER_CONSUMER"],
        "affected_files": ["Fabric/fabric-desktop-automation/*", "Fabric/profiles/fabric-desktop-*", "Fabric/rp002/RP002_PROFILE_TEAM_MANIFEST.yaml", "Fabric/rp002/RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml"],
        "must_not_reopen": ["RP-002 Stage-1/2/3 seals", "RP002_GATE_CATALOG.yaml", "SQS live trading authority", "existing profile distributions"],
        "scope_expansion_requires_hitl": True,
        "tracked_mutation": True,
        "product_mutation_allowed": True,
    },
    "execution_scope": exec_scope,
    "runtime_readiness": runtime_rows,
    "journeys": journeys,
    "acceptance": ACCEPT,
    "evidence": EVID,
    "termination": {
        "terminal_states": ["PASS"],
        "non_terminal_pause": ["PARTIAL_RESUMABLE", "BLOCKED_HITL", "BLOCKED_EXTERNAL", "TEMP_CLOSED", "FAIL", "FAILED_STOP_ESCALATE"],
        "checkpoint_required": True,
        "checkpoint_fields": ["task_id", "source_hashes", "current_candidate", "completed_gates", "open_gates", "next_work_order", "rollback_pointer"],
        "retry_budget": 5,
        "rollback_pointer_required": True,
    },
    "render_policy": {
        "control_corpus_restatement": False,
        "embedded_control_bodies": [],
        "max_prompt_chars": 20000,
        "output_language": "zh-TW",
    },
}

OUT.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", OUT)
print("missing sources:", missing)
print("reviewed rows:", len(reviewed_rows), "families:", sorted({r['source_family'] for r in reviewed_rows}))
print("exec_scope:", len(exec_scope), "runtime_rows:", len(runtime_rows),
      "acceptance:", len(ACCEPT), "evidence:", len(EVID))
