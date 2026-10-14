import hashlib, json, os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"


def rsha(rel):
    return hashlib.sha256(open(os.path.join(ROOT, *rel.split("/")), "rb").read()).hexdigest()


print("SKILL.md sha:", rsha("skill/SKILL.md"), "(read-phase sha 60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960)")
print("entry_map.json sha:", rsha("entry_map.json"))
print("existing topic sha:", rsha("skill/references/topics/construction-wave-and-remaining-procedures.md"))

t = open(os.path.join(ROOT, "skill", "references", "topics", "external-evidence-closure.md"), "rb").read()
print("--- envelope headers only ---")
for ln in t.split(b"\n"):
    if ln.startswith(b"<!-- SKCV-TOPIC-ENTRY"):
        print(ln.decode())

print("--- my deliverables present ---")
for rel in ["skill/references/topics/external-evidence-closure.md", "topic_batch_1.json",
            "topic_check.py", "phase2_result.json"]:
    p = os.path.join(ROOT, *rel.split("/"))
    print(os.path.isfile(p), rel)

print("--- underscored/hidden in my deliverable dirs ---")
for rel in ["skill/references/topics", "."]:
    d = os.path.join(ROOT, *rel.split("/")) if rel != "." else ROOT
    for n in sorted(os.listdir(d)):
        if n.startswith(".") or n.startswith("_"):
            print("  HIDDEN/UNDERSCORE:", rel, n)
print("done")
