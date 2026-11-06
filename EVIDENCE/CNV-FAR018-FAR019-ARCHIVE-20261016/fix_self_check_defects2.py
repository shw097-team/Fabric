"""Second self-check repair pass.

(a) The compiler's stdout files start with a UTF-8 BOM, so json.loads() raised and every verb read
    "UNPARSEABLE" — the check failed for a parsing reason, not for a gate reason.
(b) M14 (erase every merge sha) was NOT detected, and the mutation loop SWALLOWED the exception that
    would have explained why.  A swallowed diagnostic is how a vacuous check survives, so the loop now
    records the exception text into the mutation row and the mutation result is judged only from a real
    boolean.
"""
import io
import ast

p = "archive_closure.py"
s = io.open(p, encoding="utf-8").read()

a = '            verbs[v] = json.loads(t).get("verdict") if t else None'
b = '            verbs[v] = json.loads(t.lstrip("\\ufeff")).get("verdict") if t else None'
assert a in s, "verb parse line not found"
s = s.replace(a, b, 1)

a2 = ('    except Exception as e:  # noqa: BLE001\n'
      '        res = {"__error": type(e).__name__}\n')
b2 = ('    except Exception as e:  # noqa: BLE001\n'
      '        res = {"__error": type(e).__name__ + ": " + str(e)[:160]}\n')
assert a2 in s, "mutation exception swallow not found"
s = s.replace(a2, b2, 1)

a3 = ('        not_detected.append({"mutation": mid, "target": target, "where": where, "result": "NOT_DETECTED",\n'
      '                             "observed": res.get(target)})')
b3 = ('        not_detected.append({"mutation": mid, "target": target, "where": where, "result": "NOT_DETECTED",\n'
      '                             "observed": res.get(target), "error": res.get("__error")})')
assert a3 in s, "not_detected row not found"
s = s.replace(a3, b3, 1)

ast.parse(s)
io.open(p, "w", encoding="utf-8").write(s)
print("patched", p)
