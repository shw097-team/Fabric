# FHS W0–W2 As-Built writeback — NON_AUTHORITATIVE candidate

**Status: `NON_AUTHORITATIVE_DOCS_CANDIDATE`.** Four statements, so nothing here can be mistaken for authority:

1. These are **candidates**. The authoritative L3 texts remain the ones named by the effective
   `CURRENT_READER_MAP` in the author-side knowledge base. Nothing here supersedes them.
2. This directory creates **no** policy, gate, permit, registry entry or acceptance status. It does
   not change `effect_permission` (still `NONE`), `repository-map.json`, or `INTEGRATION/MANIFEST.json`,
   and it grants no writer, reader, issuer or checker capability.
3. Every appended chapter is **additive**: the parent L3 body is preserved byte-for-byte (verified:
   prefix sha256 equals the parent's sha256 for all three waves) and the CH structure is unchanged
   (W0 100, W1 103, W2 50 CH headings before and after).
4. Status words mean exactly this: `IMPLEMENTED` (code on a branch or merged, no domain ACK) ·
   `TESTED` (recomputable raw at its own layer) · `ORIGINAL_ACK` (**zero** this round) ·
   `NATIVE_WORLDRAW` (**none**) · `INDEPENDENT` (**none**) · `NOT_RUN` · `HOLD`.

## Read in this order

| # | File | Why |
|---|---|---|
| 1 | `SESSION_W0_W2_WP18_MATRIX.json` | all 18 work packages with state and the exact missing piece |
| 2 | `START_HERE.md` | orientation, the three hard blocks, how to reproduce |
| 3 | `W0/`, `W1/`, `W2/` | the full new L3 text plus manifest, evidence index, hold/resume, delta/test, closeout, handoff |
| 4 | `proposed_reader_map.json` | what the reader map would become **after** the original authors accept these texts — not in force now |

## The three hard blocks (in order)

1. **R1 Issuer re-registration** — only the single human OWNER can run `--reissue-issuer` in a
   protected terminal. Until registry rev 14 exists there is no Issuer Permit, so no lawful DEV.
2. **GJ02 case source** — `pipeline.intake` needs a clause-bound source locator and the SBL tree has
   none for GJ02. The maker must not author the requirement it then satisfies.
3. **Fabric policy effectiveness** — a `BOUND` record means artifacts were opened and re-hashed. It
   is not policy effect: `FABRIC_ACTIVE_EPOCH@1` still needs a Policy-Owner signature against a pinned
   key, a real Host load, and an HGK consumer ACK.

## Reproduce

`SHA256SUMS` covers every file in this directory. Each `W*/W*_EVIDENCE_INDEX.json` lists the
underlying round artifacts with their digests and the tool that produced each one.

## What this PR is not

It is not a merge request for Fabric policy, not a native acceptance, and not a request to change
this repository's navigation or permissions. The original maintainer decides whether this entry is
adopted at all; until then it is a read-only reference for external engineering.
