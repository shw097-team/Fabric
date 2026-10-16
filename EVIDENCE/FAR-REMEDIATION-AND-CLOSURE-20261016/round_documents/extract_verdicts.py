"""Extract each lane attempt's final CHECKER-VERDICT agent_message from the codex event stream into a
plain JSON file next to the attempt, so the closure builder reads a real artifact instead of scraping.

Codex streams newline-delimited events; the verdict is the text of the last `item.completed` event whose
item.type == 'agent_message' and whose text contains the verdict schema tag.
"""
import glob
import json
import pathlib
import sys

O = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-REMEDIATION-AND-CLOSURE-20261016')
TAGS = ('HGK-CHECKER-VERDICT', '"verdict"')
written = []


def verdicts_in(path):
    found = []
    for line in pathlib.Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        s = line.strip()
        if not s.startswith('{'):
            continue
        try:
            o = json.loads(s)
        except Exception:
            continue
        item = o.get('item') if isinstance(o.get('item'), dict) else None
        if not item or item.get('type') != 'agent_message':
            continue
        text = item.get('text')
        if not isinstance(text, str):
            continue
        if any(t in text for t in TAGS):
            found.append(text)
    return found


for raw in sorted(glob.glob(str(O / 'lanes' / '*' / '*' / 'raw' / '*stdout*'))):
    rp = pathlib.Path(raw)
    attempt_dir = rp.parent.parent
    got = verdicts_in(rp)
    if not got:
        continue
    body = got[-1]
    parsed = None
    try:
        parsed = json.loads(body)
    except Exception:
        # the brief requires the verdict to be one JSON line FOLLOWED by the transport token line, so
        # slice out the outermost object instead of failing the whole extraction
        i, j = body.find('{'), body.rfind('}')
        if i >= 0 and j > i:
            try:
                parsed = json.loads(body[i:j + 1])
            except Exception:
                parsed = None
    if parsed is None:
        parsed = {'_unparsed_text': body[:20000]}
    dest = attempt_dir / 'CHECKER_VERDICT.json'
    dest.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding='utf-8')
    written.append({'attempt': str(attempt_dir.relative_to(O / 'lanes')).replace('\\', '/'),
                    'chars': len(body),
                    'parsed': '_unparsed_text' not in parsed,
                    'claim_B': (parsed.get('claim_B') or {}).get('verdict'),
                    'claim_C': (parsed.get('claim_C') or {}).get('verdict'),
                    'named_suite': (parsed.get('named_suite') or {}).get('status'),
                    'dest': str(dest)})
print(json.dumps({'written': written, 'count': len(written)}, ensure_ascii=False, indent=1))
sys.exit(0)
