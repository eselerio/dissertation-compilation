import collections
import json
import re
from pathlib import Path
from build_bibliography import ROOT, WORK, bib_entries, field

paths=[ROOT/'article/manuscript.tex',*sorted((ROOT/'article/chapters').glob('*.tex'))]
texts={str(p.relative_to(ROOT)):p.read_text(encoding='utf8') for p in paths}
main='\n'.join(texts.values())
entries=bib_entries((ROOT/'article/references.bib').read_text(encoding='utf8'))
records=json.loads((WORK/'bibliography_records.json').read_text(encoding='utf8'))
aliases=json.loads((WORK/'citation_aliases.json').read_text(encoding='utf8'))
aliases.update({'YuanLin2006':'Yuan2006','ZouHastie2005':'Zou2005','Smola2004':'SmolaScholkopf2004','SturmCappaWexler2023':'Sturm2023','Viering2023':'VieringLoog2023'})
citations=[]
for path,t in texts.items():
    for match in re.finditer(r'\\cite(?:t|p|alt|alp|author|year)?\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}',t):
        citations.extend((k.strip(),path,t.count('\n',0,match.start())+1) for k in match[1].split(','))
source_keys={k for k,v in records.items() if v['sources']!=['existing']}
cited={k for k,_,_ in citations}
labels=re.findall(r'\\label\{([^}]+)\}',main)
refs=re.findall(r'\\(?:ref|eqref|cref|Cref)\{([^}]+)\}',main)
problems={}
for path,t in texts.items():
    hits=[]
    for num,line in enumerate(t.splitlines(),1):
        if re.search(r'activated-sludge|wastewater-treatment|machine-learning|\bTODO\b|\bTBD\b|\bcodebase\b|\brepository\b|\bscript(?:s)?\b|\bversion\b|\bmanifest\b|\\chapter\*?\{Results|\\section\*?\{Results',line,re.I):hits.append({'line':num,'text':line})
    if hits:problems[path]=hits
out={
    'chapters':len(re.findall(r'\\chapter\{',main)),
    'bibliography_entries':len(entries),
    'component_reference_count':len(source_keys),
    'source_counts':dict(collections.Counter(s for v in records.values() for s in v['sources'] if s!='existing')),
    'citation_instances':len(citations),
    'unique_cited':len(cited),
    'undefined_citations':sorted(cited-set(entries)),
    'uncited_component_references':sorted(source_keys-cited),
    'uncited_bibliography_entries':sorted(set(entries)-cited),
    'missing_crossreferences':sorted(set(refs)-set(labels)),
    'duplicate_labels':[k for k,v in collections.Counter(labels).items() if v>1],
    'hygiene_flags':problems,
    'citation_locations':{k:[{'path':p,'line':n} for ck,p,n in citations if ck==k] for k in sorted(source_keys)},
    'doi_by_key':{k:field(v,'doi') for k,v in entries.items()},
    'total_source_characters':sum(len(t) for t in texts.values()),
}
(WORK/'manuscript_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k not in ('citation_locations','doi_by_key')},indent=2))
