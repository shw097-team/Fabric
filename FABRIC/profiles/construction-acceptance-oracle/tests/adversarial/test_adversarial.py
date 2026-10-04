# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from evidence_readback import verify_critical_write
import tempfile, os
d = tempfile.mkdtemp(prefix="oracle-adv-")
p = os.path.join(d, "p.txt")
open(p, "wb").write(b"ok\n...[truncated]")
try:
    verify_critical_write(p)
    raise SystemExit("SENTINEL_NOT_DETECTED")
except RuntimeError:
    pass
print("TESTS_OK")
