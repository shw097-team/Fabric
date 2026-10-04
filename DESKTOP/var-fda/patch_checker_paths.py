# -*- coding: utf-8 -*-
"""Patch independent_checker.py paths for reorganized FDA folder."""
import re

P = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\independent_checker.py"
t = open(P, encoding="utf-8").read()

# governance/ subdir
for f in ("FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml", "FDA_INTEROP_DISPOSITION.yaml",
          "FDA_ROUTE_CHECK.yaml", "FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml"):
    t = t.replace(f'FDA / "{f}"', f'FDA / "governance/{f}"')

# evidence/receipts/ subdir
for f in ("FDA_C0_READBACK_RECEIPT.json", "FDA_F01_LIVE_FIXTURE_RECEIPT.json",
          "FDA_BOUNDED_CONTROL_LIVE_PROBE.json", "FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
          "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json", "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
          "FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json"):
    t = t.replace(f'FDA / "{f}"', f'FDA / "evidence/receipts/{f}"')

open(P, "w", encoding="utf-8", newline="\n").write(t)
print("checker patched")

# verify no stale root refs
stale = re.findall(r'FDA / "(FDA_[A-Z0-9_]+\.(?:json|yaml))"', t)
print("stale root refs:", stale if stale else "(none)")
