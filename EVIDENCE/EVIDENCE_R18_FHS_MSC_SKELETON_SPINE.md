# R18 evidence index (%s)

Round `R18-FHS-SKELETON-SPINE-20261029` against `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`.

Authoritative copies live outside this repo, in the round directory
`var/R18-FHS-SKELETON-SPINE-20261029/` (not published: no raw, DB, keys or credentials).

## What was measured

- source/manifest/ZIP/DAG currentness: 82 manifest rows, 83 checksum entries, 84 ZIP members
  22 nodes, 36 typed edges (`DATA_OR_ADMISSION` 34, `CAPABILITY` 2 — no acceptance edges)
- candidate validator re-run: 2789 PASS / 0 FAIL after a data-side pin repair (was 2788/1)
- 96-cell oracle re-run: 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL; 192 negative fixtures refused
- independent challenge lane (`gpt-6.1-sol`, rank 2, nonce-bound): verdict **HOLD**
- WP contract harness: 6 mechanical checks per WP over the DAG's own declared fields
- owner delegation signed and enforced: 7 WPs permitted, 6 negative controls refused

## What is NOT claimed

No native bundle, no Issuer PERMIT for HOST_OP/RELEASE, no acceptance signature, no release.
The independent verdict is HOLD because fixture consistency is not execution provenance.

Reading order: `FAR_R18_07_STOP_REVIEW_AND_OWNER_ENVELOPE.md`, `FAR_R18_09_CLAIM_RECHECK.md`,
`STATUS_HANDOFF.md`, `RESUME_HERE.md` in the round directory.
