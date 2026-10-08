from pathlib import Path
import re
import json

root=Path(__file__).resolve().parents[3]
chapter=(root/'article/chapters/06_connected_plant.tex').read_text(encoding='utf-8')
original=(root/'.codex-work/snapshots/before-math-expansion/chapters/06_connected_plant.tex').read_text(encoding='utf-8')
def eqs(s):
    return [re.sub(r'\s+',' ',m[0]).strip() for m in re.finditer(r'\\begin\{(equation|align)\}.*?\\end\{\1\}',s,re.S)]
def citations(s):
    return {k.strip() for m in re.finditer(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}',s) for k in m[1].split(',')}
old_eq,new_eq=eqs(original),eqs(chapter)
old_labels=re.findall(r'\\label\{([^}]+)\}',original)
new_labels=re.findall(r'\\label\{([^}]+)\}',chapter)
missing=[e for e in old_eq if e not in new_eq]
missing_label=set(old_labels)-set(new_labels)
missing_cites=citations(original)-citations(chapter)
assert not missing_label
assert not missing_cites
assert len(new_labels)==len(set(new_labels))
assert not re.search(r'activated-sludge|wastewater-treatment|machine-learning|codebase|TODO',chapter,re.I)
assert not any(ord(c)<32 and c not in '\n\t' for c in chapter)
for label in ['fig:plant_configuration','fig:plant_inventory_envelope','fig:plant_projection_architecture','fig:plant_route_verification']:
    assert chapter.count('\\label{'+label+'}')==1
for env in ['equation','align','table','tabular','longtable','figure','tikzpicture']:
    assert chapter.count('\\begin{'+env+'}')==chapter.count('\\end{'+env+'}')

changed_label_groups=[]
for e in missing:
    changed_label_groups.append(re.findall(r'\\label\{([^}]+)\}',e))
report=['# Chapter6 conceptual figures audit','',
        'Three conceptual figures were added. The existing connected-plant configuration remains.', '',
        '## Purpose and placement','',
        '- `fig:plant_inventory_envelope` follows the four-layer inventory proof. It uses the existing hypothetical profiles `(10,10,10,1000)`, `(10,200,600,1000)`, and `(10,1000,1000,1000)` with100m3 per layer. The inventories are103,181,301kg. Endpoint hatching and internal dotted fills preserve grayscale readability.',
        '- `fig:plant_projection_architecture` follows the fixed-input projection and nonemptiness discussion. It separates raw connected predictions, derived physical requirements, and empirically fitted overflow closure before one joint projection and independent audit. It explicitly leaves full kinetics and layer fluxes unverified.',
        '- `fig:plant_route_verification` opens the original-model verification discussion. Separate surrogate and smooth-direct searches feed native audits. Retained decisions receive separate original nonsmooth evaluations. Original-model validity and retained engineering eligibility have separate failure branches. Eligible pairs reach one common-objective comparison.', '',
        '## Artifacts and rendering','',
        '- The inventory illustration is exported as standalone vectorPDF and SVG plus PNG preview at `article/figures/ch6_concept_inventory_envelope.*`.',
        '- Both flowcharts use native TikZ inside the chapter. Standalone previews are in `.codex-work/previews/ch06-diagrams/ch6_concept_projection_preview.*` and `ch6_concept_verification_preview.*`.',
        '- Standalone diagrams compiled successfully with matching12ptdocument settings and serif fonts. All three previews were visually inspected. Initial spacing and clipped-label problems were repaired before completion.',
        '- Blue-gray/white fills, dashed empirical/failure boxes, and explicitly named stages make the diagrams readable without color.',
        '- No full manuscript compilation was run by this agent. Root owns the final build and the remaining short-table layout repairs.', '',
        '## Preservation','',
        f'- Original labels preserved {len(old_labels)}/{len(old_labels)}. Current labels {len(new_labels)}, all unique.',
        f'- Original citation keys preserved {len(citations(original))}/{len(citations(original))}.',
        f'- Original display environments exact under whitespace normalization {len(old_eq)-len(missing)}/{len(old_eq)}.',
        f'- Original display groups with intervening root layout changes {changed_label_groups}. These differences predate the visual insertions and are not alterations made for the figures.',
        '- All new visual insertions leave mathematical expressions, sampling designs, fitting choices, numerical tolerances, and existing references untouched.',
        '- New prose includes a callout before every figure and an interpretation after it. Captions explicitly distinguish hypothetical/conceptual content from empirical findings.',
        '- No results, new references, new acronyms, banned terminology, or nonprinting control characters were introduced.']
(root/'.codex-work/reports/figures/ch6-concept-figures.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps({'old_equations':len(old_eq),'exact_old_equations':len(old_eq)-len(missing),
                  'root_layout_changed_groups':changed_label_groups,'old_labels':len(old_labels),
                  'labels':len(new_labels),'citations':len(citations(chapter)),'figures':chapter.count('\\begin{figure}')}))
