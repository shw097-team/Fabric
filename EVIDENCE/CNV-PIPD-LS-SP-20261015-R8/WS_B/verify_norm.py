"""Normalized-equivalence check: R8_0_DERIVED_FROM_R7.patch vs R7/R7_VALIDATOR_DIFF.patch.
Strips git 'index'/'diff --git' headers and the a//b prefixes so only the semantic hunks compare."""
import hashlib


def norm(p):
    out = []
    for ln in open(p, encoding="utf-8").read().splitlines():
        if ln.startswith("index ") or ln.startswith("diff --git"):
            continue
        if ln.startswith("--- "):
            ln = "--- a"
        if ln.startswith("+++ "):
            ln = "+++ b"
        out.append(ln)
    return "\n".join(out)


a = norm("R8_0_DERIVED_FROM_R7.patch")
b = norm("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_VALIDATOR_DIFF.patch")
print("normalized_equal:", a == b)
print("sha256(derived):", hashlib.sha256(a.encode()).hexdigest())
print("sha256(r7):     ", hashlib.sha256(b.encode()).hexdigest())
print("lines:", len(a.splitlines()), len(b.splitlines()))
