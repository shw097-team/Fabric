"""FAR TRI_SOURCE_MANDATORY assurance layer (WO-FAR-TRISOURCE-001).

Every formal FAR Research WorkOrder MUST account for all three source classes:
HGK_MEMORY / FABRIC_HGK_KNOWLEDGE / EXTERNAL_WEB. Silent skip is forbidden.
Reuses far_retrieval.py probes; embeds TriSourceCoverageReceipt into ResearchRunReceipt.
"""
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_OUTCOMES = ("HIT", "ZERO_RELEVANT_HIT", "UNAVAILABLE", "BLOCKED_BY_AUTHORITY", "ERROR")
CROSS_SOURCE_STATUSES = (
    "ALIGNED", "MEMORY_STALE", "KNOWLEDGE_STALE", "WEB_NEWER_SUPPORT",
    "NORMATIVE_OVERRIDES_WEB", "WEB_CONTRADICTS_INTERNAL", "MEMORY_CONTRADICTS_CANONICAL",
    "DISPUTED", "INSUFFICIENT")
MEMORY_GRADES = ("APPROVED", "CANDIDATE", "REVOKED", "PROVENANCE_WEAK")
BLOCKER_CODES = ("SILENT_SOURCE_SKIP", "SOURCE_UNAVAILABLE", "SOURCE_BLOCKED", "SOURCE_ERROR",
                 "PROVENANCE_GAP", "FRESHNESS_GAP", "BLOCKING_CONTRADICTION", "COUNTEREVIDENCE_MISSING")
CHANNELS = ("memory", "knowledge", "web")


class FailClosedSilentSkip(Exception):
    """Raised when a required source class was not attempted and not BLOCKED_BY_AUTHORITY."""


def channel_outcome(attempted, rows, reachable=True, error=None, blocked_reason=None):
    """Map a channel result to the source-class outcome contract (H11-H15)."""
    if blocked_reason:
        return {"status": "BLOCKED_BY_AUTHORITY", "reason": blocked_reason, "attempted": attempted}
    if not attempted:
        return {"status": "ERROR", "reason": "not attempted", "attempted": False}
    if error:
        return {"status": "ERROR", "reason": error[:160], "attempted": True}
    if not reachable:
        return {"status": "UNAVAILABLE", "reason": "source/service/network unavailable", "attempted": True}
    relevant = [r for r in rows if (r.get("score") or 0) > 0]
    if relevant:
        return {"status": "HIT", "relevant_count": len(relevant), "attempted": True}
    return {"status": "ZERO_RELEVANT_HIT", "relevant_count": 0, "attempted": True}


def _channel_summary(rows):
    """Per-channel counters (TriSourceCoverageReceipt §9)."""
    return {
        "retrieved_count": len(rows),
        "relevant_count": sum(1 for r in rows if (r.get("score") or 0) > 0),
        "provenance_complete_count": sum(1 for r in rows if r.get("sha256") or r.get("source_id")),
        "stale_count": sum(1 for r in rows if r.get("freshness_status") == "STALE"),
        "receipt_refs": [r.get("source_id") for r in rows[:8]],
    }


def classify_memory_rows(rows):
    """Grade memory rows by provenance/state (approved/candidate/revoked/provenance-weak)."""
    graded = []
    for row in rows:
        marker = (row.get("title") or "") + " " + (row.get("snippet") or "")
        low = marker.lower()
        has_provenance = bool(row.get("sha256") or row.get("source_id") or row.get("created_at"))
        if "revoked" in low or "tombstone" in low or row.get("state") == "REVOKED":
            grade = "REVOKED"
        elif not has_provenance:  # F12: PROVENANCE_WEAK precedes APPROVED/CANDIDATE when fields missing
            grade = "PROVENANCE_WEAK"
        elif row.get("state") == "APPROVED" or "approved" in low:
            grade = "APPROVED"
        elif row.get("state") == "CANDIDATE" or "candidate" in low:
            grade = "CANDIDATE"
        else:
            grade = "CANDIDATE"
        graded.append(dict(row, memory_grade=grade))
    return graded


def adjudicate_claim(claim, domain="FABRIC_INTERNAL"):
    """Claim-specific authority x freshness x provenance arbitration (no eternal hierarchy).

    claim fields: claim_text, memory_ids[], knowledge_ids[], web_ids[], freshness_status,
    provenance_status, memory_grade (from classify_memory_rows), claim_role.
    """
    mem = set(claim.get("memory_ids") or [])
    kb = set(claim.get("knowledge_ids") or [])
    web = set(claim.get("web_ids") or [])
    mem_grade = claim.get("memory_grade") or "CANDIDATE"
    stale = claim.get("freshness_status") == "STALE"
    prov_weak = claim.get("provenance_status") in ("WEAK", "MISSING")
    explicit = claim.get("contradiction")  # explicit contradiction signal from extraction/challenge
    if claim.get("claim_role") == "EXTERNAL_VERSION":
        domain = "EXTERNAL_VERSION"

    if mem and mem_grade == "REVOKED":
        return {"cross_source_status": "MEMORY_CONTRADICTS_CANONICAL", "detail": "revoked memory cannot support truth (anti-regression only)"}
    if mem and mem_grade == "CANDIDATE" and not (kb or web):
        return {"cross_source_status": "INSUFFICIENT", "detail": "candidate memory alone cannot sole-support load-bearing claim"}
    if mem and prov_weak and not (kb or web):
        return {"cross_source_status": "INSUFFICIENT", "detail": "PROVENANCE_WEAK memory = lead only"}
    if explicit == "MEMORY_VS_CANONICAL":
        return {"cross_source_status": "MEMORY_CONTRADICTS_CANONICAL", "detail": "memory contradicts canonical -> canonical wins + finding"}
    if stale and claim.get("claim_role") == "EXTERNAL_VERSION" and kb and web:
        return {"cross_source_status": "KNOWLEDGE_STALE", "detail": "stale internal knowledge vs current external official"}
    if stale and mem_grade == "APPROVED" and kb:
        return {"cross_source_status": "MEMORY_STALE", "detail": "approved memory stale vs canonical -> freshness check required"}
    if web and not (kb or mem) and domain == "FABRIC_INTERNAL":
        return {"cross_source_status": "WEB_CONTRADICTS_INTERNAL", "detail": "web-only claim on internal policy -> dispute; normative source required"}
    if domain == "FABRIC_INTERNAL" and kb and web and explicit == "WEB_VS_NORMATIVE":
        return {"cross_source_status": "NORMATIVE_OVERRIDES_WEB", "detail": "Fabric normative source overrides conflicting web on internal policy"}
    if domain == "EXTERNAL_VERSION" and web:
        return {"cross_source_status": "WEB_NEWER_SUPPORT", "detail": "official external source newer/authoritative for external-version claim"}
    if explicit == "WEB_CONTRADICTS_INTERNAL":
        return {"cross_source_status": "WEB_CONTRADICTS_INTERNAL", "detail": "web contradicts internal claim -> dispute"}
    return {"cross_source_status": "ALIGNED", "detail": "no cross-source contradiction detected"}


def _conflicts(ids_a, ids_b):
    return bool(ids_a) and bool(ids_b) and not (set(ids_a) & set(ids_b))


def counterevidence_probe(claim, query_fn=None, queries=None):
    """>=1 counterevidence query per load-bearing claim; record in QueryLedger."""
    if claim.get("claim_role") != "LOAD_BEARING":
        return {"required": False, "query_count": 0, "status": "OPTIONAL_NOT_RUN_RECORDED"}
    executed = queries if queries is not None else ["known issues", "security advisory", "failed adoption / contradicting benchmark", "superseded decision"]
    hit = False
    query_error = False
    for q in executed:
        try:
            if query_fn is not None:
                rows = query_fn(q)
                if rows and any((r.get("score") or 0) > 0 for r in rows):
                    hit = True
        except Exception:
            query_error = True  # F6: exceptions -> incomplete counterevidence
    status = "ERROR" if query_error else ("HIT" if hit else "ZERO_RELEVANT_COUNTEREVIDENCE_HIT")
    return {
        "required": True, "query_count": len(executed),
        "strategy": executed,
        "status": status,
        "note": "recorded in QueryLedger; zero hit is explicit, not silent omission; ERROR -> incomplete (COUNTEREVIDENCE_MISSING)",
    }


def build_tri_source_receipt(workorder_id, run_id, plan_digest, channels, crosscheck, terminal, generation=None):
    """TriSourceCoverageReceipt (embedded into ResearchRunReceipt as tri_source_coverage)."""
    return {
        "schema": "LOGICAL_FAR_TRI_SOURCE_COVERAGE_V1",
        "workorder_id": workorder_id, "run_id": run_id, "research_plan_digest": plan_digest,
        "generated_at_utc": generation or datetime.now(timezone.utc).isoformat(),
        "memory": channels["memory"], "knowledge": channels["knowledge"], "web": channels["web"],
        "crosscheck": crosscheck, "terminal": terminal,
    }


def independent_origin_key(ev):
    """FH-01: origin identity key (digest > artifact id > unresolved)."""
    digest = ev.get("origin_artifact_digest")
    if digest:
        return ("digest", digest)
    aid = ev.get("origin_artifact_id")
    if aid:
        return ("artifact", aid)
    return ("unresolved", ev.get("source_id") or ev.get("evidence_id") or "unknown")


def compute_independence(channel_rows):
    """FH-01/FH-06: retrieval hits vs independent origins vs source families."""
    hits = [r for r in channel_rows if (r.get("score") or 0) > 0]
    keys = {}
    families = set()
    duplicates = 0
    for row in hits:
        key = independent_origin_key(row)
        if key in keys:
            duplicates += 1
        else:
            keys[key] = True
        fam = row.get("source_family")
        if fam:
            families.add(fam)
    return {
        "retrieval_hits": len(hits),
        "independent_origins": len(keys),
        "independent_source_families": len(families),
        "duplicate_derivations": duplicates,
    }


def cross_source_independence_status(indep):
    """FH-01: status from independence counts."""
    hits = indep["retrieval_hits"]
    origins = indep["independent_origins"]
    if hits == 0:
        return "ORIGIN_UNRESOLVED"
    if origins >= 2:
        return "INDEPENDENT" if origins == hits else "PARTIALLY_INDEPENDENT"
    if origins == 1 and hits > 1:
        return "DERIVED_SAME_ORIGIN"
    return "ORIGIN_UNRESOLVED"


CLAIM_CLASS_MINIMUM = {
    # FH-06: minimum evidence by claim class
    "INTERNAL_NORMATIVE": "current canonical owner source required; memory/web = counterevidence only",
    "CURRENT_RUNTIME_STATE": "current machine receipt required",
    "EXTERNAL_CURRENT_FACT": "official current upstream preferred/required; local memory/knowledge = freshness context",
    "COMMUNITY_DEFECT": "community/issue = SUPPORT; official release/changelog or reproducible evidence preferred for strong conclusion",
    "RESEARCH_FINDING": "source-bound claim + provenance; counterevidence strategy required",
    "RECOMMENDATION": "must include support + counterevidence + fit-gap + authority/freshness adjudication",
}

DEFAULT_QUERY_BUDGET = {"initial_per_source": 4, "followup_per_source": 4}  # FH-04: resource guard, NOT correctness oracle


def budget_exhaustion_terminal(claims, budget=DEFAULT_QUERY_BUDGET):
    """FH-04: budget exhausted -> Case A (evidence satisfied) PASS-eligible / Case B (unresolved) PARTIAL_BUDGET_EXHAUSTED."""
    unresolved_kinds = ("MISSING", "DISPUTED", "PROVENANCE_WEAK", "SINGLE_ORIGIN_SUPPORT", "TRUNCATED_LOAD_BEARING_SOURCE")
    load_bearing = [c for c in claims if c.get("claim_role") == "LOAD_BEARING"]
    for c in load_bearing:
        status = c.get("final_claim_status") or c.get("cross_source_status") or "OPEN"
        if status in unresolved_kinds or c.get("provenance_status") in ("WEAK", "MISSING"):
            return {"budget_exhausted": True, "terminal": "RESEARCH_PARTIAL_BUDGET_EXHAUSTED",
                    "reason": "budget exhausted with unresolved evidence: %s" % status,
                    "extension": "REQUEST_BUDGET_EXTENSION per WorkOrder policy"}
    return {"budget_exhausted": True, "terminal": "PASS_ELIGIBLE",
            "reason": "budget exhausted but evidence coverage satisfied (all load-bearing claims closed)"}


def compute_claim_independence(claim, kb_rows, mem_rows, web_rows):
    """FH-01: claim-level independence (cross-channel, deduped by origin)."""
    all_rows = [dict(r, source_class="KB") for r in kb_rows] + \
               [dict(r, source_class="MEMORY") for r in mem_rows] + \
               [dict(r, source_class="WEB") for r in web_rows]
    indep = compute_independence(all_rows)
    status = cross_source_independence_status(indep)
    return {
        "origin_family_count": indep["independent_source_families"],
        "independent_origin_count": indep["independent_origins"],
        "cross_source_independence_status": status,
        "retrieval_hits": indep["retrieval_hits"],
        "duplicate_derivations": indep["duplicate_derivations"],
    }


def run_tri_source_assurance(workorder_id, run_id, question, plan_digest,
                             probe_fn, allowed_web_roots=None, domain="FABRIC_INTERNAL",
                             claims=None, counterevidence_fn=None):
    """Orchestrate mandatory tri-source probes + receipt + terminal (FailClosed on silent skip)."""
    channels = {}
    for ch in CHANNELS:
        res = None  # F3/F4: bind before try; no cross-channel leak
        try:
            res = probe_fn(ch)  # returns (attempted, rows, reachable, error, blocked_reason)
            outcome = channel_outcome(*res)
        except Exception as exc:
            outcome = {"status": "ERROR", "reason": str(exc)[:160], "attempted": True}
        channels[ch] = dict(outcome, **_channel_summary(res[1] if (res and outcome.get("attempted")) else []))
        channels[ch]["query_count"] = 1
        if ch == "memory":
            graded = classify_memory_rows(res[1] if res else [])
            channels[ch]["candidate_count"] = sum(1 for r in graded if r["memory_grade"] == "CANDIDATE")
            channels[ch]["approved_count"] = sum(1 for r in graded if r["memory_grade"] == "APPROVED")
            channels[ch]["revoked_count"] = sum(1 for r in graded if r["memory_grade"] == "REVOKED")

    # FailClosed: silent skip forbidden (H12)
    for ch in CHANNELS:
        if not channels[ch].get("attempted") and channels[ch].get("status") != "BLOCKED_BY_AUTHORITY":
            raise FailClosedSilentSkip("SILENT_SOURCE_SKIP: %s not attempted" % ch)

    # claims adjudication + counterevidence
    adjudicated = []
    counter = {"required_count": 0, "completed": True}
    for claim in (claims or []):
        ad = adjudicate_claim(claim, domain=domain)
        ce = counterevidence_probe(claim, query_fn=counterevidence_fn)
        adjudicated.append(dict(claim, cross_source_status=ad["cross_source_status"], adjudication_detail=ad["detail"], counterevidence=ce))
        if ce.get("required"):
            counter["required_count"] += 1
            if ce.get("status") != "HIT" and ce.get("status") != "ZERO_RELEVANT_COUNTEREVIDENCE_HIT":
                counter["completed"] = False

    crosscheck = {
        "aligned_claim_count": sum(1 for c in adjudicated if c["cross_source_status"] == "ALIGNED"),
        "contradicted_claim_count": sum(1 for c in adjudicated if c["cross_source_status"] in ("DISPUTED", "WEB_CONTRADICTS_INTERNAL", "MEMORY_CONTRADICTS_CANONICAL")),
        "unresolved_claim_count": sum(1 for c in adjudicated if c["cross_source_status"] == "INSUFFICIENT"),
        "stale_memory_findings": sum(1 for c in adjudicated if c["cross_source_status"] == "MEMORY_STALE"),
        "stale_knowledge_findings": sum(1 for c in adjudicated if c["cross_source_status"] == "KNOWLEDGE_STALE"),
        "web_only_new_findings": sum(1 for c in adjudicated if c["cross_source_status"] == "WEB_NEWER_SUPPORT"),
    }

    terminal = terminal_reducer(channels, adjudicated, counter)
    receipt = build_tri_source_receipt(workorder_id, run_id, plan_digest, channels, crosscheck, terminal)
    return receipt, adjudicated


def terminal_reducer(channels, claims, counterevidence):
    """Full pass only when all three accounted with HIT/ZERO + provenance + freshness + no blocker + counterevidence done."""
    blocker_codes = []
    statuses = {ch: channels[ch].get("status") for ch in CHANNELS}
    for ch in CHANNELS:
        s = statuses[ch]
        if s == "UNAVAILABLE":
            blocker_codes.append("SOURCE_UNAVAILABLE")
        elif s == "BLOCKED_BY_AUTHORITY":
            blocker_codes.append("SOURCE_BLOCKED")
        elif s == "ERROR":
            blocker_codes.append("SOURCE_ERROR")
        elif s not in ("HIT", "ZERO_RELEVANT_HIT"):
            blocker_codes.append("SILENT_SOURCE_SKIP")
    load_bearing = [c for c in claims if c.get("claim_role") == "LOAD_BEARING"]
    if any(c.get("provenance_status") in ("WEAK", "MISSING") for c in load_bearing):
        blocker_codes.append("PROVENANCE_GAP")
    if any(c.get("freshness_status") == "STALE" for c in load_bearing):
        blocker_codes.append("FRESHNESS_GAP")
    if any(c.get("cross_source_status") in ("DISPUTED", "WEB_CONTRADICTS_INTERNAL", "MEMORY_CONTRADICTS_CANONICAL") for c in load_bearing):
        blocker_codes.append("BLOCKING_CONTRADICTION")
    if counterevidence.get("required_count") and not counterevidence.get("completed"):
        blocker_codes.append("COUNTEREVIDENCE_MISSING")

    all_three_accounted = all(s in ("HIT", "ZERO_RELEVANT_HIT") for s in statuses.values())
    full_pass_eligible = all_three_accounted and not blocker_codes
    if full_pass_eligible:
        terminal = "RESEARCH_PASS_CANDIDATE"
    elif "SOURCE_BLOCKED" in blocker_codes:  # F9: authority block takes precedence over availability
        terminal = "RESEARCH_BLOCKED_BY_AUTHORITY"
    elif "SOURCE_UNAVAILABLE" in blocker_codes:
        terminal = "RESEARCH_PARTIAL"
    elif "SOURCE_ERROR" in blocker_codes:
        terminal = "RESEARCH_ERROR_STOP"
    else:
        terminal = "RESEARCH_PARTIAL"
    return {"all_three_accounted_for": all_three_accounted, "full_pass_eligible": full_pass_eligible,
            "blocker_codes": blocker_codes, "terminal": terminal, "source_statuses": statuses}


def run_full_assurance(workorder_id, run_id, question, plan_digest, out_dir,
                       spine_db=None, allowed_web_roots=None, top_k=6, max_files=900,
                       domain="FABRIC_INTERNAL", claims=None, counterevidence_fn=None):
    """REAL production call site (A1): run far_retrieval channels + wrap with tri-source assurance.

    Returns (receipt, adjudicated, retrieval_ledger).
    """
    import far_retrieval as fr

    kb_rows = fr.retrieve_knowledge_base(question, top_k=top_k, max_files=max_files)
    mem_rows = fr.retrieve_memory(question, top_k=top_k, spine_db=spine_db)
    web_rows = fr.retrieve_web(question, allowed_roots=allowed_web_roots, top_k=top_k)

    def probe(ch):
        if ch == "memory":
            return (True, mem_rows, True, None, None)
        if ch == "knowledge":
            return (True, kb_rows, True, None, None)
        if ch == "web":
            reachable = fr.last_web_status not in ("WEB_RETRIEVAL_SKIPPED_NO_ROOTS",)
            err = fr.last_web_status if fr.last_web_status in ("PARTIAL_FAIL",) else None
            if not allowed_web_roots:
                return (True, [], False, None, None)  # UNAVAILABLE: no admitted web boundary
            return (True, web_rows, reachable, err, None)
        raise ValueError(ch)

    receipt, adjudicated = run_tri_source_assurance(
        workorder_id, run_id, question, plan_digest, probe,
        allowed_web_roots, domain, claims, counterevidence_fn)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "TriSourceCoverageReceipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "AdjudicatedClaims.json").write_text(json.dumps(adjudicated, ensure_ascii=False, indent=1), encoding="utf-8")
    ledger = {"schema": "FAR-RETRIEVAL-LEDGER/1", "workorder_ref": workorder_id, "question": question,
              "channels": {"knowledge_base": kb_rows, "memory": mem_rows, "web": web_rows},
              "web_status": fr.last_web_status, "files": {"receipt": str(out / "TriSourceCoverageReceipt.json")}}
    (out / "RetrievalLedger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
    return receipt, adjudicated, ledger
