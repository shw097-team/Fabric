# Decision — FAR-20261031-030

| | |
|---|---|
| decision id | `FAR-030-DECISION-01` |
| round | `FAR-20261031-030-fhs-22wp-state-and-issuer-boundary` |
| authority | HG-KSEOS control plane; owner pre-authorised signing (mandate 2026-10-31) |
| change class | engineering-base + one tooling repair (`owner_window.py close --force`) |
| claim ceiling | MEASURED_LOCAL |

## 1. Ruling

1. **The 22 packages are 2 DONE / 12 PARTIAL / 7 PARKED / 1 HOLD, and that is the answer this round
   reports.** A defensible row is not a passing row; relabelling PARKED as PASS would be exactly the
   "changed criterion" the owner's standing rule forbids.
2. **The 7 PARKED are gated on an Issuer act, not on more engineering.** All seven carry the same owner
   (*Bound-artifact original owner + HG-KSEOS Issuer*) and the same missing artefact (Issuer PERMIT).
3. **The agent does not delegate authority to itself.** The delegation signer refuses a window whose task
   does not match the delegation (`ERR_WINDOW_FOR_OTHER_TASK`, measured). Producing a matching window is
   the owner's passphrase act; the window it opens is what signs the delegation.
4. **Tooling repair adopted:** `owner_window.py close --force`. Measured defect: the signing service lives
   inside the `open` process, so when that process ends the window stays OPEN and `open` refuses a new one
   (`WINDOW_ALREADY_OPEN`) until the TTL expires — an owner lockout of up to 8 hours with no recovery path.
   The forced close signs nothing, writes a receipt (`artifacts/WINDOW_CLOSE_FORCE_*.json`) and only marks
   the window state; it cannot create authority.
5. **Continue the 12 PARTIAL under the lanes** — they are gated on evidence, not authority — while the
   owner passphrase prompt stands open for the delegation.
6. **WP-FHS-05 remains HOLD** (PIPD Writer).

## 2. Authorisation and signature

- Owner window for this task: `WIN-ff4cbf45c86e` (opened at task start, 40 ops, 8 h, ceiling
  `REPOSITORY_WRITE`, prompt source `tkinter`), force-closed with receipt after its service died.
- Issuer key: `config/issuer/issuer.key`, DPAPI-bound, key_id `135455ca00280c39`,
  `passphrase_envelope.state = NOT_REQUIRED_DPAPI_BOUND`.
- Signature recommendation: the owner enters the passphrase for a window whose task is
  `R18-FHS-SKELETON-SPINE-20261029`; the delegation is then signed **by that window** (not by an agent
  claiming authority), and the 3-kind bundle (`source_freeze`, `task_kind`, `oracle_ratification`) plus
  `lease_generation` goes to `NativeAdmission(registry).authorize` for the first PERMIT.

## 3. Rollback

- `owner_window.py`: revert the `close --force` hunk; no window state depends on it (the receipt files are
  additive evidence).
- No canonical state was transitioned this round except the FAR-029 transport ticket (previous round).

## 4. What the AO lane must check independently

1. `TERMINAL_STATE.json` says 22 defensible / 2 DONE — and this report does not claim otherwise.
2. The signer refusal is real: re-run `tools/canonical_sign_delegation.py` against a window whose task is
   not `R18-FHS-SKELETON-SPINE-20261029` and read `ERR_WINDOW_FOR_OTHER_TASK`.
3. The forced close produced a receipt with `signed_anything: false`.
4. No PERMIT artifact exists in any live tree (the seven scratch matches are under `var/**/scratch/`).
