# VERIFY BRIEF — round CNV-EVIDENCE-ARCHIVE-R7R11-20261016 (independent checker, re-derivation)

You are the independent verification lane. Your job is to re-derive the round's decisive claims from
raw inputs and say where they agree or disagree. You are NOT being asked to approve anything, and your
output is NOT an acceptance of any subject.

## 0. Nonce (mandatory, both ends)
CNVEA-VERIFY-NONCE-2b8d44
It MUST be the FIRST line of your FIRST message and the LAST line of your FINAL message.

## 1. Posture (hard)
- Write NOTHING. Do not create, edit or delete any file, anywhere. A write voids your verdict.
- The round root `C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/` is under
  a non-mutation guard: any change to it during your turn voids the verdict.
- Read-only shell commands are permitted for re-derivation. Never run a git write command.
- Python, when you need it: `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe`
- The Fabric mirror is a git repo at `C:/Projects/Agent_Workspace/Fabric` (its `origin/*` refs are the
  frozen PR heads). Treat it as read-only evidence.

## 2. Claims to re-derive independently (do all six)
For EACH, run your own command, report the exact command, and report `AGREE` / `DISAGREE` /
`UNVERIFIABLE`. `UNVERIFIABLE` is a valid and honest answer; `AGREE` from assumption is not.

**V1 — per-PR changed-file counts and heads.**
Input: `packet/PER_PR_TABLE.json` (if absent, use `A03_A05_PR_PREFLIGHT.json`).
Re-derive, for each of the eight PRs, the head sha of its branch and the number of paths that differ
from `origin/main`, e.g.
`git -C C:/Projects/Agent_Workspace/Fabric diff-tree --no-commit-id --name-only -r origin/main..origin/<head_ref>`
and compare with the row's `before_head` and `changed_files`.

**V2 — bounded evidence prefix (the change-class gate).**
Re-derive whether EVERY changed path of EVERY PR sits under that PR's single allowed
`EVIDENCE/<folder>/` prefix, and whether any changed path has a symlink/submodule git mode
(120000/160000). Report the exact number of escaping paths (0 expected) and the prefix actually found.

**V3 — the one hard secret finding.**
The round reports exactly one hard secret-shape hit, in PR #10, and claims it is a SYNTHETIC TEST
FIXTURE that already exists in `origin/main` (so it was not introduced by this round). The token's
sha256 prefix is `8b5c27ebdb59bdbd` and its length is 39 bytes; the canonical copy is claimed to live at
`HG-KSEOS/tests/test_knowledge_memory_poison.py` on `origin/main`.
Re-derive: find the token in the PR #10 evidence tree, hash it yourself, and check whether a
byte-identical token exists in `origin/main`. State whether the pre-existence claim holds.
Do NOT print the token value - report only its length and a hash.

**V4 — pack invariants.**
Read `packet/RETURN_PACK.json` and `packet/PER_PR_TABLE.json`. Check and report:
(a) eight rows, PR numbers exactly [4,5,6,7,8,9,10,11];
(b) every `merge_sha`, `readback_sha` and `maintainer_approval` is `null`;
(c) `archive_verdict == "TEMP_CLOSED"`, `production_verdict == "FAIL_CLOSED"`,
    `eia_20261016_disposition_count == 10`;
(d) no verdict-bearing field anywhere in either file contains the substring `PASS`
    (state the count of occurrences you found).

**V5 — K-ledger cross index counts.**
From `A09_KLedger_CROSS_INDEX.json` and the frozen `kledger/K_LEDGER_CROSSWALK.json` +
`kledger/KNOWN-FINDINGS.md`, re-derive: number of K rows, `source_linked` count, `same_run_retested`
count, and the baseline status histogram. The round claims 20 rows / 20 linked / 0 retested /
{RESOLVED 7, PARTIAL 7, OWNER 6}. Confirm or refute each number from the files yourself.

**V6 — preflight self-test non-vacuity.**
The round claims its secret scanner is non-vacuous: an injected positive control is detected and a
clean control is not. Look at `A03_A05_PR_PREFLIGHT.json` `scanner_self_test` and state whether the
record shows a positive control that was DETECTED and a negative control that was NOT, i.e. whether
the field could have been satisfied by a scanner that detects nothing.

## 3. Required output (stdout only, JSON, no file)
Emit exactly one JSON object:

```
{"checker_nonce":"CNVEA-VERIFY-NONCE-2b8d44",
 "checks":[{"id":"V1","verdict":"AGREE|DISAGREE|UNVERIFIABLE","command":"<the command you ran>","observed":"<short>","claim":"<short>"},
           ... V2..V6 ...],
 "overall":"AGREE|DISAGREE|PARTIAL_UNVERIFIABLE",
 "disagreements":["..."],
 "checker_wrote_files":false,
 "claim_ceiling":"candidate-round evidence re-derivation only; this is not an acceptance of the subject, not an AO verdict, and not a runtime or production claim"}
```

Then a short human-readable confirmation of the nonce.

## 4. What you must NOT do
Do not state or imply that any pull request was merged, that any product/runtime was released, that the
validator is accepted, or that the convergence is complete. Four of the round's claims are explicitly
`NOT_RUN` / `NOT_ACCEPTED` / `NOT_RECERTIFIED` / `FAIL_CLOSED`; if your report contradicts that lattice
it is wrong.
