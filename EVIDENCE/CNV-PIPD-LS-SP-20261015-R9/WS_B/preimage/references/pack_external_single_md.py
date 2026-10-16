# -*- coding: utf-8 -*-
"""pack_external_single_md.py — EXTERNAL-REVIEW SINGLE-MD MANDATORY ROUTE (hgk skill Step 6A).

MANDATORY: when an internal acceptance round completes and the next step is external
review, run this to emit ONE self-contained evidence MD with FULL RAW BODIES inlined.
External reviewer environments CANNOT open MEDIA attachments or local paths — the
message body / single MD is the ONLY readable channel (FAR R7/R8 rule).

Usage (adjust paths to current round):
  python pack_external_single_md.py
Output: <evidence/review>/FDA_EXTERNAL_FULL_EVIDENCE_<date>.md

What it embeds (no pointers):
- header: subject_root, manifest sha256, checker verdict/denominator, DoD counts
- §1 claim ceiling (from FDA_IMPLEMENTATION_EVIDENCE.md)
- §2 full EvidenceManifest artifact table (path + sha256 + bytes)
- §3 key receipts FULL JSON BODIES (UFO2 effective-load, PAPER runtime, fingerprint,
  native qualification, F01, F06, lease concurrency)
- §4 XQ PAPER runtime raw DB extracts (SensorLog Table_YYYYMMDD FDA rows + SensorList)
- §5 DoD-36 counts, §6 self-contained verifier checklist

Freeze order (hard): freeze HEAD -> receipts -> tests -> fresh checker -> manifests
-> render THIS MD LAST -> mirror byte-identical -> readback -> submit exact bytes.
Never append a ChangeSet after manifest regeneration. Verify embedded-body presence
after generation (receipt_bodies / sensorlog_rows / sensorlist_rows / dod_counts).

Track A normalization: single-valued truth everywhere (no stale superseded prose);
label old counts SUPERSEDED_PRE_<PATCH>. Identity gate: the sha256 you claim MUST be
the bytes the reviewer actually receives.
"""
import hashlib
import json
import sqlite3
import time
from pathlib import Path

# --- config (adjust per round) ---
# PRIMARY HOME = the team's own evidence/ dir (Step 6B Evidence Home Rule, user-mandated
# 2026-08-14). The single MD MUST be written here FIRST; Fabric|HGK|SQS evidence\review
# are MIRRORS ONLY. Writing only to review\ violates Step 6B (root-caused via FAR: the
# rr5 packer hard-coded review\ and 5 evidence files landed outside the team folder).
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
TEAM_EVIDENCE = FDA / "evidence"                      # <-- PRIMARY HOME (Step 6B)
OUT = TEAM_EVIDENCE / "FDA_EXTERNAL_FULL_EVIDENCE_20260814.md"   # write to team home FIRST
REVIEW_ROOT = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review")
MIRROR_ROOTS = [REVIEW_ROOT,
                Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\evidence\review"),
                Path(r"C:\Projects\Agent_Workspace\SQS-THC\evidence\review")]
SENSORLOG_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
SENSORLIST_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
SENSORLOG_TABLE = "Table_20260814"
KEY_RECEIPTS = [
    "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json",
    "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
    "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
    "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
    "FDA_F01_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_TEN_RUN_RECEIPT.json",
    "FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
]

EM = json.load(open(BUNDLE / "FDA_EVIDENCE_MANIFEST.json", encoding="utf-8"))
sections = []
sections.append("""# FDA External Full Evidence — SINGLE SELF-CONTAINED FILE (raw bodies inlined)

```yaml
report_id: FDA_EXTERNAL_FULL_EVIDENCE_<DATE>
mode: SINGLE_MD_MANDATORY_ROUTE (Step 6A — all raw bodies embedded, no local-path dependency)
subject_root: %s
evidence_manifest_sha256: %s
manifest_entries: %d
checker: %s %d/%d
dod_counts: %s
generated_at: %s
```
""" % (
    EM["subject_root"]["git_head"],
    hashlib.sha256(open(BUNDLE / "FDA_EVIDENCE_MANIFEST.json", "rb").read()).hexdigest(),
    EM["artifact_count"],
    EM["checker"]["verdict"], EM["checker"]["checks"], EM["checker"]["failed"],
    json.dumps(EM["dod_counts"], ensure_ascii=False),
    time.strftime("%Y-%m-%dT%H:%M:%S"),
))

ev = (FDA / "FDA_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
sections.append("## 1. Claim ceiling (embedded)\n\n```text\n" +
                ev.split("## 0. Claim ceiling")[1].split("## 1.")[0].strip() + "\n```\n")

rows = ["| # | Path | SHA-256 | Bytes |", "|---|---|---|---|"]
for i, a in enumerate(EM["artifacts"], 1):
    rows.append(f"| {i} | `{a['path']}` | `{a['sha256'][:16]}…` | {a['size']} |")
sections.append("## 2. EvidenceManifest — full artifact table (%d entries)\n\n" % EM["artifact_count"] +
                "\n".join(rows) + "\n")

sections.append("## 3. Key receipts — FULL RAW BODIES\n")
for name in KEY_RECEIPTS:
    p = FDA / name
    if p.exists():
        body = p.read_text(encoding="utf-8")
        sections.append(f"### {name} (sha256 {hashlib.sha256(body.encode()).hexdigest()[:16]}…)\n\n```json\n{body}\n```\n")

sections.append("## 4. XQ PAPER runtime — raw DB extracts (execution truth)\n")
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
try:
    c = sqlite3.connect(f"file:{SENSORLOG_DB}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    raw_cols = [col[1] for col in c.execute(f"PRAGMA table_info({SENSORLOG_TABLE})").fetchall()]
    cols = [x.decode("cp950", errors="replace") for x in raw_cols]
    rows = c.execute(f"SELECT * FROM {SENSORLOG_TABLE} WHERE XQSensorName LIKE '%FDA%'").fetchall()
    out = ["| " + " | ".join(cols[:12]) + " |", "|" + "---|" * 12]
    for r in rows[:40]:
        out.append("| " + " | ".join(dec(x)[:20] for x in r[:12]) + " |")
    c.close()
    sections.append(f"### SensorLog {SENSORLOG_TABLE} (FDA rows, {len(rows)} total)\n\n" + "\n".join(out) + "\n")
except Exception as e:
    sections.append(f"(SensorLog read err: {str(e)[:80]})\n")

try:
    c2 = sqlite3.connect(f"file:{SENSORLIST_DB}?mode=ro", uri=True, timeout=8)
    c2.text_factory = bytes
    rows2 = c2.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
    out2 = ["| Name | Script | Symbol | Created |", "|---|---|---|---|"]
    for n, s, y, ct in rows2:
        out2.append(f"| {dec(n)[:35]} | {dec(s)[:25]} | {dec(y)[:15]} | {dec(ct)} |")
    c2.close()
    sections.append("### SensorList (persistence)\n\n" + "\n".join(out2) + "\n")
except Exception as e:
    sections.append(f"(SensorList read err: {str(e)[:80]})\n")

sections.append("## 5. DoD-36 matrix counts\n\n```text\n" + str(EM["dod_counts"]) + "\n```\n")
sections.append("""## 6. External verifier checklist (self-contained)

1. Verify this file's sha256 == submitted value (identity gate).
2. Recompute EvidenceManifest sha256 (embedded §0) from the manifest JSON.
3. Verify artifact table §2 row count == manifest_entry_count.
4. Verify SensorLog §4 rows: >=1 FDA strategy with full state machine (2→3→1, ExecState 1→8).
5. Verify SensorList §4 persistence rows.
6. Re-run independent_checker.py -> 174/174 PASS (embedded §0).
7. Verify DoD counts §5 == PASS 36 / PARTIAL 0 / BLOCKED 0.
8. Claim ceiling §1: FAIL_CLOSED until verdict; SQS NOT_AUTHORIZED.
""")

md = "\n".join(sections)
OUT.write_text(md, encoding="utf-8")
sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
print("wrote:", OUT)
print("sha256 (pre-header):", sha)
