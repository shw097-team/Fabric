# -*- coding: utf-8 -*-
"""Slim hgk SKILL.md below 100k so gates patch can land. Collapse duplicate content only."""
p = r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\SKILL.md"
s = open(p, encoding="utf-8").read()
orig = len(s)

# 1. MANDATORY ROUTE points 4/5 -> reference (dup of HARD RULES)
old_route = """4. **Freeze order:** freeze HEAD → freeze receipts → freeze tests → fresh checker →
   SubjectManifest → EvidenceManifest → render final MD LAST → mirror byte-identical
   → readback receipt → submit exact bytes.
5. **Never append a ChangeSet after manifest regeneration."""
new_route = "4-5. Freeze order + no-append-after-manifest: see HARD RULES 1-9 below."
if old_route in s:
    s = s.replace(old_route, new_route)
    print("route collapsed")

# 2. Codex daemon entry -> shorter
start = s.find("- **Codex run fails at first request")
end = s.find("- **TWSE listing venue")
if start >= 0 and end > start:
    old_codex = s[start:end]
    new_codex = """- **Codex daemon death (`connection refused :10101`):** (a) `curl http://127.0.0.1:10101/healthz` confirm;
  (b) `ocx stop` may lie — find listener `netstat -ano | grep :10101 | grep LISTENING`, kill
  `powershell Stop-Process -Id <pid> -Force`; (c) RESTART MUST carry credential
  `export OPENCODE_GO_API_KEY=$(grep '^OPENCODE_GO_API_KEY=' "$LOCALAPPDATA/hermes/.env" | cut -d= -f2-)`
  + `export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"` BEFORE `opencodex start --port 10101`;
  (d) verify NEW pid + healthz. Daemon is NOT a service — record `OPENCODEX-DAEMON-RESTART-001` note.

"""
    s = s.replace(old_codex, new_codex)
    print("codex collapsed:", len(old_codex), "->", len(new_codex))

# 3. Focused RE-REVIEW paragraph -> shorter (points to references)
old_fr = s[s.find("**Focused RE-REVIEW repair (verified 2026-08-14, EXT-FDA-RR2"):]
old_fr = old_fr[:old_fr.find("\n\n")]
if old_fr:
    new_fr = """**Focused RE-REVIEW repair (verified 2026-08-14):** FAIL = deterministic CONTRADICTIONS inside
submitted evidence. Track A (normalization): rewrite evidence MD fresh (write_file not patch), ONE
current value per truth, label old counts SUPERSEDED_PRE_<PATCH>, grep stale tokens → 0.
Track B (rebind order): freeze HEAD → receipts → tests → fresh checker → SubjectManifest →
EvidenceManifest (rehash bundle bytes) → render final MD LAST → mirror → readback → submit.
HARD: never append ChangeSet after manifest regeneration. Identity trap: claimed file+hash MUST
equal received bytes. Full: `references/external-rereview-normalization-rebind.md`."""
    s = s.replace(old_fr, new_fr)
    print("focused-rereview collapsed:", len(old_fr), "->", len(new_fr))

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("len:", orig, "->", len(s), "saved", orig - len(s))
