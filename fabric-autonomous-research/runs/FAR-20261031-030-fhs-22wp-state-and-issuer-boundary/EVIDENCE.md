# FAR round 030 — the 22-package terminal state, and the authority act this repo refuses to let an agent take

| | |
|---|---|
| schema | `FAR-ROUND-REPORT/1` |
| round | `FAR-20261031-030-fhs-22wp-state-and-issuer-boundary` |
| control plane | HG-KSEOS (authority / state / acceptance) |
| governance contract | Fabric (`contracts/`, `assurance/`, `control/`) |
| product entry | SBL / FHS-MSC HANDOFF-PATCH-v1 |
| claim ceiling | **MEASURED_LOCAL** — state read from the round's own terminal-state receipt; no acceptance claimed |

## 1. The answer in one paragraph

Twenty-two work packages exist and every one of them is *defensible* — each has a named owner and a
next legal action — but "defensible" is not "pass", and the round's own receipt says so:
**2 DONE, 12 PARTIAL, 7 PARKED, 1 HOLD**, `defensible: 22/22`, `stop_condition_met: true`. The 12 PARTIAL
are lane work that can still be advanced. The 7 PARKED (WP-FHS-08/10/11/12/13/14/20) share exactly one
owner, *"Bound-artifact original owner + HG-KSEOS Issuer"*, and exactly one missing artefact: an **Issuer
PERMIT**. That permit cannot be produced by the agent, and this round measured *why* rather than assuming
it: the owner window opened for this task (`WIN-ff4cbf45c86e`, 40 ops, ceiling `REPOSITORY_WRITE`) is
refused by the delegation signer with `ERR_WINDOW_FOR_OTHER_TASK`, because the existing delegations are
bound to two earlier windows that are now CLOSED (`WIN-796b69117680`, `WIN-254a1c9fbe72`). Re-issuing the
delegation against a new window **is** the owner act. Doing it myself would collapse the separation the
system exists to enforce, so this round opens the window, proves the boundary, and stops there — it does
not mint authority it does not have, and it does not paint 7 PARKED packages green.

## 2. State measured this round

Source: `var/R18-FHS-SKELETON-SPINE-20261029/receipts/TERMINAL_STATE.json` (schema-carrying, 22 rows).

| status | count | packages |
|---|---|---|
| DONE | 2 | WP-FHS-00, WP-FHS-01 |
| PARTIAL | 12 | 02, 03, 04, 06, 07, 09, 15, 16, 17, 18, 19, 21 |
| PARKED | 7 | **08, 10, 11, 12, 13, 14, 20** |
| HOLD | 1 | 05 (PIPD Writer) |

The 7 PARKED share one owner string and one missing artefact (Issuer PERMIT). The HOLD (WP-FHS-05) is
owned by the PIPD Writer and is not this lane's to close.

## 3. What this round actually executed (all measured, all pushed)

| action | result | evidence |
|---|---|---|
| Goal anchored for the session | `GOAL_SET session=20261031_095700_174429 max_turns=400` | `set_goal.py show` |
| Owner pre-authorisation envelope **opened at task start** (as instructed) | `WIN-ff4cbf45c86e`, 40 ops, scope `permit_sign, admission_bundle_sign, registry_row_sign, merkle_root_sign`, ceiling `REPOSITORY_WRITE`, prompt source `tkinter` | `var/B1-PIPD-PKG-20261027/artifacts/OWNER_WINDOW.json` |
| Issuer key material | `NOT_REQUIRED_DPAPI_BOUND`, key_id `135455ca00280c39` — no passphrase prompt is needed for the key itself | `config/issuer/OWNER_AUTHORIZATION.json` |
| Transport | `RELAY_OK`, health 200, zero visible windows | `relay_daemon.py status` |
| Lane round (EXECUTE + VERIFY) with `console_window_events_delta` | `ROUND_MAY_CLOSE`, problems `[]` | `round_close_gate --round FAR-029` |
| Delegation signer under the new window | **refused**: `ERR_WINDOW_FOR_OTHER_TASK` (window task `FHS-MSC-ALLPASS-CONT-20261031`) | `tools/canonical_sign_delegation.py` output |
| Existing delegation bindings | `WIN-796b69117680` (R18), `WIN-254a1c9fbe72` (R19) — both CLOSED | `governance/delegation_*.json`, `WINDOW_R19_STATUS_BEFORE_CLOSE.json` |

## 4. Findings

| id | finding | evidence | class |
|---|---|---|---|
| **G-1** | 22/22 are defensible but only 2 are DONE; "defensible" ≠ pass and the receipt says so | `TERMINAL_STATE.json` summary | state |
| **G-2** | The 7 PARKED are gated on an Issuer PERMIT, not on more engineering | owner field identical across all 7 | authority |
| **G-3** | The permit chain is: owner window → **delegation bound to that window** → 3 signed kinds (`source_freeze`, `task_kind`, `oracle_ratification`) + `lease_generation` → `NativeAdmission(registry).authorize` → PERMIT | R18 `RESUME_HERE.md`; `native_admission.py:25` | mechanism |
| **G-4** | The signer refuses a window whose task does not match the delegation (`ERR_WINDOW_FOR_OTHER_TASK`), by design | measured refusal this round | boundary |
| **G-5** | Re-issuing the delegation is an owner act; an agent that does it for itself converts owner authority into agent authority | `f0_trace.py` forbids `issue_permit` in a consumer; the delegation JSON carries the owner's window id | boundary |
| **G-6** | No PERMIT producer exists in any live tree; matches only in scratch copies of `sbl_harness` | repo-wide search, 7 hits, all under `var/.../scratch/` | boundary |

## 5. Ruling

1. **Do not fabricate the PERMIT and do not relabel PARKED as PASS.** The user's standing rule ("no
   changed criterion, no UNKNOWN in place of FAIL") applies exactly here.
2. **Leave the window OPEN** (40 ops, 8 h) so the owner's next act costs one command, not a session.
3. **Advance the 12 PARTIAL under the lanes**, because they are gated on evidence, not on authority.
4. **WP-FHS-05 stays HOLD**: the PIPD Writer owns it.
5. The exact owner act that unblocks 7 packages is written in `PLAN.md` §B as three commands.

## 6. Honest ceiling

This round did not make 22/22 pass and does not claim to. It moved the boundary into focus: **7 of 22
cannot pass without an Issuer act that this repository deliberately does not let an agent perform**, and
the owner pre-authorisation window is now open so that act is one delegation signature away. Everything
else that was measurable this round was measured and pushed.
