"""Remedy the two governance gaps this round's apply scripts left, then read the spine back.

What actually happened (recorded rather than smoothed over):
  * attempt 1 of R1/R3 created REQ/TS/WO for R1 and was then ROLLED BACK at the FILE level only -- the
    spine rows survived, so attempt 2 hit 'UNIQUE constraint failed: requirements.requirement_id'.
    The consequence is benign (the WorkOrder for R1 exists, created once by attempt 1) but it was an
    accident, not a design, so it is read back and recorded here.
  * R2's apply script called create_workorder() without ever creating the TaskSpec, so the spine refused
    with ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC. The canonical change had already landed by then, so the
    record and the change were briefly out of step. This creates the missing REQ/TS/WO.

This script changes ONLY spine rows. It touches no product file.
"""
import json
import pathlib
import sqlite3
import subprocess
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
DB = R / 'var/shared-spine/hg-kseos.db'
OWNER = 'hermes-plan-orchestrator'
TAG = 'FAR-REMEDIATION-AND-CLOSURE-20261016'
out = {'db': str(DB), 'existing_before': {}, 'created': [], 'errors': []}


def dump(con):
    res = {}
    for t in ('requirements', 'taskspecs', 'task_specs', 'workorders'):
        try:
            rows = con.execute("select name from sqlite_master where type='table' and name=?", (t,)).fetchone()
            if not rows:
                continue
            cols = [c[1] for c in con.execute('pragma table_info(%s)' % t)]
            idcol = next((c for c in cols if c.endswith('_id')), cols[0])
            res[t] = [dict(zip(cols, r)) for r in
                      con.execute('select * from %s where %s like ?' % (t, idcol), ('%%%s%%' % TAG,))]
        except Exception as exc:
            res[t + '_error'] = str(exc)
    return res


con = sqlite3.connect(DB)
con.row_factory = None
out['existing_before'] = dump(con)

sys.path.insert(0, str(R / 'src'))
from hg_kseos.spine import SharedSpine  # noqa: E402
sp = SharedSpine(DB)
head = subprocess.run(['git', '-C', 'C:/Projects/Agent_Workspace/HG-KSEOS', 'rev-parse', 'HEAD'],
                      capture_output=True, text=True).stdout.strip()

for item in ('R2',):
    req, ts, wo = ('REQ-%s-%s' % (TAG, item), 'TS-%s-%s' % (TAG, item), 'WO-%s-%s' % (TAG, item))
    wording = ('%s of FAR_RULING.md: promote the four product files that the measured candidate-vs-'
               'canonical enumeration identified (PROMOTE set), each byte-identical to the frozen '
               'candidate, with per-file backups and an orchestrator-side oracle re-run. The candidate '
               'config files are stale (revision 19 vs canonical 20/21) and are retained, not promoted.' % item)
    try:
        sp.register_requirement(req, 'owner-order:20261016_104922_d455e7:far-remediation', wording,
                                'ACC-' + req, 'promoted files byte-identical to the frozen candidate + '
                                'orchestrator re-derived oracle', 'applying a ruling is not accepting it',
                                'fail on any promoted file that is not byte-identical', project_id='HGK-P0')
        out['created'].append(req)
    except Exception as exc:
        out['errors'].append('%s register: %s' % (req, exc))
    tok = 'TK-' + req
    try:
        sp.acquire_lease(req, OWNER, tok, 600)
        try:
            sp.transition_requirement(req, 'FROZEN', OWNER, tok, 0, str(O / 'R2_PROMOTION_RECEIPT.json'),
                                      'FRZ-' + req, payload={'ruling': item, 'late': True,
                                                             'why': 'recorded after the change landed; see docstring'})
        finally:
            sp.release_lease(req, OWNER, tok)
    except Exception as exc:
        out['errors'].append('%s freeze: %s' % (req, exc))
    try:
        sp.create_taskspec(ts, req, wording, OWNER, R,
                           {'canonical_product_edit': True, 'writer': OWNER},
                           ['promoted sha256 == frozen candidate sha256',
                            'oracle: tests.test_lane_effort_enforcement + tests.test_governed_runtime_controller'],
                           'R2_PROMOTION_RECEIPT.json + .bak copies on disk')
        out['created'].append(ts)
    except Exception as exc:
        out['errors'].append('%s taskspec: %s' % (ts, exc))
    try:
        sp.create_workorder(wo, ts, OWNER, R, head)
        out['created'].append(wo)
    except Exception as exc:
        out['errors'].append('%s workorder: %s' % (wo, exc))

out['existing_after'] = dump(con)
con.close()

rec_path = O / 'R2_PROMOTION_RECEIPT.json'
rec = json.loads(rec_path.read_text(encoding='utf-8'))
rec['workorder_remedy'] = out
rec_path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding='utf-8')
(O / 'SPINE_STATE_READBACK.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
for t, rows in out['existing_after'].items():
    if isinstance(rows, list):
        print('%-14s %d row(s): %s' % (t, len(rows), [list(r.values())[0] for r in rows]))
print('created:', out['created'])
print('errors:', out['errors'])
