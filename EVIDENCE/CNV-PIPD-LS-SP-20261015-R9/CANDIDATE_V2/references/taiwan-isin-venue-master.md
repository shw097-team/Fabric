# Taiwan instrument identity (listing venue) + Five-Clocks semantic closure

Verified 2026-08-13 on WO-RP2-DAILY-003 (external focused closure r4, report r3).
Applies to any SQS-THC daily/backtest data work that must state market scope.

## 1. Listing venue: NEVER infer from code prefix — use the TWSE ISIN master

The 6xxx code range is NOT exclusively TPEx. In the SQS daily universe the following
are all TWSE 上市 per the official ISIN master: 6005 群益證, 6024 群益期, 6128 上福,
5538 東明-KY, 5471 松翰, 5515 建國, 5876 上海商銀. A scope document built on prefix
inference claimed "38 檔 6xxx 上櫃" — factually wrong; the 258-symbol universe is
100% TWSE-listed (TPEx=0). The external acceptance officer (r3) caught the TWSE+TPEx
scope claim as a dependency invalidation of the earlier "TPEx non-blocking (TWSE-only)"
exemption — the fix is evidence, not argument.

Authoritative master (official instrument database, TWSE ISIN service):
- 上市: `https://isin.twse.com.tw/isin/C_public.jsp?strMode=2`
- 上櫃: `https://isin.twse.com.tw/isin/C_public.jsp?strMode=4`
- Big5-encoded HTML table. Rows `<tr>...</tr>`, cells `<td>...</td>`:
  cells[0] = `'6005 群益證'` (4-digit code + space + name), cells[1] = ISIN,
  cells[3] = 市場別 (`'上市'` / `'上櫃'`; strMode=2 page also has `'上市臺灣創新板'`).
- Observed row counts 2026-08-13: strMode=2 → 1097, strMode=4 → 890.
- Reachable even when other TPEx official endpoints (st43, openapi.tpex.org.tw) 404/WAF.

Parse recipe:
1. `urllib` fetch both pages, decode `big5` with errors='replace'.
2. Regex-extract rows/cells; keep rows whose first cell matches `^(\d{4})\s+(.*)$`.
3. Resolve the universe code-by-code; report resolved/unresolved counts + a
   listing_venue_count dict. Record `identity_source='TWSE_ISIN_C_PUBLIC'` and
   `identity_asof` per row (the master is a CURRENT snapshot, not history).
4. **Negative control (mandatory):** include a code the master classifies TPEx that is
   NOT in the universe (e.g. 6182 合晶 → 上櫃) and show it. This proves an all-TWSE
   result is a real property of the universe, not a parser artifact.
5. Separate three fields explicitly in evidence: `listing_venue` (master identity) /
   `provider` (actual data provider, from receipts) / `source_endpoint`/`source_identity`
   (actual API route, from receipts). Never conflate them.
6. Branch logic per external recipe: TPEx count == 0 → correct scope/evidence to
   TWSE-only (no re-download); TPEx count > 0 → prove each TPEx row's source, bind
   rights/receipts, focused subset validation only.

## 2. Five-Clocks semantic closure (external DA-EXT-004 pattern)

External reviewers require the five clocks with SEMANTIC correctness ("clock 有值 ≠
clock 正確"): event/publication/availability/ingest/decision. The accepted conservative
Daily-EOD model needs NO new columns — a canonical semantic projection suffices:

```
event_time          = asof (trading date; EOD bar has no intraday timestamp)
publication_time   := availability_time := known_at := asof + 1 calendar day
ingest_time         = retrieved_at (actual fetch timestamp, UTC)
decision_time       = consumer decision timestamp; bar visible iff availability_time <= decision_time
```

Closure artifacts (all three, in order):
1. **Clock-contract doc** (`FIVE_CLOCKS_CONTRACT_<date>.md`): mapping table + an
   owner/source-backed equivalence statement (TWSE official EOD publishes after the
   13:30 close; D+1 00:00 is the conservative safe bound) + an explicit
   "conservative consequence" sentence (a D-day decision may NOT use D's close, by
   design) + revision policy (raw immutable, DSV lineage, no in-place rewrites).
2. **Causal-ordering checker** (add as check_daily C11 via a Codex patch):
   - `known_at <= asof` count == 0  (publication after event)
   - `retrieved_at` date < `asof` count == 0  (ingest not before event)
   - structural equality publication == availability (single field, via C10
     `known_at == asof + 1 day` on every row)
3. **Same-day negative canary stays PASS**: bar dated D physically exists, but a
   decision at D 09:30 sees 0 of them; D+1 09:00 sees all. (Rerun the canary each
   round — its log hash is evidence.)

Watch out: ingest_time (physical fetch, same evening) can precede the conservative
availability (D+1 00:00) — that is fine and expected; the USE gate is
availability <= decision, not ingest <= decision.

## 3. Scope-dependency invalidation guard

Changing a scope claim in new evidence re-opens every finding whose exemption was
conditional on the OLD scope (DA-EXT-009's non-blocking was conditioned on TWSE-only;
r3's TWSE+TPEx claim invalidated it). Before asserting a broader scope, check:
- rows actually acquired for the claimed venues (receipts),
- listing venue actually correct (master crosswalk),
- source provenance actually correct (source_identity per row),
- rights receipt actually covers that provider (rights scope field).
A0 scope authority decides the TARGET; it is not runtime/data evidence.
