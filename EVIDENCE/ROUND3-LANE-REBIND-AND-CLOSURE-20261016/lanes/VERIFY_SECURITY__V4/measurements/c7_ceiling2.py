import os, re

O = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
DOCS = [
    "admission.json", "role_mandate.json", "KANBAN_SWARM_GRAPH.json",
    "PATCH1_RECEIPT.json", "R1_R2_R3_APPLY_RECEIPT.json", "PROJECTION_REPAIR_RECEIPT.json",
    "PROMOTION_RECEIPT.json",
    "evidence/EVIDENCE_LANE_AVAILABILITY.json",
    "evidence/EVIDENCE_REPO_MERGE_AND_BRANCH_CLEANUP.json",
    "evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json",
    "evidence/EVIDENCE_CANDIDATE_LANDING_SURFACE.json",
    "evidence/GUARD_VERIFY_vs_EXECUTE.json", "evidence/GUARD_VERIFY_vs_PLAN.json",
    "lanes/VERIFY_SECURITY/V4/invocation.json",
]
for d in DOCS:
    p = os.path.join(O, d.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"MISSING {d}"); continue
    t = open(p, encoding="utf-8", errors="ignore").read()
    flags = {k: v for k, v in {
        "CANDIDATE_ONLY": "CANDIDATE_ONLY" in t,
        "canonical_acceptance_mention": ("canonical_acceptance" in t or "canonical acceptance" in t.lower()),
        "NOT_PERFORMED": "NOT_PERFORMED" in t,
        "merge=owner": bool(re.search(r"merge.{0,40}owner|owner.{0,40}merge", t, re.I)),
        "branch_delete=owner": bool(re.search(r"branch.{0,50}(owner|delete)|delete.{0,50}branch", t, re.I)),
        "self_accept": bool(re.search(r"ACCEPTED BY THE (AGENT|ROUND|ORCHESTRATOR)|SELF[- ]ACCEPTED", t, re.I)),
        "claims_released": bool(re.search(r"\breleased\b", t, re.I)),
        "claims_deployed": bool(re.search(r"\bdeployed\b", t, re.I)),
    }.items() if v}
    print(f"--- {d}: {flags}")
