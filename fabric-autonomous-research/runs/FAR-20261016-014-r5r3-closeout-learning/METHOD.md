# Method

1. FAR Gate-1 route bound from the capability matrix (class `RESEARCH_LITERATURE_REPO` ->
   `NATIVE_WITH_SELECTED_ARIS` / `FAR_ROUTE_NATIVE_ARIS`); the PLAN turn was served on the mandated
   GLM-5.3-Flash lane (oneshot session `20261016_132640_b3d9f2`, exit 0), read from the runtime's own
   session store rather than from config.
2. The PLAN decision (D1..D6) was executed item by item; each EXECUTE-NOW ruling was converted into a
   measurement or a bounded local artefact, and each OWNER-READY ruling into a prepared one-action record.
3. Every verdict in the round is bound to a re-runnable command: two builds at a frozen commit, a
   member-by-member archive comparison, a live control-plane probe, a validator run, a push dry-run.
4. Disciplines applied: frozen subject; read-only checker; no release/tag/install/publication; probe defects
   reported as probe defects; a byte-diff used to DELETE hypotheses rather than to support one.
5. Residuals were split into EXECUTED-this-round versus OWNER-READY, and nothing was promoted to an
   acceptance.
