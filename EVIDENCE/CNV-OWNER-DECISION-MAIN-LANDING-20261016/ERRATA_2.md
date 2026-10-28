# Errata — CNV-OWNER-DECISION-MAIN-LANDING-20261016

- ER-2-1 (the round's most expensive finding): `--require-arm` means *must be actually served*, not *prefer*.
  Both of this round's first two GPT dispatches were admitted by the gate and then served by the pool's rank-1
  arm, which made them `ok:false` with `ERR_REQUIRED_ARM_NOT_SERVED` and exit 3. The correct invocation pins the
  rank as well: `--force-rank 2 --require-arm openai-codex/gpt-6.1-sol` with the pool named explicitly. With the
  rank pinned, both lanes served the mandated model (`required_arm == served_arm == openai-codex/gpt-6.1-sol`).
  The reusable evidence is the earlier round `var/far-ao-independence-20261010` (E9b for the pinned form, E10c
  for the unpinned failure) and its note that `--no-identity-gate` also silently disables `--require-arm`.
- ER-2-2: a read-only lane cannot write its own output file, and this round's PLAN and VERIFY lanes are read-only
  by role default. Both verdicts were therefore transcribed from the lanes' stdout with the stream hash as
  provenance. A reader should treat the transcription as mechanical and the stdout as the original.
- ER-2-3: the OpenSpec validation failed twice for the same reason as the previous round: a login shell handed an
  MSYS-style path cannot `cd`, so the validator never ran although the receipt looked like a plain failure. The
  native path form works; both attempts are recorded in `SURFACES_RECEIPT.json`.
- ER-2-4: the round's own PLAN lane reported that it missed the required first-message nonce. Its notes are
  published anyway, with the miss recorded, because suppressing a finding to tidy the record is worse.
- ER-2-5: a local lane attempt log (not published) and the scanner source inside PR #15 both contain
  credential-shaped strings: the scanner's synthetic positive-control fixtures. The independent checker treats
  that as a finding on the publication of the scanner, and that finding is why the merges are held.
