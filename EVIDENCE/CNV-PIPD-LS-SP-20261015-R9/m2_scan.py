"""M2 trusted scope + secrets preflight for the R6 archive-repair publication.

Runs OUTSIDE the PR package (this file is never imported by, and never imports from, the archived
candidate). It reads blobs straight from git objects, so it inspects exactly what a downloader
would receive, and it executes nothing that the packet contains.

Checks (EIA-R6-06 / 指揮薄 M2):
  * every path in the scanned tree lies under the single approved prefix
  * no path traversal ('..'), no absolute paths
  * git mode 120000 (symlink) inside the packet -> reported as a scope violation
  * executable-bit blobs (100755) counted and reported (archive artifacts must not be self-running)
  * credential-shaped file names reported
  * fixed secret-pattern scan over every blob's bytes; HARD patterns block, SOFT candidates are
    listed for human rationalisation
  * the operator-supplied GitHub token is never printed: only occurrence counts and its sha256

Usage:
  python m2_scan.py --rev HEAD --out M2_TRUSTED_SCOPE_SECRETS.json [--worktree C:/Projects/wt-cnv-r6]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TOOL_ID = "m2_scan.py"
TOOL_VERSION = "1.0.0"
SCHEMA = "CNV-PIPD-LS-SP-20261015/M2-TRUSTED-SCOPE-SECRETS/1"
APPROVED_PREFIX = "EVIDENCE/CNV-PIPD-LS-SP-20261015/"
TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")

HARD_PATTERNS = [
    ("aws_access_key_id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("aws_secret_access_key", re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*[A-Za-z0-9/+=]{40}")),
    ("github_pat_classic", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("github_pat_fine_grained", re.compile(r"github_pat_[A-Za-z0-9_]{22,}")),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("openai_style_key", re.compile(r"\bsk-[A-Za-z0-9]{24,}")),
    ("url_with_credentials", re.compile(r"[a-zA-Z][a-zA-Z0-9+.\-]*://[^/\s:@]{3,}:[^/\s:@]{3,}@")),
]
SOFT_PATTERNS = [
    ("secret_word_assignment", re.compile(r"(?i)(api[_-]?key|secret|token|passwd|password)\s*[=:]\s*[\"']?[A-Za-z0-9_\-]{16,}")),
    ("nonce_or_receipt_word", re.compile(r"(?i)(nonce|bearer|authorization)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,}")),
]
CREDENTIAL_NAME = re.compile(r"(?i)(^|/)(id_rsa|id_ed25519|\.env|\.npmrc|\.netrc|credentials(\.[a-z0-9]+)?|[\w.-]*\.(pem|pfx|p12|key))$")


def git(*args: str, worktree: str) -> str:
    r = subprocess.run(["git", *args], cwd=worktree, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def blob_bytes(worktree: str, sha: str) -> bytes:
    r = subprocess.run(["git", "cat-file", "blob", sha], cwd=worktree, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"cat-file {sha} failed")
    return r.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--worktree", default="C:/Projects/wt-cnv-r6")
    ap.add_argument("--out", default="M2_TRUSTED_SCOPE_SECRETS.json")
    ap.add_argument("--prefix", default=APPROVED_PREFIX)
    a = ap.parse_args()

    rev = git("rev-parse", a.rev, worktree=a.worktree).strip()
    listing = git("ls-tree", "-r", "-l", a.rev, "--", a.prefix.rstrip("/"), worktree=a.worktree)
    entries, scope, execs, creds, symlinks = [], [], [], [], []
    hard, soft, scanned, total_bytes = [], [], 0, 0
    token_value = None
    if TOKEN_FILE.exists():
        token_value = TOKEN_FILE.read_text(encoding="utf-8", errors="replace").strip()
    token_occurrences, token_name_occurrences = 0, 0

    for line in listing.splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, sha, size = meta.split()
        size = int(size)
        ent = {"path": path, "mode": mode, "type": typ, "blob_sha1": sha, "bytes": size}
        if ".." in path.split("/") or path.startswith("/"):
            scope.append({"path": path, "why": "traversal or absolute path"})
        if not path.startswith(a.prefix):
            scope.append({"path": path, "why": "outside the single approved prefix"})
        if mode == "120000":
            symlinks.append(path)
            scope.append({"path": path, "why": "symlink inside the packet"})
        if mode == "100755":
            execs.append(path)
        if CREDENTIAL_NAME.search(path):
            creds.append(path)
        data = blob_bytes(a.worktree, sha)
        scanned += 1
        total_bytes += len(data)
        text = data.decode("latin-1")
        ent["sha256"] = hashlib.sha256(data).hexdigest()
        if token_value:
            if token_value in text:
                token_occurrences += text.count(token_value)
            if "GITHUB-REPO_SHW097-4" in text:
                token_name_occurrences += text.count("GITHUB-REPO_SHW097-4")
        for name, rx in HARD_PATTERNS:
            for m in rx.finditer(text):
                hard.append({"path": path, "pattern": name, "match_len": len(m.group(0)),
                             "match_sha256_prefix": hashlib.sha256(m.group(0).encode()).hexdigest()[:12]})
        for name, rx in SOFT_PATTERNS:
            hits = rx.findall(text)
            if hits:
                soft.append({"path": path, "pattern": name, "count": len(hits)})
        entries.append(ent)

    doc = {
        "schema": SCHEMA,
        "tool": {"id": TOOL_ID, "version": TOOL_VERSION,
                 "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 "executes_packet_content": False,
                 "note": "reads git objects only; never imports or runs anything from the packet"},
        "scanned": {"repo_worktree": a.worktree, "rev_input": a.rev, "rev_resolved": rev,
                    "approved_prefix": a.prefix, "blobs_scanned": scanned, "bytes_scanned": total_bytes,
                    "scan_digest_sha256": hashlib.sha256(
                        "".join(f"{e['path']}:{e['sha256']}" for e in entries).encode()).hexdigest()},
        "scope": {"out_of_prefix_or_traversal": scope, "symlinks": symlinks,
                  "executable_bit_blobs": {"count": len(execs), "paths_sample": execs[:20],
                                           "note": "archive artifacts with the executable bit are not executed by this tooling and must not be executed by consumers"}},
        "secret_scan": {"hard_patterns": [n for n, _ in HARD_PATTERNS], "soft_patterns": [n for n, _ in SOFT_PATTERNS],
                        "hard_findings": hard, "soft_candidates": soft,
                        "credential_shaped_names": creds,
                        "operator_token": {"token_file_present": TOKEN_FILE.exists(),
                                           "token_value_sha256_prefix": (hashlib.sha256(token_value.encode()).hexdigest()[:12] if token_value else None),
                                           "occurrences_in_packet": token_occurrences,
                                           "credential_file_name_mentions": token_name_occurrences,
                                           "value_never_printed": True}},
        "verdict": "PASS" if (not scope and not hard and token_occurrences == 0) else "BLOCKED",
        "claim_ceiling": "LOCAL_TRUSTED_SCAN (tool-side scan of published blobs; not an AO verdict)",
    }
    Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": doc["verdict"], "blobs": scanned, "bytes": total_bytes,
                      "scope_violations": len(scope), "hard_secrets": len(hard),
                      "soft_candidates": len(soft), "executables": len(execs),
                      "token_occurrences": token_occurrences, "out": a.out}, ensure_ascii=False))
    return 0 if doc["verdict"] == "PASS" else 3


if __name__ == "__main__":
    sys.exit(main())
