<!-- Transcribed from the read-only verifier lane's stdout. The lane reported that it could not write
     this file itself: the sandbox withholds write authority, so the verdict exists only in its stdout
     stream. Provenance: stdout sha256 7cbfd5336955b464d5ec20a66c3ae91e646cd4a2889525ecd21807f9ca5151b6, 25255 bytes, transport opencode-go/deepseek-v4.1-flash,
     lane receipt LANE_VERIFY_RECEIPT.json. Transcription is mechanical (JSON string unescaping only). -->

## V1
V1 CLEAN: 47 identifiers compared (13 PR numbers #3-#15; 12 merge commit shas including `bcd91043b89b69c9d2f08309e46e31898ac87d89`; 12 changed-file counts 581/306/359/74/120/131/69/350/77/33/55/83/31; 12 head branch names `evidence/cnv-pipd-ls-sp-20261015-r6..r11`, `pub/lane-reliability-closure-20261016`, `pub/far-remediation-and-closure-20261016`, `pub/round3-lane-rebind-and-closure-20261016`, `evidence/cnv-evidence-archive-r7r11-20261016`, `evidence/far-018-r7r11-residual-closure`, `evidence/far-019-owner-auth-closure`, `evidence/cnv-far018-far019-archive`; blob count 4145; tree count 629; blob sha `9dd1946c3a7c9c76089c814b7ec75c46ab1210b2`). All match the task file values exactly.

## V2
V2 CLEAN: no number, link, branch, or PR in the artefact is absent from the task file. Counts (2, 221, eight, 4145, 629, 4732, 72, and the per-PR file counts) and PR numbers #3-#15 are all traceable. The `#15` row preserves the task's open-PR parenthetical verbatim.

## V3
V3 CLEAN: five required items present, in order, each as a `##` level-2 heading with two-space wording exactly — `## What this repository is`, `## Where the evidence lives`, `## Pull requests and merge commits`, `## What is NOT claimed`, `## How to verify a claim yourself`. None missing, none extra.

## V4
V4 CLEAN: all seven non-claim groups present and phrased as non-claims ("No independent acceptance has been issued.", "No canonical AO acceptance is issued.", "is not a pass", "not proven", "ABSENT", "No CI status exists...", "The 221 acceptance cases have NOT been accepted.", "the eight runtime gates have NOT been accepted").

## V5
V5 CLEAN: no independent acceptance, AO acceptance, production/runtime release, passed CI check, or merged #15 is claimed; each is explicitly negated and #15 is marked `NO — open`.

## V6
V6 CLEAN: no credential, token, key, absolute local user path, or local filesystem path — only repository-relative `EVIDENCE/...` tokens, PR numbers, and shas.

## V7
Artefact is 68 lines (4840 bytes) → within the requested 60-110 range.

VERDICT: PASS

Note: this is a finding set, not the output file. The task requires the result to exist as `.../lane_out_verify/VERDICT.md`; delivering that needs write authority that the current read-only sandbox withholds. If you want it landed, re-run me where that one path is writable (or grant the write), and I will emit exactly the block above to that file.
