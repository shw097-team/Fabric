# CHECKPOINT — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

Session `20261016_104922_d455e7`. Round 3 of this session's governed work under HG-KSEOS (control plane) with
Hermes as the governed Runtime/Orchestration plane. Authority: the owner order delivered to this session.

**Claim ceiling: CANDIDATE_ONLY. `hgk_canonical_acceptance: NOT_PERFORMED`.** No merge, no branch deletion, no
promotion beyond this working tree.

## State on handover

Landed and measured in the working tree:

* **R1/R2/R3 — lane rebind to the owner order.** `config/lane-routing-registry.yaml` (epoch 21 -> 22),
  `config/model-lane-assignment.json` (revision 22, 11 `sod` prose fields rewritten), the dispatch-time pool
  (`config/lane-route-slots.candidate.json`, revision 9 -> 10), and the conformance fixture
  (`tests/test_lane_policy.py`) all moved in one change. PLAN rank-1 is now `opencode-go/glm-5.3-flash`;
  VERIFY/SECURITY rank-1 is now `opencode-go/deepseek-v4.1-flash`; EXECUTE unchanged. `source_of_routes`
  re-pinned to the live digest. `check_drift`: **0 findings / 0 errors**. Conformance suite: **OK**.
* **SoD re-declaration.** `SOD006-C3` declared (`OWNER_ORDERED_IN_FORCE`) for EXECUTE/VERIFY; `SOD006-C2`
  SUPERSEDED and retained; both pair flags flipped.
* **R10 — enforcement agreement.** The pre-dispatch guard now honours an owner-ordered declared collision,
  additively and fail-closed, with the conflict id visible in every verdict. Authored by the **mandated
  EXECUTE lane** (`opencode-go/deepseek-v4.1-flash`, `required_arm == served_arm`, rank 1, usage receipt OK,
  508.72 s) and promoted with backups taken **before** the write. Oracle from canonical: **7/7**.
* **Frozen subject** digested (`SUBJECT_DIGEST.json`) for the checker's reference.
* **OpenSpec** change `hgk-round3-lane-rebind-20261016` authored and validated `--strict`.
* **Self-caught defects** SC-12 (backup ordering; preimages recovered by digest), SC-13 (unquoted YAML note
  made the registry unparseable), SC-14 (a bound field dropped by a rewrite; restored, not the binding
  deleted) — all disclosed in `PATCH1_RECEIPT.json` and FAR addendum A.

## Open items the next session must not silently drop

| item | state | who |
|---|---|---|
| **R11** — no admission-receipt producer exists, so the guard can refuse but never admit | OPEN, recorded | owner decides whether to build one |
| **The exemption's trust boundary** — an owner-ordered declaration in the registry is now sufficient to admit a same-model pair | recorded as an accepted risk | owner policy decision |
| **F-IND-3** — the previous round's canonical writer was not the mandated writer | not retroactively curable | owner disposition |
| **Repository merge / branch cleanup** (PRs #6, #8 and the mergeable-and-deletable branches) | mergeable; the merge is the OWNER's | owner |
| **NF-05** — the dispatch pool is read while its own `status` says CANDIDATE | recorded in the file | owner decides on promotion |
| **F-IND-2** — the detector does not cover the epoch/revision coupling | open | next round |

## Next four moves

1. Re-run `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/oracle_R10.py` and confirm 7/7 on this tree.
2. Decide R11: build an admission-receipt producer (a lane-shaped probe writing `status: ADMITTED` with the
   served arm), or remove the ADMITTED branch from the guard so the gate stops claiming a state it cannot
   reach.
3. Then, and only then, decide the merge for the open publication PRs — the repository history is the
   owner's, and the round's own packet is written so an external verifier can reject it without a merge.
4. If the lane order changes again, do NOT edit only the route row: move the five surfaces plus `epoch`,
   `revision`, the digest pin, every projection binding, and the conformance fixture in one change, or the
   suite and the guard will both be correct and disagree.

## Where the work lives

* Round: `C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\`
* Packet for the external verifier: `EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/` in the Fabric clone,
  published on branch `pub/round3-lane-rebind-and-closure-20261016`.
* Preimages for rollback: `preimages/` in the round directory (proven by digest).
