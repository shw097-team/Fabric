# WS-R9-B2 WRITER BRIEF — apply the VERIFIED successor candidate (`CANDIDATE_V2`) by overlay

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R9-0` · HGK project `CNV-R9-FARCLOSURE` (WO-TS-FARCLOSURE-03)
Role: bounded writer (Codex CLI EXECUTE lane). Authority: the FAR run `FAR-20261016-012` decision item 2, executed under this round's HGK admission.
**Claim ceiling: LOCAL / candidate-only.** A green harness run after the apply is a machine gate, not an acceptance, not a Gate PASS, not a release.

FIRST LINE OF YOUR FIRST MESSAGE and LAST LINE OF YOUR FINAL MESSAGE must both be exactly:
`R9B2-WSRITER-NONCE-2b7f91`

## 1. Situation (already established — do not re-litigate)

A first attempt to apply the repaired `hgk-governed-execution` slim candidate was **refused by this round's own
gate in two independent runs**: the harness's C6 check reported `live_references: 113, lost: 1` — the live
reference `references/product-branch-write-set-gates.md` (4986 bytes, sha256 `e59968d8fb23f18a…`) was absent
from that candidate and present nowhere in its corpus.

A successor candidate has been authored and **verified by the orchestrator**: it is the first candidate plus
that one file restored byte-identically. Running the round's own harness against it returns `overall: PASS`
(all of C1–C6 PASS). Your job is to APPLY that successor, by OVERLAY, and re-measure.

## 2. Paths (exact; do not substitute)

- Canonical target (the ONLY tree you may modify): `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/hgk-governed-execution`
- Successor candidate (the bytes to apply): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/CANDIDATE_V2/`
- Regression harness: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py`
  (usage: `--subject <tree> --live <tree> --out <json>`; pass NATIVE `C:/...` paths to it, never `/c/...`)
- Reusable rollback tool: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A/apply/rollback.py`
  (`--receipt <APPLY_RECEIPT.json> --preimage <dir>`, reads `{"dst":…, "paths":[{"path","action","before_sha256"}]}`, supports `--check`)
- Your write root (everything you produce): `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/WS_B2/` (create it)
- Interpreter, by absolute path: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`

Forbidden: any git write command and sending anything to any outside host; modifying any other skill; reading or printing credential files.

## 3. Procedure (in this order; paste each step's raw output into the receipt)

1. **Pre-image.** Copy the canonical target tree to `WS_B2/preimage/` byte-for-byte; record every path's sha256 + bytes.
2. **Pre-apply gate (must pass BEFORE you touch the target).** Run the harness against the successor candidate
   as `--subject` and the PRE-IMAGE as `--live`. Every check C1–C6 must PASS. If not, write the receipt with the
   failure and STOP — do not apply.
3. **Freeze the apply set.** Diff `CANDIDATE_V2` against the canonical tree; classify into `replaced` (present in
   both, bytes differ), `added` (candidate-only) and `canonical_only` (target-only). Write
   `WS_B2/APPLY_RECEIPT.json` with `dst` plus one row per changed path carrying `action` and `before_sha256`.
4. **Overlay — DELETE NOTHING.** Apply the candidate's `replaced` and `added` files. Every `canonical_only` file
   stays exactly as it is. This round's apply is deliberately non-destructive: the C6 gate forbids a deliberate
   deletion, and keeping a retained file costs nothing the round actually needs.
5. **Post-apply gate.** Run the harness with `--subject <canonical tree> --live <WS_B2/preimage>`. Every check
   C1–C6 must PASS. Paste the raw JSON.
6. **Rollback drill (on a COPY, not the live tree).** Copy the post-apply tree to `WS_B2/drill/`, point a copy of
   `rollback.py` + the receipt at `WS_B2/drill/` as `dst`, run it there for real, and confirm every restored file's
   sha256 equals its recorded `before_sha256` and every added file is gone. Paste the raw output. State plainly
   that the drill ran on a copy and the live tree was left APPLIED.
7. **Loader sanity.** With `HERMES_HOME` set to the canonical Hermes root, run the canonical runtime's own skill
   listing from the hermes-agent source with its venv python, and paste the row for `hgk-governed-execution`.
   If the skill is unavailable or its frontmatter unparsable, STOP and roll back.

## 4. Receipt (required)

Write `WS_B2/WS_R9B2_RECEIPT.json` + `WS_B2/WS_R9B2_RAW.md`: pre-image manifest count; the apply set by action class
with counts; both harness runs' raw JSON; the drill result; the loader row; an explicit list of what you did NOT
run; and any blocker with its raw error. Then write `WS_B2/WS_R9B2_DONE` containing only your nonce.

Final message: the counts applied, both harness verdicts, the drill result, the loader row, and the nonce.
