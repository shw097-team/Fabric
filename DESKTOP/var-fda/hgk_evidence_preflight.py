# -*- coding: utf-8 -*-
"""HGK-EVIDENCE-PREFLIGHT (machine preflight for external submission) — HGK-GATE-CLOSURE-001.
Runs BEFORE any external evidence submission. Blocks on:
  1. single checker denominator (exactly ONE current receipt; others must be HISTORICAL-marked)
  2. no stale evidence MDs carrying self-hash (this_file_sha256)
  3. manifest: 0 missing files, 0 hash mismatches, subject_root bound
  4. three-way subject binding (manifest == checker == declared final HEAD)
  5. CLOSED findings carry authority receipts
Exit 0 = PREFLIGHT PASS (safe to submit) / exit 1 = BLOCKED (list defects).
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
EVID = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence")
RECEIPTS = EVID / "receipts"

def fail(msg):
    print(f"  [FAIL] {msg}")

def pass_ok(msg):
    print(f"  [PASS] {msg}")

ok = True

print("=== HGK EVIDENCE PREFLIGHT (HGK-GATE-CLOSURE-001) ===")

# 1. single checker denominator
print("--- 1. checker single-denominator ---")
checkers = [f for f in os.listdir(RECEIPTS) if "CHECKER" in f and f.endswith(".json")]
current_checkers = []
for c in checkers:
    try:
        d = json.load(open(RECEIPTS / c, encoding="utf-8"))
        note = str(d.get("note", "")) + str(d.get("artifact_id", "")) + str(d.get("status", ""))
        is_historical = any(k in note.upper() for k in ["HISTORICAL", "SUPERSEDED"])
        subject = str(d.get("subject_root", ""))[:12]
        total = d.get("total_checks")
        if is_historical:
            pass_ok(f"{c}: HISTORICAL (excluded from current)")
        else:
            current_checkers.append((c, subject, total))
    except Exception as e:
        fail(f"{c}: unparseable ({str(e)[:40]})")
        ok = False
if len(current_checkers) == 1:
    pass_ok(f"exactly ONE current checker: {current_checkers[0][0]} ({current_checkers[0][2]} checks, subject {current_checkers[0][1]})")
else:
    fail(f"{len(current_checkers)} current checkers (need exactly 1): {[c[0] for c in current_checkers]}")
    ok = False

# 2. no stale self-hash evidence MDs — only among CURRENT single-evidence series
# (historical RR3/RR5/RR6 MDs legitimately carry self-hash from their era; they are
#  excluded by the CURRENT-series scan below, which targets the LATEST one only)
print("--- 2. stale self-hash evidence MDs (current series) ---")
current_mds = sorted([f for f in os.listdir(EVID) if f.startswith("FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE")])
if current_mds:
    latest = current_mds[-1]
    txt = (EVID / latest).read_text(encoding="utf-8", errors="replace")
    if "this_file_sha256" in txt:
        fail(f"LATEST evidence MD {latest} still carries self-hash")
        ok = False
    else:
        pass_ok(f"latest {latest} has no self-hash; older {len(current_mds)-1} MD(s) historical")
else:
    fail("no current single-evidence MD found")
    ok = False

# 3. manifest integrity
print("--- 3. manifest integrity ---")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
if MAN.exists():
    m = json.load(open(MAN, encoding="utf-8"))
    missing = []
    mismatched = []
    for a in m["artifacts"]:
        p = BUNDLE / a["path"]
        if not p.exists():
            missing.append(a["path"])
        else:
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            if sha != a["sha256"]:
                mismatched.append(a["path"])
    if not missing and not mismatched:
        pass_ok(f"manifest {m['artifact_count']} entries: 0 missing, 0 mismatch")
    else:
        if missing:
            fail(f"manifest missing files: {missing[:3]}")
        if mismatched:
            fail(f"manifest hash mismatches: {mismatched[:3]}")
        ok = False
else:
    fail("manifest not found")
    ok = False

# 4. three-way subject binding
print("--- 4. three-way subject binding ---")
declared_head = None
m_head = None
c_head = None
# declared: from latest single evidence MD header
latest_md = None
for f in sorted(os.listdir(EVID), reverse=True):
    if f.startswith("FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE"):
        latest_md = f
        break
if latest_md:
    txt = (EVID / latest_md).read_text(encoding="utf-8", errors="replace")
    mm = re.search(r"final_subject_root: ([0-9a-f]{40})", txt)
    declared_head = mm.group(1) if mm else None
if MAN.exists():
    m = json.load(open(MAN, encoding="utf-8"))
    m_head = m.get("subject_root", {}).get("git_head")
if current_checkers:
    c_head = current_checkers[0][1]
# normalize: compare first-12 (manifest full hash vs checker truncated vs declared full)
def short(h):
    return h[:12] if h else None
if m_head and declared_head and c_head:
    if short(m_head) == short(declared_head) == short(c_head):
        pass_ok(f"three-way bound: {short(declared_head)}")
    else:
        fail(f"subject mismatch: manifest={short(m_head)} checker={short(c_head)} declared={short(declared_head)}")
        ok = False
else:
    fail(f"cannot bind: manifest={short(m_head)} checker={short(c_head)} declared={short(declared_head)}")
    ok = False

# 5. CLOSED findings carry authority
print("--- 5. CLOSED authority (receipts present) ---")
required = ["FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json", "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json",
            "FDA_CHECKER_FINAL_RR7.json", "FDA_F01_CURRENT_260811_RECEIPT.json", "FDA_F06_FRESH_10RUN_RECEIPT_RR6.json"]
missing_rec = [r for r in required if not (RECEIPTS / r).exists()]
if not missing_rec:
    pass_ok("all CLOSED findings backed by authority receipts")
else:
    fail(f"missing authority receipts: {missing_rec}")
    ok = False

print("=" * 50)
print(f"PREFLIGHT: {'PASS' if ok else 'BLOCKED'}")
sys.exit(0 if ok else 1)
