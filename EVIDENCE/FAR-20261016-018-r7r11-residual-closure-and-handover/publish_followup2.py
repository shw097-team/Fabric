"""Additive (never force-push) follow-up commits binding this round's receipts to the evidence branch.

Why this is needed rather than rebuilding the original commit: a receipt describing a commit cannot
live inside the commit it describes. PACK_INDEX.json is also corrected here — the first publication
gave it a row for ITSELF whose digest was stale by construction, which failed a live remote readback
with exactly one mismatch.

usage: publish_followup2.py [correct|final]
"""
import base64, datetime, hashlib, json, sys, urllib.error, urllib.request
from pathlib import Path

TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
ROOT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
REPO = "shw097-team/Fabric"
PREFIX = "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/"
BRANCH = "evidence/far-018-r7r11-residual-closure"
API = "https://api.github.com"

# (published relative path, local path relative to ROOT)
BUNDLES = {
    "correct": [
        ("PACK_INDEX.json", "publish/payload/PACK_INDEX.json"),
        ("EVIDENCE_CLOSURE_FAR-20261016-018.md", "publish/payload/EVIDENCE_CLOSURE_FAR-20261016-018.md"),
        ("SELF_CHECK_RECEIPT.json", "SELF_CHECK_RECEIPT.json"),
        ("ADJUDICATION_AND_LIMITATIONS.json", "ADJUDICATION_AND_LIMITATIONS.json"),
        ("HANDOVER_FAR018.md", "HANDOVER_FAR018.md"),
        ("SELF_EVOLUTION_RECORD.json", "SELF_EVOLUTION_RECORD.json"),
        ("isolation_probe_receipt.json", "isolation_probe_receipt.json"),
        ("skill_entry_map_install_receipt.json", "skill_entry_map_install_receipt.json"),
        ("lane/VERIFY_VERDICT.json", "lane/VERIFY_VERDICT.json"),
        ("lane/VERIFY_ATTEMPT1_REFUSED.json", "lane/VERIFY_ATTEMPT1_REFUSED.json"),
        ("writer/entry_map.json", "writer/entry_map.json"),
        ("writer/METADATA_SEMANTICS_V2.json", "writer/METADATA_SEMANTICS_V2.json"),
        ("writer/CROSS_INDEX_V2.json", "writer/CROSS_INDEX_V2.json"),
        ("writer/WRITER_MANIFEST.json", "writer/WRITER_MANIFEST.json"),
    ],
    "final": [
        ("REMOTE_READBACK_VERIFY.json", "REMOTE_READBACK_VERIFY.json"),
        ("PUBLISH_RECEIPT.json", "PUBLISH_RECEIPT.json"),
        ("POST_PUBLICATION_ADDENDUM.md", "POST_PUBLICATION_ADDENDUM.md"),
    ],
}
MESSAGE = {
    "correct": ("FAR-20261016-018: correct PACK_INDEX self-hash and bind the round's closure receipts "
                "(additive)\n\nPACK_INDEX.json no longer lists itself: a file cannot contain its own digest, "
                "and the self-row asserted a stale value that failed a live remote readback with exactly one "
                "mismatch. The unlisted-by-itself condition is now declared in `self_excluded`. Also binds the "
                "adjudication, handover, self-evolution record, checker verdict, the preserved first-fail and "
                "the writer's artifacts. Fast-forward only; main untouched."),
    "final": ("FAR-20261016-018: bind the final readback receipt and the publication addendum (additive)\n\n"
              "A receipt describing a commit cannot live in the commit it describes, so the corrected "
              "REMOTE_READBACK_VERIFY.json, the publish receipt and the addendum land here. Fast-forward "
              "only; main untouched."),
    "sync": ("FAR-20261016-018: mirror the payload so the branch carries exactly what PACK_INDEX lists "
             "(additive)\n\nAdds the round's own harness scripts (self_check.py, build_pack.py, "
             "build_register.py, emit_closure.py, verify_pack_local.py, far018_readback2.py, ...) plus the "
             "adjudication and the preserved first-fail, so an external team can re-derive this round rather "
             "than only read it. Fast-forward only; main untouched."),
}


def token():
    t = TOKEN_FILE.read_text(encoding="utf-8", errors="replace").strip()
    for line in t.splitlines():
        if line.strip().startswith(("ghp_", "github_pat_", "gho_", "ghs_")):
            return line.strip()
    return t.split()[0]


def req(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header("Authorization", f"Bearer {token()}")
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "hgk-governed-publisher")
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:400]}


def main():
    bundle = sys.argv[1] if len(sys.argv) > 1 else "correct"
    if bundle == "sync":
        PAY = ROOT / "publish" / "payload"
        files = [(str(p.relative_to(PAY)).replace("\\", "/"), str(p.relative_to(ROOT)).replace("\\", "/"))
                 for p in sorted(PAY.rglob("*")) if p.is_file()]
    else:
        files = BUNDLES[bundle]
    out = {"schema": "FAR-20261016-018/PUBLISH-FOLLOWUP/1", "bundle": bundle,
           "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "force": False, "writes_to_main": False, "token_value_exported": False}

    st, ref = req("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    if st != 200:
        print(json.dumps({"first_fail": "BRANCH_UNREADABLE", "status": st}))
        return 2
    tip = ref["object"]["sha"]
    out["parent_commit"] = tip
    st, cm = req("GET", f"/repos/{REPO}/git/commits/{tip}")
    if st != 200:
        print(json.dumps({"first_fail": "TIP_UNREADABLE", "status": st}))
        return 3
    base_tree = cm["tree"]["sha"]

    tree, rows = [], []
    for published, local in files:
        src = ROOT / local
        if not src.is_file():
            print(json.dumps({"first_fail": "MISSING_LOCAL_ARTIFACT", "path": local}))
            return 4
        data = src.read_bytes()
        st, blob = req("POST", f"/repos/{REPO}/git/blobs",
                       {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        if st not in (200, 201):
            print(json.dumps({"first_fail": "BLOB_CREATE_FAILED", "path": published, "status": st}))
            return 5
        tree.append({"path": PREFIX + published, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        rows.append({"path": PREFIX + published, "bytes": len(data),
                     "content_sha256": hashlib.sha256(data).hexdigest(), "blob_sha": blob["sha"]})

    st, t = req("POST", f"/repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": tree})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "TREE_CREATE_FAILED", "status": st, "detail": str(t)[:300]}))
        return 6
    st, c = req("POST", f"/repos/{REPO}/git/commits",
                {"message": MESSAGE[bundle], "tree": t["sha"], "parents": [tip]})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "COMMIT_CREATE_FAILED", "status": st, "detail": str(c)[:300]}))
        return 7
    out["followup_commit"] = c["sha"]
    st, upd = req("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", {"sha": c["sha"], "force": False})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "REF_UPDATE_FAILED", "status": st, "detail": str(upd)[:300],
                          "note": "the follow-up commit exists but the ref did not move"}))
        return 8
    st, rb = req("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    out["readback"] = {"status": st, "sha": (rb.get("object") or {}).get("sha"),
                       "matches": (rb.get("object") or {}).get("sha") == c["sha"]}
    out["files"] = rows
    (ROOT / f"PUBLISH_FOLLOWUP_{bundle.upper()}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "files"}, ensure_ascii=False, indent=1))
    print("touched", len(rows), "paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
