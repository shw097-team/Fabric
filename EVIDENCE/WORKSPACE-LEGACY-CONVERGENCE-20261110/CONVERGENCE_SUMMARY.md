# FHS active-footprint and legacy-state convergence (candidate)

**Claim ceiling: CANDIDATE / LOCAL_MEASURED.** Not merged, not a native reader result, not an HGK
admission, not a release. A pushed branch is not a merge; a static check is not CI acceptance.

## Scope

| field | value |
|---|---|
| control package | `FHS_ACTIVE_FOOTPRINT_LEGACY_CONVERGENCE_THIN_CONTROL-20261110` r1, sha256 `4e682adc75e1cc652c070eaeaabdb8b7ec62d2634cd6b7a6b62df41471417fc7` |
| workspace root before | 14.09 GiB / 304,500 files |
| three resident trees (incl. `.git` internals) | far-lane-sod-003 4.74 GiB, backups 2.27 GiB, PIPD 3.26 GiB |
| independent re-measure (PowerShell + cmd) | 304,635 files / 14.10 GiB — both engines agreed to 0 files / 0 bytes on every tree |
| moved out this round (same-volume rename) | 5.57 GiB / 36 operations / 60,988 files |
| blocked operation | 1 — `err 5 access denied`, a live build sandbox; journaled, not retried |
| kept hot | 0.77 GiB across 18 rows |
| held with reason | 1.65 MiB across 8 rows |

## What the evidence changed about the previous round's claims

- **"20 unpushed commits" does not reproduce as unpushed.** The PIPD clone has an upstream
  (`origin/candidate/r21-far-20261101`) and `rev-list --count --branches --not --remotes` = **5**;
  `HEAD --not --remotes` = **0**. The number 20 is `origin/main..HEAD` — a *lead over main*, not
  unpushed work. Two of the five carry product code and both are byte-identical to files already in
  SBL (`integrations/pipd/…pre_v2_adapter.py` and four pre-v2 schemas) — absorbed, with blob evidence.
- **"241 working-tree changes" reproduces but misleads.** 0 staged, 3 unstaged (all evidence files under
  `.hgk/`, one of them a negative-control mutation left unreverted), 238 untracked *directory* entries
  (25,985 files). No product source is dirty.
- **The SBL checkout does not contain the canonical tree.** `integrations/pipd/` exists on
  `SBL origin/main` (341 files) and is **absent** from the local `826ca066` checkout, which is 47 ahead /
  110 behind main. All canonical comparisons were therefore made against `origin/main`.
- **The filesystem locator plane was not measured by R1.** The live Shared Spine registry references
  40 `var/<child>` locators: 28 resolve in the workspace, 4 in the first-round archive on this volume,
  6 on the external volume, 2 now resolve nowhere. Decision material is published; **no database write
  was performed**.

## Not claimed

- No tree is reported as "retired": the hot subtrees and every owner-held item stay in place.
- No SBL or HG-KSEOS product PR was opened: the PIPD delta needs an owner ABI decision, and the HGK
  delta is empty (no native source or contract change was made).
- Same-volume moves free no capacity; the archive has not been transferred off-volume yet.
