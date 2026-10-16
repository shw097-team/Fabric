# EXECUTE BRIEF — FAR-20261016-018 (bounded writer, EXECUTE lane)

You are the bounded writer for FAR round FAR-20261016-018. This brief is the whole specification.

NONCE: your FIRST line of output must be exactly `CNVEA-FAR018-EXECUTE-NONCE-9d41c7` and your LAST line
must repeat it. Do not omit either.

## Write root (hard)

You may create/modify files ONLY under `writer/` inside
`C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/`.
Read anything you like. Never edit: any file outside that `writer/` dir, any earlier round's directory,
the Hermes skills tree, or any file under `C:/Projects/Agent_Workspace/HG-KSEOS/config/`. No git commands,
no network calls, no package installs. Python: `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe`
(run with `-B`).

## Measured facts you must build on (do not re-measure, do not contradict)

- OS-enforced write denial IS achievable on this host: an owned directory accepts a baseline write, then
  `icacls <path> /deny <identity>:(OI)(CI)(W)` makes the write fail with `PermissionError: [Errno 13]`, and
  removing the ACE restores it. Identity: `desktop-57eo414\user`. Owner SID
  `S-1-5-21-2687334950-3868438633-1592137926-1000`.
- The same identity can remove its own deny ACE, so this is ordinary denial, NOT an immutable boundary.
- The Hermes skill's index file is absent; its five moved-payload pointer lines all verify (offset+length+
  sha256 exact) and point at four topic files under the skill's `references/topics/`.
- The previous round's `self_check.py` has a check whose success value is the literal `True`, so it can
  never fail; it also computes a variable it never uses.

## Deliverables (exactly five files, plus a manifest)

**A1 `writer/checker_isolation_probe.py`** — reusable, fail-able OS isolation harness.
- `--root <dir>`: must default to a temp dir the script creates; it must never touch anything outside it.
- Sequence: create probe dir → baseline write must SUCCEED → apply deny ACE for the current identity →
  write must be DENIED (record raw stderr) → remove ACE → write must SUCCEED again → remove probe dir.
- Always remove the deny ACE and the probe dir in a `finally` block; verify removal and record it.
- Emit one JSON receipt to stdout: identity, probe path, each command argv, returncode, raw stdout/stderr,
  the three booleans, cleanup verification.
- The receipt MUST carry an explicit limit field stating that the denying identity can lift its own ACE, so
  this proves ordinary denial and not an immutable boundary.
- `--self-test`: run a mutation where the deny step is SKIPPED and assert the harness REPORTS FAILURE
  (i.e. the check that should catch a missing deny must fire). Print `SELF_TEST=PASS` only when that
  mutation is detected. This is the guard against a vacuous probe — it is mandatory.

**A2 `writer/self_check_v2.py`** — the de-vacuumed check.
- Read the previous round's lane receipts at
  `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/lane/EXECUTE_RECEIPT.json`
  and `.../lane/VERIFY_RECEIPT.json`.
- Implement a check named S8b that actually asserts: (a) each receipt's identity gate has
  `required_arm == served_arm`; (b) the pair of arms is stated; and (c) **when the two arms are EQUAL the
  receipt must declare that model-axis diversity is absent**. The verdict is computed, never a literal.
- `--negative-control`: copy the receipt JSON in memory, strip the disclosure text, and assert the check
  now returns FAIL. Print `NEGATIVE_CONTROL=PASS` only if it fails as required.
- Exit non-zero if the check is vacuous: include a self-assertion that the returned verdict changes between
  the unmodified and the stripped input.

**A3 `writer/regen_entry_map.py`** — partial skill index reconstruction.
- Locate the skill dir by the well-known path under the Hermes home:
  `.../LocalCache/Local/hermes/skills/software-development/hgk-governed-execution` (SKILL.md is there).
- Parse every `SKCV-POINTER` line under `references/*.md`, resolve its target relative to the skill dir
  (strip a leading `skill/` prefix if present), and verify `sha256(bytes[offset:offset+length])`.
- Write `writer/entry_map.json` containing: the skill path, the generation method, every pointer record
  (pointer file, target, offset, length, claimed sha256, actual sha256, verdict), the list of destination
  topic files, and an explicit `coverage` block stating that this is a PARTIAL reconstruction and naming
  what it does not cover (the original index's full field set).
- Any pointer that does NOT verify must abort with a non-zero exit and a typed error; never emit an index
  containing an unverified pointer.
- `--self-test`: perturb one pointer's recorded digest in memory and assert the verifier ABORTS.
  Print `SELF_TEST=PASS` only when that abort happens.

**A4 `writer/metadata_semantics.py`** — mutable-subject metadata semantics.
- Read `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/A00_SOURCE_LEDGER.json`.
- Decide mutability per row: a row whose locator is a database file (`*.db`, `*.sqlite`) or a directory is
  MUTABLE_LIVE; everything else is IMMUTABLE_FILE.
- Emit `writer/METADATA_SEMANTICS_V2.json`: for every row, its id, locator, class, the recorded sha256, the
  live sha256 if the subject still exists, `hashed_at` semantics, and a `byte_exactness_claim_allowed`
  boolean that MUST be false for MUTABLE_LIVE rows.
- Emit a machine-readable `schema_addition` object naming the new fields and why each mutable row must be
  excluded from byte-exactness claims.
- Do NOT rewrite the input ledger. Assert in the output that the input file's mtime and sha256 are unchanged
  across the run.
- `--self-test`: assert that the count of rows with `byte_exactness_claim_allowed == true` equals the count
  of IMMUTABLE_FILE rows, and print `SELF_TEST=PASS`.

**A5 `writer/cross_index_v2.py`** — de-vacuumed presence indicator.
- Read the previous round's `A09_KLedger_CROSS_INDEX.json` and its `kledger/` inputs.
- Recompute the K-id set from the ledger input and the status split from the findings document.
- Emit `writer/CROSS_INDEX_V2.json` where the per-row `source_linked` is COMPUTED (the row's id must be
  present in the recomputed ledger id set) rather than hardcoded, plus `rows_checked`, `ids_expected`,
  `ids_found`, `missing_ids`, and an explicit `known_limit` field stating that this asserts PRESENCE, not
  re-verification, and that same-run retest remains 0 by construction.
- `--self-test`: inject a fake id into the expected set and assert the indicator reports the missing id
  (i.e. it can fail). Print `SELF_TEST=PASS` only then.

**A6 `writer/WRITER_MANIFEST.json`** — for each of A1–A5: relative path, bytes, sha256, and the exact
command you ran to exercise it, with its exit code and the `SELF_TEST=`/`NEGATIVE_CONTROL=` line you saw.

## Acceptance (you must run these and report the raw output)

For each script: run `--help`, then run it, then run its self-test/negative-control mode, and capture exit
codes. Every self-test must print its PASS token. If any self-test cannot be made to fail on mutation, say
so explicitly and mark that deliverable PARTIAL — do not round up.

## Claim ceiling

Report what the commands actually printed. Do not claim that any acceptance-report finding is closed, that
any checker boundary is immutable, or that anything is externally accepted.
