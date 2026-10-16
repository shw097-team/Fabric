# HGK Spine Knowledge/Memory/KG Facilities — verified inventory (audit 2026-08-14)

Read-only audit of the HGK shared-spine knowledge stack + FABRIC knowledge assets.
All numbers verified live from the DB / filesystem at audit time — re-verify before
relying on them in a new session (the corpus is actively moving).

## Shared-spine DB (single file, ~794 MB)

- Path: `C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db`
  (backups: `var\backups\hg-kseos-*.db`)
- Read-only query pattern (sqlite3 CLI missing in git-bash):
  `sqlite3.connect('file:///C:/.../hg-kseos.db?mode=ro', uri=True)`

Row counts at audit time:

| table | rows | note |
|---|---|---|
| sources | 351 | 329 ACTIVE; **all canonical_paths point to DELETED dirs** (see data-drift) |
| source_units | 351 | 1 unit per source |
| candidates | 376 | 354 PROMOTED / 22 QUARANTINED |
| knowledge_docs | 354 | body total ~136.7 MB |
| knowledge_fts | 354 | FTS5 `unicode61`; idx posting rows ~15,960 |
| memory_records | 1 | scope=`default`; PCIV-F01 closure |
| kg_edges / kg_assertions | 0 / 0 | KG pipeline exists but never used |
| provider_bindings | 79 | only 1 ENABLED: `HGK-PROVIDER-FTS5` (slot `semantic-retrieval`, PREFERRED_DEFAULT) |
| evidence_refs | 163 | requirements 556, workorders 78, acceptances 538, canonical_events 508 |

Schema chain (schema.sql L168-261): `sources → source_units → candidates /
knowledge_docs → kg_edges / kg_assertions`, plus `memory_records` and
`provider_bindings` (XOR unique index on enabled). `SharedSpine.snapshot()` counts
all knowledge tables as part of the governance snapshot.

## KnowledgeFactory API (src/hg_kseos/knowledge.py, 241 lines)

- `ingest_text(canonical_path, text, authority_rank, anchor='full')` → SRC-/UNIT-/CAND- ids; drift guard `ERR_SOURCE_DRIFT` if existing sha differs
- `promote(candidate_id, verifier, evidence_ref, title)` → DOC- id; rejects self-approval (`ERR_SELF_APPROVAL`)
- `search(query, limit=5)` → FTS5 MATCH + bm25; abstains on empty/unsupported/no-hit
- `rebuild()` → rebuilds FTS + kg_edges from ACTIVE sources only
- `add_kg_assertion(doc_id, s, p, o)` → EDGE- id (dedup via sha)
- `verify_citation(doc_id, citation)` / `withdraw_source(source_id)` (cascades FTS+KG deletes)
- `remember(scope, body, provenance, expires_at, allow_pii=False)` → MEM- id; PII + poison guards
- `active_memory(scope)` / `revoke_memory(memory_id)`

Consumers: HG-KSEOS `cli.py` (ingest/promote/search/rebuild-knowledge),
`evolution.py` (capability-gap map), 5 test files, `tools/case_executors*.py`;
**cross-project: 6 SQS-THC `data_plane/src/*.py` modules do
`from hg_kseos.knowledge import KnowledgeFactory`** (e5g1_freeze_subject,
e5g5g6_rbwi_calibration, g45g6_evo004_knowledge, g7_knowledge_nrtv,
r5g4_corpus_admission, r5g5g6_cold_start) — any extraction/migration must shim or
re-point these imports.

## Data-drift finding (critical for any KB work)

All 351 sources reference paths under `SQS-THC\SSOT\...` (12) and
`SQS-THC\技術資料庫\...` (339). **Both trees no longer exist** (0 md files).
The content was relocated to `知識庫\HG-KSEOS_SSOT\` (86 md, incl.
`RBWI_WP_CONTROL_PACK`) and `知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT\` (192 md) /
`知識庫\SQS-THC資料庫\` (139 md). Consequences:
- `ERR_SOURCE_DRIFT` can never pass on re-ingest (files gone) — FTS is a stale
  snapshot that only works because withdraw/rebuild operate on DB content.
- Any migration/re-index must treat `知識庫\HG-KSEOS_SSOT` (etc.) as the new
  canonical root and re-ingest with fresh canonical_paths.

## FABRIC-side knowledge assets (the other half of the stack)

- **知識庫** root: `C:\Projects\Agent_Workspace\知識庫\` — 9,698 md across 12 roots
  (工程基座 5,916 / ASCE-WebX 1,328 / GENIE 808 / TCA-10X 449 / HG-KSEOS資料庫 323 /
  SQS-THC & TW-ICT_FSDT-Stack_SSOT 192 / 專業技術文檔 169 / 實作相關DOC 157 /
  SQS-THC資料庫 139 / 教程字幕 128 / HG-KSEOS_SSOT 86 / Obsidian投影 3).
- **FAR tri-source** (`Fabric\fabric-autonomous-research\far_retrieval.py`, 549
  lines): channel 1 = raw file scan of 9/12 知識庫 roots (token presence scoring,
  cap 2000 files / 2 MB each); channel 2 = RO direct sqlite on spine
  `knowledge_fts` MATCH + LIKE fallback + `memory_records` — **duplicates
  KnowledgeFactory.search logic without using the API**; channel 3 = arXiv only
  (SSRF-guarded). Qualified asset (FAR v3 ACTIVE, 103 tests).
- **Governance already reserved the slot**: `Fabric\control\KNOWLEDGE_POLICY.yaml`
  (namespaces hgk/sqs/fabric/assurance/shared, cross-namespace write DENY,
  provider_runtime_validation_gate=KG1); `Fabric\HGK_STACK_MANIFEST.yaml`
  (services include `knowledge_fts`; knowledge_namespace read `[hgk.*, shared.*]`);
  `Fabric\stage\RP002-STAGE-FABRIC\` has K1/KG1 gates + `A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml`
  (denominator 171,966 files; Wiki/RAG/KG/Obsidian = candidate surfaces, NOT canonical).
- **Profile team pattern (FDA/FAR)**: `{TEAM.md, governance\*.yaml contracts,
  evidence\ manifest+impl evidence, evidence\receipts\ per-item qualification
  receipts, CAPABILITY_MATRIX, EXECUTION_BINDING, FOLDER_REORGANIZATION_RECEIPT,
  router impl, tests, WO-* workorders}`. Existing `profiles\hgk-knowledge-factory`
  is a role-level distillation profile (empty skills/) — complementary to a
  runtime-infra team, not a replacement.
- **Acceptance baseline to preserve**: `HG-KSEOS\evidence\domains\retrieval\
  RAG_KB_RUNTIME_ACCEPTANCE.json` — L3+L4, ten checks (positive_retrieval,
  multi_source, exact_source_locator, citation_verifiable, abstention,
  stale_index_detection, withdrawal_no_stale, index_rebuild, deterministic_readback,
  tenant_scope_isolation); lexical/FTS-first, vector backend DEFERRED_SOURCE_BACKED.

## Extraction-feasibility notes (FABRIC-level shared knowledge infra proposal)

- Feasible: knowledge table cluster is self-contained (8 tables + module + CLI +
  tests + 3 domain acceptance artifacts) and the governance slot already exists.
- Risks: 794 MB single-file DB; FTS5 is file-bound; promote() needs cross-table
  atomicity; 6 SQS import sites; stale sources must be re-ingested from 知識庫
  roots first; keep `evidence_graph.py` (EVO-005 canonical evidence graph) distinct
  from `kg_edges` (knowledge triples) — they are two different graphs.
