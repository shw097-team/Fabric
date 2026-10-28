# LANE BRIEFS — round CNV-OWNER-DECISION-MAIN-LANDING-20261016

Three lanes read this one file. Each lane reads ONLY its own section, writes ONLY the one file named in that
section, and echoes its own nonce. All paths are absolute Windows paths with forward slashes.

Frozen inputs, all under `C:/Projects/Agent_Workspace/_handover/CNV-OWNER-DECISION-MAIN-LANDING-20261016/`:

- `subject3/PR_FACTS.json` — live-read facts about the two open pull requests, the default branch and its tree.
- `FAR_RULING_2.json` and `FAR_STUDY_AND_RULING_2.md` — the round's ruling, nine options with dispositions.
- `../FAR-20261019-owner-authorized-closure/RC1_OPEN_ITEM_UNIVERSE.json` — 100 open items, each with an `id`,
  a `kind`, a `title` and a `minimal_action_form`.

---

## SECTION A — lane PLAN (model: GPT 6.1 SOL-MEDIUM)

Read `subject3/PR_FACTS.json` and `FAR_RULING_2.json`. The round proposes to merge both open pull requests into
the default branch and to leave its own new pack open. Your job is to be the independent planner, not an echo.

Write exactly this file: `lane_out_plan/A_PLAN_NOTES.md`

It must contain, in order:

1. `## Independent recommendation` — one line per pull request: MERGE or HOLD, with the single fact from
   `PR_FACTS.json` that decided it. If the facts do not decide it, say what is missing.
2. `## Strongest argument against each merge` — the best case for NOT merging, stated as strongly as you can,
   and then whether it survives the facts.
3. `## Order and blast radius` — the order the two merges should happen in, and what a reader would see on the
   default branch after each one. Note that pull request #15 is a pure evidence pack and #16 changes the
   repository's front page.
4. `## What you could not verify` — a list, or the single word `none`.
5. `## Residual risk after both merges` — what remains unproven even if both merges succeed.

Rules: write only that one file; run no command that changes anything anywhere else; do not add a licence, a
workflow, a badge or a link; do not include any credential, token or key; keep it under 80 lines.

The first line of your first message must be exactly: `NONCE-ACK: CNVH-PLAN-3a91f2`
The last line of your final message must be exactly: `NONCE-DONE: CNVH-PLAN-3a91f2`

---

## SECTION B — lane EXECUTE (model: DeepSeek V4.1 Flash)

Read `../FAR-20261019-owner-authorized-closure/RC1_OPEN_ITEM_UNIVERSE.json`. Take every item whose `kind` is
`OWNER_DECISION` and every item whose `kind` is `BLOCKED`. There are 14 of each; if your count differs, say so
with your count instead of forcing the number.

Write exactly this file: `lane_out_exec/OWNER_BULLETIN.md`

Format — a five-line preamble, then one row per item:

- `## What this is` — three lines: this is a preparation, not a decision; nothing here is signed, accepted or
  closed; every id is traceable to the universe file.
- `## Rows` — a markdown table with the columns: `id` | `what it needs, in one sentence` | `already prepared` |
  `only the owner can supply` | `smallest action`. Keep each cell to one short sentence. Use the item's own
  `minimal_action_form` where it exists; otherwise derive it from the title and say nothing you cannot support
  from the file.
- `## External actors` — one line per row whose need is a party that is not the owner (a second operating-system
  identity, a signed certificate, an external oracle, another repository's owner).

Rules: write only that one file; do not use the words accepted, approved, signed or released about anything you
write; do not claim any item is closed; do not include any credential, token, key or absolute user path; keep it
under 100 lines. State plainly, in the preamble, that the count of rows is your own reading of the file.

The first line of your first message must be exactly: `NONCE-ACK: CNVH-EXEC-7b40c8`
The last line of your final message must be exactly: `NONCE-DONE: CNVH-EXEC-7b40c8`

---

## SECTION C — lane VERIFY_SECURITY (model: GPT 6.1 SOL-MEDIUM), READ-ONLY

You are a read-only checker. You may write ONLY the one file named below and nothing else anywhere.

Subjects: `subject3/PR_FACTS.json`, `lane_out_exec/OWNER_BULLETIN.md` (if it exists; if it does not, record that
as `V5 UNVERIFIABLE: bulletin absent`), and `FAR_RULING_2.json`.

Re-derive these checks yourself from the frozen facts. Do not trust any summary of them, including the ones in
this brief.

- `V1` — Additivity: does every pull request in `PR_FACTS.json` show zero deletions in total AND an empty
  `files_with_any_deletion`? Report any file with a deletion.
- `V2` — Surface safety: does either pull request touch `.github/`, a workflow, or a binary-shaped path? Report
  each file whose path merely contains a word like `secret` or `token` and say whether its content is a scanner
  or report rather than a credential store.
- `V3` — Front-page honesty: does `PR_FACTS.json` support the homepage's non-claims — in particular that the
  repository has no workflow (so no continuous-integration status can be claimed) and no root licence?
- `V4` — Mergeability: are both pull requests reported mergeable and clean, and is the recorded head the head of
  its branch as listed in `branches`?
- `V5` — Bulletin compliance: does the bulletin avoid claiming any acceptance, signature or closure, and is every
  id it lists traceable to the universe file? Name any id that is not.
- `V6` — Leakage: does any artefact under the round directory contain a credential-shaped string (a token prefix
  or a key block)? Check the bulletin and the ruling in particular.

Output exactly this file: `lane_out_verify/VERDICT3.md`

One `## V<n>` heading per check with its finding, then a final line `VERDICT: PASS` or
`VERDICT: FAIL_WITH_FINDINGS`. Use PASS only if V1-V4 are clear and V5-V6 are clear or explicitly unverifiable
with a reason. List defects, not praise.

Rules: read-only; do not modify any other file; do not include any credential, token or key in your output; if
you cannot check something, write `V<n> UNVERIFIABLE: <reason>` rather than assuming it passes.

The first line of your first message must be exactly: `NONCE-ACK: CNVH-VERIFY-5e63d1`
The last line of your final message must be exactly: `NONCE-DONE: CNVH-VERIFY-5e63d1`
