# desktop-effect plane — upgrade index

Folder-local navigation for an external engineer planning an upgrade. Read
[`../INTEGRATION/UPGRADE-PLANNING-GUIDE.md`](../INTEGRATION/UPGRADE-PLANNING-GUIDE.md) first; this file only
tells you what is here and which document to trust first.

## What this folder holds
- documentation, guards and skills for the desktop-effect plane
- runtime state under `DESKTOP/var-fda/` (published as a named, bounded exception)

## Trust order inside this folder
1. the folder documentation
2. the guards (they define what may run)
3. the skills (they define how work is done)

## Planning notes
- `DESKTOP/var-fda/` is runtime state and documentation for planners, **not an approved payload**; see the manifest exceptions.
- No live-world effect is claimed anywhere in this folder.

## Global rules that override anything here
- `HG-KSEOS` is the sole control plane; this repository is a projection, not an authority.
- See [`../INTEGRATION/NON-CLAIMS.md`](../INTEGRATION/NON-CLAIMS.md) and
  [`../INTEGRATION/KNOWN-FINDINGS.md`](../INTEGRATION/KNOWN-FINDINGS.md) before relying on anything.
- Generated 2026-10-13T12:23:20.088907+00:00.
