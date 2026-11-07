# FHS W0-W2 As-Built writeback — start here

Generated 2026-11-07T23:10:08+0800. This directory is the local delivery; the GitHub side is a docs-only,
non-authoritative candidate PR in Fabric.

## Read in this order

1. `SESSION_W0_W2_WP18_MATRIX.json` — every one of the 18 work packages with its state and what is
   still missing. If you read one file, read this.
2. `W0/`, `W1/`, `W2/` — each contains the new full L3 text plus its manifest, evidence index,
   hold/resume list, delta/test result and closeout decision.
3. `proposed_reader_map.json` — what the effective reader map would become *after* the original
   authors accept these texts. Until then it is not in force.

## What the states mean

`IMPLEMENTED` (code on a branch or merged, no domain ACK) · `TESTED` (recomputable raw at its own
layer) · `ORIGINAL_ACK` (an original reader receipt — **zero** this round) · `NATIVE_WORLDRAW` (a real
world effect — **none**) · `INDEPENDENT` (different-SID protected checker — **none**) · `NOT_RUN` ·
`HOLD` (named resume predicate).

## The three hard blocks, in order

1. **R1**: only the OWNER can run `--reissue-issuer`. Until rev14 exists there is no Issuer Permit.
2. **GJ02 case source**: `pipeline.intake` needs a clause-bound source; none exists in SBL, and the
   maker must not author the requirement it then satisfies.
3. **Fabric policy effectiveness**: `FABRIC_ACTIVE_EPOCH@1` needs a Policy-Owner signature against a
   pinned key, then a real Host load, then an HGK consumer ACK. Reader-level `BOUND` is not effect.

## Reproduce

`SHA256SUMS` covers every file here. Each `*_EVIDENCE_INDEX.json` lists the round artifacts backing
that wave with their digests; each entry names the tool that produced it.
