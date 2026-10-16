"""Preserve the refused first VERIFY dispatch and inspect the writer manifest.

Why this exists: the successful retry overwrote lane/VERIFY_RECEIPT.json at turn end, so the
first-fail would otherwise be destroyed. Artifact hygiene: a receipt that can be overwritten must
have its refusal preserved explicitly.
"""
import json
from pathlib import Path

RD = Path(__file__).resolve().parent
CH = r"C:\Users\user\AppData\Local\HG-KSEOS\codex-hermes"

refused = {
    "schema": "HGK-LANE-RESOLUTION/1",
    "ok": False,
    "lane": "VERIFY_SECURITY",
    "code": "ERR_GUARD_ROOT_MISSING",
    "detail": "guard root(s) do not resolve for this process: "
              "['C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/"
              "RESIDUAL_REGISTER.json']",
    "guard_roots": [
        ".../FAR_RULING.md", ".../RESIDUAL_REGISTER.json", ".../W1_RESIDUAL_UNIVERSE.json",
        ".../writer/checker_isolation_probe.py", ".../writer/self_check_v2.py", ".../writer/entry_map.json",
        ".../lane/EXECUTE_RECEIPT.json",
        "C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/self_check.py",
    ],
    "say": "a vacuous guard would report a clean subject; refusing instead",
    "codex_home": CH,
    "codex_home_is_declared_lane_home": True,
    "generated_utc": "2026-10-16T11:25:33.246467+00:00",
    "provenance": "REFUSED FIRST dispatch of the VERIFY lane, transcribed verbatim from that dispatch's "
                  "output; guard_roots abbreviated with '...' for the shared prefix. Preserved because the "
                  "successful retry overwrote lane/VERIFY_RECEIPT.json at turn end.",
    "root_cause": "the orchestrator guarded a file it had not generated yet (RESIDUAL_REGISTER.json); the "
                  "guard correctly refused rather than reporting a vacuous clean subject",
    "remediation_applied": "build_register.py was run, then the lane was re-dispatched; the second attempt "
                           "served the required arm openai-codex/gpt-6.1-sol",
}
(RD / "lane" / "VERIFY_ATTEMPT1_REFUSED.json").write_text(
    json.dumps(refused, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote lane/VERIFY_ATTEMPT1_REFUSED.json", (RD / "lane" / "VERIFY_ATTEMPT1_REFUSED.json").stat().st_size)

wm = json.loads((RD / "writer" / "WRITER_MANIFEST.json").read_text(encoding="utf-8"))


def dig(o, p=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            out += dig(v, p + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += dig(v, p + "[%d]" % i)
    elif isinstance(o, str):
        out.append((p, o))
    return out


rows = dig(wm)
print("--- writer's own recorded self-test / exit evidence ---")
for p, v in rows:
    if ("SELF_TEST" in v or "NEGATIVE_CONTROL" in v) or "exit" in p.lower() or "command" in p.lower():
        print("  ", p, "->", v[:150].replace("\n", " "))
