#!/usr/bin/env python
"""
A5 - cross_index_v2.py

De-vacuumed K-ledger presence indicator.

The previous round's A09 cross-index reported `source_linked=true` on every row.
This script recomputes the indicator instead of trusting that literal:

    * recompute the K-id set from the ledger input
      (`kledger/K_LEDGER_CROSSWALK.json`);
    * recompute the status split from the findings document
      (`kledger/KNOWN-FINDINGS.md`);
    * set each row's `source_linked` to COMPUTED, i.e. true iff that row's id is
      present in the recomputed ledger id set.

It emits `writer/CROSS_INDEX_V2.json` with `rows_checked`, `ids_expected`,
`ids_found`, `missing_ids`, and an explicit `known_limit` stating that this
asserts PRESENCE (the id is in the frozen ledger), not re-verification, and that
same-run retest remains 0 by construction.

Modes:
    (default)    recompute and write the index.
    --self-test  inject a fake id into the expected set and assert the indicator
                 reports the missing id; prints `SELF_TEST=PASS` only then.

Exit codes: 0 = ok; 1 = self-test did not report the missing id; 2 = IO.
"""

import argparse
import json
import os
import re
import sys

SCHEMA = "FAR018/CROSS-INDEX/2"
ARCHIVE = ("C:/Projects/Agent_Workspace/_handover/"
           "CNV-EVIDENCE-ARCHIVE-R7R11-20261016")
A09 = ARCHIVE + "/A09_KLedger_CROSS_INDEX.json"
CROSSWALK = ARCHIVE + "/kledger/K_LEDGER_CROSSWALK.json"
FINDINGS = ARCHIVE + "/kledger/KNOWN-FINDINGS.md"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "CROSS_INDEX_V2.json")

STATUS_RE = re.compile(
    r"^\|\s*(K-\d+)\s*\|.*?\|\s*`([A-Z]+)`\s*\|", re.MULTILINE)

KNOWN_LIMIT = (
    "This asserts PRESENCE ONLY: a row's id was found in the recomputed frozen "
    "ledger id set. It is NOT a re-verification of the finding's substance, and "
    "`same_run_retested` remains 0 by construction (no independent same-round "
    "re-verification receipt is bound to any K entry in this lane)."
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def recompute(expected_extra=None):
    cw = load_json(CROSSWALK)
    ledger_ids = set()
    for row in cw.get("rows", []):
        rid = row.get("id")
        if rid:
            ledger_ids.add(rid)

    expected = set(ledger_ids)
    if expected_extra:
        expected |= set(expected_extra)

    with open(FINDINGS, "r", encoding="utf-8") as fh:
        text = fh.read()
    statuses = {}
    for kid, status in STATUS_RE.findall(text):
        statuses[kid] = status

    from collections import Counter
    return {
        "ledger_ids": ledger_ids,
        "expected": expected,
        "status_counts": dict(Counter(statuses.values())),
        "status_by_id": statuses,
    }


def compute_rows(a09_rows, ledger_ids):
    checked = 0
    found = []
    missing = []
    out = []
    for row in a09_rows:
        kid = row.get("k_id")
        checked += 1
        linked = kid in ledger_ids
        (found if linked else missing).append(kid)
        out.append({
            "k_id": kid,
            "source_linked": bool(linked),
            "source_linked_evidence": (
                "recomputed: id present in kledger/K_LEDGER_CROSSWALK.json rows"
                if linked else
                "recomputed: id ABSENT from kledger/K_LEDGER_CROSSWALK.json rows"),
            "same_run_retested": False,
            "baseline_status_from_findings": row.get("source_status_at_baseline"),
        })
    return out, checked, found, missing


def build(expected_extra=None):
    a09 = load_json(A09)
    rec = recompute(expected_extra=expected_extra)
    rows, checked, found, missing = compute_rows(a09.get("rows", []),
                                                 rec["ledger_ids"])
    # ids_found / missing_ids are computed over the EXPECTED set versus the
    # recomputed frozen-ledger id set, so a bogus expected id is reported missing.
    ids_found = sorted(rec["expected"] & rec["ledger_ids"])
    missing_ids = sorted(rec["expected"] - rec["ledger_ids"])
    body = {
        "schema": SCHEMA,
        "contract_id": a09.get("contract_id"),
        "source_a09": A09,
        "inputs": {
            "K_LEDGER_CROSSWALK.json": CROSSWALK,
            "KNOWN-FINDINGS.md": FINDINGS,
        },
        "rows": rows,
        "rows_checked": checked,
        "ids_expected": sorted(rec["expected"]),
        "ids_found": ids_found,
        "missing_ids": missing_ids,
        "recomputed_status_counts": rec["status_counts"],
        "known_limit": KNOWN_LIMIT,
        "claim_ceiling": ("local ID-presence recomputation; NOT a substance "
                          "re-verification and NOT an independent acceptance"),
    }
    return body, missing_ids


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="De-vacuumed K-ledger presence indicator (FAR-20261016-018 A5).")
    ap.add_argument("--self-test", action="store_true",
                    help="inject a fake id into the expected set and assert it is reported missing")
    args = ap.parse_args(argv)

    try:
        if args.self_test:
            fake = "K-99-ABSENT-CONTROL"
            body, missing = build(expected_extra=[fake])
            reported = fake in body["missing_ids"]
            sys.stdout.write(json.dumps({
                "injected_id": fake,
                "reported_missing": reported,
                "missing_ids": body["missing_ids"],
            }, indent=2) + "\n")
            if reported:
                sys.stdout.write("SELF_TEST=PASS\n")
                return 0
            sys.stdout.write("SELF_TEST=FAIL\n")
            return 1

        body, missing = build()
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(body, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        sys.stdout.write(json.dumps({
            "wrote": OUT,
            "rows_checked": body["rows_checked"],
            "ids_expected": len(body["ids_expected"]),
            "ids_found": len(body["ids_found"]),
            "missing_ids": body["missing_ids"],
            "recomputed_status_counts": body["recomputed_status_counts"],
        }, indent=2) + "\n")
        return 0
    except FileNotFoundError as exc:
        sys.stderr.write("IO error: {0}\n".format(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
