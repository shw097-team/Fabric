# FHS W0 R4C implementation evidence index

**NAVIGATION / EVIDENCE ONLY · NON-AUTHORITATIVE · effect_permission=NONE · AUTHOR_LOCAL_TEST**

Input: ZIP `f3838fb095e56ea8d636e5c52f4bd69e9d529d110569b87376c168ea35ab2a2a`, body `56d0df3db6765ee780689ea687824ca891f5a366797e04cfe6ae7c0928173f2a` (463034 bytes, 50 chapters).

| WP | Status | Scope |
|---|---|---|
| `WP-FHS-00` | DONE_LOCAL | source probe, manifest two-way coverage, three-repo head drift, host probe |
| `WP-FHS-01` | DONE_LOCAL | authority classes + typed HOLDs; zero write authority, zero permit mint |
| `WP-FHS-15` | DONE_LOCAL | three heterogeneous SPECs + Goal to FUO chains |
| `WP-FHS-16` | PARTIAL | Need to Occupant matrix; 28 occupant pin holds + 2 host pin holds; no install |
| `WP-FHS-19` | PARTIAL | executable supply-chain gate; source package ships no SBOM, so WP19 DONE not claimed |
| `WP-FHS-21` | DONE_LOCAL | 96 typed oracle rows, S1-S5 seams, 22/36/E26/84/25/22, W1-W4 handoff; TraceClosure AUTHOR_STATIC only |

## Measured

- GSTACK invariants: 21 PASS / 0 FAIL / 0 HOLD.
- Goal to SPEC to FUO: 11 chains, 11 joined, 0 missing; Oracle96 96 rows, 96 pass.
- Holds: 53 carried (39 + 14 additional) plus 13 round-scoped holds; all OPEN.

## Not claimed

- `PIPD_CANONICAL`
- `HGK_ADMITTED`
- `HOST_NATIVE_E2E`
- `PROTECTED_CHECKER`
- `RELEASED`
- `WP19_DONE`
- `TraceClosure beyond AUTHOR_STATIC`

The runnable implementation lives in the SBL candidate PR under `integrations/pipd/w0/`; this page only indexes what was measured.
