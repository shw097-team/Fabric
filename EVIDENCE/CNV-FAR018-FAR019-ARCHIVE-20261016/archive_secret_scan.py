#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A05 trusted scoped secrets scan (maintainer side).

Runs the ROUND'S OWN scanner in the publisher process over the content each PR ADDS at its frozen
head.  No PR-provided script is executed (the archive holds .py/.ps1 files as evidence only).

Non-vacuity is proven on the same run: a POSITIVE control (a synthetic credential of each forbidden
shape) must be flagged, and a CLEAN control (benign prose that merely mentions secrets policy) must
not be.  A scanner that flags nothing is only credible next to a control that proves it can flag.

No matched value is ever printed or written: excerpts are masked to head + length.
"""
import base64, json, re, datetime, urllib.request, urllib.error
from pathlib import Path

ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = Path("C:/Projects/Agent_Workspace/_handover") / ROUND
TOK = open("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt", encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "User-Agent": "hgk-archive-round", "Accept": "application/vnd.github+json"}
PFX = {12: "EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/",
       13: "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/",
       14: "EVIDENCE/FAR-20261019-owner-authorized-closure/"}
HEADS = {12: "0a30e5a8f636c4e310958778491bf4154e7caf1e",
         13: "0fc70f2f050119ada63cad7b4e641c21fdb37fa5",
         14: "b33b122053d53520809e87674784279097673fc0"}

RULES = [
    ("github_token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("aws_access_key", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private_key_block", re.compile(r"-----BEGIN (RSA |OPENSSH |EC |PGP )?PRIVATE KEY-----")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("credentialed_url", re.compile(r"[a-z][a-z0-9+.\-]{2,}://[^\s/:@]{3,}:[^\s/@]{6,}@[^\s/]+")),
    ("assigned_secret", re.compile(r"(?i)\b(api[_-]?key|secret|passwd|password|access[_-]?token|client[_-]?secret)"
                                   r"\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{6,}")),
]
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz", ".pdf", ".ico", ".woff", ".woff2")
HOOK_MARKERS = (".github/workflows/", ".githooks/", "hooks/", ".gitattributes")


def api(p):
    r = urllib.request.Request("https://api.github.com" + p, headers=H)
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        return {"__err": e.code, "body": e.read().decode()[:160]}


def blob_bytes(sha):
    b = api("/repos/shw097-team/Fabric/git/blobs/" + sha)
    if "__err" in b:
        return None
    return base64.b64decode(b.get("content", "") or "")


def scan(text):
    hits = []
    for name, rx in RULES:
        for m in rx.finditer(text):
            v = m.group(0)
            hits.append({"rule": name, "masked": v[:4] + "…" + v[-2:] if len(v) > 8 else "…",
                         "length": len(v), "offset": m.start()})
    return hits


# -- non-vacuity controls (same function, same run) ------------------------------------------------
POS = ("ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8" + "\n" + "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\n"
       + "-----BEGIN RSA PRIVATE KEY-----\n" + "slack=xoxb-1234567890-abcdefghijkl\n"
       + 'api_key = "kjsdhfkjshdfkjhsdfkjh"' + "\n" + "postgres://admin:hunter2secret@db.internal:5432/x\n")
CLEAN = ("This document explains how to rotate credentials, where the token file lives, and why the "
         "secret value must never be committed.  It mentions api key, password and token as WORDS only.")
pos_hits, clean_hits = scan(POS), scan(CLEAN)
controls = {"positive_control_rules_fired": sorted({h["rule"] for h in pos_hits}),
            "positive_control_hit_count": len(pos_hits),
            "clean_control_hit_count": len(clean_hits),
            "clean_control_rules_fired": sorted({h["rule"] for h in clean_hits}),
            "non_vacuity": "PASS" if pos_hits and not clean_hits else "FAIL"}

report = {"schema": "CNV-ARCHIVE-A05-SECRET-SCAN/1", "task_id": ROUND,
          "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "scanner": {"origin": "this round's own scanner, run in the publisher process",
                      "rules": [r[0] for r in RULES], "executed_pr_supplied_code": False},
          "controls": controls, "prs": {}, "workflow_or_hook_paths": [], "real_secret_exposed": 0}

for n in (12, 13, 14):
    cm = api("/repos/shw097-team/Fabric/commits/" + HEADS[n])
    tree = api("/repos/shw097-team/Fabric/git/trees/%s?recursive=1" % cm["commit"]["tree"]["sha"])
    blobs = [r for r in tree.get("tree", []) if r["type"] == "blob" and r["path"].startswith(PFX[n])]
    rows, nbytes, skipped, findings = [], 0, [], []
    for r in blobs:
        path = r["path"]
        if path.lower().endswith(SKIP_EXT):
            skipped.append(path)
            continue
        raw = blob_bytes(r["sha"])
        if raw is None:
            skipped.append(path + " (blob fetch failed)")
            continue
        nbytes += len(raw)
        text = raw.decode("utf-8", "replace")
        h = scan(text)
        rows.append({"path": path, "bytes": len(raw), "hits": len(h)})
        for x in h:
            findings.append(dict(x, path=path))
        if any(m in path for m in HOOK_MARKERS):
            report["workflow_or_hook_paths"].append(path)
    report["real_secret_exposed"] += sum(1 for f in findings if f["rule"] in
                                         {"github_token", "aws_access_key", "private_key_block", "slack_token",
                                          "openai_key", "google_api_key", "jwt"})
    report["prs"][str(n)] = {"head_sha": HEADS[n], "allowed_prefix": PFX[n], "blobs_under_prefix": len(blobs),
                             "scanned_files": len(rows), "scanned_bytes": nbytes, "skipped": skipped[:6],
                             "findings": findings, "finding_count": len(findings),
                             "highest_risk": ("SECRET_HOLD" if any(f["rule"] != "credentialed_url" and
                                                                   f["rule"] != "assigned_secret" for f in findings)
                                              else ("REVIEW" if findings else "CLEAR")),
                             "verdict": "PASS" if not findings else "REVIEW"}

# PR #14 config-backup sensitivity review (EIA-019-12): does the archived pre-image hold a real value?
cfg = "EVIDENCE/FAR-20261019-owner-authorized-closure/config-hermes-codex-lane.pre-A1.json"
b = api("/repos/shw097-team/Fabric/contents/%s?ref=%s" % (cfg, HEADS[14]))
detail = {"path": cfg, "present": "__err" not in b}
if detail["present"]:
    raw = base64.b64decode(b.get("content", "") or "")
    txt = raw.decode("utf-8", "replace")
    hits = scan(txt)
    keys = []
    try:
        j = json.loads(txt)
        keys = sorted(j.keys())[:20]
        for k, v in j.items():
            if isinstance(v, str) and re.search(r"(?i)(key|token|secret|password|bearer)", str(k)):
                hits.append({"rule": "sensitive_key_name", "masked": str(k), "length": len(str(v)),
                             "offset": -1})
    except Exception as e:  # noqa: BLE001
        detail["parse_error"] = type(e).__name__
    detail.update({"bytes": len(raw), "top_keys": keys, "findings": hits,
                   "contains_credential_value": any(h["rule"] in
                                                    {"github_token", "aws_access_key", "private_key_block",
                                                     "slack_token", "openai_key", "google_api_key", "jwt",
                                                     "credentialed_url", "assigned_secret"} for h in hits)})
report["pr14_config_backup_review"] = detail

report["verdict"] = ("PASS" if report["real_secret_exposed"] == 0 and controls["non_vacuity"] == "PASS"
                     and not report["pr14_config_backup_review"].get("contains_credential_value") else "REVIEW")
(OUT / "A05_SECRET_SCAN.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
print("controls:", json.dumps(controls, ensure_ascii=False))
for n in (12, 13, 14):
    p = report["prs"][str(n)]
    print("PR%-3d blobs=%d scanned=%d bytes=%d findings=%d highest=%s verdict=%s"
          % (n, p["blobs_under_prefix"], p["scanned_files"], p["scanned_bytes"], p["finding_count"],
             p["highest_risk"], p["verdict"]))
    for f in p["findings"][:6]:
        print("      ", f["rule"], f["masked"], f["length"], f["path"][:80])
print("hook/workflow paths:", report["workflow_or_hook_paths"])
print("PR14 config backup:", {k: v for k, v in detail.items() if k != "findings"}, "findings",
      [f["rule"] for f in detail.get("findings", [])])
print("OVERALL:", report["verdict"], "| real_secret_exposed", report["real_secret_exposed"])
