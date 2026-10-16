# Hermes Persistent Memory Full — Handling Recipe

Verified 2026-08-14, WO-HGK-MEM-RESEARCH-001 (board hermes-memory-far, Gate 1 FAR research
PASS, challenge lanes A1-A10 PASS + DOC-11 compliance). Use whenever MEMORY.md is at/over
~80% or the memory tool errors on add. All facts source-verified (tools/memory_tool.py,
hermes_cli/config_defaults.py, official docs, 知識庫 DOC-11).

## Mechanism facts (Hermes v0.20.0)
- Two files: `MEMORY.md` (agent notes, default 2200 chars ≈ 800 tokens) + `USER.md`
  (user profile, 1375 ≈ 500 tokens) at `<hermes_home>/memories/`, profile-scoped.
- Entries delimited by `\n§\n` (full delimiter, not bare §); multiline allowed.
- Frozen snapshot: system prompt gets the memory block at session start; mid-session
  writes update disk immediately but NOT the system prompt (prefix cache preserved).
  → edits take effect at the NEXT session; verify results there, not same-session.
- **NO auto-compaction by design**: over-limit write → error + current_entries + usage;
  agent must make room SAME TURN via replace/remove/apply_batch; fuse = max 3 failed
  consolidation attempts/turn (#42405) then terminal 'save skipped'.
- `replace` is also limit-bound (swapping in a longer entry can overflow).
- Header shows `[pct% — current/limit chars]`; >80% → consolidate BEFORE adding (official).
- drift guard (#26045): non-round-trip on-disk content → refuse write + `.bak.<ts>` +
  remediation; keep the file a clean §-list if hand-editing.
- injection/exfil scan (strict scope) on write and on snapshot load; hit entries render
  as `[BLOCKED: ...]` placeholder, raw text stays in live state for removal.
- `apply_batch` = official atomic path: remove/replace to make room + add in ONE call,
  final-budget check, all-or-nothing.

## Config (config.yaml, `memory:` section)
- `memory_enabled`, `user_profile_enabled`, `memory_char_limit` (2200), `user_char_limit`
  (1375), `write_approval` (false=free write), `provider` ('' = built-in only; ONE of 8
  external), `nudge_interval` (10). `display.memory_notifications`, `auxiliary.background_review`.
- **`flush_min_turns` is a DEAD key** (zero .py references; only in cli-config.yaml.example) —
  safe to remove, evidence-only repair.
- CLI: `hermes memory {setup,status,off,reset}`, `hermes journey` (list/delete/edit),
  `/memory` slash commands, `session_search` (FTS5, unlimited, free — use for detail,
  memory holds pointers).
- 8 external providers: honcho, openviking, mem0, hindsight, holographic, retaindb,
  byterover, supermemory. Built-in memory always active; provider is an ADDITIVE layer.

## Memory-full handling paths (official order)
1. add overflow → error → same-turn consolidate (replace merge / remove stale) → retry.
2. `apply_batch` for multi-entry consolidation (atomic, fuse-safe).
3. Manual: `hermes journey delete`, `hermes memory reset [--target all|memory|user]`,
   or edit file (keep clean § format or drift guard blocks later tool writes).
4. Raise `memory_char_limit` — last resort; docs: "Character limits keep memory focused".

## Governance mapping (知識庫 DOC-11, Hermes_Agent_OS)
- Memory ≠ truth; four gates (capture/object/recall/promotion); six classes
  (working/episodic/semantic/procedural/shared/fleet); retention must be finite;
  state snapshots belong in WorkOrder/evidence, NOT memory; procedures belong in skills;
  supersession preserves lineage; withdrawal = multi-layer propagation with readback;
  compaction must be readable-back/rollback-able (DOC-10 §9).
- P0 recipe that passed challenge: backup raw bytes → classify entries (six-class +
  operator 5-questions: source? current? scope? conflicts canonical? which layer?) →
  prune state snapshots (hashes/cron ids/in-progress projects ≈ 45-50% reclaim) +
  skill-duplicate pointers + compact env facts → target <80% → execute via memory tool
  (replace/remove/apply_batch, not manual edit) → verify next session (frozen snapshot).
- Removing duplicate pointers to ALREADY-INSTALLED skills is retention cleanup, NOT
  promotion — promotion gate (owner, anti-loop) applies only to creating NEW skills.

## FABRIC already has cross-session retrieval (verified) — do NOT reach for providers
- HGK spine: `knowledge_docs` 354 + `knowledge_fts` (SQLite FTS5, `HGK-PROVIDER-FTS5`
  binding = ENABLED/PREFERRED_DEFAULT); `KnowledgeFactory` API in
  src/hg_kseos/knowledge.py: ingest_text/search/remember/active_memory/revoke_memory/
  verify_citation; `memory_records` table (DOC-11-style, provenance/expiry/revoke).
- FAR: `far_retrieval.py` = tri-source retrieval (知識庫 root scan + spine `MATCH` + memory rows).
- 知識庫 ≈ 9,706 md; Hermes `session_search` state.db ≈ 138 MB FTS5.
- Conclusion: "need retrieval" is NOT a reason to enable an external provider; the only
  unmet gap is embedding concept-similarity (semantic) retrieval, unproven needed, and
  DOC-12 governance treats black-box similarity as a negative (hits must be source-backed).
  External provider enablement = TOOL-24 qualification WorkOrder, never a bare
  `hermes memory setup` flip.
