# FAR round 029 — relay restart, a measured round, and F3 promoted to blocking

| | |
|---|---|
| schema | `FAR-ROUND-REPORT/1` |
| round | `FAR-20261031-029-relay-round-delta-and-f3-promotion` |
| supersedes the plan in | `FAR-20261031-028` → "next step: restart 10101, run a round with delta, promote F3" |
| control plane | HG-KSEOS (authority / state / acceptance) |
| governance contract | Fabric (`contracts/`, `assurance/`, `control/`) |
| product entry | SBL / FHS-MSC HANDOFF-PATCH-v1 |
| claim ceiling | **MEASURED_LOCAL** — two consecutive lane attempts measured zero; not a multi-round population claim |

## 1. The answer in one paragraph

The "next step" did not run as written, because its first premise was false: **`console_window_events_delta`
was not wired into the dispatcher at all** (`grep -c console_window scripts/hgk-lane-dispatch.py` → **0**).
F3 existed only as a standalone gate, so "run a round with the delta" was unbuildable until the field was
produced by the thing being measured. With that closed, the rest of the sequence was executed for real:
the relay was restarted (`RELAY_OK`, health 200, zero visible windows), an EXECUTE attempt was measured
(**rank 1 `opencode-go/deepseek-v4.1-flash`, exit 0, nonce present, usage bound, delta 0**) and a
VERIFY_SECURITY attempt was measured (**rank 1 `opencode-go/mimo-v2.6-flash`, exit 0, nonce present,
usage bound, asked == served, delta 0**). Two further defects surfaced on the way and were fixed: the rollout
identity resolver built the impossible pair `openai-codex` + `opencode-go/mimo-v2.6-flash` (which refused a
turn that had served the required arm), and `lane_evidence_gate` accused that same turn of
`silent_substitution` because it compared a qualified id to a bare model name. With those repaired, the only
remaining refusal was the historical blocking ticket `TT-EXECUTE-TRANSPORT-MISSING-SESSION-001`, which was
settled **through the typed spine API** against a registered evidence digest. The round now closes:
**`ROUND_MAY_CLOSE`, no problems** — with F3 promoted to blocking inside that gate.

## 2. Findings

| id | finding | evidence | class |
|---|---|---|---|
| **F-1** | F3 was not wired: the dispatcher emitted no `console_window_events_delta`, so the promotion criterion was unmeasurable | `grep -c console_window scripts/hgk-lane-dispatch.py` → 0 before the fix | gap (blocked the plan) |
| **F-2** | The relay was **down** (`RELAY_DOWN`, port 10101 not listening; 10102 is the unrelated Codex Desktop router); `relay_daemon.py start` brings it up with health 200 and **zero visible windows** | `relay_daemon.py status` before/after; `curl /healthz` | operational |
| **F-3** | The relay's own supervision is not a repair path: `relay-supervisor.receipts.jsonl` holds **1369 checks, 947 BLOCKED / 422 HEALTHY** — most checks find it down and do not bring it back | `var/far-lane-sod-003/evidence/relay-supervisor.receipts.jsonl` | structural |
| **F-4** | First measured EXECUTE attempt: served, delta 0 | `evidence/exec_delta1_receipt.json` | measurement |
| **F-5** | The rollout identity resolver made `provider=openai-codex` + `model=opencode-go/mimo-v2.6-flash` — an impossible arm — so `--require-arm opencode-go/mimo-v2.6-flash` refused a turn that had served it (`ERR_REQUIRED_ARM_NOT_SERVED` with exit 0, nonce, usage all present) | `evidence/verify_delta1_receipt_REFUSED.json` | defect (false red) |
| **F-6** | `lane_evidence_gate` then reported `silent_substitution: asked=opencode-go/mimo-v2.6-flash served=mimo-v2.6-flash` for the SAME arm, because it compared raw strings; the receipt's own `provider` field said `opencode-go` | `evidence/lane_gate_before.json` | defect (false red, most damaging code in the repo) |
| **F-7** | `TT-EXECUTE-TRANSPORT-MISSING-SESSION-001` (blocking, OPEN) was the last refusal, and its close criterion was already met by F-4 | `round_close_gate` output before settle | state |
| **F-8** | After the three fixes the round closes with F3 blocking: a receipt with `delta=3` is refused `ERR_CONSOLE_WINDOW_EMITTED`, a receipt with no delta is refused `ERR_CONSOLE_WINDOW_UNMEASURED` | `evidence/round_close_negative.json`, `evidence/round_close_good.json` | gate |

## 3. What was changed (all applied in this round)

| file | change |
|---|---|
| `scripts/hgk-lane-dispatch.py` | samples the 20 ms window ledger on the same boundary as the usage ledger and records `console_window_events_delta`, `console_window_ledger`, `console_window_owners` on every attempt; rollout identity parses a provider-qualified model id instead of pairing it with the client's transport provider |
| `scripts/lane_evidence_gate.py` | asked/served compared as `(provider, model)` pairs; a qualified asked id must match on both halves, a bare one on the model — `silent_substitution` can no longer be produced by a string shape |
| `scripts/round_close_gate.py` | **F3 promoted to blocking**: `ERR_CONSOLE_WINDOW_EMITTED` on a measured window, `ERR_CONSOLE_WINDOW_UNMEASURED` on a null delta |
| `scripts/settle_tt_execute_transport.py` | settles the transport ticket through `SharedSpine.register_evidence` + `close_tt`, refusing unless the receipt is rank 1, exit 0, nonce present, usage bound and delta 0 |

## 4. Measurement detail (the round that met the criterion)

| attempt | lane | rank | served arm | exit | nonce | usage | asked == served | window delta |
|---|---|---|---|---|---|---|---|---|
| `exec_delta1` | EXECUTE | 1 | `opencode-go/deepseek-v4.1-flash` | 0 | yes | ok | yes | **0** |
| `verify_delta1b` | VERIFY_SECURITY | 1 | `opencode-go/mimo-v2.6-flash` | 0 | yes | ok | yes | **0** |

Both attempts ran inside windows the ledger covered, and the ledger recorded **no** console-window event
after 09:00 today — so there is no owner-scheduled-task overlap to subtract. The promotion criterion stated in
FAR-028 (two consecutive zero-delta lane attempts, no overlap) was therefore met **before** the blocking line
was enabled, and the negative control (`delta=3`) proves the gate can still say no.

## 5. Decision and next executable steps

See `DECISION.md` (ruling, authorisation, signature) and `PLAN.md` (command-level steps R1–R6, including the
resumption of WP-FHS-17 / WP-FHS-11 / WP-FHS-20 under one package per brief).

## 6. Honest ceiling

Two attempts, one host, one afternoon. This is not a claim that the class is gone in general: it is a claim
that **this lane, on this host, under measurement, emitted no window while serving**, and that the gate now
refuses a round in which it does. The relay's missing repair path (F-3) is *not* fixed by this round; it is
raised as a tracked (non-blocking) ticket for the owner, because changing the supervisor's behaviour is a
decision about the owner's machine, not about this repository.
