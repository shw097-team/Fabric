# WS-R9-B WRITER BRIEF — guarded apply of the repaired `hgk-governed-execution` slim candidate

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R9-0` · HGK project `CNV-R9-FARCLOSURE` (WO-TS-FARCLOSURE-03)
Role: bounded writer (Codex CLI EXECUTE lane). Authorization: the FAR run `FAR-20261016-012` decision item 2, executed under this round's HGK admission.
**Claim ceiling: LOCAL / candidate-only.** A green harness run after the apply is a machine gate, not an acceptance and not a Gate PASS.

FIRST LINE OF YOUR FIRST MESSAGE and LAST LINE OF YOUR FINAL MESSAGE must both be exactly:
`R9B-WSRITER-NONCE-9a4e2b`

## 1. What this is

In R8 a slimmed version of the skill `hgk-governed-execution` was produced as a candidate but **not** landable: two live reference texts did not survive into it. A FAR research worker has since verified — in scratch only — that restoring those two files verbatim makes the round's own regression harness pass all six checks (C1–C6), with zero references lost. Your job is to perform the **guarded apply** of that repaired candidate onto the canonical skill tree, with a pre-image, a receipt and a rehearsed rollback.

## 2. Paths (exact; do not substitute)

- Canonical target (the ONLY tree you may modify): `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/hgk-governed-execution`
- Repaired candidate (source of truth for the new bytes): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/FAR/ws3/repaired_candidate/`
- Regression harness (copy it into your own work root; do not run it from the R8 tree): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py` (usage: `--subject <tree> --live <pre-image tree>`)
- Reusable rollback tool: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A/apply/rollback.py` — it takes `--receipt <APPLY_RECEIPT.json>` and `--preimage <dir>`, reads `{"dst": <tree>, "paths": [{"path", "action": "replaced|added|retained_untouched", "before_sha256"}]}` and supports `--check`.
- Your write root (receipts, logs, copies): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/WS_B/` (create it).
- Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (absolute; do not rely on `python` resolving).

Forbidden: any git write command and sending anything to any outside host; modifying ANY other skill or any file outside the two trees above; reading or printing credential files; deleting anything in the canonical target that the harness does not certify as embedded.

## 3. Procedure (follow the order; each step's raw output goes in the receipt)

1. **Pre-image.** Copy the canonical target tree to `WS_B/preimage/` byte-for-byte (record every path's sha256 and byte count).
2. **Apply set.** Diff the repaired candidate against the canonical tree, path by path. Classify every canonical-only path as follows: it may be **removed** only if the harness's C6 check certifies its bytes are preserved inside the new main file; otherwise it must stay (`retained_untouched`). Build `WS_B/APPLY_RECEIPT.json` in the schema named in §2, with `before_sha256` for every path (and `after_sha256` for replaced/added).
3. **Apply** the candidate bytes into the canonical tree exactly as the receipt records.
4. **Verify (the acceptance gate).** Run the harness with `--subject <canonical tree> --live <WS_B/preimage>`. **Every check C1–C6 must PASS.** Paste the raw JSON. If any check fails, STOP, run the rollback, and report the failure with the raw output — do not adjust the harness.
5. **Rollback drill (required).** Not on the live tree: copy the CURRENT canonical tree (post-apply) to `WS_B/drill/`, point a copy of `rollback.py` + receipt at `WS_B/drill/` as `dst`, run it for real there, and confirm every restored file's sha256 equals its recorded `before_sha256` and every added file is gone. Paste the tool's raw output. State plainly that the drill ran on a copy, and that the live tree was left in the applied state.
6. **Loader sanity.** Run the repo's own skill listing through the canonical Hermes runtime (`HERMES_HOME` set to the canonical root, `./venv/Scripts/python.exe -B -m hermes_cli.main skills list`) and paste the row for `hgk-governed-execution` (expect source `local`, status `enabled`). If the loader reports the skill as unavailable or its frontmatter unparsable, STOP and roll back.

## 4. Receipt (required)

Write `WS_B/WS_R9B_RECEIPT.json` + `WS_B/WS_R9B_RAW.md`: the pre-image manifest count, the apply set by action class with counts, every step's raw output, the C1–C6 verdicts, the drill result, the loader row, an explicit list of what you did NOT run, and any blocker with its raw error. Then write `WS_B/WS_R9B_DONE` containing only your nonce.

Report in your final message: paths changed (replaced/added/removed counts), the C1–C6 verdicts, the drill result, and the loader row.
