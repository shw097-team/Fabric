"""Assemble + publish THIS round's implementation and evidence packet into the Fabric mirror.

Rule-based collection rather than a hand-maintained list, because a list that names last round's files is
how a packet silently publishes the wrong subject.

Delivered set:
    <packet>/round_documents/      every file at the round root (docs, generators, receipts, manifests)
    <packet>/evidence/             the sub-agent investigations, the whole-tree logs, the promotion summary
    <packet>/implementation/       the canonical change, before and after: config pair + product files + diffs
    <packet>/implementation/writer_output/   what the bounded writer actually produced (candidate tree)
    <packet>/lanes/                every lane attempt's receipts, verbatim, including terminations
    <packet>/openspec/             the change proposal / tasks / delta spec
    <packet>/under_governance/     the handover checkpoint and the frozen manifest
    <packet>/PACKET_MANIFEST.json  sha256 + byte length over the FINAL bytes
    <packet>/.gitattributes        `* -text`, so an external acceptor's digest comparison holds

Excluded on purpose, and named here so the exclusion is visible:
    FROZEN_MANIFEST.json's subject set is NOT re-copied (it would duplicate wholesale); its own file is
    delivered under under_governance/.
    var/ trees outside this round's directory, .bak files beyond the two config baselines this round used.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
from datetime import datetime, timezone

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
PKT = FAB / 'EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
SUF = '.bak-far-remediation-20261016'
CONFIG = ['config/lane-routing-registry.yaml', 'config/model-lane-assignment.json']
PRODUCT = ['scripts/runtime_role_binding_assert.py', 'scripts/hgk-governed-runtime-controller.py',
           'tests/test_governed_runtime_controller.py', 'tests/test_lane_effort_enforcement.py']
CHECKPOINT = R / '_handover/CHECKPOINT_HGK-ROUND3-LANE-REBIND-AND-CLOSURE-20261016.md'
OPENSPEC = R / 'OPENSPEC/changes/hgk-far-remediation-20261016'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def copy(src, rel):
    dst = PKT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def main():
    if PKT.exists():
        shutil.rmtree(PKT)
    PKT.mkdir(parents=True, exist_ok=True)
    (PKT / '.gitattributes').write_text(
        '# Published evidence packet: store bytes EXACTLY as produced.\n'
        '# Without this, git text normalization rewrites CRLF to LF in the committed blob, so an external\n'
        '# acceptor that downloads a file and compares its sha256 against PACKET_MANIFEST.json gets a\n'
        '# MISMATCH on every CRLF-bearing file. `-text` disables that for this subtree only.\n* -text\n',
        encoding='utf-8')

    counts = {}

    # 1. round documents at the root (a rule, not a list)
    n = 0
    for p in sorted(O.iterdir()):
        if p.is_file() and p.suffix.lower() in ('.md', '.json', '.py', '.txt'):
            copy(p, 'round_documents/' + p.name)
            n += 1
    counts['round_documents'] = n

    # 2. evidence sub-tree
    n = 0
    for p in sorted((O / 'evidence').rglob('*')):
        if p.is_file():
            copy(p, 'evidence/' + str(p.relative_to(O / 'evidence')).replace('\\', '/'))
            n += 1
    counts['evidence'] = n

    # 3. the canonical change: config before/after, product before/after, diffs
    n = 0
    diffs = []
    for rel in CONFIG:
        copy(R / rel, 'implementation/config/after/' + rel)
        b = R / (rel + SUF)
        if b.is_file():
            copy(b, 'implementation/config/before/' + rel)
            d = subprocess.run(['git', 'diff', '--no-index', '--', str(b), str(R / rel)],
                               capture_output=True, text=True)
            diffs.append({'path': rel, 'baseline': 'config before (this round)', 'diff': d.stdout})
            n += 3
    for rel in PRODUCT:
        if (R / rel).is_file():
            copy(R / rel, 'implementation/product/after/' + rel)
            b = R / (rel + SUF)
            if b.is_file():
                copy(b, 'implementation/product/before/' + rel)
                d = subprocess.run(['git', 'diff', '--no-index', '--', str(b), str(R / rel)],
                                   capture_output=True, text=True)
                diffs.append({'path': rel, 'baseline': 'canonical before promotion', 'diff': d.stdout})
                n += 3
    counts['implementation_files'] = n

    # 4. what the bounded writer produced
    n = 0
    for p in sorted((O / 'candidate').rglob('*')):
        if p.is_file():
            copy(p, 'implementation/writer_output/' + str(p.relative_to(O / 'candidate')).replace('\\', '/'))
            n += 1
    counts['writer_output'] = n

    # 5. lane receipts verbatim + their raw logs
    lane_files = ['dispatch.json', 'dispatch.json.attempts.ndjson', 'exit.json', 'stdout.txt', 'stderr.txt',
                  'invocation.json', 'TERMINATION.json', 'CHECKER_VERDICT.json', 'verdict_raw.txt']
    n = 0
    for d in sorted((O / 'lanes').glob('*/*')):
        if not d.is_dir():
            continue
        tag = d.parent.name + '__' + d.name
        for f in lane_files:
            if (d / f).is_file():
                copy(d / f, 'lanes/' + tag + '/' + f)
                n += 1
        for sub in ('raw', 'work'):
            sd = d / sub
            if sd.is_dir():
                for f in sorted(sd.rglob('*')):
                    if not f.is_file():
                        continue
                    rel = f.relative_to(sd)
                    # The VERIFY lane's work/ carries the runner's byte-identical COPY of the reference
                    # tree (work/subject/**) plus the pre/post/incomplete tree copies and per-test scratch
                    # directories the checker builds under work/TEST_RESULTS/. None of that is evidence:
                    # it duplicates repository content and, measured, it flattened 244 scratch files into
                    # the packet (352 files total) on the first attempt. What ships is the lane's OWN
                    # material -- files directly under work/, and the checker's own measurement files
                    # directly under work/TEST_RESULTS/ -- so the rule is a DEPTH limit, not a name list.
                    if len(rel.parts) > 2:
                        continue
                    if rel.parts and rel.parts[0] == 'TEST_RESULTS':
                        continue
                    if len(rel.parts) == 1 and f.stat().st_size < 4_000_000:
                        copy(f, 'lanes/' + tag + '/' + sub + '/' + f.name)
                        n += 1
                tr = sd / 'TEST_RESULTS'
                if tr.is_dir():
                    for f in sorted(tr.iterdir()):
                        if (f.is_file() and f.suffix.lower() in ('.json', '.txt', '.py', '.ndjson')
                                and f.stat().st_size < 2_000_000):
                            copy(f, 'lanes/' + tag + '/' + 'measurements/' + f.name)
                            n += 1
    counts['lane_files'] = n

    # 6. openspec change + governance handover
    n = 0
    for p in sorted(OPENSPEC.rglob('*')):
        if p.is_file():
            copy(p, 'openspec/' + str(p.relative_to(OPENSPEC)).replace('\\', '/'))
            n += 1
    if CHECKPOINT.is_file():
        copy(CHECKPOINT, 'under_governance/CHECKPOINT.md')
        n += 1
    for rel in ('FROZEN_MANIFEST.json', 'ROUND_CLOSURE.json', 'GATE_REPORT.json'):
        if (O / rel).is_file():
            copy(O / rel, 'under_governance/' + rel)
            n += 1
    counts['openspec_and_governance'] = n

    (PKT / 'IMPLEMENTATION_DIFFS.json').write_text(json.dumps(
        {'schema': 'HGK-ROUND-IMPLEMENTATION-DIFFS/1',
         'note': 'unified diffs, canonical-before -> canonical-after, produced by git diff --no-index',
         'diffs': diffs, 'diff_count': len(diffs)}, ensure_ascii=False, indent=2), encoding='utf-8')

    # 7. the manifest, over the FINAL bytes
    files = [{'path': str(p.relative_to(FAB)).replace('\\', '/'), 'bytes': p.stat().st_size, 'sha256': sha(p)}
             for p in sorted(PKT.rglob('*')) if p.is_file()]
    manifest = {
        'schema': 'ROUND3-LANE-REBIND-AND-CLOSURE-20261016/PACKET-MANIFEST/1',
        'round': O.name,
        'at_utc': datetime.now(timezone.utc).isoformat(),
        'collection_rule': ('every file in the round directory by suffix, plus the evidence/, lanes/, candidate/ '
                           'and openspec/ sub-trees, plus the handover checkpoint; no hand-maintained list'),
        'section_counts': counts,
        'publish_claim': ('the DELIVERED set is every file under EVIDENCE/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/. '
                          'Bytes are stored verbatim (-text). An external acceptor can recompute each sha256 '
                          'below from the delivered blob.'),
        'files': files, 'file_count': len(files),
        'canonical_acceptance': 'NOT_PERFORMED',
        'claim_ceiling': ('CANDIDATE_ONLY. This packet is evidence for an external acceptance officer; it '
                          'resolves nothing, and any checker verdict inside it is advisory.')}
    (PKT / 'PACKET_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                              encoding='utf-8')
    print(json.dumps({'packet': str(PKT), 'file_count': len(files) + 1, 'sections': counts,
                      'sample': [f['path'] for f in files[:8]]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
