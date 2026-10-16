# Focused external re-review of closure rounds (challenge-review lane, VERIFY_ONLY)

Verified 2026-08-14: focused re-review of WO-FAR-HARDENING-001 after EXT-FAR-TS-HARD-001..006
repairs (evidence MD `FAR_TRI_SOURCE_FOCUSED_HARDENING_EVIDENCE.md`, sha `58849ecd…`,
+ swarm default-on change). Read-only. Output = findings (id/sev/quote/fix) + checklist
PASS/FAIL per claim + final `CHALLENGE_VERDICT=` / `ACCEPTANCE_OFFICER_VERDICT=` lines.

## 1. Verify the fix in SOURCE, not just evidence
- grep the class/function name in the LIVE module, then READ the class body (docstring +
  the actual `raise`) — a grep hit alone proves nothing (e.g. `_NoRedirectHandler` exists
  but its `redirect_request` must RAISE on any redirect).
- Confirm the fix is wired into the real call path (`build_opener(_NoRedirectHandler())`
  inside `retrieve_web`), not just defined-and-unused decoration.

## 2. Canary verification
- Read the canary JSON on disk; assert the exact claim the closure makes (e.g. all 5
  CANARY-H4 targets REJECTED).
- Extract the MD-embedded copy and assert full JSON equality (`emb == disk`) — stronger
  than digest match; catches stale embeds.
- Web-hit samples: check HARD-006-style fields directly (requested_url / final_url /
  redirect_chain=[]).

## 3. Timestamp monotonicity (no-future-timestamps check)
- MD §0 `> 生成:` line is the upper bound.
- Python datetime parse: CANARY-H2 `retrieved_at`, and every receipt's
  `generated_at_utc` / `verified_at_utc` / `frozen_at_utc` — all must be <= MD generation
  time. Handle `Z` suffix and `+08:00` offsets (`fromisoformat(g.replace('Z','+00:00'))`).
- Check BOTH the MD-embedded values AND the on-disk receipt files.

## 4. Digest recomputation
- nodeids digest: extract §10 list, sha256 over `'\n'.join(ids)` — try both sorted and
  as-listed joins; compare to TEST_DENOMINATOR.json `nodeids_digest` AND the §10 header.
- subject manifest digest: sha256 over sorted `'relpath sha256'` rows; compare to
  embedded `subject_digest`; then verify on-disk files match manifest rows (sha256 AND
  bytes count, 0 mismatches expected).
- full-JSON equality MD-embedded section vs on-disk file for every manifest.

## 5. Section-scoped JSON extraction from evidence MD (pitfall)
Naive `re.search(r'```json\n(.*?)\n```', md, re.S)` returns the FIRST json block (often
§3 C0 manifest) → KeyError on the intended section. Split by section header first:
```python
sec = md.split('## 12.')[1].split('## 13.')[0]   # then regex inside sec
```

## 6. Test re-run
- `python -m unittest discover -s tests -t .` with merged `2>&1`; compare count + OK +
  exit code vs the embedded raw stdout. Timing differs run-to-run (1.935s vs 2.031s);
  count/OK/exit must match.
- Use the native Windows python path form `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.

## 7. Script execution hygiene (both bit this session)
- Native Windows Python REJECTS MSYS-style script paths: `/c/Users/user/x.py` →
  `can't open file 'C:\c\Users\...'`; pass `C:/Users/...` instead.
- Multi-line python containing backslashes (`rel.replace('\\', '/')`) inside a git-bash
  heredoc gets escape-mangled → `SyntaxError: unterminated string literal`. Write the
  script with write_file and run it; don't inline heredoc payloads with backslashes.
- Evidence artifacts may live outside the repo root (USER_DECISION files in
  `知識庫\實作相關DOC\fabric-autonomous-research\`); `find` broadly (whole workspace)
  before declaring a file missing.

## 8. Finding classification
- Cosmetic prose inconsistency = LOW non-blocking when the authoritative digest fields
  recompute correctly (observed: SECCL verification text "nodeids digest 4673ca8f"
  prefix ≠ recomputed `626d6472…`; §0/§10/§11 all correct). Report id/sev/quote/fix,
  note the fix, keep verdict PASS.
- Blocking = count mismatch, digest mismatch, future timestamp, missing embedded
  artifact, embedded != on-disk JSON.
- Output shape:
```
CHALLENGE_VERDICT=PASS
ACCEPTANCE_OFFICER_VERDICT=PASS
```
