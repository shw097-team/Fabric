# Archive handoff (redacted)

**CANDIDATE / LOCAL_ONLY_INDEX.** This describes how to find the archived originals from the local
workspace. It deliberately contains no inventory listing, no absolute paths, no credentials and no
file contents.

## Shape

```text
<archive root>/                  # sibling of the workspace root, same volume
  01_已分類可封存/<original relative path>    # classified, superseded round / scratch material
  02_未分類可外移/<original relative path>    # purpose unknown, proven not a program dependency
  ARCHIVE_MANIFEST_20261110.tsv              # per-tree: class, path, file count, bytes, identity verdict, digest
  RESTORE_NOTES.md                           # reverse-MOVE procedure
  _meta/                                     # inventories, disposition plan, move journal, cleanup journal, tools
```

Every archived tree keeps its **original path relative to the workspace root**, so a restore is a single
`rename` back into place — not a copy, not a re-derivation.

## What an external reader can and cannot verify from here

- Can verify: the manifest's per-tree file counts, byte totals and identity digests; the move journal's
  140 line-per-operation records; the disposition plan's per-item reason.
- Cannot verify: the archived bytes themselves — they are not published (databases, raw round output,
  receipts and work-tree material are deliberately excluded from this repository).
- Cannot verify: external-volume storage. That is a user action outside this round.

## Restoration

Restoration runs in reverse along `MOVE_JOURNAL_20261110.tsv` while the archive is still on the same
volume and the source slot is still empty. A destination that is occupied is a HOLD, never an overwrite.

## Not published, by design

Working-tree databases (`*.db`, WAL/SHM), key material, receipts and owner-ACK payloads, raw lane output,
the full local file listing, and any absolute path that embeds the local workspace layout.
