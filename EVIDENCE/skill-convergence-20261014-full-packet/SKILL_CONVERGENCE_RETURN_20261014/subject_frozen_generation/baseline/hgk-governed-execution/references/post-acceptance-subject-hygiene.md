# Post-acceptance subject hygiene: re-freeze, historical baseline, byte-restoration pitfalls

Verified 2026-08-13 FAR activation + TRI_SOURCE rounds. The AO lane (A11 class) caught a
real governance violation and the re-freeze resolution became the validated pattern.

## The violation scenario

After an external reviewer signs an evidence MD (e.g. `58de0815…`, 76,214 B), a later
operability round (docs + NBO cleanups + activation receipt) REGENERATED that same
canonical file (`58de0815…` → `eff79b73…`) while README/TEAM/AGENTS/receipts still cited
`58de0815…`. The AO lane's immutable-hash check (`sha256sum` artifact vs every documented
reference; verify claimed mirror count) flags this as A11 FAIL. The external verdict itself
is a governance RECORD (report file) and stays immutable — but the evidence MD is a
per-subject wrapper and must not be mutated after signing.

Rule: **post-acceptance rounds NEVER modify the signed evidence MD at its canonical path.**
New bytes = new post-acceptance subject (TRI_SOURCE prompt §1 semantics).

## Resolution: re-freeze (option B the AO explicitly allows)

`restore byte-identical copies OR re-freeze + update all hash references`. Re-freeze is the
reliable path (byte-identical restoration is usually impractical — see below):

1. **Archive the current bytes first**: `cp FAR_FINAL_ACCEPTANCE_EVIDENCE.md FAR_FINAL_ACCEPTANCE_EVIDENCE_<stage>_<hash8>.md`
   before touching anything.
2. **Regenerate the canonical** evidence MD from the CURRENT generator state (all artifacts,
   current bytes, dynamic timestamp). New hash X.
3. **Mirror X ×4** (Fabric root + HGK/Fabric/SQS `evidence\review\`); verify unique-hash count == 1.
4. **Sweep ALL hash references**: `sed -i 's/<old>/<new>/g'` across README.md, AGENTS.md,
   TEAM.md, FAR_ACTIVATION_RECEIPT.json, R8 baseline doc — both the abbreviated
   (`58de0815…`) and full 64-hex forms (receipts often carry the full hash; a short-form sed
   misses it). Verify: `grep -c '<new>' <each file>` > 0 and `grep -c '<old>' <each file>` == 0.
5. **Write a historical-baseline record** (`FAR_R8_HISTORICAL_BASELINE.md`-style doc):
   table of the supersession chain (verdict → stage → evidence hash → what changed), the
   immutable r8 verdict hash, and the rules (verdict immutable; MD = per-subject wrapper;
   canonical current = X). This doc prevents "old acceptance pretending to cover new bytes".
6. **Register a superseding EVD** (`EVD-FAR-ACCEPTANCE-MD-R<N+1>` = X; never re-register the
   old id — UNIQUE on evidence_id).

## Byte-exact restoration is a trap — know when to abandon

Attempting to regenerate a signed MD to its exact old hash fails when:
- The generator embeds a **dynamic timestamp** (`NOW = datetime.now(...).strftime(...)` in the
  header). Brute-forcing 60 seconds over even two minute-ranges does not converge when OTHER
  embedded artifacts also changed.
- **Embedded source files evolved** (manifest entries re-generated, receipts edited,
  new files added): the old bytes depend on a whole file-state snapshot, not one field.
- The manifest entry hashes encode historical file states (e.g. a test-stdout file that was
  later regenerated) — reproducing requires reverting those files too.

Detection: after reverting generator state (heading, semantics strings, exclusion lists),
if the hash/byte count still differ by a small residual (e.g. 25 B) and brute-force over the
timestamp range fails → STOP. Do not chase the remaining bytes; switch to re-freeze and
document the old hash as the historical baseline.

## Freeze-loop and how to end it

When the acceptance MD EMBEDS the evidence-manifest entries (external reviewers required it),
every artifact change forces: manifest regen → MD regen → mirror → hash-ref sweep → EVD churn.
The loop is inherent to embedded-manifest design. Ending it:
- The manifest generator must EXCLUDE itself and the acceptance MD (pre-self-row; otherwise
  MD-embeds-own-hash drift).
- Scope rules: manifest covers FAR-root receipts + evidence-bundle; `tests/` and `canary/`
  dirs are OUT of scope — to get a canary into the manifest, COPY its artifacts into
  `evidence-bundle/raw-canary/<run>/` (A14 class finding).
- Treat the final regeneration as THE freeze: make all changes, regenerate once, mirror,
  hash, then STOP. Any AO lane that ran against the prior hash is documented as
  post-capture (the pattern is accepted when the delta is mechanical and recorded).

## Checklist for the re-freeze sweep

```text
[ ] archive current canonical bytes (stage-named copy)
[ ] regenerate canonical MD (current generator state) -> hash X
[ ] mirror X to 3 roots + Fabric root; unique sha count == 1
[ ] sed short-form + full-form hash in README/AGENTS/TEAM/activation receipt/R8 baseline
[ ] grep old hash == 0 across those files
[ ] FAR_R8_HISTORICAL_BASELINE.md (supersession chain table + rules)
[ ] EVD-FAR-ACCEPTANCE-MD-R<N+1> (superseding; keep old rows)
[ ] record post-capture AO verification if a lane ran on the prior hash
```
