"""Find the generator of SUBJECT_DIGEST.json / the 'HGK-ROUND3-SUBJECT-DIGEST' schema string."""
import os
from pathlib import Path

ROOTS = [Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"), Path(r"C:\Projects\Agent_Workspace\Fabric")]
NEEDLES = ("HGK-ROUND3-SUBJECT-DIGEST", "76ec42a0f4c8962c", "frozen_after")
SKIP_PARTS = {"subject", "__pycache__", ".git", ".pytest_cache", ".tmp", "plugins", "node_modules"}

hits = 0
for root in ROOTS:
    for dirpath, dirnames, filenames in os.walk(root):
        parts = set(Path(dirpath).parts)
        if parts & SKIP_PARTS:
            dirnames[:] = []
            continue
        for fn in filenames:
            if not fn.endswith((".py", ".json", ".md", ".txt", ".ps1")):
                continue
            fp = Path(dirpath) / fn
            try:
                t = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for n in NEEDLES:
                if n in t:
                    print(n, "::", fp)
                    hits += 1
print("hits", hits)
