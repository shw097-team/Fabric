# R10 tooling: the two repairs to this session's own dispatch wrapper

Successor file: `dispatch_r10.py` (predecessors `dispatch_r6.py` and `dispatch_r9.py` are left BYTE-UNCHANGED;
a successor is issued instead of editing a predecessor that already underpins published evidence).
Tests: `test_dispatch_r10.py` - 8 passed, no live lane and no network required.

## Repair 1 - a same-role later turn no longer destroys an earlier turn's provenance

The predecessors named the receipt `<lane>_dispatch_receipt_attempt<attempt>.json` while rounds dispatch every
turn with the same numeric attempt, so the SECOND turn of a role overwrote the first turn's receipt.
Measured: `EXECUTE_dispatch_receipt_attempt1.json` held the later turn (835.74 s) and the earlier turn's receipt
(364.5 s) survived only because it had been snapshotted by hand.

`receipt_paths(lane, turn, stamp)` now returns `<lane>_turn<N>_<UTC>_dispatch_receipt.json` plus a matching
attempt-log directory, and `snapshot()` copies the receipt AND the attempt log into the round root's
`lane_receipts/` the moment the turn returns, recording each copy's sha256.

## Repair 2 - a nonce that IS present is no longer reported absent

The dispatcher reads the nonce only from transcript `item.completed/agent_message` events
(`nonce_source` in its own receipt). Measured on the round-before's VERIFY turn: `code:
ERR_NO_ARM_EMITTED_NONCE`, `nonce_present: false`, `used_rank`/`used_transport_model` null - while the SAME
receipt's recorded `stdout_tail` ended with the nonce the brief had asked for, and its recorded
`stdout_path` (429,783 bytes) contained it.

`attest(receipt, brief, artifact_roots)` derives the expected nonce from the BRIEF being dispatched, then
searches the surfaces the dispatcher already recorded (`attempts[].stdout_path`, `attempts[].stderr_path`) plus
any caller-declared artifact root, and writes a SIBLING attestation record. The dispatcher's receipt is never
rewritten: an authoritative record is not edited by its consumer. The served arm is read from `attempts[]`,
because the dispatcher's `used_*` fields stay null on that code path.

Re-derived against the round-before's REAL receipt and brief (no live lane): verdict
`NONCE_PRESENT_DESPITE_DISPATCHER_CODE`, found in the 429,783-byte stdout the receipt itself recorded, arm
`rank 1 / openai-codex / gpt-6.1-sol`, 768.19 s. Evidence: `W2_REPRODUCTION.json`.

## What is NOT proven here

- No live lane turn was dispatched with the successor this round: the end-to-end path is proven by fixture
  plus the re-derivation above, not by a new sealed run. Stated, not implied.
- The dispatcher-side half (having `hgk-lane-dispatch.py` read the lane's artifact root itself) is a
  CONTROL-PLANE change and is carried as an **owner-ready** item; this round did not edit the dispatcher.
- Both repairs are in the round's own harness. Neither is evidence about any product behaviour.
