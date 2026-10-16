import json, os
COPY = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject"
mla = json.load(open(os.path.join(COPY, "config", "model-lane-assignment.json"), encoding="utf-8"))
sod = mla.get("sod", {})
print("sod keys:", sorted(sod.keys()))
for k, v in sod.items():
    if isinstance(v, list):
        for e in v:
            if isinstance(e, dict) and e.get("id"):
                print("  ", e.get("id"), "->", e.get("status"))
    elif isinstance(v, dict) and v.get("id"):
        print("  ", v.get("id"), "->", v.get("status"))
# search any nested conflicts
def walk(o, path=""):
    if isinstance(o, dict):
        if "id" in o and "status" in o and isinstance(o.get("id"), str) and "SOD" in str(o.get("id")):
            print("  FOUND", path, o.get("id"), o.get("status"))
        for k, v in o.items():
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "/" + str(i))
walk(mla)
