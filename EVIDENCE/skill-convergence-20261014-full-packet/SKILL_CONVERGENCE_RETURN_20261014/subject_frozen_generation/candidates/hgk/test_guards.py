import io, json, os, shutil, sys, contextlib

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
sys.path.insert(0, ROOT)
import topic_check as tc

SANDBOX = os.path.join(ROOT, "scratch", "sandbox")


def fresh():
    if os.path.exists(SANDBOX):
        shutil.rmtree(SANDBOX)
    os.makedirs(os.path.join(SANDBOX, "skill", "references", "topics"))
    # batch + topic
    shutil.copyfile(os.path.join(ROOT, "topic_batch_1.json"),
                    os.path.join(SANDBOX, "topic_batch_1.json"))
    shutil.copyfile(os.path.join(ROOT, "skill", "references", "topics", "external-evidence-closure.md"),
                    os.path.join(SANDBOX, "skill", "references", "topics", "external-evidence-closure.md"))
    # skill + all referenced names must resolve -> copy skill dir files referenced
    shutil.copyfile(os.path.join(ROOT, "skill", "SKILL.md"),
                    os.path.join(SANDBOX, "skill", "SKILL.md"))
    shutil.copyfile(os.path.join(ROOT, "entry_map.json"),
                    os.path.join(SANDBOX, "entry_map.json"))
    refnames = [
        "FDA_ROUTE_REGISTRY.json", "capc-contract-building.md", "cross-session-integrity.md",
        "daytrading-t0-axis-authoritative-chain.md", "fda_guard_hook.py", "fda_guard_mint.py",
        "final-closure-resume.md", "order-completion-audit.md", "self-verifying-probe-authoring.md",
        "sqs-data-plane-verification.md",
    ]
    for n in refnames:
        shutil.copyfile(os.path.join(ROOT, "skill", "references", n),
                        os.path.join(SANDBOX, "skill", "references", n))
    shutil.copyfile(os.path.join(ROOT, "skill", "references", "topics", "construction-wave-and-remaining-procedures.md"),
                    os.path.join(SANDBOX, "skill", "references", "topics", "construction-wave-and-remaining-procedures.md"))
    # stubs
    batch = json.load(open(os.path.join(ROOT, "topic_batch_1.json"), encoding="utf-8"))
    for e in batch["absorbed"]:
        shutil.copyfile(os.path.join(ROOT, *e["stub_path"].split("/")),
                        os.path.join(SANDBOX, *e["stub_path"].split("/")))
    return batch


def call(root):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            tc.run(root=root)
        return ("OK", 0, buf.getvalue())
    except tc.Refusal as r:
        return (r.code, r.exit_code, r.detail)


batch = fresh()

print("sandbox GOOD:", call(SANDBOX))

# stub mismatch: overwrite one stub so its offset is wrong
sp = os.path.join(SANDBOX, *batch["absorbed"][1]["stub_path"].split("/"))
with open(sp, "w", encoding="utf-8") as f:
    f.write("SKCV-POINTER external-evidence-closure: payload moved verbatim to "
            "skill/references/topics/external-evidence-closure.md byte offset 999999 "
            "length 0 sha256 %s; do not reconstruct.\n" % ("0" * 64))
print("sandbox BAD stub:", call(SANDBOX))

# stub missing
fresh()
sp = os.path.join(SANDBOX, *batch["absorbed"][3]["stub_path"].split("/"))
os.remove(sp)
print("sandbox MISSING stub:", call(SANDBOX))

# name unresolved: point a referenced token at a nonexistent file
fresh()
skp = os.path.join(SANDBOX, "skill", "SKILL.md")
txt = open(skp, "rb").read().decode("utf-8", "surrogateescape")
txt2 = txt.replace("references/order-completion-audit.md", "references/DOES-NOT-EXIST.md")
open(skp, "wb").write(txt2.encode("utf-8", "surrogateescape"))
print("sandbox UNRESOLVED name:", call(SANDBOX))
