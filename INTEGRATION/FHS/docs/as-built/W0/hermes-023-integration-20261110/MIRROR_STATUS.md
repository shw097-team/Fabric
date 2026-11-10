# MIRROR_STATUS — Hermes 0.23.0 × FHS W0→W1 integration (2026-11-10)

**NAVIGATION / EVIDENCE MIRROR ONLY.** `effect_permission = NONE`. Nothing here grants a permit,
compiles PI, issues a WorkOrder, or signs an acceptance.

| field | value |
|---|---|
| subject | W0 six-WP contract coverage on Hermes 0.23.0 (`hgk-governed`) |
| verdict | `PARTIAL_INTEGRATION` |
| why not higher | `WP-FHS-01` A2 holds 15 `ORACLE_ENUM_ABSENT` families; `E01` and `E33` are partial; `E36` has no consumption evidence |
| claim ceiling | author-side measurement, not `ORIGINAL_ACK`, not `NATIVE`, not `RELEASE` |
| signed source | W0 r26, 668,540 B, `0ea05544499478859856f28da0c510bf0fb9b30109ecb577c00a907b435d3e0f` (3 copies, 1 digest) |
| receipts | 6/6 verify with the original reader; they bind candidate `r15`, **not** any WP artefact |
| negatives | 4 baselines + 8 negative/consumer controls, all detected (`NEGATIVES.json`) |
| host | Hermes 0.23.0 / `786a3156d1db` / PID 22880; production 0.22.5 / PID 15576 untouched |

## What a reader may conclude

- the six W0 work packages have 13 of 17 acceptance atoms backed by re-derivable evidence;
- the three lanes are `LIVE_UNVERIFIED` this round (`--menu` 9/9 admitted, four bindings `--assert` OK,
  retired arm refused with exit 9) — legality proven, liveness not;
- the three domain repositories are in three different supply-chain states (see the result document §3.2).

## What a reader may not conclude

- that W0 is complete on 0.23.0, that any original reader accepted a WP artefact, or that this mirror
  is ratified. `INTEGRATION/MANIFEST.json` and `repository-map.json` are untouched by this branch.
