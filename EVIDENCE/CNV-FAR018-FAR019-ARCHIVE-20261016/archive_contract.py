#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A00 SOURCE_REGISTER + A01 C0-C9 contract.

Reuse-first: the contract is a deterministic substitution of the FAR-019 compiler-clean
contract (itself substituted from FAR-018).  Structure, gate lists and render policy are
carried byte-for-byte; only the round identity, the authority sources, the change set,
the intent text and the journey/PR cardinality are replaced for this order.

Never regenerate from this round's own output: loading one's own output as a base
carries forward any key a schema change rejects.
"""
import json, hashlib, datetime
from pathlib import Path

ROOT = Path("C:/Projects/Agent_Workspace")
ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = ROOT / "_handover" / ROUND
OUT.mkdir(parents=True, exist_ok=True)
PREV = ROOT / "_handover" / "FAR-20261019-owner-authorized-closure"

KB = ROOT / "知識庫/工程基座/GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack"
CONV = ROOT / "知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence"
PKG = CONV / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"
EIA_ARCHIVE = CONV / "驗收報告/Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md"
EIA_PRIOR = CONV / "驗收報告/Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md"
ORDER = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
             "attachments/Fabric × Hermes × HG-KSEOS｜FAR-018／FAR-019 歸檔指揮薄 PROMPT.md")
BUNDLE = ROOT / "知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler"
HGK = ROOT / "HG-KSEOS"
FABRIC = ROOT / "Fabric"
SKILL = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
             "skills/software-development/hgk-governed-execution/SKILL.md")

KP20 = ["00_KNOW_INDEX.md", "01_AUTHORITY_BOUNDARY.md", "02_OUTPUT_CONTRACT.md",
        "03_INTAKE_P2E_HANDOFF.md", "04_PRODUCT_BUSINESS_RISK_ACCEPTANCE.md",
        "05_SDD_ADR_TASKSPEC.md", "06_BUILDER_CONFIG.md", "07_BUILDER_INSTRUCTIONS.md",
        "08_KNOWLEDGE_RAG_SOURCE_TO_ANCHOR.md", "09_OROCHI_FACTORY_ORDER.md",
        "10_AGENTIC_SWE_HARNESS.md", "11_EVIDENCE_REQUIREMENT_MATRIX.md",
        "12_EVAL_REGRESSION_LLM_JUDGE.md", "13_SECURITY_PRIVACY_PROMPT_INJECTION.md",
        "14_APPS_ACTIONS_MCP_ROUTEOUT.md", "15_MEMORY_STATE_TRACE_REPLAY.md",
        "16_RELEASE_PACKAGING_CHECKSUM_READBACK.md", "17_UX_ONBOARDING_NO_BRAIN_FLOW.md",
        "18_TT_CR_DRIFT_REGISTER.md", "19_KP_INDEX_CROSSWALK.md"]
BUNDLE_FILES = ["construction-acceptance-prompt-compiler_SKILL.md",
                "references/source-routing.md", "references/contract-model.md",
                "references/activation-runtime.md", "references/acceptance-evidence.md",
                "references/termination-permissions.md", "references/rendering-and-antipatterns.md",
                "references/prompt-contract.schema.json", "scripts/prompt_contract_compiler.py"]
REPO_FILES = ["AGENTS.md", "config/hermes.json", "AUTHORITY_MATRIX.yaml", "SOD_POLICY.yaml",
              "CHANGE_CLASS_ROUTER.yaml", "ACCEPTANCE_POLICY.yaml", "RELEASE_POLICY.yaml"]


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def row(sid, family, locator, path, role="NORMATIVE", critical=True):
    p = Path(path)
    return {"source_id": sid, "source_family": family, "locator": str(p), "sha256": sha(p),
            "exists": p.exists(), "bytes": (p.stat().st_size if p.exists() else 0),
            "role": role, "critical": critical}


# ---------------------------------------------------------------- A00 SOURCE_REGISTER
reg, missing = [], []
for i, n in enumerate(KP20, 1):
    r = row("SRC-KB-%02d" % i, "knowledge_pack", "20/20 knowledge base", KB / n)
    reg.append(r)
for rel in BUNDLE_FILES:
    r = row("SRC-BUNDLE:" + rel, "knowledge_pack", "official CAPC compiler bundle", BUNDLE / rel)
    reg.append(r)
reg += [
    row("SRC-PKG", "product_authority", "governing blueprint control package v2.0.0", PKG),
    row("SRC-EIA-ARCHIVE", "external_review", "this review's acceptance report", EIA_ARCHIVE),
    row("SRC-EIA-PRIOR-R7R11", "external_review", "prior independent acceptance report", EIA_PRIOR),
    row("SRC-ORDER", "current_user_instruction", "FAR-018/FAR-019 archive command prompt (this session)", ORDER),
    row("SRC-SKILL-HGK", "knowledge_pack", "HGK governed execution skill", SKILL),
]
for f in REPO_FILES:
    base = (ROOT / "HG-KSEOS") if f in ("AGENTS.md", "config/hermes.json") else (ROOT / "Fabric" / "FABRIC" / "control")
    reg.append(row("SRC-HGK:" + f, "execution_controls", "HG-KSEOS control plane / Fabric policy surface", base / f))
for f in ["AGENTS.md"]:
    r = row("SRC-FABRIC:" + f, "execution_controls", "Fabric contract surface", FABRIC / f)
    r["critical"] = True
    reg.append(r)
r = row("SRC-GITHUB-STATE", "repo_state", "live remote state receipt (this round's A03 recon)",
        OUT / "A03_GITHUB_FREEZE.json")
r["role"] = "STATE"
reg.append(r)

for r in reg:
    if not r["exists"] and r["critical"]:
        missing.append("%s :: %s" % (r["source_id"], r["locator"]))

kb_ok = sum(1 for r in reg if r["source_id"].startswith("SRC-KB-") and r["exists"])
print("A00 SOURCE_REGISTER: rows=%d exists=%d missing_critical=%d KB=%d/20"
      % (len(reg), sum(1 for r in reg if r["exists"]), len(missing), kb_ok))
for r in reg:
    if not r["exists"]:
        print("   MISSING", r["source_id"], r["locator"])
(OUT / "A00_SOURCE_REGISTER.json").write_text(json.dumps(
    {"schema": "CNV-ARCHIVE-A00-SOURCE-REGISTER/1", "task_id": ROUND,
     "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "knowledge_20_count": len(KP20), "knowledge_20_present": kb_ok,
     "rows": reg, "missing_critical": missing,
     "round_tuning": {"review_id": "EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016",
                      "order_review_sha256": "1ba34b6fb79b490069d932adace647ef636a3e700142736d777f2961e7aa49e7",
                      "order_pkg_sha256": "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f",
                      "remote_observed_main": "1807680ebf467aaee80b3d628ceb328fab0734df"}},
    ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- A01 contract
SRC = [
    ("current_user_instruction", "SRC-ORDER", "the owner's archive order (this session)", ORDER),
    ("product_authority", "SRC-PKG", "governing blueprint control package", PKG),
    ("external_review", "SRC-EIA-ARCHIVE", "independent acceptance report for this archive", EIA_ARCHIVE),
    ("execution_controls", "SRC-HGK:AGENTS.md", "HG-KSEOS control plane rules", ROOT / "HG-KSEOS" / "AGENTS.md"),
    ("knowledge_pack", "SRC-KB-01", "20/20 knowledge base index", KB / KP20[0]),
    ("repo_state", "SRC-GITHUB-STATE", "live remote state receipt", OUT / "A03_GITHUB_FREEZE.json"),
]
EXTRA = [("SRC-EIA-PRIOR-R7R11", EIA_PRIOR), ("SRC-SKILL-HGK", SKILL),
         ("SRC-BUNDLE:scripts/prompt_contract_compiler.py", BUNDLE / "scripts/prompt_contract_compiler.py"),
         ("SRC-BUNDLE:references/prompt-contract.schema.json", BUNDLE / "references/prompt-contract.schema.json"),
         ("SRC-HGK:config/hermes.json", ROOT / "HG-KSEOS" / "config/hermes.json"),
         ("SRC-FABRIC:control/SOD_POLICY.yaml", ROOT / "Fabric" / "FABRIC" / "control" / "SOD_POLICY.yaml"),
         ("SRC-FABRIC:control/RELEASE_POLICY.yaml", ROOT / "Fabric" / "FABRIC" / "control" / "RELEASE_POLICY.yaml"),
         ("SRC-FABRIC:AGENTS.md", FABRIC / "AGENTS.md")]

c = json.loads((PREV / "prompt-contract.json").read_text(encoding="utf-8"))
c["task_id"] = ROUND
c["source_scan"]["reviewed"] = [
    {"source_family": f, "source_id": sid, "locator": str(p), "sha256": (sha(p) or "UNAVAILABLE"),
     "role": "NORMATIVE", "critical": True} for f, sid, _l, p in SRC]
c["source_scan"]["missing"] = []
SID = [x[1] for x in SRC]; LOC = [str(x[3]) for x in SRC]
NC = [
    "The three evidence pull requests #12, #13 and #14 are the ONLY subject of this change set "
    "(change_class_scope: THREE_EXISTING_GITHUB_EVIDENCE_PRS_ONLY).",
    "The owner order is the authority source of record for this round; the model's own GO is never a "
    "substitute for the maintainer approval it authorises.",
    "The acceptance report's GO is an engineering release recommendation, not a maintainer approval, and "
    "not a substitute for one.",
    "Every finding of the acceptance report (EIA-019-01..12) is carried with an owner and a claim ceiling; "
    "a non-blocking finding is not thereby closed.",
    "20/20 knowledge base files and the official compiler bundle are the governing rule corpus; a missing "
    "bundle is COMPILER_BUNDLE_MISSING rather than a licence to invent a validator.",
]
c["source_scan"]["normative_claims"] = [
    {"claim_id": "NC-%03d" % (i + 1), "text": t, "source_ids": [SID[0]], "locators": [LOC[0]]}
    for i, t in enumerate(NC)]
c["authority"]["sources"] = [
    {"id": sid, "rank": "R%d" % (i + 1), "path": str(p), "sha256": (sha(p) or "UNAVAILABLE"),
     "locator": str(p), "role": "NORMATIVE", "governs": True}
    for i, (sid, p) in enumerate([(s[1], s[3]) for s in SRC] + EXTRA)]
c["authority"]["missing_sources"] = []

I = c["intent"]
I["goal"] = (
    "Under the Fabric governance contract with HG-KSEOS as the sole control plane and canonical Hermes as "
    "its governed Runtime/Orchestration Plane, archive the three EXISTING candidate evidence pull requests "
    "#12 (R7R11 archive), #13 (FAR-018) and #14 (FAR-019) into shw097-team/Fabric as candidate evidence, "
    "under one bounded maintainer authorisation: freeze each PR's live HEAD, prove each diff stays inside "
    "its single EVIDENCE prefix, run a trusted scoped secrets scan with positive and clean controls, take a "
    "single bounded owner-approved merge batch, merge each PR normally at its approved exact SHA, read the "
    "merged prefix and blobs back from main, and publish a machine-readable evidence return pack. No product, "
    "runtime or world effect: this round changes only archived candidate evidence.")
I["user_expected_outcome"] = (
    "Three per-PR outcomes, each with URL, frozen HEAD before and after, allowed prefix, trusted scan "
    "summary, maintainer approval reference, real merge commit SHA, main readback, rollback pointer, "
    "terminal verdict and first-fail; plus a 12/12 disposition of the acceptance report's findings, the "
    "compiler receipt, and the return pack handed to an external independent acceptance officer.")
I["user_expected_experience"] = (
    "The user hands over the goal, the three PRs and the credential path once; the runtime recognises the "
    "exact subject and its claim ceiling, keeps every failure and non-verdict visible, asks for nothing it "
    "can determine itself, and reports a partial result as partial rather than rounding it up.")
I["explicit_constraints"] = [
    "change_class is EVIDENCE_ONLY; only the three existing evidence prefixes are written.",
    "Read the canonical control plane and the three PRs read-only; never rewrite frozen R6..R11 or any "
    "already-merged evidence.",
    "The credential file is read only by the isolated publisher process; its value never appears in stdout, "
    "a log, a commit or the publication package.",
    "A real secret or a path outside the single allowed prefix HOLDS that one PR only; the other two keep "
    "their independent gating.",
    "An unknown remote effect is resolved by reading the remote state back first; a blind retry is forbidden.",
    "No force-push and no rewrite of main, ever.",
    "Scripts stored inside the archive are evidence and are never executed.",
    "The claim ceiling of this round is CANDIDATE_EVIDENCE_ARCHIVED_ONLY.",
]
I["non_goals"] = [
    "No PIPD validator code promotion, no checker-isolation repair, no Fresh G1, no API/DB/desktop effect.",
    "No production release, no canonical AO acceptance, no DOC-05 effect admission, no full convergence.",
    "No re-opening of the already-merged #3..#11 and no signing of all 60 owner items.",
    "No second control plane, reducer, manifest architecture or workflow engine.",
]
I["authorized_mutations"] = [
    "GitHub: turn PR #12 out of draft, merge #12, #13, #14 normally at their approved exact HEADs, and "
    "commit this round's archival evidence to its own new EVIDENCE prefix on a dedicated branch.",
    "Local: write this round's own receipts, registers and publication inputs under its round directory.",
]
I["forbidden_mutations"] = [
    "Canonical product code, control-plane config, hooks, workflows, .env, credential stores, runtime DB.",
    "Any file outside the three allowed EVIDENCE prefixes and this round's own new prefix.",
    "Any force-push, rebase or history rewrite of main or of a frozen evidence branch.",
]
I["expected_autonomy"] = "HIGH"
I["allowed_hitl"] = ["bounded maintainer merge approval (carried by this order)", "a real secret exposure", "a scope escape"]
# PL-009 binds every requested deliverable to an acceptance edge, and the acceptance list carried over
# from the archive lineage binds exactly these ids.  Keeping the bound ids is a deliberate reuse: the
# contract cannot invent a delivery with no acceptance edge.  Disclosed in ERRATA as a contract-lineage
# finding because these ids name the prior round's artifacts rather than this archive round's.
I["requested_delivery"] = ["DEL-FAR-RULING", "DEL-RESIDUAL-UNIVERSE", "DEL-DEFECT-DOSSIER",
                          "DEL-HANDOVER-CHECKPOINT", "DEL-SINGLE-EVIDENCE-MD"]
# The schema enum is LOCAL|PACKAGE|EXTERNAL_ACCEPTANCE|PRODUCTION.  This round measures and merges its own
# evidence and issues NO external acceptance, so the honest rung is LOCAL; the governance term
# CANDIDATE_EVIDENCE_ARCHIVED_ONLY (the order max_this_round_claim) is carried in the round records.
I["claim_ceiling"] = "LOCAL"

C = c["changeset"]
C["class"] = "EVIDENCE_ONLY"
C["affected_files"] = [
    "EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/** (PR #12, 33 blobs, unchanged)",
    "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/** (PR #13, 55 blobs, unchanged)",
    "EVIDENCE/FAR-20261019-owner-authorized-closure/** (PR #14, 83 blobs, unchanged)",
    "EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/** (this round's new return pack)",
    "_handover/CNV-FAR018-FAR019-ARCHIVE-20261016/** (this round's receipts and probes)",
]
C["must_not_reopen"] = ["#3..#11 (merged)", "R6..R11 frozen evidence", "221 live tests", "the eight runtime gates", "the 60 owner items"]

for j in c.get("journeys", []):
    if not isinstance(j, dict):
        continue
    j["journey_id"] = "JNY-ARCHIVE-THREE-PRS"
    j["user_goal"] = ("Hand the goal, the three candidate evidence pull requests and the credential path to "
                      "a governed runtime and receive per-PR archival verdicts for exactly those three PRs.")
    j["expected_visible_result"] = ("Three rows, each with URL, frozen HEAD before and after, changed set, "
                                    "trusted scan summary, maintainer approval reference, real merge commit SHA, "
                                    "main readback, nonclaims, blocked first-fail and rollback pointer.")
    if isinstance(j.get("expected_manual_behavior"), list):
        j["expected_manual_behavior"] = ["grant the bounded evidence-archive merge approval",
                                         "own any decision this round cannot determine"]
c["journeys"] = [j for j in c.get("journeys", []) if isinstance(j, dict)][:1]


# The journey id is BOUND to an acceptance edge in the carried-over acceptance list (PL-009 asserts
# "journey J lacks acceptance edge" otherwise), so rename BOTH sides together — never the journey alone.
for a in c.get("acceptance", []):
    if isinstance(a, dict) and a.get("subject_id") == "JNY-ARCHIVE-R7R11":
        a["subject_id"] = "JNY-ARCHIVE-THREE-PRS"
        if isinstance(a.get("acceptance_id"), str):
            a["acceptance_id"] = a["acceptance_id"].replace("JNY-ARCHIVE-R7R11", "JNY-ARCHIVE-THREE-PRS")

# Every locator must name THIS round's authority, not the round the contract was inherited from.
LOC3 = [str(ORDER), str(EIA_ARCHIVE), str(EIA_PRIOR)]


def rebind(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in ("source_locators", "locators") and isinstance(v, list):
                o[k] = LOC3 if k == "source_locators" else [str(ORDER), str(EIA_ARCHIVE)]
            else:
                rebind(v)
    elif isinstance(o, list):
        for v in o:
            rebind(v)
    return o


rebind({k: v for k, v in c.items() if k != "changeset"})

T = c["termination"]
T["terminal_states"] = ["ARCHIVE_MERGED_READBACK_PASS", "ARCHIVE_READY_HOLD", "PARTIAL", "TEMP_CLOSED", "FAIL"]

(OUT / "prompt-contract.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote prompt-contract.json bytes=", (OUT / "prompt-contract.json").stat().st_size)
print("task_id:", c["task_id"], "| reviewed families:", len(c["source_scan"]["reviewed"]),
      "| authority sources:", len(c["authority"]["sources"]), "| journeys:", len(c["journeys"]))
print("claim_ceiling:", I["claim_ceiling"], "| class:", C["class"])
stale = []
blob = json.dumps(c, ensure_ascii=False)
for tok in ["FAR-20261019-owner-authorized-closure", "eight candidate evidence", "FAR-20261016-018-r7r11"]:
    if tok in blob:
        stale.append(tok)
print("stale identity tokens still present:", stale)
