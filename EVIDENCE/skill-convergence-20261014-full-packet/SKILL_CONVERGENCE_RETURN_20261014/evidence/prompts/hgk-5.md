# WO-SKCV-20261014-HGK phase 2 — theme batch 1 for the hgk-governed-execution entry

Maker = Codex CLI (opencode-go/deepseek-v4.1-flash). Bounded scope, one batch, one result file.

CONTEXT YOU MAY ASSUME (do not re-derive it): the hgk-governed-execution entry has ALREADY been split losslessly by an earlier phase: skill/SKILL.md is the 21 KB main document and skill/references/topics/construction-wave-and-remaining-procedures.md holds the complementary source bytes, bound together by entry_map.json (slice source/dest digests). DO NOT touch skill/SKILL.md, entry_map.json or that existing topic file — they are done and separately verified. Your job is reference consolidation only.

HARD READ RULE: read ONLY these paths, each once. Do NOT enumerate directories, do NOT recurse, do NOT search the tree, do NOT list skill/references to see what exists:
- skill/references/external-single-md-mandatory-route.md
- skill/references/external-acceptance-single-md-closure.md
- skill/references/external-submission-gates.md
- skill/references/external-challenge-evidence-closure-far.md
- skill/references/external-challenge-review-closure.md
- skill/SKILL.md (only to confirm how these five are named and to keep every name resolving)
Connect the bytes with the same discipline the adversarial-verification-rounds candidate already used: a topic file whose envelope records, per absorbed original, its relative path, its byte offset inside the topic file, its byte length and its sha256.

Deliverables, all inside your own work directory:
1. skill/references/topics/external-evidence-closure.md — the complete original bytes of all five files, verbatim, in the order listed, each behind a short comment envelope. No reflowing, no trimming, no summarising, no normalising of line endings, no added headings inside the payload.
2. A one-line pointer stub at each of the five original paths, naming the topic file and the byte offset of that file's payload.
3. topic_batch_1.json — schema SKCV-HGK-TOPIC-BATCH/1: theme name, the topic file with its digest and byte length, and one entry per absorbed file with absorbed_path, bytes, sha256, byte_offset, payload_byte_end, stub_path.
4. topic_check.py — a checker of your own that, from raw bytes only: recomputes each absorbed digest out of the topic file, asserts each named path in skill/SKILL.md still resolves, asserts the stub at each absorbed path exists and points back at the topic file with the right offset, and refuses with a distinct typed error code for a missing segment, a duplicated segment, a reordered segment and a mutated segment.
5. Run topic_check.py on the good case and one negative probe per refusal class; record commands and exit codes.
6. phase2_result.json — schema SKCV-HGK-PHASE2-RESULT/1: what you absorbed, the exact commands with exit codes, ran/skipped counts, typed refusals observed, the physical reference-file count under skill/references before and after your writes, and an explicit statement that this is batch 1 of the reference themes while the remaining HGK themes stay OPEN.

Rules: no cap, threshold, linter, lock or policy change; no underscored/hidden files; no deletion; do not claim the reference-file count fell (it will still be higher after adding the topic file); no whole-tree scan; no canonical acceptance claim. If a command fails twice for the same reason, stop and write the failure into phase2_result.json. Stop after deliverable 6 even if budget remains.
