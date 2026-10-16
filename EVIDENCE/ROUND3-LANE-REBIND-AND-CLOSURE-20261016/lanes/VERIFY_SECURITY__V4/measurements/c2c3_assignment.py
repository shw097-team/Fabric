import json, os
COPY = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject"
mla = json.load(open(os.path.join(COPY, "config", "model-lane-assignment.json"), encoding="utf-8"))
print("revision:", mla.get("revision"), "registry_epoch:", mla.get("registry_epoch"))
for lane in ("PLAN", "VERIFY_SECURITY", "EXECUTE"):
    print("===", lane)
    for i, e in enumerate(mla["lane_chains"][lane]):
        print("  ", i, e.get("provider"), e.get("model"), "| default:", e.get("default"),
              "| arm:", e.get("arm"), "| automatic_selection:", e.get("automatic_selection"),
              "| role:", e.get("role"))
