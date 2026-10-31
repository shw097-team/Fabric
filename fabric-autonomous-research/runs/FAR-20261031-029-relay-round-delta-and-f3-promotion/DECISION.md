# Decision — FAR-20261031-029

| | |
|---|---|
| decision id | `FAR-029-DECISION-01` |
| round | `FAR-20261031-029-relay-round-delta-and-f3-promotion` |
| authority | HG-KSEOS control plane; owner pre-authorised the engineering ruling (`OWNER_MANDATE.txt`) |
| change class | engineering-base, reversible, code + state (one TT settled with evidence) |
| claim ceiling | MEASURED_LOCAL (two attempts, one host, one afternoon) |

## 1. Ruling

1. **F3 is promoted to blocking.** `round_close_gate` now refuses a round whose lane receipt (a) opened a
   console window during the attempt (`ERR_CONSOLE_WINDOW_EMITTED`), or (b) carries no measurement at all
   (`ERR_CONSOLE_WINDOW_UNMEASURED`). A null delta is refused exactly like a nonzero one: an unmeasured
   dispatch has not been shown to be windowless.
2. **The promotion criterion was met before the line was enabled**: two consecutive lane attempts
   (EXECUTE `opencode-go/deepseek-v4.1-flash`, VERIFY_SECURITY `opencode-go/mimo-v2.6-flash`) served with
   exit 0, nonce present, usage bound, asked == served and `console_window_events_delta == 0`, inside windows
   the 20 ms ledger covered, with no owner-scheduled-task overlap to subtract.
3. **Arm identity is compared as `(provider, model)`, never as a string.** A qualified asked id must match on
   both halves; a bare one on the model alone. `silent_substitution` is the most damaging verdict this
   repository can emit and must not be produced by a naming convention.
4. **The rollout identity carries the provider of the model id when the id is qualified.** The codex client's
   transport provider (`openai-codex`, because the CLI talks to the loopback relay) is not the served arm's
   provider.
5. **`TT-EXECUTE-TRANSPORT-MISSING-SESSION-001` is settled**, through `SharedSpine.register_evidence` +
   `close_tt`, against the digest of a receipt that satisfies its close criterion. This is a state
   transition recorded with a locator + sha256, not an assertion.
6. **`TT-RELAY-LIFECYCLE-NO-REPAIR-001` is raised (tracked, non-blocking), not closed.** The relay supervisor has run 1369 checks
   with 947 `BLOCKED` and 422 `HEALTHY`: it observes the outage and does not repair it, so every round begins
   with a manual restart. Changing what runs on the owner's machine on a five-minute timer is an owner
   decision (FAR-028 F7/F8), not an engineering one. It is non-blocking on purpose: the relay works when started,
   so its missing self-repair does not invalidate a round's evidence -- making it blocking would stop the very
   work packages this round exists to resume.

## 2. Authorisation and signature

- Authority envelope: `config/issuer/OWNER_AUTHORIZATION.json` (DPAPI-bound, no passphrase prompt on this
  host — verified earlier in this session, so no owner-key envelope window was opened).
- Signature recommendation: seal the digest of `DECISION.md` + `EVIDENCE_INDEX.json` with
  `scripts/issue_grant.py` under the existing issuer key, attach the grant to `EVIDENCE_INDEX.json`, and let
  the AO lane read the sealed record rather than this prose.
- What is **not** authorised here: production, release, Stage-3 / SQP1, any live trading path, and any change
  to the owner's scheduled tasks or the second Hermes instance.

## 3. Rollback

Single-file reverts, no state migration:

| change | revert |
|---|---|
| F3 blocking | `git revert` the `round_close_gate.py` hunk — the receipts keep their delta field either way |
| identity normalisation | `git revert` the `hgk-lane-dispatch.py` + `lane_evidence_gate.py` hunks |
| TT settlement | re-open with `SharedSpine.open_tt(...)` (same id, `blocking=1`), evidence ref retained |

## 4. What the AO lane must check independently

1. `EVIDENCE_INDEX.json` digests match the files, and no entry digests itself.
2. §4 of `EVIDENCE.md` reproduces from the two receipts alone (rank, exit, nonce, usage, delta).
3. The promotion is **blocking**, proven by the negative fixture (`delta=3` → `ERR_CONSOLE_WINDOW_EMITTED`),
   and the promotion criterion was met **before** the change (the two zero-delta attempts predate it).
4. The TT is `CLOSED` with an `evidence_ref` that resolves to a registered sha256 — not merely absent from the
   open list.
5. `TT-RELAY-LIFECYCLE-NO-REPAIR-001` is present and open: this round must not be read as "the relay is now
   self-healing".
