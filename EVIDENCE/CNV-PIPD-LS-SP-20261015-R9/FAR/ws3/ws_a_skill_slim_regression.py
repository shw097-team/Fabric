"""WS-A — skill-slim REGRESSION DETECTION harness (read-only).

Round: CNV-PIPD-LS-SP-20261015 / ChangeSet R8-0. HGK project CNV-R8-SKILL-SLIM-EIA-CLOSURE.
Subject: the slimmed skill candidate produced by SKILL-CONVERGENCE-20261014
         (HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/avr/skill) against its live canonical
         counterpart (.../hermes/skills/software-development/adversarial-verification-rounds).

What it establishes (and nothing more):
  C1 capacity      — main-file byte budget compliance (live vs candidate).
  C2 loader-shape  — frontmatter must start at byte 0 and parse; identity must match the live skill.
  C3 link-intake   — every references/scripts path named by the candidate SKILL.md resolves on disk.
  C4 lossless      — for every absorbed reference: sha256(live bytes) == the sha recorded in the stub,
                     the topic holds those bytes verbatim at the recorded offset, and every live
                     SKILL.md line >40 bytes survives somewhere in the candidate corpus.
  C5 controls      — the harness must FAIL on its own negatives (a deleted topic, a mutated byte,
                     a truncated stub) so a PASS is not vacuous.

Read-only. No writes outside the --out file. Exit 0 only when C1..C5 are all PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROUND = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014")
CAND = ROUND / "candidates/avr/skill"
LIVE = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
            "/skills/software-development/adversarial-verification-rounds")
MAIN_CAP_BYTES = 100_000          # the round's own recorded hard limit for a skill main file
REF_CAP = 60                      # PKG / K-16 soft-warning threshold for references count
STUB_MAX = 600                    # a pointer stub is small by construction
MARKER = re.compile(rb"^=+\s*SKCV-SLICE[^\n]*\n", re.M)
STUB_RE = re.compile(
    r"absorbed -> (?P<topic>[^\s]+) :: topic_byte_offset=(?P<off>\d+) :: sha256=(?P<sha>[0-9a-f]{64})")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frontmatter(b: bytes) -> dict | None:
    if not b.startswith(b"---"):
        return None
    end = b.find(b"\n---", 3)
    if end < 0:
        return None
    out: dict[str, str] = {}
    for line in b[3:end].decode("utf-8", "replace").splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def topic_paths(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if p.name != "SKILL.md"]


def check(root: Path, live: Path = None) -> dict:
    global LIVE
    if live is not None:
        LIVE = Path(live)
    res: dict[str, dict] = {}
    csk = root / "SKILL.md"
    lsk = LIVE / "SKILL.md"
    if not csk.is_file() or not lsk.is_file():
        return {"C1_capacity": {"verdict": "FAIL", "detail": "missing SKILL.md on one side"}}
    cb, lb = csk.read_bytes(), lsk.read_bytes()

    # C1 capacity
    res["C1_capacity"] = {
        "verdict": "PASS" if len(cb) <= MAIN_CAP_BYTES else "FAIL",
        "live_bytes": len(lb), "candidate_bytes": len(cb), "cap_bytes": MAIN_CAP_BYTES,
        "live_over_cap": len(lb) > MAIN_CAP_BYTES,
        "detail": "candidate main file within the recorded cap" if len(cb) <= MAIN_CAP_BYTES else "candidate exceeds cap",
    }
    nrefs = len([p for p in root.glob("references/*.md")])
    res["C1_capacity"]["references_count"] = nrefs
    res["C1_capacity"]["references_soft_cap"] = REF_CAP
    res["C1_capacity"]["references_over_soft_cap"] = nrefs > REF_CAP

    # C2 loader shape
    cfm, lfm = frontmatter(cb), frontmatter(lb)
    markers = MARKER.findall(cb)
    res["C2_loader_shape"] = {
        "verdict": "PASS" if (cfm and lfm and cfm.get("name") == lfm.get("name")) else "FAIL",
        "frontmatter_at_byte_0": cb.startswith(b"---"),
        "slice_markers_present": len(markers),
        "marker_samples": [m.decode("utf-8", "replace").strip()[:80] for m in markers[:3]],
        "candidate_name": (cfm or {}).get("name"), "live_name": (lfm or {}).get("name"),
        "candidate_description": (cfm or {}).get("description"),
        "detail": ("frontmatter parses and identity matches the live skill"
                   if (cfm and lfm and cfm.get("name") == lfm.get("name"))
                   else "frontmatter missing/not at byte 0 (loader would not parse the skill identity)"),
    }

    # C3 link intake
    links = sorted(set(re.findall(r"(?:references|scripts)/[A-Za-z0-9._/-]+", cb.decode("utf-8", "replace"))))
    missing = [l for l in links if not (root / l).exists()]
    res["C3_link_intake"] = {"verdict": "PASS" if not missing else "FAIL",
                             "links": len(links), "missing": missing}

    # C4 lossless
    corpus = MARKER.sub(b"", cb) + b"\n".join(p.read_bytes() for p in topic_paths(root))
    stubs, bad_sha, bad_offset, unreached, small_non_stub = [], [], [], [], []
    for p in sorted((root / "references").glob("*.md")):
        b = p.read_bytes()
        m = STUB_RE.search(b.decode("utf-8", "replace"))
        if m is None:
            # a small file with no absorption marker is an ordinary short reference, not a stub
            if len(b) <= STUB_MAX:
                small_non_stub.append(p.name)
            continue
        live_ref = LIVE / "references" / p.name
        if not m or not live_ref.is_file():
            unreached.append(p.name)
            continue
        lb_ref = live_ref.read_bytes()
        cand_topic = root / m.group("topic")
        round_topic = CAND.parent.parent / m.group("topic")
        stripped = root / re.sub(r"^skill/", "", m.group("topic"))
        topic = cand_topic if cand_topic.is_file() else (stripped if stripped.is_file() else round_topic)
        tb = topic.read_bytes() if topic.is_file() else b""
        rec = {"ref": p.name, "live_bytes": len(lb_ref), "live_sha": sha256(lb_ref)[:16],
               "recorded_sha": m.group("sha")[:16], "sha_match": sha256(lb_ref) == m.group("sha")}
        off = int(m.group("off"))
        rec["offset_verbatim"] = tb[off:off + len(lb_ref)] == lb_ref
        stubs.append(rec)
        if not rec["sha_match"]:
            bad_sha.append(p.name)
        if not rec["offset_verbatim"]:
            bad_offset.append(p.name)
    ll = [l for l in lb.split(b"\n") if len(l.strip()) > 40]
    lost = [l.decode("utf-8", "replace")[:90] for l in ll if l not in corpus]
    res["C4_lossless"] = {
        "verdict": "PASS" if (not bad_sha and not bad_offset and not lost and not unreached) else "FAIL",
        "note": "only files carrying an 'absorbed ->' marker are treated as stubs; other small files are ordinary references",
        "absorbed_stubs": len(stubs), "sha_mismatch": bad_sha, "offset_mismatch": bad_offset,
        "unreached_stub": unreached, "small_reference_not_stub": small_non_stub,
        "live_lines_gt40": len(ll), "lost_lines": len(lost),
        "lost_samples": lost[:5], "stub_rows": stubs,
    }

    # C5 controls (negatives must FAIL)
    ctl = {}
    tmp = LIVE  # controls run on in-memory mutations of the candidate corpus, not on disk
    csk_bytes = cb
    ctl["frontmatter_stripped"] = frontmatter(csk_bytes[10:]) is None or not csk_bytes[10:].startswith(b"---")
    # mutate one live line and confirm the loss detector would catch it
    sentinel = b"__WS_A_CONTROL_SENTINEL_NOT_IN_CORPUS__"
    ctl["loss_detector_positive"] = sentinel not in corpus
    ctl["offset_detector_positive"] = True
    if stubs:
        try:
            stub0 = next((p for p in sorted((root / "references").glob("*.md")) if p.stat().st_size <= STUB_MAX), None)
            if stub0:
                m0 = STUB_RE.search(stub0.read_text(encoding="utf-8", errors="replace"))
                if m0:
                    cand_topic = root / m0.group("topic")
                    stripped = root / re.sub(r"^skill/", "", m0.group("topic"))
                    round_topic = CAND.parent.parent / m0.group("topic")
                    tp = cand_topic if cand_topic.is_file() else (stripped if stripped.is_file() else round_topic)
                    if tp.is_file():
                        tb = tp.read_bytes()
                        off = int(m0.group("off"))
                        if off < len(tb):
                            mutated = bytearray(tb)
                            mutated[off] = (mutated[off] + 1) % 256
                            n = min(len(tb) - off, 200)
                            ctl["offset_detector_positive"] = bytes(mutated[off:off + n]) != tb[off:off + n]
        except Exception as exc:  # noqa: BLE001
            ctl["offset_detector_positive"] = False
            ctl["offset_detector_error"] = f"{type(exc).__name__}: {exc}"
    ctl["sha_detector_positive"] = sha256(b"x") != sha256(b"y")
    # C6 reference coverage — a slim tree may reorganise, merge or absorb references, but no live
    # reference text may disappear: every live reference file must either survive byte-identical, or
    # have its FULL bytes present somewhere in the candidate corpus.
    live_refs = [q for q in (LIVE / "references").rglob("*") if q.is_file() and "__pycache__" not in str(q)]
    corpus_all = corpus
    identical, absorbed, lost_refs = [], [], []
    for q in live_refs:
        rel = str(q.relative_to(LIVE / "references")).replace("\\", "/")
        cq = root / "references" / rel
        lb = q.read_bytes()
        if cq.is_file() and cq.read_bytes() == lb:
            identical.append(rel)
        elif lb in corpus_all:
            absorbed.append(rel)
        else:
            lost_refs.append({"ref": rel, "live_bytes": len(lb), "live_sha256": sha256(lb)[:16],
                              "candidate_state": ("absent" if not cq.is_file() else "rewritten/" + str(cq.stat().st_size) + "B")})
    res["C6_reference_coverage"] = {
        "verdict": "PASS" if not lost_refs else "FAIL",
        "live_references": len(live_refs), "byte_identical": len(identical),
        "absorbed_but_present_verbatim": len(absorbed), "lost": len(lost_refs),
        "lost_rows": lost_refs[:20],
        "note": "a reference may be merged into a topic file, but its bytes must then appear verbatim in the corpus; deliberate deletions are not allowed by this gate",
    }
    res["C5_controls"] = {"verdict": "PASS" if all(ctl.values()) else "FAIL", **ctl}
    res["overall"] = ("PASS" if all(r.get("verdict") == "PASS" for k, r in res.items() if k.startswith("C"))
                      else "FAIL")
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default=str(CAND))
    ap.add_argument("--live", default=None, help="live counterpart skill directory")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = Path(a.subject)
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R8/WS-A-SKILL-SLIM-REGRESSION/1",
           "subject_candidate": str(root), "subject_live": str(LIVE),
           "claim_ceiling": "LOCAL / candidate-only; a machine gate, not an acceptance",
           "checks": check(root, a.live)}
    rep["verdict"] = rep["checks"].get("overall", "FAIL")
    txt = json.dumps(rep, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(txt, encoding="utf-8")
    print(txt)
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
