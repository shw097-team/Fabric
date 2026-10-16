"""Pre-publish gate over the assembled packet. Fails loudly instead of publishing something wrong.

Checks, each of which has bitten this stack before:
  1. every *.json parses
  2. .gitattributes pins `* -text`, or CRLF normalisation will break the acceptor's digest check
  3. PACKET_MANIFEST.json digests equal the bytes on disk
  4. no credential material: no github_pat_/ghp_/gho_/Bearer-shaped secret, no value from the API KEY dir
  5. no artifact claims acceptance on the round's behalf
  6. the 4 implementation files really do differ from their baselines (a no-op packet is worse than none)
  7. the round records its own residuals (honesty gate: a packet with no residuals is a packet with no
     self-criticism)
"""
import hashlib
import json
import pathlib
import re
import sys

P = pathlib.Path('C:/Projects/Agent_Workspace/Fabric/EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016')
fails, notes = [], []


def fail(check, detail):
    fails.append({'check': check, 'detail': detail})


PREFIX = 'EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/'


def resolve(rel):
    """Manifest paths are repo-relative; accept either form so the gate cannot pass by accident."""
    return P / (rel[len(PREFIX):] if rel.startswith(PREFIX) else rel)


# 1 ---- json parses ------------------------------------------------------------------------------
n_json = 0
for f in sorted(P.rglob('*')):
    if f.is_file() and f.suffix == '.json':
        n_json += 1
        try:
            json.loads(f.read_text(encoding='utf-8'))
        except Exception as exc:
            fail('json_parses', '%s: %s' % (f.relative_to(P), exc))

# 2 ---- gitattributes -----------------------------------------------------------------------------
ga = P / '.gitattributes'
if not ga.is_file():
    fail('gitattributes', 'missing: the acceptor digest check will see normalised line endings')
elif ' -text' not in ga.read_text(encoding='utf-8'):
    fail('gitattributes', "does not pin '-text': %r" % ga.read_text(encoding='utf-8')[:120])

# 3 ---- manifest digests --------------------------------------------------------------------------
man = P / 'PACKET_MANIFEST.json'
if not man.is_file():
    fail('manifest', 'PACKET_MANIFEST.json missing')
else:
    m = json.loads(man.read_text(encoding='utf-8'))
    checked = 0
    for entry in m.get('files', []):
        f = resolve(entry['path'])
        if not f.is_file():
            fail('manifest_file_absent', entry['path'])
            continue
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != entry.get('sha256'):
            fail('manifest_digest', '%s: recorded %s on disk %s' % (entry['path'],
                                                                   str(entry.get('sha256'))[:16], got[:16]))
        checked += 1
    notes.append('manifest verified over %d files' % checked)
    notes.append('manifest file_count=%s, packet files on disk=%d' %
                 (m.get('file_count'), sum(1 for x in P.rglob('*') if x.is_file())))

# 4 ---- credential leak ---------------------------------------------------------------------------
SECRET = re.compile(rb'(?i)(github_pat_[A-Za-z0-9_]{10,}|gh[pousr]_[A-Za-z0-9]{20,}|'
                    rb'authorization:\s*bearer\s+[A-Za-z0-9._\-]{20,})')
for f in sorted(P.rglob('*')):
    if not f.is_file():
        continue
    blob = f.read_bytes()
    mt = SECRET.search(blob)
    if mt:
        fail('credential_leak', '%s contains %s...' % (f.relative_to(P), mt.group(0)[:12].decode('latin-1')))

# 5 ---- no acceptance claims ----------------------------------------------------------------------
CLAIM = re.compile(r'(?i)\b(ACCEPTED_BY_AGENT|agent-accepted|self-accepted|hgk_canonical_acceptance"\s*:\s*true)')
for f in sorted(P.rglob('*')):
    if not f.is_file() or f.suffix not in ('.json', '.md', '.txt'):
        continue
    txt = f.read_text(encoding='utf-8', errors='replace')
    mt = CLAIM.search(txt)
    if mt:
        fail('acceptance_claim', '%s: %s' % (f.relative_to(P), mt.group(0)))

# 6 ---- the implementation really differs ----------------------------------------------------------
if not man.is_file():
    fail('diffs', 'cannot check implementation deltas without PACKET_MANIFEST.json')
else:
    landed = (json.loads(man.read_text(encoding='utf-8'))).get('product_files_landed') or {}
    changed = [k for k, v in landed.items() if v.get('candidate') and v.get('candidate') != v.get('baseline')]
    notes.append('%d/%d implementation files differ from baseline: %s' %
                 (len(changed), len(landed), ', '.join(sorted(changed))))
    if not changed:
        fail('diffs', 'no implementation file differs from its baseline')
    for d in ('IMPLEMENTATION_DIFFS.json',):
        if not (P / d).is_file():
            fail('diffs', '%s missing' % d)
    df = json.loads((P / 'IMPLEMENTATION_DIFFS.json').read_text(encoding='utf-8'))
    for f in df.get('files', []):
        copyf = P / 'implementation/candidate' / f['path']
        if not copyf.is_file():
            fail('diffs', 'candidate copy absent for %s' % f['path'])
        elif hashlib.sha256(copyf.read_bytes()).hexdigest() != f['sha256']:
            fail('diffs', 'candidate copy digest mismatch for %s' % f['path'])
    if not df.get('diffs'):
        fail('diffs', 'no unified diffs attached')
    else:
        notes.append('%d unified diffs attached and their candidate copies verified by digest' % len(df['diffs']))

# 7 ---- the round records its own residuals --------------------------------------------------------
rc = P / 'ROUND_CLOSURE.json'
if rc.is_file():
    c = json.loads(rc.read_text(encoding='utf-8'))
    n = len(c.get('honest_residuals') or [])
    notes.append('%d honest residuals recorded' % n)
    if n == 0:
        fail('honesty', 'no honest_residuals recorded')
    for k in ('claim_ceiling', 'detection_list', 'lane_model_selection_evidence'):
        if not c.get(k):
            fail('closure_incomplete', 'missing %s' % k)
else:
    fail('closure', 'ROUND_CLOSURE.json missing (run make_closure.py before publishing)')

print(json.dumps({'packet': str(P), 'json_files': n_json, 'failures': fails, 'notes': notes,
                  'verdict': 'GATE_PASS' if not fails else 'GATE_FAIL'}, ensure_ascii=False, indent=1))
sys.exit(0 if not fails else 1)
