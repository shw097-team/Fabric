# External provider-tool governed enablement (TOOL-24 class)

Session: WO-HGK-GENIE-PREDESIGN-001, 2026-08-13. Trigger: user asked to "啟用 MATT SKILL"
(= Matt Pocock Skills). Verified end-to-end; the canary install passed 6/6 loader checks.

## Ground truth: HGK P0 tool registry (registered ≠ installed)

- Row: `registries/PROTECTED_IDENTITY_CLASS_QUALIFICATION.csv`:
  `P0-TOOL-016,mattpocock-skills v1.1,INSTALLABLE_PROVIDER_TOOL,DEFAULT_ENABLED_AFTER_QUALIFICATION,
  TOOL-24,...,runtime remains NOT_EXECUTED,FINAL_R2_CLASS_SPECIFIC_QUALIFICATION_DEFINED / NOT_EXECUTED`
- Mirrors (identical row): `control/prompts/PC-12.md`, `control/workflows/WF-08.md`,
  `control/state-machines/SM-06.md`, `control/agents/AP-10.md`.
- HLPE adapter exists but unbound: `worktrees/hlpe-qualification/adapters/mattpocock-skills.json`
  = ADAPTER-NO-005, `adoption_state: EXTERNAL_REQUIRED`, entrypoint `hlpe.adapters.route`,
  `source_plan_hash: cacf1f3c…` (canonical copy: 知識庫 工程基座 sdlc-prw-hlpe-formal adapters).
- Full-stack grep (case-sensitive `MATT`) found NO physical install: HGK tree, HGK
  control/skills (22 skills), Hermes skills dir, GENIE KB. Conclusion: registered, not
  installed — confirm with the user before assuming presence, and report the exact
  registry status rather than a bare "沒裝".

## Upstream identity (web verification)

- `github.com/mattpocock/skills` — "Skills for Real Engineers. Straight from my .agents
  directory." — ~216k stars, MIT, default branch `main`.
- Tags: v1.2.3 (latest), v1.2.2, v1.2.0, **v1.1.0** (matches registry's "v1.1"), v1.0.1.
- Official installer: `npx skills add mattpocock/skills` (skills.sh) — writes to
  `~/.claude/skills` (Claude Code ecosystem), NOT the Hermes skills dir. Hermes-compatible
  install = manual copy of the SKILL.md dirs.
- 35 SKILL.md across categories: engineering (18), in-progress (6 — skip for curated),
  misc (4), productivity (7). Browser verification note: browser_exec may fail with
  `ModuleNotFoundError: pydantic_core._pydantic_core` (broken env) — use
  `curl -s https://api.github.com/repos/<owner>/<repo>` instead.

## Enablement route (canary, user-authorized)

1. Pin: `git clone --depth 1 --branch v1.2.3 https://github.com/mattpocock/skills`
   into `HGK/var/a2/mattpocock-skills-v1.2.3` → PIN = v1.2.3 @ 6acc160e4e0cd062dbbbd7a1b26ae92855edf07e.
2. Curated subset (document-factory context, 6): `engineering/to-spec`,
   `productivity/grill-me`, `productivity/grilling` (grill-me dependency — install both),
   `engineering/code-review`, `productivity/handoff`, `engineering/research`.
3. Copy each dir (SKILL.md + `agents/openai.yaml` sidecars) to
   `C:\Users\user\AppData\Local\hermes\skills\mattpocock\<name>\` — vendor category keeps
   provenance; sidecars are Claude subagent configs (Hermes uses delegate_task) — keep as
   reference only.
4. Verify with the runtime itself: venv python YAML frontmatter parse per SKILL.md;
   `skills_list(category='mattpocock')` → 6; `skill_view` → `readiness_status=available`.
   Frontmatter: name/description + Claude extras (`disable-model-invocation`,
   `argument-hint`) tolerated; CRLF line endings fine.
5. Freeze `USER_DECISION_<TOPIC>_<date>.md` in `var/a2/` (decision_id/authority=USER/
   decided_at/status/bound_into + per-decision-point table + non-claims).
6. Registry honesty: P0-TOOL-016 stays `NOT_EXECUTED` — formal qualification (registry
   update + adapter binding) is a SEPARATE WorkOrder; record that non-claim explicitly.
7. Kanban: heartbeat the discussion card with the decision id.

## Adaptation notes (Claude-targeted bodies)

- `to-spec`: body says "run /setup-matt-pocock-skills" + "publish to the project issue
  tracker" — local context has no such tracker; USE THE SPEC TEMPLATE only (Problem
  Statement / Solution / User Stories / Implementation Decisions / Testing Decisions /
  Out of Scope / Further Notes) and skip issue publishing.
- `grill-me` delegates to `grilling` — always install both.

## Design-discussion method (grilling) for 實作前設計開發討論

Load `grilling`; map the decision space as a design tree; each round ask the WHOLE
frontier (questions whose prerequisites are settled), numbered, each with a
`➡️ recommended answer`; wait for answers before the next round; facts are the agent's
job (dispatch read-only lanes / look them up), decisions are the user's; done when the
frontier is empty — do not act until the user confirms shared understanding. Settled
decisions freeze as `USER_DECISION_*` files. In this round's usage: MATT ambiguity was
resolved by the user's one-line clarification (a decision), not by guessing.
