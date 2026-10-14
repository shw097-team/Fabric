# WO-SKCV-20261014-HGK phase 2 — topic references ownership + alias compatibility

Maker = Codex CLI opencode-go/deepseek-v4.1-flash. PLAN/oracle = current Hermes owner route. Checker = fresh GLM lane, not you. Bounded single step; claim ceiling PARTIAL_TOPIC_ONLY. Do not replan, do not run broad suites, do not recurse the whole repository.

CWD is candidates/hgk. Phase-1 artifacts already exist and are evidence: entry_extract.py, entry_map.json, phase1_result.json, skill/SKILL.md, skill/references/topic-source-remainder.md. Never delete, rewrite or re-derive phase-1 evidence in this turn.

Deliver this one step: consolidate the existing skill/references directory into a small owned topic set while keeping every original byte recoverable.

Requirements:
1. Read the current entry SKILL.md routing table and skill/references/support-files-index.md to learn which reference paths are actually linked.
2. Create at most 8 files under skill/references/topics/ (plain visible Markdown, no underscore-prefixed names). Each topic file owns a named theme and must contain, verbatim and without any rewrite, the complete original bytes of the reference files it absorbs, each preceded by a short machine-readable envelope recording the original relative path, byte offset and sha256 of that segment.
3. For every original reference file that is no longer a real standalone file after consolidation, leave a visible Markdown stub at its original relative path containing a one-line pointer to the owning topic file and an explicit "original bytes preserved, not rewritten" note. A stub is compatibility only: do not claim it reduces the physical reference count.
4. Consume phase-1 topic-source-remainder.md into the same topic set the same way, then delete it only after its bytes are provably absorbed; keep entry_map.json consistent with the new layout and record which of its slices moved.
5. Emit consolidation_map.json: for every original reference file, its sha256, its destination (real file, or stub path plus owning topic plus byte offset), and a coverage verdict. Also emit a refusal-first missing/orphan report.
6. Add a self-check script (topic_check.py) that recomputes, from the consolidated tree only, the concatenated bytes of every absorbed original, compares each to the recorded sha256, asserts SKILL.md-linked paths all resolve on disk, asserts no dangling link and no orphan topic, and refuses (non-zero exit with a typed error code) on a missing, duplicated, reordered or mutated segment.
7. Run the self-check with the qualified interpreter C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe, plus a negative probe per refusal class, and record actual commands, exit codes, byte counts and ran/skipped in phase2_result.json.

Constraints: no change to the 100k hard cap, the 24k body advisory, the 60-reference warning threshold, the linter source, mutation locks or any policy. Do not hide files with an underscore prefix, do not delete contradicting history, do not raise or claim a lower reference count than physically exists. State plainly in phase2_result.json that physical alias-count debt is still open and that topic ownership is an engineering improvement, not a warning suppression. Stop after this step.
