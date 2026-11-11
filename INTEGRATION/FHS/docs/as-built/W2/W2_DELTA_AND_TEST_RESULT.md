# W2 As-Built delta and test results

- parent `FHS_PIPD-LS-PKG_W2_r5.md` @ `647ee5598d6344f4c7540974d67182a55b0205a8e25bb46b8cc08c97ee206729` (430,128 B)
- candidate `FHS_PIPD-LS-PKG_W2_r6.md` @ `a325e2a3d59de1b69e0b16ee5e66b75e7e4c80501bf12bdffbf464c88c69770a` (435,780 B)
- append-only: the parent body is byte-identical up to the appended chapter

## WP states

- `WP-FHS-06` HOLD
- `WP-FHS-08` NOT_RUN
- `WP-FHS-09` NOT_RUN
- `WP-FHS-18` NOT_RUN

## Tests actually run for this wave's claims

| suite | command | result |
|---|---|---|
| Fabric consumers (merged main + D-24 merge) | `pytest fabric/consumers/tests -q` | 202 passed, 91 subtests |
| SBL ACK gate (merged main) | `pytest tests/test_ack_binding.py tests/test_modes.py -q` | 58 passed |
| SBL ACK gate matrix (8 cases) | `probe.py <case>` | 8/8 as specified, incl. legacy closure and the replay gap |
| GJ02 oracle pair | `gj02_runner.py <checkout>` | RED(0.03, exit 1) / GREEN(0.02, exit 0), same oracle |
| Host store contract | `probe_db.py report --open` | 4 tables + generation/fence/work_id, v99 refused |
| Host runtime suites | repo runner | hermes_state 1,675 passed / gateway 11,917 passed, zero patch-caused failures |
