#!/usr/bin/env python
"""run_on_evidence_commit.py — run C3/C5 against the REAL evidence commit (not the KB mirror).

The KB mirror cannot resolve commit-relative descriptor paths, which made the C5 reading invalid.
This runner uses `git cat-file blob` against the SWOF evidence worktree, so descriptor paths resolve
exactly as a control-plane check would see them.

usage: python run_on_evidence_commit.py <evidence_commit_sha>
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("aic", HERE / "acceptance_integrity_checks.py")
aic = importlib.util.module_from_spec(spec); spec.loader.exec_module(aic)

EWT = Path("C:/Projects/Agent_Workspace/SWOF-w2-evidence-wt")
CAND = "6f332c3cedc52bafc98949f4ce9226b1d1696bc3"
ROOT = f"acceptance/evidence/w2r1/{CAND}"


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", str(EWT), *a], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def run(commit: str):
    def read(rel):  # restored: the splice that switched C3 to the shipped predicate removed this helper
        return git("show", f"{commit}:{ROOT}/{rel}", binary=True)
    tree = [l for l in git("ls-tree", "-r", "--name-only", commit, ROOT).splitlines() if l.strip()]
    rels = [t.split(f"{ROOT}/", 1)[-1] for t in tree]
    out = {"evidence_commit": commit, "files_in_root": len(rels)}

    # ---------- C3 over the real committed artifacts (SHIPPED predicate, not an inlined copy) ----------

    # Fidelity fix (independent-checker finding): an earlier revision inlined a reduced C3 that omitted

    # rule (b), so the evidence numbers exercised a divergent subset. Materialise the commit root into a

    # temp tree and call the shipped, tested module instead.

    import tempfile

    c3_findings = []

    with tempfile.TemporaryDirectory() as _td:

        _tdp = Path(_td)

        for _rel in rels:

            _dst = _tdp / _rel

            _dst.parent.mkdir(parents=True, exist_ok=True)

            _dst.write_bytes(git("show", f"{commit}:{ROOT}/{_rel}", binary=True))

        _round_of = {_r: (aic._round_token(_r) or "") for _r in rels}

        c3_findings, checked = aic.c3_cross_round_identity(_tdp, round_of=_round_of)

    out["C3"] = {"files_with_round_token_checked": checked, "findings": len(c3_findings),

                 "by_type": {k: sum(1 for f in c3_findings if f[0] == k) for k in {f[0] for f in c3_findings}},

                 "examples": [{"artifact": a, "detail": d} for _, a, d in c3_findings[:4]],

                 "exempt_present_in_commit": sum(1 for _r in rels if aic._is_exempt(_r)),

                 "predicate_source": "SHIPPED acceptance_integrity_checks.c3_cross_round_identity"}


    # ---------- C5 over the readset's descriptors, resolved against the commit ----------
    rs = [r for r in rels if "READSET" in r.upper()]
    out["C5"] = {"readsets": rs}
    if rs:
        d = json.loads(read(rs[0]))
        raw = d.get("descriptors")
        items = []
        if isinstance(raw, dict):
            for nm, v in raw.items():
                if isinstance(v, dict):
                    v = dict(v); v.setdefault("path", nm); items.append(v)
        elif isinstance(raw, list):
            items = raw
        def lookup(p):
            # descriptors name paths relative to the evidence commit root
            for cand in (p, f"acceptance/evidence/w2r1/{CAND}/{p}", p.split(f"{CAND}/", 1)[-1]):
                b = git("show", f"{commit}:{cand}", binary=True)
                if b:
                    return b
            return None
        f5 = aic.c5_descriptor_resolvability(items, lookup)
        out["C5"].update({"descriptors": len(items), "findings": len(f5),
                          "by_type": {k: sum(1 for x in f5 if x[0] == k) for k in {x[0] for x in f5}},
                          "examples": [{"artifact": str(a), "detail": dt} for _, a, dt in f5[:6]]})
    # ---------- C6 over the committed Return Pack ----------
    pk = [r for r in rels if "RETURN_PACK" in r.upper()]
    if pk:
        packs = [(pk[0], json.loads(read(pk[0]).decode("utf-8")))]
        f6 = aic.c6_publication_preflight(packs)
        out["C6"] = {"findings": len(f6), "details": [{"artifact": a, "detail": d} for _, a, d in f6]}
    return out


if __name__ == "__main__":
    commits = sys.argv[1:] or ["d3e311c2c26b48f4cc0b4b60d02390628f1365b6"]
    res = [run(c) for c in commits]
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (HERE / "fixture_on_evidence.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
