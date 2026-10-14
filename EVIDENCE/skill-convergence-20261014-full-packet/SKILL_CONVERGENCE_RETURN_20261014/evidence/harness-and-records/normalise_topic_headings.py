"""Normalise the pilot topic headings so a heading cannot be mistaken for a live file path.

Why this exists: the pilot wrote each absorbed original's path as a level-2 heading, which keeps the name
greppable but also makes the tree mention a path that no longer exists, so the round's dangling-name
invariant reported fourteen new dangling names in generation 2. The content bytes are not touched; only the
heading lines are rewritten to name the file without the path form. The rewrite is done by the round harness,
not by the maker lane, so the maker's recorded digest for the topic file is stale and is superseded here.
"""
import pathlib,re,json,hashlib,datetime
RUN=pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014')
res_p=RUN/'candidates/hgk/remediation_result.json'
res=json.loads(res_p.read_text(encoding='utf-8'))
topic=res['topic_file']['path'];rel=topic.split('skill/',1)[-1] if 'skill/' in topic else topic
tp=RUN/'candidates/hgk/skill'/rel
before=tp.read_bytes();before_sha=hashlib.sha256(before).hexdigest()
text=before.decode('utf-8')
pat=re.compile(r'^## references/([^\n]+)$',re.M)
names=pat.findall(text)
new=pat.sub(lambda m:f'## {m.group(1)} (absorbed in generation 2; content preserved verbatim below; the original file no longer exists)',text)
after=new.encode('utf-8')
tp.write_bytes(after)
# prove the absorbed content bytes are untouched: everything except heading lines must be identical
strip=lambda s:re.sub(r'^## .*$','## <heading>',s,flags=re.M)
content_unchanged=strip(text)==strip(new)
rec={'schema':'SKCV-HARNESS-HEADING-NORMALISATION/1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'file':str(tp),'headings_rewritten':len(names),
 'bytes_before':len(before),'bytes_after':len(after),'sha256_before':before_sha,'sha256_after':hashlib.sha256(after).hexdigest(),
 'content_unchanged_excluding_heading_lines':content_unchanged,
 'maker_recorded_topic_sha256':res['topic_file'].get('sha256'),
 'maker_record_record_is_now_stale_for_this_file':True,
 'why':'a heading that reproduces a path makes the tree mention a file that no longer exists; the name is kept, the path form is not. This edit was made by the round harness after the maker lane, so the maker digest is superseded and no claim is made that the maker wrote these bytes',
 'claim_ceiling':'a heading-line normalisation with a byte-level proof that the absorbed content is unchanged; it grants no acceptance'}
(RUN/'evidence/postfreeze/heading_normalisation.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps({'headings_rewritten':len(names),'content_unchanged':content_unchanged,'bytes_before':len(before),'bytes_after':len(after)},ensure_ascii=False,indent=1))
