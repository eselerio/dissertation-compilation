import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

root=Path(__file__).resolve().parents[3]
backup=root/'.codex-work/snapshots/before-math-expansion'
chapters=sorted((root/'article/chapters').glob('*.tex'))

def displays(text):
    result={}
    for m in re.finditer(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}',text,re.S):
        for label in re.findall(r'\\label\{([^}]+)\}',m[2]):
            result[label]=re.sub(r'\s+','',m[0])
    return result

def citation_set(text):
    return {k.strip() for m in re.findall(r'\\cite\w*\{([^}]+)\}',text) for k in m.split(',')}

coverage=[]
for path in chapters:
    original=(backup/'chapters'/path.name).read_text(encoding='utf8')
    current=path.read_text(encoding='utf8')
    old_disp,new_disp=displays(original),displays(current)
    removed=sorted(set(old_disp)-set(new_disp))
    changed=sorted(k for k in old_disp if k in new_disp and old_disp[k]!=new_disp[k])
    lost_citations=sorted(citation_set(original)-citation_set(current))
    coverage.append({'chapter':path.name,'original_labeled_formulas':len(old_disp),'current_labeled_formulas':len(new_disp),'removed_formulas':removed,'changed_original_formula_blocks':changed,'lost_citation_keys':lost_citations,'characters_before':len(original),'characters_after':len(current)})

# Independent arithmetic checks for the root-authored examples.
checks={}
checks['two_component_prediction_errors']=(2**2+(-1)**2==5 and 1**2+(-1)**2==2)
checks['clipping_inventory']=(11-1==10 and 11+0==11 and 10+0==10)
for a in (0,2,11,13):
    first=Fraction(4)+a-(3*a-3)/Fraction(2)
    second=Fraction(3)+2*a-(3*a-3)/Fraction(2)
    assert first+second==10
    assert first==Fraction(11,2)-Fraction(a,2)
    assert second==Fraction(9,2)+Fraction(a,2)
checks['affine_response_and_slopes']=True
checks['coordinate_normalization']=(Fraction(15-10,30-10)==Fraction(1,4) and 10+Fraction(3,4)*(30-10)==25)
checks['latin_stratum']=(Fraction(2)+Fraction(3,5))/4==Fraction(13,20) and 10+Fraction(13,20)*10==Fraction(33,2)
checks['jitter_endpoints']=(2**64-1)//2**11==2**53-1
checks['log_state_step']=math.isclose(2*math.exp(-0.1),1.809674836071919)
checks['horizon_cases']=[max(400,50/max(w,0.001)) for w in (0.01,0.20,0)]==[5000,400,50000]
residual_terms=[Fraction(100),Fraction(-60),Fraction('-39.99999')]
checks['balance_residual']=abs(sum(residual_terms))/max(Fraction(1),*map(abs,residual_terms))==Fraction(1,10**7)
scores=[Fraction('.40'),Fraction('.42'),Fraction('.38'),Fraction('.41'),Fraction('.39')]
mean=sum(scores)/5
sq=sum((x-mean)**2 for x in scores)
std=math.sqrt(float(sq/4))
se=std/math.sqrt(5)
checks['one_standard_error_rule']=mean==Fraction(2,5) and sq==Fraction(1,1000) and 0.406<float(mean)+se<0.430
checks['error_metrics']=Fraction(1+4,2)==Fraction(5,2) and Fraction(1+2,2)==Fraction(3,2) and Fraction(1-2,2)==Fraction(-1,2) and 1-Fraction(5,8)==Fraction(3,8)
checks['two_normalization_metrics']=math.isclose(math.sqrt(0.625),0.7905694150420949) and math.isclose(math.sqrt((0.25**2+0.5**2)/2),0.39528470752104744)
checks['multistart_and_poll_counts']=(1+2*7==15 and 4*math.comb(7,2)==84 and 14+84+8==106)
checks['feasible_diagonal_poll']=math.isclose((0.5-0.1/math.sqrt(2))+(0.5+0.1/math.sqrt(2)),1) and 0.5-0.1/math.sqrt(2)<0.5
checks['route_quality_scales']=(Fraction('.8')/1+Fraction(4)/2)/2==Fraction('1.4') and (Fraction('.8')/Fraction('.5')+Fraction(4)/2)/2==Fraction('1.8')
checks['objective_differences']=Fraction('.90')-Fraction('1.10')==Fraction('-.20') and Fraction('.95')-Fraction('.98')==Fraction('-.03') and Fraction('1.10')-Fraction('.98')==Fraction('.12')
checks['percentage_points_and_relative_error']=100*(1-Fraction(2,200))==99 and 100*(1-Fraction(4,200))==98 and 100*Fraction(4-2,2)==100
checks['normalized_control_difference']=math.isclose(math.sqrt(0.25**2/7),0.0944911182523068)
checks['cost_amortization']=(100+20*3==160 and 20*6==120 and 100+50*3==250 and 50*6==300 and 100+34*3<34*6 and 100+33*3>33*6)
assert all(checks.values()),checks

title_pat=r'\\newcommand\{\\thesisTitle\}\{([^}]+)\}'
title_unchanged=re.search(title_pat,(root/'article/manuscript.tex').read_text(encoding='utf8'))[1]==re.search(title_pat,(backup/'manuscript.tex').read_text(encoding='utf8'))[1]
bibliography_unchanged=hashlib.sha256((root/'article/references.bib').read_bytes()).digest()==hashlib.sha256((backup/'references.bib').read_bytes()).digest()
out={'title_unchanged':title_unchanged,'bibliography_unchanged':bibliography_unchanged,'chapter_coverage':coverage,'root_example_arithmetic':checks}
(root/'.codex-work/reports/mathematics/math-expansion-audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
