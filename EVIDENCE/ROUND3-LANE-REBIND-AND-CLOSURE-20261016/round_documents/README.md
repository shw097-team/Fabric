# ROUND3-LANE-REBIND-AND-CLOSURE-20261016 — packet entry point

Round 3 of this session's governed work under HG-KSEOS. **Read this file first**; every other path in the
packet is named below with the question it answers.

**Claim ceiling: CANDIDATE_ONLY.** This packet performs no merge, deletes no branch, and asserts no
canonical acceptance. The repository merge and the branch cleanup are the OWNER's decisions; what is
published here is the implementation and the evidence an external verifier needs to accept or reject it.

## What the round did

The owner order delivered to session `20261016_104922_d455e7` re-pointed the three governed lanes:

| lane | model (owner order) | surface |
|---|---|---|
| PLAN & Orchestrator | `opencode-go/glm-5.3-flash` | in-process (this agent) |
| EXECUTE bounded writer | `opencode-go/deepseek-v4.1-flash` | CODEX CLI, sealed lane home |
| VERIFY / SECURITY checker | `opencode-go/deepseek-v4.1-flash` | CODEX CLI, sealed lane home |

That order **inverts** the separation-of-duties axis of epoch 21: the pair that had to be distinct
(EXECUTE vs VERIFY) becomes the same model, and the pair that carried a recorded owner-ordered collision
(PLAN vs VERIFY) stops colliding. Applying it therefore required one coupled change across five surfaces,
and it exposed two product defects that this round measured and (for one of them) repaired.

## Where to look

| file | question it answers |
|---|---|
| `round_documents/FAR_RULING.md` | what the round ruled, with the rejected options and their reasons |
| `round_documents/FAR_RULING_ADDENDUM_A.md` | the defects found *while executing* the ruling, and their disposition |
| `round_documents/R1_R2_R3_APPLY_RECEIPT.json` | per-file before/after digests for the rebind |
| `round_documents/PROJECTION_REPAIR_RECEIPT.json` | the 17 re-bound projection expectations, driven by `check_drift` |
| `round_documents/PATCH1_RECEIPT.json` | SC-12/13/14: the three self-caught defects and their corrections |
| `round_documents/PROMOTION_RECEIPT.json` | the bounded writer's change promoted into this tree, with backups taken FIRST |
| `round_documents/diff_R10_guard_exemption.patch` | the promoted change as a unified diff a reviewer can apply |
| `evidence/ORACLE_R10_RECEIPT.json`, `evidence/ORACLE_R10_*.txt` | the seven measured cases of the guard change |
| `round_documents/SUBJECT_DIGEST.json` | the frozen subject the checker judged, and the rule that built it |
| `lanes/EXECUTE__R1/`, `lanes/VERIFY_SECURITY__V4/` | the two lane dispatches: invocation, dispatch receipt, raw stdout/stderr |
| `preimages/` | the four pre-edit files, recovered by digest, with their provenance |
| `implementation/writer_output/` | what the bounded writer actually produced (its full candidate tree) |
| `round_documents/ROUND_CLOSURE.json` | the round's own account of what it closed and what it did not |
| `round_documents/FROZEN_MANIFEST.json`, `round_documents/GATE_REPORT.json`, `round_documents/PACKET_MANIFEST.json` | what was frozen, what the gate decided, and the sha256 of every file you are reading |
| `under_governance/CHECKPOINT.md` | the session handover and the next four moves |
| `openspec/` | the OpenSpec change this round authored and validated `--strict` |

## How to check it without trusting any summary

1. Recompute `PACKET_MANIFEST.json`: every listed file's sha256 and byte length must match the bytes you hold.
2. Recompute the frozen subject digest using the rule in `SUBJECT_DIGEST.json` and compare.
3. Re-derive the registry claims directly from `config/lane-routing-registry.yaml` and
   `config/model-lane-assignment.json`: epoch, revision, the `source_of_routes.sha256` against the live
   file bytes, the two route rows, the SoD pairs, and the two conflict entries.
4. Re-run the guard cases in `evidence/ORACLE_R10_*.txt` and confirm the exit codes and the
   `declared_conflict` field.
5. Read the checker's verdict in `lanes/VERIFY_SECURITY/V4/` and weigh it against the disclosure below.

## Disclosures you must carry

* The **checker shares the writer's model** (`opencode-go/deepseek-v4.1-flash`) BY OWNER ORDER. Model-axis
  independence between maker and checker is absent; what remains is process, lane and evidence-path
  independence plus the no-self-acceptance rule. This is declared in the registry as `SOD006-C3`, and no
  artifact in this packet claims model diversity.
* The pre-dispatch guard's `ADMITTED` state is **not** reached in this round: the product has no producer of
  an admission receipt (gap **R11**), so the guard's own verdicts here stop at the admission check. The
  lane serving evidence submitted instead is the lane's own dispatch receipt (`required_arm == served_arm`),
  which is a different thing and is labelled as such.
* `WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE` appears in both lanes' stderr: the credential-posture detector
  could not reach a verdict. It is a non-fatal, product-designed warning; it is **not** a pass.
