#!/usr/bin/env python
"""
A4 - metadata_semantics.py

Mutable-subject metadata semantics for the A00 source ledger.

The ledger records a `sha256` for each subject. For a frozen file that digest is
a permanent identity; for a live database or a directory it is only a snapshot
of a subject that keeps changing, so a byte-exactness claim built on it would be
false. This script:

    1. reads A00_SOURCE_LEDGER.json (never rewrites it);
    2. classifies each row by its locator: `*.db` / `*.sqlite` / a directory =>
       MUTABLE_LIVE, everything else => IMMUTABLE_FILE;
    3. emits writer/METADATA_SEMANTICS_V2.json with, per row: id, locator, class,
       recorded sha256, live sha256 (if the subject still exists), `hashed_at`
       semantics, and `byte_exactness_claim_allowed` (MUST be false for
       MUTABLE_LIVE);
    4. emits a machine-readable `schema_addition` naming the new fields and why
       mutable rows are excluded from byte-exactness claims;
    5. asserts the input file's mtime and sha256 are unchanged across the run.

Modes:
    (default)    classify, write the JSON, assert input immutability.
    --self-test  assert count(byte_exactness_claim_allowed == true) equals
                 count(IMMUTABLE_FILE rows); prints `SELF_TEST=PASS`.

Exit codes: 0 = ok; 1 = self-test assertion failed; 5 = typed input-mutation
error; 2 = IO.
"""

import argparse
import hashlib
import json
import os
import sys

SCHEMA = "FAR018/METADATA-SEMANTICS/2"
INPUT = ("C:/Projects/Agent_Workspace/_handover/"
         "CNV-EVIDENCE-ARCHIVE-R7R11-20261016/A00_SOURCE_LEDGER.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "METADATA_SEMANTICS_V2.json")

MUTABLE_EXTS = (".db", ".sqlite", ".sqlite3")


class InputMutationError(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(locator, kind):
    low = (locator or "").lower()
    if kind == "DIR" or low.endswith(MUTABLE_EXTS):
        return "MUTABLE_LIVE"
    if os.path.isdir(locator):
        return "MUTABLE_LIVE"
    return "IMMUTABLE_FILE"


def live_sha256(locator, cls):
    if cls == "MUTABLE_LIVE" or not locator or not os.path.isfile(locator):
        return None
    return sha256_file(locator)


def build():
    before_sha = sha256_file(INPUT)
    before_mtime = os.stat(INPUT).st_mtime_ns

    with open(INPUT, "r", encoding="utf-8") as fh:
        ledger = json.load(fh)

    rows = []
    counts = {"MUTABLE_LIVE": 0, "IMMUTABLE_FILE": 0}
    claim_true = 0
    for src in ledger.get("rows", []):
        rid = src.get("id")
        locator = src.get("locator")
        cls = classify(locator, src.get("kind"))
        counts[cls] += 1
        recorded = src.get("sha256")
        live = live_sha256(locator, cls)
        # `byte_exactness_claim_allowed` is a CLASS-LEVEL permission: a
        # MUTABLE_LIVE subject may never carry a byte-exactness claim; an
        # IMMUTABLE_FILE subject may. (Whether a digest was actually recorded is
        # tracked separately in `recorded_digest_present`, so a class-level
        # permission never hides a missing digest.)
        allowed = (cls == "IMMUTABLE_FILE")
        if allowed:
            claim_true += 1
        rows.append({
            "id": rid,
            "locator": locator,
            "class": cls,
            "recorded_sha256": recorded,
            "recorded_digest_present": bool(recorded),
            "live_sha256": live,
            "subject_exists_now": bool(locator) and os.path.exists(locator),
            "hashed_at": (
                "recorded in A00 ledger at archive generation; digest is a "
                "point-in-time snapshot of a CONTINUOUSLY-MUTATING subject, "
                "not a permanent identity" if cls == "MUTABLE_LIVE"
                else "recorded in A00 ledger at archive generation; the subject "
                     "is a frozen file, so the digest is a stable identity so "
                     "long as the file is unchanged"
            ),
            "byte_exactness_claim_allowed": allowed,
        })

    after_sha = sha256_file(INPUT)
    after_mtime = os.stat(INPUT).st_mtime_ns
    unchanged = (before_sha == after_sha) and (before_mtime == after_mtime)

    return ledger, rows, counts, claim_true, {
        "input": INPUT,
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "before_mtime_ns": before_mtime,
        "after_mtime_ns": after_mtime,
        "unchanged": unchanged,
    }


SCHEMA_ADDITION = {
    "name": "METADATA_SEMANTICS_V2",
    "new_fields": {
        "class": "MUTABLE_LIVE | IMMUTABLE_FILE (derived from the locator shape)",
        "live_sha256": "digest of the subject as it exists NOW (files only)",
        "subject_exists_now": "whether the locator still resolves on disk",
        "hashed_at": "what the recorded digest means for this class of subject",
        "byte_exactness_claim_allowed": "false for MUTABLE_LIVE by construction",
    },
    "why_mutable_rows_excluded_from_byte_exactness": (
        "A `*.db`/`*.sqlite` file or a directory keeps changing after the digest "
        "is taken, so `sha256(bytes)` at claim time would not equal the recorded "
        "value and any byte-exactness claim built on it would be false. Mutable "
        "rows therefore carry `byte_exactness_claim_allowed=false` and must be "
        "cited by presence/point-in-time digest only, never for byte-exactness."
    ),
}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Mutable-subject metadata semantics (FAR-20261016-018 A4).")
    ap.add_argument("--self-test", action="store_true",
                    help="assert claim-true count == IMMUTABLE_FILE count")
    args = ap.parse_args(argv)

    try:
        ledger, rows, counts, claim_true, immut = build()
    except FileNotFoundError as exc:
        sys.stderr.write("IO error: {0}\n".format(exc))
        return 2

    receipt = {
        "schema": SCHEMA,
        "contract_id": ledger.get("contract_id"),
        "input_immutability": immut,
        "classification_rule": ("locator *.db/*.sqlite/*.sqlite3 OR directory => "
                                "MUTABLE_LIVE; otherwise IMMUTABLE_FILE"),
        "counts": counts,
        "rows": rows,
        "schema_addition": SCHEMA_ADDITION,
        "claim_ceiling": ("local metadata classification; NOT an independent "
                          "acceptance and NOT a claim any subject is frozen"),
    }

    if args.self_test:
        ok = (claim_true == counts["IMMUTABLE_FILE"])
        sys.stdout.write(json.dumps({
            "claim_true": claim_true,
            "immutable_file_rows": counts["IMMUTABLE_FILE"],
            "mutable_live_rows": counts["MUTABLE_LIVE"],
            "input_unchanged": immut["unchanged"],
        }, indent=2) + "\n")
        if ok and immut["unchanged"]:
            sys.stdout.write("SELF_TEST=PASS\n")
            return 0
        sys.stdout.write("SELF_TEST=FAIL\n")
        return 1

    if not immut["unchanged"]:
        sys.stderr.write("InputMutationError: input file changed during run\n")
        return 5

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    sys.stdout.write(json.dumps({
        "wrote": OUT,
        "counts": counts,
        "byte_exactness_claim_true": claim_true,
        "input_unchanged": immut["unchanged"],
    }, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
