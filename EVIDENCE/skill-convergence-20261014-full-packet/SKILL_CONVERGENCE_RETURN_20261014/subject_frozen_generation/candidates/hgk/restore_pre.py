import os, shutil

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
SRC = os.path.join(ROOT, "scratch", "readonce")
ABSORBED = [
    "skill/references/external-single-md-mandatory-route.md",
    "skill/references/external-acceptance-single-md-closure.md",
    "skill/references/external-submission-gates.md",
    "skill/references/external-challenge-evidence-closure-far.md",
    "skill/references/external-challenge-review-closure.md",
]
for i, rel in enumerate(ABSORBED):
    src = os.path.join(SRC, "src%d.bin" % i)
    dst = os.path.join(ROOT, *rel.split("/"))
    shutil.copyfile(src, dst)
topic = os.path.join(ROOT, "skill", "references", "topics", "external-evidence-closure.md")
if os.path.exists(topic):
    os.remove(topic)
batch = os.path.join(ROOT, "topic_batch_1.json")
if os.path.exists(batch):
    os.remove(batch)
print("restored originals; removed topic + batch (if present)")
