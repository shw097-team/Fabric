# WO-SKCV-20261014-HGK phase 3 — theme batch 2 for the hgk-governed-execution entry

Maker = Codex CLI (opencode-go/deepseek-v4.1-flash). One bounded batch. Batch 1 already landed: theme `external-evidence-closure` absorbed five references and produced topic_batch_1.json; do not redo it and do not touch its topic file or its stubs.

HARD READ RULE: read ONLY these paths, each once. Do NOT enumerate, do NOT recurse, do NOT search the tree.
- references/codex-canary-powershell.md
- references/codex-lane-log-liveness-markers.md
- references/codex-sealed-lane-windows.md
- references/codex-workspace-write.md
- references/topics/external-evidence-closure.md (only its envelope lines, to copy the batch-1 envelope shape)
- topic_batch_1.json (only to copy the record shape)

Deliverables, all inside your own work directory:
1. skill/references/topics/codex-lane-execution-and-workspace-write.md — the complete original bytes of the four files, verbatim, in the order listed, each behind a short comment envelope matching the batch-1 envelope shape. No reflowing, trimming, summarising or line-ending normalisation.
2. A one-line pointer stub at each of the four original paths, naming the topic file and the byte offset of that file's payload.
3. topic_batch_2.json — schema SKCV-HGK-TOPIC-BATCH/1, same shape as topic_batch_1.json: the topic file with digest and byte length, plus one entry per absorbed file with absorbed_path, bytes, sha256, byte_offset, payload_byte_end, stub_path.
4. Extend topic_check.py (it exists from batch 1) so it validates BOTH batches: recompute every absorbed digest out of its topic file, assert every named path still resolves, assert each stub names the right topic file and offset, and refuse with distinct typed codes for a missing, duplicated, reordered and mutated segment.
5. Run topic_check.py over both batches plus one negative probe per refusal class; record commands and exit codes.
6. phase3_result.json — schema SKCV-HGK-PHASE3-RESULT/1: what was absorbed in batch 2, the exact commands with exit codes, ran/skipped counts, typed refusals observed, the physical reference-file count under skill/references before and after, and an explicit statement that this is batch 2 of the reference themes while the remaining HGK themes stay OPEN.

Rules: no cap, threshold, linter, lock or policy change; no underscored/hidden files; no deletion; do not touch SKILL.md, entry_map.json or the batch-1 topic file; do not claim the reference-file count fell; no whole-tree scan; no canonical acceptance or promotion claim. If a command fails twice for the same reason, stop and record the failure. Stop after deliverable 6.
