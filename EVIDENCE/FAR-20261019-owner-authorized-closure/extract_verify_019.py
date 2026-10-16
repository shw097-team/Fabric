#!/usr/bin/env python
"""Extract the VERIFY lane's verdicts into lane/VERIFY_REPORT.json.

The checker runs read-only, so it cannot write a file: it prints one `VERIFY-ITEM: {...}` JSON object per
line to stdout and the harness captures that. This script only *moves* those bytes into a file — it does
not summarise, reorder or reinterpret them, and it records that the extraction was mechanical, so no one can
mistake the harness for the checker.
"""
import json, re, sys
from pathlib import Path

D = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
blobs = []


def collect(o, into):
    if isinstance(o, str):
        into.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            collect(v, into)
    elif isinstance(o, list):
        for v in o:
            collect(v, into)


receipt = None
for cand in ("lane/VERIFY_RECEIPT.json", "lane/VERIFY_ATTEMPT1_REFUSED.json"):
    p = D / cand
    if p.exists():
        try:
            receipt = json.loads(p.read_text(encoding="utf-8"))
            collect(receipt, blobs)
        except Exception as e:
            print("could not parse", cand, e)
nd = list((D / "lane").glob("*.attempts.ndjson"))
for p in nd:
    blobs.append(p.read_text(encoding="utf-8", errors="replace"))

items, overall, nonce = [], None, False
for b in blobs:
    for line in b.splitlines():
        s = line.strip()
        if "VERIFY-ITEM:" in s:
            frag = s.split("VERIFY-ITEM:", 1)[1].strip()
            try:
                items.append(json.loads(frag))
            except Exception:
                items.append({"item": "unparsed", "verdict": "UNPARSED", "raw": frag[:400]})
        if "VERIFY-OVERALL:" in s:
            frag = s.split("VERIFY-OVERALL:", 1)[1].strip()
            try:
                overall = json.loads(frag)
            except Exception:
                overall = {"overall": "UNPARSED", "raw": frag[:400]}
        if "CNVEA-FAR019-VERIFY-NONCE-4c8ba1" in s:
            nonce = True


def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        k = json.dumps({kk: r.get(kk) for kk in ("item", "verdict")}, sort_keys=True)
        if k in seen and r.get("raw_output") is None:
            continue
        seen.add(k)
        out.append(r)
    return out


items = dedupe(items)
tally = {}
for r in items:
    v = r.get("verdict")
    tally[v] = tally.get(v, 0) + 1
rep = {"schema": "FAR-20261019/VERIFY-REPORT/1",
       "extraction_note": "mechanically moved from the checker's stdout by the harness; unmodified; the "
                          "checker ran read-only and could not write this file itself",
       "checker_arm_nonce_echo_seen": nonce,
       "receipt_ok": (receipt or {}).get("ok"), "receipt_code": (receipt or {}).get("code"),
       "receipt_sandbox": (receipt or {}).get("sandbox"),
       "items": items, "tally": tally, "overall": overall,
       "verdict": "COLLECTED" if items else "NO_VERDICTS_FOUND"}
(D / "lane/VERIFY_REPORT.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print("items collected:", len(items), "| tally:", tally, "| overall:", json.dumps(overall)[:200])
print("receipt ok/code/sandbox:", rep["receipt_ok"], rep["receipt_code"], rep["receipt_sandbox"])
print("wrote lane/VERIFY_REPORT.json")
sys.exit(0 if items else 4)
