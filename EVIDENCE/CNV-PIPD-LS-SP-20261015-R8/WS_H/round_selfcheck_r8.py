#!/usr/bin/env python
"""R8 TF-10 repair: offline, fail-closed self-check; never a packet acceptance.

All snapshot expectations come from locally available Git objects at resolved HEAD.
No network and no Git writes. Original six assertion families are retained; remote
assertions remain FAIL/environment-gap rather than being silently made local PASS.
Policy constants (allowed verdicts, secret regexes, prohibited modes) are contracts,
not snapshot expectations. A deliberately empty inventory MUST fail check 2.
"""
from __future__ import annotations
import argparse
import ast
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
READ_ONLY_GIT = {'rev-parse', 'symbolic-ref', 'ls-tree', 'cat-file', 'diff', 'for-each-ref'}


def guarded_write(path, data):
    target = Path(path).resolve()
    if target.parent != OUT.resolve() or target == Path(__file__).resolve():
        raise ValueError('write refused: target must be an output directly inside WS_H')
    target.write_bytes(data)


def safe_path(path, prefix):
    if not isinstance(path, str) or not path.startswith(prefix):
        return False
    p = PurePosixPath(path)
    return (not p.is_absolute() and '\\' not in path and ':' not in path
            and all(x not in ('', '.', '..') for x in path.split('/')))


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob_id(data, algorithm):
    h = hashlib.new(algorithm)
    h.update(b'blob ' + str(len(data)).encode() + b'\0' + data)
    return h.hexdigest()


class Snapshot:
    def git(self, *args):
        if not args or args[0] not in READ_ONLY_GIT:
            raise ValueError('git read-only gate refused subcommand')
        env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1',
                   GIT_TERMINAL_PROMPT='0')
        p = subprocess.run(['git', '--no-optional-locks', '-C', str(self.worktree), *args],
                           capture_output=True, timeout=90, env=env)
        if p.returncode:
            raise RuntimeError('git ' + args[0] + ': ' + p.stderr.decode(errors='replace'))
        return p.stdout

    def text(self, *args):
        return self.git(*args).decode('utf-8').strip()

    def tree(self, rev, prefix=None):
        args = ['ls-tree', '-r', '-z', rev]
        if prefix is not None:
            args += ['--', prefix.rstrip('/')]
        out = {}
        for row in self.git(*args).split(b'\0'):
            if row:
                meta, path = row.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                out[path.decode('utf-8')] = dict(mode=mode, type=kind, oid=oid)
        return out

    def raw(self, rev, path):
        return self.git('cat-file', 'blob', rev + ':' + path)

    def __init__(self, worktree, prefix=None):
        self.worktree = Path(worktree).resolve()
        root = self.text('rev-parse', '--show-toplevel')
        self.worktree = Path(root).resolve()
        self.head = self.text('rev-parse', '--verify', 'HEAD^{commit}')
        self.branch = self.text('symbolic-ref', '--short', 'HEAD')
        self.algorithm = self.text('rev-parse', '--show-object-format')
        whole = self.tree(self.head)
        candidates = []
        for path, ent in whole.items():
            if ent['type'] == 'blob' and path.endswith('/PACKET_MANIFEST.json'):
                doc = json.loads(self.raw(self.head, path))
                if doc.get('branch') == self.branch:
                    candidates.append(path.rsplit('/', 1)[0] + '/')
        if len(candidates) != 1:
            raise ValueError('packet root discovery must find exactly one manifest bound to branch: ' + repr(candidates))
        discovered = candidates[0]
        self.prefix = discovered if prefix is None else prefix
        if self.prefix != discovered or not safe_path(self.prefix + 'PACKET_MANIFEST.json', self.prefix):
            raise ValueError('wrong/unsafe prefix; does not match branch-bound live manifest')
        self.packet_dir = self.worktree.joinpath(*self.prefix.rstrip('/').split('/'))
        if not self.packet_dir.is_dir() or not self.packet_dir.resolve().is_relative_to(self.worktree):
            raise ValueError('packet directory absent or outside repository')
        self.entries = {p: e for p, e in whole.items() if p.startswith(self.prefix)}
        self.blobs = {p: e for p, e in self.entries.items() if e['type'] == 'blob'}
        if not self.blobs:
            raise ValueError('empty packet: never a vacuous PASS')
        self.manifest_raw = self.raw(self.head, self.prefix + 'PACKET_MANIFEST.json')
        self.manifest = json.loads(self.manifest_raw)
        # Local R7 evidence is historical input, never rewritten by this harness.
        self.handover = OUT.parent.parent / self.packet_dir.name
        self.legacy = self.handover / 'selfcheck/round_selfcheck.py'
        self.start_refs = self.text('for-each-ref', '--format=%(refname) %(objectname)')

    def inventory(self):
        out = {}
        for base, dirs, files in os.walk(self.packet_dir, followlinks=False):
            for name in list(dirs):
                p = Path(base) / name
                if p.is_symlink() or not p.resolve().is_relative_to(self.packet_dir.resolve()):
                    out[p.relative_to(self.worktree).as_posix()] = None
                    dirs.remove(name)
            for name in files:
                p = Path(base) / name
                rel = p.relative_to(self.worktree).as_posix()
                if p.is_symlink() or not p.resolve().is_relative_to(self.packet_dir.resolve()):
                    out[rel] = None
                else:
                    out[rel] = blob_id(p.read_bytes(), self.algorithm)
        return out


def legacy_contract(s):
    """Parse policy literals only: never import or execute packet/historical code."""
    tree = ast.parse(s.legacy.read_bytes())
    wanted = {'R7_SCHEMA', 'ALLOWED_ITEM_VERDICTS', 'ALLOWED_OVERALL'}
    return {node.targets[0].id: ast.literal_eval(node.value) for node in tree.body
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in wanted}


def check_1(s):
    tracking = 'refs/remotes/origin/' + s.branch
    cached = s.text('rev-parse', '--verify', tracking + '^{commit}')
    recorded = json.loads((s.handover / 'R7_POST_COMMIT_READBACK.json').read_bytes())['repo']['head_after_r7']
    facts = dict(local_head=s.head, cached_tracking_head=cached, historical_recorded_head=recorded,
                 local_equals_cached=s.head == cached, historical_record_matches=s.head == recorded,
                 live_remote_verified=False, gap='Network forbidden: cached ref is NOT a live remote readback')
    # Preserve remote verification and recorded-head equality: cannot green either by relabeling.
    return (facts['local_equals_cached'] and facts['historical_record_matches']
            and facts['live_remote_verified']), facts


def inventory_result(s, local):
    missing = sorted(set(s.blobs) - set(local))
    extra = sorted(set(local) - set(s.blobs))
    bad = sorted(p for p in set(local) & set(s.blobs) if local[p] != s.blobs[p]['oid'])
    ok = bool(s.blobs) and bool(local) and not (missing or extra or bad)
    return ok, dict(head=s.head, git_blobs=len(s.blobs), local_files=len(local),
                    missing=missing, local_only=extra, raw_blob_id_mismatches=bad)


def check_2(s):
    return inventory_result(s, s.inventory())


def manifest_result(s, doc):
    inv = doc.get('tracked_inventory')
    excluded = doc.get('local_only_excluded')
    if not isinstance(inv, list) or not isinstance(excluded, list):
        return False, dict(error='inventory/exclusions must be arrays')
    if not all(isinstance(p, str) for p in inv + excluded):
        return False, dict(error='inventory/exclusions must contain paths')
    expected = set(s.blobs)
    tracked = doc.get('tracked_file_count')
    fc = doc.get('file_count')
    conditions = dict(nonempty=bool(inv), no_duplicates=len(inv) == len(set(inv)),
                      excluded_unique=len(excluded) == len(set(excluded)),
                      set_equality=set(inv) == expected,
                      prefix_containment=all(safe_path(p, s.prefix) for p in inv + excluded),
                      excluded_not_tracked=not (set(inv) & set(excluded)),
                      tracked_equals_live=type(tracked) is int and tracked == len(expected),
                      file_count_reconciliation=type(fc) is int and type(tracked) is int
                      and fc - tracked == len(excluded))
    return all(conditions.values()), dict(conditions=conditions, git_blobs=len(expected),
           tracked_file_count=tracked, file_count=fc, inventory_paths=len(inv),
           excluded_paths=len(excluded), missing=sorted(expected - set(inv)),
           extra=sorted(set(inv) - expected))


def check_3(s):
    ok, detail = manifest_result(s, s.manifest)
    local_raw = (s.packet_dir / 'PACKET_MANIFEST.json').read_bytes()
    equal = local_raw == s.manifest_raw
    detail.update(manifest_committed_sha256=sha256(s.manifest_raw),
                  manifest_local_sha256=sha256(local_raw), manifest_exact_bytes_equal=equal)
    return ok and equal, detail


def check_4(s):
    baseline = json.loads(s.raw(s.head, s.prefix + 'R7_BASELINE_MAIN.json'))
    base = s.text('rev-parse', '--verify', baseline['main_sha_at_baseline'] + '^{commit}')
    frozen = baseline['r6r7_prefix']
    if frozen == s.prefix or not safe_path(frozen + 'PACKET_MANIFEST.json', frozen):
        raise ValueError('invalid frozen archive scope in baseline')
    cached_main = s.text('rev-parse', '--verify', 'refs/remotes/origin/main^{commit}')
    before = s.tree(base, frozen)
    now = s.tree(s.head, frozen)
    cached = s.tree(cached_main, frozen)
    braw = s.raw(base, frozen + 'PACKET_MANIFEST.json')
    hraw = s.raw(s.head, frozen + 'PACKET_MANIFEST.json')
    changed = [p.decode() for p in s.git('diff', '--no-ext-diff', '--no-renames',
               '--name-only', '-z', base, s.head, '--').split(b'\0') if p]
    forbidden = sorted(p for p in changed if not safe_path(p, s.prefix))
    local_conditions = dict(baseline_nonempty=bool(before),
        cached_main_equals_baseline=cached_main == base,
        archive_full_tree_unchanged=before == now == cached,
        baseline_record_count_matches=baseline['r6r7_blobs'] == len(before),
        baseline_record_manifest_matches=baseline['r6r7_manifest_sha256'] == sha256(braw),
        archive_manifest_exact_bytes_equal=braw == hraw,
        changed_paths_contained=not forbidden)
    detail = dict(baseline_head=base, cached_main=cached_main, frozen_prefix=frozen,
                  baseline_blobs=len(before), head_blobs=len(now),
                  baseline_manifest_sha256=sha256(braw), head_manifest_sha256=sha256(hraw),
                  local_conditions=local_conditions, changed_paths=len(changed),
                  forbidden_changed_paths=forbidden, live_main_verified=False,
                  gap='Network forbidden: live main equality cannot be established')
    return all(local_conditions.values()) and detail['live_main_verified'], detail


def check_5(s):
    record = json.loads((s.handover / 'M2_TRUSTED_SCOPE_SECRETS_R7.json').read_bytes())
    old_scope = record['scope']
    historic_ok = (record.get('verdict') == 'PASS'
                  and not old_scope['out_of_prefix_or_traversal'] and not old_scope['symlinks']
                  and old_scope['executable_bit_blobs']['count'] == 0
                  and not record['secret_scan']['hard_findings'])
    # Carry forward every M2 hard regex without executing m2_scan.py.
    policy_tree = ast.parse(s.raw(s.head, s.prefix + 'm2_scan.py'))
    patterns = []
    for node in policy_tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'HARD_PATTERNS':
            for entry in node.value.elts:
                name, call = entry.elts
                if not isinstance(call, ast.Call) or call.keywords or len(call.args) != 1:
                    raise ValueError('unsupported secret policy; refusing to skip a regex')
                patterns.append((ast.literal_eval(name), re.compile(ast.literal_eval(call.args[0]))))
    if not patterns:
        raise ValueError('no M2 hard-secret policy: refusing vacuous PASS')
    scope, hard, digest_parts = [], [], []
    for path, ent in sorted(s.entries.items()):
        if not safe_path(path, s.prefix) or ent['type'] != 'blob' or ent['mode'] != '100644':
            scope.append(dict(path=path, mode=ent['mode'], type=ent['type']))
        if ent['type'] != 'blob':
            continue
        data = s.git('cat-file', 'blob', ent['oid'])
        digest_parts.append(path + ':' + sha256(data))
        text = data.decode('latin-1')
        for name, rx in patterns:
            count = sum(1 for _ in rx.finditer(text))
            if count:
                hard.append(dict(path=path, pattern=name, count=count))
    return historic_ok and not scope and not hard, dict(historical_record_pass=historic_ok,
        historical_scan_head=record['scanned']['rev_resolved'], scan_head=s.head,
        scanned_blobs=len(s.blobs), hard_policy_patterns=len(patterns),
        scope_violations=scope, hard_findings=hard,
        scan_digest_sha256=sha256(''.join(digest_parts).encode()),
        note='Live re-scan; historical record alone is not current evidence. No packet code executed. Operator token exact-value scan not performed.')


def check_6(s):
    contract = legacy_contract(s)
    path = s.handover / 'R7_CHECKER_ATTEMPT3/R7_CHECKER_VERDICT.json'
    doc = json.loads(path.read_bytes())
    items = doc.get('items', [])
    conditions = dict(schema=doc.get('schema') == contract['R7_SCHEMA'],
        overall=doc.get('overall_verdict') in contract['ALLOWED_OVERALL'],
        items=bool(items) and all(i.get('verdict') in contract['ALLOWED_ITEM_VERDICTS'] for i in items))
    return all(conditions.values()), dict(conditions=conditions, schema=doc.get('schema'),
        overall_verdict=doc.get('overall_verdict'), items=len(items), ids=[i.get('id') for i in items],
        first_fail=doc.get('first_fail'), policy_source=str(s.legacy), verdict_source=str(path),
        note='Historical verdict format check only; not a fresh independent checker verdict')


def negative_controls(s):
    empty_ok, empty_detail = inventory_result(s, {})
    mutated = copy.deepcopy(s.manifest)
    mutated['tracked_inventory'][0] = s.prefix + '__deliberately_absent__'
    wrong_set_ok, wrong_set_detail = manifest_result(s, mutated)
    wrong_prefix_rejected = False
    try:
        Snapshot(s.worktree, s.prefix + '__wrong_prefix__/')
    except ValueError:
        wrong_prefix_rejected = True
    write_rejected = git_rejected = False
    try:
        guarded_write(OUT.parent / 'forbidden-write-probe', b'never written')
    except ValueError:
        write_rejected = True
    try:
        s.git('push', 'origin', s.branch)
    except ValueError:
        git_rejected = True
    detail = dict(empty_inventory_check_2='PASS' if empty_ok else 'FAIL',
        empty_inventory_missing=len(empty_detail['missing']),
        equal_count_wrong_set_check_3='PASS' if wrong_set_ok else 'FAIL',
        wrong_set_conditions=wrong_set_detail['conditions'],
        wrong_prefix_rejected=wrong_prefix_rejected, outside_write_refused=write_rejected,
        git_push_refused=git_rejected)
    return (not empty_ok and not wrong_set_ok and wrong_prefix_rejected and write_rejected and git_rejected), detail


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worktree', required=True)
    parser.add_argument('--prefix', help='optional asserted prefix; must match runtime discovery')
    args = parser.parse_args(argv)
    print('claim_ceiling: LOCAL / candidate-only. No acceptance, Gate PASS or merge authorization.')
    print('UTC:', datetime.datetime.now(datetime.timezone.utc).isoformat())
    print('MODE: offline; read-only Git; no credential reads; no packet repair/writes')
    try:
        s = Snapshot(args.worktree, args.prefix)
    except Exception as e:
        print('SNAPSHOT FAIL:', type(e).__name__, str(e))
        print('OVERALL_SELFCHECK_VERDICT: FAIL')
        return 1
    print('SNAPSHOT:', json.dumps(dict(worktree=str(s.worktree), packet_root=s.prefix,
          branch=s.branch, head=s.head, git_blobs=len(s.blobs)), sort_keys=True))
    rows = []
    checks = (check_1, check_2, check_3, check_4, check_5, check_6)
    for number, check in enumerate(checks, 1):
        try:
            ok, detail = check(s)
        except Exception as e:
            ok, detail = False, dict(error=type(e).__name__, message=str(e))
        rows.append((str(number), ok))
        print('[%s] %s: %s' % (number, check.__name__, 'PASS' if ok else 'FAIL'))
        print(json.dumps(detail, ensure_ascii=True, indent=2, sort_keys=True))
    try:
        nc_ok, detail = negative_controls(s)
    except Exception as e:
        nc_ok, detail = False, dict(error=repr(e))
    print('NEGATIVE_CONTROL:', 'PASS (violations rejected)' if nc_ok else 'FAIL')
    print(json.dumps(detail, indent=2, sort_keys=True))
    stable = (s.text('rev-parse', '--verify', 'HEAD^{commit}') == s.head
              and s.text('for-each-ref', '--format=%(refname) %(objectname)') == s.start_refs)
    print('HEAD_AND_REFS_STABLE:', stable)
    print(' '.join(n + '=' + ('PASS' if ok else 'FAIL') for n, ok in rows))
    overall = all(ok for _, ok in rows) and nc_ok and stable
    print('OVERALL_SELFCHECK_VERDICT:', 'PASS' if overall else 'FAIL')
    print('Repairs: harness expectation derivation only; packet and historical evidence remain unchanged.')
    print('Remote branch/main, provider/model attestation, upstream CI and acceptance authority remain unverified.')
    return 0 if overall else 1


if __name__ == '__main__':
    sys.exit(main())
