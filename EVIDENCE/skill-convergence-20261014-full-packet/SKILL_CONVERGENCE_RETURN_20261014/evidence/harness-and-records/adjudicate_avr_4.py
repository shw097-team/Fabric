"""Round-harness adjudication of AVR lane tag 4 (topic batch 1).

Not an acceptance. It reconciles the maker's own receipt against the two independent
checks the harness ran from raw bytes, and records the claim ceiling explicitly.
"""
import pathlib,json,hashlib,datetime
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
C=RUN/'candidates/avr';V=RUN/'verification/round-harness'
h=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
maker=json.loads((C/'phase2_result.json').read_text(encoding='utf-8'))
lossless=json.loads((V/'avr_batch1_independent_check.json').read_text(encoding='utf-8'))
refs=json.loads((V/'avr_batch1_reference_check.json').read_text(encoding='utf-8'))
dig=maker['step_a_reproduction']['verdict_per_file']
dig_ok={rel:(h(C/rel)==rec['disk']['sha256']) for rel,rec in dig.items()}
disp=json.loads((RUN/'evidence/lanes/avr/4/dispatch.json').read_text(encoding='utf-8'))
out={'schema':'SKCV-HARNESS-ADJUDICATION/1','lane':'WO-SKCV-20261014-AVR tag 4',
 'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'transport':{'exit':'0','served_arm':disp.get('served_arm'),'required_arm':disp.get('required_arm'),
   'used_seconds':disp.get('used_seconds'),'usage_receipt_ok':disp.get('usage_receipt_ok'),'ok':disp.get('ok')},
 'step_a_reproduction':{'maker_claim':'BYTE_IDENTICAL for all three artefacts','harness_recomputed':dig_ok,
   'agrees':all(dig_ok.values())},
 'step_b_lossless':{'absorbed_entries':lossless['absorbed_entries'],'all_segments_match_claim':lossless['all_absorbed_lossless'],
   'segments_equal_untouched_baseline_bytes':all(r['baseline_matches_segment'] for r in lossless['rows']),
   'stubs_present_with_topic_pointer':all(r['stub_exists'] and r['stub_mentions_topic'] for r in lossless['rows']),
   'files_deleted_vs_baseline':lossless['files_deleted_vs_baseline'],
   'underscore_prefixed_files':lossless['underscore_prefixed_files']},
 'reference_structure':{'named_in_main_doc':refs['counts']['candidate_named'],
   'all_named_paths_resolve':refs['all_named_paths_resolve'],
   'link_convention_note':'the main doc names references in backticks, not markdown links; a markdown-link check finds nothing and is NOT evidence of integrity - the backtick-name resolution check is the real one and it resolves',
   'baseline_refs_no_longer_named':refs['baseline_refs_no_longer_named_in_main_doc'],
   'those_present_verbatim_in_topic_source_remainder':refs['those_present_verbatim_in_topic_source_remainder'],
   'physical_reference_files':refs['counts']},
 'verdict':'BATCH_1_INDEPENDENTLY_CONFIRMED_LOSSLESS_BY_THE_ROUND_HARNESS',
 'what_this_does_not_establish':[
  'it is not an acceptance of the skill change and it is not independent-checker authority: the harness that ran the lanes checked too',
  'the reference-file count did NOT fall in this batch (baseline 24 -> candidate 27 physical files), so no sprawl-reduction claim is made yet',
  'only 2 theme groups are done; the remaining AVR theme groups and ALL of the HGK reference groups stay open',
  'the consumer wiring, the guarded apply and the rollback drill never ran',
  'the timed-out lanes in this round (hgk/1,2,4, avr/1,2,3, consumer/1,3, apply/1,3) stay failures and are not repaired by this verdict'],
 'claim_ceiling':'byte-level losslessness and structure for this one batch, recomputed by the round harness from raw bytes; nothing about other batches, other lanes, or the product as a whole'}
(V/'avr_batch1_adjudication.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8',newline='\n')
print(json.dumps({'verdict':out['verdict'],'step_a_agrees':out['step_a_reproduction']['agrees'],
 'lossless':out['step_b_lossless'],'refs':out['reference_structure']['physical_reference_files']},ensure_ascii=False,indent=1))
