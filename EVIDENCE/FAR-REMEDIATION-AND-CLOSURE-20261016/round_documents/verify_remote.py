"""Read the publication back from GitHub's API and compare it with what I believe I pushed.

The push command's own output is not evidence; this reads the remote. Prints only digests, counts and
statuses — never the token.
"""
import hashlib
import json
import pathlib
import re
import urllib.error
import urllib.request

KEY = pathlib.Path('C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt')
REPO, BRANCH, PR = 'shw097-team/Fabric', 'pub/far-remediation-and-closure-20261016', None
PREFIX = 'EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016'
# The PR number is not known until the PR exists, so read it from the receipt my own PR script wrote
# rather than hard-coding it (a hard-coded number silently verifies the WRONG pull request).
_pr = pathlib.Path(__file__).resolve().parent / 'PR_CREATED.json'
if PR is None and _pr.is_file():
    PR = json.loads(_pr.read_text(encoding='utf-8')).get('number')
LOCAL = pathlib.Path('C:/Projects/Agent_Workspace/Fabric') / PREFIX

tok = re.search(r'github_pat_[A-Za-z0-9_]+', KEY.read_text(encoding='utf-8', errors='replace')).group(0)
H = {'Authorization': 'Bearer %s' % tok, 'Accept': 'application/vnd.github+json',
     'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'hg-kseos-governed-runtime'}


def get(path):
    req = urllib.request.Request('https://api.github.com' + path, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, {'_error': e.read().decode('utf-8', errors='replace')[:300]}


out = {}
local_head = None
try:
    import subprocess
    local_head = subprocess.run(['git', '-C', 'C:/Projects/Agent_Workspace/Fabric', 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, check=True).stdout.strip()
except Exception as exc:
    local_head = 'unavailable: %s' % exc

st, pr = get('/repos/%s/pulls/%d' % (REPO, PR))
out['pull_request'] = {'http': st, 'number': pr.get('number'), 'state': pr.get('state'),
                       'head_sha': (pr.get('head') or {}).get('sha'),
                       'head_ref': (pr.get('head') or {}).get('ref'),
                       'base_ref': (pr.get('base') or {}).get('ref'),
                       'commits': pr.get('commits'), 'changed_files': pr.get('changed_files'),
                       'mergeable_state': pr.get('mergeable_state'),
                       'html_url': pr.get('html_url')}

st, br = get('/repos/%s/branches/%s' % (REPO, BRANCH))
out['remote_branch_sha'] = (br.get('commit') or {}).get('sha')
out['local_head_sha'] = local_head
out['sha_match'] = bool(out['remote_branch_sha'] and out['remote_branch_sha'] == local_head)

# the remote tree: is the whole packet actually there?
st, tree = get('/repos/%s/git/trees/%s?recursive=1' % (REPO, out['remote_branch_sha'] or 'main'))
paths = [t['path'] for t in tree.get('tree', []) if t['path'].startswith(PREFIX + '/')]
out['remote_packet_files'] = len(paths)
out['remote_manifest_present'] = (PREFIX + '/PACKET_MANIFEST.json') in paths

# byte-for-byte: pull the manifest back from the REMOTE and compare with the local bytes
dest = pathlib.Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex.2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch')
try:
    req = urllib.request.Request('https://api.github.com/repos/%s/contents/%s/PACKET_MANIFEST.json?ref=%s'
                                 % (REPO, PREFIX, BRANCH), headers=H)
    with urllib.request.urlopen(req, timeout=60) as r:
        doc = json.loads(r.read().decode('utf-8'))
    remote_sha = doc.get('sha')
    local_manifest = (LOCAL / 'PACKET_MANIFEST.json').read_bytes()
    out['manifest_remote_git_blob'] = remote_sha
    out['manifest_local_git_blob'] = hashlib.sha1(
        b'blob %d\x00' % len(local_manifest) + local_manifest).hexdigest()
    out['manifest_byte_identical'] = out['manifest_remote_git_blob'] == out['manifest_local_git_blob']
    out['manifest_local_sha256'] = hashlib.sha256(local_manifest).hexdigest()
except urllib.error.HTTPError as e:
    out['manifest_readback_error'] = '%s %s' % (e.code, e.read().decode('utf-8', errors='replace')[:200])

print(json.dumps(out, ensure_ascii=False, indent=1))
