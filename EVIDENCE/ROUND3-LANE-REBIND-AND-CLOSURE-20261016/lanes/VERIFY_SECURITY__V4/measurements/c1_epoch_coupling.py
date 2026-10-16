import hashlib, json, os, sys

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016"
COPY = os.path.join(ROOT, "lanes", "VERIFY_SECURITY", "V4", "work", "subject")

mla_path = os.path.join(COPY, "config", "model-lane-assignment.json")
reg_path = os.path.join(COPY, "config", "lane-routing-registry.yaml")

raw = open(mla_path, "rb").read()
live_sha = hashlib.sha256(raw).hexdigest()
mla = json.loads(raw.decode("utf-8"))

print("mla_sha256_recomputed:", live_sha)
print("mla_revision:", mla.get("revision"))
print("mla_registry_epoch:", mla.get("registry_epoch"))

# parse registry minimally (text) without yaml dep
reg = open(reg_path, "r", encoding="utf-8").read()
import re
m = re.search(r"^epoch:\s*(\d+)", reg, re.M)
print("registry_epoch_field:", m.group(1) if m else None)
for line in reg.splitlines():
    if "sha256" in line:
        print("registry_sha_line:", line.strip())
    if "revision" in line:
        print("registry_rev_line:", line.strip())
