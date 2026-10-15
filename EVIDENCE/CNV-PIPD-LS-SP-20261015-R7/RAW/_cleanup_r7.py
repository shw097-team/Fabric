"""One-shot cleanup of superseded raw probe artifacts (kept in the writer receipt)."""
from pathlib import Path

RAW = Path(__file__).resolve().parent
ROOT = RAW.parent
for name in ("acl_probe.ps1", "acl_probe.stdout.txt", "acl_read_probe.ps1",
             "acl_read_probe.py", "acl_read_probe.stdout.txt", "read_probe.py",
             "isolation_review.stdout.txt"):
    p = RAW / name
    if p.resolve().is_relative_to(ROOT) and p.is_file():
        p.unlink()
        print(f"removed {p}")
pc = RAW / "__pycache__"
if pc.resolve().is_relative_to(ROOT) and pc.is_dir():
    import shutil
    shutil.rmtree(pc)
    print(f"removed {pc}")
iso = RAW / "iso_review"
if iso.resolve().is_relative_to(ROOT) and iso.is_dir():
    import shutil
    shutil.rmtree(iso, ignore_errors=True)
    print(f"removed {iso}")
print("remaining RAW:")
for c in sorted(RAW.iterdir()):
    print(" ", c.name)
