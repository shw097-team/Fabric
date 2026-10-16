"""check_drift-driven projection repair for round ROUND3-LANE-REBIND-AND-CLOSURE-20261016.

The re-binding moved the live site; the registry's projections[].bindings[].expected strings are the pinned
agreement, so each one that names a moved value must be re-pinned. They are NEVER guessed: this script asks
check_drift for the exact (path, pointer, expected, actual) set, rewrites only those bindings' expected
values, and re-runs check_drift to prove the agreement holds.

Safety:
  * every binding is a single-line flow mapping `- {pointer: <P>, expected: <V>}`; a line that does not parse
    that way aborts the run (no blind text surgery);
  * each drifting pointer must resolve to exactly ONE binding line, or the run aborts;
  * the number of rewrites must equal the number of drift findings -- a silent extra or a missed one aborts;
  * CRLF is preserved byte-faithfully (preflight as in apply_R1_R2_R3.py);
  * nothing is written without --apply.
"""
import hashlib
import json
import pathlib
import re
import shutil
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
REG = R / 'config/lane-routing-registry.yaml'
STAMP = 'round3-lane-rebind-20261016'
APPLY = '--apply' in sys.argv
sys.path.insert(0, str(R / 'src'))
from hg_kseos import lane_policy as lp  # noqa: E402

rp = str(REG)
reg = lp.load_registry(rp)
findings = lp.check_drift(rp, root=str(R), registry=reg)
drifts = [f for f in findings if f['code'] == 'DRIFT_VALUE']
others = [f for f in findings if f['code'] != 'DRIFT_VALUE']
raw = REG.read_bytes()
text = REG.read_text(encoding='utf-8')
crlf = raw.count(b'\r\n') > 0
assert text.replace('\n', '\r\n').encode('utf-8') == raw, 'PREFLIGHT: newline round-trip is not byte-faithful'

lines = text.split('\n')
LINE_RE = re.compile(r'^(\s*- \{pointer: (?P<ptr>[^,]+), expected: )(?P<val>.*)\}$')
by_pointer = {}
for i, ln in enumerate(lines):
    m = LINE_RE.match(ln.rstrip('\r'))
    if m:
        by_pointer.setdefault(m.group('ptr').strip(), []).append(i)

def render(old_val_text, new):
    """Render the new value the way the old one was written: bare scalar or double-quoted string."""
    quoted = old_val_text.startswith('"')
    if quoted or isinstance(new, str):
        return json.dumps(new, ensure_ascii=False)
    return json.dumps(new, ensure_ascii=False)

rewrites, notes = [], []
for f in drifts:
    ptr = f['pointer']
    hits = by_pointer.get(ptr)
    if not hits or len(hits) != 1:
        raise SystemExit('POINTER NOT UNIQUELY BOUND: %s -> %r' % (ptr, hits))
    i = hits[0]
    m = LINE_RE.match(lines[i].rstrip('\r'))
    old_txt = m.group('val').strip()
    new_line = m.group(1) + render(old_txt, f['actual']) + '}'
    if new_line == lines[i].rstrip('\r'):
        continue
    rewrites.append({'pointer': ptr, 'expected_old': f['expected'], 'expected_new': f['actual'],
                     'line': i + 1})
    lines[i] = new_line + ('\r' if lines[i].endswith('\r') else '')

if len(rewrites) != len(drifts):
    raise SystemExit('REWRITE COUNT %d != DRIFT COUNT %d -- refusing partial repair'
                     % (len(rewrites), len(drifts)))

# the projection's own descriptive note is a declaration-level statement, not a binding, and it still names
# the superseded default arm; move it with the order (it is not drift-checked, so it must be done by hand
# and is therefore done explicitly here).
old_note = ('    note: canonical policy revision 21 (owner order 2026-10-16, round '
            'FAR-REMEDIATION-AND-CLOSURE-20261016). PLAN rank-1 is openai-codex/gpt-6.1-sol (medium, OAuth) '
            'with the owner-chain fallbacks GLM-5.3-Flash then DeepSeek V4.1 Flash; the additional EXECUTE '
            'route is operator-selectable only; VERIFY_SECURITY arm A is openai-codex/gpt-6.1-sol and arm B '
            'is opencode-go/glm-5.3-flash. Supersedes the 2026-10-15 GLM rebind, whose 429 premise was '
            'measured false on 2026-10-16.')
new_note = ('    note: canonical policy revision 22 (owner order 2026-10-16, round '
            'ROUND3-LANE-REBIND-AND-CLOSURE-20261016). PLAN rank-1 is opencode-go/glm-5.3-flash (medium, '
            'OpenCode Go) with the owner-chain fallbacks GPT-6.1-SOL (non-default) then DeepSeek V4.1 Flash; '
            'the additional EXECUTE route is operator-selectable only; VERIFY_SECURITY arm A is '
            'opencode-go/deepseek-v4.1-flash and arm B is openai-codex/gpt-6.1-sol (non-default '
            'operator-selectable). SUPERSEDES the epoch-21 order that put PLAN and VERIFY/SECURITY on '
            'openai-codex/gpt-6.1-sol: the writer and the checker now share one model BY OWNER ORDER, which '
            'is declared as SOD006-C3 rather than hedged.')
body = '\n'.join(lines)
if old_note in body:
    body = body.replace(old_note, new_note, 1)
    notes.append('projection note moved to revision 22 / SOD006-C3')
else:
    notes.append('projection note NOT FOUND VERBATIM (left untouched)')

before = hashlib.sha256(raw).hexdigest()
if APPLY:
    b = pathlib.Path(str(REG) + '.bak-' + STAMP)
    if not b.is_file():
        shutil.copy2(REG, b)
    REG.write_bytes(body.replace('\n', '\r\n').encode('utf-8') if crlf else body.encode('utf-8'))
after = hashlib.sha256(REG.read_bytes()).hexdigest()

print(json.dumps({'schema': 'HGK-ROUND3-PROJECTION-REPAIR/1', 'apply': APPLY,
                  'drift_findings': len(drifts), 'rewrites': len(rewrites),
                  'non_drift_findings': [{'code': x['code'], 'path': x['path']} for x in others],
                  'note_edits': notes, 'sha256_before': before, 'sha256_after': after},
                 ensure_ascii=False, indent=1))
for r in rewrites:
    print('  %-52s line %-4d %s' % (r['pointer'], r['line'],
                                    str(r['expected_old'])[:46].replace('\n', ' ')))

if APPLY:
    (R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016' / 'PROJECTION_REPAIR_RECEIPT.json').write_text(
        json.dumps({'schema': 'HGK-ROUND3-PROJECTION-REPAIR/1', 'round':
                    'ROUND3-LANE-REBIND-AND-CLOSURE-20261016', 'drift_findings': len(drifts),
                    'rewrites': rewrites, 'non_drift_findings': others, 'note_edits': notes,
                    'sha256_before': before, 'sha256_after': after}, ensure_ascii=False, indent=2),
        encoding='utf-8')
    print('\nre-running check_drift to prove the agreement now holds:')
    reg2 = lp.load_registry(rp)
    f2 = lp.check_drift(rp, root=str(R), registry=reg2)
    errs = [x for x in f2 if x.get('severity') == 'error']
    print('  findings=%d errors=%d' % (len(f2), len(errs)))
    for x in errs[:20]:
        print('   STILL:', x['code'], x['pointer'], str(x.get('expected'))[:40], '->', str(x.get('actual'))[:40])
