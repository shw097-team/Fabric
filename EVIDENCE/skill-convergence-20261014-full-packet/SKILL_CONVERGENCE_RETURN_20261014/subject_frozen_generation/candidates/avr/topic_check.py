#!/usr/bin/env python
"""WO-SKCV-20261014-AVR phase 2: verifier for topic_batch_1 groups ONLY.

Checks, for the two theme groups recorded in topic_batch_1.json:
  * each absorbed digest is recomputed from the topic file bytes,
  * every path linked from skill/SKILL.md still resolves (no dangling link),
  * segment order / identity in each topic file matches the manifest,
and refuses with a typed error code (single-purpose exit) on a missing,
duplicated, reordered or mutated segment, or a dangling link. Fail-closed:
an absent/empty input is INCONCLUSIVE, never a pass. It never accepts an
out-of-enum verdict.

Commands: check | negative. Reads only; writes nothing.
Typed codes: OK, MANIFEST_MISSING, INCONCLUSIVE, MISSING_SEGMENT,
DUPLICATED_SEGMENT, REORDERED_SEGMENT, MUTATED_SEGMENT, SEGMENT_LENGTH,
STUB_MISSING, STUB_MISMATCH, DANGLING_LINK, TOPIC_FILE_MISSING.
"""
import argparse, hashlib, json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAIN_REL = "skill/SKILL.md"
BATCH_REL = "topic_batch_1.json"

CODE_EXIT = {
    "OK": 0, "MISSING_SEGMENT": 10, "DUPLICATED_SEGMENT": 11,
    "REORDERED_SEGMENT": 12, "MUTATED_SEGMENT": 13, "SEGMENT_LENGTH": 14,
    "STUB_MISSING": 15, "STUB_MISMATCH": 16, "DANGLING_LINK": 17,
    "TOPIC_FILE_MISSING": 18, "MANIFEST_MISSING": 19, "INCONCLUSIVE": 20,
}
SEGMENT_RE = re.compile(rb"===== SKCV-TOPIC-SEGMENT (\d+) BEGIN path=([^ ]+) offset=(\d+) bytes=(\d+) sha256=([0-9a-f]{64}) =====")
LINK_RE = re.compile(rb"`([A-Za-z0-9._/-]+\.(?:md|py|json))`")

sha = lambda b: hashlib.sha256(b).hexdigest()


class Refuse(Exception):
    def __init__(self, code, detail=""):
        super().__init__(code)
        self.code, self.detail = code, detail


def default_loader():
    manifest = (BASE / BATCH_REL)
    if not manifest.exists():
        raise Refuse("MANIFEST_MISSING", BATCH_REL)
    m = json.loads(manifest.read_text(encoding="utf-8"))
    files = {}
    for a in m["absorbed"]:
        p = BASE / a["topic_file"]
        if p.exists():
            files[a["topic_file"]] = p.read_bytes()
    if (BASE / MAIN_REL).exists():
        files[MAIN_REL] = (BASE / MAIN_REL).read_bytes()
    stubs = {}
    for a in m["absorbed"]:
        p = BASE / a["stub_path"]
        stubs[a["stub_path"]] = p.read_bytes() if p.exists() else None
    return m, files, stubs


def check(m, files, stubs):
    absorbed = m.get("absorbed") or []
    if not absorbed:
        raise Refuse("INCONCLUSIVE", "no segments in manifest")
    seen_paths, seen_slots = {}, set()
    for a in absorbed:
        path = a["absorbed_path"]
        if path in seen_paths:
            raise Refuse("DUPLICATED_SEGMENT", path)
        seen_paths[path] = a
        slot = (a["owned_by_theme"], a["segment_index"])
        if slot in seen_slots:
            raise Refuse("DUPLICATED_SEGMENT", "%s#%s" % slot)
        seen_slots.add(slot)
        tf = a["topic_file"]
        if tf not in files:
            raise Refuse("TOPIC_FILE_MISSING", tf)
        blob = files[tf]
        if a["payload_byte_end"] > len(blob):
            raise Refuse("MISSING_SEGMENT", "%s truncated (%d > %d)" % (path, a["payload_byte_end"], len(blob)))
        payload = blob[a["byte_offset"]:a["payload_byte_end"]]
        if len(payload) != a["bytes"]:
            raise Refuse("SEGMENT_LENGTH", "%s %d != %d" % (path, len(payload), a["bytes"]))
        if sha(payload) != a["sha256"]:
            raise Refuse("MUTATED_SEGMENT", path)
        # identity/order: the segment header immediately before the payload must
        # name this path, this index and this offset.
        head = blob.rfind(b"===== SKCV-TOPIC-SEGMENT", 0, a["byte_offset"])
        if head < 0:
            raise Refuse("REORDERED_SEGMENT", "%s no header" % path)
        line_end = blob.find(b"\r\n", head)
        header = blob[head:line_end]
        h = SEGMENT_RE.match(header)
        if (not h or h.group(2).decode("ascii") != path or int(h.group(1)) != a["segment_index"]
                or int(h.group(4)) != a["bytes"] or h.group(5).decode() != a["sha256"]):
            raise Refuse("REORDERED_SEGMENT", "%s header mismatch" % path)
        if int(h.group(3)) != a["byte_offset"]:
            raise Refuse("REORDERED_SEGMENT", "%s offset %s != %s" % (path, h.group(3).decode(), a["byte_offset"]))
    # order within each topic: segment_index ascending by byte_offset
    by_theme = {}
    for a in absorbed:
        by_theme.setdefault(a["owned_by_theme"], []).append(a)
    for theme, entries in by_theme.items():
        ordered = sorted(entries, key=lambda x: x["byte_offset"])
        if [x["segment_index"] for x in ordered] != sorted(x["segment_index"] for x in ordered):
            raise Refuse("REORDERED_SEGMENT", theme)
    # stubs: each absorbed original is a visible pointer stub
    tmpl = m["stub_template"]
    for a in absorbed:
        sp = a["stub_path"]
        want = tmpl.format(theme=a["owned_by_theme"], offset=a["byte_offset"], sha256=a["sha256"]).encode("utf-8")
        got = stubs.get(sp)
        if got is None:
            raise Refuse("STUB_MISSING", sp)
        if got != want:
            raise Refuse("STUB_MISMATCH", sp)
    # every path linked from skill/SKILL.md resolves on disk; no dangling link
    main = files.get(MAIN_REL)
    if main is None:
        raise Refuse("INCONCLUSIVE", "skill/SKILL.md unreadable")
    linked = sorted({m.group(1).decode("ascii") for m in LINK_RE.finditer(main)})
    if not linked:
        raise Refuse("INCONCLUSIVE", "no links parsed from skill/SKILL.md")
    for rel in linked:
        target = (BASE / "skill" / rel) if not rel.startswith("skill/") else (BASE / rel)
        if not target.exists():
            raise Refuse("DANGLING_LINK", rel)
    return dict(code="OK", checked_segments=len(absorbed), linked_paths=len(linked),
                themes=sorted(by_theme), stub_count=len(absorbed))


def cmd_check(_a):
    try:
        r = check(*default_loader())
    except Refuse as e:
        print("REFUSE %s: %s" % (e.code, e.detail))
        return CODE_EXIT[e.code]
    print(json.dumps(r, indent=2))
    return 0


def negative_cases():
    m, files, stubs = default_loader()
    cases = []

    def clone():
        return (json.loads(json.dumps(m)), dict(files), dict(stubs))

    mm, ff, ss = clone()                       # missing segment (topic truncated)
    a = mm["absorbed"][0]
    ff[a["topic_file"]] = ff[a["topic_file"]][:a["payload_byte_end"] - 3]
    cases.append(("missing_segment", (mm, ff, ss), "MISSING_SEGMENT"))

    mm, ff, ss = clone()                       # duplicated segment (same path twice)
    mm["absorbed"].append(dict(mm["absorbed"][0]))
    cases.append(("duplicated_segment", (mm, ff, ss), "DUPLICATED_SEGMENT"))

    mm, ff, ss = clone()                       # reordered segment (indices swapped)
    theme = mm["absorbed"][0]["owned_by_theme"]
    same = [a for a in mm["absorbed"] if a["owned_by_theme"] == theme]
    same[0]["segment_index"], same[-1]["segment_index"] = same[-1]["segment_index"], same[0]["segment_index"]
    cases.append(("reordered_segment", (mm, ff, ss), "REORDERED_SEGMENT"))

    mm, ff, ss = clone()                       # mutated segment (flip one payload byte)
    a = mm["absorbed"][0]
    b = bytearray(ff[a["topic_file"]]); b[a["byte_offset"] + 1] ^= 0x01
    ff[a["topic_file"]] = bytes(b)
    cases.append(("mutated_segment", (mm, ff, ss), "MUTATED_SEGMENT"))

    mm, ff, ss = clone()                       # dangling link (main doc points nowhere)
    ff[MAIN_REL] = ff[MAIN_REL] + b"\r\n`references/does-not-exist-phase2.md`\r\n"
    cases.append(("dangling_link", (mm, ff, ss), "DANGLING_LINK"))

    out = []
    for tag, args, want in cases:
        try:
            check(*args)
            out.append(dict(case=tag, refused=False, code="OK", expected=want, pass_=False))
        except Refuse as e:
            out.append(dict(case=tag, refused=True, code=e.code, expected=want, pass_=e.code == want))
    return out


def cmd_negative(_a):
    results = negative_cases()
    for r in results:
        print("NEG %s: refused=%s code=%s expected=%s -> %s"
              % (r["case"], r["refused"], r["code"], r["expected"], "OK" if r["pass_"] else "FAIL"))
    return 0 if all(r["pass_"] for r in results) else 4


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["check", "negative"])
    a = ap.parse_args()
    return {"check": cmd_check, "negative": cmd_negative}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
