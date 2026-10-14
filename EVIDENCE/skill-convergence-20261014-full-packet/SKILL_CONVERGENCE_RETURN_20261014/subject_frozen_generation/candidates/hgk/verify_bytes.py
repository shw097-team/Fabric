import hashlib, json, os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
SRC = os.path.join(ROOT, "scratch", "readonce")
TOPIC = os.path.join(ROOT, "skill", "references", "topics", "external-evidence-closure.md")

batch = json.load(open(os.path.join(ROOT, "topic_batch_1.json"), encoding="utf-8"))
t = open(TOPIC, "rb").read()
print("topic file bytes", len(t), "sha", hashlib.sha256(t).hexdigest())
print("batch topic", batch["topic_file"])
ok = True
for i, e in enumerate(batch["absorbed"]):
    seg = t[e["byte_offset"]:e["payload_byte_end"]]
    ref = open(os.path.join(SRC, "src%d.bin" % i), "rb").read()
    match = seg == ref and hashlib.sha256(seg).hexdigest() == e["sha256"] and len(seg) == e["bytes"]
    ok = ok and match
    print(i, e["absorbed_path"], "seg==orig:", seg == ref, "digest_ok:", hashlib.sha256(seg).hexdigest() == e["sha256"])
print("ALL_OK", ok)

print("--- stubs ---")
for e in batch["absorbed"]:
    p = os.path.join(ROOT, *e["stub_path"].split("/"))
    b = open(p, "rb").read()
    print(p, len(b), repr(b.decode("utf-8")))
