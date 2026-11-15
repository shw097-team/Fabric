# W1 As-Built delta and test results

- parent `FHS_PIPD-LS-PKG_W1_r3.md` @ `936a8bcb62e16cd205ac8e5799e802293916bbb9de6e5ba8260ea3e1dd013cbf` (868,138 B)
- candidate `FHS_PIPD-LS-PKG_W1_r4.md` @ `c7e33e40b0149dd4867eca1fb6a81f981e9100cf27070e7dc7249151b7258f1b` (876,684 B)
- append-only: the parent body is byte-identical up to the appended chapter

## WP states

- `WP-FHS-02` IMPLEMENTED
- `WP-FHS-03` HOLD
- `WP-FHS-04` IMPLEMENTED
- `WP-FHS-05` TESTED
- `WP-FHS-07` IMPLEMENTED
- `WP-FHS-11` NOT_RUN
- `WP-FHS-17` HOLD
- `WP-FHS-20` NOT_RUN

## Tests actually run for this wave's claims

| suite | command | result |
|---|---|---|
| Fabric consumers (merged main + D-24 merge) | `pytest fabric/consumers/tests -q` | 202 passed, 91 subtests |
| SBL ACK gate (merged main) | `pytest tests/test_ack_binding.py tests/test_modes.py -q` | 58 passed |
| SBL ACK gate matrix (8 cases) | `probe.py <case>` | 8/8 as specified, incl. legacy closure and the replay gap |
| GJ02 oracle pair | `gj02_runner.py <checkout>` | RED(0.03, exit 1) / GREEN(0.02, exit 0), same oracle |
| Host store contract | `probe_db.py report --open` | 4 tables + generation/fence/work_id, v99 refused |
| Host runtime suites | repo runner | hermes_state 1,675 passed / gateway 11,917 passed, zero patch-caused failures |
