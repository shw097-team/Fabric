# POST-PUBLICATION ADDENDUM — FAR-20261016-018

claim ceiling: **LOCAL** · `canonical_AO_acceptance` = `NOT_ISSUED` · this pack is a **candidate** for
external acceptance; nothing here is an acceptance, a release, or a merge.

## 1. What was published

branch `evidence/far-018-r7r11-residual-closure` → PR **#13** (left **Draft** on purpose).
Base `main` = `312baa0ee2aa591000959cc878bb978a31c89796` and **unchanged** by this round.

| commit | kind | what |
|---|---|---|
| `f9a73ee5` | payload | the first publication of the 38-file payload |
| `1e2f0cc6` | additive | corrects `PACK_INDEX.json` + binds the closure receipts |
| `47548b51` | additive | mirrors the payload so the branch carries exactly what the index lists (the round's own harness scripts, the adjudication, the preserved first-fail) |
| *(final)* | additive | the final readback receipt, the publish receipt and this addendum |

Every additive commit is a fast-forward on the same branch; **`main` was never written and no force push
was used**.

## 2. Disclosures (things that went wrong, kept rather than hidden)

1. **An accidental publish.** Probing the publish broker with `--help` **executed it**: the broker has no
   argument parser, so it treated the probe as an invocation and published the payload that
   `PUBLISH_MANIFEST.json` already pinned. The resulting commit is exactly the intended payload, so no
   corrective write was needed — but the invocation was unintended and is recorded here rather than
   presented as a deliberate step. A broker intended to be probed should fail closed on an unknown flag.
2. **`PACK_INDEX.json` listed itself with a stale digest.** A file cannot contain its own digest, so the
   self-row asserted the digest of its *previous* content. The live remote readback caught it as **exactly
   one mismatch** (`PACK_INDEX.json`, 5606 bytes recorded vs 6039 actual). Fixed by excluding the index
   from its own listing and declaring the exclusion in `self_excluded` + `not_listed_by_design`, with the
   reason stated in the artifact. Its digest is now carried by the publish/readback receipts instead.
3. **A guard root that did not exist.** The first VERIFY dispatch failed closed with
   `ERR_GUARD_ROOT_MISSING` because the round guarded a file it had not generated yet; the dispatcher
   refused rather than report a vacuous clean subject. Preserved at
   `lane/VERIFY_ATTEMPT1_REFUSED.json` with its root cause and the remediation actually applied.
4. **A maker probe that could not fail.** The round's own self-check item S3 looked up a work-order count
   under a guessed key and silently read zero, which is the precise defect class the governance skill
   warns about. The harness's own negative control said so out loud (`not_detected: ["admission"]` —
   undetectable *because the check was already broken*). Fixed to assert a key HIT, after which the
   negative control detected **14/14** injected mutations.
5. **A first-fail that a retry erases.** The successful VERIFY retry overwrote the refused attempt's
   receipt. That is recorded as errata ER1 and the first-fail was preserved explicitly.

## 3. Independent verification of this round's artifacts

The checker ran on a **different model axis** from the writer:
EXECUTE = `opencode-go/deepseek-v4.1-flash`, VERIFY = `openai-codex/gpt-6.1-sol` (pinned with
`--require-arm`; the pool's rank 1 was the writer's own model, so pinning rank 2 is what makes the
cross-model separation real). The checker did **not** mutate the subject
(`subject_mutation: CLEAN`, 9 guarded files identical before and after).

| verdict | count | detail |
|---|---|---|
| AGREE | 5 | V1 counts recomputed independently; V3 the de-vacuumed check changes verdict on strip; V4 all 5 pointer slices recomputed byte-exact with a mutation that aborts; V5 the previous round's S8b really is a literal `True` (confirmed by AST scan — `sod_declared` is stored and never loaded); V6 no unachieved outcome is asserted |
| UNVERIFIABLE | 2 | V2 the checker's sandbox is read-only so it could not execute the isolation harness; V7 the historical guard refusal cannot be authenticated from artifacts |
| DISAGREE | 0 | — |

Both UNVERIFIABLE items were **narrowed, never rounded up**: see `ADJUDICATION_AND_LIMITATIONS.json`.

## 4. Readback

`REMOTE_READBACK_VERIFY.json` compares the remote tree's blob id against a locally computed git blob id
(`sha1("blob <len>\0" + bytes)`) — an exact byte check needing no download:

**50/50 listed files byte-exact, 0 mismatches, 0 committed-but-unindexed, 0 missing, `main` unchanged,
PR #13 open and Draft.**

## 5. Nonclaims

- No acceptance-report finding is claimed closed by this pack. `R7-03`'s **formal** closure still needs a
  boundary the checker cannot lift (a distinct OS identity) — the round demonstrates the mechanism only.
- The two UNVERIFIABLE items are open, and are named as such in the adjudication.
- `full_convergence_verdict` = `TEMP_CLOSED_CHALLENGE`, `production_verdict` = `FAIL_CLOSED`,
  `canonical_AO_acceptance` = `NOT_ISSUED` — unchanged by this round.
- Nothing here is merged. the peer chain (#6/#8/#10), `R7-02`, `R7-04`, the canonical lane pin, the KP R04
  polarity repair and PR #13's promotion are all **owner-gated** and were deliberately not executed.
