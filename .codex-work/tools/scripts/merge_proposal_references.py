import json
import re
from pathlib import Path
from build_bibliography import ROOT, WORK, bib_entries, field

base=bib_entries((WORK/'snapshots/before-proposal-integration/references.bib').read_text(encoding='utf8'))
pool=bib_entries((WORK/'references/imports/proposal-reference-import.bib').read_text(encoding='utf8'))
manual=bib_entries((WORK/'references/imports/proposal-manual-references.bib').read_text(encoding='utf8'))
records=json.loads((WORK/'references/records/proposal-reference-inventory.json').read_text(encoding='utf8'))
renames={
    'DezMontero2019':'DiezMontero2019','Galn1999':'Galan1999',
    'GuelliUlsonDeSouza2011':'GuelliSouza2011','Lain1999':'Laine1999',
    'Szelg2022':'Szelag2022','TabiosIII2020':'Tabios2020',
    'Takcs2006':'TakacsVanrolleghem2006','Jain2017':'JainKar2017',
    'Kusiak2012':'KusiakWei2013','Tawfik2009':'Tawfik2010',
    'Winkler2019':'WinklerStraka2019','Damalerio2022':'DamalerioRemoval2022',
    'Damalerio2022Context':'DamalerioBarriers2022',
}
excluded={
    'Bazemo2021':'Publisher identifier not independently resolved and sulfur odor modeling is outside the adopted component scope.',
    'Bisschop2018':'General software documentation is unnecessary to establish the current scientific contribution.',
    'NEDA2010':'The supplied attribution and title could not be confirmed from an authoritative original report. Philippine context uses verified scholarly sources.',
    'Li2022Context':'Atmospheric pollutant optimization does not strengthen the wastewater component or plant formulation.',
    'Zhang2016':'Caffeine-enriched wetland microbial communities are outside the modeled activated sludge process.'
}
merged=dict(base)
selected={}
for rec in records:
    old=rec['canonical_key']
    if rec['already_in_manuscript']:
        rec['integration_decision']='Retained from component-source bibliography';rec['final_key']=old
        continue
    if old in excluded:
        rec['integration_decision']='Not transferred';rec['decision_reason']=excluded[old]
        continue
    # Two Yang2014 entries identify distinct works; preserve the established fuzzy-control key.
    key='YangNetwork2014' if rec['doi']=='10.1021/ie500978h' else renames.get(old,old)
    if key in manual: entry=manual[key]
    elif old in pool: entry=pool[old].replace('{'+old+',','{'+key+',',1)
    else: raise RuntimeError('Missing verified source '+old)
    entry=entry.replace('\u2010','-').replace('\u2011','-').replace('\u2212','-')
    entry=entry.replace('İ',r'{\.{I}}').replace('ı',r'{\i}')
    entry=entry.replace('\u202f',' ').replace('\u2009',' ').replace('\u00a0',' ')
    for bad,good in [('activated-sludge','activated sludge'),('wastewater-treatment','wastewater treatment'),('machine-learning','machine learning')]:
        entry=entry.replace(bad,good)
    if key=='Dold1981':
        entry=re.sub(r'title = \{.*?\},',r'title = {A general model for the activated sludge process},',entry)
    if key in base and field(base[key],'doi').lower()!=rec['doi'].lower():
        raise RuntimeError('Citation collision '+key)
    merged[key]=entry
    rec['integration_decision']='Transferred as relevant background';rec['final_key']=key
    selected[key]=rec
(ROOT/'article/references.bib').write_text('\n\n'.join(merged[k] for k in sorted(merged))+'\n',encoding='utf8')
(WORK/'references/records/proposal-reference-decisions.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
(WORK/'references/records/proposal-selected-reference-keys.json').write_text(json.dumps(sorted(selected),indent=2),encoding='utf8')
print(json.dumps({'component_references_retained':len(base),'new_proposal_references':len(selected),
                  'bibliography_total':len(merged),'not_transferred':excluded},indent=2))
