# WO-SKCV-20261014-CONSUMER phase 3 — rewire the existing consumer instead of adding a parallel one

Maker = Codex CLI (opencode-go/deepseek-v4.1-flash). One bounded deliverable. Read-only outside your allow-list.

HARD READ RULE: read ONLY these paths, each once. Do NOT enumerate the tree, do NOT recurse, do NOT grep the repository.
- tools/skill_manager_tool.py
- tools/skill_linter.py
- tools/skill_manager_batch.py
- tests/tools/test_lint_full_current.py
- tests/tools/conftest.py
- phase1_result.json
- phase2_result.json (if it exists; if not, say so and continue from phase1_result.json)

CONTEXT YOU MAY ASSUME: phase 1 patched tools/skill_manager_tool.py and tools/skill_manager_batch.py and added tests/tools/test_lint_full_current.py; phase 2 built the full-current lint primitive and proved it detects the two oversized governance entries, but nothing consumes its findings yet — an unread finding is detection, not enforcement. An earlier phase-3 turn exhausted its budget while exploring and produced nothing; do not repeat that.

Deliverable (all inside your own work directory):
1. A bounded reader in tools/skill_manager_tool.py: when an edit/apply request targets a skill, the tool consults the existing lint primitive for that skill and records the findings it used. Reuse the existing primitive — do not build a second linter, do not add a daemon, database or lock manager, and do not change any cap, threshold or policy constant.
2. The same consultation path in tools/skill_manager_batch.py, so batch mode reports the same findings shape as single mode.
3. One focused test in tests/tools/ that proves the reader path fires for an oversized subject and returns the same findings the primitive returns directly. Keep it small.
4. Run that test plus the existing tests/tools/test_lint_full_current.py with the qualified interpreter and record the exact command, exit code and pass/skip/fail counts. If a test cannot run in this environment, say so explicitly instead of reporting it green.
5. phase3_result.json — schema SKCV-CONSUMER-PHASE3-RESULT/1: files changed with before/after digests, the reader's shape, the commands with exit codes, ran/skipped counts, which parts of the consumer chain remain unwired, and an explicit statement that no policy, cap or threshold was changed and no acceptance is claimed.

Rules: no deletion, no underscore-hidden files, no whole-tree scan, no canonical acceptance or promotion claim, no self-verification claim. If a command fails twice for the same reason, stop and record the failure. Stop after deliverable 5 even if budget remains.
