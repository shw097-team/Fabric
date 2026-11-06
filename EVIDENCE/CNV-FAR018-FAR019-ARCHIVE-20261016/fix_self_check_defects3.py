"""Third self-check repair pass — both causes now measured, not guessed.

(a) C02 re-parsed an already-parsed dict: the loader json.loads() every .txt receipt, so `d[...]` IS the
    verb dict and `json.loads(t)` raised TypeError into the "UNPARSEABLE" path.  A check failed because of
    the harness's own double-parse, not because of a gate.
(b) M14's TypeError came from `dict.get(k, "-")[:12]`: `.get` falls back only on a MISSING key, never on a
    present-but-null value, so a nulled merge sha produced `None[:12]`.  Same shape as the M13 mutation.
"""
import io
import ast

p = "archive_closure.py"
s = io.open(p, encoding="utf-8").read()

a1 = ('        t = d.get("compiler/%s.stdout.txt" % v)\n'
      '        try:\n'
      '            verbs[v] = json.loads(t.lstrip("\\ufeff")).get("verdict") if t else None\n'
      '        except Exception:  # noqa: BLE001\n'
      '            verbs[v] = "UNPARSEABLE"')
b1 = ('        # the loader already json.loads() every receipt, so t is the verb dict itself.\n'
      '        t = d.get("compiler/%s.stdout.txt" % v)\n'
      '        verbs[v] = t.get("verdict") if isinstance(t, dict) else None')
assert a1 in s, "(a) verb line not found"
s = s.replace(a1, b1, 1)

a2 = ('                "main tip=%s equals PR14 merge commit=%s (%s)" % (str(MAIN_TIP)[:12],\n'
      '                                                                  a08["prs"]["14"].get("merge_commit_sha", "-")[:12],\n'
      '                                                                  MAIN_EQ)))')
b2 = ('                "main tip=%s equals PR14 merge commit=%s (%s)" % (str(MAIN_TIP)[:12],\n'
      '                                                                  (a08["prs"]["14"].get("merge_commit_sha") or "-")[:12],\n'
      '                                                                  MAIN_EQ)))')
assert a2 in s, "(b) C12 detail not found"
s = s.replace(a2, b2, 1)

ast.parse(s)
io.open(p, "w", encoding="utf-8").write(s)
print("patched", p)
