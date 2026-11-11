# r26 mirror inventory does not match the bytes it lists (2026-11-11)

**Documentation-only report. No payload, inventory or policy is changed by this branch.**
**Claim ceiling: `SOURCE_READ` — two files hashed at `main`, one test named. Not an acceptance,
not a governance finding about intent, not a release.**

## 1. Measured

At `main` (`a6f1fa897052cb4a3bcba316e774721d3d4fe62b`), in
`INTEGRATION/FHS/docs/as-built/W0/r26/`:

| file | sha256 |
|---|---|
| `GATE_R26.json` (actual bytes) | `231e2ac7e8b096d7aa8975b83605389f7b21320afd2a27687d95c8ac002f58fd` |
| `GATE_R26.json` as pinned by `SHA256SUMS` | `b9e7c2fce27673755418830852bd43aa6fa5c06950c85c46dc09ed57c7c598fc` |

```
$ sha256sum INTEGRATION/FHS/docs/as-built/W0/r26/GATE_R26.json
231e2ac7…58fd
$ grep GATE_R26 INTEGRATION/FHS/docs/as-built/W0/r26/SHA256SUMS
b9e7c2fc…98fc  GATE_R26.json
```

## 2. Why it matters

The entry's own admission test asserts this equality:

```
$ python -m unittest discover -s INTEGRATION/FHS/tests
FAIL: test_payload_directory_untouched (test_manifest_admission.AdmissionRecordTests)
AssertionError: '231e2ac7…58fd' != 'b9e7c2fc…98fc' : GATE_R26.json
Ran 51 tests — FAILED (failures=1)
```

`test_payload_directory_untouched` is not a stylistic check: it is the assertion that the published
as-built payload "gained no file and lost no byte" (its own docstring). Against the published bytes
it fails, so a reader who runs the entry's tests on a clean clone gets a red result that has nothing
to do with their own changes.

## 3. What this branch does not claim

- It does not claim which of the two digests is the intended one, nor that the payload was tampered
  with. A stale `SHA256SUMS` after a later rewrite and a rewritten payload after a correct `SUMS`
  look identical from here.
- It does not touch `GATE_R26.json`, `SHA256SUMS`, `MANIFEST.json` or any test.
- It does not re-derive the inventory: doing so would assert a new state for a r26 record, which is
  the mirror owner's decision, not a documentation change.

## 4. What the owner may want to decide

1. Re-derive `SHA256SUMS` for the r26 payload (if the current `GATE_R26.json` is the intended one), or
2. restore the byte the inventory pins (if the inventory is the authority), and
3. state which of the two is the immutable record for r26, so a later reader does not have to guess.

## 5. How to reproduce

```bash
git checkout a6f1fa897052cb4a3bcba316e774721d3d4fe62b
cd INTEGRATION/FHS/docs/as-built/W0/r26
sha256sum GATE_R26.json      # 231e2ac7…
grep GATE_R26 SHA256SUMS     # b9e7c2fc…
cd - && python -m unittest discover -s INTEGRATION/FHS/tests   # 1 failure, this one
```

Reproduced on Windows, Python 3.11.9, in an FHS_NEXT W0 workspace that imports this repository's
files byte-identically (`source_sha256 == target_sha256`, 0 mismatches) and deliberately does **not**
import the `docs/as-built/**` payload as source.
