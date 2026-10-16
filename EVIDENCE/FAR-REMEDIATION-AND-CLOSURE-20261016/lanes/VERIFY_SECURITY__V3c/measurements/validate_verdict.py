import json
from pathlib import Path

work = Path(__file__).resolve().parent.parent
verdict = json.loads((work / 'CHECKER_VERDICT.json').read_text(encoding='utf-8'))
details = json.loads((work / 'TEST_RESULTS/details.json').read_text(encoding='utf-8'))
final = json.loads((work / 'TEST_RESULTS/final_checks.json').read_text(encoding='utf-8'))
suites = json.loads((work / 'TEST_RESULTS/whole_with_path.json').read_text(encoding='utf-8'))
assert [claim['id'] for claim in verdict['claims']] == ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7']
assert all(claim['verdict'] in ('AGREE', 'DISAGREE', 'UNCERTAIN') and claim['why'] and claim['evidence'] for claim in verdict['claims'])
assert final['candidate_files_checked'] == 200 and not final['candidate_mismatches']
assert details['SC1_reconstructed']['matches_recorded_before']
added = sorted(set(suites['after']['names']) - set(suites['before']['names']))
removed = sorted(set(suites['before']['names']) - set(suites['after']['names']))
assert not added and len(removed) == 1 and 'test_registry_and_projection_shape' in removed[0]
assert len(suites['after']['names']) == 46 and len(suites['before']['names']) == 47
print(json.dumps({'verdict_schema': 'valid', 'candidate_entries_match': 200, 'incomplete_reconstruction_hashes_match': True, 'paired_added': added, 'paired_removed': removed, 'counts_after': suites['after']['status'], 'counts_before': suites['before']['status']}))
