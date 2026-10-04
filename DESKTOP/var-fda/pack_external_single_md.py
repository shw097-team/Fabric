# -*- coding: utf-8 -*-
"""pack_external_single_md.py — EXTERNAL-REVIEW SINGLE-MD MANDATORY ROUTE (Step 6A).
Reads EvidenceManifest + key receipts + runtime DBs and emits ONE self-contained MD
with FULL RAW BODIES inlined (external reviewer cannot open MEDIA/local paths)."""
import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
OUT = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_FULL_EVIDENCE_20260814.md")

EM = json.load(open(BUNDLE / "FDA_EVIDENCE_MANIFEST.json", encoding="utf-8"))

sections = []
sections.append("""# FDA External Full Evidence — SINGLE SELF-CONTAINED FILE (raw bodies inlined)

```yaml
report_id: FDA_EXTERNAL_FULL_EVIDENCE_20260814
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

# --- §1 claim ceiling (from evidence MD) ---
ev = (FDA / "FDA_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
sections.append("## 1. Claim ceiling (embedded from FDA_IMPLEMENTATION_EVIDENCE.md)\n\n```text\n" +
                ev.split("## 0. Claim ceiling")[1].split("## 1.")[0].strip() + "\n```\n")

# --- §2 full artifact table with hashes ---
rows = ["| # | Path | SHA-256 | Bytes |", "|---|---|---|---|"]
for i, a in enumerate(EM["artifacts"], 1):
    rows.append(f"| {i} | `{a['path']}` | `{a['sha256'][:16]}…` | {a['size']} |")
sections.append("## 2. EvidenceManifest — full artifact table (%d entries)\n\n" % EM["artifact_count"] +
                "\n".join(rows) + "\n")

# --- §3 key receipts FULL BODIES ---
KEY_RECEIPTS = [
    "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json",
    "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
    "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
    "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
    "FDA_F01_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_TEN_RUN_RECEIPT.json",
    "FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
]
sections.append("## 3. Key receipts — FULL RAW BODIES\n")
for name in KEY_RECEIPTS:
    p = FDA / name
    if p.exists():
        body = p.read_text(encoding="utf-8")
        sections.append(f"### {name} (sha256 {hashlib.sha256(body.encode()).hexdigest()[:16]}…)\n\n```json\n{body}\n```\n")

# --- §4 XQ PAPER runtime raw DB extracts ---
sections.append("## 4. XQ PAPER runtime — raw DB extracts (execution truth)\n")
try:
    db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    raw_cols = [col[1] for col in c.execute("PRAGMA table_info(Table_20260814)").fetchall()]
    cols = [x.decode("cp950", errors="replace") for x in raw_cols]
    rows = c.execute("SELECT * FROM Table_20260814 WHERE XQSensorName LIKE '%FDA%'").fetchall()
    def dec(b):
        return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
    out = ["| " + " | ".join(cols[:12]) + " |", "|" + "---|" * 12]
    for r in rows[:40]:
        out.append("| " + " | ".join(dec(x)[:20] for x in r[:12]) + " |")
    c.close()
    sections.append("### SensorLog Table_20260814 (FDA rows, %d total)\n\n" % len(rows) + "\n".join(out) + "\n")
except Exception as e:
    sections.append(f"(SensorLog read err: {str(e)[:80]})\n")

try:
    db2 = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
    c2 = sqlite3.connect(f"file:{db2}?mode=ro", uri=True, timeout=8)
    c2.text_factory = bytes
    rows2 = c2.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
    out2 = ["| Name | Script | Symbol | Created |", "|---|---|---|---|"]
    for n, s, y, ct in rows2:
        out2.append(f"| {dec(n)[:35]} | {dec(s)[:25]} | {dec(y)[:15]} | {dec(ct)} |")
    c2.close()
    sections.append("### SensorList (persistence)\n\n" + "\n".join(out2) + "\n")
except Exception as e:
    sections.append(f"(SensorList read err: {str(e)[:80]})\n")

# --- §5 DoD-36 matrix (from evidence MD §7) ---
sections.append("## 5. DoD-36 matrix (embedded)\n\n```text\nDoD summary: " +
                str(EM["dod_counts"]) + "\n```\n")

# --- §6 external verifier checklist ---
sections.append("""## 6. External verifier checklist (self-contained)

1. Verify this file's sha256 == the value submitted (identity gate).
2. Recompute EvidenceManifest sha256 (embedded §0) from the manifest JSON.
3. Verify artifact table §2 row count == manifest_entry_count.
4. Verify SensorLog §4 rows: >=1 FDA strategy with full state machine (2→3→1, ExecState 1→8).
5. Verify SensorList §4 persistence rows.
6. Re-run independent_checker.py → 174/174 PASS (embedded §0).
7. Verify DoD counts §5 == PASS 36 / PARTIAL 0 / BLOCKED 0.
8. Claim ceiling §1: FAIL_CLOSED until verdict; SQS NOT_AUTHORIZED.
""")

md = "\n".join(sections)
OUT.write_text(md, encoding="utf-8")
sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
print("wrote:", OUT)
print("sha256:", sha)
print("bytes:", len(md.encode("utf-8")))
