import concurrent.futures
import html
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / '.codex-work'
COMP = ROOT / 'compile' if (ROOT / 'compile').exists() else ROOT / 'article/compile'

def bib_entries(text):
    out = {}
    for match in re.finditer(r'@(\w+)\s*\{([^,]+),', text):
        start = match.start()
        level = 1
        end = match.end()
        while level:
            if text[end] == '{' and text[end-1] != '\\': level += 1
            if text[end] == '}' and text[end-1] != '\\': level -= 1
            end += 1
        out[match[2].strip()] = text[start:end]
    return out

def field(entry, name):
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*\{', entry, re.I)
    if not m: return ''
    level, i, start = 1, m.end(), m.end()
    while level:
        if entry[i] == '{' and entry[i-1] != '\\': level += 1
        if entry[i] == '}' and entry[i-1] != '\\': level -= 1
        i += 1
    return entry[start:i-1]

def latex(s):
    s = html.unescape(re.sub(r'<[^>]+>', '', str(s)))
    s = s.replace('\u2013', '--').replace('\u2014', '---').replace('\u2019', "'").replace('\u2018', "'")
    s = s.replace('\u201c', '``').replace('\u201d', "''")
    for old,new in [('&',r'\&'), ('%',r'\%'), ('_',r'\_'), ('#',r'\#')]: s = s.replace(old,new)
    # Latin extended characters are rendered through standard LaTeX accents.
    result = ''
    accents = {'\u0301':"'", '\u0300':'`', '\u0308':'"', '\u0302':'^', '\u0303':'~', '\u0327':'c', '\u030c':'v', '\u030a':'r'}
    for ch in s:
        if ord(ch) < 128: result += ch; continue
        special = {'ø':r'{\o}', 'Ø':r'{\O}', 'ß':r'{\ss}', 'ł':r'{\l}', 'Ł':r'{\L}', 'æ':r'{\ae}', 'œ':r'{\oe}'}
        if ch in special: result += special[ch]; continue
        dec = unicodedata.normalize('NFD',ch)
        if len(dec)==2 and dec[1] in accents: result += '{\\' + accents[dec[1]] + '{' + dec[0] + '}}'
        else: result += ch
    return result

def fetch(doi):
    cache = WORK / 'references/crossref-cache' / (re.sub('[^A-Za-z0-9._-]', '_',doi)+'.json')
    if cache.exists(): return json.loads(cache.read_text(encoding='utf8'))
    for trial in range(3):
        try:
            req = urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''), headers={'User-Agent':'DissertationReferenceAudit/1.0'})
            with urllib.request.urlopen(req, timeout=35) as response: data=json.load(response)['message']
            cache.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
            return data
        except Exception as err:
            if trial == 2: return {'error':str(err),'DOI':doi}
            time.sleep(trial+1)

def to_bib(key, metadata):
    typ = metadata.get('type','journal-article')
    btype = {'book':'book','edited-book':'book','monograph':'book','book-chapter':'incollection','proceedings-article':'inproceedings','dissertation':'phdthesis','posted-content':'misc'}.get(typ,'article')
    if key == 'Henze2006': btype='book'
    data = {}
    people = metadata.get('author',metadata.get('editor',[]))
    names = []
    for person in people:
        if 'family' in person:
            name=latex(person['family']) + ', ' + latex(person['given']) if person.get('given') else '{'+latex(person['family'])+'}'
            if person.get('suffix'): name=latex(person['family'])+', '+latex(person['suffix'])+', '+latex(person.get('given',''))
        else: name='{'+latex(person.get('name','Unknown'))+'}'
        names.append(name)
    data['author'] = ' and '.join(names)
    if key == 'JeppssonDiehl1996': data['author'] = 'Jeppsson, Ulf and Diehl, Stefan'
    date = metadata.get('published-print',metadata.get('published',metadata.get('issued',{}))).get('date-parts',[[None]])[0]
    data['year'] = str(date[0])
    if key == 'Zhang2026': data['year'] = '2026'
    title=metadata.get('title',[''])[0]
    if metadata.get('subtitle') and metadata['subtitle'][0]: title += ': ' + metadata['subtitle'][0]
    title = latex(title)
    for banned, replacement in [('activated-sludge','activated sludge'),('wastewater-treatment','wastewater treatment'),('machine-learning','machine learning')]:
        title=title.replace(banned,replacement)
    title=re.sub(r'\b(?:[A-Z][A-Z0-9-]{1,}|ASM2d|TabNet|XGBoost|LightGBM|CatBoost|Optuna|Julia)\b',lambda m:'{'+m[0]+'}',title)
    data['title']=title
    container=metadata.get('container-title',[''])
    if container and container[0]: data['booktitle' if btype in ('inproceedings','incollection') else 'journal']=latex(container[0])
    if btype in ('book','inproceedings','incollection'): data['publisher']=latex(metadata.get('publisher',''))
    for origin,target in [('volume','volume'),('issue','number'),('page','pages'),('article-number','pages')]:
        if metadata.get(origin): data[target]=latex(metadata[origin]).replace('-','--') if origin=='page' else latex(metadata[origin])
    data['doi']=metadata.get('DOI','')
    if key == 'Henze2006':
        data['author']='Henze, M. and Gujer, W. and Mino, T. and van Loosdrecht, M. C. M.'
        for f in ('journal','volume','number','pages'): data.pop(f,None)
    if key == 'JeppssonDiehl1996':
        data['pages']='85--92'
        data['number']='5--6'
    return '@'+btype+'{'+key+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in data.items() if v)+'\n}'

def main():
    (WORK/'references/crossref-cache').mkdir(exist_ok=True)
    original=bib_entries((WORK/'snapshots/original-manuscript/references.bib').read_text(encoding='utf8'))
    doikey={field(v,'doi').lower().replace(r'\_','_'):k for k,v in original.items() if field(v,'doi')}
    records={k:{'key':k,'doi':field(v,'doi').replace(r'\_','_'),'raw':v,'sources':['existing']} for k,v in original.items()}
    opt=(COMP/'optimization/manuscript.tex').read_text(encoding='utf8')
    optrefs=re.findall(r'\\bibitem\[.*?\]\{(.*?)\}\s*(.*?)(?=\\bibitem|\\end\{thebibliography\})',opt,re.S)
    aliases={}
    for key,raw in optrefs:
        m=re.search(r'https://doi.org/([^}]+)',raw)
        doi=m[1] if m else ''
        # Alternate registered identifier for the same McKay paper.
        if key=='McKay1979': doi=field(original['McKay1979'],'doi')
        canonical=doikey.get(doi.lower(),key)
        aliases[key]=canonical
        if canonical not in records: records[canonical]={'key':canonical,'doi':doi,'raw':raw,'sources':[]}
        records[canonical]['sources'].append('optimization')
        if doi: doikey[doi.lower()]=canonical
    projection=(COMP/'projection/manuscript.tex').read_text(encoding='utf8').split(r'\section*{References}')[1]
    for raw in re.findall(r'\\noindent\s+(.*?)(?=\n\s*\n|\\end\{document\})',projection,re.S):
        m=re.search(r'doi:\s*(.+?)\.\s*$',raw.strip())
        doi=m[1].replace(r'\_','_') if m else ''
        first=re.split(r'[, ]',raw)[0].replace('$','')
        year=re.search(r'\((\d{4})\)',raw)[1]
        proposals={'Arik':'ArikPfister2021','Kircher':'KircherVotsmeier2025','Smola':'SmolaScholkopf2004','Mack':'Mack1981','Min':'Min2024','Utkarsh':'Utkarsh2025'}
        key=doikey.get(doi.lower(),proposals.get(first,first+year))
        if key not in records: records[key]={'key':key,'doi':doi,'raw':raw,'sources':[]}
        records[key]['sources'].append('projection')
        if doi: doikey[doi.lower()]=key
    icsor_path=WORK/'references/records/icsor-references.json'
    if icsor_path.exists():
        for rec in json.loads(icsor_path.read_text(encoding='utf8')):
            doi=rec.get('doi','') or ''
            key=doikey.get(doi.lower(),rec['key'])
            aliases[rec['key']]=key
            if key not in records: records[key]={**rec,'key':key,'sources':[]}
            records[key]['sources'].append('icsor')
            if doi: doikey[doi.lower()]=key
    all_dois=sorted(set(r['doi'].lower() for r in records.values() if r.get('doi') and not r['doi'].startswith('10.48550/')))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        metadata=dict(zip(all_dois,pool.map(fetch,all_dois)))
    (WORK/'references/records/bibliography-records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
    (WORK/'references/records/citation-aliases.json').write_text(json.dumps(aliases,indent=2),encoding='utf8')
    entries={}
    for key,rec in records.items():
        md=metadata.get(rec.get('doi','').lower())
        if md and 'error' not in md:
            entries[key]=to_bib(key,md)
        elif key in original:
            entries[key]=original[key]
        else:
            entries[key]='% MANUAL METADATA REQUIRED '+key+'\n% '+rec.get('raw','').replace('\n',' ')
    (WORK/'references/imports/references-import.bib').write_text('\n\n'.join(entries[k] for k in sorted(entries))+'\n',encoding='utf8')
    print(json.dumps({'records':len(records),'doi_records':len(all_dois),'manual':[k for k,e in entries.items() if e.startswith('%')],'errors':{d:m['error'] for d,m in metadata.items() if 'error' in m}},indent=2))

if __name__=='__main__': main()
