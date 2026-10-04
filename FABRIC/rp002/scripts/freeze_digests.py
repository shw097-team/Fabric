# -*- coding: utf-8 -*-
import hashlib, os, json
def dir_tree_digest(root):
    rows = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ('.git', '__pycache__')]
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, '/')
            rows.append((rel, os.path.getsize(p), hashlib.sha256(open(p, 'rb').read()).hexdigest()))
    rows.sort()
    h = hashlib.sha256()
    for r, s, dig in rows:
        h.update(("{}\t{}\t{}\n".format(r, s, dig)).encode('utf-8'))
    return h.hexdigest(), len(rows)

kp = r"C:\Projects\Agent_Workspace\Fabric\Oracle\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack"
comp = r"C:\Projects\Agent_Workspace\Fabric\Oracle\工程基座\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler_SKILL.md"
d, n = dir_tree_digest(kp)
print("KPACK_DIR_DIGEST", d, "files", n)
c = hashlib.sha256(open(comp, 'rb').read()).hexdigest()
print("COMPILER_SKILL_MD", c, os.path.getsize(comp))
