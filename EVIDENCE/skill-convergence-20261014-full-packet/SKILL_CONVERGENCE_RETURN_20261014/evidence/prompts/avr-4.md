# WO-SKCV-20261014-AVR phase 2 (serial remediation) — reproduce phase 1, then ONE topic batch

Maker = Codex CLI opencode-go/deepseek-v4.1-flash. This is a remediation turn: two earlier AVR turns exhausted their budget while enumerating the tree. Bounded scope and a hard execution rule below.

HARD EXECUTION RULE — read this twice. Do NOT run any recursive directory listing or whole-tree search: no Get-ChildItem -Recurse, no -Recurse anywhere, no `rg` over the tree, no listing of skill/references to "see what is there". Read ONLY these exact paths, each at most once:
- baseline/adversarial-verification-rounds/SKILL.md
- skill/SKILL.md
- skill/references/topic-source-remainder.md
- entry_map.json
- phase1_result.json
- skill/references/support-files-index.md
Anything else you need, derive from those. Read them, then act. Budget your turn for the work, not for exploration.

Step A (mandatory first, keep it small): re-run the existing entry_extract.py generate/reconstruct/negative entry points with the qualified interpreter C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe. Record whether the regenerated skill/SKILL.md, topic-source-remainder.md and entry_map.json are byte-identical to the bytes already on disk (compare digests). If any file diverges, STOP and report divergence instead of overwriting.

Step B: pick exactly TWO theme groups from the reference paths you can see referenced in skill/SKILL.md — for example one group for the verification/acceptance-lane references and one group for the lane-harness/handover references. For those two groups ONLY, write skill/references/topics/<theme>.md containing the complete original bytes of each absorbed file verbatim behind a short envelope (original relative path, byte offset, sha256). Leave a visible one-line pointer stub at each absorbed original path. Write topic_batch_1.json listing every absorbed path, its digest, its owning topic and offset.

Step C: extend topic_check.py (create it if absent) to verify the batch-1 groups only: recompute each absorbed digest from the topic file, assert every path linked from skill/SKILL.md still resolves, assert no dangling link, and refuse with a typed error code on a missing, duplicated, reordered or mutated segment. Run it and one negative probe per refusal class.

Step D: write phase2_result.json with: the reproduction verdict per file, the exact commands and exit codes you ran, the absorbed-path list, ran/skipped counts, the typed refusals observed, and an explicit statement that this batch covers only 2 of the themes while the remaining themes and the physical alias-file count debt stay OPEN.

Constraints: no cap/threshold/linter/lock/policy change, no underscore-hidden files, no deletion of contradicting history, no claim that the reference count fell, no whole-tree scan. Stop after Step D even if budget remains — a complete small step beats an incomplete large one.
