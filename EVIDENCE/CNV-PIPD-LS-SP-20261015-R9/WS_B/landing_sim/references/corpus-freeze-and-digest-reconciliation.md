# Corpus source-freeze, denominator proof and digest reconciliation

Verified on a governed pre-construction round: a 724-file / ~306 MB corpus across a nested
`P0/ PI-PKG/ PD-PKG/ <RUNBOOK>/` tree, with a 34-package decision denominator and a frozen
author-side digest to reconcile.

## When to use
- An order demands **full physical read / no sampling** of a source corpus root, a
  deterministic inventory digest, current-vs-superseded resolution, and proof of a decision
  denominator (e.g. `PI-PKG-00..17 + PD-PKG-00..15 = 34/34`).
- A frozen author-side digest does **not** reproduce from the current tree and you must decide
  whether that is content drift, stale ledger, or layout drift.
- You must show a ledgered row round-trips to its exact source line.

## Procedure

1. **Count before you read.** `find <root> -type f | wc -l` and `du -sh <root>`. A corpus root
   that holds hundreds of files will not match a document's "flat snapshot" file count — check
   the tree shape (`find <root> -type d`) before concluding anything is missing.
2. **Hash with the frozen algorithm, not a convenient one.** Publish TWO hashes per source:
   - `raw_bytes_sha256 = SHA256(exact bytes)` — the only value legitimate for byte-level
     packaging/readback.
   - `normalized_text_lf_sha256`, computed only for UTF-8 / UTF-8-BOM decodable text: strip BOM,
     `CRLF → LF`, lone `CR → LF`, change nothing else (final-newline state included), encode
     UTF-8 no-BOM, then SHA-256.
   Rule of use: raw differs but normalized matches ⇒ byte-drift / text-equivalent; normalized
   differs ⇒ content drift.
3. **Build the deterministic inventory digest.** One canonical row per source:
   `relative_path<TAB>raw_bytes_sha256<TAB>size_bytes<TAB>logical_lines\n` with `/` separators
   and case preserved, rows sorted by **ordinal UTF-8 byte order of `relative_path`**, then
   serialized UTF-8 no-BOM and SHA-256'd. Pin the decision-corpus digest with the same algorithm
   but the denominator fixed to the current decision subjects only — that is the value
   downstream ledgers are keyed to.
4. **Handle long Windows paths.** Corpus filenames here run past 260 chars. `os.walk` lists them
   fine, but `open()` raises `FileNotFoundError` — which reads exactly like "file absent" and
   sends you hunting for a missing source. Use an extended-length opener for every read:
   ```python
   def xopen(path, mode="rb"):
       p = os.path.abspath(path).replace("/", "\\")
       if not p.startswith("\\\\?\\"):
           p = "\\\\?\\" + p
       return open(p, mode)
   ```
   (Also pass forward-slash native paths like `C:/...` to external binaries; MSYS does not
   translate paths for native programs.)
   A `pathlib.rglob()` / `is_file()` walk silently **DROPS** these files too (observed 723 vs
   `os.walk` 724 on the same tree), and a bare `except OSError: pass` around `getsize` then
   shortens the byte total — producing a phantom "source drift" whose unexplained delta EXACTLY
   equals the dropped file's size and whose file count is short by exactly one. That exactness is
   the tell that the EXTRACTOR is wrong, not the corpus: re-walk with `os.walk` + `xopen` and
   confirm the per-file hash before declaring drift or triggering a re-freeze. Corollary: inspect
   a receipt's ACTUAL key names before reporting a gap — probes built on guessed keys (`write_set`
   vs `proposed_bounded_write_set`, `gates` vs `active_gates`, top-level vs nested `corpus`)
   report false failures and can send you chasing a defect that does not exist.
5. **Resolve the denominator explicitly.** Match decision subjects by pattern against the
   package-body files at their documented level — direct children of the package directories,
   not the `DOC/` or blueprint subtrees, or you inflate the count. Assert exactly one current
   body per canonical id and list any missing/duplicate id as a bounded blocker.
6. **Reconcile a frozen digest before calling drift.** If the frozen value does not reproduce:
   FIRST recompute using the **author's own recorded names** (documents often froze a flat-root
   snapshot with auto-suffixed duplicates like `name(2).md`, while the live tree is nested and
   unsuffixed). If the frozen digest reproduces byte-exactly under the author-side names while
   every per-file raw hash also matches, the verdict is `PATH_LAYOUT_DRIFT_BODIES_IDENTICAL` — a
   layout artifact, not content drift. Reproducing the frozen value is what converts "mismatch"
   into a reconciled finding; a mismatch alone is not evidence of a stale corpus.
7. **Locator round-trip against the ledger, not against a regex.** A ledger of normalised family
   tokens will NOT be found literally in source: `D03-WF-01` and `PI17-D07-WF-001` normalise to
   `WF-01` / `WF-001`. So do not search the body for the ledger token. Instead:
   - take the row's own `source_locator` (`<file>:L<n>`);
   - resolve the file (normalise `(1)/(2)/(3)` suffixes before comparing basenames) and read
     line `n`;
   - assert the **FULL** ledger token at that line with a boundary that excludes alphanumerics
     but **permits a preceding `-`** (required, because the source form carries a hyphenated
     owner prefix): `(?<![A-Za-z0-9])TOKEN(?![A-Za-z0-9])`.
   Asserting only a suffix (`01`, `000`, `A`) has no discriminating power — short suffixes occur
   on thousands of unrelated lines.
8. **Emit the receipt** with: mode, counts (files/bytes/logical lines/decodable), both digests,
   denominator with the reconciliation verdict, supersession class counts, ledger digests,
   quarantine counts, and every unavailable external registry as an explicit
   `TEMP_CLOSED_REGISTRY_ROW` bound-blocker with its close evidence.

## Pitfalls (rule + mechanism)

- **Sort paths by encoded bytes, not by Python `str`.** `sorted()` on `str` compares code points
  and is NOT ordinal-UTF-8-byte order for non-ASCII paths — with CJK directory names the digest
  silently differs from a spec that says "ordinal UTF-8 byte order". Use
  `key=lambda r: r.split("\t", 1)[0].encode("utf-8")`.
- **A ledger TSV digest reproduces only under one exact serialization.** Find it empirically
  (this stack: non-empty lines joined with `\n` and **no trailing newline**, UTF-8) rather than
  assuming a trailing newline or the fenced block as-is; a wrong serialization looks like a
  wrong digest and invites a false "ledger tampered" claim.
- **Never fabricate a row to close a denominator.** When an external registry body is not
  mounted, preserve the range carrier and mark the exact row body `TEMP_CLOSED_REGISTRY_ROW`
  with close evidence. A denominator closed by invented rows is the failure the gate exists to
  catch.
- **A per-package denominator that reproduces for most packages but not all is usually the
  documented carrier convention, not a defect** — check the ledger's own contract note for
  explicit carrier rows above the source-ID count before reporting a mismatch.
- **Classify supersession by tree position, not by filename guessing.** Blueprint/`藍圖`
  subtrees are provenance-only; only the documented current level admits positive normative
  authority. Counting a `藍圖` copy as current inflates both the denominator and the claim.
