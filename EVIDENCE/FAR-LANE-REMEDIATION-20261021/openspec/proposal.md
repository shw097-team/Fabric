# Proposal: FAR lane/model declaration remediation (epoch 23)

## Why

Round `FAR-LANE-VERSION-MIX-20261021` measured 8 declaration surfaces for the three governed lanes and found
at least 4 contradictions (registry vs AGENTS.md vs live profile vs pool role labels), a toolchain pin that
names a non-existent binary, `check_drift` reporting 2 hard `DRIFT_VALUE` rows, and four routing files with
**no commit lineage** (`git status` = `??`). The owner has pre-authorized the FAR report's P0–P4 plan.

## What changes

1. **P0** — `PLAN` default = `openai-codex/gpt-6.1-sol` (medium, OpenAI OAuth, engine hermes);
   `VERIFY_SECURITY` default = `openai-codex/gpt-6.1-sol` (medium, OAuth, engine codex-cli);
   `EXECUTE` unchanged (`opencode-go/deepseek-v4.1-flash`, codex-cli). Registry advances to **epoch 23**.
2. **P1** — toolchain pin names the installed build (`0.163.0-alpha.10.2`) with its measured sha256;
   the dead `e78bad9887fa50cf` path is removed from the pin; Hermes `model.codex_bin` unified.
3. **P2** — pool rank/role labels agree with rank order; the in-Hermes PLAN-plane profile binds gpt-6.1-sol;
   registry projection expected values are synchronised in the same change set.
4. **P3** — owner-chain oracle updated **by owner authorization** (not to make a red test green for its own
   sake); the PLAN/VERIFY model-axis collision is declared `SOD006-C4 OPEN_OWNER_ORDERED`, not hidden.
5. **P4** — the four routing files are brought under git so the next rebind has commit lineage.

## Impact

- Lane dispatch: pinned dispatch (`force-rank` + `require-arm`) continues to work; unpinned PLAN/VERIFY now
  resolve to gpt-6.1-sol by default.
- Independence: PLAN vs VERIFY share one model by owner order → model-axis SoD absent for that pair; maker
  (EXECUTE=deepseek) vs checker (gpt) still distinct. Process separation only for the PLAN/VERIFY pair.
- Non-goals: no product-code change, no remote/release action, no `round_model_exclusions` bypass.

## Rollback

Per-file `.bak-farremediation-<utc>` copies plus the apply receipt's pre/post sha256 map.
