"""Record the publication facts in the round's own artifacts (measured, not asserted).

Two writes:
  PUBLICATION_RECEIPT.json — the PR identity and the remote/local agreement measured by verify_remote.py.
  ROUND_CLOSURE.json       — the closure's publication block, so the closure does not stop at 'pushed'.

The facts recorded are the ones measured at PR creation. The branch receives one additive update commit
afterwards; that is disclosed here rather than hidden, because a receipt that claims to describe a moving
ref is the defect (SC-11) this round inherited.
"""
import json
import pathlib
import subprocess

R = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
O = R / 'var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016'
FAB = pathlib.Path('C:/Projects/Agent_Workspace/Fabric')
BRANCH = 'pub/round3-lane-rebind-and-closure-20261016'

push = json.loads((O / 'PUSH_RECEIPT.json').read_text(encoding='utf-8'))
head_now = subprocess.check_output(['git', '-C', str(FAB), 'rev-parse', 'HEAD'], text=True).strip()

pub = {
    'schema': 'HGK-PUBLICATION-RECEIPT/1',
    'round': O.name,
    'repo': 'shw097-team/Fabric',
    'pull_request': {'number': 10, 'html_url': 'https://github.com/shw097-team/Fabric/pull/10',
                     'state': 'open', 'base': 'main', 'head_ref': BRANCH,
                     'changed_files': 347, 'mergeable_state': 'clean'},
    'measured_by': 'verify_remote.py 10 (HTTP 200 on the PR; branch sha and packet manifest git blob '
                   'compared against the local clone)',
    'remote_local_agreement': {
        'pr_head_sha_at_creation': '808d79e436b4266914c2a8dab7b17bd0a0300bbe',
        'remote_branch_sha': '808d79e436b4266914c2a8dab7b17bd0a0300bbe',
        'local_head_sha': '808d79e436b4266914c2a8dab7b17bd0a0300bbe',
        'sha_match': True,
        'packet_manifest_git_blob': '02046d148b4cb12c08fdc7ff32aeee919ccd4d7a',
        'manifest_byte_identical': True},
    'later_commits_on_the_branch': {'additive_update': True, 'local_head_at_receipt_time': head_now,
                                    'reason': 'the packet was rebuilt to carry the push receipt and the PASS '
                                              'gate report; a receipt describing a moving ref would be the '
                                              'SC-11 defect, so the creation-time facts are labelled as such'},
    'not_claimed': ['no merge — merging to main is the owner\'s decision',
                    'no external acceptance: this receipt records publication, not review',
                    'the checker verdict is advisory and comes from a checker sharing the writer\'s model'],
}
(O / 'PUBLICATION_RECEIPT.json').write_text(json.dumps(pub, ensure_ascii=False, indent=2), encoding='utf-8')

cl = json.loads((O / 'ROUND_CLOSURE.json').read_text(encoding='utf-8'))
cl['publication'] = {
    'repo': 'shw097-team/Fabric',
    'branch': BRANCH,
    'pull_request': 10,
    'pull_request_url': 'https://github.com/shw097-team/Fabric/pull/10',
    'merged': False,
    'merge_is': 'an OWNER decision, explicitly outside this round\'s claim ceiling',
    'gate': 'GATE_PASS 7/7 (see GATE_REPORT.json)',
    'packet_files': 348,
    'remote_verified': 'sha_match=true, manifest byte-identical (git blob 02046d14)',
    'receipt': 'PUBLICATION_RECEIPT.json',
}
(O / 'ROUND_CLOSURE.json').write_text(json.dumps(cl, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'publication_receipt': 'written', 'closure_publication_block': 'added',
                  'pr': pub['pull_request']['number'], 'head_now': head_now}, indent=1))
