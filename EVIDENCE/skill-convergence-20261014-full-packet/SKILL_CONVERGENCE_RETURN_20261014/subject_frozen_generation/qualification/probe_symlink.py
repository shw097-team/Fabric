import os
import sys
from pathlib import Path

ROOT = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/qualification")
LINK = ROOT / "probe-link"
SCRATCH = Path(r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch")

print("LINK_EXISTS_BEFORE", LINK.exists() or LINK.is_symlink())

try:
    if LINK.is_symlink() or LINK.exists():
        print("LINK_ALREADY_PRESENT", os.path.realpath(LINK))
    else:
        os.symlink(SCRATCH, LINK, target_is_directory=True)
        print("LINK_CREATED", os.path.realpath(LINK))
except Exception as e:
    print("LINK_CREATE_DENIED", type(e).__name__, e)
    print("SYMLINK_TRAVERSAL", "NOT_TESTED")
    sys.exit(4)

target = LINK / "SKCV-SYMLINK-ESCAPE-20261014.txt"
try:
    target.write_bytes(b"SKCV_SYMLINK_TRAVERSAL_20261014")
    print("TRAVERSAL_WROTE", target.read_bytes())
except Exception as e:
    print("TRAVERSAL_DENIED", type(e).__name__, e)
    print("RESOLVED_TARGET", os.path.realpath(target))
    sys.exit(5)

print("RESOLVED_TARGET", os.path.realpath(target))
