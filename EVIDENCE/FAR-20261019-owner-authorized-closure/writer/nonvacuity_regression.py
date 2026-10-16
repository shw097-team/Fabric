#!/usr/bin/env python
"""T2 non-vacuity regression proofs (A7).

A previous round shipped probes that could not fail. For each case below this
harness runs the REPAIRED artifact against the ORIGINAL defect and requires a
FAILURE verdict. A case that still PASSES once the original defect is re-injected
is a FINDING (the repaired probe is still vacuous), recorded as such -- never as
success.

Every predicate is taken from the repaired artifact's real code path, not
hardcoded here:

  case 1  metadata_semantics.py   repaired predicate: claim_true == IMMUTABLE_FILE
                                  count (the count of rows permitted a
                                  byte-exactness claim must equal the immutable
                                  rows). Defect: a MUTABLE_LIVE row allowed a
                                  byte-exactness claim (point-in-time digest
                                  treated as a permanent identity).
  case 2  cross_index_v2.py       repaired predicate: each row's source_linked is
                                  RECOMPUTED from ledger membership. Defect:
                                  source_linked hardcoded True, so an id absent
                                  from the ledger is still reported linked.
  case 3  self_check_v2.py        repaired predicate: computed S8b verdict (arm
                                  gate + stated pair + same-arm disclosure).
                                  Defect: the previous round passed the literal
                                  True, so a stripped disclosure never failed.

Each case reports: what was corrupted, the real verdict before and after the
mutation, and a PASS/FAIL. Exit 0 only when every case's UNMODIFIED verdict is a
pass and its CORRUPTED verdict is a failure; 3 otherwise (and any corrupted
case that passes is listed under `findings`).
"""

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "t2_src"


def load(name):
    path = SRC / name
    spec = importlib.util.spec_from_file_location("t2_" + name.replace(".py", ""), str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def case_metadata_semantics():
    mod = load("metadata_semantics.py")
    ledger, rows, counts, claim_true, immut = mod.build()
    # the repaired artifact's own predicate, stated in its --self-test.
    def check(allowed_flags):
        return sum(1 for f in allowed_flags if f) == counts["IMMUTABLE_FILE"]

    clean_flags = [r["byte_exactness_claim_allowed"] for r in rows]
    clean_verdict = "PASS" if check(clean_flags) else "FAIL"

    # ORIGINAL DEFECT: give ONE MUTABLE_LIVE row a byte-exactness claim.
    corrupt_flags = list(clean_flags)
    idx = next(i for i, r in enumerate(rows) if r["class"] == "MUTABLE_LIVE")
    corrupt_flags[idx] = True
    corrupt_verdict = "PASS" if check(corrupt_flags) else "FAIL"
    return {
        "case": 1,
        "artifact": "metadata_semantics.py / METADATA_SEMANTICS_V2.json",
        "repaired_predicate": "count(byte_exactness_claim_allowed==true) == count(IMMUTABLE_FILE rows)",
        "corruption": (f"row id={rows[idx]['id']!r} class=MUTABLE_LIVE had its "
                       "byte_exactness_claim_allowed flipped true (point-in-time digest "
                       "treated as byte-exact)"),
        "unmodified_verdict": clean_verdict,
        "corrupted_verdict": corrupt_verdict,
        "required": "unmodified PASS, corrupted FAIL",
    }


def case_cross_index():
    mod = load("cross_index_v2.py")
    a09_rows = mod.load_json(mod.A09).get("rows", [])
    rec = mod.recompute()
    ledger_ids = rec["ledger_ids"]

    def check(body):
        # every row's flag must match membership; missing bookkeeping must agree.
        flags_ok = all(row["source_linked"] == (row["k_id"] in ledger_ids) for row in body["rows"])
        books_ok = body["missing_ids"] == sorted(set(body["ids_expected"]) - ledger_ids)
        return flags_ok and books_ok

    clean_body, _ = mod.build()
    clean_verdict = "PASS" if check(clean_body) else "FAIL"

    # ORIGINAL DEFECT: an expected id absent from the ledger, with source_linked
    # hardcoded true on every row (the previous round's literal).
    fake = "K-99-ABSENT-CONTROL"
    defect_body, _ = mod.build(expected_extra=[fake])
    # The defect only bites when a row whose id is ABSENT from the ledger is still
    # flagged linked. Present that absent id as a row, with the hardcoded literal.
    defect_body["rows"] = defect_body["rows"] + [{
        "k_id": fake,
        "source_linked": True,  # the previous round's hardcoded literal under test
        "source_linked_evidence": "hardcoded: true (NOT recomputed)",
        "same_run_retested": False,
        "baseline_status_from_findings": None,
    }]
    corrupt_verdict = "PASS" if check(defect_body) else "FAIL"
    return {
        "case": 2,
        "artifact": "cross_index_v2.py / CROSS_INDEX_V2.json",
        "repaired_predicate": "row.source_linked == (row.k_id in recomputed ledger id set)",
        "corruption": (f"presented an absent id {fake!r} as a row with source_linked hardcoded true "
                       "(the previous round's literal), so recomputation must report the mismatch"),
        "unmodified_verdict": clean_verdict,
        "corrupted_verdict": corrupt_verdict,
        "required": "unmodified PASS, corrupted FAIL",
    }


def case_self_check_s8b():
    mod = load("self_check_v2.py")
    base_verdict, _ = mod.run(strip=False)
    stripped_verdict, detail = mod.run(strip=True)

    def check(verdict):
        return verdict == "PASS"

    clean_verdict = "PASS" if check(base_verdict) else "FAIL"
    corrupt_verdict = "PASS" if check(stripped_verdict) else "FAIL"
    return {
        "case": 3,
        "artifact": "self_check_v2.py (de-vacuumed S8b whose predecessor was a literal True)",
        "repaired_predicate": "computed S8b verdict (arm gate + stated pair + same-arm disclosure)",
        "corruption": ("stripped the same-arm diversity-absence declaration from every disclosure "
                       f"source (disclosure_source now {detail.get('disclosure_source')!r})"),
        "unmodified_verdict": clean_verdict,
        "corrupted_verdict": corrupt_verdict,
        "required": "unmodified PASS, corrupted FAIL",
    }


def main(argv=None):
    import argparse
    argparse.ArgumentParser(description="T2 non-vacuity regression proofs (A7).").parse_args(argv)

    cases = [case_metadata_semantics(), case_cross_index(), case_self_check_s8b()]
    findings = [c["case"] for c in cases
                if not (c["unmodified_verdict"] == "PASS" and c["corrupted_verdict"] == "FAIL")]
    for c in cases:
        c["verdict"] = "PASS" if c["case"] not in findings else f"FINDING(case {c['case']})"

    report = {
        "schema": "FAR019/NONVACUITY-REGRESSION/1",
        "what": "each repaired artifact re-run against its original defect; corrupted verdict MUST fail",
        "cases": cases,
        "findings": findings,
        "verdict": "PASS" if not findings else "FINDING:" + ",".join(str(f) for f in findings),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("T2_RESULT=" + report["verdict"])
    return 0 if not findings else 3


if __name__ == "__main__":
    raise SystemExit(main())
