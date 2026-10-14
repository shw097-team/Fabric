import os

ROOT = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\SKILL-CONVERGENCE-20261014\candidates\hgk"
d = os.path.join(ROOT, "skill", "references")

top = []
rec = []
for base, dirs, files in os.walk(d):
    for fn in files:
        p = os.path.join(base, fn)
        rec.append(os.path.relpath(p, d).replace("\\", "/"))
        if base == d:
            top.append(fn)

print("recursive files under skill/references =", len(rec))
print("top-level files directly in skill/references =", len(top))
print("subdirs:", sorted(n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n))))
print("topics files:", sorted(f for f in os.listdir(os.path.join(d, "topics"))))
