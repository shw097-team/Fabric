# Repo hygiene report — 2026-10-13T11:50:38.128148+00:00

Method: read-only GitHub API inventory of `main` before the change, then the same inventory after.
Counts are tree listings; nothing here is estimated.

| measure | before | after |
|---|---|---|
| blobs | 1994 | see `ExecutionReceipt` after push |
| `*.pyc` blobs | 127 | 0 (intended) |
| `*.lnk` blobs | 1 | 0 (intended) |
| root `.gitignore` | False | present |
| `INTEGRATION/MANIFEST.json` | present | present, reconciled |
| LICENSE | absent | **still absent — owner decision** |

## Findings addressed
1. **Declared-exclusion contradiction.** `MANIFEST.json` declared `var/` excluded while `DESKTOP/var-fda/**`
   was published. Direction chosen (lowest risk, keeps evidence intact): the **declaration is
   reconciled with reality and the runtime subtree is recorded as a named, bounded exception with its
   own disposition** — nothing was deleted for this finding.
2. **Generated files.** Bytecode and a Windows shortcut are not part of an approved payload; they are
   removed by omission from the new tree, and a root publish-control file prevents recurrence.
3. **Publication procedure.** No builder existed in-repo; this change-set is itself the recorded
   procedure (`SOURCE-PROJECTION.md` + this report).

## Findings deliberately NOT resolved here
- **LICENSE** — a legal choice; owner decision.
- **Large binaries** (16 blobs over 400 KB, largest 9,824,365 bytes) — evidence or source data;
  disposition is an owner decision, and deleting evidence to make a repo smaller is the wrong trade.
- **Remote linkage of the local `Fabric` tree** — owner decision.
- **Credential exposure** — measured **negative at the filename level** against the owner's credential
  file names and against `.env`; this is not a claim that no secret exists anywhere, and content-level
  scanning was not performed.

## Residual risk
`DESKTOP/var-fda/**` remains published as a named exception. It is runtime state and documentation for the
desktop-effect plane; anyone planning an upgrade should treat it as documentation, not as a payload.
