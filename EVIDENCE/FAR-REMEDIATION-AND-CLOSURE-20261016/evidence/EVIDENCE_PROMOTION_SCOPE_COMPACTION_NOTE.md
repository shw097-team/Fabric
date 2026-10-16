# Where the per-file promotion enumeration went, and why this note exists

`EVIDENCE_PROMOTION_SCOPE.md` ends one of its sections with *"Every file is individually listed in the
JSON."* **That JSON is not in this packet.** It is not missing by accident and it was not withheld; it was
compacted, and this note restores the disclosure that a later re-run destroyed.

## What existed, and what remains

| | |
|---|---|
| produced by | the read-only whole-tree walk of canonical vs the frozen candidate (this round's sub-agent) |
| named | `evidence/EVIDENCE_PROMOTION_SCOPE.json` — approximately **114 MB** of per-file entries |
| why not published | a 114 MB listing cannot ship in an evidence packet; the round's PLAN recorded the size, and the compaction branch in `apply_R2_promote.py` fires above 8 MB |
| what was retained | `EVIDENCE_PROMOTION_SCOPE.md` (method + counts + the PROMOTE set) and `EVIDENCE_PROMOTION_SCOPE.summary.json` (machine-readable counts, completeness and the exactness claim) |
| what was NOT retained | every individual per-file classification line |
| the original file's exact byte count | **NOT RECOVERABLE** — it was held only in `R2_PROMOTION_RECEIPT.json.enumeration_compacted`, which a later run overwrote (see below). ~114 MB is the figure this round's own PLAN states |

The counts survive because they are what the round's claims rest on: 243,465 canonical files enumerated,
243,272 known differences classified as **4 PROMOTE / 242,920 DO_NOT_PROMOTE / 348
NEEDS_OWNER_DECISION**, with 757 access-denied canonical directories and 3 reparse boundaries recorded as
**limitations rather than as completeness**. The exactness claim is therefore
`CANDIDATE_COMPARISON_COMPLETE; CANONICAL_ONLY_ENUMERATION_INCOMPLETE_ACCESS_DENIED` — an honest partial, not
a whole-tree certification.

## The defect this note is answering

`apply_R2_promote.py` records the compaction inside the receipt it writes. That script is idempotent (a
second run finds the files already identical and writes no bytes), and it was re-invoked during this round;
the re-run **rewrote the same receipt file**, and the rewrite did not re-visit the compaction branch because
the large file was already gone. The result:

1. the receipt of record contains **no** `enumeration_compacted` key (verified: it reads `null`),
2. so the only in-packet record of why the enumeration is absent disappeared,
3. while the surviving `.md` still pointed a reader at the deleted file.

**Three rules follow, and they generalise beyond this round:**

- A receipt that a re-runnable script overwrites is not a receipt. Either make the re-run APPEND a new
  revision, or make the destroy-only-once branch re-assert its record on every run.
- A written disclosure can be destroyed by a later idempotent run, so its survival needs a check — the same
  way a digest needs a check — not just a good intention at authoring time.
- A publication gate should extract every artifact filename the round's own documents cite and fail on any
  that is not present in the packet. Measured here: two citations (`FAR_RULING.md` lines 105 and 187) still
  name `EVIDENCE_PROMOTION_SCOPE.json`, and the `.md` names it again in prose. Nothing else in this round
  could see that, because every check compared counts, not citations.

## Claim ceiling

This note adds no measurement. It restores a disclosure and names a defect in this round's own tooling. The
promotion decision it describes is unchanged: **4 files, byte-verified, promoted under this round's
WorkOrders, with the governance limits stated in `FINDINGS_V3C_INDEPENDENT_VERDICT.md` (F-IND-3)**.
