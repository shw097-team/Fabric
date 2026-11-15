# FHS workspace hygiene R2 — footprint and dispositions (candidate)

**Claim ceiling: CANDIDATE / LOCAL_MEASURED.** Not merged, not a reader ACK, not an HGK admission,
not a release. A pushed branch is not a merge; a green static check is not CI acceptance.

## What this round measured

| metric | value |
|---|---|
| control package | `FHS-WORKSPACE-RESIDUAL-FOOTPRINT-R2-THIN-CONTROL-20261110` r1, sha256 `05d048644f0e44926422b322ac21126463dad4aae1397de1a29061af7fc8c605` |
| workspace root before (measured) | 18.07 GiB / 429,668 files |
| workspace root after | 14.10 GiB / 304,623 files |
| moved out of the workspace (same-volume native rename) | 3.98 GiB / 304 operations / 124,953 files |
| archive: classified / unclassified | 125 / 180 items |
| identity readback | 302 trees byte-for-byte equal, 2 destination-superset, 0 losses |
| kept active (live dependency proven) | 7 trees / 11.19 GiB |
| held with reason | 75 trees / 2.22 GiB |
| regenerable cleanup | 0 bytes (nothing removed; the only remaining cache directory is ACL-refused) |
| free bytes on the workspace volume | before 50,588,123,136 → after 47,661,690,880 |

**Same-volume moves free no capacity.** The archived originals still occupy the same volume until the
user transfers the archive off-volume. The observed free-space change in this window is not attributable
to this round: another process was writing into the workspace root during the scan.

## Why the remaining tree is not "the same as before"

The residual mass is not unexamined: it is either tracked source, a live database, a fixed-path contract,
or a tree a live consumer actually reads. The three biggest held items are named with the exact evidence
in `R2_VALIDATION_SUMMARY.json` (`holds`). A round that reported a fixed target size would have had to
move one of them, and that would have broken a live path.

## Independent re-measure

A second lane re-derived the same root with PowerShell/`Get-ChildItem`, `cmd dir /s` and a .NET stack walk:
429,991 files / 18.08 GiB (this round's Python walk:
429,668 / 18.07 GiB). The tree changed while both were measuring
(+13 files / +82008 bytes over 12 minutes), so the spread is drift, not
disagreement.

## Not claimed

- Not a re-run of any wave work package, gate, quorum or signature.
- Not a statement that the external volume now holds this archive — the transfer is the user's step.
- Not a repair of the live registry's locator gaps; those are named and left to the owner.
