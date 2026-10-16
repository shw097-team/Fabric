# Strategy backtest correctness + method-finalization honest closure (SQS/RBWI)

Verified 2026-08-20/21 on the SQS-THC 方案D/B runs (overnight-pullback REJECTED →
rf-overnight Slow-Loop supersede). Applies to ANY governed strategy backtest / method
finalization in the HGK|SQS stack. The recurring errors below were all caught by
FRESH-CONTEXT independent verification lanes (Codex readback + SWARM delegates) — never
trust a maker's own number claim; the whole point of the multi-surface harness is to
let a checker falsify the maker.

## A. Backtest-pipeline correctness traps (each silently corrupts results)

1. **Temporal split MUST be chronological, not per-symbol row slice.**
   Rows ordered `(symbol, date)`; `X[:int(N*0.6)]` slices the FIRST 60% of *symbols*
   across their FULL date range, so OOS (last 40% symbols) OVERLAPS the train calendar —
   it is NOT out-of-time. Real fix: collect each sample's date, take the 60th percentile
   unique-date as cutoff, `is_train = d0 <= cut` (true global out-of-time). Codex flagged
   this as FAIL; correct numbers changed the root cause reading.
2. **Gap / cross-section lookup key MUST be `(symbol, date)`, never `date` alone.**
   A dict `gapd[d0]` maps one date to ONE value, but 258 symbols trade the same day →
   ~82k of ~88k OOS rows silently attributed the wrong symbol's gap → wrong PnL. Key by
   `gapmap[(sym, d0)]`. A fresh lane found 82,053 mismatches and re-derived true gross
   (32bp vs script 8.92bp) — still negative, but different numbers.
3. **PIT cleanliness**: features from bars `i-5..i-1` + close[i]; label = `(open[i+1]-close[i])/close[i]`;
   nothing from bar i+1 may enter the signal. Check all prior-day closes fed to ma/eq50.
4. **Cost idempotency**: for a daily-scalp/overnight round trip (buy close, sell next
   open) the cost is `fee both sides + tax(sell) + slip both sides` = `14.25*2 + 30 + 5*2`
   = **68.5bp**, NOT `54.25` (fee counted once). When a receipt's summary field disagrees
   with the per-trade applied cost, fix the field to the APPLIED value; verify
   `avg_net ≈ avg_gross − 68.5bp` as a reconciliation check (it is a strong noise-catcher).

## B. Honest end-to-end method-finalization closure (no over-claim)

The correct disposition when a hypothetical strategy backtests negative, verified against
DOC-20/25 + RBWI §6 + TW-ICT v3.0 DOC-05:

1. **REJECT is evidence, not failure**: a falsified hypothesis becomes a
   `NEGATIVE_RESULT_<method>_REJECTED.json` (gross-pnl, gross win% vs breakeven%, cost
   6.64×, IS+OOS mechanism). Keep it; DOC-20 "失敗是資產" forbids deleting failed artifacts
   or overfit-rescue (no param-tune-to-green, no silent re-run).
2. **New candidate via Slow-Loop MethodChange supersede**: new `EXPERIMENT_SPEC_*.json`
   (candidate, anti-overfit gate, cost_model, acceptance = "gross>0 FIRST, then
   cost-adjusted", nonclaim). Not a direct swap; keeps lineage + rollback pointer.
3. **Result separation**: `gross edge vs baseline` and `cost-adjusted net` are different
   claims. A signal can have REAL edge (+14bp) yet still be **cost-adjusted-negative**
   (-32bp) when TWSE 68.5bp exceeds the edge → verdict
   `HYPOTHESIS_NOT_ESTABLISHED_FOR_PAPER_SHADOW`, Paper/Shadow **NOT_INITIATED**. Do NOT
   start Paper because the signal "has an edge" — the premise is cost-adjusted positive
   expectancy, and absence of it is the honest terminal.
4. **Per-regime honesty**: a combined boolean verdict hides an inverted IS<0 / OOS>0
   imbalance. Disclose per-regime and downgrade the verdict (e.g. proxy run had
   `FEASIBILITY_ONLY_POSITIVE_OOS_DRIVEN`). A robust / established-experience claim is NOT
   met by an OOS-only-positive split.
5. **Proxy vs real RF**: a signal proxy run (approximating the model) does NOT equal the
   real model weights. Run the real RandomForest (or configured model) before claiming
   anything; real-vs-proxy can reverse (proxy OOS positive, real RF gross positive but net
   negative after the same cost).

## C. Codex lane / CRLF traps (recur in this skill's own files)

- **Codex CLI against the HGK lane REQUIRES exporting `CODEX_HOME`** to the isolated
  lane BEFORE invoking the pinned executable (from bash: `export
  CODEX_HOME="$LOCALAPPDATA/HG-KSEOS/codex-hermes"` then `codex.exe ...`). Without it,
  codex reads the HUMAN `~/.codex` auth → `"model ... not supported when using Codex with
  a ChatGPT account"` 400. The daemon (port 10101) being up is necessary but not
  sufficient; the CODEX_HOME binding is what selects the lane. Route "fixed by another
  session" can still fail until CODEX_HOME is set in the invoking shell.
- **CRLF break-line trap** when patching this skill's reference files: a Windows path
  ending in `\` (e.g. `evidence\rbwi-fullrun\`) gets the backslash joined to the line
  terminator → `evidence\r\nbwi-fullrun` corruption inside the file. Fix with a
  **bytes-level replace** of `b"evidence\r\nbwi-fullrun"` → `b"evidence\rbwi-fullrun"`
  (read as bytes, replace, write bytes) — the patch tool has already run by then, so this
  is the repair step, not a way to avoid it.

## D. Test-suite baseline command (SQS)

SQS canonical suite requires `PYTHONPATH=src`:
`PYTHONPATH=src <python> -m unittest discover -s tests -t .` → 231 (base) / 244 (after
方案D method modules). Without PYTHONPATH you get false "ModuleNotFoundError: No module
named 'kernel'" loader errors (199-ran/5-error) that are NOT real failures — re-run with
PYTHONPATH before diagnosing.
