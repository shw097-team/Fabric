#!/usr/bin/env python
"""WO-SKCV-20261014-AVR phase 1 (PARTIAL_ENTRY_ONLY): one atomic entry extraction.

Frozen source -> candidate skill/SKILL.md (exact protected slices + refusal-first
routing table) + one visible topic reference (all complementary slices) + entry_map.json
whose slices reconstruct the whole source byte-for-byte.
Commands: generate | reconstruct | negative | phase1. Author/execute only inside candidates/avr.
"""
import argparse, hashlib, json, platform, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parents[1] / "baseline" / "adversarial-verification-rounds" / "SKILL.md"
SRC_SHA = "4be690a4feaee5ba1fcf7bb5c109b6c41a3834060f1e962a3d9112952f66e97e"
SRC_LEN = 101488
PROT = [(0, 6069), (8615, 15004), (44763, 48598), (49896, 51145), (55137, 57343)]
HINTS = [b"---\r\nname: adversarial-verification-rounds", b"7. **Claim ceilings",
         b"33. **A human decision", b"35. **Score CLAIM-vs-CODE", b"39. **Contract for the WIRING"]
MAIN_REL = "skill/SKILL.md"
TOPIC_REL = "skill/references/topic-source-remainder.md"
MAP_REL, RESULT_REL = "entry_map.json", "phase1_result.json"
ROUTING = (
 "## Refusal-first entry routing (PARTIAL_ENTRY_ONLY)\r\n\r\n"
 "Refuse before acting when any of these hold:\r\n"
 "- R-01 subject not frozen (no master/stage digest) - do not open a round.\r\n"
 "- R-02 required arm/checker unbound or self-declared - refuse; never swap in a healthy-looking arm.\r\n"
 "- R-03 evidence summary-only, stale or foreign - refuse; recompute from raw bytes.\r\n"
 "- R-04 guard/comparator passes on missing input (vacuous pass) - refuse; demand PASS/FAIL/INCONCLUSIVE.\r\n"
 "- R-05 promotion is not acceptance - no maker self-accept, no commander-signed receipt.\r\n"
 "- R-06 a human token closes only what it names - never extend it.\r\n\r\n"
 "Index (this file holds the protected cores; the topic reference holds the rest, verbatim):\r\n"
 "| Rules | Subject | Where |\r\n"
 "| 1-6 | errata in place, manifest self-exclusion, derived counts, tier loss, as-of stamps | topic A |\r\n"
 "| 7-11 | claim ceilings / quotation-coverage / model-binding | inline below |\r\n"
 "| 12-32 | write ceilings, self-check, arm-that-serves, budget, mirrors, durable routes | topic B |\r\n"
 "| 33 | human-act authority | inline below |\r\n"
 "| 34 | brief bound by rule, not a frozen SHA | topic C |\r\n"
 "| 35 | CLAIM-vs-CODE agreement as its own axis | inline below |\r\n"
 "| 36-38 | preimage byte-identical, delivered tree, self-disclosed limits | topic D |\r\n"
 "| 39-40 | wiring contract / frozen instrument | inline below |\r\n"
 "| 41-58 | measurement apparatus, fail-closed probes, subject binding, claim boundaries | topic E |\r\n\r\n"
 "- reference: `references/topic-source-remainder.md` (all complementary source bytes, verbatim).\r\n\r\n"
 "## Protected rule cores (verbatim)\r\n\r\n")

sha = lambda b: hashlib.sha256(b).hexdigest()

def complement(n):
    out, p = [], 0
    for s, e in PROT:
        if s > p: out.append((p, s))
        p = e
    if p < n: out.append((p, n))
    return out

class Packer:
    def __init__(self, rel): self.rel, self.buf, self.slices = rel, bytearray(), []
    def text(self, t): self.buf += t.encode("utf-8") if isinstance(t, str) else t
    def mark(self, sid, s, e, payload):
        h = sha(payload)
        self.text(f"===== SKCV-SLICE {sid} BEGIN src={s}..{e} sha256={h} =====\r\n")
        d0 = len(self.buf); self.buf += payload; d1 = len(self.buf)
        self.text(f"===== SKCV-SLICE {sid} END =====\r\n")
        self.slices.append(dict(id=sid, src_start=s, src_end=e, src_sha256=h, dst_file=self.rel,
                                dst_start=d0, dst_end=d1, dst_sha256=h))

def build():
    b = SOURCE.read_bytes()
    if len(b) != SRC_LEN or sha(b) != SRC_SHA: raise SystemExit("REFUSE SOURCE_DRIFT: digest/length != frozen")
    prev = 0
    for (s, e), hint in zip(PROT, HINTS):
        if not (0 <= s < e <= len(b)): raise SystemExit(f"REFUSE BOUNDS {s}..{e}")
        if s < prev: raise SystemExit(f"REFUSE OVERLAP {s}..{e}")
        if not b[s:e].startswith(hint): raise SystemExit(f"REFUSE HINT at {s}")
        if s and b[s-2:s] != b"\r\n": raise SystemExit(f"REFUSE NOT_LINE_START {s}")
        if e != len(b) and b[e-2:e] != b"\r\n": raise SystemExit(f"REFUSE NOT_LINE_END {e}")
        prev = e
    main, topic = Packer(MAIN_REL), Packer(TOPIC_REL)
    main.mark("S1", *PROT[0], b[PROT[0][0]:PROT[0][1]]); main.text(ROUTING)
    for i, (s, e) in enumerate(PROT[1:], 2): main.mark(f"S{i}", s, e, b[s:e])
    topic.text("<!-- SKCV-AVR complementary source remainder: verbatim bytes, PARTIAL_ENTRY_ONLY -->\r\n\r\n")
    for j, (s, e) in enumerate(complement(len(b)), 1): topic.mark(f"T{j}", s, e, b[s:e])
    slices = sorted(main.slices + topic.slices, key=lambda x: x["src_start"])
    if len(main.buf.decode("utf-8")) >= 24000: raise SystemExit("REFUSE MAIN_OVER_24K")
    m = dict(schema="SKCV-AVR-ENTRY-MAP/1", workorder="WO-SKCV-20261014-AVR", phase="PARTIAL_ENTRY_ONLY",
             source=dict(path=str(SOURCE).replace("\\", "/"), sha256=SRC_SHA, total_bytes=len(b)),
             protected_intervals=[list(x) for x in PROT],
             complementary_intervals=[list(x) for x in complement(len(b))],
             generated={MAIN_REL: dict(sha256=sha(main.buf), bytes=len(main.buf)),
                        TOPIC_REL: dict(sha256=sha(topic.buf), bytes=len(topic.buf))},
             envelope=dict(begin="===== SKCV-SLICE {id} BEGIN src={s}..{e} sha256={h} =====",
                           end="===== SKCV-SLICE {id} END =====", newline="CRLF"),
             slices=slices,
             reconstruct=dict(recipe="read generated main+topic, take each slice dst range, concat "
                                     "in ascending src_start, verify slice sha256 and full source sha256"),
             not_claimed=["reference consolidation", "comprehensive tests", "final acceptance",
                          "canonical promotion"])
    return bytes(main.buf), bytes(topic.buf), m

def reconstruct(m, load):
    srcs = [s["src_start"] for s in m["slices"]]
    if srcs != sorted(srcs) or len(set(srcs)) != len(srcs):
        return False, "REORDERED_MAP", "map slices not strictly ascending by src_start"
    out, pos = bytearray(), 0
    for s in m["slices"]:
        if s["src_start"] != pos: return False, "COVERAGE_GAP", f"expected src {pos}, got {s['src_start']}"
        f = load(s["dst_file"])
        if s["dst_start"] < 0 or s["dst_end"] < s["dst_start"] or s["dst_end"] > len(f):
            return False, "DST_RANGE_INVALID", f"{s['id']} {s['dst_start']}..{s['dst_end']} of {len(f)}"
        blob = f[s["dst_start"]:s["dst_end"]]
        if len(blob) != s["src_end"] - s["src_start"]: return False, "DST_LENGTH_MISMATCH", s["id"]
        if sha(blob) != s["src_sha256"] or sha(blob) != s["dst_sha256"]:
            return False, "SLICE_HASH_MISMATCH", s["id"]
        out += blob; pos = s["src_end"]
    if pos != m["source"]["total_bytes"]: return False, "COVERAGE_GAP", f"tail {pos} != {m['source']['total_bytes']}"
    if sha(out) != m["source"]["sha256"]: return False, "FULL_DIGEST_MISMATCH", sha(out)
    return True, "OK", bytes(out)

def write_all(main_b, topic_b, m):
    (BASE / MAIN_REL).write_bytes(main_b)
    (BASE / TOPIC_REL).write_bytes(topic_b)
    (BASE / MAP_REL).write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

load_map = lambda: json.loads((BASE / MAP_REL).read_text(encoding="utf-8"))
loader = lambda m: (lambda rel: (BASE / rel).read_bytes())

def negative_cases(m):
    base = loader(m); cases = []
    mm = json.loads(json.dumps(m)); mm["slices"].pop(len(mm["slices"]) // 2)
    cases.append(("missing_slice", mm, base, "COVERAGE_GAP"))
    mm = json.loads(json.dumps(m)); s = mm["slices"][len(mm["slices"]) // 2]
    s["src_start"], s["src_end"] = s["src_end"], s["src_start"]
    cases.append(("reordered_slice", mm, base, "REORDERED_MAP"))
    mm = json.loads(json.dumps(m)); tgt = mm["slices"][len(mm["slices"]) // 2]
    def bad_load(rel, tgt=tgt):
        b = bytearray(base(rel))
        if rel == tgt["dst_file"]: b[tgt["dst_start"] + 1] ^= 0x01
        return bytes(b)
    cases.append(("corrupt_slice", mm, bad_load, "SLICE_HASH_MISMATCH"))
    results = []
    for tag, mm, load, want in cases:
        ok, code, _ = reconstruct(mm, load)
        results.append(dict(case=tag, refused=not ok, code=code, expected=want, pass_=(not ok and code == want)))
    return results

def cmd_generate(_a):
    main_b, topic_b, m = build(); write_all(main_b, topic_b, m)
    print("GENERATE_OK main=%s(%d) topic=%s(%d) slices=%d" % (sha(main_b), len(main_b),
          sha(topic_b), len(topic_b), len(m["slices"])))
    return 0

def cmd_reconstruct(_a):
    m = load_map(); ok, code, info = reconstruct(m, loader(m))
    print(("RECONSTRUCT_OK bytes=%d sha=%s" % (len(info), sha(info))) if ok
          else ("REFUSE %s: %s" % (code, info)))
    return 0 if ok else 3

def cmd_negative(_a):
    results = negative_cases(load_map())
    for r in results:
        print(f"NEG {r['case']}: refused={r['refused']} code={r['code']} "
              f"expected={r['expected']} -> {'OK' if r['pass_'] else 'FAIL'}")
    return 0 if all(r["pass_"] for r in results) else 4

def cmd_phase1(_a):
    t0 = time.time(); main_b, topic_b, m = build(); write_all(main_b, topic_b, m)
    main2, topic2, _ = build()
    repeat_ok = main_b == main2 and topic_b == topic2
    ok, code, recon = reconstruct(m, loader(m)); neg = negative_cases(m)
    res = dict(schema="SKCV-AVR-PHASE1-RESULT/1", workorder="WO-SKCV-20261014-AVR",
               phase="PARTIAL_ENTRY_ONLY", status="PHASE1_ATOMIC_ENTRY_EXTRACT_DONE",
               interpreter=sys.executable, python=platform.python_version(), platform=platform.platform(),
               source=dict(path=str(SOURCE).replace("\\", "/"), sha256=SRC_SHA, total_bytes=SRC_LEN),
               commands={k: "%s entry_extract.py %s" % (sys.executable, k)
                         for k in ("generate", "reconstruct", "negative", "phase1")},
               protected_intervals=[list(x) for x in PROT], generated=m["generated"],
               main_decoded_body_chars=len(main_b.decode("utf-8")),
               main_under_24000=len(main_b.decode("utf-8")) < 24000,
               repeat_generation_digest_equal=repeat_ok,
               reconstruct=dict(ok=ok, code=code, source_sha256=sha(recon) if ok else None),
               negative_checks=neg,
               boundary_validation="PASS (source sha256, line-start/line-end alignment, interval hints)",
               files_written=[MAIN_REL, TOPIC_REL, MAP_REL],
               unchanged="all other skill/references/* and skill/scripts/* untouched",
               partial_entry_only=True, not_reference_consolidation=True, not_final_tests=True,
               not_acceptance=True, hgk_canonical_acceptance="NOT_PERFORMED",
               sqs_live_trading="NOT_AUTHORIZED",
               successors=["full reference grouping", "comprehensive tests", "independent acceptance"])
    (BASE / RESULT_REL).write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(dict(repeat_generation_digest_equal=repeat_ok, reconstruct=ok,
                          reconstruct_code=code, negative=neg, elapsed_s=round(time.time() - t0, 3)), indent=2))
    return 0 if repeat_ok and ok and all(n["pass_"] for n in neg) else 5

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["generate", "reconstruct", "negative", "phase1"])
    a = ap.parse_args()
    return {"generate": cmd_generate, "reconstruct": cmd_reconstruct,
            "negative": cmd_negative, "phase1": cmd_phase1}[a.cmd](a)

if __name__ == "__main__":
    raise SystemExit(main())