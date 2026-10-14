## Independent acceptance/challenge-verification lane (VERIFY_ONLY, verified 2026-08-13 FAR TRI_SOURCE challenge)

Fresh-context adversarial review of a delivered assurance layer (challenge + AO lanes).
Read-only; output = findings (id/severity/quote/fix) + A1..A14 PASS/FAIL table +
`CHALLENGE_VERDICT=` / `ACCEPTANCE_OFFICER_VERDICT=` final lines. Full recipe:
`references/acceptance-verification-lane.md`. Verified checks:

- **Documented immutable hash vs on-disk bytes (A11 class):** `sha256sum` the artifact and
  compare to every hash in README/TEAM/AGENTS/receipts; verify claimed mirror counts.
  Found: FAR_FINAL_ACCEPTANCE_EVIDENCE.md documented `58de0815…` → on-disk `eff79b73…`
  (mtime = review day, 2 of 4 claimed mirrors exist) = FAIL. Never trust git status for
  immutability (untracked files give no proof).
- **Cited evidence files must exist (A14 class):** D-decisions cited
  `var/far/github_d_research.json` — absent on disk.
- **Production call sites vs test-only (A1 class):** `grep import <module>` excluding
  tests/ — zero production imports = "mandatory" layer not wired into any WO flow.
- **WO doc + rollback pointer (A12 class):** grep the WO id across md/json/yaml; missing
  WO doc + missing RB-* pointer (crosswalk had only RB-WO-FAR-001..008, RB-WO-FAR-USE-001)
  = FAIL.
- **Reproduce canaries empirically** (in-memory heredoc python, no writes) instead of
  trusting canary JSON claims; **inspect the receipt body**, because tests can pass while
  masking receipt corruption (TS-013 asserted terminal only); flag stub probes
  (`# replaced below` never replaced → fake full PASS with zero retrieval) and
  unreachable guard branches (producer function's status domain makes a blocker
  structurally impossible).
- **Untouched-file proof by hash:** FAR_CAPABILITY_MATRIX.yaml == manifest frozen hash
  `2469d85b…` matched (PASS); CHANGE_INPUT_MANIFEST listing only baseline files = new
  subject has no frozen hash (finding).
- **Focused-hardening rounds: adversarial security probes + denominator recompute
  (verified 2026-08-14 WO-FAR-HARDENING-001).** Run SSRF/XML/truncation probe matrices
  against the LIVE functions instead of asserting from source — empirical probing is
  what catches real gaps (6to4-embedded loopback `2002:7f00:1::1` escapes ipaddress
  classification; DOCTYPE smuggle past a 4096-byte scan window still safe only via
  expat defaults). Verify the test denominator by recomputing the sorted-nodeids sha256
  against TEST_DENOMINATOR.json; re-running a deterministic canary is read-only-safe
  (output regenerates byte-identical); read the spine with
  `sqlite3.connect('file:...?mode=ro', uri=True)`; check mirror byte-identity across
  all evidence\review roots. Full probe bank + H-item verification recipe:
  `references/python-security-review-probes.md`.
- **External focused RE-REVIEW of closure rounds (verified 2026-08-14, same WO):** when
  a prior external challenge returned EXT-*-HARD-* findings and the maker shipped a
  closure, re-review = verify each fix IN SOURCE (grep + read the class body + confirm
  wiring in the real call path), assert canary claims on-disk AND embedded==disk JSON
  equality, recompute EVERY digest (nodeids via sorted/as-listed join, subject manifest
  via sorted relpath+sha rows, then on-disk files vs manifest rows incl. byte counts),
  and run the timestamp-monotonicity check (all receipt `generated_at_utc` /
  `retrieved_at` / `frozen_at_utc` <= evidence-MD §0 generation time, python datetime
  parse handling `Z` and `+08:00`). Section-scoped JSON extraction from a multi-```json
  MD requires splitting on `## N.` headers first (naive re.search grabs the first block).
  Cosmetic prose-digest mismatches (e.g. SECCL text says `4673ca8f` while recomputed
  nodeids digest is `626d6472…`) = LOW non-blocking; keep verdict PASS. Full recipe:
  `references/focused-hardening-rereview.md`.
- **Independent lanes must hunt VACUOUS / SELF-ASSERTED probes, not just hash mismatches
  (verified on a pre-construction qualification round: the adversarial lane returned PARTIAL
  on probe quality while confirming the claim ceiling itself was NOT exceeded — so a probe
  finding must not be inflated into a product failure either).** Dispatch the challenge lane
  with an explicit instruction to read the PRODUCER'S probe code and look for:
  (a) a hardcoded expected verdict (`resolver_output: "QUARANTINE"`, `pass: True`) with no
  resolver actually invoked; (b) a probe whose PASS is derived from rows that are all
  `NOT_APPLICABLE`/default — the derived field is then unsupported even though every row
  reads green; (c) `.get(key, default)` where the key SPACES differ — a register keyed
  `"PD00"` looked up as `"PD-PKG-00"` silently returns the default for every call and
  short-circuits an entire probe family; (d) a readiness field contradicting its own
  lifecycle / `work_required`.
  Mandatory fix pattern: every negative/adversarial probe ships a CONTROL case that must
  resolve the other way, proving the test can distinguish — an assertion that cannot fail is
  not evidence. A `NOT_APPLICABLE` result must NEVER count toward a PASS.
- **When an independent lane finds a defect in YOUR measuring instrument, fix the instrument
  and re-run the entire downstream chain (verified same round).** Do not re-word the claim and
  do not leave the artifact set mixed-generation. Record a corrective-action artifact
  (defect id, severity, finding, root cause, fix, re-run proof, status) as first-class
  evidence, regenerate every dependent receipt/checkpoint/pack/dossier, and state plainly that
  all pre-fix hashes are invalidated. Then re-dispatch a FRESH verification round whose
  instructions NAME each prior defect and require independent confirmation that it is genuinely
  fixed — a corrected artifact set that has not itself been re-verified carries no more
  authority than the first one did.

