# FAR study and ruling — CNV-OWNER-DECISION-MAIN-LANDING-20261016

Three subjects were ordered: what is waiting on the owner, which candidates and skills are actually
landable, and which unmerged candidates belong on the default branch. Each option below carries the
measurement it rests on, a friction/feasibility/necessity reading, and a disposition.

## Measurement

- Open item universe: {"BLOCKED": 14, "CLOSED_NOW": 6, "GAP": 28, "NEW_FROM_FAR018": 10, "OWNER_DECISION": 14, "RESIDUAL": 15, "UNLANDED_CANDIDATE": 13}
- Default branch: `bcd91043b89b`; branches present: evidence/cnv-far018-far019-archive, evidence/skill-convergence-20261014-full-packet, homepage/cnv-hygiene-readme-closure-20261016, main

- PR #15: head `a22ad7e17559`, mergeable=True/clean, 31 files, +6837/-0, secrets-shaped paths: ['EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/A05_SECRET_SCAN.json', 'EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/archive_secret_scan.py'], workflow paths: none
- PR #16: head `09b11bd235ef`, mergeable=None/unknown, 21 files, +3678/-0 (README +77/-0), secrets-shaped paths: none, workflow paths: none

## The defect this round repaired before recommending anything

The homepage candidate in PR #16 was published with CRLF line endings while the repository is LF-only (`old crlf=0`, `branch crlf=149`). The pull request therefore showed `+149/-72` in one hunk over the whole file: a front-page rewrite disguised as an addition. The rebuilt blob is `crlf=0`, and the diff is now pure insertion (`{"equal": 72, "insert": 77}`). The earlier claim that every other section was unchanged was false as published and is corrected here.

## Ruling

### R-B1 — Merge PR #15 into the default branch (EXECUTE_NOW)
- Ratings: friction LOW, feasibility HIGH, necessity HIGH, engineering weight NONE
- Gate: cross-model verifier PASS, then a fresh live read of mergeable/mergeable_state
- Why: 31 files, purely additive (+6837/-0), mergeable clean, and its blobs were read back byte for byte when it was published. It has been waiting only for a maintainer act.

### R-B2 — Merge PR #16 into the default branch (EXECUTE_NOW)
- Ratings: friction LOW, feasibility HIGH, necessity HIGH, engineering weight NONE
- Gate: cross-model verifier PASS; HOLD and re-read if mergeable is unknown rather than retrying blind
- Why: It puts the corrected homepage on the default branch. Its one real blocker was found and repaired this round: the published copy used CRLF line endings where the repository is LF-only, so the homepage diff rewrote all 72 lines (+149/-72) and the 'otherwise unchanged' claim was false. The repaired blob is +77/-0 and the homepage diff is now purely additive.

### R-B3 — Rebuild the homepage blobs with the repository's line convention (EXECUTED_THIS_ROUND)
- Ratings: friction LOW, feasibility HIGH, necessity HIGH, engineering weight NONE
- Gate: opcode check: the rebuilt text must produce insert-only diffs against the default branch
- Why: A merge that rewrites every line of the front page is not a reviewable change, whatever the text says. Detected by reading the pull request's own diff, not by trusting the earlier claim.

### R-B4 — Issue a one-page owner bulletin for the 14 items whose kind is OWNER_DECISION (EXECUTE_NOW)
- Ratings: friction LOW, feasibility HIGH, necessity HIGH, engineering weight NONE
- Gate: the bulletin may prepare and rank; it may not sign, accept or claim
- Why: Fourteen items are waiting on a human. The useful engineering act is to shrink each to one minimal action form with the prerequisite already prepared, so the owner's cost is a decision rather than an investigation.

### R-B5 — Measure the installed skill surface and state which skill items are landable without a signature (EXECUTE_NOW)
- Ratings: friction LOW, feasibility HIGH, necessity MEDIUM, engineering weight NONE
- Gate: measurement only: inventory, entry-map five-point status, loader smoke cases listed but not claimed as accepted
- Why: The honest answer to 'which skills are practically landable' starts with what is installed and what its loader actually selects, rather than with another skill file.

### R-B6 — Consolidate the skill references that cover the same topic instead of adding more (EXECUTE_NOW)
- Ratings: friction LOW, feasibility HIGH, necessity MEDIUM, engineering weight REDUCES_ENGINEERING
- Gate: the skill linter's own sprawl report is the measure; fold the new note into the existing topical reference
- Why: The linter already reported 114 files under references/. Adding a file per round is the drift this round is supposed to stop, so the round folds its lesson into the existing reference and says so.

### R-B7 — Name the external actor each BLOCKED item needs (PREPARE_FOR_OWNER)
- Ratings: friction LOW, feasibility MEDIUM, necessity MEDIUM, engineering weight NONE
- Gate: no agent may close an item that needs a second OS identity, a signed certificate or an external oracle
- Why: These 14 items are not blocked by work; they are blocked by a party that is not in this session. Recording the party is the only honest act available.

### R-B8 — Add a LICENSE, add continuous integration, or set repository metadata (REJECTED)
- Ratings: friction LOW, feasibility HIGH, necessity LOW, engineering weight HIGH
- Gate: unchanged from the previous round's ruling
- Why: A licence is a legal choice, a workflow would change how evidence is produced, and metadata is cosmetics. None of the three is this round's business, and each would look like progress.

### R-B9 — Merge this round's own pack (OWNER_GATED)
- Ratings: friction LOW, feasibility HIGH, necessity LOW, engineering weight NONE
- Gate: a round never merges its own delivery
- Why: Merging the pack that certifies the merges would make the round its own approver. The two previously verified candidates are merged; this round's pack is left open for the owner.

## Non-goals

- reopening the 221 acceptance cases or the eight runtime gates
- closing any item that needs a second operating-system identity, a signature or an external oracle
- touching the lane registry or route slots to make a lane succeed
- rewriting any published evidence blob
- deleting anything locally, including the control-plane database pre-images

## Claim ceiling

Candidate only. Nothing here is an acceptance, an acceptance-officer
decision, a release or a production effect.
