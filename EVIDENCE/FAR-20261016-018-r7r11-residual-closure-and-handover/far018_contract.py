#!/usr/bin/env python
"""Build the FAR-20261016-018 CAPC prompt contract by deterministic substitution of the previous
round's compiler-clean contract. Reuse, not re-derivation: every structural block, invariant list and
render policy is carried over byte-for-byte; only the round identity, sources, claims and intent text
are replaced.
"""
import json, hashlib, datetime
from pathlib import Path

PREV = Path("C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016")
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
PREV_CMD = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
                "attachments/Fabric × Hermes × HG-KSEOS｜R7～R11 外部驗收後續作「指揮薄 PROMPT」.md")
EIA = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
           "attachments/Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md")
PKG = Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
           "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")
SKILL = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
             "skills/software-development/hgk-governed-execution/SKILL.md")
FARRUN = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/"
              "FAR-20261016-018-r7r11-residual-closure-and-handover")


def sha(p, fallback="UNAVAILABLE"):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return fallback


# Always regenerate from the compiler-clean previous contract: loading this round's own previous output as a
# base would carry forward any key a schema change rejects (it did: a stale non_source_gaps key).
c = json.loads((PREV / "prompt-contract.json").read_text(encoding="utf-8"))

c["task_id"] = "FAR-20261016-018-r7r11-residual-closure-and-handover"

SRC = [
    ("current_user_instruction", "SRC-FAR018-MANDATE", "FAR-20261016-018 owner mandate (this round's command)", None),    ("product_authority", "SRC-PKG", "PKG", PKG),
    ("external_review", "SRC-EIA-R7R11", "EIA", EIA),
    ("execution_controls", "SRC-PREV-ROUND", "previous round RETURN_PACK.json", PREV / "packet/RETURN_PACK.json"),
    ("knowledge_pack", "SRC-SKILL-HGK", "HGK skill", SKILL),
    ("repo_state", "SRC-FAR-RUN", "FAR run dir", FARRUN / "DECISION_QUESTION.md"),
]
c["source_scan"]["reviewed"] = [
    {"source_family": fam, "source_id": sid,
     "locator": (str(p) if p else "(owner message in this session, 2026-10-16)"),
     "sha256": (sha(p) if p else "UNAVAILABLE"), "role": "NORMATIVE", "critical": True}
    for fam, sid, _label, p in SRC]
c["source_scan"]["missing"] = []
# NOTE (recorded in the ruling, not hidden): the contract schema has no field for "a governing file that
# should exist is absent", so the absent Fabric/AGENTS.md cannot be declared here. The previous round's
# contract had the same empty list for the same reason. Declared instead in the round's own residual register.
# The absent Fabric/AGENTS.md cannot be declared in the contract: source_scan.missing is a set of source
# FAMILIES and the schema forbids extra keys. It is declared in this round's own residual register and named
# in the ruling instead of being silently dropped.

c["source_scan"]["normative_claims"] = [
    {"claim_id": "NC-001",
     "text": "This round is a governed FAR research round whose executable actions are the low-friction, "
             "agent-authorised subset of its own ruling; owner-gated items are prepared, never attempted.",
     "source_ids": ["SRC-FAR018-MANDATE", "SRC-EIA-R7R11"], "locators": ["owner mandate", str(EIA)]},
    {"claim_id": "NC-002",
     "text": "Remote publication is evidence-only: no product code, no policy, no workflow and no hook is "
             "modified in the target repository, and no existing merged evidence is rewritten.",
     "source_ids": ["SRC-PKG", "SRC-PREV-ROUND"], "locators": [str(PKG)]},
    {"claim_id": "NC-003",
     "text": "Writer and checker run on different model axes; the checker arm is pinned by --require-arm "
             "because the verification pool's rank-1 arm is the writer's own model.",
     "source_ids": ["SRC-FAR018-MANDATE"], "locators": ["owner mandate"]},
    {"claim_id": "NC-004",
     "text": "The acceptance report's P0 findings are closed only by their own 1:1 oracle; an archive "
             "merge, a file's existence or a green aggregate is not that oracle.",
     "source_ids": ["SRC-EIA-R7R11"], "locators": [str(EIA)]},
    {"claim_id": "NC-005",
     "text": "Every count in the evidence pack is derived from artifacts on disk by a script and is "
             "re-derivable by an independent lane.",
     "source_ids": ["SRC-FAR018-MANDATE"], "locators": ["owner mandate"]},
]

c["authority"]["sources"] = [
    {"id": sid, "rank": "R1" if i == 0 else f"R{i + 1}",
     "path": (str(p) if p else "(session text)"), "sha256": (sha(p) if p else "UNAVAILABLE"),
     "locator": (str(p) if p else "owner mandate, this session"), "role": "NORMATIVE", "governs": True}
    for i, (_fam, sid, _l, p) in enumerate(SRC)]

c["authority"]["missing_sources"] = []
c["authority"]["conflicts"] = []

c["intent"]["goal"] = (
    "Under the Fabric governance contract with HG-KSEOS as the sole control plane and canonical Hermes as "
    "its governed Runtime/Orchestration Plane, run the FAR method (run id FAR-20261016-018) over every "
    "residual, gap, blocked item, owner-decision item, unlanded candidate asset and session "
    "closeout/handover obligation left by the R7-R11 evidence-archive round; state one ranked engineering "
    "ruling whose executable actions are low-friction, high-feasibility, high-necessity, not "
    "over-engineered and aligned with the upper blueprint and the acceptance report; then execute that "
    "ruling, because the owner has pre-authorised its execution, and publish the evidence.")
c["intent"]["user_expected_outcome"] = (
    "A ranked ruling with a machine-readable residual register; the agent-executable actions actually "
    "executed with raw receipts (a measured checker-isolation probe, the reconstructed skill entry map, a "
    "reproducible lane-defect dossier, a session handover checkpoint); the owner-gated items prepared in "
    "one-action form; and a published, readback-bound evidence pack for external acceptance.")
c["intent"]["explicit_constraints"] = [
    "HG-KSEOS remains the sole control plane; no second scheduler, reducer, DB, board or evidence authority is created.",
    "Remote publication is evidence-only under a single new EVIDENCE/ prefix; no existing evidence is rewritten.",
    "The maker never self-accepts; the checker lane is pinned cross-model and may not write to the subject.",
    "Owner-gated items (merge, release, cross-repo code promotion, canonical control-plane edits, product-host ACL) are prepared, not attempted.",
    "Every probe must be able to fail, and must be shown failing, before it is shown passing.",
    "Counts live inside artifacts; a number that exists only in chat is unverifiable.",
    "The registry is read, never edited, to make a measurement come out right.",
    "Credential values are read only by a local broker process and never printed or committed.",
]
c["intent"]["non_goals"] = [
    "Full 221-case / G-A-H convergence, production promotion, or any RUNTIME_READY claim.",
    "Promoting the R7-02 validator code into the PIPD repository, or merging the peer chain #6/#8/#10.",
    "Promoting PR #12 out of draft, or editing any merged R6-R11 evidence.",
    "Re-slimming the two already-slimmed skills, or treating the reference-count soft warning as a hard gate.",
    "Building a new governance plane, virtualization layer or verifier system to close the isolation finding.",
]
c["intent"]["authorized_mutations"] = [
    "Create one new EVIDENCE/ prefix in shw097-team/Fabric holding this round's evidence pack (additive commits on a new branch).",
    "Create the round's own probe scripts, receipts and registers under the round's handover directory.",
    "Reconstruct the missing entry_map.json index for the HGK skill from the skill's own verified SKCV pointer lines (local asset, additive; no existing byte altered).",
    "Create the session handover/closure artifacts and the FAR run's own METHOD/DECISION_QUESTION/EXECUTION_RECORD documents.",
]
c["intent"]["forbidden_mutations"] = [
    "Editing config/lane-routing-registry.yaml, config/lane-route-slots.candidate.json or any canonical control-plane file.",
    "Editing, deleting or force-updating any branch or evidence already merged into main.",
    "Merging any pull request, promoting any draft, tagging or releasing.",
    "Executing any archived .py/.ps1 helper from an evidence tree.",
    "Printing, committing or transmitting the credential value.",
]
c["intent"]["allowed_hitl"] = [
    "Owner-scoped merge of the peer chain #6/#8/#10.",
    "Owner-scoped promotion or merge of PR #12.",
    "Cross-repo validator code promotion (R7-02) and the Fresh G1 owner certificate (R7-04).",
    "Any canonical control-plane or product-host ACL change.",
    "Any expansion of this round's change class beyond EVIDENCE_ONLY.",
]
DELS = ["DEL-FAR-RULING", "DEL-RESIDUAL-UNIVERSE", "DEL-DEFECT-DOSSIER", "DEL-HANDOVER-CHECKPOINT",
        "DEL-SINGLE-EVIDENCE-MD"]
c["intent"]["requested_delivery"] = DELS
_tpl = [x for x in c["acceptance"] if x.get("subject_type") == "DELIVERABLE"][0]
for _d in DELS:
    _row = json.loads(json.dumps(_tpl))
    _row["acceptance_id"] = "ACC-" + _d
    _row["subject_id"] = _d
    _row["source_locators"] = ["(owner mandate, this session, 2026-10-16)"]
    _row["positive_fixture"] = (
        _d + ": the artifact exists, is produced by a script from artifacts on disk, and an independent lane "
        "re-derives its counts and verdicts from primary sources. Positive control: the mandated input is "
        "accepted and leaves a raw receipt.")
    _row["negative_fixture"] = (
        "Refusal case on the same fixture: a missing, hand-written or non-re-derivable value is refused with "
        "its own typed code, with a positive control that must succeed on the same run.")
    c["acceptance"].append(_row)

c["changeset"]["class"] = "EVIDENCE_ONLY"
c["changeset"]["affected_domains"] = ["evidence", "verification", "local_asset_repair", "handover"]
c["changeset"]["affected_files"] = [
    "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/** (new prefix, this round's pack)",
    "Fabric/fabric-autonomous-research/runs/FAR-20261016-018-*/{METHOD.md,DECISION_QUESTION.md,EXECUTION_RECORD.md}",
    "hermes/skills/software-development/hgk-governed-execution/entry_map.json (reconstructed index)",
    "_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/** (round receipts and probes)",
]
c["changeset"]["must_not_reopen"] = [
    "PR #3..#11 merged evidence", "PR #12 draft packet snapshot",
    "canonical lane registry and route slots", "the published R6-R11 FAIL/NOT_RUN receipts",
    "the R7-02/R7-03/R7-04 owner decisions", "the 221-case applicability question",
]
c["changeset"]["product_mutation_allowed"] = False
c["changeset"]["tracked_mutation"] = True

c["intent"]["claim_ceiling"] = "LOCAL"

# termination: restored verbatim from the compiler-clean previous contract (the schema pins its fields;
# replacing it wholesale is what broke lint), then only the round-specific additions are applied.
c["termination"] = json.loads((PREV / "prompt-contract.json").read_text(encoding="utf-8"))["termination"]
# extend, do not replace: the acceptance rows reference terminals from the previous set, so the allowed
# vocabulary must be a union or PL-010 turns the carried-over rows into violations.
for _t in ("FAR_RULING_EXECUTED", "FAR_RULING_PARTIAL_OWNER_GATED", "FAR_RULING_BLOCKED"):
    if _t not in c["termination"]["terminal_states"]:
        c["termination"]["terminal_states"].append(_t)
c["termination"]["rollback_pointer_required"] = True

(OUT / "prompt-contract.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
print("contract written:", (OUT / "prompt-contract.json").stat().st_size, "bytes")
print("task_id:", c["task_id"], "| class:", c["changeset"]["class"], "| ceiling:", c["intent"]["claim_ceiling"])
print("sources:", len(c["source_scan"]["reviewed"]), "| claims:", len(c["source_scan"]["normative_claims"]))
for r in c["source_scan"]["reviewed"]:
    print("   ", r["source_id"], r["sha256"][:16], r["locator"][:70])
