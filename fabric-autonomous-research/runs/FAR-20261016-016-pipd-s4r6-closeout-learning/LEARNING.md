# Learning

## 1. Inherited verdicts are claims about the machine that produced them

The command薄 shipped `compiler_verdict_here: PROMPT_COMPILE_BLOCKED` with its own explanation —
"本交付環境未取得 compiler references/schema/scripts". That is true of the author's container. Run
against this machine, the same gates pass. A round that treated the field as a product verdict would
have stopped at the preflight and reported a blocker that does not exist. **Rule: before accepting an
inherited blocked/verdict field, look for the same-version tooling locally and run the gate.**

## 2. A bounded repair is bounded by the defect, not by the named line

The report names one line (`--release-id preview.4` paired with a preview.3 commit). Fixing exactly that
line leaves the reader with an example that references a directory which does not exist at any commit —
a failing command instead of a mis-stamped one. The defect is "this example's identity fields are not
one release", so the repair has to cover every field of the example plus the existence of the pack it
names. **Rule: repair the identity invariant, then re-read the whole block as the reader would.**

## 3. Checker independence is a model-axis property

The VERIFY_SECURITY pool's rank-1 was the writer's own model. Dispatching "the VERIFY lane" would have
produced a verdict from the same weights that made the change — a self-check wearing a lane name.
Rank-pinning plus a model pin produced a real second axis, and the receipt now carries required vs
served so a third party can verify that independence without reading the round's prose. **Rule: record
the served arm in the receipt, and treat lane identity as insufficient evidence of SoD.**

## 4. Do not edit a registry to make a measurement come out right

The divergence between the pool and the mandate was resolved at dispatch time, not by rewriting
`lane-route-slots.candidate.json`. A round that edits the registry to align reality with its mandate
destroys the value of the measurement for everyone after it.

## 5. Marker gates should be satisfied, not evaded

The lane's remote-write scan is a substring scan whose marker list contains `publish`, so a read-only
checker brief that merely uses the word "published" is refused. The wrong fix is to reword the brief
around the scanner. The right fix is to state, in the brief, the WorkOrder that actually owns the
publication — which is true and also makes the gate's condition real.

## 6. Measured bytes beat quoted digests

The R6 report explicitly could not download the release bytes ("本輪容器 Internet DNS 不可用") and said so.
This round could, and recomputed the digest from the served bytes. The upgrade from *quoted* to
*measured* is the whole value of the exercise: the same number, but now falsifiable by anyone.

## 7. Serving bytes can carry older provenance than the tag

The served Web-fallback document's own header declares `v0.1.1-preview.3`, and it is a preview.4 asset
whose digest matches the repo copy — so this is not transport damage, it is a projection that was
generated from the previous release and published under the new one. Nothing in the release metadata
records this. **Rule: for a release, verify the content's self-declared identity as well as its hash.**

## 8. Local counts are not CI counts

621/20 locally vs 624/6 on the CI runner. Same suite, different environment and skip set. Presenting the
local number as a reproduction of the CI number would be a false provenance claim in the direction of
*more* evidence, which is the easiest kind to get away with and the most damaging when found.

## 9. A check that cannot fail is not evidence

The round's detector carries a paired mutation for every check (7/7 fired). Without the pairing, a
detector that only ever prints PASS is indistinguishable from a detector that reads nothing.

## 10. The immutable-release constraint propagates

Finding 7 above cannot be repaired in place: the document is one of seven frozen assets. The only legal
repair is at the next release. Discoveries about an immutable artefact become inputs to the *next*
release, never edits to the current one.
