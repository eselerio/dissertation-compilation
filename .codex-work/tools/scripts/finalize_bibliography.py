import json
import re
from build_bibliography import ROOT, WORK, bib_entries, field

records=json.loads((WORK/'references/records/bibliography-records.json').read_text(encoding='utf8'))
entries=bib_entries((WORK/'references/imports/references-import.bib').read_text(encoding='utf8'))
manual=WORK/'references/imports/manual-references.bib'
if not manual.exists(): raise SystemExit('Manual bibliographic entries are still being completed.')
entries.update(bib_entries(manual.read_text(encoding='utf8')))
source_keys={k for k,v in records.items() if v['sources']!=['existing']}
missing=source_keys-set(entries)
if missing: raise SystemExit('Missing source entries '+str(sorted(missing)))
aliases=json.loads((WORK/'references/records/citation-aliases.json').read_text(encoding='utf8'))
aliases.update({'YuanLin2006':'Yuan2006','ZouHastie2005':'Zou2005','Smola2004':'SmolaScholkopf2004','SturmCappaWexler2023':'Sturm2023','Viering2023':'VieringLoog2023'})
for path in (ROOT/'article/chapters').glob('*.tex'):
    text=path.read_text(encoding='utf8')
    def fix_citation(match):
        new=','.join(aliases.get(k.strip(),k.strip()) for k in match[2].split(','))
        return match[1]+'{'+new+'}'
    text=re.sub(r'(\\cite(?:t|p|alt|alp|author|year)?\*?(?:\[[^\]]*\]){0,2})\{([^}]+)\}',fix_citation,text)
    path.write_text(text,encoding='utf8')
for k in source_keys:
    entry=entries[k]
    for old,new in [('activated-sludge','activated sludge'),('wastewater-treatment','wastewater treatment'),('machine-learning','machine learning')]: entry=entry.replace(old,new)
    entries[k]=entry
(ROOT/'article/references.bib').write_text('\n\n'.join(entries[k] for k in sorted(source_keys))+'\n',encoding='utf8')
meta={k:{'author':field(entries[k],'author'),'year':field(entries[k],'year'),'title':field(entries[k],'title'),'doi':field(entries[k],'doi'),'sources':records[k]['sources']} for k in sorted(source_keys)}
(WORK/'references/records/final-reference-metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
print('Consolidated bibliography with '+str(len(source_keys))+' distinct component references.')
