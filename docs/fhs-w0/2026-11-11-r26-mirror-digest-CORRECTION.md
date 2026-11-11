# Correction — the r26 mirror digest mismatch is a local checkout artefact, not a repository defect

**Status: finding WITHDRAWN.** The claim in `2026-11-11-r26-mirror-digest.md` on this branch does
not survive re-measurement against the GitHub object store. This file is appended rather than
deleting the original, because the original is what an external reader may already have seen.

## The original claim

> `INTEGRATION/FHS/docs/as-built/W0/r26/SHA256SUMS` pins `GATE_R26.json` at
> `b9e7c2fce27673755418830852bd43aa6fa5c06950c85c46dc09ed57c7c598fc`, but the file at the same
> commit hashes to `231e2ac7e8b096d7aa8975b83605389f7b21320afd2a27687d95c8ac002f58fd`.

## What is actually true (measured 2026-11-11, second pass)

Read through the GitHub contents API — i.e. the blob as stored, not a working tree:

| ref | path | blob sha | bytes | sha256 |
|---|---|---|---|---|
| `a6f1fa897052cb4a3bcba316e774721d3d4fe62b` | `…/W0/r26/GATE_R26.json` | `741d380ff6a8…` | 6438 | `b9e7c2fce27673755418830852bd43aa6fa5c06950c85c46dc09ed57c7c598fc` |
| `main` | `…/W0/r26/GATE_R26.json` | `741d380ff6a8…` | 6438 | `b9e7c2fce27673755418830852bd43aa6fa5c06950c85c46dc09ed57c7c598fc` |

The stored blob **matches** the digest `SHA256SUMS` pins, at the imported commit *and* on `main`.
There is no inventory mismatch in the repository.

## Where `231e2ac7…` came from

From a Windows working tree with `core.autocrlf` in effect. The same path in a local clone:

```
bytes   6649
CRLF    211
sha256  231e2ac7e8b096d7aa8975b83605389f7b21320afd2a27687d95c8ac002f58fd   <- reported
```

Normalising `CRLF -> LF` on that working-tree copy yields exactly the stored blob:

```
bytes   6438          (6649 - 211 = 6438)
sha256  b9e7c2fce27673755418830852bd43aa6fa5c06950c85c46dc09ed57c7c598fc
        == GitHub blob at a6f1fa89 and at main, byte-for-byte identical: True
```

`SHA256SUMS` is an inventory of **git blobs**. A SHA256 taken over a CRLF-expanded working-tree
file is not comparable to it, and the 211-byte delta is exactly the 211 line terminators. The
mismatch was therefore produced by the measuring environment, not by the repository.

## Consequence for the reader

- `INTEGRATION/FHS/docs/as-built/W0/r26/` is internally consistent; the provenance chain
  `SHA256SUMS` -> payload holds on the stored bytes.
- Any consumer verifying that payload on Windows must verify the **blob** (`git cat-file -p <sha>`,
  or the contents API), not the checked-out file, or must disable CRLF conversion for the check
  (`git -c core.autocrlf=false …`, `.gitattributes` `-text`, or `sha256sum` over the LF-normalised
  bytes).
- The test `test_manifest_admission.AdmissionRecordTests.test_payload_directory_untouched` asserts
  this invariant correctly; it was never failing against upstream bytes. Its failure in a local run
  is an artefact of the same CRLF expansion.

## What this correction does not do

It does not touch the payload, `SHA256SUMS`, or any test. It does not ask for a merge. It records
that the original report on this branch is withdrawn, with the measurement that withdraws it, so
that the next reader does not re-open a defect that does not exist.

**Claim ceiling**: `SOURCE_READ` on two refs of one repository plus one host measurement. No native
admission, no release, no acceptance of any subject.
