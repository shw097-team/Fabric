"""WS-A step 5: loss proof FROM BYTES.

(a) For each absorbed reference, assert the current live bytes appear verbatim at the
    recorded topic offset (recorded in the stub).
(b) Assert every line of the live SKILL.md longer than 40 bytes appears somewhere in
    (repaired SKILL.md  U  topic files  U  carried-live references).

The union for (b) is built as the harness builds its C4 corpus: the SKCV-slice marker
lines stripped from the repaired SKILL.md, plus the bytes of every non-SKILL .md file in
the repaired tree (which covers references/topics/*, topic-source-remainder.md, the pointer
stubs, and any carried-live reference). Raw output saved to WS_A/s5_loss_proof.txt/.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")
SRC = W / "repaired_candidate"
LIVE = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
            "/skills/software-development/adversarial-verification-rounds")
STUB_RE = re.compile(r"absorbed -> (?P<topic>[^\s]+) :: topic_byte_offset=(?P<off>\d+) :: sha256=(?P<sha>[0-9a-f]{64})")
MARKER = re.compile(rb"^=+\s*SKCV-SLICE[^\n]*\n", re.M)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    lines: list[str] = []

    def emit(s: str = "") -> None:
        lines.append(s)
        print(s)

    # (a) offset-verbatim proof for absorbed references
    emit("=== (a) offset-verbatim proof: current live bytes at recorded topic offset ===")
    absorbed = []
    a_ok = True
    for p in sorted((SRC / "references").glob("*.md")):
        b = p.read_bytes()
        m = STUB_RE.search(b.decode("utf-8", "replace"))
        if m is None:
            continue
        live_ref = LIVE / "references" / p.name
        lb = live_ref.read_bytes()
        topic = SRC / m.group("topic")
        if not topic.is_file():
            topic = SRC / re.sub(r"^skill/", "", m.group("topic"))
        tb = topic.read_bytes()
        off = int(m.group("off"))
        verbatim = tb[off:off + len(lb)] == lb
        a_ok = a_ok and verbatim
        absorbed.append({"ref": p.name, "topic": str(topic.relative_to(SRC)), "offset": off,
                         "live_bytes": len(lb), "live_sha256": sha(lb),
                         "offset_verbatim": verbatim})
        emit(f"  {p.name:52s} off={off:6d} bytes={len(lb):6d} verbatim={verbatim}")

    # (b) live SKILL.md line survival
    emit("")
    emit("=== (b) live SKILL.md line survival (len>40) in repaired corpus ===")
    cb = (SRC / "SKILL.md").read_bytes()
    corpus = MARKER.sub(b"", cb) + b"\n".join(
        p.read_bytes() for p in sorted(SRC.rglob("*.md")) if p.name != "SKILL.md")
    ll = [l for l in (LIVE / "SKILL.md").read_bytes().split(b"\n") if len(l.strip()) > 40]
    lost = [l.decode("utf-8", "replace") for l in ll if l not in corpus]
    b_ok = not lost
    emit(f"  live_lines_gt40 = {len(ll)}")
    emit(f"  corpus_bytes    = {len(corpus)}")
    emit(f"  lost_lines      = {len(lost)}")
    for s in lost[:10]:
        emit(f"    LOST: {s[:100]}")

    verdict = "PASS" if (a_ok and b_ok) else "FAIL"
    emit("")
    emit(f"step5_verdict = {verdict}   (a_offset_verbatim={a_ok} b_line_survival={b_ok})")
    out = {"step": "s5_loss_proof", "verdict": verdict, "a_offset_verbatim": a_ok,
           "b_line_survival": b_ok, "absorbed": absorbed,
           "live_lines_gt40": len(ll), "lost_lines": len(lost),
           "lost_samples": [s[:100] for s in lost[:10]]}
    (W / "s5_loss_proof.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    (W / "s5_loss_proof.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
