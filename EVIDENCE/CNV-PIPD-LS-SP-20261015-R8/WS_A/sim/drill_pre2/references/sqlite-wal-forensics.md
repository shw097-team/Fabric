# SQLite WAL forensics (claim-safe checks, in order)

Run these in order and let each one bound what you may claim. A single "the WAL is corrupt" statement
is almost always wrong in one direction or the other, and an adversarial checker will contradict it.

## 1. Header

WAL header is 32 bytes. Read the first 4 bytes and interpret them **big-endian**:

| bytes (hex) | big-endian | meaning |
|---|---|---|
| `37 7f 06 82` | `0x377f0682` | valid WAL magic, little-endian checksums |
| `37 7f 06 83` | `0x377f0683` | valid WAL magic, big-endian checksums |
| anything else | — | not a WAL header |

`00 00 10 00` at bytes 8–11 is the page size (big-endian), typically 4096.

A **valid magic does NOT mean the file is usable** — and an invalid one licenses only "this file is not
a WAL header", never "this file is not a WAL".

## 2. Frame alignment

Frame size = `24 + page_size`; the file is `32 + n * frame_size`:

```
(size - 32) mod (24 + page_size) == 0   ->  whole frames, aligned
else                                   ->  truncated mid-frame (tail is a partial frame)
```

Worked example: size 8,321,499, page 4096 → frame 4120 → `(8321499-32)/4120 = 2019.77` → 2019 whole
frames + 3,187-byte remainder ⇒ **truncated tail**. Report it that way; "the WAL is truncated" alone is
incomplete but not false.

## 3. Checksum chain

WAL frame checksums **chain**: each frame's checksum is seeded from the previous frame's (frame 1 from
the header's). So the first frame that fails salts/checksum ends verification — everything after it is
unverifiable *even though the bytes are present*.

Report the result as a prefix, not a verdict:

- "frames 1..N valid, first failure at frame M" ⇒ there is a **salvageable committed prefix** (N frames,
  N × page_size bytes of page images); only *whole-file replay* is off the table.
- The frame header carries the page number, the db-size-after-commit and the salt, so you can name the
  commit frames (frames whose db-size field is non-zero).

Never write "no replay" as a blanket claim: it contradicts a verified prefix and is a finding.

## 4. The sibling artifacts

Check the whole family before characterising any one member: the live WAL, the forensic copy, the
zero-byte sibling, and the main database's own `PRAGMA quick_check` (read-only:
`file:/abs/path?mode=ro`, plus `&immutable=1` for static copies). A copy whose `quick_check` is
`malformed` falsifies any record claiming that artifact is intact — and "same size, different hash" is
the cleanest way to say the record's bound artifact cannot be reproduced.

## 5. Reconciling a rescue export against the live store

The export gives you the *only* trustworthy "existed then" evidence:

- Every id in the export that is absent from the live store is **proven** loss (present-then-absent).
- An id gap in the live store that never appeared in the export is a **candidate**: the row may never
  have been assigned or may not have been committed. Do not count these as loss.
- An estimate from the original incident record that you cannot reproduce stays **unverified** — say so
  instead of "disproved", because the export's coverage ends somewhere and later writes were never in it.
- Always state the export's coverage bound (lowest/highest id and timestamp) next to the numbers.

## 6. Shelf-life of the claim

A salvageable prefix is a claim about *what data exists*, not about *what the application will accept*.
If the deliverable is "recover rows from the prefix", the artifact is a **controlled salvage attempt on
a copy** (original untouched, digest unchanged, result recorded), never an assertion that the file is
unusable or that recovery is guaranteed.
