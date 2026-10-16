# FAR-20261019 handover

Round `FAR-20261019-owner-authorized-closure`, project `FAR-019-OWNER-AUTH`, claim ceiling `LOCAL`.

## What an external reviewer should read first
1. `FAR_RULING_019.md` — the ranked action set and its authority graph.
2. `OWNER_ACTION_ITEMS_019.md` — everything that still needs the owner, in one-action form.
3. `ERRATA_AND_FINDINGS_019.md` — what this round got wrong or discovered about its own process.
4. `TIER_A_EXECUTION.json`, `A4_A5_REPO_ACTS.json`, `REMOTE_READBACK_VERIFY_019.json` — raw receipts.

## Reproduce
```
python far019_contract.py   # regenerate the contract from the previous round, never from own output
python publish_019.py --stage payload
```

## Register delta
118 previous items re-checked; 6 genuinely closed; 10 new items created by the previous round; 94 open ({"agent-executable-now": 3, "other-round": 31, "owner-signature-required": 60}).

## Honest limits
See `ADJUDICATION_AND_LIMITATIONS_019.json`. No acceptance, no release, no production claim.
