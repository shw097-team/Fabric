# HG-KSEOS (control plane) — upgrade index

Folder-local navigation for an external engineer planning an upgrade. Read
[`../INTEGRATION/UPGRADE-PLANNING-GUIDE.md`](../INTEGRATION/UPGRADE-PLANNING-GUIDE.md) first; this file only
tells you what is here and which document to trust first.

## What this folder holds
- contracts, typed lifecycle vocabulary, requirement/taskspec/workorder records, evidence receipts, lane configuration
- governance entry: `AGENTS.md`, `README.md`

## Trust order inside this folder
1. `AGENTS.md` (rules that bind every actor)
2. `README.md` (orientation)
3. the spine schema and typed lifecycle definitions
4. individual requirement/workorder receipts as evidence

## Planning notes
- A gate that is not named is not passed; a receipt is evidence of a run, not an acceptance.
- The runtime binding baseline is **not re-certified**; see `../INTEGRATION/KNOWN-FINDINGS.md`.

## Global rules that override anything here
- `HG-KSEOS` is the sole control plane; this repository is a projection, not an authority.
- See [`../INTEGRATION/NON-CLAIMS.md`](../INTEGRATION/NON-CLAIMS.md) and
  [`../INTEGRATION/KNOWN-FINDINGS.md`](../INTEGRATION/KNOWN-FINDINGS.md) before relying on anything.
- Generated 2026-10-13T12:23:20.088907+00:00.
