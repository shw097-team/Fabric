#!/usr/bin/env python
"""Build the FAR-20261019 CAPC prompt contract by deterministic substitution of FAR-018's
compiler-clean contract. Reuse, not re-derivation: structure, invariant lists and render policy are
carried over byte-for-byte; only the round identity, the authority sources, the changeset and the
intent text are replaced.

Always regenerates from FAR-018's contract, never from this round's own output: loading one's own
output as a base carries forward any key a schema change rejects (it did once: a stale key).
"""
import json, hashlib, glob, datetime
from pathlib import Path

PREV = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
OUT.mkdir(parents=True, exist_ok=True)
FARRUN = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261019-owner-authorized-closure")
OLD = "FAR-20261016-018-r7r11-residual-closure-and-handover"
NEW = "FAR-20261019-owner-authorized-closure"

SRC = [
    ("current_user_instruction", "SRC-FAR019-OWNER-AUTHORIZATION",
     "owner authorization (sole Fabric & HG-KSEOS owner, this session): authorises direct execution of "
     "this round's ruling over all residual, blocked, unclosed and owner-decision items", None),
    ("execution_controls", "SRC-FAR018-RULING", "FAR-018 ruling", PREV / "FAR_RULING.md"),
    ("execution_controls", "SRC-FAR018-REGISTER", "FAR-018 residual register", PREV / "RESIDUAL_REGISTER.json"),
    ("execution_controls", "SRC-FAR018-ADJUDICATION", "FAR-018 adjudication and limitations",
     PREV / "ADJUDICATION_AND_LIMITATIONS.json"),
    ("execution_controls", "SRC-FAR018-LINEAGE", "FAR-018 HGK lineage receipt",
     PREV / "HGK_WORKORDER_RESULTS_AND_DELIVERY.json"),
    ("product_authority", "SRC-PKG", "PKG",
     Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
          "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")),
    ("external_review", "SRC-EIA-R7R11", "EIA",
     Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
          "attachments/Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md")),
    ("knowledge_pack", "SRC-SKILL-HGK", "HGK skill",
     Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
          "skills/software-development/hgk-governed-execution/SKILL.md")),
    ("repo_state", "SRC-FAR-RUN", "FAR run dir", FARRUN / "DECISION_QUESTION.md"),
    ("execution_controls", "SRC-PREV-ROUND", "FAR-018 publish receipt", PREV / "PUBLISH_RECEIPT.json"),
    ("execution_controls", "SRC-PREV-READBACK", "FAR-018 remote readback",
     PREV / "REMOTE_READBACK_VERIFY.json"),
]
# The schema requires exactly these six families in source_scan.reviewed; a missing family is PL-003.
REQUIRED_FAMILIES = ["current_user_instruction", "product_authority", "external_review",
                     "execution_controls", "knowledge_pack", "repo_state"]


def sha(p, fallback="UNAVAILABLE"):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return fallback


def sub_text(s):
    return s.replace(OLD, NEW)


c = json.loads((PREV / "prompt-contract.json").read_text(encoding="utf-8"))
c["task_id"] = NEW

# source_scan.reviewed allows exactly ONE entry per required family (two entries in a family is
# reported as duplicate=True by PL-003). The remaining inputs are declared under authority.sources.
PRIMARY = {"current_user_instruction": "SRC-FAR019-OWNER-AUTHORIZATION",
           "product_authority": "SRC-PKG", "external_review": "SRC-EIA-R7R11",
           "execution_controls": "SRC-FAR018-RULING", "knowledge_pack": "SRC-SKILL-HGK",
           "repo_state": "SRC-FAR-RUN"}
c["source_scan"]["reviewed"] = [
    {"source_family": fam, "source_id": sid,
     "locator": (str(p) if p else "(session text)"),
     "sha256": (sha(p) if p else "UNAVAILABLE"), "role": "NORMATIVE", "critical": True}
    for fam, sid, _l, p in SRC if PRIMARY.get(fam) == sid]
c["source_scan"]["missing"] = []
# The schema forbids extra keys under source_scan (PL-SCHEMA), so the absent Fabric root AGENTS.md is
# declared in the round's residual register and ruling instead of here. Recorded, not hidden.

if isinstance(c.get("authority", {}).get("sources"), list):
    # Correct entry shape (measured from the previous compiler-clean contract): id / rank / path /
    # sha256 / locator / role / governs. A missing `rank` or `governs`, or an extra `kind`, is PL-SCHEMA.
    c["authority"]["sources"] = [
        {"id": sid, "rank": "R%d" % (i + 1),
         "path": (str(p) if p else "(session text)"),
         "sha256": (sha(p) if p else "UNAVAILABLE"),
         "locator": (str(p) if p else "owner mandate, this session"),
         "role": "NORMATIVE", "governs": True}
        for i, (fam, sid, _l, p) in enumerate(SRC)]

c["intent"]["goal"] = (
    "Under the Fabric governance contract with HG-KSEOS as the sole control plane and canonical Hermes as "
    "its governed Runtime/Orchestration Plane, run the FAR method over every item still open after round "
    "FAR-20261016-018 — residual, gap, blocked, unclosed and owner-decision items, unlanded candidate "
    "assets and skills, and this session's own closeout and handover — and produce ONE ranked engineering "
    "ruling that is low-friction, high-feasibility, necessary, not over-engineered, aligned with the "
    "session goal and with the governing blueprint package and acceptance report. The sole owner of Fabric "
    "and HG-KSEOS has authorised direct execution of that ruling, so the round must execute every action "
    "the ruling marks executable under that authority and leave only genuinely human-owned assertions "
    "(facts only the owner can attest, and normative semantic changes) as prepared single-action items.")

c["changeset"]["affected_files"] = [
    "EVIDENCE/FAR-20261019-owner-authorized-closure/** (new prefix, this round's pack)",
    "Fabric/fabric-autonomous-research/runs/FAR-20261019-*/{METHOD.md,DECISION_QUESTION.md}",
    "_handover/FAR-20261019-owner-authorized-closure/** (round receipts and probes)",
    "HG-KSEOS/config/** (only if the ruling authorises the canonical repair, with backup and hash readback)",
]

gov = [str(PREV / "FAR_RULING.md"), str(PREV / "RESIDUAL_REGISTER.json"),
       str(PREV / "ADJUDICATION_AND_LIMITATIONS.json"), str(PREV / "W1_RESIDUAL_UNIVERSE.json")]
for block in c.get("execution_scope", []):
    if isinstance(block, dict) and "source_locators" in block:
        block["source_locators"] = gov[:2] + [gov[2]]

for j in c.get("journeys", []):
    if isinstance(j, dict):
        j["journey_id"] = sub_text(str(j.get("journey_id", "JNY")))
        if isinstance(j.get("source_locators"), list):
            j["source_locators"] = [sub_text(x) for x in j["source_locators"]]

# Carry-over fields still name the old round in places; substitute only where the string is an identity
# reference, and leave locators that deliberately point at FAR-018's artifacts untouched.
for key in ("termination", "evidence", "acceptance"):
    if key in c:
        blob = json.dumps(c[key], ensure_ascii=False)
        if OLD in blob and "FAR_RULING" not in blob:
            c[key] = json.loads(sub_text(blob))

(OUT / "prompt-contract.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", OUT / "prompt-contract.json", (OUT / "prompt-contract.json").stat().st_size, "bytes")
print("task_id:", c["task_id"], "| sources:", len(c["source_scan"]["reviewed"]))

cand = glob.glob("C:/Projects/Agent_Workspace/**/prompt_contract_compiler.py", recursive=True)
print("compiler candidates:", cand[:4])
