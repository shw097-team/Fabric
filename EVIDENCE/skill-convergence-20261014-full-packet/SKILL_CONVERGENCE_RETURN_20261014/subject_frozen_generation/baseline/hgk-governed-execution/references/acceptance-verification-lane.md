# Independent acceptance/challenge-verification lane (VERIFY_ONLY)

Fresh-context adversarial review of a delivered assurance layer or governed changeset.
Read-only: report findings + AO checklist table + final verdict lines
(`CHALLENGE_VERDICT=...`, `ACCEPTANCE_OFFICER_VERDICT=PASS|FAIL`). Never repair.
Verified 2026-08-13 on the FAR TRI_SOURCE_MANDATORY challenge (WO-FAR-TRISOURCE-001).

## Recipe (order matters — cheapest falsifiers first)

1. **Read the subject module fully** (all lines, no skimming). Note: imports (stdlib-only =
   no second control plane), injected dependencies (probe functions = source-as-data trust
   boundary), dead params (`allowed_web_roots` accepted, never used), stub bodies.
2. **Run the test suite read-only**, capture the summary line (`Ran N tests ... OK`).
   Then ask: what do the tests NOT assert? Passing tests frequently mask the real bugs
   (see defect classes below).
3. **Verify documented immutable hashes against on-disk bytes.** `sha256sum` the artifact
   and compare to every hash documented in README/TEAM/AGENTS/activation receipts. Also
   verify claimed mirror counts (`find` for all copies, compare hashes across mirrors).
   Hash mismatch or missing mirrors = immutability claim broken = FAIL (A11 class).
4. **Check cited evidence files exist.** Walk every `evidence_locator` /
   `evidence_files` field in D-decisions/manifests/receipts; `ls` each path. Absent file =
   evidence-exactness FAIL (A14 class).
5. **Grep production call sites.** `grep -rn "<module>" --include="*.py" . | grep -v
   tests/ | grep -v __pycache__`. Zero production imports of the new module = the
   "mandatory" layer is not wired into any executable flow (A1 class FAIL). Also grep for
   the WO id across md/json/yaml — missing WO doc + missing RB-* rollback pointer = FAIL
   (A12 class).
6. **Reproduce canary claims empirically.** Run the module's functions in-memory
   (heredoc python, no file writes) against each canary scenario; compare produced
   statuses/terminals to the canary JSON claims. This catches hand-written canaries that
   assert behavior the code doesn't actually produce.
7. **Verify "untouched" files by hash, not git status.** Hash the frozen file and compare
   to the manifest's frozen hash (porcelain can be empty for untracked files and gives no
   proof either way).
8. **Check the CHANGE_INPUT_MANIFEST for the NEW artifacts.** A manifest listing only
   baseline files means the new subject has no frozen hash and no rollback anchor.
9. **Template header hygiene.** Check for dual/uncommented legacy headers (TSV/CSV
   templates with the old header row left above the new one — parsers read it as data).

## Defect classes found (all empirically confirmed 2026-08-13)

- **Stale-loop-variable on exception (Python).** Pattern:
  ```python
  for ch in CHANNELS:
      try:
          res = probe_fn(ch)
          outcome = channel_outcome(*res)
      except Exception as exc:
          outcome = {"status": "ERROR", "attempted": True}
      channels[ch] = dict(outcome, **_channel_summary(res[1] if outcome.get("attempted") else []))
  ```
  When `probe_fn(ch)` raises: (a) on the FIRST iteration `res` is unbound → `NameError`
  crash instead of the documented ERROR outcome; (b) on a LATER iteration `res` retains
  the previous channel's tuple → the ERROR channel's receipt summary shows the PREVIOUS
  channel's rows (provenance misattribution: knowledge ERROR showed `receipt_refs:
  ['memory-1']`). The passing test masked it by asserting only terminal status, never the
  receipt body. Fix pattern: `res = None` before try; guard
  `_channel_summary(res[1] if res else [])`.
- **Stub-probe landmine.** `def probe(ch): return (True, [], True, None, None)  # replaced
  below by real channel dispatch` — never replaced, orchestrator function never called →
  the adapter would emit a fake `RESEARCH_PASS_CANDIDATE` with zero retrieval. Dead code
  with no callers is still a live landmine; flag it.
- **Unreachable guard branch.** A blocker code (`COUNTEREVIDENCE_MISSING`) is computed but
  structurally unreachable because the probe function only ever returns statuses that keep
  `completed=True`. Test exercises the reducer directly, masking the dead path. Check the
  producer functions for the full status domain before trusting the reducer's guard.
- **Documented-hash drift.** `FAR_FINAL_ACCEPTANCE_EVIDENCE.md` documented as
  `58de08155b…` (四處 byte-identical) but on-disk hash `eff79b73f…`, mtime = review day,
  only 2 of 4 claimed mirrors present.
- **Phantom evidence.** D-decision `research_basis.evidence_files` cited
  `var/far/github_d_research.json` + `_r2.json` — both absent on disk.
- **Test-only enforcement.** `far_trisource` imported by zero production modules; the
  mandatory three-probe loop only reachable from tests.
- **Missing WO/rollback.** No `WO-FAR-TRISOURCE-001` doc and no `RB-WO-FAR-TRISOURCE-001`
  pointer anywhere; crosswalk lists only `RB-WO-FAR-001..008`, `RB-WO-FAR-USE-001`.
- **Dual TSV header.** `ClaimLedger.tsv` kept the legacy 9-column header uncommented above
  the new 15-column header.

## Useful commands (git-bash, Windows)

```bash
sha256sum <file> | cut -c1-16                      # compare vs documented hash prefix
find . -maxdepth 8 -name "<artifact>"              # verify claimed mirror count
grep -rn "WO-XXX" --include="*.md" --include="*.json" --include="*.yaml" .   # WO/rollback existence
grep -rn "<module>" --include="*.py" . | grep -v tests/ | grep -v __pycache__ # production call sites
stat -c '%y %s' <file>                             # mtime/size — was it touched today?
# In-memory canary reproduction (no file writes):
python - <<'EOF'
import sys; sys.path.insert(0, '.')
import <module> as m
# ... call m.adjudicate_claim / m.terminal_reducer with canary inputs; print + compare
EOF
```

## Output shape

Findings list (id, severity, quote, fix) + AO checklist table (A1..A14 PASS/FAIL with
one-line evidence each) + final two lines:
`CHALLENGE_VERDICT=CHALLENGED` / `ACCEPTANCE_OFFICER_VERDICT=FAIL` (or PASS).
## Digest-basis rule (cost the planner a falsified draft)

Before calling any recorded digest "stale", establish WHICH BYTES it was computed over. An evidence
manifest built from a worktree hashes worktree bytes (CRLF on Windows); comparing it against the
git blob (LF) or against the current worktree alone manufactures false staleness. Classify each
mismatch against every plausible basis - current worktree, blob at the manifest's sealed candidate,
CRLF and LF normalisations of both - and report UNEXPLAINED only when nothing fits. If the manifest
has no self-described basis, read its sibling seal for the candidate tuple and say so.

Keep per-criterion verdicts binary; put caveats in the evidence column.

## Lane-operation lessons (hard-won; each cost a full re-run)

- **Make the checker write its receipt BEFORE it investigates.** A long-context session can
  terminate with no error, no closing message and no receipt — the log simply stops after a tool
  result. Have the brief order `AO_VERDICT.json` created first as
  `{"verdict":"INCOMPLETE_IN_PROGRESS"}` and rewritten as each claim completes, so a death still
  leaves a partial receipt.
- **Cap every command's output and forbid whole-file dumps.** Multi-hundred-KB round artifacts are
  the usual context killer. `grep -n`, per-field `python -c`, `head`/`tail`; no command above ~200
  lines. Also cap the run: a command that would exceed ~3 minutes is skipped and recorded `NOT_RUN`
  with its reason, never hung on.
- **A lane that exits without a receipt is `NO VERDICT`, never a pass.** Record it as such, keep the
  log as failed-first evidence, and re-run with a tightened brief rather than inferring anything.
- **Each attempt has its own subject.** A new commit invalidates the previous receipt by
  construction; name the subject commit and tree in every attempt row.
- **`NON_MUTATION_VERDICT=PASS` does not refute a mid-run mutation finding.** The guard compares
  before/after; a checker that restores what its own mandated commands changed still violated the
  read-only rule *during* the run. The checker's blocking wording is authoritative; do not let the
  guard's PASS dilute it.
- **Read-only rules are satisfiable by fixing the tools, not by narrowing the rule.** When the
  repo's own mandated commands mutate tracked files, redirect the call site (`--artifact <tmp>`,
  `--out <scratch>`) so the literal rule holds. Narrowing the rule after a FAIL is moving the
  goalposts.
- **Verify the model lane with a two-turn tool call, not the catalogue.** A model listed by the
  endpoint can still be unentitled (`400 not supported when using Codex with a ChatGPT account`) and
  a thinking-mode model can die after the first tool call (`reasoning_content must be passed back`)
  when the adapter does not echo it. Probe with one tool call plus a follow-up, and declare any
  substitution instead of silently swapping.
- **Never hand a native binary an MSYS path.** `git clone /c/Projects/... <dst>` neither clones to
  the intended place nor fails loudly; it creates a `C:\c\...` tree. Pass `C:/...` to git, python,
  curl — MSYS `/c/...` is translated only by bash builtins.
- **An interrupted `git worktree add` leaves a worktree that looks catastrophic and is not.**
  Symptoms: `git worktree list` shows `locked ... (initializing)` and `git status --porcelain`
  reports every tracked path as a staged deletion (hundreds of `D ` lines) while the directory is
  fully populated. Cause: the add died leaving no `index` and a stale zero-byte `index.lock`. Do
  NOT conclude the work is destroyed and do NOT expect `git reset --hard HEAD` to fix it (with no
  index it cannot); the index.lock pedigree explains most of these cases but the repair does not need
  the pedigree. Establish safety by sampling the disk against HEAD —
  `git hash-object <f>` vs `git rev-parse HEAD:<f>` for two or three files — then
  `git worktree unlock <path> && git worktree remove --force <path> && git worktree add <path> <branch>`.
  Files present-but-untracked relative to an empty index are the tell that no real work existed.
- **A hex digest can trip the write guard by accident — disclose, never bypass.** A commit/tree sha
  whose letters happen to spell a guarded marker makes `write_file`/`patch` refuse a payload that
  contains no protected material at all. The sanctioned remedy is to rewrite the payload so the
  contiguous marker disappears: keep a safe prefix, record the full length, and add the exact
  command a reader runs to reproduce the value, then say in the artifact itself that the digest was
  reduced and why. Never route the same bytes through the terminal to dodge the guard, and never
  edit the guarded repo config to widen the route registry.
