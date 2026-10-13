# ERRATA — WO-FABRIC-REPO-ASSESS-20261013

Independent checker: sealed-lane arm refused by the route registry, so the owner-mandated
`opencode-go/glm-5.3-flash` checker was run provider-direct through the same Codex CLI against the
same relay. Verdict **PARTIAL**, model diversity declared true (three distinct models this round).

- **F1 (HIGH) — accepted.** The refusal of a wholesale "COMPLETE update" is a **scope rejection**, not
  a closure of the owner requirement. The requirement (an external engineer can plan a complete
  upgrade from what the repository shows) needs a current, explainable source→projection relationship
  plus the readiness artifacts (approved upgrade scope, dependencies, contracts, validation, rollback,
  non-claims). None of those exists today, so that requirement stays **OPEN**, and this round cannot
  claim it is served.
- **F2 (MEDIUM) — accepted.** "Published ad hoc" is downgraded to the measured fact: no builder was
  found **inside the four trees searched**, so the publication method is unlocated through the searched
  scope. "Ad hoc" is an inference requiring the publication records or an external method artifact.
- **F3 (MEDIUM) — accepted, with the nuance recorded.** The measured numbers are consistent, but
  `extension_mix` records `.gitignore` blobs **inside** the payload while no root `.gitignore` exists;
  the finding is therefore "no root publish-control file", not "no .gitignore anywhere".
- Findings beyond F3 were not fully transcribed before this round's budget closed; they remain
  **carry-forward** and are listed as such below rather than silently dropped.

## Carry-forward (not resolved here)
- Completion of the checker's remaining findings (F4+) and their corrections.
- A reproducible publication procedure for the mirror.
- The declared-exclusion contradiction (`var/` declared excluded, the desktop runtime folder published).
- Manifest refresh, external-engineer documentation, LICENSE, large-binary disposition, remote linking.
- Adding the mandated checker arm to the VERIFY_SECURITY pool (route-registry change is an owner decision).
