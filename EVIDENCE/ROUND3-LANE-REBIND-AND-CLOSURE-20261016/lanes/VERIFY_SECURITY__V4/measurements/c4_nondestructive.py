import json, os, subprocess, sys
COPY = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject"
cfg = os.path.join(COPY, "config")
sys.path.insert(0, os.path.join(COPY, "src"))
from hg_kseos import lane_policy as lp

live = lp.load_registry(os.path.join(cfg, "lane-routing-registry.yaml"))
pre = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\preimages\lane-routing-registry.yaml.pre-38f0436b9bde"
bak = lp.load_registry(pre)

live_conf = [c["id"] for c in live["sod_invariants"]["declared_conflicts"]]
bak_conf = [c["id"] for c in bak["sod_invariants"]["declared_conflicts"]]
print("live_conflict_ids:", live_conf)
print("pre_edit_conflict_ids:", bak_conf)
print("removed_ids (native to pre-edit, absent live):", [i for i in bak_conf if i not in live_conf])
print("added_ids:", [i for i in live_conf if i not in bak_conf])
print("live_statuses:", {c["id"]: c["status"] for c in live["sod_invariants"]["declared_conflicts"]})
print("live_pairs:", [(p["maker"], p["checker"], p["distinct_required"]) for p in live["sod_invariants"]["pairs"]])
print("live_epoch:", live["epoch"])
