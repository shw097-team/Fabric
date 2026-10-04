# -*- coding: utf-8 -*-
"""Evidence readback validator: raw byte readback + sha256 + truncation sentinel scan."""
import hashlib, sys
SENTINEL = b"...[truncated]"
def verify_critical_write(path: str) -> dict:
    raw = open(path, "rb").read()
    if SENTINEL in raw:
        raise RuntimeError(f"ERR_LITERAL_TRUNCATION_SENTINEL:{path}")
    return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
if __name__ == "__main__":
    import tempfile, os
    d = tempfile.mkdtemp(prefix="oracle-rb-")
    p = os.path.join(d, "probe.txt")
    open(p, "wb").write(b"good\n" * 3)
    r = verify_critical_write(p)
    poison = os.path.join(d, "poison.txt")
    open(poison, "wb").write(b"x\n...[truncated]\n")
    try:
        verify_critical_write(poison)
        ok = False
    except RuntimeError as exc:
        ok = "ERR_LITERAL_TRUNCATION_SENTINEL" in str(exc)
    ok = ok and len(r["sha256"]) == 64 and r["bytes"] == 15
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", r)
    sys.exit(0 if ok else 1)
