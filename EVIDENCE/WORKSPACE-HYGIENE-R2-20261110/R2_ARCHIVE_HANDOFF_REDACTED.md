# R2 archive handoff (redacted)

**CANDIDATE / LOCAL_ONLY_INDEX.** How an external engineer would obtain the archived originals from the
owner. No inventory listing, no absolute paths, no credentials, no file contents.

## Shape

```text
<archive root>/                       # sibling of the workspace root, same volume
  01_已分類可封存/<original relative path>
  02_未分類可外移/<original relative path>
  R2_ARCHIVE_MANIFEST.tsv             # per tree: files, bytes, pre-move counts, identity digest, verdict
  RESTORE_NOTES.md
  _meta/                              # inventories, dispositions, move journal, cleanup journal, tools
```

Every archived tree keeps its original path relative to the workspace root, so restoring is one rename
back into place — not a copy, not a re-derivation.

## What a reader can verify here

- Per-tree file counts, byte totals and identity digests (`R2_ARCHIVE_MANIFEST.tsv`).
- The 304 line-per-operation move journal and the single blocked operation with its error.
- The disposition of every candidate, including the ones deliberately kept.

## What cannot be verified from this repository

- The archived bytes themselves: databases, receipts, key material and raw round output are not published.
- The external-volume transfer: that is the owner's action.
- The live registry's own view: reading it requires the domain's Shared Spine reader, not GitHub.

## Known gaps the owner must decide on

5 registry-referenced trees now sit on an external volume,
6 have no copy at all, and 1 sits in the
first-round archive on the workspace volume. Repairing the locators is a canonical mutation and was not
performed here.
