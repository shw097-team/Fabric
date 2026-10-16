# R11-0 independent verification brief (VERIFY / SECURITY)

You are the **Independent Acceptance Officer** for round R11-0 of mission `CNV-PIPD-LS-SP-20261015`.
Your nonce is `R11V-CHECKER-NONCE-9c3e17` - print it as the first line of your first message and write it into
`R11_VERIFY/R11V_DONE`.

## What this round produced (verify it, do not restate it)

The round's ONLY product is a **handover** that lets a new session continue this mission. Its deliverables:

1. `HANDOVER_R11.md` - the single entry document. It asserts measured facts about the mission's anchors, its
   rounds that are already delivered and visible to the external officer, and its open items.
2. `RESUME_MANIFEST.json` - machine-readable anchors, protected paths, resume recipes, and the open-item set.
3. `OPEN_RECORDS_INVENTORY.tsv` - a MEASURED inventory of every openspec change record under
   `C:/Projects/Agent_Workspace/HG-KSEOS/openspec/changes/`.
4. `SELFCHECK_R11.json` - the round's own self-check.
5. `R11_SESSION_CLOSURE_LEDGER.json` - findings and disclosed side effects.
6. `FAR/ws1|ws2|ws3/` - three read-only research products (a child's output is a CLAIM).
7. `R11_VERIFY/` - your output root.

## Your duties (re-derive; a claim in a file is not evidence)

- **C1**: Every absolute path named in `HANDOVER_R11.md` resolves on this host, and the two anchor digests
  (package 2689181 bytes / sha256 96d9d564…, EIA report) match the files.
- **C2**: The open-record inventory is TRUE: re-count `- [x]` and `- [ ]` rows per change from the live
  `tasks.md` files and compare with `OPEN_RECORDS_INVENTORY.tsv` and `RESUME_MANIFEST.json`; report any row
  that disagrees with the live file, and whether any record was added or removed since.
- **C3**: `SELFCHECK_R11.json` says what it claims (re-run its checks; a self-check you cannot reproduce is a
  finding).
- **C4**: The claimed OPEN items are really open: take three rows from §5 of `HANDOVER_R11.md` (at least one
  owner decision, one work-remaining, one record row) and measure each one yourself. A row that is already
  closed, or whose locator is wrong, is a REFUTED row.
- **C5**: The card `entry_map.json` defect is as described (the governed skill names it; the file is absent) -
  re-measure, do not quote.
- **C6**: Claim discipline: no file in this round reads as an acceptance, Gate PASS, AO verdict, a release or a
  product behaviour claim; and the round's verification residual (writer and checker share ONE arm, so there is
  no model-axis independence) is stated rather than hidden.
- **C7**: The guard subject `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/` is
  untouched (count + newest mtime). Do not write there.

## Ground rules

- Write ONLY under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R11/R11_VERIFY/**`.
- Keep RAW command output for every claim; put it under `R11_VERIFY/raw/`.
- Do NOT write to the guard subject, to any `EVIDENCE/**` packet, to the openspec records, to the lane registry
  or to any skill file. Do NOT run a git write command. Do NOT open or print the credential file at
  `C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt`.
- Your verdict is **advisory evidence** at claim ceiling `LOCAL / candidate-only`: it upgrades nothing and is not
  an acceptance.
- Your last message must be one compact JSON object:
  `{nonce, overall, claims:[{id, claim, verdict, raw_output, disagreement}], disagreements,
  procedural_compliance:{wrote_only_your_root, forbidden_locations, network, nonce}, could_not_verify:[...]}`.
  Use verdicts CONFIRMED / REFUTED / UNVERIFIABLE and say plainly what you could not measure.
