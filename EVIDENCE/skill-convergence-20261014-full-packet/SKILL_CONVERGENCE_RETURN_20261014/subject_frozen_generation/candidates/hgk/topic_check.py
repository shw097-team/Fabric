#!/usr/bin/env python3
"""SKCV-HGK reference-consolidation checker (phase 3: batch 1 + batch 2).

Verifies, from raw bytes only, that for every topic batch:
  * every absorbed file's payload is present verbatim inside the topic file and
    recomputes to the recorded sha256;
  * every absorbed / stub path named in the batch still resolves on disk;
  * the one-line pointer stub at each absorbed path exists and points back at
    the topic file with the recorded byte offset;
  * every path named in skill/SKILL.md still resolves.

Refuses with a distinct typed error code for a missing / duplicated /
reordered / mutated segment (and for stub / name / topic problems).
`--topic` overrides the topic file under test (used by the negative probes);
the topic-level digest/length assertion is skipped only in that override mode.
"""

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
BATCHES = ["topic_batch_1.json", "topic_batch_2.json"]
SKILL_REL = "skill/SKILL.md"

# exit codes
EXIT_OK = 0
EXIT_SEGMENT_MISSING = 11
EXIT_SEGMENT_DUPLICATED = 12
EXIT_SEGMENT_REORDERED = 13
EXIT_SEGMENT_MUTATED = 14
EXIT_STUB = 20
EXIT_NAME = 21
EXIT_TOPIC = 22
EXIT_INPUT = 23

ERR_TOPIC_MISSING = "ERR_SKCV_TOPIC_MISSING"
ERR_BATCH_MISSING = "ERR_SKCV_BATCH_MISSING"
ERR_SEGMENT_MISSING = "ERR_SKCV_SEGMENT_MISSING"
ERR_SEGMENT_DUPLICATED = "ERR_SKCV_SEGMENT_DUPLICATED"
ERR_SEGMENT_REORDERED = "ERR_SKCV_SEGMENT_REORDERED"
ERR_SEGMENT_MUTATED = "ERR_SKCV_SEGMENT_MUTATED"
ERR_SEGMENT_DIGEST = "ERR_SKCV_SEGMENT_DIGEST"
ERR_STUB_MISSING = "ERR_SKCV_STUB_MISSING"
ERR_STUB_MISMATCH = "ERR_SKCV_STUB_MISMATCH"
ERR_SKILL_NAME_UNRESOLVED = "ERR_SKCV_SKILL_NAME_UNRESOLVED"
OK = "OK"

HEADER_RE = re.compile(
    rb"<!-- SKCV-TOPIC-ENTRY path=(\S+) offset=(\d+) length=(\d+) "
    rb"sha256=([0-9a-f]{64}) -->\n"
)
STUB_RE = re.compile(rb"payload moved verbatim to (\S+) byte offset (\d+)")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


class Refusal(Exception):
    def __init__(self, code, exit_code, detail):
        super().__init__(code)
        self.code = code
        self.exit_code = exit_code
        self.detail = detail


def parse_blocks(topic):
    blocks = []
    for m in HEADER_RE.finditer(topic):
        path = m.group(1).decode("utf-8")
        off = int(m.group(2))
        length = int(m.group(3))
        declared = m.group(4).decode("ascii")
        phys = m.end()  # payload starts right after the header line
        payload = topic[phys:phys + length]
        blocks.append({
            "path": path,
            "offset": off,
            "length": length,
            "declared_sha": declared,
            "phys_offset": phys,
            "header_start": m.start(),
            "payload": payload,
        })
    return blocks


def check_segments(topic, batch):
    expected = batch["absorbed"]
    exp_paths = [e["absorbed_path"] for e in expected]
    exp_by_path = {e["absorbed_path"]: e for e in expected}

    blocks = parse_blocks(topic)
    got_paths = [b["path"] for b in blocks]

    # -- duplicates -----------------------------------------------------------
    seen = {}
    for b in blocks:
        seen[b["path"]] = seen.get(b["path"], 0) + 1
    dups = sorted(p for p, n in seen.items() if n > 1)
    if dups:
        raise Refusal(ERR_SEGMENT_DUPLICATED, EXIT_SEGMENT_DUPLICATED,
                      "duplicated segment(s): %s" % ", ".join(dups))

    # -- missing --------------------------------------------------------------
    absent = [p for p in exp_paths if p not in seen]
    unexpected = [p for p in got_paths if p not in exp_by_path]
    if absent or unexpected or len(blocks) != len(expected):
        detail = "missing=%s unexpected=%s blocks=%d expected=%d" % (
            absent, unexpected, len(blocks), len(expected))
        raise Refusal(ERR_SEGMENT_MISSING, EXIT_SEGMENT_MISSING, detail)

    # -- reordered (physical block order vs declared order) -------------------
    if got_paths != exp_paths:
        raise Refusal(ERR_SEGMENT_REORDERED, EXIT_SEGMENT_REORDERED,
                      "physical order=%s expected=%s" % (got_paths, exp_paths))

    # -- per-segment offset / length / content --------------------------------
    for b in blocks:
        e = exp_by_path[b["path"]]
        if b["offset"] != b["phys_offset"] or b["offset"] != e["byte_offset"]:
            raise Refusal(ERR_SEGMENT_REORDERED, EXIT_SEGMENT_REORDERED,
                          "declared offset %d != physical %d (expected %d) for %s"
                          % (b["offset"], b["phys_offset"], e["byte_offset"], b["path"]))
        if b["length"] != e["bytes"] or len(b["payload"]) != e["bytes"]:
            raise Refusal(ERR_SEGMENT_MISSING, EXIT_SEGMENT_MISSING,
                          "length mismatch for %s: declared %d expected %d actual %d"
                          % (b["path"], b["length"], e["bytes"], len(b["payload"])))

    # content digest: recompute each absorbed digest out of the topic file
    for b in blocks:
        e = exp_by_path[b["path"]]
        d = sha256(b["payload"])
        if d != e["sha256"] or d != b["declared_sha"]:
            raise Refusal(ERR_SEGMENT_MUTATED, EXIT_SEGMENT_MUTATED,
                          "digest mismatch for %s: recomputed %s expected %s declared %s"
                          % (b["path"], d, e["sha256"], b["declared_sha"]))

    return blocks


def check_skill_names(skill_text, root):
    tokens = set()
    for m in re.finditer(r"`([A-Za-z0-9_./\\-]+)`", skill_text):
        t = m.group(1)
        if t.startswith("references/") or t == "entry_map.json":
            tokens.add(t)
    unresolved = []
    for t in sorted(tokens):
        cands = [os.path.join(root, *t.split("/")),
                 os.path.join(root, "skill", *t.split("/"))]
        if not any(os.path.isfile(c) for c in cands):
            unresolved.append(t)
    if unresolved:
        raise Refusal(ERR_SKILL_NAME_UNRESOLVED, EXIT_NAME,
                      "unresolved name(s) in skill/SKILL.md: %s" % ", ".join(unresolved))
    return sorted(tokens)


def check_stubs(batch, topic_rel, root):
    for e in batch["absorbed"]:
        # every named path must still resolve on disk (it is now a stub)
        for key in ("absorbed_path", "stub_path"):
            named = e[key]
            if not os.path.isfile(os.path.join(root, *named.split("/"))):
                raise Refusal(ERR_STUB_MISSING, EXIT_STUB,
                              "named path does not resolve: %s (%s)" % (named, key))
        sp = os.path.join(root, *e["stub_path"].split("/"))
        if not os.path.isfile(sp):
            raise Refusal(ERR_STUB_MISSING, EXIT_STUB, "stub missing: %s" % e["stub_path"])
        with open(sp, "rb") as f:
            b = f.read()
        m = STUB_RE.search(b)
        if not m:
            raise Refusal(ERR_STUB_MISMATCH, EXIT_STUB,
                          "stub not a pointer: %s" % e["stub_path"])
        named_topic = m.group(1).decode("utf-8")
        named_off = int(m.group(2))
        if named_topic != topic_rel or named_off != e["byte_offset"]:
            raise Refusal(ERR_STUB_MISMATCH, EXIT_STUB,
                          "stub %s points to %s@%d, expected %s@%d"
                          % (e["stub_path"], named_topic, named_off,
                             topic_rel, e["byte_offset"]))


def load_batch(batch_rel, root):
    bp = os.path.join(root, *batch_rel.split("/"))
    if not os.path.isfile(bp):
        raise Refusal(ERR_BATCH_MISSING, EXIT_INPUT, "missing %s" % batch_rel)
    with open(bp, encoding="utf-8") as f:
        return json.load(f)


def check_one(batch_rel, root, topic_path=None):
    batch = load_batch(batch_rel, root)
    topic_rel = batch["topic_file"]["path"]
    tp = topic_path or os.path.join(root, *topic_rel.split("/"))
    if not os.path.isfile(tp):
        raise Refusal(ERR_TOPIC_MISSING, EXIT_TOPIC, "missing topic file %s" % tp)
    with open(tp, "rb") as f:
        topic = f.read()

    if topic_path is None:
        d = sha256(topic)
        if len(topic) != batch["topic_file"]["bytes"] or d != batch["topic_file"]["sha256"]:
            raise Refusal(ERR_SEGMENT_DIGEST, EXIT_TOPIC,
                          "topic digest/length mismatch: got %d/%s expected %d/%s"
                          % (len(topic), d, batch["topic_file"]["bytes"],
                             batch["topic_file"]["sha256"]))

    blocks = check_segments(topic, batch)
    check_stubs(batch, topic_rel, root)

    return {
        "batch": batch_rel,
        "status": OK,
        "theme": batch.get("theme"),
        "topic": topic_rel,
        "topic_bytes": len(topic),
        "topic_sha256": sha256(topic),
        "segments": len(blocks),
    }


def run(batch_rels=None, topic_path=None, root=ROOT):
    if batch_rels is None:
        batch_rels = list(BATCHES)

    # skill/SKILL.md name resolution, once per run
    sp = os.path.join(root, *SKILL_REL.split("/"))
    with open(sp, "rb") as f:
        skill_text = f.read().decode("utf-8", "surrogateescape")
    names = check_skill_names(skill_text, root)

    results = [check_one(b, root, topic_path=topic_path) for b in batch_rels]
    return {"status": OK, "batches": results, "skill_names_resolved": names}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", action="append", default=None,
                    help="batch file(s) under the repo root; default = both batches")
    ap.add_argument("--topic", default=None, help="override topic file under test")
    args = ap.parse_args(argv)
    try:
        res = run(batch_rels=args.batch, topic_path=args.topic)
    except Refusal as r:
        print(json.dumps({"status": "REFUSED", "code": r.code, "detail": r.detail}, indent=2))
        return r.exit_code
    print(json.dumps(res, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())