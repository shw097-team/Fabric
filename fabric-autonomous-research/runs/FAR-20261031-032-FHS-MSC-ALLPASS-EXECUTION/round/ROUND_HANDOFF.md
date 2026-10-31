# ROUND HANDOFF — FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031

Authority: the owner, this round, `config/issuer/OWNER_AUTHORIZATION.json` (session `20261031_201542_761b82`,
`granted_at 2026-10-31T13:10:00Z`). Owner key window `WIN-68f2056b1972` opened by passphrase in the broker
(tkinter prompt, 8 h TTL, 40 ops, scope `permit_sign,admission_bundle_sign,registry_row_sign`, ceiling
`REPOSITORY_WRITE`, fingerprint `412b351937be72a1`) so the round would not stall waiting for a signature.

Governance: Fabric = contract, SBL = product-engineering entry, HG-KSEOS = native authorisation/state/acceptance
control plane. Lanes: PLAN `openai-codex/gpt-6.1-sol` medium, EXECUTE `opencode-go/deepseek-v4.1-flash`,
VERIFY `openai-codex/gpt-6.1-sol` medium — all three dispatched through `hgk-lane-dispatch.py`.

## 1. Lane acceptance — the claim, measured, pinned where pinning works

| Lane | Pinned (`--require-arm`) | Result | Evidence |
|---|---|---|---|
| PLAN | `openai-codex/gpt-6.1-sol` | **required == served**, rank 1, nonce echoed, 5.51 s | `receipts/PLAN_reqarm.json` |
| VERIFY | `openai-codex/gpt-6.1-sol` | **required == served**, rank 1, nonce echoed, 4.37 s | `receipts/VERIFY_reqarm.json` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | **pinning is broken** — see D-16 | `receipts/EXECUTE_reqarm.json` |
| EXECUTE | unpinned | serves: rank 1, deepseek-v4.1-flash, nonce echoed, 3.89 s | `receipts/EXECUTE_probe.json` |
| VERIFY | officer sitting C (unpinned) | `ok: true`, rank 1 gpt-6.1-sol, nonce echoed, 154.5 s, 2.5 M input tokens | `receipts/VERIFY_officer_C.json` |

**The prior round's finding stands and is now pinned for two of three lanes:** the lanes serve, and the
"VERIFY is blocked" reading came from `--identity-source relay-usage`, which cannot obtain a usage row for an
OAuth-direct turn on this host. That is now the *default's* opposite: the dispatcher defaults to
`codex-rollout`, and the frozen failure vocabulary is unchanged and test-pinned.

**D-16 (new, open):** `--require-arm opencode-go/deepseek-v4.1-flash` makes the child unroutable —
`{"type":"error","message":"The 'opencode-go/deepseek-v4.1-flash' model is not supported when using Codex with a
ChatGPT account."}`, exit 1 in 2.84 s. The pin is enforced by filtering candidates, but the pinned spawn path
hands the qualified model id to the Codex CLI instead of the relay that owns it. Unpinned EXECUTE routes
correctly. Consequence: **no EXECUTE receipt can carry `required_arm` today**, which is why the officer recorded
C1 as NOT_DISCHARGED.

## 2. Work-package state — 22 rows, before → after

| | before | after |
|---|---|---|
| PASS | 16 | **17** (`WP-FHS-10` re-bound to existing signed B1 evidence, `EVT-32277089ea9c024b`) |
| FAIL | 3 | **3** (`WP-12`, `WP-13`, and `WP-17` now FAIL *with an officer verdict* instead of `NOT_RUN`) |
| NOT_RUN | 3 | **2** (`WP-11`, `WP-20`) |

`WP-FHS-17` is **not** PASS. The commander's original-tree run reached
`PACKAGED → GRANT_OK → INSTALLED → HOST_LOADED → INVOKED → FUNCTIONALLY_QUALIFIED` with all fifteen negatives
refusing for the reason under test (`evidence/install.json`, `evidence/load.json`, `evidence/negatives/*`), but
the independent officer **could not execute the subject tree inside its enforced write roots** and recorded FAIL.
A checker that cannot run the subject cannot pass it — so the row is FAIL, and the reason is recorded in the
acceptance payload rather than explained away.

## 3. Defects found and fixed this round

| # | Where | What it was |
|---|---|---|
| F1 | `WP-FHS-17/tools/wp17_receiver.py` | `sha_file(a.grant)` on a `str` (2 sites) → `AttributeError`, parent then read the previous run's `install.json` |
| F2 | `build_evidence.py` | replay negative re-issued the **live** grant's nonce as its fixture, consuming the nonce the positive install needed |
| F3 | `build_evidence.py` | traversal negative ran against an absent root → refused `ROOT_ABSENT`, not the refusal under test |
| F4 | `build_evidence.py` | a crashed child's stale receipt was read as this run's verdict |
| F5 | `build_evidence.py` | run-local consumption ledger accumulated across runs → later negatives refused `ERR_NONCE_REPLAY` instead of their own codes |
| F6 | `build_evidence.py` | `host_op` was the constant string `"PARK"` |
| F7 | `build_evidence.py` | `disposition` / `missing_object` typed as PARK / grant-missing |
| F8 | `build_evidence.py` | second run reused a non-empty install root → `ERR_PREIMAGE_NOT_ABSENT` |
| F9 | `build_evidence.py` | the first fix of F6 still re-read the file; found by the officer's sitting B, now reads the crash-checked `install_obj` and honours `stale_receipt_ignored` |
| D-13 | `config/lane-routing-registry.yaml` | VERIFY route carried `transport_model: opencode-go/mimo-v2.6-flash` while provider/model said `openai-codex/gpt-6.1-sol` — the pool **declared** gpt and would have **sent** MiMo |
| D-14 | `sod_invariants.pairs` | declared `PLAN != VERIFY_SECURITY` distinct while epoch 40 binds both to gpt-6.1-sol |
| D-15 | `scripts/work_queue.py` | `DELIVERY` pointed at a `SBL_PIPD` segment that does not exist on this host |
| D-16 | `scripts/hgk-lane-dispatch.py` | pinning a non-OpenAI-provider arm makes it unroutable (above) |

## 4. What is still open (do not read this round as ALL PASS)

1. `WP-11`, `WP-20` — `NOT_RUN`. Same chain as WP-17: writeset → `issue_grant.py admit/issue/verify` → receiver
   install → fresh load → VERIFY. The WP-17 tree is the template; its eight defects are already fixed there.
2. `WP-12`, `WP-13` — FAIL with named first-fails.
3. **Native admission** — untouched. The bounded receiver is not the original Host Installer/Loader/Registry;
   `EVIDENCE_GAP.md` stands. `EXECUTED_BOUNDED_LOCAL ≠ native admission ≠ release`.
4. **D-16** — EXECUTE pin path. Needs the pinned spawn to route through the provider's relay rather than the
   Codex CLI's model selector.
5. **The officer's C2/C3/C5** — the oracle's nonce contract was written for one round-level nonce while each lane
   dispatched with its own; C4's probe (resolver accepting an unrelated rollout from the same directory) is a
   real finding about `codex-rollout` identity and needs its own requirement.
6. **`candidate/r18` vs `main`** — unrelated histories (267 ahead / 83 behind). This round published a
   main-based review branch (`lane/epoch-40-identity-source-20261031`) instead of forcing the graft.
7. **Delivery copy is lossy** — 415 of 909 manifest rows missing from the extracted knowledge-base copy
   (398 paths ≥260 chars, 17 under a renamed top directory). Bytes are intact in `C:\wg\pkg` (909/909).
8. **The queue driver is halted** — `continuation_driver.py` stopped WP-17 at 19:17:08 after eleven EXECUTE
   receipts (`halted_repeat`). Nothing restarts it; a fresh round must start it deliberately.

## 5. Opening commands for the next session

```
cd C:/wg/queue/WP-FHS-17 && python tools/build_evidence.py        # expect EXECUTED_BOUNDED_LOCAL, negatives_all_refused true
cd C:/Projects/Agent_Workspace/HG-KSEOS
  python scripts/scoreboard_consistency.py --json                 # authority = work_queue; fix projections, never the authority
  python scripts/lane_policy_reconcile.py --check                 # expect CONSISTENT at epoch 40
  PYTHONPATH="src;tests" python -m unittest tests.test_lane_policy tests.test_lane_identity_source_default
  python scripts/hgk-lane-dispatch.py --lane EXECUTE --require-arm opencode-go/deepseek-v4.1-flash ...   # D-16 reproduces here
```

Next package: `WP-FHS-11`. Issue the grant with `scripts/issue_grant.py admit` then `issue` (the key is present
and DPAPI-bound; `GRANT_VALID` is the expected verify output), install with the package's own receiver, then hand
the tree to VERIFY — and give the checker a write root that actually contains the subject, or the sitting will
be FAIL again for an environment reason.

## 6. Evidence index

- `receipts/` — every lane dispatch this round (JSON + attempts.ndjson + dispatch log)
- `oracle/ORACLE_LANE_ACCEPTANCE.md` — PLAN's oracle, written by the PLAN lane, hashed before the officer sat
- `oracle/ORACLE_WP-FHS-17.md` — WP-17 acceptance oracle, transcribed from the registered requirement
- `oracle/VERIFY_officer_C_output.txt` — the officer's full sitting-C output
- `WP-FHS-17_EIGHT_DEFECTS.md` — the chain that was reported PARK for eleven sittings
- `FAR_EVOLUTION_RECORD.md` — self-research / self-learning record for this round
- `WP-FHS-17-tools/` — the fixed tool tree, so the repository alone can reproduce it
