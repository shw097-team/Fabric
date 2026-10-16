# WS-A WRITER BRIEF — repair and land the slimmed `adversarial-verification-rounds` skill

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`. HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`,
WorkOrder lineage `WO-TS-CLOSURE-01..04`. Authority: PKG v2.0.0 G-A (Skills) + EIA-R6-09 + K-16/K-17.
Claim ceiling: **LOCAL / candidate-only**; your receipt is a claim, the orchestrator's re-run is the evidence.

## Why this turn exists
A regression harness was run against the frozen slim-skill candidate produced by the earlier
`SKILL-CONVERGENCE-20261014` round. Result (`WS_A_REGRESSION_CANDIDATE.json` in this directory):
- `C1 capacity` PASS — live main file is **101,488 bytes (over the 100,000 cap)**; candidate 22,091 bytes; 25 references ≤ 60.
- `C2 loader-shape` **FAIL** — the candidate `SKILL.md` carries 10 `SKCV-SLICE … END` marker lines and does
  **not** begin with `---`, so a skill loader cannot parse its identity.
- `C3 link-intake` PASS — all 8 referenced paths resolve.
- `C4 lossless` **FAIL** — 6 of 7 absorbed references verify (recorded sha256 == live bytes, bytes verbatim at
  the recorded topic offset); **`references/verifier-lane-handover.md` is STALE**: the stub records
  `aebb35ea…` while the live file is now `2126b82e…` (29,708 bytes) — the live tree moved after the freeze.
- `C5 controls` PASS — the harness's own negatives are detected.

So the candidate may not be landed as-is. Your job is the bounded repair + the guarded landing, with the
stale reference handled honestly (no silent overwrite of newer live text).

## Inputs (absolute paths)
- Frozen round: `C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/`
- Candidate: `…/candidates/avr/skill/` (SKILL.md, references/, references/topics/, scripts/)
- Live target (canonical Hermes skills tree):
  `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/adversarial-verification-rounds/`
- Harness: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py`
  (run it with `--subject <dir> --out <json>`; the interpreter is
  `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`)
- Your work root: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A/`

## Steps (do them in this order, record every command and exit code)
1. Copy the candidate tree to `WS_A/repaired_candidate/`. Never edit anything under the frozen round.
2. In the copy, remove every line matching `^=+\s*SKCV-SLICE.*$` from `SKILL.md`. Assert the result starts
   with `---` and that its frontmatter parses with `name: adversarial-verification-rounds`, `version: 1.0.0`.
3. `references/verifier-lane-handover.md`: **do not absorb it.** Copy the CURRENT live file verbatim into
   `WS_A/repaired_candidate/references/verifier-lane-handover.md`. Record it in the receipt as
   `EXCLUDED_STALE_ABSORPTION` with both shas.
4. Re-verify every remaining stub against the CURRENT live bytes: recompute sha256 of
   `<live>/references/<name>` and compare with the sha recorded in the stub. Any further mismatch is
   handled the same way as step 3 (carry the live file verbatim) and recorded.
5. Loss proof, from bytes (not from prose): for each absorbed reference assert the current live bytes appear
   verbatim at the recorded topic offset; and assert that every line of the live `SKILL.md` longer than 40
   bytes appears somewhere in (repaired SKILL.md ∪ topic files ∪ carried-live references). Save the raw
   output.
6. Run the harness against `WS_A/repaired_candidate` — it must print `verdict: PASS` (C1..C5). Save the JSON.
7. **Guarded landing** into the live skill directory:
   - `WS_A/apply/preimage/` — for every target path that already exists, a byte copy plus its sha256 and size.
   - `WS_A/apply/APPLY_RECEIPT.json` — per-path `before_bytes/before_sha256/after_bytes/after_sha256/action`
     (`added` | `replaced` | `retained_untouched`), plus the tree-level counts.
   - Copy the repaired candidate into the live directory: add files it has and the live tree lacks, replace
     files whose bytes differ. **Do not delete** any live file the candidate lacks; list those as
     `retained_untouched` in the receipt.
   - `WS_A/apply/rollback.py` — restores every pre-image byte-for-byte and deletes every file this turn added.
8. Re-run the harness against the **live directory** — must print `verdict: PASS`. If it fails, run
   `rollback.py`, re-run the harness to prove the live tree is back to its pre-turn state, and record the
   failure with the raw output.
9. Write `WS_A/WS_A_RECEIPT.md`: what ran, exact commands, exit codes, the before/after table, the excluded
   stale absorption, and an honest list of anything you could not do or verify. Print the same summary last.

## Hard constraints (a violation voids your turn)
- Write only under `WN_ROOT = C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A/` **and** the
  live skill directory named above. Nothing else on this machine.
- Do not modify any other skill, any HG-KSEOS file, any product repo, or the frozen round directory.
- Do not run any git write command and do not send anything to any outside host.
- Do not read, copy or print credential material.
- Do not claim the skill is "accepted", "approved" or "verified independent" — you are the maker; an
  independent checker runs after you.
- If a step cannot be completed, stop and record it as a blocker with the raw error. A partial result reported
  honestly is the required outcome; a fabricated pass is a failure.
