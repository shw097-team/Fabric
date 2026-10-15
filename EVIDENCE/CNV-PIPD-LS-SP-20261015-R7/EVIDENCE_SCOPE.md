# EVIDENCE_SCOPE — what is published in this packet, and what is deliberately not

ChangeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION` (mission `CNV-PIPD-LS-SP-20261015`).
Claim ceiling: **LOCAL / candidate-only**.

## Published
- The round's governed records: the R7 plan/spec/checklist, the HGK typed admission, both briefs, the writer's
  artifacts and raw outputs (`R7_*`, `RAW/`), the checker's three attempts
  (`R7_CHECKER/` = attempt 3, the authoritative verdict; `R7_CHECKER_ATTEMPT1_VOID/`,
  `R7_CHECKER_ATTEMPT2_CONTENT_VOID/` = the two voided attempts, each with its own RAW outputs and, for
  attempt 1, the dispatcher's void marker), the disclosure and remediation records
  (`R7_CHECKER_DISPOSITION.md`, `R6_DELIVERY_RAW_RESTORE.json`, `R7_SIDE_EFFECTS.json`,
  `R7_TOOLING_FINDINGS.json`, `R7_NON_CLAIMS.md`, `R7_EXTERNAL_ACCEPTOR_GUIDE.md`, `R7_BASELINE_MAIN.json`).
- The FAR research run (candidate research product, not authority) as `FAR/FAR-20261015-010-*`.
- The R6R7 closure records previously held only in the workspace, as `R6R7_CLOSURE/*` — published so an external
  acceptor can re-derive them: post-commit readback, merge-and-closure, maintainer approval (and its request),
  the M2 scan at the final head, the handover state, the return pack, and the open-item list.
- `m2_scan.py` — the out-of-packet scope/secret scanner, so the M2 claim can be reproduced without trusting us.

## Deliberately NOT published (and why)
- **Lane scratch copies of whole trees**: `R7_CHECKER/pre/`, `R7_CHECKER_ATTEMPT2/{pre,checkproduct,MUTCOPY,INPUTS}/`,
  `R7_CHECKER_ATTEMPT3/{a3_driver,a3_mutc}/`. These are working copies of the product and control-plane trees that
  the lanes made under their own roots to run tests without touching the subject. They are not evidence: they
  duplicate megabytes, they contain symlink farms (some unreadable by ordinary traversal), and republishing copies
  of a product tree inside an evidence packet invites exactly the "which copy is the artifact" confusion this
  round is trying to remove. What matters from those runs is in the `RAW/` output files, which are published.
- **Anything under `EVIDENCE/CNV-PIPD-LS-SP-20261015/`** (the R6 archive) — unchanged and referenced by blob id,
  never re-published.
- **The R7 round's own publication records** (`R7_PUBLICATION_VERIFICATION.json`, the post-commit readback and the
  PR receipts): by construction they describe the push that carries this packet, so they are held outside the
  commit and reported in the pull request thread.
- **Credential material**: never read, never copied, never printed. The M2 record states an exact-substring check
  that the operator's credential value appears zero times in the packet.

## Note on byte fidelity
Evidence bytes are the subject of verification, so the packet sets `* -text` in `.gitattributes`: no line-ending
normalisation is applied, and every recorded sha256/blob id can be recomputed from the file as downloaded. A
checker pass that applied text filters produced false diffs (177 of 300) before being corrected — a reminder to
disable filters when comparing evidence bytes.
