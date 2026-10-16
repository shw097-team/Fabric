"""R7 — cross-field declaration agreement: the class of defect check_drift cannot see.

check_drift compares each projection pointer against the value at that pointer. Two fields in the SAME
file may therefore contradict each other while every pointer is individually satisfied — which is exactly
what config/model-lane-assignment.json did: lane_chains.VERIFY_SECURITY[0] named arm A as
openai-codex/gpt-6.1-sol (and the registry's projections on that pointer pinned it) while five sibling
sod.* prose fields named arm A as opencode-go/glm-5.3-flash, and check_drift reported ZERO fatal findings
in that state.

This is the detector for that class. It is run against BOTH states — the pre-change snapshot preserved on
disk as the .bak file, and the canonical file — so the finding is demonstrated rather than asserted.

Usage: check_declaration_agreement.py <path-to-model-lane-assignment.json> [label]
"""
import json
import pathlib
import re
import sys

MODELS = ['deepseek-ai/deepseek-v4.1-flash', 'deepseek-v4.1-flash', 'gpt-6-luna', 'gpt-6.1-sol',
          'glm-5.3-flash']
# prose fields that are DECLARED to name one lane's default arm
SINGLE = {'/sod/plan_lane': 'PLAN',
          '/sod/verify_security_lane': 'VERIFY_SECURITY',
          '/sod/verify_security_default_arm': 'VERIFY_SECURITY',
          '/sod/verify_security_arm_A': 'VERIFY_SECURITY'}
DEFAULT_MARKERS = ['default primary arm a =', 'arm a =', 'a = ']


def get(doc, ptr):
    cur = doc
    for p in [x for x in ptr.split('/') if x]:
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    return cur


def claimed_default(text):
    """The claimed default is the model named FIRST after a default marker, by POSITION.

    Taking the first match in MODELS order instead is a bug: in the pre-change text
    'DEFAULT primary arm A = opencode-go / glm-5.3-flash; NON-DEFAULT ... arm B = openai-codex /
    gpt-6.1-sol' a list-ordered search returns gpt-6.1-sol and reports AGREES, hiding the very
    contradiction this detector exists to find. Position wins.
    """
    low = text.lower()
    for m in DEFAULT_MARKERS:
        i = low.find(m)
        if i >= 0:
            tail = text[i + len(m):]
            hits = [(tail.find(tok), tok) for tok in MODELS if tok in tail]
            if hits:
                return min(hits)[1], m
    hits = [(text.find(tok), tok) for tok in MODELS if tok in text]
    return (min(hits)[1], 'first model token') if hits else (None, 'none')


def chain_default(doc, lane):
    c = doc['lane_chains'][lane][0]
    return '%s/%s' % (c.get('provider'), c.get('model')), c.get('model')


def run(path, label):
    doc = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    out = {'label': label, 'path': str(path), 'findings': [], 'info': []}
    for ptr, lane in SINGLE.items():
        text = get(doc, ptr)
        chain_str, chain_model = chain_default(doc, lane)
        claimed, via = claimed_default(text)
        out['findings'].append({'pointer': ptr, 'lane': lane, 'chain_default': chain_str,
                                'claimed_default': claimed, 'parsed_via': via,
                                'verdict': 'AGREES' if claimed == chain_model else 'CONTRADICTS_THE_CHAIN'})
    for ptr in ('/sod/verify_vs_plan_model_separation', '/sod/provider_separation',
                '/sod/provider_separation_status', '/sod/maker_self_acceptance'):
        text = get(doc, ptr)
        out['info'].append({'pointer': ptr, 'model_tokens_present': [t for t in MODELS if t in text],
                           'rule': 'multi-lane prose: listed, not strictly judged'})
    out['contradictions'] = sum(1 for f in out['findings'] if f['verdict'] != 'AGREES')
    return out


if __name__ == '__main__':
    results = [run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'unnamed')]
    print(json.dumps(results[0], ensure_ascii=False, indent=1))
    for f in results[0]['findings']:
        print('%-42s %-16s chain=%-28s claimed=%-18s %s' % (f['pointer'], f['lane'],
                                                            f['chain_default'], f['claimed_default'],
                                                            f['verdict']))
    print('CONTRADICTIONS =', results[0]['contradictions'])
