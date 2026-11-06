# Repair note — the inputs your first verdict could not check

Your first verdict returned `FAIL_WITH_FINDINGS`, with V2 and V4 unverifiable and a V6 observation. This file and
`PR_FACTS2.json` answer them. Re-derive every check against `PR_FACTS2.json`; do not carry your earlier
conclusions forward unexamined, and do not treat this note as evidence — the facts are in the JSON.

## V2 — the two paths whose names contain `secret`

Both files were fetched from pull request #15's own branch and scanned for credential shapes. The results are
under `secret_named_artifacts_verified` in `PR_FACTS2.json`:

- `EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/A05_SECRET_SCAN.json` — the scan report; no credential-shaped
  string was matched in it.
- `EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/archive_secret_scan.py` — the scanner source; it matches an
  access-key shape, a private-key header and a token shape. A scanner must contain the patterns it searches for;
  the matched shapes are its detection patterns, not stored credentials. Decide for yourself whether that
  explanation is sufficient, and say so either way.

## V4 — binding each recorded head to its branch

`branch_tips` in `PR_FACTS2.json` now records the tip SHA of every branch, read live. `pr15_head_matches_branch`
and `pr16_head_matches_branch` record whether each pull request's `head_sha` equals its branch's tip. Re-derive
the comparison yourself from `pull_requests[].head_sha`, `pull_requests[].head_ref` and `branch_tips`.

## V6 — credential-shaped strings, restated precisely

The strings your first run found were in a local lane attempt log that is not part of any published pack, and in
the scanner source described above. Neither is a live credential, and neither is in the bulletin or the ruling.
Check `PR_FACTS2.json`, the bulletin and the ruling yourself and report what you find, including whether any
published artefact carries such a string.

## What is unchanged

The merge gate for this round is your verdict, not this note. If you still cannot clear V2 or V4, or if you find
a credential-shaped string in a published artefact, say so and the merges will be held.
