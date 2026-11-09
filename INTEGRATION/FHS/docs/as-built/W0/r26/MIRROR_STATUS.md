# MIRROR_STATUS — W0 r26 candidate

This directory is a **candidate mirror**, not a registered artefact.

- `INTEGRATION/MANIFEST.json` is **not** modified. Registering a path there is a Fabric policy act, and this
  round's entry contract gives it to Fabric's own reader (EC-R24-008 stays open here).
- Asserted: these are the bytes measured in round `FHS_W0_R13_ACCEPTANCE_20261108` at r26, and `PROVENANCE.json`
  describes exactly the files beside it, including the entry set it intends to cover.
- Not asserted: that Fabric's policy layer has accepted, loaded or served this.
- `FHS_ORIGINAL_ACK 6/6` is the lane-qualified label (chapter 17, corrected in 23/24, extended in 25). It is not
  a traditional per-domain acknowledgement (`HIST-01`, `NOT_APPLICABLE_BY_DESIGN`) and not a release grant.
