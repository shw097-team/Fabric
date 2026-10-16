# Post-publication addendum — binding the readback

This file exists because a receipt that describes a commit cannot live inside the commit it describes.
The packet's first commit (`e13cd1846f521ed778ff9dbc694cbdbea3f6d0da`) carries the candidate evidence and
`PACK_INDEX.json`; this additive follow-up commit carries the receipts that describe **that** commit:

| file | what it binds |
|---|---|
| `PUBLISH_RECEIPT.json` | the branch/commit/PR actually created, with the credential's scope probe result and `token_value_exported: false` |
| `REMOTE_READBACK_VERIFY.json` | the remote re-hash of every committed blob against `PACK_INDEX.json`, the `main`-unchanged assertion and the PR state |
| `SELF_CHECK_RECEIPT.json` | the round's self-check with S12 (publication readback) now evaluated rather than `NOT_RUN` |
| `POST_PUBLICATION_ADDENDUM.md` | this file |

Provenance rule being applied: the round's claim about a GitHub commit is bound to what the remote
serves, not to the local working copy. `PACK_INDEX.json` carries the byte length and SHA-256 of every
other file; this addendum and the three receipts above are deliberately NOT in that index, because they
could not have existed when the indexed commit was created.

Claim ceiling is unchanged by this commit: `CANDIDATE_EVIDENCE_ARCHIVED_ONLY`. No pull request is
merged; `main` is untouched; the validator, the checker isolation, the runtime re-certification and
production all remain open exactly as the first commit states.
