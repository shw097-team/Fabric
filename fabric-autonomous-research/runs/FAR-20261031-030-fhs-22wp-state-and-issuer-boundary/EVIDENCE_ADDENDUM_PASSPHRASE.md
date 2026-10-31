# Addendum — the passphrase was entered, and the instrument it signed does not contain the 7 PARKED

Written after the owner entered the passphrase (`已輸入口令授權`, 2026-10-31).

## What the passphrase actually produced

| step | result |
|---|---|
| window opened under the task the signer accepts | `WIN-b0b6e958d441`, task `R18-FHS-SKELETON-SPINE-20261029`, 30 ops, expires `1793468960`, serving on `127.0.0.1:4767` |
| delegation signed by the broker | **`R18-CANON-f5ebdd5f`**, `signing_window_id: WIN-b0b6e958d441`, `private_key_exposure: "none: the key stayed in the broker process; the agent only received a signature"` |
| allowlist of the new instrument | `WP-FHS-00, 01, 06, 09, 18, 19, 21` |
| effect classes | `SOURCE_READ`, `REPO_WRITE_TO_CANDIDATE_BRANCH` |
| deny | `RELEASE`, **`HOST_INSTALL`**, `secrets`, `force-push`, `main`, `merge`, `tag` |

So the owner act succeeded and is receipted: a real owner-signed instrument now exists that did not exist an
hour ago, and the private key never left the broker process. It unblocks **7 packages** (2 of them DONE,
5 PARTIAL) — those can be re-driven under it immediately.

## Why the 7 PARKED are still parked

| instrument | allowlist | has HOST_INSTALL? |
|---|---|---|
| `R18-CANON-f5ebdd5f` (signed now) | 00,01,06,09,18,19,21 | **denied** |
| `R19-CANON-2c250b16` (signed earlier, not installed) | 00,01,05,06,07,09,15,16,18,19,21 | **denied** |

`WP-FHS-08, 10, 11, 12, 13, 14, 20` appear in **neither** allowlist, and both instruments deny
`HOST_INSTALL` — which is exactly the effect class those packages need, because their own acceptance
requires a host-side install plus a fresh-load proof (`ACTUAL_INSTALL_FRESH_LOAD_INVOKE` in WP-FHS-17's
clause list; `functional_raw_and_original_reader_ack` in WP-FHS-20's gap file).

The passphrase did not fail. The **scope** of the standing instruments excludes the blocked packages. No
amount of retrying, and no additional passphrase entry, changes that: it is a scope question.

## What I did about it

**Owner then authorised R21 explicitly, and it is now signed and verified:**

| | |
|---|---|
| delegation | `R21-CANON-c0542636` |
| signature verifies locally against the owner public key | **true** |
| signing window | `WIN-b0b6e958d441` (ops_used_after 3) |
| `wp_allowlist` | **08, 10, 11, 12, 13, 14, 20** — exactly the seven PARKED |
| `effect_class_allowlist` | `SOURCE_READ`, `REPO_WRITE_TO_CANDIDATE_BRANCH`, `LOCAL_DRAFT_WRITE`, **`HOST_INSTALL`** |
| still denied | `RELEASE`, `secrets`, `force-push`, `main`, `merge`, `tag` |
| not_after | 2026-11-14 |
| private key exposure | none — the broker signed, the agent received a signature |

It widens exactly two axes and nothing else, and `host_install_boundaries` confines installs to
`var/R21-NATIVE-EXEC/occupants/**` with one PERMIT per package binding wp + occupant sha256 + policy epoch +
registry root + TTL. The draft it was signed from is unchanged at
`governance/delegation_R21_amendment_DRAFT_for_owner.json`.

## State after this addendum

| | before passphrase | after passphrase |
|---|---|---|
| owner-signed instrument covering the parked set | none | still none (allowlist excludes them) |
| owner-signed instrument covering 7 other packages | none (both old windows CLOSED) | **`R18-CANON-f5ebdd5f`** |
| packages the agent may legally drive | 0 under a live instrument | **7** |
| parked packages legally drivable | 0 | 0 |
