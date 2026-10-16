# Errata and disclosures — CNV-HYGIENE-README-CLOSURE-20261016

- ER-H1: the round's own driver (the one that was meant to open the four orchestration surfaces in one pass) hung
  with a zero-byte log; it was killed and the surfaces were driven again with a bound on every call. The board's
  cards and the SWARM graph come from the second, bounded run. Recorded because a hung driver that leaves no
  output is exactly the failure a receipt is supposed to make visible.
- ER-H2: quite separately from ER-H1, this round found that the round's earlier claimed card set could not be
  trusted until re-read, because a killed driver may have completed some calls and not others. The board was
  therefore read back through the CLI rather than assumed.
- ER-H3: `str(Path)` yields a backslashed path, which bash refuses; the OpenSpec validation silently did not run
  until the path was passed in forward-slash form. The validator then reported the change valid.
- ER-H4: the verifier lane reported that it could not write its own verdict file because the read-only sandbox
  withholds write authority. Its finding set therefore lives in the lane's stdout and was transcribed into
  VERDICT.md with the stdout hash as provenance. The transcription is mechanical.
- ER-H5: the change `hgk-cnv-hygiene-readme-closure` carries two spec deltas, because the hung driver had already
  written one before it hung. Both validate strictly; the duplication is cosmetic and is left rather than
  rewritten, since rewriting a record to look tidier is not this round's business.
- ER-H6: large single-file writes from this session were truncated in flight by the context layer. Every script
  of this round was therefore split into small files; the first attempt exists in the round history as evidence.
- ER-H7: PR #16 (this round's pack) is deliberately NOT merged by the round. The homepage is the repository's
  most externally visible surface and the one that states what is and is not accepted, so publishing it to the
  default branch is left to the owner.
