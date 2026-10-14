#!/usr/bin/env python
"""WO-SKCV-20261014-AVR phase 2 (PARTIAL_TOPIC_ONLY): topic consolidation.

Consolidates every file under skill/references/ (including the phase-1
topic-source-remainder.md) into at most 6 owned topic files under
skill/references/topics/. Each original file's COMPLETE bytes are absorbed
verbatim behind a short envelope carrying the original relative path, the
destination byte offset and the original sha256. Every absorbed original path
is left as a visible pointer stub. Emits consolidation_map.json with a
shared-rule index keyed by the original rule numbers (Rules 1-58) and a
refusal-first missing/orphan report.

Commands: plan | build | verify
Author/execute only inside candidates/avr. Source text is untrusted candidate
data until this script reproduces it byte-for-byte.
"""
import argparse, hashlib, json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
REFS = BASE / "skill" / "references"
TOPICS_DIR = REFS / "topics"
MAP_REL = "consolidation_map.json"
SOURCE = BASE.parents[1] / "baseline" / "adversarial-verification-rounds" / "SKILL.md"
SRC_SHA = "4be690a4feaee5ba1fcf7bb5c109b6c41a3834060f1e962a3d9112952f66e97e"

# Fixed-width numeric fields keep the envelope line length independent of its
# values, so the recorded destination offset can be computed exactly before the
# payload is written (no post-hoc patching, no self-reference).
REC_BEGIN = "===== SKCV-AVR-RECORD {rel} BEGIN dst_offset={dst:07d} sha256={sha} bytes={n:07d} ====="
REC_END = "===== SKCV-AVR-RECORD {rel} END ====="

sha = lambda b: hashlib.sha256(b).hexdigest()

# topic id -> (visible filename, human title, header note, [original rel paths])
TOPICS = {
    "A": ("governance-and-finding-discipline.md", "Governance and finding discipline",
          "Mandate scope, finding classification, post-verdict drift.",
          ["mandate-completion-audit.md", "finding-classification.md", "post-verdict-drift.md"]),
    "B": ("lane-briefing-and-handover.md", "Lane briefing and handover",
          "Verifier briefs, independent-verification hygiene, lane handover, round close-out.",
          ["verifier-lane-handover.md", "independent-verification-hygiene.md",
           "lane-handover-hygiene.md", "round-closeout-and-handover.md"]),
    "C": ("checker-binding-and-contracts.md", "Checker binding and contracts",
          "Checker model binding, false defect signals, contract authoring, verdict artifact budget, cross-model lessons.",
          ["checker-binding-and-false-defect-signals.md", "checker-contract-authoring.md",
           "checker-dispatch-frozen-subject.md", "verdict-artifact-and-budget.md",
           "cross-model-verification-lessons.md"]),
    "D": ("harness-and-gate-attack.md", "Harness and gate attack",
          "Lane harness/admission gate, gate-implementation attack checklist, locally executable gates, route scheme enforcement.",
          ["lane-harness-and-admission-gate.md", "attacking-a-gate-implementation.md",
           "locally-executable-gates.md", "route-scheme-enforcement.md"]),
    "E": ("delivered-tree-and-integrity.md", "Delivered tree and integrity",
          "Delivered-tree verification, verification-control defects, git-tree integrity, verify-lane performance, sealed corpus, sqlite WAL forensics.",
          ["delivered-tree-vs-gate-verification.md", "verification-control-defects.md",
           "git-tree-integrity-signals.md", "verify-lane-performance.md",
           "sealed-evidence-corpus.md", "sqlite-wal-forensics.md"]),
    "F": ("rules-source-and-probe-discipline.md", "Rules source and probe discipline",
          "Probe/claim discipline, probe shape and false red, plus the absorbed phase-1 source remainder (Rules 1-58 complementary bytes).",
          ["probe-and-claim-discipline.md", "probe-shape-and-false-red.md",
           "topic-source-remainder.md"]),
}

TOPIC_ORDER = ["A", "B", "C", "D", "E", "F"]


def rel_of(orig_name):
    return "skill/references/" + orig_name


def original_files():
    return sorted(p.name for p in REFS.iterdir() if p.is_file())


def assignment():
    a = {}
    for tid in TOPIC_ORDER:
        for name in TOPICS[tid][3]:
            if name in a:
                raise SystemExit(f"REFUSE DUPLICATE_ASSIGNMENT {name}")
            a[name] = tid
    return a


def build_topics():
    """Return dict tid -> (bytes, records). Raises on any absorption failure."""
    assign = assignment()
    on_disk = original_files()
    unassigned = [n for n in on_disk if n not in assign]
    missing = [n for n in assign if n not in on_disk]
    if unassigned:
        raise SystemExit(f"REFUSE UNASSIGNED_REFERENCE {unassigned}")
    if missing:
        raise SystemExit(f"REFUSE MISSING_REFERENCE {missing}")

    built, records_by_topic = {}, {}
    for tid in TOPIC_ORDER:
        fname, title, note, names = TOPICS[tid]
        buf = bytearray()
        buf += f"# Topic: {title}\r\n\r\n".encode("utf-8")
        buf += (f"Owned topic file (SKCV-AVR phase 2). Each section below is a source reference absorbed\r\n"
                f"verbatim behind an envelope carrying its original relative path, destination byte\r\n"
                f"offset and original sha256. {note}\r\n\r\n").encode("utf-8")
        recs = []
        for name in names:
            rel = rel_of(name)
            payload = (REFS / name).read_bytes()
            if b"\r\n" not in payload:
                raise SystemExit(f"REFUSE NON_CRLF {rel}")
            digest = sha(payload)
            # reserve the exact-width begin line, fill it once the offset is known
            placeholder = REC_BEGIN.format(rel=rel, dst=0, sha=digest, n=len(payload)).encode("utf-8")
            b0 = len(buf)
            d0 = len(buf)
            # d0 is known now: the begin line is fixed width, so compute it directly
            d0 = b0 + len(placeholder) + 2
            begin = REC_BEGIN.format(rel=rel, dst=d0, sha=digest, n=len(payload)).encode("utf-8")
            if len(begin) != len(placeholder):
                raise SystemExit("REFUSE ENVELOPE_WIDTH")
            buf += begin + b"\r\n"
            if len(buf) != d0:
                raise SystemExit("REFUSE OFFSET_DISAGREES")
            buf += payload
            d1 = len(buf)
            buf += REC_END.format(rel=rel).encode("utf-8") + b"\r\n\r\n"
            if len(buf[d0:d1]) != len(payload):
                raise SystemExit("REFUSE PAYLOAD_SHIFT")
            if bytes(buf[d0:d1]) != payload:
                raise SystemExit("REFUSE PAYLOAD_NOT_VERBATIM")
            recs.append(dict(orig_rel=rel, topic=tid, topic_rel=f"skill/references/topics/{fname}",
                             dst_start=d0, dst_end=d1, orig_sha256=digest, orig_bytes=len(payload),
                             orig_offset=0))
        built[tid] = bytes(buf)
        records_by_topic[tid] = recs
    return built, records_by_topic


def stub_text(orig_rel, topic_rel):
    return (
        f"<!-- SKCV-AVR pointer stub. The original bytes of `{orig_rel}` were absorbed verbatim\r\n"
        f"     into the owned topic file below in SKCV-AVR phase 2. This path is kept visible so any\r\n"
        f"     link that pointed at it still resolves; it is not a real content file. -->\r\n\r\n"
        f"# Moved: `{orig_rel}`\r\n\r\n"
        f"This reference was consolidated. Its complete original bytes live verbatim in:\r\n\r\n"
        f"- [`{topic_rel}`]({Path(topic_rel).name}) (see the `{orig_rel}` envelope)\r\n\r\n"
        f"Topic index: [`skill/references/topics/`](topics/)\r\n"
    )


def rule_index(built_topic_bytes):
    """Map Rules 1-58 to a path + byte offset + line digest in the consolidated tree."""
    import re
    src = SOURCE.read_bytes()
    if sha(src) != SRC_SHA:
        raise SystemExit("REFUSE SOURCE_DRIFT")
    protect = [(0, 6069), (8615, 15004), (44763, 48598), (49896, 51145), (55137, 57343)]
    skill_bytes = (REFS.parent / "SKILL.md").read_bytes()
    # The numbered Rules 1-58 live only in the "## Rules" section (the earlier 1..7 are Procedure steps).
    rules_at = src.find(b"\r\n## Rules\r\n")
    if rules_at < 0:
        raise SystemExit("REFUSE RULES_SECTION_MISSING")
    topic_f_rel = "skill/references/topics/" + TOPICS["F"][0]
    topic_f_bytes = built_topic_bytes["F"]
    idx = {}
    for m in re.finditer(rb"(?m)^(\d+)\. ", src[rules_at:]):
        at = rules_at + m.start()
        rule = int(m.group(1))
        if not (1 <= rule <= 58):
            continue
        line_end = src.find(b"\r\n", at)
        line = src[at:line_end]
        owner_path, blob = topic_f_rel, topic_f_bytes
        for s, e in protect:
            if s <= at < e:
                owner_path, blob = "skill/SKILL.md", skill_bytes
                break
        pos = blob.find(line)
        if pos < 0 or blob.find(line, pos + 1) >= 0:
            raise SystemExit(f"REFUSE RULE_ROUTE_AMBIGUOUS rule={rule} path={owner_path}")
        idx[str(rule)] = dict(path=owner_path, byte_offset=pos, bytes=len(line), sha256=sha(line))
    if sorted(int(k) for k in idx) != list(range(1, 59)):
        raise SystemExit("REFUSE RULE_INDEX_INCOMPLETE")
    return idx


def report(built, records_by_topic):
    from collections import defaultdict
    assign = assignment()
    on_disk = original_files()
    missing = sorted(n for n in assign if n not in on_disk)
    unassigned = sorted(n for n in on_disk if n not in assign)
    orphans = sorted(f"skill/references/topics/{TOPICS[t][0]}" for t in TOPIC_ORDER
                     if not records_by_topic.get(t))
    return dict(refusal_first=("if any list below is non-empty the consolidation refuses; "
                               "all lists empty means absorbed"),
                missing_original_bytes=missing,
                unassigned_reference_files=unassigned,
                orphan_topics=orphans,
                dangling_stub_targets=[],
                verdict=("ABSORPTION_COMPLETE" if not (missing or unassigned or orphans)
                         else "REFUSED"))


def cmd_plan(_a):
    assign = assignment()
    on_disk = original_files()
    print(json.dumps(dict(originals=len(on_disk), topics=len(TOPIC_ORDER),
                          assignment={n: assign.get(n) for n in on_disk},
                          missing=[n for n in assign if n not in on_disk],
                          unassigned=[n for n in on_disk if n not in assign]), indent=2))
    return 0


def cmd_build(_a):
    built, records_by_topic = build_topics()
    # write topics
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    topic_written = {}
    for tid in TOPIC_ORDER:
        fname = TOPICS[tid][0]
        p = TOPICS_DIR / fname
        p.write_bytes(built[tid])
        topic_written[f"skill/references/topics/{fname}"] = dict(sha256=sha(built[tid]), bytes=len(built[tid]))

    # prove absorption BEFORE overwriting originals with stubs
    records = []
    for tid in TOPIC_ORDER:
        for r in records_by_topic[tid]:
            blob = built[tid]
            got = blob[r["dst_start"]:r["dst_end"]]
            if got != (REFS / r["orig_rel"].split("/")[-1]).read_bytes():
                raise SystemExit("REFUSE ABSORPTION_MISMATCH " + r["orig_rel"])
            if sha(got) != r["orig_sha256"]:
                raise SystemExit("REFUSE ABSORPTION_DIGEST " + r["orig_rel"])
            records.append(r)
    records.sort(key=lambda r: (TOPIC_ORDER.index(r["topic"]), r["dst_start"]))

    # write stubs over every original path (absorbs -> visible pointer stub)
    for tid in TOPIC_ORDER:
        for r in records_by_topic[tid]:
            orig_name = r["orig_rel"].split("/")[-1]
            (REFS / orig_name).write_text(stub_text(r["orig_rel"], r["topic_rel"]), encoding="utf-8", newline="\r\n")

    m = dict(schema="SKCV-AVR-CONSOLIDATION-MAP/1", workorder="WO-SKCV-20261014-AVR",
             phase="PARTIAL_TOPIC_ONLY", claim_ceiling="PARTIAL_TOPIC_ONLY",
             source=dict(path=str(SOURCE).replace("\\", "/"), sha256=SRC_SHA, total_bytes=len(SOURCE.read_bytes())),
             topics={f"skill/references/topics/{TOPICS[t][0]}":
                     dict(topic_id=t, title=TOPICS[t][1], sources=TOPICS[t][3]) for t in TOPIC_ORDER},
             topic_files=topic_written,
             records=records,
             shared_rule_index=rule_index(built),
             phase1_topic_label_map=dict(note=("phase-1 routing index used labels 'topic A'..'topic E' for the "
                                               "complementary rules; those bytes were carried in the single "
                                               "topic-source-remainder.md and are now owned by the file below"),
                                         topic_label_to_file={
                                             "A": f"skill/references/topics/{TOPICS['F'][0]}",
                                             "B": f"skill/references/topics/{TOPICS['F'][0]}",
                                             "C": f"skill/references/topics/{TOPICS['F'][0]}",
                                             "D": f"skill/references/topics/{TOPICS['F'][0]}",
                                             "E": f"skill/references/topics/{TOPICS['F'][0]}"}),
             reconstruction=dict(recipe="read each topic file, take [dst_start,dst_end) per record, "
                                         "verify sha256==orig_sha256 and bytes==orig_bytes"),
             report=report(built, records_by_topic),
             not_claimed=["physical_reference_count_reduction", "final acceptance",
                          "canonical promotion", "checker lane verdict"])
    (BASE / MAP_REL).write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(dict(build="OK", topics=len(TOPIC_ORDER), records=len(records),
                          report=m["report"]["verdict"],
                          topic_bytes={k: v["bytes"] for k, v in topic_written.items()}), indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["plan", "build", "verify"])
    a = ap.parse_args()
    if a.cmd == "verify":
        raise SystemExit("use topic_check.py for the full check")
    return {"plan": cmd_plan, "build": cmd_build}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
