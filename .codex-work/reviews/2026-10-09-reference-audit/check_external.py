import concurrent.futures
import json
from pathlib import Path
import re
import urllib.request
import audit

report=json.loads((audit.OUT/'audit-initial.json').read_text(encoding='utf-8'))
entries={e['key']:e for e in audit.parse_bib((audit.ARTICLE/'references.bib').read_text(encoding='utf-8'))}
(audit.OUT/'external').mkdir(exist_ok=True)
def run(r):
    key=r['key']; f=entries[key]['fields']; url=f.get('url','')
    if not url: return {'key':key,'status':'no_external_url'}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 DissertationReferenceAudit/1.0'})
        with urllib.request.urlopen(req,timeout=30) as response:
            data=response.read(); final=response.url; content=response.headers.get('Content-Type','')
        ext='pdf' if data.startswith(b'%PDF') else 'html'
        path=audit.OUT/'external'/f'{key}.{ext}'; path.write_bytes(data)
        text=data.decode('utf-8',errors='replace') if ext=='html' else ''
        meta=re.findall(r'<meta\b[^>]+>',text,re.I)
        metadata=[s for s in meta if any(x in s.lower() for x in ['citation_','dc.title','dc.date','og:title'])]
        title=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
        return {'key':key,'url':url,'final_url':final,'status':'retrieved','content_type':content,'title':title[1].strip() if title else '', 'metadata':metadata}
    except Exception as ex: return {'key':key,'url':url,'status':'request_failed','error':str(ex)}
items=[r for r in report['references'] if r['status'] not in ['verified','doi_title_mismatch']]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,items))
(audit.OUT/'external-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results: print(json.dumps(r,ensure_ascii=True))
