# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from oracle_preflight import validate
bad = {"verdict": "PASS"}
assert not validate(bad)["ok"] and "MISSING:oracle_id" in validate(bad)["errors"]
print("TESTS_OK")
