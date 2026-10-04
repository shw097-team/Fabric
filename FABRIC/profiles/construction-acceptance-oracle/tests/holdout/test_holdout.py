# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from subject_binding import bind
r = bind({"subject_digest": "f" * 64, "acceptance_pack_ids": ["stack"]}, "f" * 64, ["stack"])
assert r["ok"]
r2 = bind({"subject_digest": "f" * 64, "acceptance_pack_ids": []}, "f" * 64, ["stack"])
assert not r2["ok"]
print("TESTS_OK")
