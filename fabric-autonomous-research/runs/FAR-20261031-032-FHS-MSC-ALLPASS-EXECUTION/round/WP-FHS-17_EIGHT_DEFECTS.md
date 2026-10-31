# WP-FHS-17 — the chain that was reported PARK for eleven sittings, and the eight defects that made it so

Round: `FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031`
Tree: `C:/wg/queue/WP-FHS-17` (bounded WP-local receiver; **not** the original Host Installer/Loader/Registry)

## What the previous rounds recorded

`work_queue` said `WP-FHS-17 NOT_RUN`; the queue driver's officer verdict said `INCONCLUSIVE`; the EXECUTE lane
returned `PARK_GRANT_MISSING` with `missing_object: original-Issuer OPS grant for operation=install_occupant`
eleven times and the driver halted on repeat (`halted_repeat`, `phase_died count 27`, 19:17:08).

That reading was wrong in two independent ways, and each way was a defect in a file rather than a fact about the host.

## The eight defects, in the order they blocked the chain

| # | File | Defect | How it presented |
|---|---|---|---|
| F1 | `tools/wp17_receiver.py` | `sha_file(a.grant)` passed a `str` where a `Path` was required (2 sites) | `AttributeError` in the child; the parent then read the **previous run's** `install.json` and reported it |
| F2 | `tools/build_evidence.py` | the replay negative re-issued the **live** grant's nonce as its fixture | seeding it consumed the nonce the positive install was about to spend → `ERR_NONCE_REPLAY` at GATE, 0 effects |
| F3 | `tools/build_evidence.py` | the traversal negative ran against an absent root | refused `ROOT_ABSENT` — **not** the refusal under test (`PATH_TRAVERSAL`) |
| F4 | `tools/build_evidence.py` | a crashed child's stale receipt was read as this run's verdict | `install.json` from 1793415151 reported as the current result |
| F5 | `tools/build_evidence.py` | the run-local consumption ledger accumulated across runs | on the second run every fixture nonce read as spent; `nonce-regrant` and `gate-preimage` both refused `ERR_NONCE_REPLAY` instead of their own codes |
| F6 | `tools/build_evidence.py` | `host_op` was the **constant string** `"PARK"` | a receipt that says PARK after `INSTALLED` — a conclusion typed in, not a measurement |
| F7 | `tools/build_evidence.py` | `disposition`/`missing_object` were typed as PARK/grant-missing | same class as F6, in the host-op status artefact |
| F8 | `tools/build_evidence.py` | a second run reused a non-empty install root | `ERR_PREIMAGE_NOT_ABSENT`: a fresh install legitimately requires `preimage=ABSENT` |

## What was also true and was not a defect

The Issuer could sign all along. `scripts/issue_grant.py` needs `cryptography`; the interpreter that ran
`build_evidence.py` had it. The header comment in `build_evidence.py` — "No NEW signed admission can be issued in
this session" — was written when an interpreter without `cryptography` was used, and it then *stayed* in the file as
the reason for parking. A real Ed25519 grant was issued this round
(`key_id 135455ca00280c39`, nonce `G-135455ca00280c39-1793451375-0b1a8508`, `GRANT_VALID`) and the receiver's own
gate accepted it: all fourteen binding checks `ok`, with `nonce_unspent` the only one that ever failed, and only
because F2 had already spent it.

## Result after the fixes, reproduced from commands

```
cd C:/wg/queue/WP-FHS-17 && python tools/build_evidence.py
{
  "install": "INSTALLED",
  "install_code": null,
  "host_op": "EXECUTED_BOUNDED_LOCAL",
  "host_op_ceiling": "bounded WP-local receiver chain; NOT native Host admission",
  "load": "LOADED_AND_INVOKED",
  "consumer": "CONSUMER_ACK",
  "tamper_code": "LOADED_CHANGED_DURING_INVOKE",
  "negatives_all_refused": true,
  "grant_ledgered": true
}
```

Lifecycle: `PACKAGED → GRANT_OK → INSTALLED → HOST_LOADED → INVOKED → FUNCTIONALLY_QUALIFIED`.
Written files: `occupant/capboot_attest.py` (9,557 B, sha256 `c90cd91e…`, `matches_package: true`) and its
manifest (`929 B`, sha256 `d9676565…`).
All fifteen negatives refused **for the reason under test**, including `traversal_refused`,
`regrant_refused_before_effect`, `gate_preimage_refused`, `replay_refused_through_install`,
`replay_install_zero_effects`, `alias_refused`, `tamper_refused_at_load`, `tamper_withheld_consumer_ack`.

## Claim ceiling — do not read this as native admission

`EXECUTED_BOUNDED_LOCAL` means: a real signed grant was accepted, the exact WriteSet was applied with
`O_CREAT|O_EXCL` semantics, a **fresh process** loaded the occupant from its resolved origin and hashed its own
bytes, the needed feature was invoked with real input, and the original consumer acknowledged the output.

It does **not** mean the original Host Installer registered the occupant, nor that the original Host capability
Registry/Consumer resolved it through the CAP-BOOT ABI. `EVIDENCE_GAP.md` in the same tree states that gap and it
is still open. Native admission remains a separate requirement, and `PASS` on this artefact must carry
`BOUNDED_WP_LOCAL_RECEIVER` with it.

## Why the maker cannot be the officer here

Every one of F1–F8 was invisible to the run that produced it, because the run's own success criterion was
"the script printed something". F1 hid behind a stale file; F2 hid behind a negative that passed for the wrong
reason; F3 and F5 hid behind refusals that looked like rigour; F6 and F7 were assertions dressed as measurements.
Only re-running the tree from outside, and asking *which* refusal happened, exposes them.
