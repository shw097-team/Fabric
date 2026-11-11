# W0 As-Built delta and test results

- parent `FHS_PIPD-LS-PKG_W0_r5.md` @ `60b0c36e1bde6d0be1127461aa87a6bbb91dd69d6a31875d216ad8ddc88dbf0b` (475,265 B)
- candidate `FHS_PIPD-LS-PKG_W0_r6.md` @ `69a08e7fae0404d7fc33842d66c28a21684a6d13caa6ac40ba7a269411db28d5` (481,212 B)
- append-only: the parent body is byte-identical up to the appended chapter

## WP states

- `WP-FHS-00` TESTED
- `WP-FHS-01` NOT_RUN
- `WP-FHS-15` NOT_RUN
- `WP-FHS-16` NOT_RUN
- `WP-FHS-19` TESTED
- `WP-FHS-21` TESTED

## Tests actually run for this wave's claims

| suite | command | result |
|---|---|---|
| Fabric consumers (merged main + D-24 merge) | `pytest fabric/consumers/tests -q` | 202 passed, 91 subtests |
| SBL ACK gate (merged main) | `pytest tests/test_ack_binding.py tests/test_modes.py -q` | 58 passed |
| SBL ACK gate matrix (8 cases) | `probe.py <case>` | 8/8 as specified, incl. legacy closure and the replay gap |
| GJ02 oracle pair | `gj02_runner.py <checkout>` | RED(0.03, exit 1) / GREEN(0.02, exit 0), same oracle |
| Host store contract | `probe_db.py report --open` | 4 tables + generation/fence/work_id, v99 refused |
| Host runtime suites | repo runner | hermes_state 1,675 passed / gateway 11,917 passed, zero patch-caused failures |
