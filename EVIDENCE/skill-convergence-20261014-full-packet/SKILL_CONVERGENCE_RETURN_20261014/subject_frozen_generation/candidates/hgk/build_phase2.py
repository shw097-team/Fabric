import hashlib, json, os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
SRC = os.path.join(ROOT, "scratch", "readonce")

THEME = "external-evidence-closure"
TOPIC_REL = "skill/references/topics/%s.md" % THEME

ABSORBED = [
    "skill/references/external-single-md-mandatory-route.md",
    "skill/references/external-acceptance-single-md-closure.md",
    "skill/references/external-submission-gates.md",
    "skill/references/external-challenge-evidence-closure-far.md",
    "skill/references/external-challenge-review-closure.md",
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def header(path, offset, length, digest):
    return ("<!-- SKCV-TOPIC-ENTRY path=%s offset=%d length=%d sha256=%s -->\n"
            % (path, offset, length, digest))


def count_refs():
    d = os.path.join(ROOT, "skill", "references")
    top = 0
    for name in os.listdir(d):
        if os.path.isfile(os.path.join(d, name)):
            top += 1
    rec = 0
    for base, _dirs, files in os.walk(d):
        rec += len(files)
    return top, rec


before_top, before_rec = count_refs()
print("BEFORE top-level files in skill/references = %d ; recursive = %d" % (before_top, before_rec))

payloads = []
for i in range(len(ABSORBED)):
    with open(os.path.join(SRC, "src%d.bin" % i), "rb") as f:
        payloads.append(f.read())

parts = []      # bytes already emitted
out = bytearray()
entries = []

for path, pay in zip(ABSORBED, payloads):
    digest = sha(pay)
    length = len(pay)
    # fixpoint: offset depends on header length which depends on offset digits
    offset = len(out)
    while True:
        h = header(path, offset, length, digest)
        new_off = len(out) + len(h)
        if new_off == offset:
            break
        offset = new_off
    h = header(path, offset, length, digest)
    out += h.encode("utf-8")
    out += pay
    entries.append({
        "absorbed_path": path,
        "bytes": length,
        "sha256": digest,
        "byte_offset": offset,
        "payload_byte_end": offset + length,
        "stub_path": path,
    })

topic_bytes = bytes(out)

# write topic file
tp = os.path.join(ROOT, *TOPIC_REL.split("/"))
os.makedirs(os.path.dirname(tp), exist_ok=True)
with open(tp, "wb") as f:
    f.write(topic_bytes)

# write one-line pointer stubs at each original path
for e in entries:
    stub = ("SKCV-POINTER %s: payload moved verbatim to %s byte offset %d length %d sha256 %s; "
            "do not reconstruct.\n" % (THEME, TOPIC_REL, e["byte_offset"], e["bytes"], e["sha256"]))
    sp = os.path.join(ROOT, *e["stub_path"].split("/"))
    with open(sp, "wb") as f:
        f.write(stub.encode("utf-8"))

# topic_batch_1.json
batch = {
    "schema": "SKCV-HGK-TOPIC-BATCH/1",
    "theme": THEME,
    "topic_file": {
        "path": TOPIC_REL,
        "bytes": len(topic_bytes),
        "sha256": sha(topic_bytes),
    },
    "absorbed": entries,
}
with open(os.path.join(ROOT, "topic_batch_1.json"), "w", encoding="utf-8") as f:
    json.dump(batch, f, indent=2)
    f.write("\n")

after_top, after_rec = count_refs()
print("AFTER  top-level files in skill/references = %d ; recursive = %d" % (after_top, after_rec))

print("before_refs(top,rec)=%s after_refs(top,rec)=%s" % ((before_top, before_rec), (after_top, after_rec)))
print("topic_bytes=%d topic_sha=%s" % (len(topic_bytes), sha(topic_bytes)))
for e in entries:
    print("  %s off=%d len=%d" % (e["absorbed_path"], e["byte_offset"], e["bytes"]))
