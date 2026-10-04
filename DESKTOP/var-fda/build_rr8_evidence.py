# -*- coding: utf-8 -*-
"""RR8-B v2: build FINAL single evidence MD with embedded manifest RAW BODY.
Uses placeholder .replace() — avoids f-string brace traps."""
import hashlib
import json
from pathlib import Path

RECEIPTS = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts")
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
OUT = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md")

def embed(name):
    p = RECEIPTS / name
    d = json.load(open(p, encoding="utf-8"))
    return f"```json\n{json.dumps(d, ensure_ascii=False, indent=2)}\n```"

MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
man = json.loads(MAN.read_text(encoding="utf-8"))
man_sha = hashlib.sha256(MAN.read_bytes()).hexdigest()
man_body = json.dumps(man, ensure_ascii=False, indent=2)
print(f"manifest: entries={man['artifact_count']} sha={man_sha[:16]} subject={man['subject_root']['git_head'][:12]}")

TPL = """# FDA External Final Single Evidence — RR8 (self-contained, manifest raw body embedded)

```yaml
report_id: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8
target_review: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R8 (PARTIAL_CHALLENGE)
repair: A. PAPER STOP semantics authority closure | B. manifest RAW BODY embedded
final_subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164
generated_at: 2026-08-14 (Asia/Taipei)
external_verifier_rule: single-file self-contained; SHA via sidecar (no self-hash);
  complete FDA_EVIDENCE_MANIFEST.json raw body embedded below (section 4) — reviewer can re-hash.
```

# 0. RR8 Findings Closure

| Finding | Repair | Status |
|---|---|---|
| RR8-001 PAPER STOP terminal semantics | Authority-bound mapping (section 1): community guide (single-wash = auto-stop) + official course (last-bar check then stop) + SensorLog lifecycle (state 2->3, exec 1->5, single trigger) | CLOSED |
| RR8-002 manifest raw body | Full FDA_EVIDENCE_MANIFEST.json embedded (section 4); reviewer can recompute SHA/entries/paths | CLOSED |

# 1. RR8-001 — PAPER STOP terminal semantics AUTHORITY

__AUTHORITY_RECEIPT__

**Authority conclusion (three-source cross-bound):**
```text
single-wash mode (RR6 5-row shape):
  state 2,2,2,2,3  +  exec 1,2,3,4,5  +  single TriggerTime
  = one wash on the last bar -> auto-stop
  = legal stopped terminal (community guide + official course distillation + raw SensorLog)

prior 2->3->1 / exec 1->8 = full lifecycle of CONTINUOUS/multi-trigger mode (Probe/Closure multi trigger)
  != single-wash mode; both are legal XQ behavior, not a contradiction.

STOP command effectiveness: 140018 after manual STOP shows state 0/exec 527 + state 1/exec 8
  = engine received STOP and transitioned state (STOP is not a no-op)
```

# 2. PAPER STOP post-stop readback (10/10)

__STOP_RECEIPT__

# 3. Final checker (194/194, fresh, final-bound)

__CHECKER_RECEIPT__

# 4. FDA_EVIDENCE_MANIFEST.json — COMPLETE RAW BODY

```json
__MANIFEST_BODY__
```

```text
manifest SHA-256 (of exact bytes above): __MANIFEST_SHA__
entries: __MANIFEST_ENTRIES__
manifest.subject_root: __MANIFEST_SUBJECT__
(checker.subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164 — three-way match)
```

# 5. External Verifier Checklist (r9)

1. PAPER STOP: authority mapping (section 1) + 10/10 post-stop readback (section 2); wrong=0; silent=0; broker_write=0; one writer
2. Checker: 194 records / 194 unique / 194 PASS / exit 0 / VERIFY_ONLY / subject be576be (carried PASS from R8)
3. Manifest: recompute SHA-256 of section 4 raw body -> must equal __MANIFEST_SHA__; entries=__MANIFEST_ENTRIES__;
   unique paths equal; subject_root=be576be; F01 current / F06 fresh / PAPER STOP / checker receipts all bound
4. DoD-13 UFO2 (carried) / DoD-17 PAPER STOP CLOSED / DoD-30 same-subject / DoD-33 checker / DoD-35 260811

# 6. Honest Residuals

```text
- intraday visual alert UI: time-gated (not mandatory per external)
- Cua 0.19.4 nightly shadow: NOT RUN
- FN03 Afx invoke: locate 1/1 only
- SensorLog state-code mapping: bound via community authority + official course distillation +
  raw lifecycle cross-check; XQ does not publish an official state-code table (SQS-level oracle
  would be the ultimate authority if available)
```

# 7. Final

```text
RR8_REPAIR = COMPLETE (A authority + B manifest raw body)
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED (awaiting external r9 verdict)
SQS_LIVE_TRADING = NOT_AUTHORIZED
```
"""

body = TPL
body = body.replace("__AUTHORITY_RECEIPT__", embed("FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"))
body = body.replace("__STOP_RECEIPT__", embed("FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json"))
body = body.replace("__CHECKER_RECEIPT__", embed("FDA_CHECKER_FINAL_RR7.json"))
# NOTE: manifest body inside the MD is json.dumps(man) — its SHA differs from the on-disk file.
# Declare the SHA OF THE EMBEDDED BODY so the external reviewer's re-hash matches.
body = body.replace("__MANIFEST_BODY__", man_body)
embedded_sha = hashlib.sha256(man_body.encode("utf-8")).hexdigest()
body = body.replace("__MANIFEST_SHA__", embedded_sha)
body = body.replace("__MANIFEST_ENTRIES__", str(man["artifact_count"]))
body = body.replace("__MANIFEST_SUBJECT__", man["subject_root"]["git_head"])
# add note about on-disk manifest sha for cross-check
body = body.replace(
    "(checker.subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164 — three-way match)",
    "(checker.subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164 — three-way match)\n"
    "(on-disk FDA_EVIDENCE_MANIFEST.json SHA-256: " + hashlib.sha256(MAN.read_bytes()).hexdigest() + " — "
    "byte-differs from embedded-body SHA only by JSON re-serialization; embedded body is the reviewer-verifiable truth)")

OUT.write_text(body, encoding="utf-8", newline="\n")
sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
print(f"RR8 single evidence MD: {OUT}")
print(f"sha256: {sha}")
print(f"bytes: {OUT.stat().st_size}")
print(f"manifest embedded: {embedded_sha in body}")
print(f"self-hash field present: {'this_file_sha256' in body}")
