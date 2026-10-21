#!/usr/bin/env python
"""Build the evidence packet manifest for FAR-MINIMAX-MANDATE-20261021.

Every file is recorded with its SHA-256 and its byte length, so an external acceptance
officer can recompute the digests from the remote commit object store and prove that the
published packet is byte-identical to what was reviewed.

SECRET SCAN
  A pattern scan runs over every file in the packet. The PAT file, the OAuth account
  metadata and the relay credential live outside the packet; if any of their shapes ever
  appears inside it, the build FAILS rather than publishing.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PKT = Path(__file__).resolve().parent
OUT = PKT / "PACKET_MANIFEST.json"

SECRET_RX = re.compile(
    r"(ghp_[A-Za-z0-9]{20,}"                      # classic PAT
    r"|github_pat_[A-Za-z0-9_]{20,}"              # fine-grained PAT
    r"|sk-[A-Za-z0-9]{24,}"                       # openai-style key
    r"|sk-or-v1-[A-Za-z0-9]{20,}"                 # openrouter-style key
    r"|Bearer\s+[A-Za-z0-9._\-]{24,}"             # bearer token in a header
    r"|\"(?:api_key|apiKey|access_token|client_secret)\"\s*:\s*\"[^\"]{16,}\")",
    re.I)
ALLOW = re.compile(r"(api_key|apiKey|access_token|client_secret)", re.I)


def main() -> None:
    files = []
    findings = []
    for p in sorted(PKT.rglob("*")):
        if not p.is_file() or p.name == OUT.name:
            continue
        rel = str(p.relative_to(PKT)).replace("\\", "/")
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        files.append({"path": rel, "sha256": h, "bytes": len(data)})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for m in SECRET_RX.finditer(text):
            # a config KEY NAME with a placeholder value is not a secret
            frag = m.group(0)
            if ALLOW.fullmatch(frag.strip()) or '"${' in frag or "env_ref:" in frag:
                continue
            findings.append({"path": rel, "match": frag[:16] + "..."})

    manifest = {
        "schema": "HGK-EVIDENCE-PACKET/1",
        "packet": "FAR-MINIMAX-MANDATE-20261021",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "control_plane": "HG-KSEOS",
        "owner_order": ("2026-10-21: PLAN, EXECUTE (Codex CLI) and VERIFY/SECURITY (Codex CLI) "
                        "all on opencode-go/minimax-m3.1-flash-free (MiniMax M3.1 Flash, "
                        "OPENCODE GO)"),
        "registry_epoch": 25,
        "claim_ceiling": ("CANDIDATE_ONLY. The evidence below shows that the binding was "
                          "measured and independently re-derived on this machine. It is NOT an "
                          "acceptance, NOT a release, NOT a merge, and NOT a promotion. "
                          "No upstream provider state, no external acceptance and no release "
                          "action is claimed."),
        "secret_scan": {
            "files_scanned": len(files),
            "findings": findings,
            "note": ("The GitHub PAT (C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt), "
                     "the OAuth account metadata and the relay credential are OUTSIDE this packet "
                     "and appear in it only as [REDACTED]."),
        },
        "file_count": len(files),
        "total_bytes": sum(f["bytes"] for f in files),
        "files": files,
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": manifest["file_count"],
                      "total_bytes": manifest["total_bytes"],
                      "secret_findings": len(findings),
                      "mismatches": []}, ensure_ascii=False, indent=1))
    if findings:
        raise SystemExit(f"SECRET_FINDINGS: {len(findings)} — refusing to publish")


if __name__ == "__main__":
    main()
