"""Fix three defects the round's OWN self-check exposed, plus the receipt field they exposed.

C02 compared the hash verb's digest of the contract FILE with the compiler report's digest of its own
normalised contract — two different quantities.  C04/C12 compared the live merge sha against a receipt
field the idempotent RERUN path never populated.  C09 was VACUOUS: `all(s in recent for s in mshas if s)`
is TRUE over an empty list, so it passed while every sha was None.  Each fixed check also gets a mutation
that must be detected, so none of them can pass for the wrong reason.
"""
import io
import ast


def edit(path, pairs):
    s = io.open(path, encoding="utf-8").read()
    for o, n in pairs:
        assert o in s, "NOT FOUND in %s: %r" % (path, o[:80])
        s = s.replace(o, n, 1)
    ast.parse(s)
    io.open(path, "w", encoding="utf-8").write(s)
    print("patched", path)


edit("archive_merge.py", [(
    '        step("merge", result="SKIPPED_ALREADY_MERGED", merge_commit_sha=pr.get("merge_commit_sha"))\n'
    '        rec["status"] = "ALREADY_MERGED_READBACK_ONLY"',
    '        rec["merge_commit_sha"] = pr.get("merge_commit_sha")\n'
    '        step("merge", result="SKIPPED_ALREADY_MERGED", merge_commit_sha=rec["merge_commit_sha"],\n'
    '             note="merge sha read from the LIVE PR, not carried from a first-run artifact")\n'
    '        rec["status"] = "ALREADY_MERGED_READBACK_ONLY"')])

edit("archive_closure.py", [
    ('                             "compiler/hash.stdout.txt")}',
     '                             "compiler/hash.stdout.txt", "compiler/lint.stdout.txt",\n'
     '                             "compiler/activation.stdout.txt", "compiler/acceptance.stdout.txt",\n'
     '                             "compiler/compile.stdout.txt", "compiler/duplication.stdout.txt")}'),
    ('    out.append(("C02", rep.get("verdict") == "PROMPT_COMPILE_PASS" and rep.get("error_count") == 0\n'
     '                and str(d["compiler/hash.stdout.txt"]).strip() == rep.get("contract_sha256"),\n'
     '                "compiler verdict=%s errors=%s contract_sha=%s" % (rep.get("verdict"), rep.get("error_count"),\n'
     '                                                                   str(rep.get("contract_sha256"))[:12])))',
     '    verbs = {}\n'
     '    for v in ("lint", "activation", "acceptance", "compile"):\n'
     '        t = d.get("compiler/%s.stdout.txt" % v)\n'
     '        try:\n'
     '            verbs[v] = json.loads(t).get("verdict") if t else None\n'
     '        except Exception:  # noqa: BLE001\n'
     '            verbs[v] = "UNPARSEABLE"\n'
     '    out.append(("C02", rep.get("verdict") == "PROMPT_COMPILE_PASS" and rep.get("error_count") == 0\n'
     '                and len(verbs) == 4 and all(x == "PROMPT_COMPILE_PASS" for x in verbs.values()),\n'
     '                "report=%s errors=%s verbs=%s report_digest=%s file_digest=%s"\n'
     '                % (rep.get("verdict"), rep.get("error_count"), verbs, str(rep.get("contract_sha256"))[:10],\n'
     '                   str(d["compiler/hash.stdout.txt"]).strip()[:10])))'),
    ('    c4_ok = all(merged[n].get("merged") is True and merged[n].get("merge_commit_sha")\n'
     '                == a08["prs"][str(n)].get("merge_commit_sha") for n in (12, 13, 14))',
     '    c4_shas = {n: a08["prs"][str(n)].get("merge_commit_sha") for n in (12, 13, 14)}\n'
     '    c4_ok = (all(merged[n].get("merged") is True for n in (12, 13, 14))\n'
     '             and all(c4_shas[n] and merged[n].get("merge_commit_sha") == c4_shas[n] for n in (12, 13, 14)))'),
    ('    out.append(("C09", all(s in recent for s in mshas if s),\n'
     '                "merge commits visible in main\'s recent history: %s"\n'
     '                % {s[:8]: (s in recent) for s in mshas if s}))',
     '    c09 = len(mshas) == 3 and all(mshas) and all(s in recent for s in mshas)\n'
     '    out.append(("C09", c09, "merge commits in main\'s recent history: %s (non_null=%d)"\n'
     '                % ({str(s)[:8]: (s in recent) for s in mshas}, len([s for s in mshas if s]))))'),
    ('    ("M12", "C11", "publish failed", lambda d: d["PUBLISH_RECEIPT_ARCHIVE.json"].update({"verdict": "FAIL_REF"})),\n]',
     '    ("M12", "C11", "publish failed", lambda d: d["PUBLISH_RECEIPT_ARCHIVE.json"].update({"verdict": "FAIL_REF"})),\n'
     '    ("M13", "C04", "drop a merge sha from the receipt",\n'
     '     lambda d: d["A08_MERGE_RECEIPT.json"]["prs"]["12"].update({"merge_commit_sha": None})),\n'
     '    ("M14", "C09", "erase all merge shas",\n'
     '     lambda d: [d["A08_MERGE_RECEIPT.json"]["prs"][str(n)].update({"merge_commit_sha": None}) for n in (12, 13, 14)]),\n'
     '    ("M15", "C02", "a compiler verb stops passing",\n'
     '     lambda d: d.update({"compiler/lint.stdout.txt": json.dumps({"verdict": "PROMPT_COMPILE_BLOCKED",\n'
     '                                                                 "error_count": 2})})),\n'
     '    ("M16", "C12", "main tip is not the PR14 merge commit",\n'
     '     lambda d: d["A08_MERGE_RECEIPT.json"]["prs"]["14"].update({"merge_commit_sha": "a" * 40})),\n]'),
])
print("both files patched; run archive_merge.py --merge then archive_closure.py")
