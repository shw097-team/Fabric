# -*- coding: utf-8 -*-
"""Oracle preflight validator: receipt schema + required fields + verdict enum."""
import json, sys, hashlib
def validate(receipt: dict) -> dict:
    errs = []
    for k in ("oracle_id", "oracle_package_digest", "subject_digest", "acceptance_oracle_digest", "verdict"):
        if k not in receipt:
            errs.append(f"MISSING:{k}")
    if receipt.get("verdict") not in ("PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"):
        errs.append(f"BAD_VERDICT:{receipt.get('verdict')}")
    for k in ("oracle_package_digest", "subject_digest", "acceptance_oracle_digest"):
        v = receipt.get(k, "")
        if v and (len(v) != 64 or any(c not in "0123456789abcdef" for c in v)):
            errs.append(f"BAD_DIGEST:{k}")
    return {"ok": not errs, "errors": errs}
if __name__ == "__main__":
    good = {"oracle_id": "CONSTRUCTION_ACCEPTANCE_ORACLE", "oracle_package_digest": "a" * 64,
            "subject_digest": "b" * 64, "acceptance_oracle_digest": "c" * 64, "verdict": "PASS"}
    bad = {"verdict": "SELF_APPROVED"}
    r1, r2 = validate(good), validate(bad)
    ok = r1["ok"] and not r2["ok"] and "MISSING:oracle_id" in r2["errors"]
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", json.dumps({"good": r1, "bad": r2}))
    sys.exit(0 if ok else 1)
