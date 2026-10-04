# -*- coding: utf-8 -*-
"""Subject binding validator: receipt must bind exact subject digest + pack ids."""
import json, sys
def bind(receipt: dict, subject_digest: str, pack_ids: list[str]) -> dict:
    errs = []
    if receipt.get("subject_digest") != subject_digest:
        errs.append("SUBJECT_MISMATCH")
    missing = [p for p in pack_ids if p not in receipt.get("acceptance_pack_ids", [])]
    if missing:
        errs.append(f"MISSING_PACKS:{missing}")
    return {"ok": not errs, "errors": errs}
if __name__ == "__main__":
    good = {"subject_digest": "d" * 64, "acceptance_pack_ids": ["hermes-runtime", "kanban"]}
    bad = {"subject_digest": "e" * 64, "acceptance_pack_ids": []}
    r1 = bind(good, "d" * 64, ["hermes-runtime"])
    r2 = bind(bad, "d" * 64, ["hermes-runtime"])
    ok = r1["ok"] and not r2["ok"]
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", json.dumps({"good": r1, "bad": r2}))
    sys.exit(0 if ok else 1)
