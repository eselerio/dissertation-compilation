from collections import Counter
import json
from pathlib import Path
import re
import shutil
import audit

path = audit.ARTICLE/'references.bib'
original = path.read_text(encoding='utf-8')
entries = audit.parse_bib(original)
report = json.loads((audit.OUT/'audit-initial.json').read_text(encoding='utf-8'))
uncited = set(report['structure']['uncited_entries'])
changes = {
 'Dold1981': {'booktitle':'Water Pollution Research and Development'},
 'Madhav2019': {'booktitle':'Sensors in Water Pollutants Monitoring: Role of Material', 'series':'Advanced Functional Materials and Sensors', 'editor':'Pooja, D. and Kumar, Praveen and Singh, Pardeep and Patil, Sandip'},
 'Petersen2003': {'booktitle':'Biotechnology for the Environment: Wastewater Treatment and Modeling, Waste Gas Handling', 'series':'Focus on Biotechnology', 'volume':'3C', 'editor':'Agathos, Spiros N. and Reineke, Walter'},
 'Tabios2020': {'booktitle':'Water Resources Systems of the Philippines: Modeling Studies', 'series':'World Water Resources', 'volume':'4'},
 'Ulrich2009': {'title':'Decentralised wastewater treatment systems ({DEWATS}) and sanitation in developing countries: A practical guide'},
 'Meijer2004': {'url':'https://repository.tudelft.nl/record/uuid:e0d5af2b-7bf6-4cd8-9a22-aac3f8d112fe'},
 'Drucker1997': {'url':'https://mlanthology.org/icml/1997/drucker1997icml-improving/'},
 'Min2024': {'url':'https://arxiv.org/abs/2410.10807v1'},
}
shutil.copy2(path,audit.OUT/'references.before.bib')
removed=[]
kept=[]
change_log=[]
for entry in entries:
    a,b=entry['span']
    block=original[a:b]
    if entry['key'] in uncited:
        removed.append(block)
        continue
    edits=[]
    for field,value in changes.get(entry['key'],{}).items():
        old=entry['fields'].get(field)
        if old==value: continue
        if old is not None:
            s,e=entry['field_spans'][field]
            edits.append((s-a,e-a,value))
        else:
            end=block.rfind('}')
            trimmed=block[:end].rstrip()
            prefix='' if trimmed.endswith(',') else ','
            edits.append((end,end,prefix+'\n  '+field+' = {'+value+'}\n'))
        change_log.append({'key':entry['key'],'field':field,'before':old,'after':value})
    # Missing fields share the same insertion offset and are joined before applying.
    merged={}
    for s,e,value in edits:
        if s==e and (s,e) in merged:
            merged[(s,e)]=merged[(s,e)].rstrip()+','+value.lstrip(',')
        else: merged[(s,e)]=value
    for (s,e),value in sorted(merged.items(),reverse=True): block=block[:s]+value+block[e:]
    kept.append(block)
path.write_text('\n\n'.join(kept)+'\n',encoding='utf-8')
(audit.OUT/'removed-uncited.bib').write_text('\n\n'.join(removed)+'\n',encoding='utf-8')
(audit.OUT/'changes.json').write_text(json.dumps(change_log,ensure_ascii=False,indent=2),encoding='utf-8')

external_notes={
 'Alex2008':('https://www2.iea.lth.se/publications/Reports/LTH-IEA-7229.pdf','Lund University report indexed as TEIE-7229 (2008). Direct download encountered a certificate-chain error; indexed primary-source record confirms identity.'),
 'Bergstra2011':('https://proceedings.neurips.cc/paper/2011/hash/86e8f7ab32cfd12577bc2619bc635690-Abstract.html','NeurIPS proceedings metadata confirms authors, title, volume and year; no reliable Crossref DOI found.'),
 'Cawley2011':('https://proceedings.mlr.press/v16/cawley11a.html','PMLR metadata confirms author, title, publication year and pages; no reliable Crossref DOI found.'),
 'Demsar2006':('https://www.jmlr.org/papers/v7/demsar06a.html','JMLR metadata confirms author, title, year, volume and pages; no reliable Crossref DOI found.'),
 'Drucker1997':('https://mlanthology.org/icml/1997/drucker1997icml-improving/','ICML anthology and indexed original paper confirm author, title, year and pages. Unreachable CiteSeer URL replaced with the conference anthology record; no reliable DOI found.'),
 'DamalerioBarriers2022':('https://www.cetjournal.it/index.php/cet/article/view/CET2297062','Publisher metadata confirms all authors, year, volume, pages and DOI. Crossref DOI lookup returned HTTP 404; retain publisher-confirmed DOI.'),
 'Guyon2011':('https://proceedings.mlr.press/v16/guyon11a.html','PMLR metadata confirms all authors, title, year and pages; no reliable Crossref DOI found.'),
 'Hoover1952':('https://www.jstor.org/stable/25031842','JSTOR indexed primary-source title and bibliographic details identify the historical article; direct content retrieval encountered a client challenge. No reliable DOI found.'),
 'Ke2017':('https://proceedings.neurips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html','NeurIPS proceedings metadata confirms authors, title, year and volume; no reliable Crossref DOI found.'),
 'Kraft1988':('https://degenerateconic.com/uploads/2018/03/DFVLR_FB_88_28.pdf','Original scanned technical report retrieved. No reliable Crossref DOI found.'),
 'Marais1976':('https://www.wrc.org.za/water-sa-issue/02-no-4-october-1976/','Publisher issue archive and Water SA bibliographic index identify the article; publisher-hosted references confirm volume 2(4), 163–200 (1976). Issue-page retrieval timed out. No reliable DOI found.'),
 'Meijer2004':('https://repository.tudelft.nl/record/uuid:e0d5af2b-7bf6-4cd8-9a22-aac3f8d112fe','TU Delft repository and research portal confirm author, dissertation title and 2004 date. Updated resolver URL to current repository record; no reliable DOI found.'),
 'Min2024':('https://arxiv.org/abs/2410.10807v1','Original 2024 arXiv source confirms the three cited authors and title. Later arXiv revisions change the title and author list, so the URL now points to the cited original. DOI is an arXiv/DataCite identifier, not Crossref.'),
 'Prokhorenkova2018':('https://proceedings.neurips.cc/paper/2018/hash/14491b756b3a51daac41c24863285549-Abstract.html','NeurIPS proceedings metadata confirms authors, title, year and volume; no reliable Crossref DOI found.'),
 'Ragonneau2022':('https://arxiv.org/abs/2210.12018','arXiv confirms author, title, first-submission year and doctoral-thesis status. The title-similar Crossref search candidate concerns different software work and was rejected. DOI is arXiv/DataCite.'),
 'Simon2013':('https://arxiv.org/abs/1311.6529','arXiv confirms title, three authors and 2013 date; DOI is arXiv/DataCite.'),
 'StenstromSong1991':('http://seas.ucla.edu/stenstro/referreed.html','Author-hosted UCLA publication list confirms authors, journal, volume 63(3), pages 208–219 and 1991 date. The list shortens/paraphrases the title; indexed original paper uses the existing oxygen-transport title. No reliable DOI found.'),
 'TakacsVanrolleghem2006':('https://modeleau.fsg.ulaval.ca/fileadmin/modeleau/documents/Publications/pvr673.pdf','Indexed original author-hosted paper confirms title, two authors and IWA copyright 2006. URL currently returns HTTP 404; retained pending a verified replacement. No reliable DOI found.'),
 'USEPA2009':('https://www.epa.gov/sites/default/files/2019-02/documents/nutrient-control-design-manual-state-tech.pdf','Original EPA PDF confirms report title, EPA/600/R-09/012 and January 2009. No reliable DOI found.'),
 'Ulrich2009':('https://repository.lboro.ac.uk/articles/book/9585188','Repository API and original book preliminaries confirm editors, publication year, publisher and ISBN. The book explicitly recommends the editors as the citation heading. Added omitted DEWATS wording to the title; no assigned DOI found.'),
 'Vandekerckhove2018':('https://biblio.ugent.be/publication/8584187','Ghent University repository confirms author, dissertation title, year and awarding institution; no reliable DOI found.'),
 'Utkarsh2025':('https://arxiv.org/abs/2506.07003','arXiv confirms title, authors and 2025 date. DOI is arXiv/DataCite.'),
 'Xie2021':('https://repository.uantwerpen.be/link/irua/182099','Indexed Antwerp repository record and university-hosted dissertation confirm author, title and 2021 date. Live repository endpoint returned an empty application shell. No reliable DOI found.'),
}
special={
 'Henze2006':'Retain original 2000 book date, editors, report number 9 and ISBN. Crossref describes the later electronic manifestation (2015), with malformed volume/issue/page fields that must not overwrite the original edition. TU Delft chapter records and publisher material confirm the 2000 edition.',
 'Zhang2026':'Retain 2026. The publisher recommends npj Clean Water 9, 4 (2026), with the final article dated 7 January 2026; Crossref still uses the early-online date of 6 December 2025. https://www.nature.com/articles/s41545-025-00537-4',
 'Takacs1991':'Retain all three authors. Crossref incorrectly lists only TAKACS; original article and component-source bibliography identify Takacs, Patry and Nolasco.',
}
for key in ['Akiba2019','ChenGuestrin2016','Kaufman2012']:
    special[key]='Full title verified by combining Crossref title and subtitle. The initial title-only mismatch was a metadata-parsing false positive; retain existing title.'
final_refs=[]
for r in sorted(report['references'],key=lambda r:r['key']):
    item=dict(r)
    key=r['key']
    if key in external_notes:
        url,note=external_notes[key]
        item.update(review_status='verified_by_primary_or_authoritative_record',evidence_url=url,review_note=note)
    else:
        item.update(review_status='verified_by_crossref',evidence_url='https://api.crossref.org/works/'+r['doi'])
    if key in special: item['review_note']=special[key]
    if key in changes: item['corrections']=changes[key]
    final_refs.append(item)
updated=audit.parse_bib(path.read_text(encoding='utf-8'))
current_keys={e['key'] for e in updated}
assert current_keys==set(report['structure']['citation_locations'])
assert len(updated)==146
final={'scope':'article/manuscript.tex and every recursively included LaTeX source',
       'skill':'audit-latex-references; adapted to BibTeX because bundled script supports manual references only',
       'summary':{'cited_references':146,'crossref_verified':123,'verified_through_other_records':23,
                  'missing_citations':[], 'uncited_database_entries_removed':len(uncited),
                  'references_corrected':len(changes),'doi_additions':0,'doi_updates':0,
                  'cited_references_removed_for_crossref_absence':0,'unverified_reference_identities':[],
                  'references_without_doi':[e['key'] for e in updated if not e['fields'].get('doi')],
                  'access_limitations':['Alex2008','Hoover1952','Marais1976','TakacsVanrolleghem2006','Xie2021'],
                  'broken_reference_url_retained':['TakacsVanrolleghem2006']},
       'removed_uncited_keys':sorted(uncited),'changes':change_log,'references':final_refs,
       'citation_locations':report['structure']['citation_locations']}
(audit.OUT/'audit-final.json').write_text(json.dumps(final,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(audit.OUT/'audit-final.json',audit.ARTICLE/'manuscript.reference-audit.json')
print(json.dumps(final['summary'],indent=2))
