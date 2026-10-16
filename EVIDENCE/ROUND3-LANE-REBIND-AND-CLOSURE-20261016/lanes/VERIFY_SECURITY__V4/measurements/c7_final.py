import os, re

O = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
DOCS = [
    "PLAN.md", "FAR_RULING.md", "FAR_RULING_ADDENDUM_A.md",
    "README.md", "SELF_EVOLUTION.md", "RETROSPECTIVE.md",
    "PROMOTION_RECEIPT.json", "R1_R2_R3_APPLY_RECEIPT.json", "PROJECTION_REPAIR_RECEIPT.json",
    "PATCH1_RECEIPT.json", "role_mandate.json", "admission.json",
    "evidence/ORACLE_R10_RECEIPT.json",
    "evidence/EVIDENCE_REPO_MERGE_AND_BRANCH_CLEANUP.md",
    "evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.md",
    "lanes/EXECUTE/R1/dispatch.json",
    "lanes/VERIFY_SECURITY/V4/invocation.json",
]
for d in DOCS:
    p = os.path.join(O, d.replace("/", os.sep))
    if not os.path.exists(p):
        print(f"MISSING {d}"); continue
    t = open(p, encoding="utf-8", errors="ignore").read()
    has_token = "canonical_acceptance" in t
    print(f"{d:60s} CANDIDATE_ONLY={'CANDIDATE_ONLY' in t}  "
          f"key_canonical_acceptance={has_token} NOT_PERFORMED={'NOT_PERFORMED' in t}  "
          f"merge_owner={bool(re.search(r'merge.{0,40}owner|owner.{0,40}merge',t,re.I))} "
          f"branchdel_owner={bool(re.search(r'branch.{0,50}(owner|delete)',t,re.I))}")
