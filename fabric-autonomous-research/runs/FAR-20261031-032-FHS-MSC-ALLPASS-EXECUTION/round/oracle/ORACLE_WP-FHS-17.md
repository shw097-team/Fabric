# WP-FHS-17 acceptance oracle — bounded occupant install chain

Registered before this round's officer sitting. Transcribed from the work package's own requirement
(`REQ/R18-WP-FHS-17`, delivery `11_WORKPACKAGES_AND_DAG.md`) and from `EVIDENCE_GAP.md` in the same tree.
The maker supplies the subject; the officer derives its claims from this file.

## What PASS requires

1. **A signed grant is accepted by the receiver's own gate.** A grant issued by the original Issuer for
   `operation=install_occupant` over this package, with a nonce that is unspent, within TTL, matching the
   WriteSet, the candidate digest and an admission record whose subject/operation/candidate all match.
   A grant minted by a "conformance seam" inside the tool does not count.
2. **The exact WriteSet is applied.** The declared paths are created and nothing else is; an existing path where
   the WriteSet says `preimage=ABSENT` refuses rather than overwrites.
3. **A fresh process loads the occupant from its resolved origin.** `LoadedSHA` equals the pinned candidate
   bytes, and the load happens in a process that did not perform the install.
4. **The needed feature is invoked with real input** and its output is validated.
5. **The original consumer acknowledges the output.** A self-report by the receiver is not an ack.
6. **Every negative refuses for the reason under test.** A refusal whose code is `ROOT_ABSENT`,
   `ERR_NONCE_REPLAY` or `ERR_GRANT_MISSING` where a preimage / traversal / regrant / alias code was expected
   does NOT discharge the clause — that is a check that never happened.

## What PASS does not mean

This tree is a **bounded WP-local receiver**, not the original Host Installer / Loader / Registry. A PASS here is
`EXECUTED_BOUNDED_LOCAL` and is **not** native admission, canonical acceptance, promotion or release.
`EVIDENCE_GAP.md` names that gap and it stays open.

## Falsifiers

- any of the six clauses above failing, or
- the run being unable to execute in the original tree (a checker that cannot run the subject cannot pass it), or
- the summary reading a receipt this run did not write.
