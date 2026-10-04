#!/usr/bin/env python
"""run_fixture.py — exercise the C2/C3/C4/C5/C6 predicates against the REAL SWOF corpus.

Purpose: prove each control (a) catches the NAMED historical findings it claims, and (b) does NOT
false-positive on by-design historical/cumulative artifacts (the challenge lane's BLOCKING concern).

The corpus is the read-only knowledge-base mirror 知識庫/實作相關Doc(SWOF)/驗收證據/{W2,W2R1,W2R2,W2R3,W2R4}.
Blob resolution uses the mirror files themselves (the local stand-in for the committed evidence tree).
"""
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("aic", HERE / "acceptance_integrity_checks.py")
aic = importlib.util.module_from_spec(spec); spec.loader.exec_module(aic)

CORPUS = Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/SWOF/驗收證據")
ROUNDS = ["W2", "W2R1", "W2R2", "W2R3", "W2R4"]

out = {"controls": {}, "false_positive_probe": {}, "notes": []}

# ---------- C3 over the whole corpus ----------
root = CORPUS
findings, checked = aic.c3_cross_round_identity(root, round_of={})
by_type = {}
for cid, art, det in findings:
    by_type.setdefault(cid, []).append({"artifact": art, "detail": det})
exempt = [p.relative_to(root).as_posix() for p in root.rglob("*")
          if p.is_file() and aic._is_exempt(p.relative_to(root).as_posix())]
out["controls"]["C3_cross_round_identity"] = {
    "files_checked": checked, "findings_total": len(findings),
    "by_type": {k: len(v) for k, v in by_type.items()},
    "examples": {k: v[:3] for k, v in by_type.items()},
    "exempt_files_skipped": len(exempt),
    "exempt_examples": exempt[:5]}

# ---------- C5 over every readset present ----------
descs, blob_lookup = [], (lambda p: (root / p).read_bytes() if (root / p).exists() and (root / p).is_file() else None)
readset_files = [p for p in root.rglob("*") if p.is_file() and "READSET" in p.name.upper()]
for rf in readset_files:
    try:
        d = json.loads(rf.read_text(encoding="utf-8"))
    except Exception:
        continue
    # descriptors may be a DICT (name -> {sha256,bytes,...}) or a list; handle both
    for key in ("descriptors", "item_descriptors", "files"):
        raw = d.get(key)
        items = []
        if isinstance(raw, dict):
            for nm, v in raw.items():
                if isinstance(v, dict):
                    v = dict(v); v.setdefault("path", nm); items.append(v)
                elif isinstance(v, str):
                    items.append({"path": nm, "sha256": v})
        elif isinstance(raw, list):
            items = raw
        for item in items:
            if isinstance(item, dict) and item.get("sha256"):
                descs.append({"path": item.get("path") or item.get("repo_path") or item.get("name"),
                              "sha256": item.get("sha256"),
                              "bytes": item.get("bytes", item.get("size_bytes"))})
    for item in (d.get("items") or []):
        if isinstance(item, dict) and item.get("sha256"):
            descs.append({"path": item.get("item") or item.get("repo_path"), "sha256": item.get("sha256"),
                          "bytes": item.get("bytes")})
c5 = aic.c5_descriptor_resolvability(descs, blob_lookup)
c5_types = {}
for cid, art, det in c5:
    c5_types.setdefault(cid, []).append({"artifact": str(art), "detail": det})
out["controls"]["C5_descriptor_resolvability"] = {
    "descriptors_examined": len(descs), "readsets_found": len(readset_files),
    "findings_total": len(c5), "by_type": {k: len(v) for k, v in c5_types.items()},
    "examples": {k: v[:4] for k, v in c5_types.items()}}

# ---------- C6 over every Return Pack ----------
packs = []
for rf in root.rglob("*"):
    if rf.is_file() and "RETURN_PACK" in rf.name.upper():
        try:
            packs.append((rf.relative_to(root).as_posix(), json.loads(rf.read_text(encoding="utf-8"))))
        except Exception:
            pass
c6 = aic.c6_publication_preflight(packs)
out["controls"]["C6_publication_preflight"] = {
    "packs_examined": len(packs), "findings_total": len(c6),
    "findings": [{"artifact": a, "detail": d} for _, a, d in c6]}

# ---------- C4 readset vs its round's publication receipt ----------
c4 = []
for rd in readset_files:
    rnd = next((r for r in ROUNDS if f"/{r}/" in rd.as_posix()), None)
    if not rnd:
        continue
    try:
        readset = json.loads(rd.read_text(encoding="utf-8"))
    except Exception:
        continue
    cands = [p for p in (root / rnd).glob("*PUBLICATION_RECEIPT*.json")]
    if not cands:
        continue
    try:
        receipt = json.loads(cands[0].read_text(encoding="utf-8"))
    except Exception:
        continue
    c4 += [{"round": rnd, "detail": d} for _, _, d in aic.c4_handoff_subject_equality(readset, receipt)]
out["controls"]["C4_handoff_subject_equality"] = {"findings_total": len(c4), "findings": c4}

# ---------- C2 against the R4 declared minimum matrix ----------
r4_receipt_path = CORPUS / "W2R4" / "R4_FRESH_CHECKER_RECEIPT.json"
if r4_receipt_path.exists():
    rec = json.loads(r4_receipt_path.read_text(encoding="utf-8"))
    # declared minimum matrix from the R4 order Gate 2 (A1..A10 as enumerated cases)
    REQUIRED = ["AAC1", "AAC2", "AAC3", "AAC9", "CRITICAL",
                "missing_or_malformed_floor_fails_closed", "strong_authority_does_not_compensate_weak_authn"]
    miss, total = aic.c2_minimum_matrix_coverage(REQUIRED, rec)
    out["controls"]["C2_minimum_matrix_coverage"] = {
        "required_cases": total, "missing": [m[1] for m in miss], "findings_total": len(miss),
        "note": "keys are matched case-insensitively against the receipt JSON; this receipt's own fields are used as the coverage surface"}
else:
    out["controls"]["C2_minimum_matrix_coverage"] = {"NOT_APPLICABLE": "no R4 checker receipt in corpus"}

# ---------- FALSE-POSITIVE PROBE (the challenge's BLOCKING concern) ----------
fp = {}
fp["exempt_tree_exists"] = len(exempt) > 0
fp["C3_findings_inside_exempt_paths"] = sum(1 for _, a, _ in findings if aic._is_exempt(a))
# cumulative W2R1 bundle: does C3 condemn its legitimate self-labelled R1..R4 sub-rounds?
w2r1 = [f for f in findings if f[1].startswith("W2R1/")]
fp["C3_findings_in_W2R1_bundle"] = len(w2r1)
fp["W2R1_examples"] = [{"artifact": a, "detail": d} for _, a, d in w2r1[:5]]
out["false_positive_probe"] = fp

print(json.dumps(out, ensure_ascii=False, indent=1))
(HERE / "fixture_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
