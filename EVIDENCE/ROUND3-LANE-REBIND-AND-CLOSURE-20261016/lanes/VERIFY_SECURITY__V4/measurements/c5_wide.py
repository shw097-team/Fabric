import os, sys, json
ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
COPY = os.path.join(ROOT, "lanes", "VERIFY_SECURITY", "V4", "work", "subject")
sys.path.insert(0, os.path.join(COPY, "src"))
from hg_kseos import lane_policy as lp

def R(pairs, conflicts):
    return {"sod_invariants": {"pairs": pairs, "declared_conflicts": conflicts}}

# A: distinct_required False + conflict OWNER_ORDERED_IN_FORCE -> exempt
r = R([{"maker": "A", "checker": "B", "distinct_required": False}],
      [{"id": "X1", "pairs": [["A", "B"]], "status": "OWNER_ORDERED_IN_FORCE"}])
print("A_exempt:", lp.sod_declaration_exemption(r, "A", "B"))

# B: distinct_required False but conflict status OPEN -> must NOT exempt
r = R([{"maker": "A", "checker": "B", "distinct_required": False}],
      [{"id": "X1", "pairs": [["A", "B"]], "status": "OPEN"}])
print("B_status_open:", lp.sod_declaration_exemption(r, "A", "B"))

# C: distinct_required True + conflict OWNER_ORDERED_IN_FORCE -> must NOT exempt
r = R([{"maker": "A", "checker": "B", "distinct_required": True}],
      [{"id": "X1", "pairs": [["A", "B"]], "status": "OWNER_ORDERED_IN_FORCE"}])
print("C_distinct_true:", lp.sod_declaration_exemption(r, "A", "B"))

# D: distinct_required False + OWNER_ORDERED but conflict names a DIFFERENT pair -> must NOT exempt
r = R([{"maker": "A", "checker": "B", "distinct_required": False}],
      [{"id": "X1", "pairs": [["A", "C"]], "status": "OWNER_ORDERED_IN_FORCE"}])
print("D_wrong_pair:", lp.sod_declaration_exemption(r, "A", "B"))

# E: no lane -> fail closed
print("E_no_lane:", lp.sod_declaration_exemption(R([], []), None, "B"))

# F: status "owner_ordered_in_force" lower-case -> must NOT exempt (exact match)
r = R([{"maker": "A", "checker": "B", "distinct_required": False}],
      [{"id": "X1", "pairs": [["A", "B"]], "status": "owner_ordered_in_force"}])
print("F_case:", lp.sod_declaration_exemption(r, "A", "B"))

# Live registry: confirm ONLY distinct_required==False pair is EXECUTE/VERIFY
reg = lp.load_registry(os.path.join(COPY, "config", "lane-routing-registry.yaml"))
print("live_pairs:", [(p.get("maker"), p.get("checker"), p.get("distinct_required")) for p in reg["sod_invariants"]["pairs"]])
print("live_conflict_statuses:", [(c.get("id"), c.get("status")) for c in reg["sod_invariants"]["declared_conflicts"]])
