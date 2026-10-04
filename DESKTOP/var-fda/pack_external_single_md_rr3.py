# -*- coding: utf-8 -*-
"""pack_external_single_md.py — v3 (RR3) EXTERNAL-REVIEW SINGLE-MD MANDATORY ROUTE (hgk skill Step 6A).
Emits ONE self-contained evidence MD with FULL RAW BODIES inlined:
- header: subject root, manifest sha (loop-free single-direction), exact sets, checker, DoD
- §1 claim ceiling (embedded)
- §2 exact-set definitions (payload/manifest/bundle/self-entry policy)
- §3 full EvidenceManifest artifact table (51 payload rows)
- §4 key receipts FULL JSON BODIES (7 receipts from evidence/receipts/)
- §5 XQ PAPER runtime raw DB extracts (SensorLog Table_20260814 + SensorList)
- §6 DoD-36 counts
- §7 self-contained external verifier checklist
"""
import hashlib
import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

# --- config ---
BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
REC = FDA / "evidence" / "receipts"
OUT = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md")
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
mh = hashlib.sha256(open(BUNDLE / "FDA_EVIDENCE_MANIFEST.json", "rb").read()).hexdigest()
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

S = []
S.append(f"""# FDA External Single Evidence — FULLY EMBEDDED (RR3 packaging closure)

```yaml
report_id: FDA_EXTERNAL_SINGLE_EVIDENCE_RR3
mode: SINGLE_MD_MANDATORY_ROUTE (Step 6A — all raw bodies embedded; no local-path dependency)
this_file_sha256: <FINAL_FILL>
generated_at_utc: {now}
subject_root: {EM['subject_root']['git_head']}
manifest_sha256: {mh}
checker: {EM['checker']['verdict']} {EM['checker']['checks']}/{EM['checker']['failed']}
dod_counts: {json.dumps(EM['dod_counts'], ensure_ascii=False)}
exact_sets: {json.dumps({k: EM['exact_sets'][k] for k in ('payload_entries','manifest_entries','bundle_files')}, ensure_ascii=False)}
self_entry_policy: {EM['exact_sets']['self_entry_policy']}
```""")

# §1 claim ceiling
ev = (FDA / "FDA_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
S.append("## 1. Claim ceiling (embedded)\n\n```text\n" +
         ev.split("## 0. Claim ceiling")[1].split("## 1.")[0].strip() + "\n```\n")

# §2 exact sets
S.append("## 2. Exact-set definitions (unambiguous, rehashable)\n\n```text\n" +
         "payload_entries   = %d  (manifest rows; EXCLUDES manifest itself AND evidence MD)\n"
         "manifest_entries  = %d  (payload + 1 = manifest JSON physically present, not self-listed)\n"
         "bundle_files      = %d  (physical recursive count in FDA_RAW_REVIEW_BUNDLE)\n"
         "self_entry_policy = manifest excludes itself AND evidence reducer MD (loop breaker);\n"
         "                    MD references manifest by sha256 (single direction); reviewer\n"
         "                    recomputes MD sha from submitted bytes\n" % (
             EM["exact_sets"]["payload_entries"], EM["exact_sets"]["manifest_entries"],
             EM["exact_sets"]["bundle_files"]) + "```\n")

# §3 manifest artifact table
rows = ["| # | Path | SHA-256 | Bytes |", "|---|---|---|---|"]
for i, a in enumerate(EM["artifacts"], 1):
    rows.append(f"| {i} | `{a['path']}` | `{a['sha256']}` | {a['size']} |")
S.append(f"## 3. EvidenceManifest — full payload table ({EM['artifact_count']} rows)\n\n" + "\n".join(rows) + "\n")

# §4 key receipts FULL BODIES
S.append("## 4. Key receipts — FULL RAW BODIES\n")
for name in KEY_RECEIPTS:
    p = REC / name
    if p.exists():
        body = p.read_text(encoding="utf-8")
        S.append(f"### {name} (sha256 {hashlib.sha256(body.encode()).hexdigest()})\n\n```json\n{body}\n```\n")
    else:
        S.append(f"### {name}\n\n(MISSING: {p})\n")

# §5 XQ PAPER raw DB extracts
S.append("## 5. XQ PAPER runtime — raw DB extracts (execution truth)\n")
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
try:
    c = sqlite3.connect(f"file:{SENSORLOG_DB}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    raw_cols = [col[1] for col in c.execute(f"PRAGMA table_info({SENSORLOG_TABLE})").fetchall()]
    cols = [x.decode("cp950", errors="replace") for x in raw_cols]
    rows = c.execute(f"SELECT * FROM {SENSORLOG_TABLE} WHERE XQSensorName LIKE '%FDA%'").fetchall()
    out = ["| " + " | ".join(cols[:10]) + " |", "|" + "---|" * 10]
    for r in rows[:50]:
        out.append("| " + " | ".join(dec(x)[:18] for x in r[:10]) + " |")
    c.close()
    S.append(f"### SensorLog {SENSORLOG_TABLE} (FDA rows: {len(rows)})\n\n" + "\n".join(out) + "\n")
except Exception as e:
    S.append(f"(SensorLog read err: {str(e)[:100]})\n")

try:
    c2 = sqlite3.connect(f"file:{SENSORLIST_DB}?mode=ro", uri=True, timeout=8)
    c2.text_factory = bytes
    rows2 = c2.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
    out2 = ["| Name | Script | Symbol | Created |", "|---|---|---|---|"]
    for n, s, y, ct in rows2:
        out2.append(f"| {dec(n)[:35]} | {dec(s)[:25]} | {dec(y)[:15]} | {dec(ct)} |")
    c2.close()
    S.append("### SensorList (persistence)\n\n" + "\n".join(out2) + "\n")
except Exception as e:
    S.append(f"(SensorList read err: {str(e)[:100]})\n")

# §6 DoD counts
S.append("## 6. DoD-36 counts\n\n```text\n" + json.dumps(EM["dod_counts"], ensure_ascii=False) + "\n```\n")

# §7 verifier checklist
S.append("""## 7. External verifier checklist (self-contained, no local access needed)

1. Verify this file's sha256 == submitted value (identity gate).
2. Recompute EvidenceManifest sha256 (header) from the manifest JSON (bundled).
3. Verify artifact table §3 row count == payload_entries; every row path unique.
4. Verify every §3 row hash/size against the bundled file bytes.
5. Verify SensorLog §5: >=1 FDA strategy with full state machine (XSSensorState 2->3->1,
   ExecState 1->8, SymbolID=2330.TW, multiple TriggerTime cycles).
6. Verify SensorList §5 persistence rows (>=5 FDA strategies).
7. Re-run independent_checker.py -> 176/176 PASS (header).
8. Verify DoD counts §6 == PASS 36 / PARTIAL 0 / BLOCKED 0.
9. Verify claim ceiling §1: FAIL_CLOSED until verdict; SQS NOT_AUTHORIZED.
10. Verify subject root: git rev-parse HEAD == header subject_root.
""")

md = "\n".join(S)
OUT.write_text(md, encoding="utf-8")
sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
print("wrote:", OUT)
print("pre-header sha256:", sha)
print("bytes:", len(md.encode("utf-8")))
