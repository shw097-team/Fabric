# Executable plan — the one owner act, then the lanes

## A. Where the work stands (measured, not claimed)

| group | packages | what is missing | who can close it |
|---|---|---|---|
| DONE | 00, 01 | — | — |
| PARTIAL | 02, 03, 04, 06, 07, 09, 15, 16, 17, 18, 19, 21 | per-package evidence at the package's own Reader | lanes (EXECUTE + independent VERIFY) |
| PARKED | 08, 10, 11, 12, 13, 14, 20 | **Issuer PERMIT** | owner passphrase → delegation → permit |
| HOLD | 05 | PIPD Writer ruling | PIPD Writer |

## B. The owner act (three commands, in this order)

The window's task string is the binding the signer checks (`TASK = "R18-FHS-SKELETON-SPINE-20261029"` in
`tools/canonical_sign_delegation.py`). A window opened under any other task is refused by design.

```bash
cd /c/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027

# 1. open the window under the task the delegation is bound to (passphrase prompt appears here)
python owner_window.py open --task R18-FHS-SKELETON-SPINE-20261029 \
  --ttl-hours 6 --max-ops 30 --scope permit_sign,admission_bundle_sign,registry_row_sign

# 2. while it serves, sign the delegation against THAT window
cd /c/Projects/Agent_Workspace/var/R18-FHS-SKELETON-SPINE-20261029/tools
python canonical_sign_delegation.py --workspace <window workspace>

# 3. three kinds + lease_generation -> first PERMIT
python -c "import sys;sys.path.insert(0,'/c/Projects/Agent_Workspace/HG-KSEOS/src');\
from hg_kseos.native_admission import NativeAdmission;..."   # bundle: source_freeze, task_kind, oracle_ratification
```

If step 1 is already open from an earlier attempt, close it first:

```bash
python owner_window.py close           # preferred: POSTs to the service
python owner_window.py close --force   # only when the service is gone; writes a receipt, signs nothing
```

## C. Then, per PARKED package (08, 10, 11, 12, 13, 14, 20)

1. Mint the PERMIT for that package's operation (`install_occupant` / release op) against its Subject +
   CandidateSHA + policy epoch.
2. Run the package's own builder under the permit; capture the original Reader's ACK (that is the only thing
   that satisfies `functional_raw_and_original_reader_ack` in WP-FHS-20's gap list).
3. Dispatch an independent VERIFY (`--require-arm opencode-go/mimo-v2.6-flash`, `--sandbox read-only`,
   `--identity-source codex-rollout`); the receipt must carry `console_window_events_delta: 0`.
4. Close the round with `round_close_gate --lane-receipt EXECUTE=… --lane-receipt VERIFY_SECURITY=…`.

## D. The 12 PARTIAL, in the order that unblocks the most

1. **WP-FHS-17** — officer FAIL lists four things: a CurrentNeed-bound native occupant (not a capability
   probe), Host-side loaded-origin proof (parent-side hashing is not enough), the tamper negative refusing on
   the right admission subject, and replay/preimage defects. Fix those four and re-run `officer/verify.py`.
2. **WP-FHS-21 / 03 / 02** — Issuer-owned, and the permit path above is the shared prerequisite.
3. **WP-FHS-15 / 16 / 18 / 19** — plugin/package-author evidence; the builders exist under each package.
4. **WP-FHS-04 / 06 / 07 / 09** — runtime/lane evidence; lane receipts already carry producer sha + git head.

## E. Stop conditions

- A window that opens and then cannot be closed is a tooling defect, not a state to work around: use
  `close --force` and record the receipt.
- A signer refusal is never bypassed by editing the delegation's window id; that converts an owner act into
  an agent act.
- A package whose original Reader does not exist on this host is `NO_FIT_WITH_REASON` from that Reader's
  owner — not PASS, and not "blocked" forever.
