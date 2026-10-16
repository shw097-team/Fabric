#!/usr/bin/env python
"""
A3 - regen_entry_map.py

PARTIAL reconstruction of the Hermes skill's absent index file.

The skill `hgk-governed-execution` has no `entry_map.json`; its payload was moved
into four topic files under `references/topics/`, and each move left a
`SKCV-POINTER` line in the source `references/*.md` naming the destination,
byte offset, length and sha256 of the moved slice. This script:

    1. locates the skill dir by the well-known Hermes path (SKILL.md present);
    2. parses every `SKCV-POINTER` line under `references/*.md`;
    3. resolves each target relative to the skill dir (stripping a leading
       `skill/` prefix if present);
    4. verifies `sha256(bytes[offset:offset+length])` against the claimed digest;
    5. writes `writer/entry_map.json` with every pointer record, the destination
       topic files, and an explicit PARTIAL-`coverage` block.

Any pointer that does NOT verify ABORTS with a non-zero exit and a typed error;
an index containing an unverified pointer is never written.

Modes:
    (default)    parse, verify, write `writer/entry_map.json`.
    --self-test  perturb one recorded digest in memory and assert the verifier
                 ABORTS; prints `SELF_TEST=PASS` only when the abort happens.

Exit codes: 0 = verified (default) / abort detected (--self-test);
            1 = self-test did not detect the mutation; 3 = typed verify failure;
            4 = typed parse/locate failure; 2 = IO.
"""

import argparse
import hashlib
import json
import os
import re
import sys

SCHEMA = "FAR018/ENTRY-MAP/1"
SKILL_DIR = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
             "LocalCache/Local/hermes/skills/software-development/hgk-governed-execution")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_map.json")

POINTER_RE = re.compile(
    r"SKCV-POINTER\s+(?P<label>\S+?):\s*payload moved verbatim to\s+"
    r"(?P<target>\S+)\s+byte offset\s+(?P<offset>\d+)\s+length\s+(?P<length>\d+)\s+"
    r"sha256\s+(?P<sha>[0-9a-fA-F]{64})"
)


class PointerParseError(Exception):
    pass


class PointerVerifyError(Exception):
    pass


def locate_skill():
    if os.path.isfile(os.path.join(SKILL_DIR, "SKILL.md")):
        return SKILL_DIR
    raise PointerParseError("skill dir not found (no SKILL.md): {0}".format(SKILL_DIR))


def find_pointer_lines(skill_dir):
    refs = os.path.join(skill_dir, "references")
    records = []
    for name in sorted(os.listdir(refs)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(refs, name)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                if "SKCV-POINTER" in line:
                    m = POINTER_RE.search(line)
                    if not m:
                        raise PointerParseError(
                            "unparseable SKCV-POINTER at {0}:{1}".format(name, lineno))
                    records.append({
                        "pointer_file": "references/" + name,
                        "pointer_line": lineno,
                        "label": m.group("label"),
                        "target_raw": m.group("target"),
                        "offset": int(m.group("offset")),
                        "length": int(m.group("length")),
                        "claimed_sha256": m.group("sha").lower(),
                    })
    return records


def resolve_target(skill_dir, target_raw):
    t = target_raw
    if t.startswith("skill/"):
        t = t[len("skill/"):]
    return os.path.join(skill_dir, t.replace("/", os.sep)), t


def verify_records(skill_dir, records, perturb_index=None):
    """Resolve + verify every record. Raises PointerVerifyError on first failure."""
    out = []
    for idx, rec in enumerate(records):
        path, rel = resolve_target(skill_dir, rec["target_raw"])
        if not os.path.isfile(path):
            raise PointerVerifyError(
                "target missing for {0} -> {1}".format(rec["pointer_file"], rel))
        with open(path, "rb") as fh:
            blob = fh.read()
        sl = blob[rec["offset"]:rec["offset"] + rec["length"]]
        actual = hashlib.sha256(sl).hexdigest()
        claimed = rec["claimed_sha256"]
        if perturb_index == idx:
            claimed = ("0" * 64)
        ok = (len(sl) == rec["length"]) and (actual == claimed)
        row = {
            "pointer_file": rec["pointer_file"],
            "pointer_line": rec["pointer_line"],
            "label": rec["label"],
            "target": rel,
            "offset": rec["offset"],
            "length": rec["length"],
            "slice_len_actual": len(sl),
            "claimed_sha256": claimed,
            "actual_sha256": actual,
            "verdict": "VERIFIED" if ok else "MISMATCH",
        }
        out.append(row)
        if not ok:
            raise PointerVerifyError(
                "pointer failed verification: {0} -> {1} offset={2} length={3} "
                "claimed={4} actual={5}".format(
                    rec["pointer_file"], rel, rec["offset"], rec["length"],
                    claimed, actual))
    return out


def destination_topic_files(skill_dir):
    topics = os.path.join(skill_dir, "references", "topics")
    if not os.path.isdir(topics):
        return []
    return ["references/topics/" + n for n in sorted(os.listdir(topics))]


COVERAGE = {
    "status": "PARTIAL",
    "basis": ("reconstructed only from `SKCV-POINTER` lines discovered under "
              "references/*.md; the original index file is absent"),
    "covers": [
        "pointer_file", "target", "offset", "length", "claimed_sha256",
        "actual_sha256", "verdict", "destination topic files",
    ],
    "does_not_cover": [
        "the original index's full field set: per-topic titles/summaries",
        "topic-to-source provenance beyond the byte-slice pointer",
        "the skill's ordering/priority metadata for each entry",
        "any entry that was never emitted as a SKCV-POINTER move record",
        "SKCV-TOPIC-ENTRY lines inside topic files (a different record type; "
        "their slices resolve against the topic file itself, not a source file)",
    ],
    "note": ("Presence of a verified pointer proves the byte slice moved verbatim; "
             "it is not a claim that the reconstructed index is complete."),
}


def build(skill_dir, perturb_index=None):
    records = find_pointer_lines(skill_dir)
    verified = verify_records(skill_dir, records, perturb_index=perturb_index)
    return {
        "schema": SCHEMA,
        "skill_path": skill_dir.replace("\\", "/"),
        "generation_method": ("parse every SKCV-POINTER line under references/*.md; "
                              "resolve target relative to the skill dir (strip leading "
                              "`skill/`); verify sha256(bytes[offset:offset+length])"),
        "pointers": verified,
        "destination_topic_files": destination_topic_files(skill_dir),
        "coverage": COVERAGE,
        "claim_ceiling": ("byte-slice move verification only; NOT an independent "
                          "acceptance and NOT a claim the original index is restored"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="PARTIAL skill index reconstruction (FAR-20261016-018 A3).")
    ap.add_argument("--self-test", action="store_true",
                    help="perturb one recorded digest and assert the verifier ABORTS")
    args = ap.parse_args(argv)

    try:
        skill_dir = locate_skill()
    except PointerParseError as exc:
        sys.stderr.write("PointerParseError: {0}\n".format(exc))
        return 4

    if args.self_test:
        try:
            build(skill_dir, perturb_index=0)
        except PointerVerifyError as exc:
            sys.stderr.write("PointerVerifyError (expected): {0}\n".format(exc))
            sys.stdout.write("SELF_TEST=PASS\n")
            return 0
        sys.stdout.write("SELF_TEST=FAIL\n")
        return 1

    try:
        index = build(skill_dir)
    except PointerParseError as exc:
        sys.stderr.write("PointerParseError: {0}\n".format(exc))
        return 4
    except PointerVerifyError as exc:
        sys.stderr.write("PointerVerifyError: {0}\n".format(exc))
        return 3

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    sys.stdout.write(json.dumps({
        "wrote": OUT,
        "pointers_verified": len(index["pointers"]),
        "pointers_total": len(index["pointers"]),
        "destination_topic_files": index["destination_topic_files"],
        "coverage_status": index["coverage"]["status"],
    }, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
