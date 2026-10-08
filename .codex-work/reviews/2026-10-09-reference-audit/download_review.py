import concurrent.futures
from pathlib import Path
import urllib.request

out=Path(__file__).resolve().parent/'external'
urls={
 'Zhang2026-publisher':'https://www.nature.com/articles/s41545-025-00537-4',
 'Ulrich2009-repository':'https://api.figshare.com/v2/articles/9585188',
 'Min2024-original':'https://arxiv.org/abs/2410.10807v1',
 'Meijer2004-repository':'https://repository.tudelft.nl/record/uuid:e0d5af2b-7bf6-4cd8-9a22-aac3f8d112fe',
 'StenstromSong1991-publications':'http://seas.ucla.edu/stenstro/referreed.html',
 'TakacsVanrolleghem2006-alternative':'https://modeleau.fsg.ulaval.ca/fileadmin/modeleau/documents/Publications/pvr673.pdf',
 'Ulrich2009-publisher':'https://wedc-knowledge.lboro.ac.uk/resources/books/DEWATS_full.pdf',
 'Alex2008-report':'http://www2.iea.lth.se/publications/Reports/LTH-IEA-7229.pdf',
 'Ulrich2009-preliminaries':'https://ndownloader.figshare.com/files/52120196',
}
def fetch(item):
    k,u=item
    try:
        d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()
        ext='pdf' if d.startswith(b'%PDF') else 'html'
        (out/(k+'.'+ext)).write_bytes(d)
        print(k,len(d),flush=True)
    except Exception as e: print(k,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(fetch,urls.items()))
