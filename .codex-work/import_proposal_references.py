import concurrent.futures
import json
import re
from pathlib import Path
from build_bibliography import ROOT, WORK, bib_entries, field, fetch, to_bib

t=(WORK/'approved-proposal-layout.txt').read_text(encoding='utf8')
t=t[t.index('\n9   References'): ] if '\n9   References' in t else t[t.index('\n9    References'):]
t=t.split('\n10   Budgetary')[0] if '\n10   Budgetary' in t else t
t=re.sub(r'\f','\n',t)
t=re.sub(r'(?m)^P\s*a\s*g\s*e\s*\|\s*\d+\s*$','',t)
t=re.sub(r'(?m)^Page\s*\|\s*\d+\s*$','',t)
starts=[m.start() for m in re.finditer(r'(?m)^[^\s\d][^\n]{0,180}(?:,|NEDA).*\n',t)
        if re.match(r'(?m)^[^\s]',t[m.start():]) and re.search(r'\((?:19|20)\d\d[a-z]?\)',t[m.start():m.start()+750])]
records=[]
for i,start in enumerate(starts):
    block=t[start:starts[i+1] if i+1<len(starts) else len(t)].strip()
    # Nonreference headings can only occur after the last bibliography entry.
    block=re.split(r'\n(?:10|11)\s+',block)[0]
    raw=' '.join(block.split())
    year=re.search(r'\((19|20)\d{2}[a-z]?\)',raw)
    if not year: continue
    y=year[0][1:5]
    prefix=raw[:year.start()].strip()
    first=prefix.split(',')[0]
    slug=re.sub('[^A-Za-z0-9]','',first)
    doi=''
    m=re.search(r'https?://doi\.org/(.*?)(?=\s*https?://|$)',raw,re.I)
    if m:
        doi=re.sub(r'\s+','',m[1]).rstrip('.')
        doi=re.sub(r'/(METRICS|BIBTEX|S1|TABLES/1)$','',doi,flags=re.I)
    titlepart=raw[year.end():].strip().lstrip('.').strip()
    records.append({'proposal_id':i+1,'proposed_key':slug+y,'year_as_cited':y,
                    'authors_as_cited':prefix,'doi':doi.lower(),'raw':raw,
                    'title_fragment':titlepart[:220]})
existing=bib_entries((ROOT/'article/references.bib').read_text(encoding='utf8'))
bydoi={field(v,'doi').lower():k for k,v in existing.items() if field(v,'doi')}
seen={}
for r in records:
    d=r['doi']
    if d and d in bydoi:
        r['canonical_key']=bydoi[d];r['already_in_manuscript']=True
    elif d and d in seen:
        r['canonical_key']=seen[d];r['duplicate']=True;r['already_in_manuscript']=False
    else:
        key=r['proposed_key']
        # Resolve distinct same-author-year works before generating citations.
        if key in seen.values():key+='Context'
        r['canonical_key']=key;r['already_in_manuscript']=False
        if d:seen[d]=key
dois=sorted(set(r['doi'] for r in records if r['doi'] and not r['already_in_manuscript']))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    metadata=dict(zip(dois,pool.map(fetch,dois)))
new={}
for r in records:
    md=metadata.get(r['doi'])
    if md and 'error' not in md:
        r['verified_title']=md.get('title',[''])[0]
        r['verified_type']=md.get('type')
        r['verified_year']=md.get('published-print',md.get('published',md.get('issued',{}))).get('date-parts',[[None]])[0][0]
        new[r['canonical_key']]=to_bib(r['canonical_key'],md)
    elif md:r['verification_error']=md['error']
(WORK/'proposal_reference_inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
(WORK/'proposal_reference_import.bib').write_text('\n\n'.join(new[k] for k in sorted(new))+'\n',encoding='utf8')
print(json.dumps({'proposal_entries':len(records),'shared_existing':sum(r['already_in_manuscript'] for r in records),
                  'new_crossref_entries':len(new),'missing_doi':[r['canonical_key'] for r in records if not r['doi']],
                  'verification_errors':{d:m['error'] for d,m in metadata.items() if 'error' in m}},indent=2))
