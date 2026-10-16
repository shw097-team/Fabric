"""Assemble + publish the round's implementation and evidence packet into the Fabric mirror.

Target layout (matches the repo's own convention, verified against origin/main):
    EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/...        the packet (flat files + PACKET_MANIFEST.json)
    EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/.gitattributes   `* -text`, so the committed bytes are the
                                                              produced bytes and an external acceptor's
                                                              sha256 comparison against the manifest holds

Refuses to publish if the four product files in the candidate are byte-identical to the canonical ones
(that would mean ChangeSet B/C never landed, and publishing a packet claiming otherwise would be a
false claim). Writes PACKET_MANIFEST.json last, over the FINAL bytes.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/FAR-REMEDIATION-AND-CLOSURE-20261016'
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
PKT = FAB / 'EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016'

PRODUCT = ['scripts/runtime_role_binding_assert.py',
           'scripts/hgk-governed-runtime-controller.py',
           'tests/test_governed_runtime_controller.py',
           'tests/test_lane_effort_enforcement.py']
CONFIG = ['config/model-lane-assignment.json', 'config/lane-routing-registry.yaml']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def copy(src, rel):
    dst = PKT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def main():
    landed, identical = {}, []
    for rel in PRODUCT:
        c, b = O / 'candidate' / rel, R / rel
        landed[rel] = {'candidate': sha(c), 'baseline': sha(b) if b.is_file() else None,
                       'changed': (sha(c) != sha(b)) if b.is_file() else True}
        if b.is_file() and sha(c) == sha(b):
            identical.append(rel)
    if identical and len(identical) == len(PRODUCT):
        print(json.dumps({'stage': 'REFUSED', 'why': 'no product file changed: B/C never landed',
                          'unchanged': identical}, indent=1))
        return 2

    if PKT.exists():
        shutil.rmtree(PKT)
    PKT.mkdir(parents=True, exist_ok=True)
    (PKT / '.gitattributes').write_text(
        '# Published evidence packet: store bytes EXACTLY as produced.\n'
        '# Without this, the repository text normalization rewrites CRLF to LF in the committed blob, so\n'
        '# an external acceptor that downloads a file and compares its sha256 against PACKET_MANIFEST.json\n'
        '# gets a MISMATCH on every CRLF-bearing file. `-text` disables that for this subtree only.\n'
        '* -text\n', encoding='utf-8')

    # ---- 1. the implementation, both as files and as diffs against the baseline ----
    diffs = []
    for rel in PRODUCT:
        src = O / 'candidate' / rel
        copy(src, 'implementation/candidate/' + rel)
        base = R / rel
        if base.is_file():
            copy(base, 'implementation/baseline/' + rel)
            d = subprocess.run(['git', 'diff', '--no-index', '--',
                                str(base), str(src)], capture_output=True, text=True)
            diffs.append({'path': rel, 'diff': d.stdout})
    for rel in CONFIG:
        copy(R / rel, 'implementation/canonical/' + rel)
        bak = R / (rel + '.bak-lane-reliability-20261016')
        if bak.is_file():
            copy(bak, 'implementation/baseline_canonical/' + rel)
    (PKT / 'IMPLEMENTATION_DIFFS.json').write_text(
        json.dumps({'schema': 'HGK-ROUND-IMPLEMENTATION-DIFFS/1',
                    'note': 'unified diffs, baseline (canonical) -> candidate, produced by git diff --no-index',
                    'files': [{'path': d['path'], 'sha256': landed[d['path']]['candidate']} for d in diffs],
                    'diffs': diffs}, ensure_ascii=False, indent=2), encoding='utf-8')

    # ---- 2. the round's own documents and machine evidence ----
    singles = {
        'README.md': O / 'README.md',
        'ROUND_CLOSURE.json': O / 'ROUND_CLOSURE.json',
        'CHECKPOINT.md': R / '_handover/CHECKPOINT_HGK-FAR-REMEDIATION-AND-CLOSURE-20261016.md',
        'CHECKER_BRIEF.md': O / 'CHECKER_BRIEF.md',
        'FINDINGS_CHECKER_BRIEF_V1_WRITE_CONTRADICTION.md': O / 'FINDINGS_CHECKER_BRIEF_V1_WRITE_CONTRADICTION.md',
        'FINDINGS_SELF_CORRECTION_BC1_ARM_CLAIM.md': O / 'FINDINGS_SELF_CORRECTION_BC1_ARM_CLAIM.md',
        'FROZEN_MANIFEST.json': O / 'FROZEN_MANIFEST.json',
        'RETROSPECTIVE.md': O / 'RETROSPECTIVE.md',
        'RETROSPECTIVE.json': O / 'RETROSPECTIVE.json',
        'PLAN.md': O / 'PLAN.md',
        'BUILD_B_SPEC.md': O / 'BUILD_B_SPEC.md',
        'BUILD_BC3_SPEC.md': O / 'BUILD_BC3_SPEC.md',
        'FINDINGS_F1_PLAN_ROUTE_OUTLIER.md': O / 'FINDINGS_F1_PLAN_ROUTE_OUTLIER.md',
        'KANBAN_SWARM_GRAPH.json': O / 'KANBAN_SWARM_GRAPH.json',
        'HGK_TYPED_ADMISSION.json': O / 'admission.json',
        'ROLE_MANDATE.json': O / 'role_mandate.json',
        'PLAN_LANE_AVAILABILITY.json': O / 'PLAN_LANE_AVAILABILITY.json',
        'CHANGESET_A_MEASUREMENT.json': O / 'CHANGESET_A_MEASUREMENT.json',
        'CHANGESET_A_APPLY_RECEIPT.json': O / 'CHANGESET_A_APPLY_RECEIPT.json',
        'SELFCHECK_REPORT.json': O / 'SELFCHECK_REPORT.json',
        'SELFCHECK_REPORT.txt': O / 'SELFCHECK_REPORT.txt',
        'OPENSPEC_PROPOSAL.md': R / 'OPENSPEC/changes/hgk-lane-reliability-closure-20261016/proposal.md',
        'OPENSPEC_TASKS.md': R / 'OPENSPEC/changes/hgk-lane-reliability-closure-20261016/tasks.md',
        'OPENSPEC_DELTA_SPEC.md': R / 'OPENSPEC/changes/hgk-lane-reliability-closure-20261016/specs/lane-governance-gates/spec.md',
    }
    for rel, src in singles.items():
        if pathlib.Path(src).is_file():
            copy(src, rel)

    # ---- 3. every lane attempt's receipt, verbatim ----
    lane_files = ['dispatch.json', 'dispatch.json.attempts.ndjson', 'exit.json', 'stdout.txt',
                  'stderr.txt', 'invocation.json', 'TERMINATION.json', 'CHECKER_VERDICT.json']
    for d in sorted((O / 'lanes').glob('*/*')) if (O / 'lanes').is_dir() else []:
        if not d.is_dir():
            continue
        tagname = d.parent.name + '__' + d.name
        for f in lane_files:
            if (d / f).is_file():
                copy(d / f, 'lanes/' + tagname + '/' + f)
        raw = d / 'raw'
        if raw.is_dir():
            for f in sorted(raw.iterdir()):
                if f.is_file():
                    copy(f, 'lanes/' + tagname + '/raw/' + f.name)

    # ---- 4. the manifest, over the FINAL bytes ----
    files = []
    for p in sorted(PKT.rglob('*')):
        if p.is_file():
            files.append({'path': str(p.relative_to(FAB)).replace('\\', '/'),
                          'bytes': p.stat().st_size, 'sha256': sha(p), 'tracked': True})
    manifest = {
        'schema': 'FAR-REMEDIATION-AND-CLOSURE-20261016/PACKET-MANIFEST/1',
        'round': O.name,
        'at_utc': datetime.now(timezone.utc).isoformat(),
        'publish_claim': ('the DELIVERED set is every file under EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/. '
                          'Bytes are stored verbatim (-text). An external acceptor can recompute each sha256 '
                          'below from the delivered blob.'),
        'product_files_landed': landed,
        'files': files,
        'file_count': len(files),
        'canonical_acceptance': 'NOT_PERFORMED',
        'claim_ceiling': ('CANDIDATE_ONLY. This packet is evidence for an external acceptance officer; it resolves '
                          'nothing and its checker verdicts (if any) are advisory.'),
    }
    (PKT / 'PACKET_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                              encoding='utf-8')
    print(json.dumps({'packet': str(PKT), 'files': len(files) + 1, 'product_files_landed': landed,
                      'sample': [f['path'] for f in files[:6]]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
