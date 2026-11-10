# MIRROR_STATUS_FABRIC — W0 r26 mirror, Fabric-side admission (EC-R26-013 / R26-09)

**State: `ADMITTED_FOR_NAVIGATION_ONLY`. This supersedes `candidate / not policy loaded`.**

| field | value |
|---|---|
| subject | `FHS-W0-PIPD-LS-PKG-r26` |
| mirror path | `INTEGRATION/FHS/docs/as-built/W0/r26/FHS_PIPD-LS-PKG_W0_r26.md` |
| `sha256` (re-hashed from the mirrored file itself) | `0ea05544499478859856f28da0c510bf0fb9b30109ecb577c00a907b435d3e0f` |
| `bytes` | `668540` |
| source | `shw097-team/SBL@1cb8abb0ef118bdd80b08961fd9ca54c657881b9` |
| `effect_permission` | `NONE` — identical to `FHS-NAV/v2` (`INTEGRATION/FHS/repository-map.json`) |
| `admission_state` | `ADMITTED_FOR_NAVIGATION_ONLY` |
| `claim_ceiling` | `MIRROR_ADMITTED_FOR_NAVIGATION_WITH_BOUND_DIGEST_ONLY` |
| admission record | `INTEGRATION/MANIFEST.json` → `subject_admissions[0]` (`admission_id` `ADM-FABRIC-R26-FHS-W0-MIRROR-001`) |
| reader | `INTEGRATION/FHS/tools/validate_manifest_admission.py` |

## What changed, exactly

1. `INTEGRATION/MANIFEST.json` gained **one** additive key, `subject_admissions`, holding one entry for the
   r26 mirror. No pre-existing key, value or array element was edited; the diff is a pure insertion of 25
   lines before `approval_list_status`, and `--baseline` against `3b47550:INTEGRATION/MANIFEST.json` proves
   it (`ADDITIVE_ONLY_VIOLATION` fires if any older entry moves).
2. The digest in that entry was **measured here**, by re-hashing the mirrored file in this repository. It
   agrees with `r26/MANIFEST.json` and `r26/SHA256SUMS`, and it was not copied from either of them.
3. This file was added, stating the rated state. It is the Fabric-side status, not a rewrite of the
   mirrored payload.

## Why `ADMITTED_FOR_NAVIGATION_ONLY` and not `ADMITTED_FOR_CONSUMPTION`

`FHS-NAV/v2` declares `effect_permission=NONE` and `source_state=PROPOSED_NOT_OWNER_RATIFIED`. Nothing in
this repository loads, caches or serves the r26 document as policy — there is no loader, no daemon and no
consumer that reads it at request time. `ADMITTED_FOR_CONSUMPTION` would assert that the mirror *is*
policy for a surface that serves it; that assertion has no artifact behind it here, and the reader refuses
it while `effect_permission` is not `WRITE` (`ADMISSION_STATE_PERMISSION_MISMATCH`). So the highest honest
state is the navigation one: the mirror is admitted, the digest is bound, and the permission stays `NONE`.

This is deliberately **not** an upgrade of navigation into write authority. `effect_permission` is copied
unchanged from `FHS-NAV/v2`, and `EFFECT_PERMISSION_ESCALATION` refuses any entry that outranks it.

## Why `r26/MIRROR_STATUS.md` was not edited

`r26/MIRROR_STATUS.md` is part of the mirrored payload. Its digest is pinned twice — in
`r26/MANIFEST.json` (`7581614f…`, 804 bytes) and in `r26/SHA256SUMS` — and `r26/PROVENANCE.json` asserts
that it "describes exactly the files beside it". Editing it in place would either break two pinned digests
or force a rewrite of a manifest entry, and adding files *inside* `r26/` would falsify that
"exactly the files beside it" sentence without touching it. The Fabric-side state therefore lives here, in
the sibling directory, and the payload stays byte-identical:

- payload `r26/` — untouched, all 9 files and all pinned digests unchanged;
- `r26-admission/` — this file plus `F0_POLICY_CONSUMER_TRACE.json` (the consumption trace).

## What is still not claimed

Not owner-ratified, not externally accepted, not loaded as policy, no write authority, no live world
effect. `FHS_ORIGINAL_ACK 6/6` keeps its lane-qualified meaning and is not a release grant. `FHS-NAV` is
not "effective for all sessions": this repository admits one mirror for navigation, with its digest bound.
