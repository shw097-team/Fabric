# Method

1. **Gate-1 route.** The round was classed `RESEARCH_LITERATURE_REPO` and routed through the live
   named-method registry: `src/hg_kseos/named_methods.py` `registry_snapshot()` reported 8
   `ACTIVE_SELECTED` methods, and `route(flow)` was executed for each flow the round uses
   (`round_closeout`, `lane_dispatch`, `doc_identity_repair`, `evidence_return`, `memory_write`,
   `handoff_write`, plus 2 more) — recorded in
   `_handover/PIPD-S4-R6-CLOSEOUT-20261016/route_check.json`. A negative control routed an unrelated
   flow to `NATIVE` with no provider, proving the router discriminates rather than always arming.
   Decision: `NATIVE_WITH_SELECTED_ARIS` / `FAR_ROUTE_NATIVE_ARIS`.
2. **Frozen subject first.** `origin/main`, the tag ref, the tag object and the tag target were read
   from the live remote before anything else; the working candidate was produced in a detached
   worktree so the operator's checkout was never touched.
3. **Compile before believing the envelope.** The command薄 declares `PROMPT_COMPILE_BLOCKED`. The
   round located a same-version compiler bundle locally, built the contract
   (`OROCHI_FACTORY_ORDER.v1` + CAPC prompt contract) and ran all four gates for real.
4. **Typed admission then board.** HGK typed admission was executed (5 WorkOrders), and the round's
   KANBAN board was created with a card per gate; each card was closed with its evidence string and
   structured metadata rather than a bare "done".
5. **Writer on the mandated EXECUTE arm.** The two-file documentation repair was dispatched to the
   Codex CLI EXECUTE lane with `--require-arm opencode-go/deepseek-v4.1-flash`; the receipt records the
   served rank and model.
6. **Measurement, not quotation.** The release was verified by downloading the served bytes and
   recomputing sha256 locally, and the archive was opened member-by-member. The challenge report could
   not do this (its container had no DNS).
7. **Self-check that can fail.** A detector with paired mutations was built: each check has a mutation
   that must make exactly that check fire, and the run reports both.
8. **Independent checker on the other model axis.** The VERIFY_SECURITY lane was pinned to
   `openai-codex/gpt-6.1-sol` with `--require-arm` and `--force-rank 2`, because the pool's rank-1 is the
   writer's own model. The lane receipt records required vs served.
9. **Every count derived.** The evidence pack is produced by a generator that reads the artefacts on
   disk; no count in it is typed by hand.
