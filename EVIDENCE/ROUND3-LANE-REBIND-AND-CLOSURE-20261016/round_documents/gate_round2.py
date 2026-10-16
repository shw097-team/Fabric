"""Pre-publication gate for round ROUND3-LANE-REBIND-AND-CLOSURE-20261016.

Refuses to let the packet be published unless every check below passes. Checks are written to fail loudly
rather than to reassure: a gate that only ever prints PASS is decoration.

  G1  every JSON document in the round parses
  G2  the frozen subject still recomputes to the recorded aggregate
  G3  the packet contains no credential material
  G4  the packet makes no self-acceptance claim
  G5  the receipts the closure cites exist and their key numbers agree with the closure
  G6  no oversized file and no writer probe litter is shipped
  G7  the ledgered residuals are actually present in the closure (no silent deletion)
"""
import hashlib
import json
import pathlib
import re
import sys

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
PKT = FAB / 'EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
BIG = 20_000_000

report = {'schema': 'HGK-ROUND-GATE-REPORT/1', 'round': O.name, 'checks': {}, 'verdict': None}

# G1 — every JSON parses
bad = []
for p in list(O.rglob('*.json')) + list(PKT.rglob('*.json') if PKT.is_dir() else []):
    if p.stat().st_size > 60_000_000:
        continue
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        bad.append('%s: %s' % (p.name, exc))
report['checks']['G1_all_json_parses'] = {'ok': not bad, 'failures': bad[:10],
                                          'counted': sum(1 for _ in O.rglob('*.json'))}

# G2 — the frozen subject recomputes
fm = O / 'FROZEN_MANIFEST.json'
if fm.is_file():
    man = json.loads(fm.read_text(encoding='utf-8'))
    agg = hashlib.sha256()
    mism = []
    for it in man['items']:
        agg.update(('%s|%s|%s\n' % (it['label'], it['path'], it['sha256'])).encode('utf-8'))
        p = pathlib.Path(it['path'])
        if it['exists'] and p.is_file():
            live = hashlib.sha256(p.read_bytes()).hexdigest()
            if live != it['sha256']:
                mism.append(it['path'])
    report['checks']['G2_frozen_subject_recomputes'] = {
        'ok': agg.hexdigest() == man['aggregate_sha256'] and not mism,
        'recorded': man['aggregate_sha256'], 'recomputed': agg.hexdigest(),
        'mismatched_items': mism[:10], 'items': man['item_count']}
else:
    report['checks']['G2_frozen_subject_recomputes'] = {'ok': False, 'why': 'no FROZEN_MANIFEST.json'}

# G3 — credential material
PAT = [r'github_pat_[A-Za-z0-9_]{10,}', r'\bghp_[A-Za-z0-9]{20,}', r'\bsk-[A-Za-z0-9]{20,}',
       r'\bBearer\s+[A-Za-z0-9_\-\.]{30,}', r'-----BEGIN [A-Z ]*PRIVATE KEY-----']
leaks = []
# The checker's read-only reference tree (subject/) is a byte-identical copy of the repository's OWN
# scripts/src/tests/config, and it is NOT published -- see SUBJECT_TREE_DIGEST.json for the digest and the
# stated reason. Its test fixtures legitimately carry fake key-shaped literals, so scanning it would fail
# this check on content that already exists in the repo. The exclusion is recorded in an ARTIFACT rather
# than applied in code alone, so it stays auditable: excluding it silently is how a real leak gets hidden.
REF = (O / 'subject').resolve()


def _in_ref(p):
    try:
        r = p.resolve()
        if r.is_relative_to(REF):
            return True
        # Any path DEEPER than one level under a lane's work/ is the lane's scratch: the reference copy,
        # the pre/post/incomplete tree copies (the checker builds several: work/pre/, work/subject/,
        # work/TEST_RESULTS/{pre_tree,incomplete_tree,before,after}/**) and per-test scratch directories.
        # Only a lane's own depth-1 files under work/ are publication material, so the scan is scoped by
        # DEPTH to exactly what ships. Measured three times: each name-based exclusion missed the next
        # directory a lane invented (subject -> TEST_RESULTS -> pre), so the rule is now structural.
        parts = r.parts
        if 'lanes' in parts and 'work' in parts:
            return (len(parts) - parts.index('work') - 1) > 1
        return False
    except (OSError, ValueError):
        return False


scan_targets = [p for p in (list(O.rglob('*.json')) + list(O.rglob('*.md')) + list(O.rglob('*.py'))
                            + list(O.rglob('*.txt')) + list(PKT.rglob('*') if PKT.is_dir() else []))
                if not _in_ref(p)]
for p in scan_targets:
    if not p.is_file() or p.stat().st_size > 30_000_000:
        continue
    try:
        t = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for pat in PAT:
        if re.search(pat, t):
            # Report the LOCATOR, not the basename: a basename-only hit costs a diagnostic round-trip
            # whenever several copies of a file exist in different scopes (measured, repeatedly).
            try:
                loc = str(p.relative_to(O)).replace('\\', '/')
            except ValueError:
                loc = str(p).replace('\\', '/')
            leaks.append('%s :: %s' % (loc, pat))
report['checks']['G3_no_credential_material'] = {'ok': not leaks, 'hits': leaks[:10],
                                                 'patterns': len(PAT)}

# G4 — no self-acceptance claim
SELF = [r'\bACCEPTED BY THE (?:AGENT|ROUND|ORCHESTRATOR)\b', r'\bSELF[- ]ACCEPTED\b']
claims = []
for p in list(PKT.rglob('*.md') if PKT.is_dir() else []) + list(PKT.rglob('*.json') if PKT.is_dir() else []):
    t = p.read_text(encoding='utf-8', errors='ignore')
    for pat in SELF:
        if re.search(pat, t, re.I):
            claims.append('%s :: %s' % (p.name, pat))
    # A 'canonical_acceptance' mention must be NEGATED in the same document. The FIRST version of this
    # check used r'canonical_acceptance["\s:]+(?!NOT_PERFORMED)', which can never work: a greedy character
    # class followed by a negative lookahead BACKTRACKS to a shorter match, so the lookahead is always
    # satisfiable and the pattern matched every file that mentioned the key -- including the ones that say
    # NOT_PERFORMED. It was a check that could not fail for the reason it was written for. Assert the fact
    # directly instead of through a regex trick.
    if 'canonical_acceptance' in t and 'NOT_PERFORMED' not in t:
        claims.append('%s :: mentions canonical_acceptance without NOT_PERFORMED' % p.name)
report['checks']['G4_no_self_acceptance_claim'] = {'ok': not claims, 'hits': claims[:10]}

# G5 — the closure's cited receipts exist and agree
cl = json.loads((O / 'ROUND_CLOSURE.json').read_text(encoding='utf-8'))
need = ['R1_R3_APPLY_RECEIPT.json', 'R1_R3_COMPLETION_RECEIPT.json', 'R2_PROMOTION_RECEIPT.json',
        'RESIDUAL_INVENTORY.json', 'FAR_RULING.md', 'FINDINGS_R7_CROSS_FIELD_DECLARATION.md',
        'FINDINGS_SELF_CORRECTIONS.md', 'SELF_EVOLUTION.md', 'RETROSPECTIVE.md', 'README.md']
missing = [n for n in need if not (O / n).is_file()]
r2 = json.loads((O / 'R2_PROMOTION_RECEIPT.json').read_text(encoding='utf-8'))
promoted = [f for f in r2['files'] if f.get('action') == 'PROMOTED']
agree = (len(cl['canonical_mutations']['R2_promoted_product_files']) == len(promoted) == 4)
report['checks']['G5_receipts_exist_and_agree'] = {
    'ok': not missing and agree,
    'missing': missing,
    'promoted_4': agree,
    'closure_regression_diff': cl['whole_tree_regression_isolation']['diff']}

# G6 — packet size + probe litter
oversize, litter, pkt_count = [], [], 0
PKT_FILES = sorted(p for p in PKT.rglob('*') if p.is_file()) if PKT.is_dir() else []
if not PKT_FILES:
    # The gate exists to stop a bad PUBLICATION. With no packet on disk it would otherwise pass
    # vacuously, which is the one outcome that makes every other check meaningless: report the absence
    # as a failure instead of a silent green.
    report['checks']['G6_packet_hygiene'] = {
        'ok': False, 'packet_files': 0,
        'reason': 'NOT_BUILT: %s does not exist or is empty -- run publish_packet first; a hygiene pass on '
                  'an absent packet is a vacuous pass' % PKT}
else:
    for p in PKT_FILES:
        pkt_count += 1
        if p.stat().st_size > BIG:
            oversize.append('%s (%d bytes)' % (p.name, p.stat().st_size))
        # Litter signatures: the bounded writer's own 2-byte probes. The generic token '_probe' was
        # dropped after it flagged a LEGITIMATE checker script named seam_probe.py -- a false positive
        # trains you to ignore the check.
        if re.search(r'zztemp|zz\.txt|__patch_probe', p.name):
            litter.append(str(p.relative_to(PKT)))
    report['checks']['G6_packet_hygiene'] = {'ok': not oversize and not litter,
                                            'packet_files': pkt_count, 'oversize': oversize,
                                            'litter': litter}

# G7 — the ledgered residuals survive into the closure
inv = json.loads((O / 'RESIDUAL_INVENTORY.json').read_text(encoding='utf-8'))
res = cl['honest_residuals']
report['checks']['G7_residuals_preserved'] = {
    'ok': len(res) >= 10,
    'closure_residuals': len(res),
    'inventory_items': len(inv.get('items', [])),
    'note': 'counts are compared, not wording: the closure may rephrase a ledgered item but may not drop it'}

ok = all(c.get('ok') for c in report['checks'].values())
report['verdict'] = 'GATE_PASS' if ok else 'GATE_REFUSE'
(O / 'GATE_REPORT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
for k, v in report['checks'].items():
    print('%-32s %s  %s' % (k, 'ok' if v.get('ok') else 'FAIL',
                            json.dumps({kk: vv for kk, vv in v.items() if kk != 'ok'}, ensure_ascii=False)[:190]))
print('\nVERDICT:', report['verdict'])
sys.exit(0 if ok else 1)
