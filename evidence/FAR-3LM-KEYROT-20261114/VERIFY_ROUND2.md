R3 PASS — `ops/rotate_3lm_key.py:54`, `ops/rotate_3lm_key.py:57`, `ops/rotate_3lm_key.py:60`, `ops/rotate_3lm_key.py:62`, `ops/rotate_3lm_key.py:70`, `ops/rotate_3lm_key.py:86`, `ops/rotate_3lm_key.py:109`, `ops/rotate_3lm_key.py:132`, `ops/rotate_3lm_key.py:220`; exit codes 2-10 are unique and reachable. Manifest parse failures are typed `MANIFEST_INVALID` at `ops/rotate_3lm_key.py:74`.

R4 PASS — `ops/rotate_3lm_key.py:203` plan, `ops/rotate_3lm_key.py:214` backup, `ops/rotate_3lm_key.py:217` probe, `ops/rotate_3lm_key.py:229` apply. Probe failure returns at `ops/rotate_3lm_key.py:223` before apply, with a receipt at `ops/rotate_3lm_key.py:220` and `mutated: false` at `ops/rotate_3lm_key.py:221`.

R6 PASS — `RUNBOOKS/3LM_KEY_ROTATION.md:6` states dry-run plus read-only `--pin-refresh` were executed and no `--apply` has run against a new credential.

R1 PASS — `ops/rotate_3lm_key.py:142` stores `stdout_sha12`, `ops/rotate_3lm_key.py:143` stores `stderr_len`, and `ops/rotate_3lm_key.py:144` sets `raw_output_stored: false`; the pin path persists only the parsed version token at `ops/rotate_3lm_key.py:172`.

CLAIM_CEILING=LOCAL_CHECK_ONLY
