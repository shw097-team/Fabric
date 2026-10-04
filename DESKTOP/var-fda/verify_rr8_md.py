# -*- coding: utf-8 -*-
"""Verify RR8 MD: embedded manifest body SHA == declared in MD (reviewer-equivalent check)."""
import hashlib
import json
import re

MD = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md"
txt = open(MD, encoding="utf-8").read()

# declared sha in the MD
m_decl = re.search(r"manifest SHA-256 \(of exact bytes above\): ([0-9a-f]{64})", txt)
declared = m_decl.group(1) if m_decl else None

# extract embedded body
m = re.search(r"# 4\. FDA_EVIDENCE_MANIFEST\.json — COMPLETE RAW BODY\n\n```json\n(.*?)\n```", txt, re.DOTALL)
if m:
    man_body = m.group(1)
    sha = hashlib.sha256(man_body.encode("utf-8")).hexdigest()
    d = json.loads(man_body)
    print("embedded body sha:", sha)
    print("declared in MD  :", declared)
    print("MATCH:", sha == declared)
    print("entries:", d["artifact_count"], "| unique paths:", len({a["path"] for a in d["artifacts"]}))
    print("subject:", d["subject_root"]["git_head"][:12])
    paths = [a["path"] for a in d["artifacts"]]
    for k in ["FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json", "FDA_CHECKER_FINAL_RR7.json",
              "FDA_F01_CURRENT_260811_RECEIPT.json", "FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
              "FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"]:
        print(f"  bound {k}: {any(k in p for p in paths)}")
else:
    print("manifest body NOT found")
