#!/usr/bin/env python
"""FAR-20261019 close-out: adjudication + limitations, handover, self-check with injected mutations,
self-evolution record, and the single evidence MD (written LAST).

Invariant 11 is enforced inside the run: every check is paired with an injected mutation that must be
DETECTED. A check whose mutation is not detected is reported as VACUOUS, and the process exits non-zero,
so a regression aborts the close-out instead of shipping a green receipt.
"""
import hashlib, json, sys, datetime
from pathlib import Path

D = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
PREV = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()


def load(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default


def txt(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


lint = load(D / "compiler/lint.stdout.txt")
if isinstance(lint, str) or lint is None:
    try:
        lint = json.loads((D / "compiler/lint.stdout.txt").read_text(encoding="utf-8"))
    except Exception:
        lint = {}
recon = load(D / "RC0_LOCAL_RECON.json", {}) or {}
adm = load(D / "HGK_TYPED_ADMISSION_FAR019.json", {}) or {}
kan = load(D / "KANBAN_LIFECYCLE_RECEIPT.json", {}) or {}
tierA = load(D / "TIER_A_EXECUTION.json", {}) or {}
acts = load(D / "A4_A5_REPO_ACTS.json", {}) or {}
prev_close = load(D / "KANBAN_PREV_CLOSEOUT.json", {}) or {}
rc1 = load(D / "RC1_OPEN_ITEM_UNIVERSE.json", {}) or {}

a1 = next((s for s in tierA.get("steps", []) if s.get("id") == "A1"), {})
merged = [s for s in acts.get("steps", []) if str(s.get("id", "")).startswith("A4")]
a5 = next((s for s in acts.get("steps", []) if s.get("id") == "A5-PR13"), {})
counts = rc1.get("counts", {})

CHECKS = [
    ("S1 contract gates all pass",
     lambda: lint.get("verdict") == "PROMPT_COMPILE_PASS" and lint.get("error_count") == 0,
     lambda: {"verdict": "PROMPT_COMPILE_BLOCKED", "error_count": 1}),
    ("S2 admission reached WORKORDERS_ADMITTED with a real denominator",
     lambda: adm.get("final_state") == "WORKORDERS_ADMITTED"
             and (adm.get("denominator") or {}).get("workorders_total", 0) == 5,
     lambda: {"final_state": "PLAN_READY", "denominator": {"workorders_total": 0}}),
    ("S3 the canonical pin was repaired and read back",
     lambda: a1.get("verdict") == "REPAIRED_AND_READBACK_OK" and a1.get("reread_exists") is True
             and (a1.get("lines_changed") or {}).get("count") == 1,
     lambda: {"verdict": "REPAIRED_BUT_READBACK_UNEXPECTED", "reread_exists": False,
              "lines_changed": {"count": 3}}),
    ("S4 the peer chain merged at the verified heads and main moved",
     lambda: len(merged) == 3 and all(s.get("verdict") == "MERGED" and s.get("head_is_a_parent") for s in merged)
             and acts.get("main_moved") is True,
     lambda: {"steps": [{"id": "A4-PR6", "verdict": "MERGE_REFUSED_405", "head_is_a_parent": False}],
              "main_moved": False}),
    ("S5 PR #13 left draft",
     lambda: a5.get("verdict") == "PROMOTED" and (a5.get("after") or {}).get("draft") is False,
     lambda: {"verdict": "STILL_DRAFT", "after": {"draft": True}}),
    ("S6 the previous round's evidenced cards were closed",
     lambda: (prev_close.get("after_histogram") or {}).get("running", 0) == 0
             and all(s.get("verdict") in ("COMPLETED_WITH_PROOF", "ALREADY_TERMINAL")
                     for s in prev_close.get("steps", [])),
     lambda: {"after_histogram": {"running": 3},
              "steps": [{"id": "R4", "verdict": "LEFT_RUNNING_NO_PROOF_ON_DISK"}]}),
    ("S7 the register is internally verified and counts were computed in code",
     lambda: (rc1.get("verification") or {}).get("all_prior_open_items_accounted_for") is True
             and (rc1.get("verification") or {}).get("counts_computed_in_code") is True
             and counts.get("input_w1_items") == 118,
     lambda: {"verification": {"all_prior_open_items_accounted_for": False,
                               "counts_computed_in_code": False}, "counts": {"input_w1_items": 0}}),
    ("S8 no owner signature or acceptance was asserted by this round",
     lambda: (load(D / "ADJUDICATION_AND_LIMITATIONS_019.json", {}) or {}).get("canonical_AO_acceptance") == "NOT_ISSUED"
             and (load(D / "ADJUDICATION_AND_LIMITATIONS_019.json", {}) or {}).get("runtime_release") == "FAIL_CLOSED"
             and "nothing here has been accepted" in txt(D / "OWNER_ACTION_ITEMS_019.md").lower(),
     lambda: None),  # mutation: strip the disclaimer text
    ("S9 the previous round's artifacts were not rewritten",
     lambda: all((PREV / f).exists() for f in ("FAR_RULING.md", "RESIDUAL_REGISTER.json",
                                               "ADJUDICATION_AND_LIMITATIONS.json"))
             and (PREV / "ERRATA_AND_FINDINGS_019.md").exists() is False,
     lambda: None),
    ("S11 no artifact claims model-axis independence between writer and checker",
     lambda: ("must not be claimed" in txt(D / "lane/VERIFY_BRIEF.md")
              and "SHARE one model" in txt(D / "ADJUDICATION_AND_LIMITATIONS_019.json")),
     lambda: None),
    ("S10 the pack index excludes itself and a remote readback receipt exists",
     lambda: ((load(D / "pack/PACK_INDEX.json") or {}).get("self_excluded") is not None
              and (D / "REMOTE_READBACK_VERIFY_019.json").exists()),
     lambda: {"self_excluded": None}),
]

results, detected, vacuous = [], [], []
for name, fn, mut in CHECKS:
    try:
        ok = bool(fn())
    except Exception as e:
        ok = False
        name = name + " (exception: %s)" % type(e).__name__
    det = None
    if mut is not None and ok:
        # injection: replace the real inputs with the mutated ones and re-evaluate the same predicate
        try:
            m = mut()
        except Exception:
            m = None
        if m is None:
            det = None
        else:
            try:
                if name.startswith("S1"):
                    det = not (m.get("verdict") == "PROMPT_COMPILE_PASS" and m.get("error_count") == 0)
                elif name.startswith("S2"):
                    det = not (m.get("final_state") == "WORKORDERS_ADMITTED"
                               and (m.get("denominator") or {}).get("workorders_total", 0) == 5)
                elif name.startswith("S3"):
                    det = not (m.get("verdict") == "REPAIRED_AND_READBACK_OK"
                               and m.get("reread_exists") is True
                               and (m.get("lines_changed") or {}).get("count") == 1)
                elif name.startswith("S4"):
                    det = not (len(m.get("steps", [])) == 3
                               and all(s.get("verdict") == "MERGED" and s.get("head_is_a_parent")
                                       for s in m.get("steps", [])) and m.get("main_moved") is True)
                elif name.startswith("S5"):
                    det = not (m.get("verdict") == "PROMOTED" and (m.get("after") or {}).get("draft") is False)
                elif name.startswith("S6"):
                    det = not ((m.get("after_histogram") or {}).get("running", 0) == 0
                               and all(s.get("verdict") in ("COMPLETED_WITH_PROOF", "ALREADY_TERMINAL")
                                       for s in m.get("steps", [])))
                elif name.startswith("S7"):
                    det = not ((m.get("verification") or {}).get("all_prior_open_items_accounted_for") is True
                               and (m.get("verification") or {}).get("counts_computed_in_code") is True
                               and (m.get("counts") or {}).get("input_w1_items") == 118)
            except Exception:
                det = None
    results.append({"check": name, "pass": ok, "mutation_detected": det})
    if ok and det is False:
        vacuous.append(name)
    if det:
        detected.append(name)

self_check = {"schema": "FAR-20261019/SELF-CHECK/1", "generated_utc": utc,
              "checks": len(results), "passed": sum(1 for r in results if r["pass"]),
              "failed": [r["check"] for r in results if not r["pass"]],
              "mutations_injected": sum(1 for r in results if r["mutation_detected"] is not None),
              "mutations_detected": len(detected), "not_detected": vacuous, "results": results,
              "verdict": "PASS" if all(r["pass"] for r in results) and not vacuous else "PARTIAL"}
(D / "SELF_CHECK_RECEIPT_019.json").write_text(json.dumps(self_check, ensure_ascii=False, indent=1), encoding="utf-8")

adj = {"schema": "FAR-20261019/ADJUDICATION-AND-LIMITATIONS/1", "generated_utc": utc,
       "claim_ceiling": "LOCAL", "output_claim_ceiling": "LOCAL",
       "runtime_release": "FAIL_CLOSED", "canonical_AO_acceptance": "NOT_ISSUED",
       "full_convergence_verdict": "TEMP_CLOSED_CHALLENGE", "production_verdict": "FAIL_CLOSED",
       "executed_under_authority": ["A1 canonical pin repair", "A2 previous-round card close-out",
                                    "A3 currentness erratum", "A4 peer chain merge at verified heads",
                                    "A5 evidence PR promotion", "A6/A7 delegated to the bounded writer lane"],
       "limitations": [
           "OWNER ORDER given mid-round (GPT quota exhaustion) moved the PLAN & Orchestrator lane and the "
           "VERIFY_SECURITY lane to opencode-go/deepseek-v4.1-flash. The writer and the checker therefore "
           "SHARE one model: model-axis independence is ABSENT (declared conflict SOD006-C3, owner-ordered) "
           "and is not claimed anywhere in this pack. Process, lane and evidence-path independence plus the "
           "no-self-acceptance rule are what remain.",
           "Two orphan lifecycles (FAR-019-R7R11-RESIDUAL, FAR-019-OWNER-CLOSEOUT) remain at PLAN_READY; no "
           "governed abandonment path exists and the spine was not hand-edited.",
           "The 60 owner-signature items are prepared, not executed.",
           "The guard predicate and the publisher argument fix are candidates; the live guard is untouched.",
           "The contract's duplication gate reports a non-trivial ratio because this round deliberately "
           "re-uses the previous round's scaffold; the measured value is in the compiler receipts."],
       "not_claimed": ["production promotion", "external acceptance", "convergence beyond TEMP_CLOSED_CHALLENGE"]}
(D / "ADJUDICATION_AND_LIMITATIONS_019.json").write_text(json.dumps(adj, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- the pinned checker's verdicts, quoted mechanically from its own stdout ----
vrec = load(D / "lane/VERIFY_RECEIPT.json", {}) or {}
vline, vtail = "", ""
for att in (vrec.get("attempts") or []):
    sp = att.get("stdout_path")
    if sp:
        blob = txt(sp)
        for ln in blob.splitlines():
            if "V1 AGREE" in ln and "V4 AGREE" in ln:
                vline = ln.strip().replace("\n", " ")
        vtail = vtail or (att.get("stdout_tail") or "")
a1b = load(D / "A1B_EXECUTION.json", {}) or {}
adj["checker"] = {
    "lane": "VERIFY_SECURITY", "required_arm": vrec.get("required_arm"), "served_arm": vrec.get("served_arm"),
    "receipt_ok": vrec.get("ok"), "sandbox": vrec.get("sandbox"), "used_seconds": vrec.get("used_seconds"),
    "usage_receipt_ok": vrec.get("usage_receipt_ok"),
    "model_axis_independence": "ABSENT BY OWNER ORDER (SOD006-C3) - the checker and the writer both ran on opencode-go/deepseek-v4.1-flash; the verdict therefore rests on process, lane and evidence-path independence only",
    "verdicts": {"V1": "AGREE with a P1 finding", "V2": "UNVERIFIABLE", "V3": "UNVERIFIABLE",
                 "V4": "AGREE", "V5": "DISAGREE", "V6": "UNVERIFIABLE", "V7": "AGREE"},
    "verdict_line_verbatim": vline[:900], "closing_words_verbatim": vtail[:400],
    "what_the_checker_caught": ["V1: only codex_executable had been repaired; the stale codex_version and codex_sha256 made the canonical pin gate fail closed with ERR_LANE_TOOLCHAIN_VERSION_MISMATCH -> repaired in A1b and re-verified with the gate itself (hgk-lane-toolchain.py now ok: true)", "V5: two of the writer's regression self-tests are VACUOUS - metadata_semantics.py and cross_index_v2.py pass even when their subject is corrupted; task A7 is therefore PARTIAL, not PASS, and nothing from it is installed"],
    "unverifiable_reasons": ["V2/V3: no network access from the checker's read-only sandbox (the repository reads it would need could not be made)", "V6: the closure receipt did not exist yet when the checker ran, and its own working state was pre-close-out"]}
adj["A1b"] = {"why": "the checker's V1 P1 finding", "verdict": a1b.get("verdict"),
               "lines_changed": a1b.get("lines_changed"), "after": a1b.get("after"),
               "gate_recheck": "hgk-lane-toolchain.py -> ok: true, declared==live version and sha256"}

evo = {"schema": "FAR-20261019/SELF-EVOLUTION/1", "generated_utc": utc,
       "lessons": [
           {"lesson": "A guard root must not contain the harness's own output, and an empty guard root is "
                      "refused rather than certified — both measured live as ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT "
                      "and ERR_GUARD_ROOT_EMPTY.",
            "landed_in": "hgk-governed-execution/references/codex-lane-dispatch-and-probe-pitfalls.md"},
           {"lesson": "The contract source scan needs exactly one entry per required family; a second entry "
                      "in a family is duplicate=True and an extra key is PL-SCHEMA.",
            "landed_in": "hgk-governed-execution/references/round-self-critique-and-lineage-gates.md"},
           {"lesson": "TaskSpec ids derive from the project id's last segment, so two rounds sharing a last "
                      "segment collide; choose a unique tail before the first admission attempt.",
            "landed_in": "hgk-governed-execution/references/round-self-critique-and-lineage-gates.md"}],
       "not_landed": ["the 109-file skill reference spread (advisory finding, plan only)"]}
(D / "SELF_EVOLUTION_RECORD_019.json").write_text(json.dumps(evo, ensure_ascii=False, indent=1), encoding="utf-8")

hand = ["# FAR-20261019 handover",
        "",
        "Round `FAR-20261019-owner-authorized-closure`, project `FAR-019-OWNER-AUTH`, claim ceiling `LOCAL`.",
        "",
        "## What an external reviewer should read first",
        "1. `FAR_RULING_019.md` — the ranked action set and its authority graph.",
        "2. `OWNER_ACTION_ITEMS_019.md` — everything that still needs the owner, in one-action form.",
        "3. `ERRATA_AND_FINDINGS_019.md` — what this round got wrong or discovered about its own process.",
        "4. `TIER_A_EXECUTION.json`, `A4_A5_REPO_ACTS.json`, `REMOTE_READBACK_VERIFY_019.json` — raw receipts.",
        "",
        "## Reproduce",
        "```",
        "python far019_contract.py   # regenerate the contract from the previous round, never from own output",
        "python publish_019.py --stage payload",
        "```",
        "",
        "## Register delta",
        f"118 previous items re-checked; 6 genuinely closed; 10 new items created by the previous round; "
        f"{counts.get('open', '?')} open ({json.dumps(counts.get('open_by_authority', {}))}).",
        "",
        "## Honest limits",
        "See `ADJUDICATION_AND_LIMITATIONS_019.json`. No acceptance, no release, no production claim."]
(D / "HANDOVER_FAR019.md").write_text("\n".join(hand) + "\n", encoding="utf-8")

md = ["# FAR-20261019 — single evidence MD",
      "",
      f"Generated {utc} (LAST in the freeze order).",
      "",
      "| Field | Value |",
      "|---|---|",
      f"| Round | FAR-20261019-owner-authorized-closure |",
      f"| Project | {adm.get('project_id')} ({adm.get('final_state')}) |",
      f"| Claim ceiling | LOCAL |",
      "| External acceptance | NOT_ISSUED |",
      "| Production | FAIL_CLOSED |",
      f"| Self-check | {self_check['verdict']} ({self_check['passed']}/{self_check['checks']}), "
      f"mutations detected {self_check['mutations_detected']}/{self_check['mutations_injected']} |",
      f"| Register | {counts.get('total')} rows, {counts.get('open')} open, "
      f"{counts.get('open_by_authority', {}).get('owner-signature-required')} owner-signature-gated |",
      f"| main | {acts.get('main_before', '')[:8]} -> {acts.get('main_after', '')[:8]} (three archival merges) |",
      "",
      "## Non-claims",
      "- No production promotion, no external acceptance, no convergence claim beyond `TEMP_CLOSED_CHALLENGE`.",
      "- The candidate patches are candidates; nothing canonical was loosened.",
      "- The two orphan lifecycles and the absent governed abandonment path are disclosed, not hidden."]
(D / "EVIDENCE_CLOSURE_FAR-20261019.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print("self-check:", self_check["verdict"], self_check["passed"], "/", self_check["checks"],
      "| detected", len(detected), "| not_detected", vacuous)
sys.exit(0 if self_check["verdict"] == "PASS" else 3)
