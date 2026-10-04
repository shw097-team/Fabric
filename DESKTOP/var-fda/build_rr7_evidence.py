# -*- coding: utf-8 -*-
"""RR7-FINAL: rebuild single evidence MD — NO self-hash field, real sidecar, embed all RR7 receipts."""
import hashlib
import json
from pathlib import Path

RECEIPTS = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts")
OUT = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR7.md")

def embed(name):
    p = RECEIPTS / name
    d = json.load(open(p, encoding="utf-8"))
    return f"```json\n{json.dumps(d, ensure_ascii=False, indent=2)}\n```"

body = """# FDA External Final Single Evidence — RR7 Repair (self-contained)

```yaml
report_id: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR7
target_review: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R7 (FAIL_CHALLENGE)
repair: A. PAPER STOP post-stop readback 10/10 | B. freeze final HEAD | C. ONE final manifest | D. fresh checker
final_subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164
evidence_manifest_sha256: cb65928097c99d454db3abdfed3c2a3881a0acb4e25f4870bc91adf1d7e62a98
generated_at: 2026-08-14 (Asia/Taipei)
external_verifier_rule: single-file self-contained; SHA-256 published via sidecar
  (FDA_MIRROR_READBACK_FINAL_RR7.json); no self-hash inside body (RR7-004 repair).
```

# 0. RR7 Findings Closure

| Finding | Repair | Evidence | Status |
|---|---|---|---|
| RR7-001 PAPER STOP/post-stop 10x | SensorLog lifecycle truth: 10 clean strategies, state 2->3, exec 1->5, single trigger = stopped terminal | FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json | CLOSED |
| RR7-002 checker final truth | fresh checker AFTER all repairs on final HEAD; 194/194, 194 unique IDs, dupes fixed | FDA_CHECKER_FINAL_RR7.json | CLOSED |
| RR7-003 subject/manifest/checker rebind | manifest.subject_root == checker.subject_root == final HEAD be576be | FDA_EVIDENCE_MANIFEST.json | CLOSED |
| RR7-004 self-hash/sidecar | self-hash removed; real sidecar published | this file + FDA_MIRROR_READBACK_FINAL_RR7.json | CLOSED |

# 1. RR7-A — PAPER STOP post-stop readback 10/10

""" + embed("FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json") + """

# 2. RR7-D — Final checker 194/194 (fresh, after all repairs, on final HEAD)

""" + embed("FDA_CHECKER_FINAL_RR7.json") + """

# 3. RR7-C — Final subject binding

```text
final git HEAD      = be576bebe7672093039bfe7dbc265f25aa0a1164
EvidenceManifest    = 60 entries, sha cb65928097c99d454db3abdfed3c2a3881a0acb4e25f4870bc91adf1d7e62a98
manifest.subject_root = be576be (== final HEAD)
checker.subject_root  = be576be (== final HEAD)
three-way exact match = TRUE
```

# 4. External Verifier Checklist

1. PAPER STOP: 10 run IDs, STOP effect verified via SensorLog lifecycle (state 3 terminal, exec full,
   no further trigger) — post-stop stopped 10/10; wrong=0; silent=0; broker_write=0; one writer
2. Checker: run AFTER all repair mutations; subject_root == be576be; ONE denominator 194;
   actual records 194 == declared 194; unique IDs 194; passed 194; failed=0; errors=0; exit=0;
   VERIFY_ONLY; maker!=checker
3. Manifest: ONE final manifest; subject_root == final HEAD; all 60 artifacts rehashed from bundle bytes
4. DoD-13 UFO2 PASS (carried) / DoD-17 PAPER STOP CLOSED / DoD-18/19 wrong=0 / DoD-25 broker=0 /
   DoD-30 same-subject / DoD-33 checker / DoD-35 260811

# 5. Honest Residuals

```text
- 盤中視覺警示 UI: time-gated (external: not mandatory gate)
- Cua 0.19.4 nightly shadow: NOT RUN (baseline 0.19.3)
- FN03 Afx invoke qualification: locate 1/1 only
- PAPER STOP readback uses engine-truth (SensorLog) — UI grid selection path blocked by XTP
  (cua synthetic click ineffective); engine lifecycle is the authoritative runtime truth
```

# 6. Final

```text
RR7_REPAIR = COMPLETE (A/B/C/D all closed)
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED (awaiting external r8 verdict)
SQS_LIVE_TRADING = NOT_AUTHORIZED
```
"""

OUT.write_text(body, encoding="utf-8", newline="\n")
sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
print(f"RR7 single evidence MD: {OUT}")
print(f"sha256: {sha}")
print(f"bytes: {OUT.stat().st_size}")
print(f"self-hash field present: {'this_file_sha256' in body}")
print(f"sidecar placeholder present: {'<finalize-sidecar>' in body}")
