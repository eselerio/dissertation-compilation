import concurrent.futures
from collections import Counter
import difflib
import html
import json
from pathlib import Path
import re
import time
import unicodedata
import urllib.request
import urllib.parse

OUT = Path(__file__).resolve().parent
ARTICLE = Path('article').resolve()

def parse_bib(text):
    entries = []
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,]+),', text):
        depth = 1
        i = m.end()
        while depth and i < len(text):
            if text[i] == '{' and (i == 0 or text[i-1] != '\\'): depth += 1
            if text[i] == '}' and (i == 0 or text[i-1] != '\\'): depth -= 1
            i += 1
        block = text[m.end():i-1]
        fields = {}
        spans = {}
        for f in re.finditer(r'(\w+)\s*=\s*\{', block):
            a = f.end()
            b = a
            d = 1
            while d:
                if block[b] == '{' and block[b-1] != '\\': d += 1
                if block[b] == '}' and block[b-1] != '\\': d -= 1
                b += 1
            fields[f[1].lower()] = block[a:b-1]
            spans[f[1].lower()] = [m.end()+a, m.end()+b-1]
        entries.append({'key':m[2].strip(), 'type':m[1].lower(), 'fields':fields, 'span':[m.start(),i], 'field_spans':spans})
    return entries

def tex_plain(s):
    s = html.unescape(re.sub(r'<[^>]*>', '', s))
    s = s.replace(r'\&', '&').replace(r'\%', '%').replace('~', ' ')
    s = re.sub(r'\\[\"\'`^~=.]\s*\{?([A-Za-z])\}?', r'\1', s)
    s = re.sub(r'\\[A-Za-z]+\s*', '', s)
    return s.replace('{','').replace('}','')

def norm(s):
    s = unicodedata.normalize('NFKD',tex_plain(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', s)

def read_sources():
    seen = set()
    texts = {}
    def read(p):
        p = p.resolve()
        if p in seen: return
        seen.add(p)
        s = re.sub(r'(?<!\\)%[^\n]*', '', p.read_text(encoding='utf-8'))
        texts[str(p.relative_to(ARTICLE))] = s
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', s):
            cp = Path(child)
            if not cp.suffix: cp = cp.with_suffix('.tex')
            candidates = [ARTICLE/cp, p.parent/cp]
            actual = next((q for q in candidates if q.exists()), None)
            if actual is None: raise ValueError(f'Missing input: {child}')
            read(actual)
    read(ARTICLE/'manuscript.tex')
    return texts

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':'DissertationReferenceAudit/1.0', 'Accept':'application/json'})
    for n in range(3):
        try:
            with urllib.request.urlopen(req, timeout=35) as r: return json.load(r)['message']
        except Exception:
            if n == 2: raise
            time.sleep(1+n)

def verify(entry):
    key = entry['key']
    f = entry['fields']
    doi = f.get('doi','').strip()
    cache = OUT/'crossref'/f'{key}.json'
    result = {'key':key, 'doi':doi, 'issues':[]}
    try:
        if cache.exists(): m = json.loads(cache.read_text(encoding='utf-8'))
        elif doi and not doi.lower().startswith('10.48550/'):
            m = fetch('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''))
            cache.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
        else:
            query = tex_plain(f.get('title',''))+' '+tex_plain(f.get('author',f.get('editor','')).split(' and ')[0])+' '+f.get('year','')
            items = fetch('https://api.crossref.org/works?rows=5&query.bibliographic='+urllib.parse.quote(query))['items']
            (OUT/'crossref'/f'{key}.candidates.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
            ranked = sorted(items,key=lambda x:difflib.SequenceMatcher(None,norm(f.get('title','')),norm(' '.join(x.get('title',[])))).ratio(),reverse=True)
            m = ranked[0] if ranked else {}
            similarity = difflib.SequenceMatcher(None,norm(f.get('title','')),norm(' '.join(m.get('title',[])))).ratio()
            first = f.get('author',f.get('editor','')).split(' and ')[0].split(',')[0]
            names = m.get('author',m.get('editor',[]))
            author_ok = bool(names) and (norm(first) in norm(names[0].get('family','')) or norm(names[0].get('family','')) in norm(first))
            if similarity < .92 or not author_ok:
                result.update(status='not_verified_by_crossref',best_candidate=m.get('DOI'),candidate_similarity=round(similarity,3))
                return result
            cache.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
        title = ' '.join(m.get('title',[]))
        similarity = difflib.SequenceMatcher(None,norm(f.get('title','')),norm(title)).ratio()
        result.update(status='verified' if similarity >= .9 else 'doi_title_mismatch',title_similarity=round(similarity,3),crossref_doi=m.get('DOI'),crossref_title=title)
        if not doi and m.get('DOI'): result['issues'].append({'field':'doi','current':'','crossref':m['DOI']})
        for field, crfield in [('volume','volume'),('number','issue'),('pages','page')]:
            cv = str(m.get(crfield,''))
            if cv and norm(f.get(field,'')) != norm(cv): result['issues'].append({'field':field,'current':f.get(field,''),'crossref':cv})
        if m.get('article-number') and not m.get('page') and norm(f.get('pages','')) != norm(m['article-number']):
            result['issues'].append({'field':'pages','current':f.get('pages',''),'crossref':m['article-number']})
        years = {x:m[x]['date-parts'][0][0] for x in ['published-print','published-online','published','issued'] if m.get(x,{}).get('date-parts')}
        result['years'] = years
        preferred = years.get('published-print',years.get('published',years.get('issued',years.get('published-online'))))
        if preferred and str(preferred) != f.get('year'): result['issues'].append({'field':'year','current':f.get('year'),'crossref':str(preferred)})
        names = m.get('author',[])
        bibnames = f.get('author','').split(' and ') if f.get('author') else []
        if names and bibnames:
            families = [n.get('family','') for n in names]
            expected = [x.split(',')[0] if ',' in x else x.split()[-1] for x in bibnames]
            if len(names) != len(bibnames) or any(norm(a)!=norm(b) for a,b in zip(families,expected)):
                result['issues'].append({'field':'author','current':expected,'crossref':families})
        if title and norm(title) != norm(f.get('title','')): result['issues'].append({'field':'title','current':f.get('title'),'crossref':title})
        container = ' '.join(m.get('container-title',[]))
        field = 'journal' if entry['type']=='article' else 'booktitle' if entry['type'] in ['incollection','inproceedings'] else None
        if field and container and norm(f.get(field,'')) != norm(container): result['issues'].append({'field':field,'current':f.get(field,''),'crossref':container})
        if m.get('update-to'): result['updates'] = m['update-to']
        return result
    except Exception as ex:
        result.update(status='crossref_request_failed',error=str(ex))
        return result

def run():
    (OUT/'crossref').mkdir(exist_ok=True)
    text = (ARTICLE/'references.bib').read_text(encoding='utf-8')
    entries = parse_bib(text)
    texts = read_sources()
    locations = {}
    for fn,s in texts.items():
        for m in re.finditer(r'\\(?:cite[A-Za-z]*|nocite)\*?(?:\[[^\]]*\])*\{([^}]+)\}',s):
            for key in m[1].split(','):
                locations.setdefault(key.strip(),[]).append({'file':fn,'line':s[:m.start()].count('\n')+1})
    keys = {e['key'] for e in entries}
    cited = [e for e in entries if e['key'] in locations]
    structural = {'included_sources':list(texts),'database_entries':len(entries),'cited_entries':len(cited),
                  'missing_citation_keys':sorted(set(locations)-keys),'uncited_entries':sorted(keys-set(locations)),
                  'duplicate_keys':[k for k,v in Counter(e['key'] for e in entries).items() if v>1],
                  'duplicate_dois':{k:v for k,v in ((d,[e['key'] for e in entries if e['fields'].get('doi','').lower()==d]) for d in {e['fields'].get('doi','').lower() for e in entries}- {''}) if len(v)>1},
                  'citation_locations':locations}
    print(json.dumps({k:v for k,v in structural.items() if k not in ['citation_locations','included_sources']},indent=2),flush=True)
    report = {'structure':structural,'references':[]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(verify,e):e for e in cited}
        for i,future in enumerate(concurrent.futures.as_completed(futures),1):
            result = future.result()
            report['references'].append(result)
            if result['status']!='verified' or result['issues']: print(json.dumps(result,ensure_ascii=True),flush=True)
            if i%20==0: print(f'Checked {i}/{len(cited)}',flush=True)
            (OUT/'audit-initial.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Complete',dict(Counter(r['status'] for r in report['references'])),flush=True)

if __name__=='__main__': run()
