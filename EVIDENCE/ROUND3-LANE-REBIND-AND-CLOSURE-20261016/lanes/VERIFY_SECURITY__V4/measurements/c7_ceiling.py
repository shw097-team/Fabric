import os, re, json

O = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
DOCS = [
    "PROMOTION_RECEIPT.json", "PLAN.md", "FAR_RULING.md", "FAR_RULING_ADDENDUM_A.md",
    "PATCH1_RECEIPT.json", "R1_R2_R3_APPLY_RECEIPT.json", "PROJECTION_REPAIR_RECEIPT.json",
    "README.md", "SELF_EVOLUTION.md", "RETROSPECTIVE.md",
    "lanes/EXECUTE/R1/dispatch.json", "lanes/VERIFY_SECURITY/V4/dispatch.json",
    "evidence/ORACLE_R10_RECEIPT.json",
]
for d in DOCS:
    p = os.path.join(O, d.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"MISSING {d}")
        continue
    t = open(p, encoding="utf-8", errors="ignore").read()
    flags = {
        "CANDIDATE_ONLY": "CANDIDATE_ONLY" in t,
        "candidate-only(lower)": "candidate-only" in t.lower(),
        "mentions_merge_owner": bool(re.search(r"merge.{0,40}owner|owner.{0,40}merge", t, re.I)),
        "mentions_branch_delete_owner": bool(re.search(r"branch.{0,40}(owner|delete)|delete.{0,40}(owner|branch)", t, re.I)),
        "canonical_acceptance_mentioned": "canonical_acceptance" in t or "canonical acceptance" in t.lower(),
        "NOT_PERFORMED": "NOT_PERFORMED" in t,
        "self_acceptance_claim": bool(re.search(r"ACCEPTED BY THE (AGENT|ROUND|ORCHESTRATOR)|SELF[- ]ACCEPTED", t, re.I)),
        "advisory": "advisory" in t.lower(),
        "claims_released": bool(re.search(r"\breleased\b", t, re.I)),
        "claims_deployed": bool(re.search(r"\bdeployed\b", t, re.I)),
    }
    print(f"--- {d}")
    print("   ", {k: v for k, v in flags.items() if v})
