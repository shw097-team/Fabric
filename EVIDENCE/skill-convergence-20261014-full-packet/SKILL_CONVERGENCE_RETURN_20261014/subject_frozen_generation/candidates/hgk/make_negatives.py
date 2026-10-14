import os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
TOPIC = os.path.join(ROOT, "skill", "references", "topics", "external-evidence-closure.md")
NEG = os.path.join(ROOT, "scratch", "negatives")
os.makedirs(NEG, exist_ok=True)

topic = open(TOPIC, "rb").read()

import re
HDR = re.compile(rb"<!-- SKCV-TOPIC-ENTRY path=(\S+) offset=(\d+) length=(\d+) sha256=[0-9a-f]{64} -->\n")
blocks = []
for m in HDR.finditer(topic):
    start = m.start()
    phys = m.end()
    length = int(m.group(3))
    blocks.append((start, phys + length, m.group(1).decode("utf-8")))

# missing: drop block index 2 (external-submission-gates)
keep = topic[:blocks[2][0]] + topic[blocks[2][1]:]
open(os.path.join(NEG, "missing.md"), "wb").write(keep)

# duplicated: append a copy of block index 0
dup = topic + topic[blocks[0][0]:blocks[0][1]]
open(os.path.join(NEG, "duplicated.md"), "wb").write(dup)

# reordered: swap block 0 and block 1
reord = (topic[blocks[1][0]:blocks[1][1]] + topic[blocks[0][0]:blocks[0][1]]
         + topic[blocks[2][0]:])
open(os.path.join(NEG, "reordered.md"), "wb").write(reord)

# mutated: flip one payload byte inside block 0 (payload starts after its header)
p0 = blocks[0][1] - 5  # a byte inside block0 payload (len 2546)
m0 = bytearray(topic)
m0[p0] = (m0[p0] + 1) % 256
open(os.path.join(NEG, "mutated.md"), "wb").write(bytes(m0))

print("wrote negatives; blocks:", [(p, s, e) for (s, e, p) in blocks])
