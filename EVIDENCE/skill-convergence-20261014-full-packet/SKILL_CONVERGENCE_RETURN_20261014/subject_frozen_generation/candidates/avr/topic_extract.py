#!/usr/bin/env python
"""WO-SKCV-20261014-AVR phase 2 (TOPIC_BATCH_1): absorb TWO theme groups.

For exactly TWO theme groups, this tool absorbs the complete verbatim bytes of
files that skill/SKILL.md links into skill/references/topics/<theme>.md behind a
short envelope (original relative path, byte offset within the topic, sha256),
leaves a visible one-line pointer stub at each absorbed original path, and
records topic_batch_1.json. Two themes only: the remaining themes and the
physical alias-file count debt stay OPEN. Commands: generate | verify.
Writes only under candidates/avr (plus its own stdout).
"""
import argparse, hashlib, json, re
from pathlib import Path

BASE = Path(__file__).resolve().parent
MAIN_REL = "skill/SKILL.md"
BATCH_REL = "topic_batch_1.json"
TOPICS_DIR_REL = "skill/references/topics"

# Two theme groups. Paths are skill-relative, as they appear in skill/SKILL.md.
THEMES = {
    "verification-and-acceptance-lane": [
        "references/independent-verification-hygiene.md",
        "references/sealed-evidence-corpus.md",
        "references/verdict-artifact-and-budget.md",
        "references/finding-classification.md",
    ],
    "lane-harness-and-handover": [
        "references/verifier-lane-handover.md",
        "references/checker-binding-and-false-defect-signals.md",
        "references/lane-harness-and-admission-gate.md",
    ],
}

PATH_RE = re.compile(rb"`([A-Za-z0-9._/-]+\.(?:md|py|json))`")

STUB_TEMPLATE = ("[SKCV-AVR phase2 absorbed -> skill/references/topics/{theme}.md "
                 ":: topic_byte_offset={offset} :: sha256={sha256} "
                 ":: original bytes verbatim in topic, no byte edits]\r\n")

sha = lambda b: hashlib.sha256(b).hexdigest()
skill_abs = lambda rel: BASE / "skill" / rel


def linked_paths():
    """Every path-like token skill/SKILL.md links, with its raw byte offset."""
    mb = (BASE / MAIN_REL).read_bytes()
    out = []
    for m in PATH_RE.finditer(mb):
        rel = m.group(1).decode("ascii")
        out.append((rel, m.start(1)))
    return out


def build():
    links = linked_paths()
    offset_of = {}
    for rel, off in links:
        offset_of.setdefault(rel, off)
    for theme, rels in THEMES.items():
        for rel in rels:
            if rel not in offset_of:
                raise SystemExit(f"REFUSE LINK_NOT_FOUND {rel}")
            if not skill_abs(rel).exists():
                raise SystemExit(f"REFUSE ORIGINAL_MISSING {rel}")
    topics, absorbed = {}, []
    for theme, rels in THEMES.items():
        ordered = sorted(rels, key=lambda r: offset_of[r])  # doc order, deterministic
        out = bytearray()
        out += ("===== SKCV-TOPIC-BATCH BEGIN theme=%s =====\r\n" % theme).encode("utf-8")
        out += ("topic: %s\r\n" % theme).encode("utf-8")
        out += ("note: complete verbatim bytes of absorbed files; envelope only, no byte edits; "
                "byte offset = offset of the absorbed file's first byte within this topic file\r\n").encode("utf-8")
        out += ("segment_count: %d\r\n\r\n" % len(ordered)).encode("utf-8")
        for idx, rel in enumerate(ordered, 1):
            raw = skill_abs(rel).read_bytes()
            if len(raw) == 0:
                raise SystemExit(f"REFUSE ABSORBED_EMPTY {rel}")
            h = sha(raw)
            # payload starts right after the header line; the header's own width
            # depends on the (decimal) offset, so solve the fixpoint explicitly
            # rather than patching a placeholder afterwards.
            payload_start = len(out)
            while True:
                header = ("===== SKCV-TOPIC-SEGMENT %d BEGIN path=%s offset=%d bytes=%d sha256=%s =====\r\n"
                          % (idx, rel, payload_start, len(raw), h)).encode("utf-8")
                fixed = len(out) + len(header)
                if fixed == payload_start:
                    break
                payload_start = fixed
            out += header
            assert len(out) == payload_start, (len(out), payload_start)
            out += raw
            payload_end = len(out)
            out += ("===== SKCV-TOPIC-SEGMENT %d END =====\r\n" % idx).encode("utf-8")
            absorbed.append(dict(
                absorbed_path=rel,
                sha256=h,
                bytes=len(raw),
                owned_by_theme=theme,
                segment_index=idx,
                topic_file="%s/%s.md" % (TOPICS_DIR_REL, theme),
                byte_offset=payload_start,
                payload_byte_end=payload_end,
                main_doc_offset=offset_of[rel],
                stub_path="skill/" + rel,
            ))
        out += b"===== SKCV-TOPIC-BATCH END =====\r\n"
        topics[theme] = bytes(out)
    batch = dict(
        schema="SKCV-AVR-TOPIC-BATCH/1",
        workorder="WO-SKCV-20261014-AVR",
        phase="TOPIC_BATCH_1",
        batch_scope="2_of_many_theme_groups",
        theme_groups=list(THEMES.keys()),
        topics={t: dict(file="%s/%s.md" % (TOPICS_DIR_REL, t),
                        sha256=sha(b), bytes=len(b),
                        segments=len([a for a in absorbed if a["owned_by_theme"] == t]))
                for t, b in topics.items()},
        absorbed=absorbed,
        stub_template=STUB_TEMPLATE,
        main_doc_linked_paths=[dict(path=r, offset=o) for r, o in links],
        open_debt=[
            "theme groups not in this batch remain unaugmented",
            "physical alias-file count debt (stubs + topics do not reduce the physical file count)",
        ],
        not_claimed=["reference count reduction", "comprehensive tests",
                     "independent acceptance", "canonical promotion"],
        partial_entry_only=True, not_final_tests=True, not_acceptance=True,
        hgk_canonical_acceptance="NOT_PERFORMED",
        sqs_live_trading="NOT_AUTHORIZED",
    )
    return topics, batch


def stub_bytes(entry):
    return STUB_TEMPLATE.format(theme=entry["owned_by_theme"], offset=entry["byte_offset"],
                                sha256=entry["sha256"]).encode("utf-8")


def write_all(topics, batch):
    (BASE / TOPICS_DIR_REL).mkdir(parents=True, exist_ok=True)
    for theme, b in topics.items():
        (BASE / (TOPICS_DIR_REL + "/" + theme + ".md")).write_bytes(b)
    for entry in batch["absorbed"]:
        (BASE / entry["stub_path"]).write_bytes(stub_bytes(entry))
    (BASE / BATCH_REL).write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_generate(_a):
    topics, batch = build()
    write_all(topics, batch)
    print("GENERATE_OK themes=%d absorbed=%d" % (len(topics), len(batch["absorbed"])))
    for t, b in topics.items():
        print("  topic %s = %s (%d bytes, %d segments)" % (t, sha(b), len(b),
              len([a for a in batch["absorbed"] if a["owned_by_theme"] == t])))
    return 0


def cmd_verify(_a):
    topics, batch = build()
    bad = []
    for t, b in topics.items():
        p = BASE / (TOPICS_DIR_REL + "/" + t + ".md")
        if not p.exists() or p.read_bytes() != b:
            bad.append("topic:%s" % t)
    for entry in batch["absorbed"]:
        p = BASE / entry["stub_path"]
        if not p.exists() or p.read_bytes() != stub_bytes(entry):
            bad.append("stub:%s" % entry["stub_path"])
    print("VERIFY_FAIL " + ",".join(bad) if bad else "VERIFY_OK")
    return 7 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["generate", "verify"])
    a = ap.parse_args()
    return {"generate": cmd_generate, "verify": cmd_verify}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
