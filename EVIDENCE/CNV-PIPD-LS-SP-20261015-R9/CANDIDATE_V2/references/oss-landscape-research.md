# FAR research execution: OSS-landscape scan mechanics + challenge closure (verified 2026-08-14, GENIE vNext WO-HGK-GENIE-VNEXT-RESEARCH-001)

Companion to `predesign-design-discussion.md` — the EXECUTION mechanics of the research
batches, not the discussion method. Verified on 2 batches + 1 challenge lane.

## Delegation batching (hard limits)
- `max_concurrent_children=3`: plan research as batch 1 (≤3 lanes) + batch 2 (1 lane).
  Dispatch batch 2 only AFTER batch 1's result re-enters the conversation.
- **A single delegation call MUST use `goal` + `context` — NOT the `tasks` array.**
  Batch mode rejects a one-element array with `"Batch mode requires at least 2 tasks"`
  (hit twice this round). `tasks=[{...}]` with one item is the same error; switch shape.
- Give every lane an explicit verdict vocabulary + output table shape (item | verdict |
  candidate repo+stars+last-push | rationale) so the integration step is mechanical.
  Vocabularies that worked: KEEP/REPLACE_WITH_OSS/OUTDATED/MERGE (thin layers);
  BUILD_THIN/INTEGRATE_OSS/ADOPT_OSS_PATTERN/REDESIGN/DROP (gaps);
  SUPERSEDES/EXTENDS/ORTHOGONAL/NOT_COVERED (new-corpus vs gaps).

## GitHub unauthenticated API rate limit (60/hr) — verified fallbacks
Shared IPs exhaust the limit in ~20 queries. Working workarounds (in order):
- shields.io badges for live stars/last-commit: `https://img.shields.io/github/stars/<o>/<r>`
  and `/last-commit/<o>/<r>` — cached ~24h, within ~1% of live; fine for verdicts.
- `https://github.com/<o>/<r>/commits.atom` feed for last-commit dates (no rate cost).
- HTML page `aria-label` star attributes for star counts.
- `raw.githubusercontent.com` README heads are NOT rate-limited — use for purpose
  disambiguation (e.g. "Skills for Real Engineers").
- Renamed/gone repos 404 (huggingface/agents→smolagents, awslabs/multi-agent-orchestrator
  gone): treat 404 as renamed-or-dead, search for the successor, note it honestly.
- **Star attribution trap:** a content repo (mattpocock/skills 216k★) vs its installer
  (vercel-labs/skills 28k★) are different repos — a challenge lane will fail any claim
  that blurs them. Cite owner/repo identifiers on every tool row.

## Challenge lane on integrated research output
- Fresh-context reviewer, given the integrated list + the evidence files (absolute paths)
  + 4 dimensions: EVIDENCE (spot-check stars/dates via curl), LOGIC (cross-batch
  contradictions, double-listing, dual-classified items), COMPLETENESS, OVER-REACH
  (OSS-claimed tools that are actually SaaS).
- Expect `PASS_CHALLENGE (conditional)`: the verdict structure rarely flips; findings are
  integrity/documentation defects. Close EVERY condition EXPLICITLY in the next artifact
  version (vN → vN.1) before HITL:
  - disambiguate star attribution (content repo vs installer);
  - fix item accounting (dedupe thin-build rows that are also embedded in integrate rows —
    annotate "see 類3" instead of double-listing);
  - split dual-listed items into -a/-b with a one-line explanation;
  - re-scope unsourced implementation couplings to "decision at next gate";
  - add owner/repo identifiers for traceability.
- Challenge reviewer re-verified 25/26 quantitative claims ≤0.5% — spot checks hold up
  when lanes were told "REAL values only, never fabricated".

## New-corpus re-classification (user adds KB material mid-task)
"相關資料已補進知識庫" → scan the new corpora (keyword counts + file citations per item)
and re-classify gaps with SUPERSEDES/EXTENDS/ORTHOGONAL/NOT_COVERED. Corpora CAN flip
items to SUPERSEDED (投影帳冊池-WXMA replaced the Projection-Ledger gap; TCA-10X AAA
replaced productization) — drop those from build lists, cite them as design sources.
Zero-hit keywords are evidence TOO (反模仿 0 hits → anti-mimicry stays a real thin-build).

## Product-family landing judgment (old design × governed stack)
- Subject = the master blueprint's product lanes (e.g. 總藍圖 r2 §6.1 lane map + §9
  20-subsection Mini-DocPacks with MVP schemas/EvalSpec) — the user may re-frame
  "基礎設施" to mean these lanes mid-discussion; re-root, don't keep the old frame.
- Map lane-by-lane: ✅已落地(rename/productize) / ✅大部分(thin layer) / ⚠️部分(OSS
  integrate) / ❌自建. The user's own claim ("HGK≈GENIE-MAKER, FABRIC≈MVP GENIE") is
  usually RIGHT — verify with the capability matrix, don't argue. Zero from-scratch lanes
  is a legitimate outcome; the real work collapses to thin layers + OSS integration +
  productization, and the build order should name the shared substrate first (e.g.
  store ledger → installer gate → taint → identity binding).
