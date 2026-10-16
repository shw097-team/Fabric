#!/usr/bin/env python
"""Merge W1 + W2 + the ruling's action set into ONE machine-readable residual register.

Every count in the output is computed from the inputs, never typed by hand.
"""
import json, hashlib, datetime, collections
from pathlib import Path

RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
PREV = Path("C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016")

w1 = json.loads((RD / "W1_RESIDUAL_UNIVERSE.json").read_text(encoding="utf-8"))
w2 = json.loads((RD / "W2_DEFECT_DOSSIER.json").read_text(encoding="utf-8"))

# Actions the ruling marks executable-now, with the artifact each one must leave behind.
ACTIONS = {
    "A1": {"title": "OS-enforced checker isolation harness (fail-able)", "priority": "P0",
           "closes": "mechanism half of EIA-20261016-02 / R7-03", "artifact": "writer/checker_isolation_probe.py",
           "residual_after": "an immutable, non-liftable boundary still needs a distinct OS identity (owner-gated OG6)"},
    "A2": {"title": "de-vacuum the previous round's S8b check", "priority": "P1",
           "closes": "SELF-CHECK-NONVacutiy (found by W1)", "artifact": "writer/self_check_v2.py"},
    "A3": {"title": "reconstruct the skill index from verified pointers (partial)", "priority": "P1",
           "closes": "EIA-20261016-07 dangling reference", "artifact": "writer/entry_map.json",
           "residual_after": "the original index's full field set is unrecoverable from the pointers alone"},
    "A4": {"title": "mutable-subject metadata semantics", "priority": "P2",
           "closes": "MUTABLE-SOURCE-HASH-METADATA (errata E2)", "artifact": "writer/METADATA_SEMANTICS_V2.json"},
    "A5": {"title": "de-vacuum the presence indicator", "priority": "P2",
           "closes": "CROSS-INDEX-PRESENCE-NONVacutiy (errata E4)", "artifact": "writer/CROSS_INDEX_V2.json"},
    "A6": {"title": "register + ruling + handover + single evidence MD + publish/readback", "priority": "P0",
           "closes": "the round's own closeout/handover obligation", "artifact": "publish/payload/EVIDENCE_CLOSURE_FAR-20261016-018.md"},
}
EXECUTED = {k: {"evidence_present": (RD / v["artifact"]).exists(), "artifact": v["artifact"]}
            for k, v in ACTIONS.items()}

OG = {
    "OG1": "peer chain #6/#8/#10 merge", "OG2": "R7-02 validator cross-repo code promotion",
    "OG3": "R7-04 Fresh G1 owner certificate", "OG4": "canonical codex_executable pin repair",
    "OG5": "KP R04 polarity (20 clauses) + source#6 status", "OG6": "immutable checker boundary (distinct OS identity)",
    "OG7": "PR #12 promotion out of draft", "OG8": "guard predicate precision (runtime plane)",
}

reg = {
    "schema": "FAR-20261016-018/RESIDUAL-REGISTER/1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "round": "FAR-20261016-018-r7r11-residual-closure-and-handover",
    "claim_ceiling": "LOCAL",
    "nonclaims": [
        "no acceptance-report finding is claimed closed except those this register names as closed",
        "the checker boundary demonstrated in A1 is ordinary OS denial, not an immutable boundary",
        "no merge, release, cross-repo promotion or canonical control-plane edit was performed by this round",
        "external acceptance remains with a real acceptance officer; canonical_AO_acceptance stays NOT_ISSUED",
    ],
    "inputs": {
        "W1": {"path": "W1_RESIDUAL_UNIVERSE.json",
               "sha256": hashlib.sha256((RD / "W1_RESIDUAL_UNIVERSE.json").read_bytes()).hexdigest(),
               "items_as_reported": w1.get("counts")},
        "W2": {"path": "W2_DEFECT_DOSSIER.json",
               "sha256": hashlib.sha256((RD / "W2_DEFECT_DOSSIER.json").read_bytes()).hexdigest(),
               "defects_as_reported": len(w2.get("defects", []))},
    },
    "recomputed_counts": {
        "w1_items_total": len(w1.get("items", [])),
        "w1_by_kind": dict(collections.Counter(i.get("kind") for i in w1.get("items", []))),
        "w1_by_authority": dict(collections.Counter(i.get("authority_needed") for i in w1.get("items", []))),
        "w1_agent_executable_open": [i["id"] for i in w1.get("items", [])
                                     if i.get("authority_needed") == "agent-executable-now"
                                     and i.get("kind") != "CLOSED_ALREADY"],
        "w2_defects": len(w2.get("defects", [])),
        "w2_confirmed_defects": sum(1 for d in w2.get("defects", []) if d.get("class") == "CONFIRMED_DEFECT"),
    },
    "executable_now_actions": {
        "actions": ACTIONS, "evidence_present_at_registration": EXECUTED,
        "all_evidence_present": all(v["evidence_present"] for v in EXECUTED.values()),
    },
    "owner_gated": OG,
    "previous_round_state": {
        "main_sha": "312baa0ee2aa591000959cc878bb978a31c89796",
        "evidence_chain_merged": {"4": "12cdeefe5ff5", "5": "b03962313596", "7": "c1debccd8bd0",
                                  "9": "74431eb24564", "11": "312baa0ee2aa"},
        "peer_chain_open": [6, 8, 10], "packet_pr": 12, "packet_draft": True,
    },
    "final_verdicts": {"full_convergence_verdict": "TEMP_CLOSED_CHALLENGE",
                       "production_verdict": "FAIL_CLOSED", "canonical_AO_acceptance": "NOT_ISSUED"},
}
(RD / "RESIDUAL_REGISTER.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(reg["recomputed_counts"], ensure_ascii=False, indent=1))
print("evidence present:", json.dumps(EXECUTED, ensure_ascii=False))
print("all present:", reg["executable_now_actions"]["all_evidence_present"])
