#!/usr/bin/env python
"""acceptance_integrity_checks.py — FAR PE-HGK-SWOF-ACCEPTANCE-INTEGRITY-001 (v2 controls).

Additive, deterministic predicates over artifacts the control plane already owns. No new subsystem.
Implements the inventory-INDEPENDENT controls (C2, C3, C4, C5, C6). C1/C7/C8 are gated on the
U1/U2/U3 inventories (which resolved as: no oracle pointer; no monotonic sequence; no compiler digest)
and are therefore specified, not implemented, in this revision.

Every check returns a list of findings; each finding is (check_id, artifact, detail). A check that
cannot run reports a NOT_APPLICABLE finding rather than silently passing - a vacuous pass is a defect.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
POST_TOKENS = ("NEW_EVIDENCE_COMMIT_PUBLISHED", "READY_FOR_W2_EXTERNAL_RECHALLENGE")
# Provenance markers: an artifact under one of these path segments is exempt from current-round rules.
EXEMPT_SEGMENTS = ("historical/", "superseded/", "_SUPERSEDED")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _na(check: str, subject: str, reason: str):
    """A check that cannot run must say so. Returning clean on an unrunnable input is a vacuous pass
    (independent-checker finding: only C7 honoured this before)."""
    return [(f"{check}.NOT_APPLICABLE", subject, reason)]


def _is_exempt(rel: str) -> bool:
    return any(seg in rel for seg in EXEMPT_SEGMENTS)


def _round_token(name: str) -> str | None:
    """Extract a round token like R2 / W2R3 from a filename or path."""
    m = re.search(r"(?:^|[/_\-])(W\d?R\d|R\d)(?=[_\-.]|$)", name)
    return m.group(1) if m else None


# ---------------------------------------------------------------- C3
def c3_cross_round_identity(root: Path, round_of: dict[str, str] | None = None, carried_decls: dict | None = None):
    """C3: newly-authored artifacts of round R must carry R's schema/order identity, a filename round
    consistent with content, and a carried file must be DECLARED carried (not a blanket sha diff).

    Exempt: historical/ and superseded/ paths, and artifacts declared immutable predecessors.
    """
    findings, checked = [], 0
    carried_decls = carried_decls or {}
    if round_of is None:
        _rp = Path(root)
        round_of = {str(f.relative_to(_rp)): (_round_token(str(f.relative_to(_rp))) or "")
                    for f in _rp.rglob("*.json")}
    if round_of is None:
        round_of = {str(f.relative_to(root)): (_round_token(str(f.relative_to(root))) or "")
                    for f in Path(root).rglob("*.json")}
    declared_carried = {"carried", "immutable_predecessor", "immutable", "cumulative_bundle"}
    for f in sorted(root.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(root).as_posix()
        if _is_exempt(rel):
            continue
        rnd = round_of.get(rel) or _round_token(rel)
        if not rnd:
            continue
        checked += 1
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # declared-carried escape hatch (challenge over-breadth finding): an artifact that DECLARES it
        # is a carried/immutable predecessor is exempt, exactly as the control's own contract states.
        try:
            _j = json.loads(txt)
            if any(_j.get(k) is True for k in declared_carried):
                continue
        except Exception:
            pass
        # (a) an explicit repair_id in content must agree with the artifact's own round
        m = re.search(r'"repair_id"\s*:\s*"(SWOF-W2-CLOSURE-[A-Z0-9]+)"', txt)
        if m:
            content_round = m.group(1).rsplit("-", 1)[-1]
            fn_round = rnd.lstrip("W").replace("W", "")
            if content_round not in (fn_round, fn_round.lstrip("R"), fn_round.replace("R", "")):
                findings.append(("C3.repair_id_round_mismatch", rel,
                                 f"content repair_id={m.group(1)} but artifact round={rnd}"))
        # (b) a frozen canonical pack schema literal must name the artifact's own round
        m2 = re.search(r'"schema"\s*:\s*"(SWOF-[A-Z0-9\-]*EVIDENCE-RETURN-PACK/\d)"', txt)
        if m2:
            sch_round = _round_token(m2.group(1))
            if sch_round and sch_round != rnd:
                findings.append(("C3.schema_round_frozen", rel,
                                 f'schema literal {m2.group(1)} frozen at {sch_round}, artifact round {rnd}'))
        # (c) order_id must not be a predecessor order when the artifact names a later round
        m3 = re.search(r'"order_id"\s*:\s*"([^"]+)"', txt)
        if m3 and re.search(r"REPAIR-001$", m3.group(1)) and rnd not in ("R1", "W2R1"):
            findings.append(("C3.order_id_frozen", rel,
                             f'order_id={m3.group(1)} frozen at REPAIR-001 but artifact round={rnd}'))
    if checked == 0:
        return _na("C3", str(root), "no artifact carried a round token - selector matched nothing"), 0
    return findings, checked


# ---------------------------------------------------------------- C4
def c4_handoff_subject_equality(readset: dict, receipt: dict):
    """C4: top-level subject == receipt subject on source and evidence SHA. readset_location excluded;
    a SELF_REFERENTIAL publication_state is a sanctioned design, not a defect."""
    findings = []
    subj = (readset.get("subject") or {})
    if not subj or not receipt:
        return _na("C4", "handoff", "readset/receipt inputs unresolvable - cannot evaluate")
    for k in ("w2_source_candidate_sha", "w2_evidence_commit_sha"):
        rk = k.replace("w2_", "")
        a = subj.get(k)
        b = receipt.get(k) or receipt.get(rk)
        if a and b and a != b:
            findings.append(("C4.subject_mismatch", "readset_vs_receipt", f"{k}: {a} != {b}"))
    ps = (readset.get("publication_state") or {})
    status = str(ps.get("status") or ps.get("w2_evidence_commit_sha_status") or "")
    if "SELF_REFERENTIAL" not in status:
        pushed = (ps.get("pushed") or {})
        _known = {subj.get("w2_source_candidate_sha"), subj.get("w2_evidence_commit_sha"), receipt.get("source_candidate_sha"), receipt.get("evidence_commit_sha")}
        if pushed.get("source") and pushed["source"] not in _known and pushed.get("evidence") not in _known and \
           pushed["source"] != subj["w2_source_candidate_sha"]:
            findings.append(("C4.nested_subject_stale", "readset.publication_state.pushed",
                             f"nested source {pushed['source']} != top-level {subj['w2_source_candidate_sha']}"))
    return findings


# ---------------------------------------------------------------- C5
def c5_descriptor_resolvability(descriptors: list[dict], blob_lookup):
    """C5: key on descriptor PATH + recomputed bytes (NOT on sha alone). Empty-SHA is legal only for a
    genuinely zero-byte blob."""
    if not descriptors:
        return _na("C5", "descriptors", "no descriptors supplied - cannot evaluate (NOT a pass)")
    findings = []
    for d in descriptors:
        path = d.get("path") or d.get("repo_path") or d.get("name")
        declared = d.get("sha256")
        size = d.get("bytes", d.get("size_bytes"))
        blob = blob_lookup(path) if path else None
        if blob is None:
            findings.append(("C5.descriptor_unresolvable", str(path), "declared descriptor resolves to no committed blob"))
            continue
        if declared and _sha(blob) != declared:
            findings.append(("C5.descriptor_sha_mismatch", str(path), f"declared {declared[:12]} != recomputed {_sha(blob)[:12]}"))
        if size is not None and len(blob) != size:
            findings.append(("C5.descriptor_size_mismatch", str(path), f"declared {size} bytes != resolved {len(blob)}"))
        if declared == EMPTY_SHA and len(blob) != 0:
            findings.append(("C5.empty_sha_for_nonempty", str(path), "canonical empty-blob SHA declared for a non-empty artifact"))
        if declared == EMPTY_SHA and size not in (0, None):
            findings.append(("C5.empty_sha_nonzero_size", str(path), f"empty-blob SHA declared with bytes={size}"))
    return findings


# ---------------------------------------------------------------- C2
def c2_minimum_matrix_coverage(required_cases: list[str], receipt: dict):
    """C2: every case in the contract's DECLARED MINIMUM matrix must carry an assertion.

    Coverage is evaluated against the receipt's EXPLICIT covered_cases list. A prose substring match is
    NOT accepted as coverage - the independent checker demonstrated that 'see AAC9 discussion' would
    otherwise count as covered (a false NEGATIVE). Full-cartesian auto-derivation is not required.
    """
    if not required_cases:
        return _na("C2", "contract", "no declared minimum matrix resolvable - cannot evaluate"), 0
    covered = receipt.get("covered_cases")
    if not isinstance(covered, list):
        return _na("C2", "checker_receipt",
                   "receipt exposes no explicit covered_cases list; prose matching is refused as a "
                   "false-negative source"), len(required_cases)
    cov = {str(c) for c in covered}
    missing = [c for c in required_cases if c not in cov]
    return [("C2.minimum_case_uncovered", c, "case listed in the contract minimum matrix but absent from covered_cases")
            for c in missing], len(required_cases)


# ---------------------------------------------------------------- C6
def c6_publication_preflight(artifacts: list[tuple[str, dict]]):
    """C6: a prepublication-typed artifact must not carry postpublication claim tokens while its
    evidence SHA is null; PUBLISHED state requires an IndependentReceipt with verdict PASS."""
    if not artifacts:
        return _na("C6", "artifacts", "no artifacts supplied - cannot evaluate")
    findings = []
    _NEG_WORDS = ("MUST_NOT", "NOT ", "NOT_", "DO_NOT", "NEVER", "SHALL_NOT", "NO_", "WITHOUT")
    for name, a in artifacts:
        raw_ceiling = str(a.get("claim_ceiling") or "")
        # REMOVE negated forms before scanning (challenge over-breadth): a ceiling that explicitly
        # DISCLAIMS a token must not be read as asserting it.
        # a token is NEGATED when a negation marker appears within the preceding window, e.g.
        # 'MUST_NOT_CLAIM_NEW_EVIDENCE_COMMIT_PUBLISHED'. Substring-removal alone is insufficient
        # because the negated form still CONTAINS the token (independent-checker counterexample).
        ceiling = raw_ceiling
        for _tok in POST_TOKENS:
            _i = ceiling.find(_tok)
            while _i != -1:
                _win = ceiling[max(0, _i - 24):_i].upper()
                if any(w in _win for w in _NEG_WORDS):
                    ceiling = ceiling[:_i] + " " * len(_tok) + ceiling[_i + len(_tok):]
                _i = ceiling.find(_tok, _i + 1)
        ev = a.get("w2_evidence_commit_sha")
        for t in POST_TOKENS:
            if t in ceiling and ev in (None, "", "null"):
                findings.append(("C6.postpub_claim_with_null_sha", name, f"claim_ceiling contains {t} while evidence SHA is null"))
        if str(a.get("publication_state")) == "PUBLISHED":
            ir = a.get("independent_receipt") or a.get("checker_receipt") or a.get("checker") or {}
            if ir.get("verdict") != "PASS":
                findings.append(("C6.published_without_checker_pass", name, "publication_state=PUBLISHED with no IndependentReceipt verdict PASS"))
    return findings


if __name__ == "__main__":
    print("module: import and call the C2/C3/C4/C5/C6 predicates")


# =====================================================================================
# C1 / C7 / C8 — the three controls the U1-U3 inventories gated.
# RESOLUTION: none of them requires a DB schema change.
#   C7 uses SQLite's implicit rowid for event order (precedent: src/hg_kseos/evidence_graph.py
#      uses ORDER BY rowid) instead of wall-clock created_at.
#   C1 and C8 add RECEIPT-CONTRACT fields - a validation predicate, not a migration.
# =====================================================================================

# ---------------------------------------------------------------- C7
def c7_admission_precedes_mutation(conn, workorder_id: str) -> list[tuple[str, str, str]]:
    """C7: a candidate mutation must be ordered by EVENT SEQUENCE (rowid), never by wall-clock.

    Reads canonical_events for the entity and asserts the admission/registration event has a strictly
    smaller rowid than the first mutation event. Uses rowid - no schema column is added.
    """
    findings = []
    rows = conn.execute(
        "SELECT rowid, entity_type, entity_id, to_state, actor FROM canonical_events "
        "WHERE entity_id=? ORDER BY rowid", (workorder_id,)).fetchall()
    if not rows:
        return [("C7.NOT_APPLICABLE", workorder_id, "no canonical_events rows for this entity")]
    admit = [r for r in rows if str(r[3]).upper() in ("ADMITTED", "FROZEN", "PLANNED", "BOUND", "CREATED")]
    mut = [r for r in rows if str(r[3]).upper() in ("MUTATING", "APPLIED", "WRITTEN", "COMPLETED")]
    if not admit:
        findings.append(("C7.no_admission_event", workorder_id, "no admission-state event in the sequence"))
    if not mut:
        findings.append(("C7.not_applicable_no_mutation", workorder_id, "no mutation-state event recorded"))
        return findings
    if admit and mut and not (admit[0][0] < mut[0][0]):
        findings.append(("C7.mutation_precedes_admission", workorder_id,
                         f"first mutation rowid={mut[0][0]} <= first admission rowid={admit[0][0]}"))
    findings.append(("C7.ordering_oracle", workorder_id,
                     "rowid (monotonic insertion order); wall-clock created_at is NOT used as the oracle"))
    return findings


def c7_wall_clock_ordering_sites(src_root: Path) -> list[tuple[str, str, str]]:
    """C7 supporting check: find ordering decisions that rely on wall-clock created_at rather than a
    monotonic sequence. These are the sites where the named defect can re-enter."""
    findings = []
    for f in sorted(Path(src_root).rglob("*.py")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(txt.splitlines(), 1):
            if "ORDER BY created_at" in line:
                findings.append(("C7.wall_clock_ordering_site", f"{f.name}:{i}", line.strip()[:120]))
    return findings


# ---------------------------------------------------------------- C1
def c1_oracle_basis_attribution(checker_receipt: dict, name: str = "checker_receipt"):
    """C1: every checker assertion must be attributable to a frozen canonical authority locator.
    NARROWED per challenge: an expected value that legitimately repeats a canonical constant is fine;
    only UNATTRIBUTABLE provenance fails. Requires the receipt to carry `oracle_basis` (U1 gap)."""
    findings = []
    assertions = checker_receipt.get("assertions")
    if assertions is None:
        return [("C1.receipt_lacks_oracle_basis_field", name,
                 "checker receipt carries no per-assertion oracle_basis field (U1 inventory: absent)")]
    if not assertions:
        return _na("C1", name, "no assertions to attribute - cannot evaluate")
    for a in assertions:
        basis = (a or {}).get("oracle_basis")
        if not basis:
            findings.append(("C1.unattributable_expected_value", name,
                             f"assertion {a.get('id','?')} has no oracle_basis"))
    return findings


# ---------------------------------------------------------------- C8(b)
def c8_compiler_identity(compile_receipt: dict, canonical_digest: str | None,
                         name: str = "compile_receipt"):
    """C8(b): the compile receipt must carry a compiler IDENTITY digest, not merely a path.
    U3 inventory: the real receipt carries `compiler_root` (a filesystem path) only."""
    findings = []
    digest = compile_receipt.get("compiler_identity_digest")
    if not digest:
        findings.append(("C8.compiler_identity_digest_absent", name,
                         "receipt carries no compiler_identity_digest; a path cannot prove which compiler bytes ran"))
    elif canonical_digest and digest != canonical_digest:
        findings.append(("C8.compiler_identity_digest_mismatch", name,
                         f"{str(digest)[:12]} != canonical {str(canonical_digest)[:12]}"))
    return findings
