import json
import re
from pathlib import Path

root=Path(__file__).resolve().parents[1]
paths=[root/'article/manuscript.tex',*sorted((root/'article/chapters').glob('*.tex')),
       *sorted((root/'article/figures').glob('*.tex'))]
phrases={
    'mass mass conservation':'mass conservation',
    'Consistent with mass conservation changes':'Changes consistent with mass conservation',
    'consistent with mass conservation changes':'changes consistent with mass conservation',
    'consistent with mass conservation states':'states consistent with mass conservation',
    'non-negative conserved segment':'segment satisfying mass conservation and non-negativity',
    'Restore the invariants':'Project for mass conservation',
    'repairs its negative coordinate':'sets its negative coordinate to zero',
    'Strict positivity of the provisional target':'Strict positivity of the provisional target',
    'Kircher--Votsmeier conservative projection':'Kircher--Votsmeier projection for mass conservation and non-negativity',
    'Affine restoration of the invariants':'Affine projection for mass conservation',
    'affine restoration of the invariants':'affine projection for mass conservation',
    'conserved component balance':'component balance for mass conservation',
    'conserved component combinations':'component combinations defining mass conservation',
    'independent conserved combination':'independent component combination defining mass conservation',
    'conserved-flux learning':'flux learning for mass conservation',
    'conserving approach':'approach for mass conservation',
    'conserving layer':'layer for mass conservation',
    'conservative subspace':'subspace defined by mass conservation',
    'conservative effluent estimate':'effluent estimate consistent with mass conservation',
    'non-negative conserved states':'states satisfying mass conservation and non-negativity',
    'non-negative and conservative':'non-negative and consistent with mass conservation',
    'conservative non-negative state':'state satisfying mass conservation and non-negativity',
    'not conservative':'inconsistent with mass conservation',
    'or conservative':'or consistent with mass conservation',
    'prediction conservative':'prediction consistent with mass conservation',
    'is conservative':'satisfies mass conservation',
    'sum is conserved':'sum is fixed by mass conservation',
    'physical reconciliation':'projection for mass conservation',
    'Output positivity':'Output non-negativity',
    'mass conservation and positivity':'mass conservation and non-negativity',
    'mass conservation with positivity':'mass conservation with non-negativity',
    'intermediate positivity':'strict positivity of the provisional target',
    'restore non-negativity':'enforce non-negativity',
    'restores non-negativity':'enforces non-negativity',
    'restore feasibility':'satisfy the specified constraints',
    'repair a large physical inconsistency':'reduce violations of the specified physical constraints',
    'equality alignment':'affine projection for mass conservation',
    'the aligned state':'the projected state',
    'the consistent with mass conservation affine set':'the affine set defined by mass conservation',
    'an consistent with mass conservation affine set':'an affine set defined by mass conservation',
    'mass conservation dimensionality reduction':'dimensionality reduction with mass conservation',
    'conservation-restoring corrections':'projections for mass conservation',
    'conservation-restoring correction':'projection for mass conservation',
    'conservation correction':'projection for mass conservation',
    'conservation corrections':'projections for mass conservation',
    'conservation-restoring nudge':'projection for mass conservation',
    'conservative but negative state':'state that satisfies mass conservation but violates non-negativity',
    'conservative affine reference':'affine reference satisfying mass conservation',
    'conservative affine state':'affine state satisfying mass conservation',
    'conservative raw state':'raw state satisfying mass conservation',
    'conservative candidate':'candidate satisfying mass conservation',
    'conservative candidates':'candidates satisfying mass conservation',
    'conservative prediction':'prediction satisfying mass conservation',
    'conservative predictions':'predictions satisfying mass conservation',
    'conservative state':'state satisfying mass conservation',
    'conservative states':'states satisfying mass conservation',
    'conservative change':'change satisfying mass conservation',
    'conservative changes':'changes satisfying mass conservation',
    'conservative correction':'projection for mass conservation',
    'conservative direction':'direction satisfying mass conservation',
    'conservative segment':'segment satisfying mass conservation',
    'conservative flux':'flux satisfying mass conservation',
    'conservative framework':'framework for mass conservation',
    'conserved inventories':'inventories used for mass conservation',
    'conserved inventory':'inventory used for mass conservation',
    'conserved combinations':'component combinations used for mass conservation',
    'conserved quantities':'quantities used for mass conservation',
    'conserved quantity':'quantity used for mass conservation',
    'conserved vectors':'vectors defining mass conservation',
    'conserved fluxes':'fluxes satisfying mass conservation',
    'conserved material':'material tracked by mass conservation',
    'conserved sum':'sum fixed by mass conservation',
    'conserved total':'total fixed by mass conservation',
    'conserved line':'line defined by mass conservation',
    'invariant-consistent':'consistent with mass conservation',
    'invariant-consistency':'mass conservation',
    'invariant consistency':'mass conservation',
    'invariant-aligned':'projected for mass conservation',
    'equality-aligned comparator predictions':'comparator predictions after affine projection',
    'equality-aligned comparator accuracy':'comparator accuracy after affine projection',
    'equality-aligned':'affine-projected',
    'equality-only affine alignment':'affine projection for mass conservation',
    'affine alignment':'affine projection',
    'comparator alignment':'comparator projection',
    'positivity control':'non-negativity enforcement',
    'positivity enforcement':'non-negativity enforcement',
    'positivity shortening':'projection interpolation for non-negativity',
    'positivity backtracking':'projection interpolation for non-negativity',
    'positivity is preserved':'non-negativity is enforced',
    'mass- and energy-conserving':'mass conservation and energy-balance',
    'mass-conserving':'mass conservation',
    'atom conservation':'mass conservation through atom balances',
    'conservation alone':'mass conservation alone',
    'physical correction':'projection',
    'physical corrections':'projections',
    'post correction':'post projection',
    'corrective constraints':'projection constraints',
    'corrective correction':'projection',
    'corrective layer':'projection layer',
    'conservation bookkeeping':'mass conservation',
    'material bookkeeping':'mass conservation',
    'bookkeeping':'mass conservation',
}

def change(t):
    protected=[]
    def store(m):
        protected.append(m[0]);return f'ZZPROTECTEDTOKEN{len(protected)-1}ZZ'
    t=re.sub(r'\\(?:label|ref|eqref|cref|Cref|cite\w*|input|includegraphics)\*?(?:\[[^\]]*\])*?\{[^}]+\}',store,t)
    for old,new in sorted(phrases.items(),key=lambda x:-len(x[0])):
        t=re.sub(r'\b'+re.escape(old)+r'\b',lambda m:new[0].upper()+new[1:] if m[0][0].isupper() else new,t,flags=re.I)
    # Preserve strict positivity of logarithmic inputs and reciprocal weights.
    t=re.sub(r'\bnonnegativity\b',lambda m:'Non-negativity' if m[0][0].isupper() else 'non-negativity',t,flags=re.I)
    t=re.sub(r'\bnonnegative\b',lambda m:'Non-negative' if m[0][0].isupper() else 'non-negative',t,flags=re.I)
    t=re.sub(r'\bcorrections\b','projections',t)
    t=re.sub(r'\bcorrection\b',lambda m:'Projection' if m[0][0].isupper() else 'projection',t,flags=re.I)
    t=re.sub(r'\bcorrected\b','projected',t,flags=re.I)
    t=re.sub(r'(?<!mass )\bconservation\b',lambda m:'Mass conservation' if m[0][0].isupper() else 'mass conservation',t,flags=re.I)
    t=t.replace('mass mass conservation','mass conservation')
    t=t.replace('mass-conservation','mass conservation')
    t=re.sub(r'\bmass mass conservation\b','mass conservation',t,flags=re.I)
    t=re.sub(r'(?m)^non-negativity','Non-negativity',t)
    t=re.sub(r'([.!?]\s+)non-negativity',r'\1Non-negativity',t)
    for i,s in enumerate(protected):t=t.replace(f'ZZPROTECTEDTOKEN{i}ZZ',s)
    return t

records=[]
for p in paths:
    t=p.read_text(encoding='utf8')
    new=change(t)
    if new!=t:p.write_text(new,encoding='utf8')
    records.append({'path':str(p.relative_to(root)),'changed':new!=t})
(root/'.codex-work/terminology_pass.json').write_text(json.dumps(records,indent=2),encoding='utf8')
print('Standardized terms in',sum(r['changed'] for r in records),'visible LaTeX sources.')
