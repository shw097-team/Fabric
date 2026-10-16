"""Freeze THIS round's subject: the canonical change (both states) plus the evidence the claims rest on.

Different from the previous round's freeze, deliberately. There, the subject WAS the candidate tree. Here
the candidate tree holds only the bounded writer's output for one item; the round's substance is a change to
the canonical configuration and to four canonical product files, plus the receipts that carry the numbers.
So the frozen subject is:

  A. the canonical change, both states   — the config pair and the four product files, before and after
  B. the round's own instruments/results — root-level documents, the evidence sub-tree, the lane receipts

Excluded, and why: `candidate/` (it is a live writer workspace during the round), `frozen/` (derived from
A), and the compacted 114 MB enumeration (already replaced by its summary).

A checker MUST recompute the aggregate from the tree before any verdict; a mismatch means it is judging
something other than what this round claims about.
"""
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
SUF = '.bak-far-remediation-20261016'
CONFIG = ['config/lane-routing-registry.yaml', 'config/model-lane-assignment.json']
PRODUCT = ['scripts/runtime_role_binding_assert.py', 'scripts/hgk-governed-runtime-controller.py',
           'tests/test_governed_runtime_controller.py', 'tests/test_lane_effort_enforcement.py']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def entry(label, p):
    p = pathlib.Path(p)
    return {'label': label, 'path': str(p).replace('\\', '/'), 'exists': p.is_file(),
            'bytes': p.stat().st_size if p.is_file() else None,
            'sha256': sha(p) if p.is_file() else None}


items = []
for rel in CONFIG:
    items.append(entry('config.after', R / rel))
    items.append(entry('config.before', R / (rel + SUF)))
for rel in PRODUCT:
    items.append(entry('product.after', R / rel))
    items.append(entry('product.before', R / (rel + SUF)))

docs = 0
SELF_REF = {'FROZEN_MANIFEST.json', 'GATE_REPORT.json'}
for p in sorted(O.iterdir()):
    # The round's OWN helper scripts (*.py) are deliberately NOT in the frozen set. The freeze is the
    # subject the round's CLAIMS rest on, and a helper is edited legitimately between runs -- freezing it
    # only produces a mismatch alarm about the orchestrator's own apparatus. Tooling integrity is covered
    # by the PACKET manifest, which hashes every published file. Stated here, not applied silently.
    #
    # SELF_REF closes a defect an independent checker found by RECOMPUTING the aggregate: the manifest was
    # hashing ITSELF, so the digest recorded for FROZEN_MANIFEST.json could only ever be the PREVIOUS
    # revision's bytes -- the manifest could never verify (measured: expected 18015 bytes / 5d51820b vs
    # actual 18180 / 48d91dc8, the sole mismatching item). GATE_REPORT.json is the same class one step
    # removed: the gate REWRITES it on every run, and the gate is also what verifies this manifest, so
    # freezing it makes the pair mutually unverifiable. Both are still published and hashed by the packet
    # manifest; they are excluded from the aggregate this file computes about ITSELF.
    if p.is_file() and p.name not in SELF_REF and p.suffix.lower() in ('.md', '.json', '.txt'):
        items.append(entry('round_document', p))
        docs += 1
for p in sorted((O / 'evidence').rglob('*')):
    if p.is_file():
        items.append(entry('evidence', p))
LANE_RECEIPTS = list((O / 'lanes').glob('*/*/*'))
# The runner sets the checker's cwd to its lane's work/ dir, so the lane's own verdict lands at
# lanes/<role>/<tag>/work/<file>. Include those top-level files (never the reference copy under work/).
LANE_RECEIPTS += [p for p in (O / 'lanes').glob('*/*/work/*') if 'subject' not in p.parts]
for p in sorted(LANE_RECEIPTS):
    if p.is_file() and p.stat().st_size < 4_000_000:
        items.append(entry('lane_receipt', p))

agg = hashlib.sha256()
for it in items:
    agg.update(('%s|%s|%s\n' % (it['label'], it['path'], it['sha256'])).encode('utf-8'))

REV = int(sys.argv[2]) if len(sys.argv) > 2 else 1
PREV = ('frozen/FROZEN_MANIFEST.rev%d.SUPERSEDED.json' % (REV - 1)) if REV > 1 else None

manifest = {
    'schema': 'HGK-FROZEN-SUBJECT-MANIFEST/2',
    'round': O.name,
    'revision': REV,
    # The frozen set deliberately INCLUDES the derived closure document, so a legitimate regeneration of
    # that document invalidates the manifest. The remedy is to freeze LAST, immediately before it is
    # consumed, and to keep every earlier revision: the chain is then auditable instead of looking like
    # tampering. Revision 1 was taken before the checker's first verdict and before the round's helper
    # scripts settled, which is exactly the staleness the first checker correctly refused on.
    'supersedes': PREV,
    'freeze_policy': 'freeze last, before each consumption; retain every revision',
    'frozen_utc': datetime.now(timezone.utc).isoformat(),
    'subject_definition': ('the canonical change in both states (config pair, four product files) plus the '
                           'round documents, the evidence sub-tree and the lane receipts'),
    'excluded': ['candidate/ (live writer workspace)', 'frozen/ (derived from A)',
                 'the compacted per-file enumeration (replaced by its summary)',
                 'subject/ (the VERIFY lane reference tree: a byte-identical copy of the repository, '
                 'digested in SUBJECT_TREE_DIGEST.json and excluded from the packet)',
                 "the round's own helper scripts (*.py at the round root): edited legitimately between "
                 'runs, their integrity asserted by the packet manifest rather than by this freeze',
                 'FROZEN_MANIFEST.json and GATE_REPORT.json: SELF-REFERENCE. A manifest cannot bind its own '
                 'bytes (it would only ever record the previous revision) and the gate rewrites its own '
                 'report on every run while also being what verifies this file, which makes the pair '
                 'mutually unverifiable. Both are published and hashed by the packet manifest instead'],
    'item_count': len(items),
    'round_document_count': docs,
    'aggregate_sha256': agg.hexdigest(),
    'items': items,
    'how_to_recheck': ('recompute sha256 per item and the aggregate over "label|path|sha256\\n" in the '
                       'recorded order; a mismatch means the subject moved after the freeze'),
    'claim_ceiling': ('The frozen subject, nothing more. Freezing is not accepting; the checker\'s verdict '
                      'remains advisory and hgk_canonical_acceptance stays NOT_PERFORMED.'),
}
(O / 'FROZEN_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'manifest': str(O / 'FROZEN_MANIFEST.json'), 'items': len(items),
                  'round_documents': docs, 'aggregate_sha256': agg.hexdigest(),
                  'config_after': [i['sha256'][:16] for i in items if i['label'] == 'config.after'],
                  'product_after': [i['sha256'][:16] for i in items if i['label'] == 'product.after']},
                 ensure_ascii=False, indent=1))
