# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from oracle_preflight import validate
good = {"oracle_id": "O", "oracle_package_digest": "a" * 64, "subject_digest": "b" * 64,
        "acceptance_oracle_digest": "c" * 64, "verdict": "PASS"}
assert validate(good)["ok"]
print("TESTS_OK")
