#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WO-SKCV-20261014-HGK successor: ONE atomic entry-extraction step.

PARTIAL maker engineering only (PARTIAL_ENTRY_ONLY). Keeps the protected main
entry (frontmatter/identity/triggers, architecture + execution invariants 1-11,
and the mandatory local pre-action/authorization hard gates) and moves every
complementary original byte verbatim into one visible Markdown reference.
Reconstruction is defined solely by entry_map.json -- never by rereading source.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.normpath(
    os.path.join(HERE, "..", "..", "baseline", "hgk-governed-execution", "SKILL.md"))
EXPECTED_SRC_SHA = "174df0185026de09c673b92d1df5b8f01dcb35cf0cf7facbbdf095b368fdf9e4"
MAIN_REL = "skill/SKILL.md"
REF_REL = "skill/references/topics/construction-wave-and-remaining-procedures.md"
# Protected source byte intervals selected by the independent Hermes reader.
MAIN_RANGES = [(0, 3531), (11574, 22333), (97867, 103288)]
EDGES = {0: b"---\r\nname: hgk-governed-execution",
         3531: b"## Routing map",
         11574: b"## Architecture invariants (never violate)",
         22333: b"12. **Construction-wave execution law",
         97867: b"## Step 9 \xe2\x80\x94 FDA / Windows",
         103288: b"### Step 9 "}
ROUTING = (
    "\n## Entry routing map (SKCV-20261014 extraction - refusal-first)\n\n"
    "This main entry keeps the inlined core: frontmatter/identity/triggers, architecture +\n"
    "execution invariants 1-11, and the mandatory local pre-action/authorization hard gates\n"
    "(Step 9-0 / Step 9-0a). Every other original byte was moved verbatim, without decode.\n\n"
    "| Need | Read (verbatim original text) |\n"
    "|---|---|\n"
    "| Skill routing map, RP-002 v2.0 status | `references/topics/construction-wave-and-remaining-procedures.md` (slice 1) |\n"
    "| External-challenge closure, independent acceptance lane, Steps 0-8, watchdog, evidence home/closure pipelines (6B/6C/6D), Step 10A, pitfalls | same file (slice 3) |\n"
    "| Step 9 operations detail, Step 9A, Step 10, Support files | same file (slice 5) |\n"
    "| Exact byte provenance / reconstruction | `entry_map.json` (per-slice source+destination offsets and sha256) |\n\n"
    "Construction-wave and remaining procedures route to their original moved bytes in the\n"
    "reference above. Refusal-first: do NOT reconstruct or paraphrase those procedures from\n"
    "memory. If the reference is missing, a slice is missing/reordered/corrupt, or a digest\n"
    "disagrees with `entry_map.json`, STOP and report the `ERR_ENTRY_MAP_*` code - never return\n"
    "a green result for an incomplete entry. Moved text carries the same authority; this\n"
    "pointer adds none.\n")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def _slice(sid, role, a, c, data, dest_file, s, e):
    return {"slice_id": sid, "role": role,
            "source": {"start": a, "end": c, "len": c - a, "sha256": sha256(data)},
            "dest": {"file": dest_file, "start": s, "end": e, "len": e - s,
                     "sha256": sha256(data)}}


def build(original):
    """Return (main_bytes, reference_bytes, ordered_slices) from the original bytes."""
    main, ref, slices = bytearray(), bytearray(), []
    d0 = original[0:3531]
    main += d0
    slices.append(_slice(0, "main", 0, 3531, d0, MAIN_REL, 0, len(main)))
    main += ROUTING.encode("utf-8")
    d2 = original[11574:22333]
    s = len(main)
    main += d2
    slices.append(_slice(2, "main", 11574, 22333, d2, MAIN_REL, s, len(main)))
    d4 = original[97867:103288]
    s = len(main)
    main += d4
    slices.append(_slice(4, "main", 97867, 103288, d4, MAIN_REL, s, len(main)))
    for sid, a, c in [(1, 3531, 11574), (3, 22333, 97867), (5, 103288, len(original))]:
        data = original[a:c]
        ref += ("\n<!-- BEGIN SLICE %d src[%d,%d) sha256=%s -->\n"
                % (sid, a, c, sha256(data))).encode("ascii")
        s = len(ref)
        ref += data
        e = len(ref)
        ref += ("\n<!-- END SLICE %d -->\n" % sid).encode("ascii")
        slices.append(_slice(sid, "reference", a, c, data, REF_REL, s, e))
    slices.sort(key=lambda r: r["source"]["start"])
    return bytes(main), bytes(ref), slices


def mapdoc(original, slices, main, ref):
    return {"schema": "SKCV-ENTRY-MAP/1", "task": "WO-SKCV-20261014-HGK",
            "phase": "PARTIAL_ENTRY_ONLY",
            "source": {"path": "baseline/hgk-governed-execution/SKILL.md",
                       "sha256": sha256(original), "bytes": len(original)},
            "artifacts": {"main": MAIN_REL, "reference": REF_REL},
            "envelope_policy": "Envelope/comment text is explanatory only and is NOT a mapped slice.",
            "reconstruction": "Concatenate each slice's destination byte range in list order.",
            "slices": slices}


def verify(doc, root, original):
    """Fail-closed recheck: ordering, coverage, destination digests, reconstruction."""
    total = len(original)
    prev = -1
    for sl in doc["slices"]:
        if sl["source"]["start"] <= prev:
            return "ERR_ENTRY_MAP_ORDER"
        prev = sl["source"]["start"]
    cur = 0
    for sl in doc["slices"]:
        if sl["source"]["start"] != cur:
            return "ERR_ENTRY_MAP_GAP"
        cur = sl["source"]["end"]
    if cur != total:
        return "ERR_ENTRY_MAP_GAP"
    for sl in doc["slices"]:
        path = os.path.join(root, sl["dest"]["file"])
        if not os.path.exists(path):
            return "ERR_ENTRY_MAP_MISSING_ARTIFACT"
        with open(path, "rb") as fh:
            data = fh.read()[sl["dest"]["start"]:sl["dest"]["end"]]
        if len(data) != sl["source"]["len"] or sha256(data) != sl["source"]["sha256"]:
            return "ERR_ENTRY_MAP_DEST_DIGEST"
    recon = bytearray()
    for sl in doc["slices"]:
        with open(os.path.join(root, sl["dest"]["file"]), "rb") as fh:
            recon += fh.read()[sl["dest"]["start"]:sl["dest"]["end"]]
    return "OK" if bytes(recon) == original else "ERR_RECONSTRUCTION_MISMATCH"


def negatives(doc, root, original):
    """Deterministic negative seams: missing / reordered / corrupt slices must refuse."""
    out = {}
    miss = json.loads(json.dumps(doc))
    miss["slices"] = miss["slices"][:2] + miss["slices"][3:]
    out["missing_slice"] = verify(miss, root, original)
    reord = json.loads(json.dumps(doc))
    reord["slices"][0], reord["slices"][1] = reord["slices"][1], reord["slices"][0]
    out["reordered_slice"] = verify(reord, root, original)
    tmp = tempfile.mkdtemp()
    try:
        for rel in sorted({sl["dest"]["file"] for sl in doc["slices"]}):
            dst = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(root, rel), dst)
        sl0 = doc["slices"][0]
        path = os.path.join(tmp, sl0["dest"]["file"])
        raw = bytearray(open(path, "rb").read())
        raw[sl0["dest"]["start"]] ^= 0xFF
        open(path, "wb").write(bytes(raw))
        out["corrupt_slice"] = verify(doc, tmp, original)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    with open(src, "rb") as fh:
        original = fh.read()
    checks = {"source_sha256": sha256(original), "source_bytes": len(original),
              "baseline_unchanged": sha256(original) == EXPECTED_SRC_SHA,
              "boundaries_valid": all(original.startswith(tok, pos)
                                       for pos, tok in EDGES.items())}
    if not checks["baseline_unchanged"] or not checks["boundaries_valid"]:
        print("REFUSED: baseline drift or boundary mismatch"); return 2
    main_b, ref_b, slices = build(original)
    doc = mapdoc(original, slices, main_b, ref_b)
    main_b2, ref_b2, slices2 = build(original)
    doc2 = mapdoc(original, slices2, main_b2, ref_b2)
    checks["repeat_generation_stable"] = (
        main_b == main_b2 and ref_b == ref_b2
        and json.dumps(doc, sort_keys=True) == json.dumps(doc2, sort_keys=True))
    i0 = original.index(b"---\r\n")
    fm_end = original.index(b"\r\n---\r\n", i0 + 3) + len(b"\r\n---\r\n")
    checks["frontmatter_unchanged"] = main_b[:fm_end] == original[:fm_end]
    checks["frontmatter_bytes"] = fm_end
    checks["main_decoded_chars"] = len(main_b.decode("utf-8"))
    checks["main_decoded_chars_under_24000"] = checks["main_decoded_chars"] < 24000
    os.makedirs(os.path.join(HERE, os.path.dirname(REF_REL)), exist_ok=True)
    with open(os.path.join(HERE, MAIN_REL), "wb") as fh:
        fh.write(main_b)
    with open(os.path.join(HERE, REF_REL), "wb") as fh:
        fh.write(ref_b)
    map_bytes = json.dumps(doc, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    with open(os.path.join(HERE, "entry_map.json"), "wb") as fh:
        fh.write(map_bytes)
    checks["verify"] = verify(doc, HERE, original)
    checks["negatives"] = negatives(doc, HERE, original)
    checks["artifact_sha256"] = {"main": sha256(main_b), "reference": sha256(ref_b),
                                 "entry_map": sha256(map_bytes)}
    neg = checks["negatives"]
    ok = (checks["baseline_unchanged"] and checks["boundaries_valid"]
          and checks["repeat_generation_stable"] and checks["frontmatter_unchanged"]
          and checks["main_decoded_chars_under_24000"]
          and checks["verify"] == "OK"
          and neg["missing_slice"] == "ERR_ENTRY_MAP_GAP"
          and neg["reordered_slice"] == "ERR_ENTRY_MAP_ORDER"
          and neg["corrupt_slice"] == "ERR_ENTRY_MAP_DEST_DIGEST")
    result = {
        "task": "WO-SKCV-20261014-HGK", "phase": "PARTIAL_ENTRY_ONLY",
        "claim": "PARTIAL_ENTRY_ONLY - one atomic entry-extraction artifact/measurement step only.",
        "command": "%s %s %s" % (sys.executable, os.path.abspath(__file__), src),
        "qualified_python": "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe",
        "checks": checks, "checks_pass": ok,
        "deferred_to_next_successor": [
            "New reference consolidation across all moved topic files",
            "Broader positive/negative/boundary tests and holdout",
            "Consumer/linter adaption, guarded apply and rollback exercise",
            "Independent (GLM) verification and canonical acceptance"],
        "transport_token": "SKCV_HGK_3_OK"}
    with open(os.path.join(HERE, "phase1_result.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
    print("main_decoded_chars=%d verify=%s negatives=%s checks_pass=%s"
          % (checks["main_decoded_chars"], checks["verify"], neg, ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
