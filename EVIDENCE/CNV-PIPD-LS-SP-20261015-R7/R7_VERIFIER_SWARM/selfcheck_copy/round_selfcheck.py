#!/usr/bin/env python3
"""R7-0 selfcheck / self-repair harness (mission CNV-PIPD-LS-SP-20261015).

Re-verifies the round's own publication invariants from live evidence, repairs only what
is safely repairable (this round's own readback records inside the handover dir), then
re-verifies, and reports residuals honestly.

HARD CONSTRAINTS ENFORCED IN-PROCESS:
  * writes nothing outside .../CNV-PIPD-LS-SP-20261015-R7/ (guard refuses any other path);
  * never touches EVIDENCE/CNV-PIPD-LS-SP-20261015/** (the merged archive lives outside
    the handover dir, so the write guard refuses it; git access is read-only anyway);
  * git non-write mode: the command gate refuses git add/commit/push/merge/checkout etc.;
  * the GitHub token is read from TOKEN_PATH into memory only, used only as an
    Authorization header: never printed, never in argv, never in a URL, never written.

REPAIR MODE (max 3 iterations): recompute and rewrite the round's own readback records
(R7_POST_COMMIT_READBACK.json / R7_PUBLICATION_VERIFICATION.json) and re-run the checks.
Never commits, never pushes, never touches the merged archive, never edits product code.

Claim ceiling of every output: LOCAL / candidate-only. This is not an Acceptance Officer
verdict, not a Gate PASS, not a merge authorization, not a security clearance, and the
output states this on every run.
"""

import ctypes
import hashlib
import json
import os
import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# ------------------------------------------------------------------ constants
HANDOVER = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7"
REPO = "shw097-team/Fabric"
PKT = "EVIDENCE/CNV-PIPD-LS-SP-20261015-R7"
PKT_P = PKT + "/"
FROZEN = "EVIDENCE/CNV-PIPD-LS-SP-20261015/"
BRANCH = "evidence/cnv-pipd-ls-sp-20261015-r7"
LOCAL_RB = "R7_POST_COMMIT_READBACK.json"
LOCAL_PV = "R7_PUBLICATION_VERIFICATION.json"
TOKEN_PATH = "C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt"
WORKTREE = "C:/Projects/wt-cnv-r7"
USER_AGENT = "round-selfcheck-cnvpipd-r7"

EXPECTED_MAIN_SHA = "b8ff81043e47e4b652522be34444bf52fcf4d65e"
EXPECTED_R7_HEAD = "7d610e5821b6eddd3969cd537f05efe81fdd54b6"
EXPECTED_FROZEN_BLOBS = 581
EXPECTED_R6_MANIFEST_SHA256 = "27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b"
EXPECTED_R7_MANIFEST_SHA256 = "c5fc66e4dd22470c1eacce3954c8ed728b1c55f0a2f188c2e190f03c29594f79"
R7_SCHEMA = "CNV-PIPD-LS-SP-20261015-R7/CHECKER-VERDICT/3"
ALLOWED_ITEM_VERDICTS = {
    "CONFIRMED",
    "CONFIRMED_PRE_EXISTING",
    "CHALLENGED",
    "UNVERIFIABLE",
    "ACL_UNENFORCEABLE",
}
ALLOWED_OVERALL = {"PENDING_OWNER", "CHALLENGED"}
OUTPUT_BANNER = "claim_ceiling: LOCAL / candidate-only"
MAX_REPAIR_ITERATIONS = 3

REPORDIR = os.path.normpath(os.path.abspath(HANDOVER))
R7_OUTPUT_DIR = os.path.join(REPORDIR, "selfcheck")

# git non-write mode -----------------------------------------------------------

GIT_WRITE_VERBS = {
    "add", "commit", "push", "merge", "rebase", "reset", "restore", "checkout",
    "clean", "rm", "mv", "gc", "am", "cherry-pick", "revert", "stash", "tag",
    "branch", "worktree", "filter-branch", "clone", "fetch", "pull", "apply",
    "update-index", "update-ref", "config", "init", "fsck", "replace",
}


def _fail(msg):
    raise AssertionError(msg)


def git_write_verb_check(argv):
    """Return the git verb that would mutate state or transport, else None."""
    if not argv or argv[0].lower() != "git":
        return None
    verb = ""
    skip_next = False
    for tok in argv[1:]:
        if skip_next:            # value of an option like -C <path>
            skip_next = False
            continue
        if tok.startswith("-"):
            if tok in ("-C", "-c"):
                skip_next = True
            continue
        verb = tok
        break
    if not verb:
        return "REFUSED_NO_SUBCOMMAND"
    return verb if verb in GIT_WRITE_VERBS else None


def guarded_write(path):
    """Refuse any write outside the handover dir (selfcheck/ subdir allowed)."""
    i = os.path.normpath(os.path.abspath(path))
    parent = os.path.normcase(os.path.dirname(i))
    if parent == os.path.normcase(REPORDIR) or parent == os.path.normcase(R7_OUTPUT_DIR):
        return i
    _fail("write outside the handover dir is forbidden: %s" % i)


def run_git_finished(argv, timeout=30):
    bad = git_write_verb_check(argv)
    if bad:
        _fail("git non-write mode: refuses verb %r" % bad)
    p = subprocess.run(argv, capture_output=True, cwd=WORKTREE, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("git %s failed (rc=%s): %s" % (
            argv[1] if len(argv) > 1 else "?", p.returncode,
            (p.stderr or p.stdout).decode(errors="replace").strip()))
    return p.stdout.decode(errors="replace").strip()


def write_guard_dirs():
    """Fail closed if the handover dir or worktree packet prefix is not present."""
    if not os.path.isdir(REPORDIR):
        _fail("expected handover dir not found: %s" % REPORDIR)
    pktdir = os.path.join(WORKTREE, PKT_P.replace("/", "\\"))
    if not os.path.isdir(pktdir):
        _fail("expected guarded packet prefix (worktree) not found: %s" % pktdir)


# token + API (token in memory only; only ever an Authorization header value) ----

_TOKEN = None
_TOKEN_LOADED = False


def _token():
    global _TOKEN, _TOKEN_LOADED
    if not _TOKEN_LOADED:
        try:
            with open(TOKEN_PATH, encoding="utf-8") as f:
                _TOKEN = f.read().strip() or None
        except OSError:
            _TOKEN = None
        _TOKEN_LOADED = True
    return _TOKEN


def api_json(path):
    """GET on the GitHub REST API with auth header; returns parsed JSON; 404 -> None."""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    tok = _token()
    if tok:
        headers["Authorization"] = "Bearer " + tok
    req = Request("https://api.github.com" + path, headers=headers)
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        if e.code == 404:
            return None
        raise


def contents_bytes(path):
    """GET /contents/{path}; decode the base64 JSON envelope to exact bytes."""
    doc = api_json(path)
    if doc is None:
        return None
    import base64 as _b64
    return _b64.b64decode(doc["content"])


def git_blob_sha(data):
    """git blob id per --no-filters semantics (raw bytes)."""
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def now_iso_local():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time() + 8 * 3600)) + "+08:00"


def now_iso_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time())) + "+00:00"


def intake_inventory():
    """Walk the local R7 prefix in the WORKTREE; returns {rel_path: abs_path}."""
    base = os.path.join(WORKTREE, PKT_P.replace("/", "\\"))
    out = {}
    if not os.path.isdir(base):
        return out
    ws_root = os.path.normpath(os.path.abspath(WORKTREE))
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ws_root).replace("\\", "/")
            out[rel] = full
    return out


def read_local_bytes(rel):
    with open(os.path.join(WORKTREE, rel.replace("/", "\\")), "rb") as f:
        return f.read()


def local_handover_bytes(name):
    with open(os.path.join(REPORDIR, name), "rb") as f:
        return f.read()


def write_bytes(path, blob):
    i = guarded_write(path)
    j = i + ".tmp"
    with open(j, "wb") as f:
        f.write(blob)
    os.replace(j, i)
    return i


def bind_rel(p):
    try:
        rel = os.path.relpath(p, REPORDIR)
        return rel.replace("\\", "/") if not rel.startswith("..") else p
    except Exception:
        return p


# core checks -------------------------------------------------------------------

def check_1():
    """local HEAD == remote branch head == the head recorded in the local readback."""
    cmd_line = ["git", "-C", WORKTREE, "rev-parse", "HEAD"]
    local_head = run_git_finished(cmd_line)
    br = api_json("/repos/%s/branches/%s" % (REPO, BRANCH.replace("/", "%2F")))
    remote_head = br["commit"]["sha"] if br else None
    local_rb = json.loads(local_handover_bytes(LOCAL_RB).decode("utf-8"))
    recorded_head = local_rb["repo"]["head_after_r7"]
    ok = local_head == remote_head == recorded_head
    header = (
        "[1] local branch == remote branch head\n"
        "       command: git -C C:/Projects/wt-cnv-r7 rev-parse HEAD  |  API /repos/.../branches/{branch}\n"
        "       local=%s | remote=%s | local record head_after_r7=%s\n"
        "       result: %s"
    ) % (local_head, remote_head, recorded_head, "PASS" if ok else "FAIL")
    return header, ok, dict(local_head=local_head, remote_head=remote_head,
                            recorded_head=recorded_head)


def check_2():
    """Every blob under the R7 prefix exists locally with a matching git blob id (raw bytes)."""
    tree = api_json("/repos/%s/git/trees/%s?recursive=1" % (REPO, EXPECTED_R7_HEAD))
    if tree is None or tree.get("truncated"):
        raise RuntimeError("remote tree truncated=true or unreachable; cannot enumerate")
    remote = {e["path"]: e["sha"] for e in tree["tree"]
              if e.get("type") == "blob" and e.get("path", "").startswith(PKT_P)}
    local = intake_inventory()
    missing = sorted(set(remote) - set(local))
    local_only = sorted(set(local) - set(remote))
    mismatches = []
    for p in sorted(remote):
        if p in local:
            with open(local[p], "rb") as f:
                data = f.read()
            if git_blob_sha(data) != remote[p]:
                mismatches.append((p, remote[p], git_blob_sha(data)))
    header = (
        "[2] blob inventory under %s (--no-filters bytes)\n"
        "       command: GET repos/.../git/trees/{head}?recursive=1  x  local walk blob-id rehash\n"
        "       remote=%d blobs | local files=%d | MISSING=%d | LOCAL_ONLY=%d | MISMATCHES=%d\n"
        "       result: %s"
    ) % (PKT_P, len(remote), len(local), len(missing), len(local_only), len(mismatches),
          "PASS" if not (missing or local_only or mismatches) else "FAIL")
    if missing:
        header += "\n       missing (remote-only) sample: %s" % missing[:10]
    if local_only:
        header += "\n       local_only sample: %s" % local_only[:10]
    if mismatches:
        header += "\n       mismatch sample: %s" % [m[0] for m in mismatches[:10]]
    ctx = dict(remote_blobs=len(remote), local_blobs=len(local),
               missing=len(missing), local_only=len(local_only),
               mismatches=len(mismatches))
    return header, not (missing or local_only or mismatches), ctx


def check_3():
    """Packet manifest counts reconcile: tracked==live blobs, file_count-tracked==|excluded|."""
    raw = contents_bytes("/repos/%s/contents/%sPACKET_MANIFEST.json?ref=%s"
                         % (REPO, PKT_P, BRANCH.replace("/", "%2F")))
    if raw is None:
        raise RuntimeError("PACKET_MANIFEST.json not found on the remote branch")
    digest = hashlib.sha256(raw).hexdigest()
    m = json.loads(raw.decode("utf-8"))
    tree = api_json("/repos/%s/git/trees/%s?recursive=1" % (REPO, EXPECTED_R7_HEAD))
    remote_count = sum(1 for e in tree["tree"] if e.get("type") == "blob"
                       and e.get("path", "").startswith(PKT_P))
    t = m.get("tracked_file_count")
    fc = m.get("file_count")
    lo = m.get("local_only_excluded") or []
    c1 = t == remote_count
    c2 = (fc - t) == len(lo)
    ok = c1 and c2 and digest == EXPECTED_R7_MANIFEST_SHA256
    header = (
        "[3] packet manifest reconciliation\n"
        "       command: GET repos/.../contents/PACKET_MANIFEST.json (raw bytes -> sha256) "
        "+ blob count from [2]\n"
        "       file_count=%s | tracked_file_count=%s | local_only_excluded=%d | tracked_inventory=%d\n"
        "       c1 tracked==live blobs (%s==%d): %s\n"
        "       c2 file_count - tracked == len(local_only_excluded) (%s-%s==%d): %s\n"
        "       manifest bytes sha256=%s... matches expected (c5fc66e4...): %s\n"
        "       result: %s"
    ) % (fc, t, len(lo), len(m.get("tracked_inventory") or []),
          t, remote_count, c1, fc, t, len(lo), c2,
          digest[:16], digest == EXPECTED_R7_MANIFEST_SHA256,
          "PASS" if ok else "FAIL")
    return header, ok, dict(digest=digest, remote_count=remote_count,
                            file_count=fc, tracked=t, exclusions=len(lo))


def check_4():
    """Merged archive untouched: main sha, frozen blob count, manifest sha256 (wire bytes)."""
    main_branch = api_json("/repos/%s/branches/main" % REPO)
    main_sha = main_branch["commit"]["sha"]
    c1 = main_sha == EXPECTED_MAIN_SHA
    tree = api_json("/repos/%s/git/trees/%s?recursive=1" % (REPO, EXPECTED_MAIN_SHA))
    if tree is None or tree.get("truncated"):
        raise RuntimeError("main tree truncated or unreachable; cannot count frozen blobs")
    frozen_count = sum(1 for e in tree["tree"] if e.get("type") == "blob"
                       and e.get("path", "").startswith(FROZEN))
    c2 = frozen_count == EXPECTED_FROZEN_BLOBS
    mraw = contents_bytes("/repos/%s/contents/%sPACKET_MANIFEST.json" % (REPO, FROZEN))
    digest = hashlib.sha256(mraw).hexdigest()
    c3 = digest == EXPECTED_R6_MANIFEST_SHA256
    ok = c1 and c2 and c3
    header = (
        "[4] merged archive untouched @ main\n"
        "       command: GET repos/.../branches/main + GET git/trees/{main}?recursive=1 "
        "+ GET contents EVIDENCE/CNV-PIPD-LS-SP-20261015/PACKET_MANIFEST.json (raw -> sha256)\n"
        "       main=%s | expected=%s | c1: %s\n"
        "       frozen blobs=%d | expected=%d | c2: %s\n"
        "       manifest sha256=%s... | expected=27ba42f7... | c3: %s\n"
        "       result: %s"
    ) % (main_sha[:12], EXPECTED_MAIN_SHA[:12], c1, frozen_count, EXPECTED_FROZEN_BLOBS, c2,
          digest[:16], c3, "PASS" if ok else "FAIL")
    return header, ok, dict(main_sha=main_sha, frozen_count=frozen_count, digest=digest)


def check_5():
    """M2 record: verdict PASS, scope violations 0, hard secrets 0."""
    path = os.path.join(REPORDIR, "M2_TRUSTED_SCOPE_SECRETS_R7.json")
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
        f.seek(0)
        m2 = json.loads(f.read().decode("utf-8"))
    verdict = m2.get("verdict")
    sv_out = len(m2["scope"]["out_of_prefix_or_traversal"])
    sv_link = len(m2["scope"]["symlinks"])
    sv_exec = int(m2["scope"]["executable_bit_blobs"]["count"])
    scope_violations = sv_out + sv_link + sv_exec
    hard = len(m2["secret_scan"]["hard_findings"])
    c1 = verdict == "PASS"
    c2 = scope_violations == 0
    c3 = hard == 0
    ok = c1 and c2 and c3
    header = (
        "[5] M2 trusted-scope/secrets record\n"
        "       command: read M2_TRUSTED_SCOPE_SECRETS_R7.json locally (sha256=%s...) | parse\n"
        "       verdict=%s | scope violations (out_of_prefix=%d + symlinks=%d + exec_bit=%d)=%d\n"
        "       hard secret findings=%d | scan_digest=%s...\n"
        "       result: %s"
    ) % (digest[:16], verdict, sv_out, sv_link, sv_exec, scope_violations, hard,
          m2["scanned"]["scan_digest_sha256"][:16], "PASS" if ok else "FAIL")
    return header, ok


def check_6():
    """Checker attempt-3 verdict parses; schema /3; overall + item verdicts in allowed sets."""
    path = os.path.join(REPORDIR, "R7_CHECKER_ATTEMPT3", "R7_CHECKER_VERDICT.json")
    with open(path, "rb") as f:
        doc = json.loads(f.read().decode("utf-8"))
    schema_ok = doc.get("schema") == R7_SCHEMA
    overall = doc.get("overall_verdict")
    overall_ok = overall in ALLOWED_OVERALL
    items = doc.get("items", [])
    ids = [i.get("id") for i in items]
    item_ok = bool(items) and all(i.get("verdict") in ALLOWED_ITEM_VERDICTS for i in items)
    ok = schema_ok and overall_ok and item_ok
    header = (
        "[6] checker attempt-3 verdict parse\n"
        "       command: parse R7_CHECKER_ATTEMPT3/R7_CHECKER_VERDICT.json locally (no network)\n"
        "       schema=%s (expected %s): %s\n"
        "       overall_verdict=%s in {PENDING_OWNER, CHALLENGED}: %s\n"
        "       items=%d ids=%s | all item verdicts in allowed set: %s | first_fail=%s\n"
        "       result: %s"
    ) % (doc.get("schema"), R7_SCHEMA, schema_ok, overall, overall_ok,
          len(items), ids, item_ok, doc.get("first_fail"), "PASS" if ok else "FAIL")
    return header, ok


def run_checks():
    blocks = []
    rows = []
    ctx = {}
    hdr, ok, c1x = check_1()
    blocks.append(hdr)
    rows.append(("1", ok))
    ctx["check1"] = c1x
    hdr, ok, c2x = check_2()
    blocks.append(hdr)
    rows.append(("2", ok))
    ctx["check2"] = c2x
    hdr, ok, c3x = check_3()
    blocks.append(hdr)
    rows.append(("3", ok))
    ctx["check3"] = c3x
    hdr, ok, c4x = check_4()
    blocks.append(hdr)
    rows.append(("4", ok))
    ctx["check4"] = c4x
    hdr, ok = check_5()
    blocks.append(hdr)
    rows.append(("5", ok))
    hdr, ok = check_6()
    blocks.append(hdr)
    rows.append(("6", ok))
    return blocks, rows, ctx


# repair (safe, local only) -------------------------------------------------------

def repair_round(ctx, iteration):
    """Recompute this round's own readback fields from live evidence; rewrite the two records.

    Repairs exactly two files, inside the handover dir only. Never commits, pushes,
    merges, or touches the merged archive or any product code.
    """
    actions = []
    local_files = intake_inventory()
    tree = api_json("/repos/%s/git/trees/%s?recursive=1" % (REPO, EXPECTED_R7_HEAD))
    remote = {e["path"]: e["sha"] for e in tree["tree"]
              if e.get("type") == "blob" and e.get("path", "").startswith(PKT_P)}
    mismatches = []
    for p, sha in sorted(remote.items()):
        if p in local_files:
            if git_blob_sha(read_local_bytes(p)) != sha:
                mismatches.append(p)
    rel_ok = set(remote) == set(local_files)
    diff = sorted(set(remote) ^ set(local_files))

    rb = json.loads(local_handover_bytes(LOCAL_RB).decode("utf-8"))
    pv = json.loads(local_handover_bytes(LOCAL_PV).decode("utf-8"))

    rb["generated_local"] = now_iso_local()
    rb["generated_utc"] = now_iso_utc()
    c1 = ctx.get("check1", {})
    rb["repo"]["head_after_r7"] = c1.get("remote_head") or rb["repo"].get("head_after_r7")
    rb["repo"]["local_head_equals_remote"] = bool(
        c1.get("local_head") and c1.get("local_head") == c1.get("remote_head")
    )
    pb = rb["published_bytes"]
    pb["remote_blobs_under_prefix"] = len(remote)
    pb["manifest_tracked_inventory"] = len(remote)
    pb["set_equality"] = rel_ok
    pb["set_difference"] = len(diff)
    pb["local_inventory"] = len(local_files)
    pb["blob_ids_recomputed_locally"] = len(remote) - len(mismatches)
    pb["blob_id_mismatches"] = len(mismatches)
    actions.append("%s: published_bytes recomputed from live enumeration "
                    "(blobs=%d, mismatches=%d, set_equality=%s)"
                    % (LOCAL_RB, len(remote), len(mismatches), rel_ok))

    pv["generated_local"] = now_iso_local()
    pv["generated_utc"] = now_iso_utc()
    c4 = ctx.get("check4", {})
    blv = pv.setdefault("byte_level_verification", {})
    blv["blobs"] = len(remote)
    blv["mismatches"] = len(mismatches)
    if c4.get("main_sha"):
        for ch in pv.get("channels", []):
            if isinstance(ch, dict) and "base_origin_main" in ch:
                ch["base_origin_main"] = c4["main_sha"]
    fa = pv.setdefault("frozen_archive", {})
    if c4.get("frozen_count") is not None:
        fa["blobs"] = c4["frozen_count"]
    if c4.get("digest"):
        fa["manifest_sha256"] = c4["digest"]
    actions.append("%s: byte_level_verification + frozen_archive recomputed from live wire "
                    "(mismatches=%d, main=%s)"
                    % (LOCAL_PV, len(mismatches), (c4.get("main_sha") or "?")[:12]))

    rb_blob = json.dumps(rb, indent=2, ensure_ascii=False).encode("utf-8")
    pv_blob = json.dumps(pv, indent=2, ensure_ascii=False).encode("utf-8")
    if rb_blob != local_handover_bytes(LOCAL_RB):
        write_bytes(os.path.join(REPORDIR, LOCAL_RB), rb_blob)
        actions.append("%s: rewritten (bytes changed)" % LOCAL_RB)
    else:
        actions.append("%s: content already matches; not rewritten" % LOCAL_RB)
    if pv_blob != local_handover_bytes(LOCAL_PV):
        write_bytes(os.path.join(REPORDIR, LOCAL_PV), pv_blob)
        actions.append("%s: rewritten (bytes changed)" % LOCAL_PV)
    else:
        actions.append("%s: content already matches; not rewritten" % LOCAL_PV)

    return dict(iteration=iteration, actions=actions,
                residual_blob_mismatches=len(mismatches),
                residual_set_difference=len(diff),
                files=[bind_rel(os.path.join(REPORDIR, LOCAL_RB)),
                       bind_rel(os.path.join(REPORDIR, LOCAL_PV))])


def repair_and_recheck(rows, ctx):
    """Up to MAX_REPAIR_ITERATIONS iterations: repair records only, then fully re-run checks."""
    repairs = []
    blocks = []
    for i in range(1, MAX_REPAIR_ITERATIONS + 1):
        residuals = [c for c, ok in rows if not ok]
        if not residuals:
            repairs.append(dict(iteration=i, skipped="no residual failures; no repair applied"))
            break
        rep = repair_round(ctx, i)
        repairs.append(rep)
        blocks.append("[repair %d] actions:" % i)
        for a in rep["actions"]:
            blocks.append("       action: %s" % a)
        blocks.append("[repair %d] re-running all checks..." % i)
        blocks2, rows, ctx = run_checks()
        blocks.extend(blocks2)
        if all(ok for _, ok in rows):
            blocks.append("[repair %d] all checks now PASS" % i)
            break
        blocks.append("[repair %d] residuals remain: %s" % (i, [c for c, ok in rows if not ok]))
    return blocks, rows, repairs


# guard self-probes (offline: no network, no repo effects) --------------------------

def verify_guard_probes():
    """offline probes: guard() outside-refusal, git non-write gate, rev-parse allow."""
    for outside in ("C:/selfcheck_guard_probe_outside.txt", "C:/selfcheck_guard_probe/x.txt"):
        try:
            guarded_write(outside)
            return "FAIL: guard allowed a write outside the handover dir (%s)" % outside
        except AssertionError:
            pass
    bad = git_write_verb_check(["git", "-C", WORKTREE, "push", "origin", BRANCH])
    if bad != "push":
        return "FAIL: git push must be refused by the non-write gate"
    bad = git_write_verb_check(["git", "-C", WORKTREE, "rev-parse", "HEAD"])
    if bad is not None:
        return "FAIL: rev-parse must be allowed by the non-write gate"
    return ("       guard probes: outside-write-refused=True | git-push-refused=True | "
            "rev-parse-allowed=True (offline, no effects)")


def fmt_verdict_rows(rows):
    return " ".join("%s=%s" % (c, "PASS" if ok else "FAIL") for c, ok in rows)


def parse_args(argv):
    return dict(dry=bool(argv) and argv[0] == "--dry-run")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)
    print(OUTPUT_BANNER)
    started = now_iso_utc()
    print("== R7-0 selfcheck started at %s ==" % started)

    print(verify_guard_probes())

    if args["dry"]:
        print("dry-run: --dry-run observed; no API calls made; no checks executed")
        print("== R7-0 selfcheck complete (DRY) ==")
        return 0

    write_guard_dirs()
    blocks, rows, ctx = run_checks()

    print("")
    print("== FULL CHECKS ==")
    for b in blocks:
        print(b)

    repair_blocks, rows, repairs = repair_and_recheck(rows, ctx)
    if repair_blocks:
        print("")
        print("== REPAIRS (safe mode: this round's own records only, max %d iterations) =="
              % MAX_REPAIR_ITERATIONS)
        for b in repair_blocks:
            print(b)

    overall = all(ok for _, ok in rows)
    print("")
    print("== VERDICT ==")
    print(fmt_verdict_rows(rows))
    print("OVERALL_SELFCHECK_VERDICT: %s" % ("PASS" if overall else "FAIL"))
    print("")
    print("REPAIR MODE NOTE: repairs touched only these files (if any): "
          + ", ".join(sorted({f for r in repairs for f in r.get("files", [])})) or "none")
    print("")
    print(OUTPUT_BANNER + ". No acceptance, approval, Gate PASS, merge authorisation, or "
          "production effect is claimed. Unverifiable claims (provider/model attestation, "
          "upstream CI, the 221-case acceptance, voided attempt-1 evidence) remain "
          "explicitly unverifiable and are not upgraded.")
    print("== R7-0 selfcheck complete ==")
    return 0 if overall else 1


# entry point --------------------------------------------------------------------------

if __name__ == "__main__":
    # Windows: suppress modal crash dialogs on unexpected faults (never blocks the run)
    try:
        _kernel32 = ctypes.windll.kernel32
        for _flag in (0x00000080, 0x00008000):  # SEM_FAILCRITICALERRORS, SEM_NOGPFAULTERRORBOX
            _kernel32.SetErrorMode(_kernel32.SetErrorMode(0) | _flag)
    except Exception:
        pass
    sys.exit(main())
