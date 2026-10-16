# SQS-THC Data-Plane Verification (台股歷史資料庫 cross-confirmation)

Use when asked to cross-confirm the SQS-THC 台股歷史資料庫 (Taiwan stock historical
database) against the upstream blueprint, or to inventory/verify the data plane.
Read-only pattern; no WorkOrder needed for a pure status cross-check.

## Upstream spec (normative — Shioaji-first blueprint operationalization)

`SQS-THC\data_plane\config\data_policy.yaml`:
- retention: daily 5y (authority PATCH_DEFAULT) / minute_1m 12mo
  (RBWI_ONE_YEAR_MINUTE_K_BASELINE) / tick 6mo MICROSTRUCTURE_SUBSET.
- universe: research_target_symbols 20–50, basis historical_liquidity_eligibility.
- timeframes: canonical_download [1m]; derived [3m, 5m, 15m, 30m].
- backtest_database layers: raw = parquet immutable provider artifacts,
  core = parquet canonical research minute bars, analytical = duckdb,
  metadata = sqlite catalog; PIT/Five-Clocks (asof, known_at, ts, source) on every row.
- publish_requirements: source_identity, rights_receipt, schema_pass.

`SQS-THC\data_plane\config\provider_profile.yaml`:
- shioaji.historical = QUALIFIED_READ_ONLY (max_kbar_window_days: 30 → backfill in
  ≤29-day windows); realtime = ADMISSION_PENDING; simulation = ADMISSION_PENDING;
  live = BLOCKED (by design, never a gap).
- finmind = CONDITIONAL_NOT_REQUIRED; TWSE/TPEx = REQUIRED_REFERENCE.

## Governed database as verified 2026-08-13 (reference snapshot)

DSV-2026-08-11-r1 — SHIOAJI 1.7.2; 49 symbols (50 requested, `2311:NO_CONTRACT` failed);
exactly 12 months 2025-08-11→2026-08-10; 2,793,223 rows; 242 trading days × ~266 1m
bars/day (09:01–13:30); 637 acquisition receipts (29-day windows) all FETCHED with
per-fetch sha256. Layout:

```
data_plane/data/raw/shioaji_kbars/symbol=XXX/start=YYYY-MM-DD_end=YYYY-MM-DD.parquet   (637)
data_plane/data/core/minute/symbol=XXX/minute.parquet                                  (49)
data_plane/data/backtest.duckdb            → minute_bars (2,793,223 rows, provider SHIOAJI)
data_plane/data/metadata/catalog.sqlite    → dataset_versions (DSV sha == manifest sha)
data_plane/data/metadata/dataset_manifest.json       (sha 62b10084…, rows 2,793,223)
data_plane/data/metadata/acquisition_receipts.jsonl  (637 lines, all FETCHED, all sha256)
data_plane/data/metadata/acquisition_summary.json
```

## Verification recipe (all read-only)

1. Counts: `os.listdir` symbol= dirs (49); `find data_plane/data/raw -name '*.parquet' | wc -l`
   (637, NO head pipe); receipts lines (637) with `"status": "FETCHED"` and `sha256` per line.
2. duckdb (read_only): `SELECT COUNT(*)`, `SELECT DISTINCT provider` (SHIOAJI),
   per-symbol `MIN/MAX(event_time)` (2025-08-11 09:01 → 2026-08-10 13:30), daily bar counts
   (`SELECT event_time::DATE, COUNT(*) … GROUP BY 1`), PIT columns populated.
3. Hash consistency: `sha256(dataset_manifest.json)` == catalog.sqlite
   `dataset_versions.sha` (byte-identical, no drift). Spot-check a raw parquet sha against
   its receipt line (verified: 2330 first window `038a4b99…` MATCH, rows 5851 / bytes 76947).
4. Config spec: provider_profile.yaml + data_policy.yaml values (above).
5. 知識庫 legacy disambiguation (cross-check target):
   - `知識庫\SQS-THC資料庫\台股價格歷史資料\finmind\` (6.7GB) = Spartoi-era (2025-10)
     FinMind bulk: `raw/kbar/` ~250 symbols per-day CSVs, `raw/index_5s/` 569 files
     2023-07-03→2025-10-31, `raw/daily/` only 5 symbols, `normalized/` empty, 150,584 raw
     files total → LEGACY research corpus, NOT the governed DB (FinMind is now
     CONDITIONAL_NOT_REQUIRED per the current blueprint).
   - `...\Taiwan STOCK\*_history.csv` (263 files) = daily OHLCV 2023-01-03→2025-06-26
     (2.5y), unregistered in catalog, stale → partial daily layer only, NOT
     blueprint-conforming (spec = 5y, all eligible TWSE/TPEx).
6. Conformance verdict: FULL only if daily 5y all-eligible + tick 6mo + raw layer +
   update pipeline + runtime qualification are ALL closed. As of 2026-08-13:
   PARTIAL — raw/core/duckdb/sqlite layers closed; daily 5y / tick 6mo / incremental
   pipeline / runtime qualification (STATUS_VECTOR `runtime_status: NOT_RUN`,
   TT-TS014-001 BLOCKING) open. SQS claims ceiling stays LOCAL_PACKAGE_PASS only.

## Pitfalls (verified this session)

- **Truncated-listing false absence:** `find ... | head -N` cannot prove a directory is
  absent. Misreported `data_plane/data/raw/` as missing from a head-truncated find; a
  fresh-context AO lane found `raw/shioaji_kbars/` with 637 parquet. Absence claims need a
  dedicated `ls -d <path>` / unbounded `find <path> -type f | wc -l` per expected item.
- **DuckDB reserved words:** `asof` / `known_at` are keywords — quote them in SQL
  (`"asof"`). Unquoted → ParserError.
- **`fetchdf()` needs pandas** (absent on system Python) — use `fetchall()` / plain SQL.
- **duckdb import on broken `.venv-data`:** the SQS `.venv-data` venv has a broken base
  interpreter (hermes-managed generation dir removed). Workaround:
  `sys.path.insert(0, r'C:\Projects\Agent_Workspace\SQS-THC\.venv-data\Lib\site-packages')`
  on system Python311, then `import duckdb`.
- Child (AO lane) reports are self-reports: after the lane flagged the raw layer, re-verify
  independently (this session: raw parquet sha vs receipt sha MATCH confirmed) before
  amending the report. Maker claims (manifest/catalog/receipts) were all byte-exact vs
  primary sources; the only error was the checker's own truncated-inventory false negative.
