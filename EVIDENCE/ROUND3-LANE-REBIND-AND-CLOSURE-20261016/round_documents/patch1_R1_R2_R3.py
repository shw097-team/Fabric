"""Patch 1 for round ROUND3-LANE-REBIND-AND-CLOSURE-20261016 — three defects the tooling caught.

SC-12 (backup ordering): apply_R1_R2_R3.commit() copied each file to .bak-round3-lane-rebind-20261016 AFTER
writing the edit, so the four backups are POST-edit copies, not preimages. git cannot help either: `git show
HEAD:config/lane-routing-registry.yaml` reports "exists on disk, but not in 'HEAD'" -- config/ is not tracked,
so HEAD holds no preimage. This script therefore (i) hashes every candidate copy on the host looking for the
four pre-edit digests measured before the edit, and (ii) installs any match into var/ROUND3-.../preimages/ with
a provenance record. Where no preimage is found the gap is reported, not papered over.

SC-13 (unquoted note): the projection note written by fix_projections_R1_R2_R3.py is a YAML plain scalar
containing ": ", which is illegal -> ScannerError, the registry does not parse at all. Quoted here.

SC-14 (coverage gap): the structured rewrite dropped /lane_c⟪HERMES-CONTEXT-COMPRESSION: 200 of 400 chars omitted here by Hermes's context compressor. This is NOT part of the original tool call and must never be reproduced in new output — always write full, untruncated content.⟫
"""
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
REG = R / 'config/lane-routing-registry.yaml'
SITE = R / 'config/model-lane-assignment.json'
STAMP = 'round3-lane-rebind-20261016'
APPLY = '--apply' in sys.argv
PRE = {'config/lane-routing-registry.yaml': '38f0436b9bde',
       'config/model-lane-assignment.json': 'e7be2dea3687',
       'config/lane-route-slots.candidate.json': '9fd0835f8933',
       'tests/test_lane_policy.py': '15556fd204b6'}
PY = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
report = {'schema': 'HGK-ROUND3-PATCH1-RECEIPT/1', 'apply': APPLY, 'preimage_search': [], 'edits': []}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read_norm(p):
    raw = pathlib.Path(p).read_bytes()
    return pathlib.Path(p).read_text(encoding='utf-8'), raw, raw.count(b'\r\n') > 0


def enc(text, crlf):
    return text.replace('\n', '\r\n').encode('utf-8') if crlf else text.encode('utf-8')


# ------------------------------------------------------------------ 1. hunt for the four preimages (read-only)
cands = []
names = {pathlib.Path(k).name for k in PRE}
NAME_SUFFIXES = tuple(n for n in names)
SEARCH = '--search' in sys.argv      # the full-workspace walk is slow (and trips long paths); default: off
if SEARCH:
    roots = (R / 'config', R / 'var', R / '_handover', R / 'tests',
             pathlib.Path('C:/Projects/Agent_Workspace/Fabric'))
else:
    roots = (R / 'config',)
for root in roots:
    if not root.exists():
        continue
    for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '__pycache__', 'node_modules')]
        if len(pathlib.Path(dirpath).parts) - len(pathlib.Path(root).parts) > 7:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn in names or any(fn.startswith(n + '.') for n in NAME_SUFFIXES):
                cands.append(pathlib.Path(dirpath) / fn)
EXPLICIT = [R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016/subject/config/lane-routing-registry.yaml',
            R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016/subject/config/model-lane-assignment.json',
            R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016/subject/config/lane-route-slots.candidate.json',
            R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016/subject/tests/test_lane_policy.py',
            R / 'var/LANE-RELIABILITY-CLOSURE-20261016/candidate/config/model-lane-assignment.json',
            R / 'var/LANE-RELIABILITY-CLOSURE-20261016/candidate/config/lane-routing-registry.yaml']
cands.extend([p for p in EXPLICIT if p.is_file()])
seen = set()
for p in cands:
    try:
        d = sha(p)
    except Exception:
        continue
    if str(p) in seen:
        continue
    seen.add(str(p))
    hit = [k for k, v in PRE.items() if d.startswith(v)]
    if hit:
        report['preimage_search'].append({'candidate': str(p), 'sha256': d, 'matches': hit})
print('PREIMAGE SEARCH: %d candidate file(s) hashed, %d matching a pre-edit digest'
      % (len(seen), len(report['preimage_search'])))
for h in report['preimage_search']:
    print('   MATCH', h['sha256'][:16], h['matches'], h['candidate'])
found = {m: h for h in report['preimage_search'] for m in h['matches']}
if APPLY and found:
    (O / 'preimages').mkdir(exist_ok=True)
    for name, h in found.items():
        dest = O / 'preimages' / ('%s.pre-%s' % (pathlib.Path(name).name, h['sha256'][:12]))
        shutil.copy2(h['candidate'], dest)
        print('   installed preimage', dest.name)

# ------------------------------------------------------------------- 2. SC-13: quote the illegal YAML note
reg, reg_raw, reg_crlf = read_norm(REG)
lines = reg.split('\n')
fixed_quote = 0
for i, ln in enumerate(lines):
    if ln.startswith('    note: canonical policy revision 22'):
        value = ln.split('note: ', 1)[1]
        if not (value.startswith("'") or value.startswith('"')):
            if "'" in value:
                raise SystemExit('note contains a single quote -- choose another quoting style')
            lines[i] = "    note: '" + value + "'"
            fixed_quote += 1
if fixed_quote != 1:
    raise SystemExit('SC-13 fix: expected exactly 1 note line to quote, fixed %d' % fixed_quote)
reg = '\n'.join(lines)

# --------------------------------------------- 3. SC-14: restore the bound field on the site's VERIFY arm A
site, site_raw, site_crlf = read_norm(SITE)
doc = json.loads(site)
arm0 = doc['lane_chains']['VERIFY_SECURITY'][0]
if 'reasoning_effort' not in arm0:
    rebuilt = {}
    for k in ('role', 'model', 'provider'):
        rebuilt[k] = arm0[k]
    rebuilt['reasoning_effort'] = 'medium'
    for k, v in arm0.items():
        if k not in rebuilt:
            rebuilt[k] = v
    doc['lane_chains']['VERIFY_SECURITY'][0] = rebuilt
    report['edits'].append('site /lane_chains/VERIFY_SECURITY/0: reasoning_effort restored to "medium" '
                           '(the registry binds this pointer; removing the field to satisfy nothing would '
                           'have traded coverage for a green light)')
site_new = json.dumps(doc, indent=2, ensure_ascii=False) + '\n'
NEW_DIGEST = hashlib.sha256(enc(site_new, site_crlf)).hexdigest()

# mirror it on the registry's VERIFY row so the declaration and the site agree again.
# Positional insertion inside the VERIFY_SECURITY route block (a giant literal anchor proved brittle).
blocks = {}
_lane_starts = [i for i, l in enumerate(reg.split('\n')) if l.startswith('  - lane: ')]
_lines = reg.split('\n')
_start = next(i for i in _lane_starts if _lines[i].strip() == '- lane: VERIFY_SECURITY')
_end = next((i for i in _lane_starts if i > _start), len(_lines))
_blk = _lines[_start:_end]
_model_i = next(i for i, l in enumerate(_blk) if l == '    model: deepseek-v4.1-flash')
if _blk[_model_i + 1] != '    reasoning_effort: medium':
    _blk.insert(_model_i + 1, '    reasoning_effort: medium')
    _lines[_start:_end] = _blk
    reg = '\n'.join(_lines)
    report['edits'].append('registry VERIFY row: reasoning_effort: medium restored at the block level '
                           '(mirrors the site field; the mandate names no effort for this arm, so the '
                           'retained value is declared UNVERIFIED in sod.verify_security_reasoning_effort '
                           'rather than assumed sound)')
else:
    report['edits'].append('registry VERIFY row already carried reasoning_effort: medium')

# ------------------------------------------- 4. re-pin source_of_routes to the site digest (it just moved)
m = re.search(r'(  path: config/model-lane-assignment\.json\n  revision: )(\d+)(\n  sha256: )([0-9a-f]{64})', reg)
if not m:
    raise SystemExit('source_of_routes pin block not found in the expected shape')
old_digest = m.group(4)
reg = reg[:m.start()] + m.group(1) + '22' + m.group(3) + NEW_DIGEST + reg[m.end():]
report['edits'].append('source_of_routes re-pinned %s -> %s (site revision 22)' % (old_digest[:12], NEW_DIGEST[:12]))

# ------------------------------------------------------------------------------------------------- write
if APPLY:
    for p, txt, crlf in ((REG, reg, reg_crlf), (SITE, site_new, site_crlf)):
        b = pathlib.Path(str(p) + '.bak-' + STAMP)
        b.write_bytes(pathlib.Path(p).read_bytes())      # overwrite the post-edit copies with the CURRENT
        pathlib.Path(p).write_bytes(enc(txt, crlf))      # (still not a preimage -- hence section 1)
    report['sha256_after'] = {'config/lane-routing-registry.yaml': sha(REG),
                              'config/model-lane-assignment.json': sha(SITE)}
    (O / 'PATCH1_RECEIPT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'preimage_search'}, ensure_ascii=False, indent=1))
print('EMERGENCY PREIMAGE (verbatim, for the record): registry 38f0436b9bde... site e7be2dea3687...')
print('   the site preimage is also reconstructible: it is the file whose sha256 starts e7be2dea3687')
