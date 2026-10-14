# Taiwan Daily OHLCV acquisition (SQS-THC data plane)

Verified 2026-08-13 on WO-RP2-DAILY-001. Domain knowledge for the governed daily layer
of the SQS-THC backtest database, per Shioaji-first blueprint (daily tier =
TWSE/TPEx official reference authority) + user decision UD-DAILY-OHLCV-2026-08-13-001
(spec change: 5y all-eligible → 3~4y, 2023-01-03→2026-08-13, 263 TWSE/TPEx stocks).

## Endpoints (live canary results 2026-08-13)

- **TWSE STOCK_DAY** (works, 0.3–0.9 s/req):
  `https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=YYYYMMDD&stockNo=CODE`
  → `{"stat":"OK","title":...,"fields":[...],"data":[["114/08/01","45,352,225","51,714,816,380","1,145.00","1,1...`,...]}`
  - Row layout: [ROC_date, volume, amount, open, high, low, close, spread, trades, note]
  - ROC year = year + 1911; all numerics contain thousands commas — strip before float().
  - Empty `data` (or stat != OK) = code not listed on TWSE.
- **TPEx official** (UNREACHABLE from this environment — defect `TPEX_OFFICIAL_API_UNREACHABLE`):
  `st43_result.php` → 404 (endpoint moved/deprecated); `openapi/v1/*` → HTML/302 (WAF).
  Record the defect, do not retry forever; use the documented fallback instead.
- **Yahoo chart API** (fallback, works):
  `https://query1.finance.yahoo.com/v8/finance/chart/{CODE}.TWO?period1=<epoch>&period2=<epoch>&interval=1d`
  → `chart.result[0].timestamp[]` + `indicators.quote[0]{open,high,low,close,volume}` (None entries possible).
  Suffix `.TWO` = Taipei Exchange, `.TW` = TWSE. `meta.regularMarketTime` confirms the
  latest available bar (today's bar is published after ~14:00 TPE).
- **Market routing — probe, never assume:** 6xxx does NOT always mean TPEx (6505 台塑化 is
  TWSE). Strategy: try TWSE for every code; if ALL months come back empty → Yahoo `.TWO`
  → if empty → `.TW`. Record the detected venue per symbol as evidence.
- Provider/source identity per row: `TWSE_OFFICIAL` / `YAHOO_FINANCE`, venue
  `TWSE|TWO|TW`, `source_identity = TWSE_STOCK_DAY:YYYY-MM` or `YAHOO_CHART:.TWO:full`.

## Pipeline (data_plane/src/backfill_daily.py — Codex-written, English-only)

- Raw (immutable, idempotent): `data_plane/data/raw/daily_twse/symbol=XXX/start=YYYY-MM_end=YYYY-MM.parquet`
  (TWSE, one per month) or `yahoo_XXX.parquet`; zstd; atomic tmp+`os.replace`.
- Receipts journal `data_plane/data/metadata/daily_acquisition_receipts.jsonl`:
  `{symbol, source, start, end, rows, bytes, sha256, status: FETCHED|SKIP_EXISTS, at_utc}`;
  skip-if-hash-matches (re-verify existing artifact sha against journal before refetch).
- Core: `data_plane/data/core/daily/symbol=XXX/daily.parquet` — sort by date, dedup
  keep-last, deterministic full rebuild each run.
- DuckDB: `CREATE OR REPLACE TABLE daily_bars AS SELECT * FROM read_parquet('<core>/symbol=*/daily.parquet') ORDER BY symbol, date`.
- Manifest + catalog: `daily_dataset_manifest.json` (dsv `DSV-DAILY-*-r1`, universe, rows,
  coverage_start/end, failures, raw_artifact_count, receipts_sha256) → `catalog.sqlite`
  `dataset_versions` INSERT-or-REPLACE (adaptive columns: `dataset_version`|`version`,
  `symbol_count`|`symbols` — check PRAGMA table_info first).
- PIT: `asof` = `known_at` = bar date (daily data known at close); `retrieved_at` = fetch
  time UTC. `asof`/`known_at` are DuckDB reserved words — quote in SQL.
- Concurrency (repair BACKFILL-CONCURRENCY-FIX-001): `threading.Semaphore(4)` around the
  network fetch ONLY, `time.sleep(0.2)` outside any lock, per-symbol `PROGRESS` prints
  `flush=True`. (Global lock across sleep+fetch = 0 artifacts in 132 s + API stall.)
- Fail-closed: exit 0 only if symbol_failed == 0; internal repair pass re-fetches failed
  months once; outer repair loop = rerun (idempotent) + recheck.

## Verified failure modes + repairs (same round, run 1 → r3)

- **HTTP 308 from HiNetCDN (run-1 root cause, 20/263 symbols):** under concurrency TWSE
  intermittently answered `308 Permanent Redirect`; urllib raises
  `HTTPError 308` "redirect error that would lead to an infinite loop" and the built-in
  retry loop (3 × 0.4–0.8 s backoff) never recovered. Same request returns 200 when calm.
  Repair: catch `urllib.error.HTTPError` with `code == 308` → `sleep(8 + 4*attempt)` up to
  6 attempts; then the documented Yahoo fallback only if still failing. Record
  `TWSE_NETWORK_FAILURE <months>` per symbol in the manifest failures list.
- **O(n²) idempotent skip (run-2 killer, 32 symbols / 848 s → ETA 2 h+):** rerunning the
  full pipeline re-verifies every artifact via `latest_receipt()` which re-iterates the
  WHOLE journal — and each SKIP_EXISTS append grows the journal (quadratic blowup).
  Repair: build `dict[(symbol, source)] = last_receipt` ONCE from the loaded journal and
  monkeypatch `latest_receipt` to use it.
- **Surgical repair (r3, what actually finished the layer):** orchestrator tooling in
  gitignored `var/pciv/repair_daily.py` — `sys.path.insert` the module dir, import
  `backfill_daily`, monkeypatch both fixes above, `process_symbol()` ONLY the run-1 failed
  codes (idempotent per-artifact), then full rebuild for the whole universe
  (core → `build_duckdb()` → `write_manifest()` → `register_catalog()`), exit 0/1 by
  remaining failures. Product script stays codex-authored; the helper is task tooling.
- **Expected artifact count sanity:** 263 × 44 months ≈ 11.6k raw parquet + receipts 1:1;
  a symbol with a later IPO (e.g. 6958, 481 rows) legitimately has fewer — not a gap.
- **TWSE covers most 上櫃 codes too:** the market probe resulted in 0 Yahoo fallbacks for
  this 263-code universe — `venue` field therefore means "data-serving endpoint" (TWSE API
  serves both markets), not per-symbol listing exchange; disclose that semantics in
  evidence.

## Quality checker (data_plane/src/check_daily.py — read-only, JSON verdict + exit 0/1)

- C1: 263 symbols in core dirs AND duckdb table.
- C2: global min date ≤ 2023-01-04 and max ≥ 2026-08-12 (today's bar may not be published).
- C3: OHLC invariants (high ≥ max(open,close), low ≤ min(open,close), prices > 0, volume ≥ 0) = 0 violations.
- C4: (symbol, date) duplicates = 0.
- C5: max calendar gap per symbol ≤ 14 days (holiday/weekend allowance).
- C6: receipt lines valid + random sample of 50 raw files re-hashed against journal = 0 mismatches.
- C7: layer consistency — receipts rows summed by (symbol, source) LATEST receipt
  (SKIP_EXISTS-safe) == core rows == duckdb rows.
- C8: catalog has the DSV row with rows == duckdb count.
- C9: legacy cross-validation — sample 20 TWSE + 5 Yahoo symbols vs
  `知識庫\SQS-THC資料庫\台股價格歷史資料\Taiwan STOCK\{code}_history.csv` on the overlap
  window 2023-01-03→2025-06-26, |Δclose| ≤ 0.01, ratio ≥ 0.99.
- C10: PIT columns present and non-null.

## Legacy data disambiguation

- `Taiwan STOCK/` 263 `*_history.csv` (2023-01-03→2025-06-26, source unverified) = the
  cross-validation ORACLE, not the governed dataset (unregistered, stale).
- `finmind/` (6.7 GB, Spartoi-era 2025-10): kbar per-day CSVs (2025-09+), `index_5s`
  569 files (2023-07-03→2025-10-31), daily only 5 symbols — legacy research corpus;
  FinMind is CONDITIONAL_NOT_REQUIRED per the current blueprint.

## Late-round defect classes (r4 → r6, verified same day)

The first three classes below are INVISIBLE to the C1–C10 checker as originally written —
they were found by a reference-calendar audit and by cross-checking gap windows against
TWSE CURRENT data, not by check_daily itself.

- **Silent-empty month persisted as a 0-row artifact** (`BACKFILL-EMPTY-FRAME-PERSIST-001`):
  TWSE returns `stat:OK` + empty `data` for a month (transient CDN state) → the pipeline
  writes a 0-row parquet + `FETCHED` receipt rows=0 → every later run SKIPs it
  (sha matches) → the gap is permanent. Audit found 148 empty artifacts across the
  universe. Classification: months BEFORE the symbol's first non-empty month =
  pre-listing (LEGITIMATE, keep — e.g. 2646/6838/6606); empty months AFTER listing =
  transient (DELETE artifact, refetch).
- **Partial-month responses (silent truncation)**: a month can be fetched with only part of
  its rows (e.g. 5906 2025-03: 13/21 rows; 2025-02 missing 2/25–27) and persisted as if
  complete. C5's >14-day rule misses SMALL distributed deficits (5906 had ~123 missing
  rows with only 4 gaps >10d; 18 of 263 symbols were deficient, 6–123 rows each).
  Fix: reference-calendar audit — expected rows per symbol = count of a full-history
  symbol's dates (use 1101, 871 rows) within `[symbol first date, end]`; deficit >5 →
  DELETE ALL raw artifacts for that symbol → full 44-month refetch.
- **DuckDB reads polars-written String columns as BIGINT** (parquet metadata quirk; polars
  itself reads them as String): `DESCRIBE SELECT * FROM read_parquet(...)` shows
  `symbol BIGINT` → daily_bars.symbol is Int64 → legacy-CSV joins and `code + '_history.csv'`
  raise `TypeError: unsupported operand type(s) for +: 'int' and 'str'`. Fix:
  `CREATE OR REPLACE TABLE daily_bars AS SELECT CAST(symbol AS VARCHAR) AS symbol, ...`
  (and quote reserved words `"asof"`, `"known_at"` in the column list).
- **Genuine suspension vs fetch defect — verify against TWSE CURRENT data, never assume**:
  for every C5-flagged gap, query TWSE STOCK_DAY for the window months right now.
  TWSE HAS the days → fetch defect (refetch). TWSE LACKS the days → genuine
  non-trading/suspension (e.g. 1225 福懋油 suspended 2025-04-03→06-20; 1236/9918/9931
  genuinely no trades on the last 1–2 pre-CNY days — TWSE confirms). Also: `venue` from
  the probe is the data-serving endpoint, NOT the listing exchange.
- **User decision pattern — remove suspended stocks with evidence**
  (`UD-UNIVERSE-REMOVAL-2026-08-13-001`): suspended symbols are REMOVED from the universe
  (263 → 259); write `UNIVERSE_REMOVALS_<date>.md` evidence (per-symbol TWSE-verified
  non-trading windows, names taken from the TWSE `title` field, not memory); delete their
  core dirs, KEEP their raw artifacts as the historical record; universe file rewritten
  (same filename, v2 content) and checker constant `EXPECTED_SYMBOLS` updated via a Codex
  patch (writer=codex integrity).
- **Debug-test pollution**: a probe symbol (2330) fetched during a single-symbol debug run
  lands in raw+receipts but is NOT in the universe → C7 fails with receipts-core diff of
  EXACTLY one symbol (871). Cleanup: delete the raw dir, strip its receipts lines from the
  journal (backup the journal to `*.bak-YYYYMMDD` first), rebuild. Never run ad-hoc probe
  fetches inside the governed raw layer — use a scratch dir.
- **Checker constants track the universe**: after any universe change, C1's expected count
  must move with it (EXPECTED_SYMBOLS 263→259 via Codex). Record an
  AO/check-predicate update note in evidence (precedent: AO_PREDICATE_CORRECTION-001).

## Progress watchdog + mid-run spot check

Full pattern in SKILL.md §"Long background acquisitions". In short: cron `no_agent=True`
script reading the run log (progress per tick → final once via marker → silent; bounded
`repeat`); desktop sessions deliver scheduled ticks to the cron log only — use
`cronjob(action='run')` or terminal `notify_on_complete` for in-chat updates. Mid-run
conformance spot check: expected raw artifacts = 263 × 44 months (+1 per Yahoo symbol),
schema incl. all PIT columns, sample symbol date range + first-row OHLC plausibility,
provider/venue distribution, receipts = artifacts 1:1.

## Extra gotchas (polars + TWSE data semantics, verified same round)

- **`--` close = no-trade day (NOT a defect):** TWSE lists calendar days with zero
  trades as close=`--` (e.g. 5538 2025-07: 7/09, 7/21, 7/22, 7/30). A parser that
  float()-casts and skips these rows is CORRECT for backtesting (no tradable bar).
  This is also why a row-count audit against another symbol's full calendar is too
  strict — small scattered deficits of 1–4 days per month are usually no-trade days,
  not fetch defects. Verify against the source before "repairing".
- **polars `sort()` then `.unique()` does NOT preserve order** — `unique` reorders
  rows; re-sort after unique or before writing parquet (an unsorted core file looks
  like wild date gaps to naive readers).
- **`Path(p).name` on a str from `glob.glob` raises AttributeError** — always wrap
  `Path(p)` when deriving names/parents from glob results.
- **Double-fetch stability validation** for partial-month suspicion: fetch the month
  twice SEQUENTIALLY (no concurrency — CDN truncation is load-dependent); if the two
  responses' date sets agree, accept; if they differ, retry (bounded). Sequential
  single fetches consistently returned full data while 4-way-concurrent fetches got
  truncated months.
