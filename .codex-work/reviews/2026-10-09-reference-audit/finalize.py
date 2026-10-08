import json
from pathlib import Path
import re
import shutil
import audit

path=audit.ARTICLE/'references.bib'
text=path.read_text(encoding='utf-8')
entries=audit.parse_bib(text)
edits=[]
changes=[]
for e in entries:
    for field in ['title','booktitle']:
        value=e['fields'].get(field,'')
        revised=value
        for token in ['ACM','SIGKDD','AISTATS','UKACC','CONTROL','IWA','Philippines']:
            revised=re.sub(r'(?<!\{)\b'+token+r'\b(?!\})','{'+token+'}',revised)
        if revised!=value:
            a,b=e['field_spans'][field]
            edits.append((a,b,revised))
            changes.append({'key':e['key'],'field':field,'before':value,'after':revised,'reason':'Protect proper-name or acronym capitalization in APA sentence-case rendering'})
for a,b,value in sorted(edits,reverse=True): text=text[:a]+value+text[b:]
path.write_text(text,encoding='utf-8')
chapter=audit.ARTICLE/'chapters/04_prediction_projection.tex'
shutil.copy2(chapter,audit.OUT/'04_prediction_projection.before.tex')
old=chapter.read_text(encoding='utf-8')
assert old.count(r'\ref{ch:theory}')==2
chapter.write_text(old.replace(r'\ref{ch:theory}',r'\ref{ch:foundations}'),encoding='utf-8')

report=json.loads((audit.OUT/'audit-final.json').read_text(encoding='utf-8'))
report['changes'].extend(changes)
report['summary']['references_corrected']=len({x['key'] for x in report['changes']})
report['cross_reference_corrections']=[{'file':'article/chapters/04_prediction_projection.tex','old':'ch:theory','new':'ch:foundations','occurrences':2}]
report['publication_list_checks']={'Selerio2026':'Crossref DOI 10.1016/j.dche.2026.100329 verified','SelerioSSRN2026':'Crossref DOI 10.2139/ssrn.7567818 verified; publication-list entries remain separate from cited References'}
for item in report['references']:
    for change in changes:
        if change['key']==item['key']: item.setdefault('corrections',{})[change['field']]=change['after']
for target in [audit.OUT/'audit-final.json',audit.ARTICLE/'manuscript.reference-audit.json']:
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

# Rerun coverage and metadata checks after all edits.
updated=audit.parse_bib(path.read_text(encoding='utf-8'))
keys={e['key'] for e in updated}
sources=audit.read_sources()
citations={k.strip() for s in sources.values() for match in re.findall(r'\\(?:cite[A-Za-z]*|nocite)\*?(?:\[[^\]]*\])*\{([^}]+)\}',s) for k in match.split(',')}
assert keys==citations
assert len(keys)==len(updated)==146
assert all(e['fields'].get('title') and e['fields'].get('year') and (e['fields'].get('author') or e['fields'].get('editor')) for e in updated)
doi_values=[e['fields']['doi'].lower() for e in updated if e['fields'].get('doi')]
assert len(doi_values)==len(set(doi_values))
all_source='\n'.join(sources.values())
labels=set(re.findall(r'\\label\{([^}]+)\}',all_source))
refs=set(re.findall(r'\\(?:ref|eqref|cref|Cref)\{([^}]+)\}',all_source))
assert refs<=labels, refs-labels
validation={'included_source_files':len(sources),'cited_keys':len(citations),'bibliography_entries':len(updated),'missing_citation_keys':sorted(citations-keys),'uncited_entries':sorted(keys-citations),'missing_cross_reference_labels':sorted(refs-labels),'references_with_doi':len(doi_values),'citation_keys_preserved':True}
(audit.OUT/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
print(json.dumps(validation,indent=2))
