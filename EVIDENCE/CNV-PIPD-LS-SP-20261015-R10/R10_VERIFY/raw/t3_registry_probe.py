"""T3 - re-derive the control-plane values the R10 adjudication claims, with the project's own reader.

Read-only: imports the project's lane_policy and reports what it resolves.
Run from the HG-KSEOS root with PYTHONPATH=src.
"""
import hashlib
import json
import sys
from pathlib import Path

from hg_kseos import lane_policy as L

reg_path = Path("config/lane-routing-registry.yaml")
raw = reg_path.read_bytes()
print("registry path      :", reg_path.resolve())
print("registry bytes     :", len(raw))
print("registry sha256    :", hashlib.sha256(raw).hexdigest())
print("registry mtime     :", __import__("datetime").datetime.fromtimestamp(reg_path.stat().st_mtime))

reg = L.load_registry()
print("schema             :", reg.get("schema"))
print("epoch              :", L.registry_epoch(reg))
print("routes count       :", len(reg.get("routes", [])))
print("check_drift count  :", len(L.check_drift(registry=reg)))
print("check_drift(_)     :", [f.get("code") for f in L.check_drift(registry=reg)])

for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
    r = L.route_for_lane(reg, lane)
    c = L._compact_route(r) if r else None
    print()
    print("--- route %s ---" % lane)
    if c is None:
        print("ABSENT")
        continue
    for k in ("engine", "provider", "model", "canonical_identity", "auth", "oauth",
              "admission_status", "reasoning_effort", "selection_authority"):
        print("  %-20s %s" % (k, c.get(k) if k in c else (r.get(k) if r else None)))
    print("  fallbacks           ", c.get("fallbacks"))

plan = L.route_for_lane(reg, "PLAN")
ver = L.route_for_lane(reg, "VERIFY_SECURITY")
exe = L.route_for_lane(reg, "EXECUTE")
print()
print("check_sod(PLAN, VERIFY_SECURITY)          :", L.check_sod(plan, ver))
print("check_sod(EXECUTE, VERIFY_SECURITY)       :", L.check_sod(exe, ver))

print()
print("--- raw registry text for the fields the adjudication cites ---")
txt = raw.decode("utf-8")
for needle in ("epoch:", "source_of_routes", "selection_authority",
               "admission_status: ADMITTED", "admission_status: UNPROVEN",
               "SOD006-C2", "OWNER_ORDERED_IN_FORCE", "prior_revision_note"):
    hits = [ln.strip() for ln in txt.splitlines() if needle in ln]
    print("  %-28s %d occurrence(s)" % (needle, len(hits)))
    for h in hits[:3]:
        print("        ", h[:160])
