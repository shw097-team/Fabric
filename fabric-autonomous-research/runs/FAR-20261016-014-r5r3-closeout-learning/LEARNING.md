# Learning

1. **Prove the artefact before you debug the host.** A host refusal looks like a packaging problem and pulls
   you toward manifest archaeology. Rebuilding the artifact from its own recorded commit took minutes and
   deleted an entire cause class (nondeterminism). Do that first; it is cheaper than any hypothesis.
2. **A refusal with no error code needs a DISCRIMINATING experiment, not a better hypothesis.** The planned
   experiment is: send the package the host previously accepted. If that is refused too, the conclusion is
   about the account, and no amount of local work can change it. Design the experiment so both outcomes are
   informative.
3. **An innocuous word can refuse a lane.** The remote-write marker check is a substring scan, so "published"
   matches the marker "publish" and the lane never starts. Pre-scan the brief against every marker before
   dispatch; treat the refusal as a brief-editing task.
4. **A ticket's claimed defect may not exist any more — and "does not reproduce" is a different disposition
   from "was fixed".** Measure both surfaces, then say which conclusion the evidence supports and which it
   does not.
5. **A byte-level diff is strongest when used to DELETE hypotheses.** Showing that two packages are
   identical except for two provenance members removed two candidate causes and pointed at a third.
6. **Put the new measured fact where the repo already keeps that kind of fact.** A reproducibility receipt
   belongs beside the asset readback the release already ships, so the next reader finds it without trusting
   a maker sidecar — and it stays inside the write-set allowlist.
7. **State the SoD residual the moment the owner pins writer and checker to one model.** Independence then
   rests on process, lane, fresh context and re-derivation; claiming model-level separation would be false.
